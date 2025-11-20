"""Diagnose Text ID mismatch issue for Device #56"""
import sqlite3

conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

print('=== Comparing Expected vs Stored Text IDs ===\n')

# Get some mismatches from diff details
cursor.execute("""
    SELECT expected_value, actual_value FROM pqa_diff_details
    WHERE metric_id = 4
    AND diff_type = 'incorrect_attribute'
    AND xpath LIKE '%Text@id'
    LIMIT 10
""")

mismatches = cursor.fetchall()

for expected_id, actual_id in mismatches:
    print(f'Expected ID (Original XML): {expected_id}')
    print(f'Actual ID (Reconstructed):   {actual_id}')

    # Check if expected ID exists in database
    cursor.execute("""
        SELECT text_value FROM iodd_text
        WHERE device_id = 56 AND text_id = ?
    """, (expected_id,))
    expected_row = cursor.fetchone()

    # Check if actual ID exists in database
    cursor.execute("""
        SELECT text_value FROM iodd_text
        WHERE device_id = 56 AND text_id = ?
    """, (actual_id,))
    actual_row = cursor.fetchone()

    if expected_row:
        print(f'Expected ID IN database: YES - "{expected_row[0][:60]}..."')
    else:
        print(f'Expected ID IN database: NO')

    if actual_row:
        print(f'Actual ID IN database:   YES - "{actual_row[0][:60]}..."')
    else:
        print(f'Actual ID IN database:   NO')

    print()

conn.close()
