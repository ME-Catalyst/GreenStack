"""
Re-run PQA analysis for Device #56 to capture detailed logging
"""

import sqlite3
import logging
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType

# Configure logging to see all INFO messages
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

def main():
    print("=" * 80)
    print("Re-running PQA Analysis for Device #56")
    print("=" * 80)

    # Get the XML content for Device #56
    conn = sqlite3.connect("greenstack.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT file_content FROM iodd_assets
        WHERE device_id = 56 AND file_type = 'xml'
        LIMIT 1
    """)

    xml_row = cursor.fetchone()

    if not xml_row:
        print("ERROR: Could not find XML content for Device #56")
        conn.close()
        return

    xml_content = xml_row[0]
    if isinstance(xml_content, bytes):
        xml_content = xml_content.decode('utf-8')

    conn.close()

    print(f"\nFound XML content ({len(xml_content)} chars)")
    print("\nStarting analysis with detailed logging...\n")

    # Run the analysis
    orchestrator = UnifiedPQAOrchestrator()

    try:
        metrics, diff_items = orchestrator.run_full_analysis(56, FileType.IODD, xml_content)

        print("\n" + "=" * 80)
        print("Analysis Complete")
        print("=" * 80)
        print(f"Overall Score: {metrics.overall_score:.2f}%")
        print(f"Critical Data Loss: {metrics.critical_data_loss}")
        print(f"Total Diff Items: {len(diff_items)}")

        # Check if ticket was created
        conn = sqlite3.connect("greenstack.db")
        cursor = conn.cursor()
        cursor.execute("""
            SELECT id, title, status, priority
            FROM tickets
            WHERE device_id = 56
            ORDER BY created_at DESC
            LIMIT 1
        """)
        ticket = cursor.fetchone()
        conn.close()

        if ticket:
            print(f"\n✓ Ticket created: ID {ticket[0]} - {ticket[1]} [{ticket[2]}/{ticket[3]}]")
        else:
            print("\n✗ No ticket was created")

    except Exception as e:
        print(f"\nERROR during analysis: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
