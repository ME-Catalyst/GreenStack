"""
Test the ArrayT SingleValue parser fix on device 130
"""
import sys
sys.path.insert(0, 'src')

import sqlite3
from parsing import IODDParser

# Get original IODD XML from archive
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

device_id = 130

cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = ? LIMIT 1', (device_id,))
row = cursor.fetchone()
xml_content = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]

conn.close()

print(f'Testing parser fix on device {device_id}...')
print()

# Parse with updated parser
parser = IODDParser(xml_content)
iodd_data = parser.parse()

# Find V_ParaConfigFaultCollection parameter
target_param = None
for param in iodd_data.parameters:
    if param.id == 'V_ParaConfigFaultCollection':
        target_param = param
        break

if not target_param:
    print('[ERROR] V_ParaConfigFaultCollection not found in parsed data!')
    sys.exit(1)

print(f'Found Parameter:')
print(f'  ID: {target_param.id}')
print(f'  Name: {target_param.name}')
print(f'  Data Type: {target_param.data_type}')
print()

# Check SingleValues
if hasattr(target_param, 'single_values') and target_param.single_values:
    print(f'[SUCCESS] Parser extracted {len(target_param.single_values)} SingleValues!')
    print()
    print('First 5 SingleValues:')
    for i, sv in enumerate(target_param.single_values[:5]):
        print(f'  {i+1}. value={sv.value}, text_id={sv.text_id}')
    print()
    print(f'Total: {len(target_param.single_values)} (expected 25)')
    if len(target_param.single_values) == 25:
        print()
        print('[PERFECT] Extracted all 25 SingleValues correctly!')
    else:
        print()
        print(f'[WARN] Expected 25 SingleValues, got {len(target_param.single_values)}')
else:
    print('[FAILED] No SingleValues extracted!')
    print('The fix did not work.')
