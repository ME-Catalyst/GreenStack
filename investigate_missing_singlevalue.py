"""
Investigate missing SingleValue elements in Variable definitions for device 130
"""
import sys
sys.path.insert(0, 'src')

import sqlite3
from xml.etree import ElementTree as ET
from utils.forensic_reconstruction_v2 import reconstruct_iodd_xml

# Get original IODD XML from archive
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

device_id = 130

cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = ? LIMIT 1', (device_id,))
row = cursor.fetchone()
original_xml = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]

conn.close()

# Generate reconstructed IODD XML
print('Reconstructing IODD XML from database...')
reconstructed_xml = reconstruct_iodd_xml(device_id)
print('Reconstruction complete.')

# Parse both XMLs
original_root = ET.fromstring(original_xml)
reconstructed_root = ET.fromstring(reconstructed_xml)

# Define namespaces
ns = {'iodd': 'http://www.io-link.com/IODD/2010/10'}

# Find Variable elements in original
print('=' * 100)
print('ORIGINAL IODD - Variable Elements with SimpleDatatype/SingleValue:')
print('=' * 100)

original_vars = original_root.findall('.//iodd:VariableCollection/iodd:Variable', ns)
for idx, var in enumerate(original_vars[:5]):  # Check first 5
    var_id = var.get('id')
    print(f'\nVariable {idx+1}: id={var_id}')

    # Check for SimpleDatatype
    simple_dt = var.find('.//iodd:SimpleDatatype', ns)
    if simple_dt:
        print(f'  Has SimpleDatatype:')
        print(f'    type: {simple_dt.get("type")}')
        print(f'    bitLength: {simple_dt.get("bitLength")}')

        # Check for SingleValue children
        single_values = simple_dt.findall('iodd:SingleValue', ns)
        print(f'    SingleValue count: {len(single_values)}')
        for sv_idx, sv in enumerate(single_values[:3]):
            print(f'      {sv_idx+1}. value={sv.get("value")}')

print()
print('=' * 100)
print('RECONSTRUCTED IODD - Variable Elements with SimpleDatatype/SingleValue:')
print('=' * 100)

recon_vars = reconstructed_root.findall('.//iodd:VariableCollection/iodd:Variable', ns)
for idx, var in enumerate(recon_vars[:5]):  # Check first 5
    var_id = var.get('id')
    print(f'\nVariable {idx+1}: id={var_id}')

    # Check for SimpleDatatype
    simple_dt = var.find('.//iodd:SimpleDatatype', ns)
    if simple_dt:
        print(f'  Has SimpleDatatype:')
        print(f'    type: {simple_dt.get("type")}')
        print(f'    bitLength: {simple_dt.get("bitLength")}')

        # Check for SingleValue children
        single_values = simple_dt.findall('iodd:SingleValue', ns)
        print(f'    SingleValue count: {len(single_values)}')
        for sv_idx, sv in enumerate(single_values[:3]):
            print(f'      {sv_idx+1}. value={sv.get("value")}')

print()
print('=' * 100)
print('SEARCHING FOR VARIABLES WITH SIMPLEDATATYPE AND SINGLEVALUE')
print('=' * 100)

# Find Variables with SimpleDatatype and SingleValue in original
print('\nOriginal IODD:')
found_count = 0
for var in original_vars:
    var_id = var.get('id')
    simple_dt = var.find('.//iodd:SimpleDatatype', ns)
    if simple_dt:
        single_values = simple_dt.findall('iodd:SingleValue', ns)
        if len(single_values) > 0:
            found_count += 1
            if found_count <= 3:  # Show first 3
                print(f'\nVariable: id={var_id}')
                print(f'  SimpleDatatype type={simple_dt.get("type")}, bitLength={simple_dt.get("bitLength")}')
                print(f'  SingleValues: {len(single_values)}')
                for sv_idx, sv in enumerate(single_values[:3]):
                    print(f'    {sv_idx+1}. value={sv.get("value")}')

print(f'\nTotal Variables with SimpleDatatype+SingleValue in original: {found_count}')

# Find Variables with SimpleDatatype and SingleValue in reconstructed
print('\nReconstructed IODD:')
found_count_recon = 0
for var in recon_vars:
    var_id = var.get('id')
    simple_dt = var.find('.//iodd:SimpleDatatype', ns)
    if simple_dt:
        single_values = simple_dt.findall('iodd:SingleValue', ns)
        if len(single_values) > 0:
            found_count_recon += 1
            if found_count_recon <= 3:  # Show first 3
                print(f'\nVariable: id={var_id}')
                print(f'  SimpleDatatype type={simple_dt.get("type")}, bitLength={simple_dt.get("bitLength")}')
                print(f'  SingleValues: {len(single_values)}')
                for sv_idx, sv in enumerate(single_values[:3]):
                    print(f'    {sv_idx+1}. value={sv.get("value")}')

print(f'\nTotal Variables with SimpleDatatype+SingleValue in reconstructed: {found_count_recon}')

print()
print('=' * 100)
print('ISSUE SUMMARY')
print('=' * 100)
print(f'Original has {found_count} Variables with SimpleDatatype+SingleValue')
print(f'Reconstructed has {found_count_recon} Variables with SimpleDatatype+SingleValue')
print(f'Missing: {found_count - found_count_recon}')
