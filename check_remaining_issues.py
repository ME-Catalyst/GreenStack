import sqlite3

conn = sqlite3.connect('greenstack.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get devices with <100% scores
cursor.execute('''
    SELECT device_id, overall_score, structural_score, attribute_score, value_score
    FROM pqa_quality_metrics
    WHERE overall_score < 100.0
    ORDER BY overall_score ASC
    LIMIT 20
''')

rows = cursor.fetchall()
print(f'Found {len(rows)} devices with <100% scores (showing top 20 worst):')
print()

for row in rows:
    cursor.execute('SELECT vendor_id, device_id as dev_id, product_name FROM devices WHERE id = ?', (row['device_id'],))
    dev = cursor.fetchone()
    print(f"Device {row['device_id']}: {dev['vendor_id']}/{dev['dev_id']} - {dev['product_name']}")
    print(f"  Overall: {row['overall_score']:.2f}%, Structural: {row['structural_score']:.2f}%, Attribute: {row['attribute_score']:.2f}%, Value: {row['value_score']:.2f}%")

    # Get detailed issues from pqa_diff_details
    cursor.execute('''
        SELECT issue_type, COUNT(*) as count
        FROM pqa_diff_details
        WHERE device_id = ?
        GROUP BY issue_type
        ORDER BY count DESC
    ''', (row['device_id'],))

    issues = cursor.fetchall()
    if issues:
        print(f"  Issues:")
        for issue in issues:
            print(f"    - {issue['issue_type']}: {issue['count']} occurrences")
    print()

conn.close()
