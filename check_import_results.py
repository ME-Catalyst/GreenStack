"""
Check the results of the latest IODD import after Fix #86-92
"""
import sqlite3
from collections import Counter

DB_PATH = 'F:/github/GreenStack/greenstack.db'

def check_import_results():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("=" * 80)
    print("IMPORT VERIFICATION - Fix #86-92 Results")
    print("=" * 80)

    # Check device count
    cursor.execute("SELECT COUNT(*) FROM devices")
    device_count = cursor.fetchone()[0]
    print(f"\n[1] Total Devices Imported: {device_count}")

    # Check PQA stats
    cursor.execute("""
        SELECT
            COUNT(*) as total_files,
            SUM(CASE WHEN overall_score = 100.0 THEN 1 ELSE 0 END) as perfect_files,
            AVG(overall_score) as avg_score
        FROM pqa_quality_metrics
    """)
    pqa = cursor.fetchone()

    if pqa and pqa['total_files'] > 0:
        print(f"\n[2] PQA Quality Metrics:")
        print(f"    Total Files Analyzed: {pqa['total_files']}")
        print(f"    Perfect (100%) Files: {pqa['perfect_files']} ({pqa['perfect_files']/pqa['total_files']*100:.1f}%)")
        print(f"    Average Score: {pqa['avg_score']:.2f}%")
    else:
        print(f"\n[2] PQA Analysis: Not yet complete (may still be running)")

    # Check for menu duplicates (the main issue Fix #86-92 addresses)
    print(f"\n[3] Menu Duplicate Check (Fix #86-92):")

    # Get SL-x-TRIO device (Vendor 1270, Device 16) - the main test case
    cursor.execute("""
        SELECT id, product_name
        FROM devices
        WHERE vendor_id = 1270 AND device_id = 16
    """)
    sl_trio = cursor.fetchone()

    if sl_trio:
        device_id = sl_trio['id']
        product_name = sl_trio['product_name']
        print(f"    Testing: {product_name} (ID: {device_id})")

        # Check for duplicate variable_ids in menu items
        cursor.execute("""
            SELECT variable_id, COUNT(*) as count
            FROM ui_menu_items
            WHERE menu_id IN (SELECT id FROM ui_menus WHERE device_id = ?)
            AND variable_id IS NOT NULL
            GROUP BY variable_id
            HAVING COUNT(*) > 1
            ORDER BY count DESC
            LIMIT 5
        """, (device_id,))

        duplicates = cursor.fetchall()

        if duplicates:
            print(f"    [FAIL] Found {len(duplicates)} duplicate variable_ids:")
            for dup in duplicates:
                print(f"           variable_id={dup['variable_id']}: {dup['count']} occurrences (should be 1)")
            print(f"    Status: Fix #86-92 NOT working - parser still creating duplicates")
        else:
            print(f"    [PASS] NO duplicate variable_ids found!")
            print(f"    Status: Fix #86-92 WORKING CORRECTLY")
    else:
        print(f"    SL-x-TRIO device not found in import")

    # Check total diffs across all files
    cursor.execute("""
        SELECT SUM(
            COALESCE(missing_elements, 0) +
            COALESCE(extra_elements, 0) +
            COALESCE(missing_attributes, 0) +
            COALESCE(incorrect_attributes, 0) +
            COALESCE(value_changes, 0)
        ) as total_diffs
        FROM pqa_quality_metrics
    """)
    total_diffs_row = cursor.fetchone()
    total_diffs = total_diffs_row['total_diffs'] if total_diffs_row['total_diffs'] else 0

    print(f"\n[4] Total Diffs Across All Files: {total_diffs}")

    if device_count > 0:
        print(f"\n[5] Expected vs Actual:")
        print(f"    Before Fix #86-92: 299 diffs, 229 perfect files (92.7%)")
        if total_diffs > 0:
            print(f"    After Fix #86-92:  {total_diffs} diffs, {pqa['perfect_files'] if pqa else 0} perfect files ({pqa['perfect_files']/pqa['total_files']*100:.1f}%)")

            diff_reduction = 299 - total_diffs
            if diff_reduction >= 130:
                print(f"    Result: [SUCCESS] Reduced by {diff_reduction} diffs - Fix #86-92 working!")
            elif diff_reduction > 0:
                print(f"    Result: [PARTIAL] Reduced by {diff_reduction} diffs - some improvement")
            else:
                print(f"    Result: [FAIL] No significant improvement - fix may not be applied")

    print("=" * 80)
    conn.close()

if __name__ == '__main__':
    check_import_results()
