"""
Test script to verify SingleValue duplicate fix
"""
# -*- coding: utf-8 -*-
import sqlite3
import sys
import io

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'src')

from parsing import IODDParser
from storage import StorageManager

# Get the IODD XML for device 550
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()
cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = 550 LIMIT 1')
row = cursor.fetchone()
xml_content = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]
conn.close()

print('Re-importing device 550 with fixed parser...')

# Parse the IODD
parser = IODDParser(xml_content)
iodd_data = parser.parse()

# FORCE deletion of old data before saving
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()
cursor.execute('SELECT id FROM parameters WHERE device_id = 550')
param_ids = [row[0] for row in cursor.fetchall()]
if param_ids:
    placeholders = ','.join('?' * len(param_ids))
    cursor.execute(f'DELETE FROM parameter_single_values WHERE parameter_id IN ({placeholders})', param_ids)
    cursor.execute(f'DELETE FROM parameter_record_items WHERE parameter_id IN ({placeholders})', param_ids)
    cursor.execute('DELETE FROM parameters WHERE device_id = 550')
    conn.commit()
    print(f'[DEBUG] Deleted old data for {len(param_ids)} parameters')
conn.close()

# Store to database
storage = StorageManager('greenstack.db')
device_id = storage.save_device(iodd_data)

print(f'[OK] Successfully re-imported as device database ID: {device_id}')

# Check for duplicates
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

# Verify which device we're checking
cursor.execute('SELECT vendor_id, device_id as dev_id, product_name FROM devices WHERE id = ?', (device_id,))
dev_info = cursor.fetchone()
print(f'[INFO] Checking device: vendor={dev_info[0]}, device_id={dev_info[1]}, product={dev_info[2]}')

# Check record_item_single_values
cursor.execute('''
    SELECT risv.value, risv.name_text_id, COUNT(*) as cnt
    FROM record_item_single_values risv
    JOIN parameter_record_items ri ON risv.record_item_id = ri.id
    JOIN parameters p ON ri.parameter_id = p.id
    WHERE p.device_id = ? AND p.variable_id = 'V_Configuration' AND ri.subindex = 1
    GROUP BY risv.value
    ORDER BY risv.value
''', (device_id,))
rows = cursor.fetchall()
print(f'\n=== RecordItem subindex=1 SingleValues ===')
has_duplicates = False
for row in rows:
    if row[2] > 1:
        has_duplicates = True
        print(f'[FAIL] DUPLICATE: value={row[0]}, textId={row[1]}, count={row[2]}')
    else:
        print(f'[OK] value={row[0]}, textId={row[1]}, count={row[2]}')

# Check parameter_single_values
cursor.execute('''
    SELECT COUNT(*)
    FROM parameter_single_values psv
    JOIN parameters p ON psv.parameter_id = p.id
    WHERE p.device_id = ? AND p.variable_id = 'V_Configuration'
''', (device_id,))
param_sv_count = cursor.fetchone()[0]
print(f'\n=== Parameter SingleValues ===')
if param_sv_count == 0:
    print(f'[OK] V_Configuration has {param_sv_count} parameter-level SingleValues (expected 0)')
else:
    print(f'[FAIL] V_Configuration has {param_sv_count} parameter-level SingleValues (expected 0)')
    has_duplicates = True

conn.close()

if not has_duplicates and param_sv_count == 0:
    print('\n[SUCCESS] FIX VERIFIED: No duplicates found!')
else:
    print('\n[FAILED] FIX INCOMPLETE: Duplicates still exist')
    sys.exit(1)
