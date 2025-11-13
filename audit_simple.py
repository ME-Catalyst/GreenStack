"""Simple audit - compare one EDS file."""

import zipfile
import sqlite3
from eds_parser import parse_eds_file

# Extract the EDS file from the package
package_file = 'test-data/eds-packages/54611_MVK_PRO_KF5_x_19.zip'
eds_path = '01_EDS/V1.8/01_ODVA_Certified/54611_MVK_Pro_ME_DIO8_IOL8_5P.eds'

print("="*80)
print("PARSING SOURCE FILE")
print("="*80)

with zipfile.ZipFile(package_file, 'r') as zf:
    eds_content = zf.read(eds_path).decode('utf-8', errors='ignore')
    parsed_data, diagnostics = parse_eds_file(eds_content, eds_path)

print(f"\nSource File Parsed Data:")
print(f"  Product: {parsed_data['device'].get('product_name')}")
print(f"  Vendor: {parsed_data['device'].get('vendor_name')}")
print(f"  Catalog: {parsed_data['device'].get('catalog_number')}")
print(f"  Parameters: {len(parsed_data.get('parameters', []))}")
print(f"  Connections: {len(parsed_data.get('connections', []))}")
print(f"  Ports: {len(parsed_data.get('ports', []))}")

capacity = parsed_data.get('capacity', {})
print(f"  Capacity:")
print(f"    max_msg_connections: {capacity.get('max_msg_connections')}")
print(f"    max_io_producers: {capacity.get('max_io_producers')}")
print(f"    max_io_consumers: {capacity.get('max_io_consumers')}")
print(f"    TSpecs: {len(capacity.get('tspecs', []))}")

# Print first few parameters
print(f"\n  First 3 Parameters:")
for i, param in enumerate(parsed_data.get('parameters', [])[:3], 1):
    print(f"    {i}. {param.get('param_name')} (type={param.get('data_type')})")

# Print connections
print(f"\n  Connections:")
for i, conn in enumerate(parsed_data.get('connections', []), 1):
    print(f"    {i}. {conn.get('connection_name')}")

print("\n" + "="*80)
print("QUERYING DATABASE")
print("="*80)

conn = sqlite3.connect('iodd_manager.db')
cursor = conn.cursor()

# Find EDS ID 1
cursor.execute("""
    SELECT id, product_name, vendor_name, catalog_number
    FROM eds_files WHERE id = 1
""")
row = cursor.fetchone()
print(f"\nDatabase Record (ID={row[0]}):")
print(f"  Product: {row[1]}")
print(f"  Vendor: {row[2]}")
print(f"  Catalog: {row[3]}")

# Get parameters
cursor.execute("SELECT COUNT(*), GROUP_CONCAT(param_name, ', ') FROM (SELECT param_name FROM eds_parameters WHERE eds_file_id = 1 LIMIT 5)")
param_row = cursor.fetchone()
print(f"  Parameters: {param_row[0]} total")
print(f"    First few: {param_row[1]}")

# Get connections
cursor.execute("SELECT COUNT(*), GROUP_CONCAT(connection_name, ', ') FROM eds_connections WHERE eds_file_id = 1")
conn_row = cursor.fetchone()
print(f"  Connections: {conn_row[0]} total")
print(f"    Names: {conn_row[1]}")

# Get capacity
cursor.execute("""
    SELECT max_msg_connections, max_io_producers, max_io_consumers
    FROM eds_capacity WHERE eds_file_id = 1
""")
cap_row = cursor.fetchone()
print(f"  Capacity:")
if cap_row:
    print(f"    max_msg_connections: {cap_row[0]}")
    print(f"    max_io_producers: {cap_row[1]}")
    print(f"    max_io_consumers: {cap_row[2]}")
else:
    print(f"    NO CAPACITY DATA!")

# Get TSpecs
cursor.execute("SELECT COUNT(*) FROM eds_tspecs WHERE eds_file_id = 1")
tspec_count = cursor.fetchone()[0]
print(f"    TSpecs: {tspec_count}")

print("\n" + "="*80)
print("COMPARISON SUMMARY")
print("="*80)

issues = []

# Compare
db_params = param_row[0]
src_params = len(parsed_data.get('parameters', []))
print(f"\nParameters: DB={db_params}, SRC={src_params} {'✓' if db_params == src_params else '✗ MISMATCH'}")
if db_params != src_params:
    issues.append(f"Parameter count: DB={db_params}, SRC={src_params}")

db_conns = conn_row[0]
src_conns = len(parsed_data.get('connections', []))
print(f"Connections: DB={db_conns}, SRC={src_conns} {'✓' if db_conns == src_conns else '✗ MISMATCH'}")
if db_conns != src_conns:
    issues.append(f"Connection count: DB={db_conns}, SRC={src_conns}")

if cap_row:
    db_cap_msg = cap_row[0]
    src_cap_msg = capacity.get('max_msg_connections')
    print(f"Capacity (msg): DB={db_cap_msg}, SRC={src_cap_msg} {'✓' if db_cap_msg == src_cap_msg else '✗ MISMATCH'}")
    if db_cap_msg != src_cap_msg:
        issues.append(f"Capacity max_msg_connections: DB={db_cap_msg}, SRC={src_cap_msg}")

if issues:
    print(f"\n{'='*80}")
    print(f"ISSUES FOUND: {len(issues)}")
    print('='*80)
    for issue in issues:
        print(f"  - {issue}")
else:
    print(f"\n✓ ALL DATA MATCHES!")

conn.close()
