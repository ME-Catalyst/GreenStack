"""
Check for parsing gaps in EDS files
"""
import sqlite3

conn = sqlite3.connect('iodd_manager.db')
cursor = conn.cursor()

# Get summary of all EDS files
cursor.execute("""
    SELECT
        id,
        vendor_name,
        product_name,
        product_code,
        major_revision,
        minor_revision,
        length(eds_content) as content_length
    FROM eds_files
    ORDER BY id
""")

eds_files = cursor.fetchall()

print(f"{'='*80}")
print(f"EDS PARSING GAPS ANALYSIS")
print(f"{'='*80}")
print(f"\nTotal EDS Files: {len(eds_files)}\n")

for eds in eds_files:
    eds_id, vendor, product, code, maj, min_, content_len = eds

    # Get counts for this EDS
    cursor.execute("SELECT COUNT(*) FROM eds_parameters WHERE eds_file_id = ?", (eds_id,))
    param_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eds_connections WHERE eds_file_id = ?", (eds_id,))
    conn_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eds_ports WHERE eds_file_id = ?", (eds_id,))
    port_count = cursor.fetchone()[0]

    cursor.execute("""
        SELECT max_msg_connections, max_io_producers, max_io_consumers
        FROM eds_capacity WHERE eds_file_id = ?
    """, (eds_id,))
    capacity_row = cursor.fetchone()

    has_capacity = capacity_row and any(v is not None for v in capacity_row)
    capacity_vals = capacity_row if capacity_row else (None, None, None)

    # Check for issues
    issues = []
    if param_count == 0:
        issues.append("NO PARAMETERS")
    if conn_count == 0:
        issues.append("NO CONNECTIONS")
    if not has_capacity:
        issues.append("NO CAPACITY")
    if content_len == 0 or content_len is None:
        issues.append("NO CONTENT")

    status = "[!]" if issues else "[OK]"

    print(f"{status}ID {eds_id}: {vendor} - {product} ({code}) v{maj}.{min_}")
    print(f"   Content: {content_len:,} bytes")
    print(f"   Parameters: {param_count}, Connections: {conn_count}, Ports: {port_count}")
    print(f"   Capacity: MsgConn={capacity_vals[0]}, IOProd={capacity_vals[1]}, IOCons={capacity_vals[2]}")
    if issues:
        print(f"   ISSUES: {', '.join(issues)}")
    print()

# Summary statistics
cursor.execute("SELECT COUNT(*) FROM eds_files WHERE id IN (SELECT DISTINCT eds_file_id FROM eds_parameters)")
files_with_params = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM eds_files WHERE id IN (SELECT DISTINCT eds_file_id FROM eds_connections)")
files_with_conns = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM eds_capacity WHERE max_msg_connections IS NOT NULL OR max_io_producers IS NOT NULL OR max_io_consumers IS NOT NULL")
files_with_capacity = cursor.fetchone()[0]

print(f"{'='*80}")
print(f"SUMMARY")
print(f"{'='*80}")
print(f"Files with Parameters: {files_with_params}/{len(eds_files)} ({files_with_params/len(eds_files)*100:.1f}%)")
print(f"Files with Connections: {files_with_conns}/{len(eds_files)} ({files_with_conns/len(eds_files)*100:.1f}%)")
print(f"Files with Capacity: {files_with_capacity}/{len(eds_files)} ({files_with_capacity/len(eds_files)*100:.1f}%)")

conn.close()
