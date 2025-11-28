"""
Test current parser's StdVariableRef extraction for device 5189
"""
import sys
sys.path.insert(0, 'src')

import sqlite3
from parsing import IODDParser

# Get original IODD XML from archive
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()
cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = 5189 LIMIT 1')
row = cursor.fetchone()
xml_content = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]
conn.close()

print('Testing current parser on device 5189 IODD XML...')
print()

# Parse with current parser
parser = IODDParser(xml_content)
iodd_data = parser.parse()

# Check extracted StdVariableRefs
std_refs = getattr(iodd_data, 'std_variable_refs', [])

print(f'Parser extracted {len(std_refs)} StdVariableRefs:')
for i, ref in enumerate(std_refs):
    print(f'  {i+1:2d}. {ref.variable_id} (order_index={ref.order_index})')

print()
print('Expected from original XML (12 total):')
expected = [
    'V_DirectParameters_1',
    'V_DirectParameters_2',
    'V_SystemCommand',
    'V_VendorName',
    'V_VendorText',
    'V_ProductName',
    'V_ProductID',
    'V_HardwareRevision',
    'V_FirmwareRevision',
    'V_ApplicationSpecificName',
    'V_ProcessDataOut',
    'V_ProcessDataIn',
]
for i, var_id in enumerate(expected):
    print(f'  {i+1:2d}. {var_id}')

print()

# Compare
parsed_ids = [ref.variable_id for ref in std_refs]
if parsed_ids == expected:
    print('[SUCCESS] Parser correctly extracts StdVariableRefs!')
else:
    print('[FAIL] Parser extraction mismatch!')
    print()
    print('Differences:')
    extras = [v for v in parsed_ids if v not in expected]
    missing = [v for v in expected if v not in parsed_ids]
    renamed = []

    if extras:
        print(f'  EXTRA in parsed (not in original): {extras}')
    if missing:
        print(f'  MISSING from parsed (in original): {missing}')

    # Check for potential renames
    if len(extras) == len(missing):
        print(f'  POSSIBLE RENAMES:')
        for i in range(len(extras)):
            print(f'    {missing[i]} → {extras[i]} ?')
