"""
Verify database is empty after delete-all operation
"""
import sqlite3

DB_PATH = 'F:/github/GreenStack/greenstack.db'

def check_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    print("=" * 80)
    print("DATABASE VERIFICATION AFTER DELETE-ALL")
    print("=" * 80)

    # Check main tables
    tables_to_check = [
        ('devices', 'IODD Devices'),
        ('ui_menus', 'UI Menus'),
        ('ui_menu_items', 'UI Menu Items'),
        ('parameters', 'Parameters'),
        ('process_data', 'Process Data'),
        ('events', 'Events'),
        ('iodd_files', 'IODD Files'),
        ('device_variants', 'Device Variants'),
        ('communication_profile', 'Communication Profiles'),
        ('custom_datatypes', 'Custom Datatypes'),
        ('iodd_text', 'IODD Text Entries'),
        ('pqa_file_archive', 'PQA File Archive'),
        ('pqa_quality_metrics', 'PQA Quality Metrics'),
    ]

    all_empty = True

    for table, description in tables_to_check:
        try:
            cursor.execute(f"SELECT COUNT(*) FROM {table}")
            count = cursor.fetchone()[0]

            status = "[OK]  " if count == 0 else "[FAIL]"
            if count > 0:
                all_empty = False

            print(f"{status} {description:30s}: {count:6d} rows")
        except Exception as e:
            print(f"[ERR ] {description:30s}: {str(e)}")

    print("=" * 80)

    if all_empty:
        print("[SUCCESS] Database is completely empty - delete worked correctly!")
    else:
        print("[WARNING] Database still contains data - delete may not have completed")

    print("=" * 80)

    conn.close()
    return all_empty

if __name__ == '__main__':
    check_database()
