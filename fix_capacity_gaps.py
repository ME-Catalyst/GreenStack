"""
Fix capacity data for files that were imported before the multi-vendor fix
"""
import sqlite3
from eds_parser import EDSParser

# Files with missing capacity data
MISSING_CAPACITY_IDS = [3, 8, 9, 10, 11, 12, 13]

conn = sqlite3.connect('iodd_manager.db')
cursor = conn.cursor()

print("=" * 80)
print("FIXING CAPACITY DATA FOR 7 EDS FILES")
print("=" * 80)

for eds_id in MISSING_CAPACITY_IDS:
    # Get the EDS content
    cursor.execute("SELECT eds_content, vendor_name, product_name FROM eds_files WHERE id = ?", (eds_id,))
    row = cursor.fetchone()

    if not row:
        print(f"[ERROR] EDS ID {eds_id} not found")
        continue

    eds_content, vendor, product = row

    print(f"\n[{eds_id}] {vendor} - {product}")

    # Parse capacity data with current parser
    parser = EDSParser(eds_content)
    capacity = parser.get_capacity()

    print(f"  Parsed capacity:")
    print(f"    max_msg_connections: {capacity['max_msg_connections']}")
    print(f"    max_io_producers: {capacity['max_io_producers']}")
    print(f"    max_io_consumers: {capacity['max_io_consumers']}")

    # Update the capacity table
    cursor.execute("""
        UPDATE eds_capacity
        SET max_msg_connections = ?,
            max_io_producers = ?,
            max_io_consumers = ?,
            max_cx_per_config_tool = ?
        WHERE eds_file_id = ?
    """, (
        capacity['max_msg_connections'],
        capacity['max_io_producers'],
        capacity['max_io_consumers'],
        capacity['max_cx_per_config_tool'],
        eds_id
    ))

    # Update TSpecs
    cursor.execute("DELETE FROM eds_tspecs WHERE eds_file_id = ?", (eds_id,))

    for tspec in capacity['tspecs']:
        cursor.execute("""
            INSERT INTO eds_tspecs (eds_file_id, tspec_name, direction, data_size, rate)
            VALUES (?, ?, ?, ?, ?)
        """, (
            eds_id,
            tspec['tspec_name'],
            tspec['direction'],
            tspec['data_size'],
            tspec['rate']
        ))

    print(f"  [OK] Updated capacity and {len(capacity['tspecs'])} TSpecs")

conn.commit()

# Verify the fix
print("\n" + "=" * 80)
print("VERIFICATION")
print("=" * 80)

for eds_id in MISSING_CAPACITY_IDS:
    cursor.execute("""
        SELECT max_msg_connections, max_io_producers, max_io_consumers
        FROM eds_capacity WHERE eds_file_id = ?
    """, (eds_id,))

    row = cursor.fetchone()
    if row:
        msg, prod, cons = row
        status = "[OK]" if any(v is not None for v in row) else "[FAIL]"
        print(f"{status} ID {eds_id}: MsgConn={msg}, IOProd={prod}, IOCons={cons}")
    else:
        print(f"[FAIL] ID {eds_id}: No capacity row found")

conn.close()

print("\n" + "=" * 80)
print("COMPLETE!")
print("=" * 80)
