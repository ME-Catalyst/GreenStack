"""
Test PQA ticket auto-generation with enhanced logging
"""
import logging
import sqlite3
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType

# Set up detailed logging to console
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('pqa_ticket_test.log', mode='w')
    ]
)

logger = logging.getLogger(__name__)

print("="*80)
print("PQA TICKET AUTO-GENERATION TEST")
print("="*80)
print()

# Get device 1's XML content from archive ID 89 (the one that scored 91.53%)
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT file_content FROM pqa_file_archive
    WHERE id = 89
""")
row = cursor.fetchone()

if not row:
    print("ERROR: Archive ID 89 not found!")
    exit(1)

xml_content = row[0]
if isinstance(xml_content, bytes):
    xml_content = xml_content.decode('utf-8')

print(f"[OK] Retrieved XML content from archive 89: {len(xml_content)} bytes")

# Check current state
cursor.execute("SELECT COUNT(*) FROM tickets WHERE category = 'parser_quality'")
tickets_before = cursor.fetchone()[0]
print(f"[OK] Parser quality tickets BEFORE test: {tickets_before}")

# Check threshold
cursor.execute("SELECT min_overall_score, auto_ticket_on_fail FROM pqa_thresholds WHERE active = 1")
threshold = cursor.fetchone()
print(f"[OK] Active threshold: min_score={threshold[0]}, auto_ticket={threshold[1]}")

conn.close()

print()
print("="*80)
print("RUNNING PQA ANALYSIS...")
print("="*80)
print()

# Run PQA analysis
try:
    orchestrator = UnifiedPQAOrchestrator("greenstack.db")
    metrics, diff_items = orchestrator.run_full_analysis(1, FileType.IODD, xml_content)

    print()
    print("="*80)
    print("ANALYSIS COMPLETE")
    print("="*80)
    print(f"Overall Score: {metrics.overall_score:.2f}%")
    print(f"Critical Data Loss: {metrics.critical_data_loss}")
    print(f"Threshold ({threshold[0]}%): {'PASS' if metrics.overall_score >= threshold[0] else 'FAIL'}")
    print(f"Should Generate Ticket: {metrics.overall_score < threshold[0] or metrics.critical_data_loss}")

    # Check tickets after
    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE category = 'parser_quality'")
    tickets_after = cursor.fetchone()[0]
    print(f"\nParser quality tickets AFTER test: {tickets_after}")

    if tickets_after > tickets_before:
        print(f"[SUCCESS] {tickets_after - tickets_before} ticket(s) created!")

        cursor.execute("""
            SELECT ticket_number, title, status, priority, device_id
            FROM tickets
            WHERE category = 'parser_quality'
            ORDER BY created_at DESC
            LIMIT 1
        """)
        ticket = cursor.fetchone()
        print(f"\nNewest ticket:")
        print(f"  Number: {ticket[0]}")
        print(f"  Title: {ticket[1]}")
        print(f"  Status: {ticket[2]}")
        print(f"  Priority: {ticket[3]}")
        print(f"  Device ID: {ticket[4]}")
    else:
        print(f"[FAILURE] No tickets were created!")

    # Check the metric entry
    cursor.execute("""
        SELECT id, ticket_generated
        FROM pqa_quality_metrics
        WHERE device_id = 1
        ORDER BY analysis_timestamp DESC
        LIMIT 1
    """)
    metric_row = cursor.fetchone()
    if metric_row:
        print(f"\nLatest metric ID: {metric_row[0]}, ticket_generated: {metric_row[1]}")

    conn.close()

    print()
    print("="*80)
    print(f"Detailed logs saved to: pqa_ticket_test.log")
    print("="*80)

except Exception as e:
    logger.error(f"Test failed: {e}", exc_info=True)
    print(f"\n[ERROR] {e}")
