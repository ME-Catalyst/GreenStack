"""
Check if SingleValues are stored in database for V_ParaConfigFaultCollection
"""
import sys
sys.path.insert(0, 'src')

import sqlite3

conn = sqlite3.connect('greenstack.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

device_id = 130

# Find the parameter for V_ParaConfigFaultCollection
cursor.execute('''
    SELECT id, variable_id, name, data_type, bit_length
    FROM parameters
    WHERE device_id = ? AND variable_id = 'V_ParaConfigFaultCollection'
''', (device_id,))

param = cursor.fetchone()

if not param:
    print(f'[ERROR] V_ParaConfigFaultCollection not found in parameters table for device {device_id}')
    conn.close()
    sys.exit(1)

print(f'Found Parameter:')
print(f'  ID: {param["id"]}')
print(f'  Variable ID: {param["variable_id"]}')
print(f'  Name: {param["name"]}')
print(f'  DataType: {param["data_type"]}')
print(f'  BitLength: {param["bit_length"]}')
print()

# Check parameter_single_values table
cursor.execute('''
    SELECT COUNT(*) as count
    FROM parameter_single_values
    WHERE parameter_id = ?
''', (param['id'],))

count = cursor.fetchone()['count']

print(f'SingleValues in parameter_single_values table: {count}')
print()

if count > 0:
    print('[SUCCESS] SingleValues ARE stored in database!')
    print()
    print('First 5 SingleValues:')
    cursor.execute('''
        SELECT value, text_id, xsi_type, order_index
        FROM parameter_single_values
        WHERE parameter_id = ?
        ORDER BY order_index
        LIMIT 5
    ''', (param['id'],))

    for row in cursor.fetchall():
        print(f'  value={row["value"]}, text_id={row["text_id"]}, order_index={row["order_index"]}')
else:
    print('[PROBLEM] No SingleValues found in database!')
    print('This explains why reconstruction is missing them.')
    print()
    print('The issue is in the PARSER - it is not extracting SingleValues from Variable elements.')

conn.close()
