"""
Re-import all devices to apply PQA fixes

This script re-imports all devices from pqa_file_archive to apply:
1. SimpleDatatype@id fix (migration + parser updates)
2. SingleValue duplicate fix (parser fix from line 702)

Expected to eliminate:
- 547 "incorrect Name@textId" issues
- 541 "incorrect SingleValue@value" issues
"""
# -*- coding: utf-8 -*-
import sqlite3
import sys
import io
from typing import List, Tuple

# Set stdout to UTF-8
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

sys.path.insert(0, 'src')

from parsing import IODDParser
from storage import StorageManager

def get_all_devices() -> List[Tuple[int, int, int, str]]:
    """Get all devices from pqa_file_archive"""
    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()
    cursor.execute('''
        SELECT id, vendor_id, device_id, product_name
        FROM devices
        ORDER BY id
    ''')
    devices = cursor.fetchall()
    conn.close()
    return devices

def delete_device_data(device_id: int) -> None:
    """Force deletion of all device data to ensure fixes are applied"""
    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()

    # Get parameter IDs
    cursor.execute('SELECT id FROM parameters WHERE device_id = ?', (device_id,))
    param_ids = [row[0] for row in cursor.fetchall()]

    if param_ids:
        placeholders = ','.join('?' * len(param_ids))
        # Delete child tables first (FK cascade disabled)
        cursor.execute(f'DELETE FROM variable_record_item_info WHERE parameter_id IN ({placeholders})', param_ids)
        cursor.execute(f'DELETE FROM parameter_single_values WHERE parameter_id IN ({placeholders})', param_ids)
        cursor.execute(f'DELETE FROM record_item_single_values WHERE record_item_id IN (SELECT id FROM parameter_record_items WHERE parameter_id IN ({placeholders}))', param_ids)
        cursor.execute(f'DELETE FROM parameter_record_items WHERE parameter_id IN ({placeholders})', param_ids)
        cursor.execute('DELETE FROM parameters WHERE device_id = ?', (device_id,))

    # Delete other device tables
    cursor.execute('DELETE FROM events WHERE device_id = ?', (device_id,))
    cursor.execute('DELETE FROM process_data WHERE device_id = ?', (device_id,))

    # Get custom datatype IDs
    cursor.execute('SELECT id FROM custom_datatypes WHERE device_id = ?', (device_id,))
    dt_ids = [row[0] for row in cursor.fetchall()]

    if dt_ids:
        placeholders = ','.join('?' * len(dt_ids))
        cursor.execute(f'DELETE FROM custom_datatype_record_item_single_values WHERE record_item_id IN (SELECT id FROM custom_datatype_record_items WHERE datatype_id IN ({placeholders}))', dt_ids)
        cursor.execute(f'DELETE FROM custom_datatype_record_items WHERE datatype_id IN ({placeholders})', dt_ids)
        cursor.execute(f'DELETE FROM custom_datatype_single_values WHERE datatype_id IN ({placeholders})', dt_ids)
        cursor.execute('DELETE FROM custom_datatypes WHERE device_id = ?', (device_id,))

    # Delete text entries
    cursor.execute('DELETE FROM iodd_text WHERE device_id = ?', (device_id,))

    # Delete StdVariableRef data (PQA Fix: Was missing, causing stale data)
    cursor.execute('''
        DELETE FROM std_variable_ref_single_values
        WHERE std_variable_ref_id IN (SELECT id FROM std_variable_refs WHERE device_id = ?)
    ''', (device_id,))
    cursor.execute('''
        DELETE FROM std_variable_ref_value_ranges
        WHERE std_variable_ref_id IN (SELECT id FROM std_variable_refs WHERE device_id = ?)
    ''', (device_id,))
    cursor.execute('''
        DELETE FROM std_record_item_ref_single_values
        WHERE std_record_item_ref_id IN (
            SELECT id FROM std_record_item_refs
            WHERE std_variable_ref_id IN (SELECT id FROM std_variable_refs WHERE device_id = ?)
        )
    ''', (device_id,))
    cursor.execute('''
        DELETE FROM std_record_item_refs
        WHERE std_variable_ref_id IN (SELECT id FROM std_variable_refs WHERE device_id = ?)
    ''', (device_id,))
    cursor.execute('DELETE FROM std_variable_refs WHERE device_id = ?', (device_id,))

    # Set checksum to NULL to force StorageManager to re-import
    # (StorageManager skips import if checksum matches)
    cursor.execute('UPDATE devices SET checksum = NULL WHERE id = ?', (device_id,))

    conn.commit()
    conn.close()

def reimport_device(device_id: int) -> bool:
    """Re-import a single device from pqa_file_archive"""
    try:
        # Get IODD XML from archive
        conn = sqlite3.connect('greenstack.db')
        cursor = conn.cursor()
        cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = ? LIMIT 1', (device_id,))
        row = cursor.fetchone()
        conn.close()

        if not row:
            print(f'  [SKIP] No archive found for device {device_id}')
            return False

        xml_content = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]

        # Delete old data
        delete_device_data(device_id)

        # Parse IODD
        parser = IODDParser(xml_content)
        iodd_data = parser.parse()

        # Save to database
        storage = StorageManager('greenstack.db')
        saved_id = storage.save_device(iodd_data)

        if saved_id != device_id:
            print(f'  [WARN] Device ID changed: {device_id} -> {saved_id}')

        return True

    except Exception as e:
        print(f'  [ERROR] Failed to import device {device_id}: {e}')
        import traceback
        traceback.print_exc()
        return False

def main():
    print('=' * 70)
    print('Re-importing all devices to apply PQA fixes')
    print('=' * 70)
    print()
    print('Fixes being applied:')
    print('  1. SimpleDatatype@id fix (642 occurrences)')
    print('  2. SingleValue duplicate fix (547 + 541 occurrences)')
    print()

    # Get all devices
    devices = get_all_devices()
    print(f'Found {len(devices)} devices to re-import')
    print()

    success_count = 0
    failed_count = 0
    skipped_count = 0

    for idx, (db_id, vendor_id, iolink_device_id, product_name) in enumerate(devices, 1):
        print(f'[{idx}/{len(devices)}] Re-importing device {db_id}: {vendor_id}/{iolink_device_id} - {product_name}')

        result = reimport_device(db_id)

        if result is True:
            success_count += 1
            print(f'  [OK] Successfully re-imported')
        elif result is False:
            if 'SKIP' in str(result):
                skipped_count += 1
            else:
                failed_count += 1
        print()

    print('=' * 70)
    print('Re-import Summary')
    print('=' * 70)
    print(f'Total devices: {len(devices)}')
    print(f'Successfully re-imported: {success_count}')
    print(f'Failed: {failed_count}')
    print(f'Skipped: {skipped_count}')
    print()

    if failed_count == 0:
        print('[SUCCESS] All devices re-imported successfully!')
        print()
        print('Next step: Run PQA re-analysis to verify fixes')
        print('  python analyze_pqa_issues.py')
    else:
        print(f'[WARN] {failed_count} devices failed to re-import')
        print('Review errors above and retry failed devices')

if __name__ == '__main__':
    main()
