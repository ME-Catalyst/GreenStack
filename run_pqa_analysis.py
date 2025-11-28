"""
Run PQA analysis on all devices
"""
import sys
sys.path.insert(0, 'src')

import sqlite3
from utils.pqa_orchestrator import analyze_iodd_quality

# Get all devices
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()
cursor.execute('SELECT id, vendor_id, device_id, product_name FROM devices ORDER BY id')
devices = cursor.fetchall()
conn.close()

print(f'Running PQA analysis on {len(devices)} devices...')
print()

success_count = 0
failed_count = 0

for idx, (db_id, vendor_id, device_id, product_name) in enumerate(devices, 1):
    if idx % 100 == 0:
        print(f'[{idx}/{len(devices)}] Analyzing device {db_id}: {vendor_id}/{device_id} - {product_name[:50]}...')

    try:
        # Get original XML from archive
        conn = sqlite3.connect('greenstack.db')
        cursor = conn.cursor()
        cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = ? LIMIT 1', (db_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print(f'  [SKIP] No archive found for device {db_id}')
            continue

        xml_content = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]

        result = analyze_iodd_quality(db_id, xml_content)
        if result:
            success_count += 1
        else:
            failed_count += 1
    except Exception as e:
        print(f'  [ERROR] Device {db_id}: {e}')
        failed_count += 1

print()
print('=' * 70)
print('PQA Analysis Complete')
print('=' * 70)
print(f'Total devices: {len(devices)}')
print(f'Successfully analyzed: {success_count}')
print(f'Failed: {failed_count}')
