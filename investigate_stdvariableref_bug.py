"""
Investigate StdVariableRef ordering bug for device 5189

This script compares StdVariableRef elements in:
1. Original IODD XML from pqa_file_archive
2. Database std_variable_refs table
3. Reconstructed IODD XML

To identify if extra StdVariableRefs are being added during parsing.
"""
import sqlite3
import re
from xml.etree import ElementTree as ET

# Connect to database
conn = sqlite3.connect('greenstack.db')
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

# Get original IODD XML
cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = 5189 LIMIT 1')
row = cursor.fetchone()
xml_content = row['file_content'].decode('utf-8') if isinstance(row['file_content'], bytes) else row['file_content']

# Parse original XML to extract StdVariableRef elements
print('=' * 80)
print('ORIGINAL IODD XML - StdVariableRef Analysis')
print('=' * 80)
print()

# Extract all StdVariableRef elements from original XML
original_refs = []
root = ET.fromstring(xml_content)

# Define namespaces
namespaces = {
    'iodd': 'http://www.io-link.com/IODD/2009/11',
    'xsi': 'http://www.w3.org/2001/XMLSchema-instance'
}

# Try both namespace versions
if 'IODD/2009/11' not in xml_content:
    namespaces['iodd'] = 'http://www.io-link.com/IODD/2010/10'

# Find VariableCollection
var_collection = root.find('.//iodd:VariableCollection', namespaces)
if var_collection is not None:
    for idx, std_ref in enumerate(var_collection.findall('iodd:StdVariableRef', namespaces)):
        var_id = std_ref.get('id')
        if var_id:
            original_refs.append((idx, var_id))

print(f'Found {len(original_refs)} StdVariableRef elements in original IODD:')
for idx, var_id in original_refs[:20]:
    print(f'  {idx+1:2d}. {var_id}')
print()

# Get database StdVariableRefs
print('=' * 80)
print('DATABASE std_variable_refs TABLE')
print('=' * 80)
print()

cursor.execute('''
    SELECT variable_id, order_index
    FROM std_variable_refs
    WHERE device_id = 5189
    ORDER BY order_index
''')
db_refs = cursor.fetchall()

print(f'Found {len(db_refs)} StdVariableRef entries in database:')
for idx, row in enumerate(db_refs[:20]):
    print(f'  {idx+1:2d}. {row["variable_id"]} (order_index={row["order_index"]})')
print()

# Compare original vs database
print('=' * 80)
print('COMPARISON: Original IODD vs Database')
print('=' * 80)
print()

original_ids = [var_id for _, var_id in original_refs]
db_ids = [row['variable_id'] for row in db_refs]

# Find extras in database
extras_in_db = [var_id for var_id in db_ids if var_id not in original_ids]
if extras_in_db:
    print(f'FOUND {len(extras_in_db)} EXTRA StdVariableRefs in DATABASE (not in original):')
    for var_id in extras_in_db:
        db_idx = db_ids.index(var_id)
        print(f'  - {var_id} at position {db_idx+1}')
    print()
else:
    print('[OK] No extra StdVariableRefs in database')
    print()

# Find missing in database
missing_in_db = [var_id for var_id in original_ids if var_id not in db_ids]
if missing_in_db:
    print(f'FOUND {len(missing_in_db)} MISSING StdVariableRefs in database (present in original):')
    for var_id in missing_in_db:
        orig_idx = original_ids.index(var_id)
        print(f'  - {var_id} at position {orig_idx+1} in original')
    print()
else:
    print('[OK] No missing StdVariableRefs in database')
    print()

# Check if order matches
if original_ids == db_ids:
    print('[OK] Order matches exactly!')
else:
    print('[ERROR] Order mismatch detected!')
    print()
    print('Side-by-side comparison (first 20):')
    print(f'{"Original":<30} | {"Database":<30}')
    print('-' * 65)
    for i in range(min(20, max(len(original_ids), len(db_ids)))):
        orig = original_ids[i] if i < len(original_ids) else '(none)'
        db = db_ids[i] if i < len(db_ids) else '(none)'
        match = '✓' if orig == db else '✗'
        print(f'{orig:<30} | {db:<30} {match}')

conn.close()
