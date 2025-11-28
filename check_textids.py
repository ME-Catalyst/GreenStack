import sqlite3

conn = sqlite3.connect('greenstack.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute('''
    SELECT risv.value, risv.name_text_id
    FROM record_item_single_values risv
    JOIN parameter_record_items ri ON risv.record_item_id = ri.id
    JOIN parameters p ON ri.parameter_id = p.id
    WHERE p.device_id = 550 AND p.variable_id = "V_Configuration" AND ri.subindex = 1
    ORDER BY risv.id LIMIT 10
''')

rows = cursor.fetchall()
print(f"Found {len(rows)} SingleValues:")
for row in rows:
    print(f"  value={row['value']}, textId={row['name_text_id']}")

conn.close()
