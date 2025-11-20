"""
Debug script to test PQA ticket generation
"""
import logging
import sqlite3
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType

# Set up detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# Get device 1's XML content
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT file_content FROM iodd_assets
    WHERE device_id = 1 AND file_type = 'xml'
    LIMIT 1
""")
row = cursor.fetchone()

if not row:
    print("ERROR: No XML content found for device 1")
    exit(1)

xml_content = row[0]
if isinstance(xml_content, bytes):
    xml_content = xml_content.decode('utf-8')

print(f"Found XML content: {len(xml_content)} chars")

# Check current tickets
cursor.execute("SELECT COUNT(*) FROM tickets WHERE category = 'parser_quality'")
before_count = cursor.fetchone()[0]
print(f"Parser quality tickets BEFORE: {before_count}")

conn.close()

# Run PQA analysis
print("\n" + "="*80)
print("Running PQA analysis...")
print("="*80 + "\n")

try:
    orchestrator = UnifiedPQAOrchestrator("greenstack.db")
    metrics, diff_items = orchestrator.run_full_analysis(1, FileType.IODD, xml_content)

    print("\n" + "="*80)
    print("Analysis complete!")
    print("="*80)
    print(f"Overall Score: {metrics.overall_score:.1f}%")
    print(f"Critical Data Loss: {metrics.critical_data_loss}")
    print(f"Passed Threshold: {metrics.overall_score >= 95.0}")

    # Check tickets after
    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM tickets WHERE category = 'parser_quality'")
    after_count = cursor.fetchone()[0]
    print(f"\nParser quality tickets AFTER: {after_count}")

    cursor.execute("""
        SELECT ticket_number, title, status, priority
        FROM tickets
        WHERE category = 'parser_quality'
        ORDER BY created_at DESC
        LIMIT 3
    """)
    tickets = cursor.fetchall()

    if tickets:
        print("\nRecent parser quality tickets:")
        for t in tickets:
            print(f"  - {t[0]}: {t[1]} [{t[2]}] ({t[3]})")
    else:
        print("\nNO PARSER QUALITY TICKETS FOUND!")

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

except Exception as e:
    logger.error(f"Analysis failed: {e}", exc_info=True)
    print(f"\nERROR: {e}")
