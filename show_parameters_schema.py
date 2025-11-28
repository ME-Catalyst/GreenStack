"""
Show actual parameters table schema
"""
import sqlite3

conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

# Get table schema
cursor.execute("PRAGMA table_info(parameters)")
columns = cursor.fetchall()

print('parameters table columns:')
for col in columns:
    print(f'  {col[1]} ({col[2]})')

print()

# Show all parameters for device 130
cursor.execute('SELECT * FROM parameters WHERE device_id = 130 LIMIT 5')
cursor.row_factory = sqlite3.Row
cursor = conn.cursor()
cursor.execute('SELECT * FROM parameters WHERE device_id = 130 LIMIT 1')
row = cursor.fetchone()

if row:
    print('Sample row columns:')
    for key in row.keys():
        print(f'  {key}')

conn.close()
