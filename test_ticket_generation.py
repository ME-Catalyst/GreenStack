"""
Test script to verify ticket generation logic for Device #56

This script tests the PQA orchestrator's ticket generation for a device
that failed quality analysis (88.32% score, below 95% threshold).
"""

import sqlite3
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType

def test_ticket_should_generate():
    """Test if ticket should be generated for Device #56"""
    orchestrator = UnifiedPQAOrchestrator()

    # Create a mock metrics object with Device #56's actual scores
    class MockMetrics:
        overall_score = 88.32
        critical_data_loss = False

    metrics = MockMetrics()

    should_generate = orchestrator._should_generate_ticket(metrics)
    print(f"Should generate ticket: {should_generate}")
    print(f"  - Score: {metrics.overall_score}%")
    print(f"  - Critical loss: {metrics.critical_data_loss}")

    # Check threshold config
    conn = sqlite3.connect("greenstack.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT threshold_name, min_overall_score, auto_ticket_on_fail, active
        FROM pqa_thresholds WHERE active = 1
    """)
    threshold = cursor.fetchone()
    conn.close()

    if threshold:
        print(f"\nThreshold Configuration:")
        print(f"  - Name: {threshold[0]}")
        print(f"  - Min Score: {threshold[1]}%")
        print(f"  - Auto Ticket: {threshold[2]}")
        print(f"  - Active: {threshold[3]}")
        print(f"\nExpected: ticket SHOULD be generated (88.32% < {threshold[1]}%)")
    else:
        print("\nNo active threshold found!")

def check_existing_tickets():
    """Check if any tickets exist for Device #56"""
    conn = sqlite3.connect("greenstack.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT id, title, status, priority, created_at
        FROM tickets
        WHERE device_id = 56 OR title LIKE '%56%'
    """)
    tickets = cursor.fetchall()
    conn.close()

    print(f"\n\nExisting tickets for Device #56: {len(tickets)}")
    for ticket in tickets:
        print(f"  - ID {ticket[0]}: {ticket[1]} [{ticket[2]}/{ticket[3]}] - {ticket[4]}")

if __name__ == "__main__":
    print("=" * 60)
    print("PQA Ticket Generation Test - Device #56")
    print("=" * 60)

    test_ticket_should_generate()
    check_existing_tickets()

    print("\n" + "=" * 60)
