#!/usr/bin/env python
"""Test script to import CAPTRON CALIS IODD and verify all phases of data extraction"""

import sys
import sqlite3
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from greenstack import IODDManager

def test_captron_import():
    """Test importing CAPTRON CALIS IODD file"""

    # Initialize manager
    manager = IODDManager()

    # IODD file path
    iodd_path = Path("F:/github/GreenStack/iodd_storage/tmp1dou7hzeCAPTRON-CALIS-M01-20241219-IODD1.1/CAPTRON-CALIS-M01-20241219-IODD1.1.xml")

    if not iodd_path.exists():
        print(f"ERROR: IODD file not found at {iodd_path}")
        return False

    print(f"Importing IODD from: {iodd_path}")
    print("=" * 80)

    # Import the IODD
    try:
        device_id = manager.import_iodd(str(iodd_path))
        print(f"\nSUCCESS: Device imported with ID: {device_id}")
    except Exception as e:
        print(f"ERROR during import: {e}")
        import traceback
        traceback.print_exc()
        return False

    # Now verify all the new data was captured
    print("\n" + "=" * 80)
    print("VERIFICATION: Checking all 5 phases of data capture")
    print("=" * 80)

    conn = sqlite3.connect(manager.storage.db_path)
    cursor = conn.cursor()

    # Phase 1: UI Rendering Metadata
    print("\nPHASE 1: UI Rendering Metadata")
    print("-" * 40)

    cursor.execute("""
        SELECT COUNT(*) FROM process_data_ui_info
        JOIN process_data ON process_data_ui_info.process_data_id = process_data.id
        WHERE process_data.device_id = ?
    """, (device_id,))
    ui_info_count = cursor.fetchone()[0]
    print(f"  Process Data UI Info entries: {ui_info_count}")

    cursor.execute("""
        SELECT COUNT(*) FROM ui_menu_items
        WHERE gradient IS NOT NULL OR offset IS NOT NULL
    """)
    gradient_offset_count = cursor.fetchone()[0]
    print(f"  Menu items with gradient/offset: {gradient_offset_count}")

    # Phase 2: Device Variants and Conditions
    print("\nPHASE 2: Device Variants & Conditions")
    print("-" * 40)

    cursor.execute("SELECT COUNT(*) FROM device_variants WHERE device_id = ?", (device_id,))
    variants_count = cursor.fetchone()[0]
    print(f"  Device variants: {variants_count}")

    if variants_count > 0:
        cursor.execute("""
            SELECT product_id, name, device_symbol, device_icon
            FROM device_variants WHERE device_id = ?
        """, (device_id,))
        for row in cursor.fetchall():
            print(f"    - {row[0]}: {row[1]} (symbol: {row[2]}, icon: {row[3]})")

    cursor.execute("""
        SELECT COUNT(*) FROM process_data_conditions
        JOIN process_data ON process_data_conditions.process_data_id = process_data.id
        WHERE process_data.device_id = ?
    """, (device_id,))
    conditions_count = cursor.fetchone()[0]
    print(f"  Process data conditions: {conditions_count}")

    # Phase 3: Button Configurations
    print("\nPHASE 3: Button Configurations")
    print("-" * 40)

    cursor.execute("""
        SELECT COUNT(*) FROM ui_menu_buttons
        JOIN ui_menu_items ON ui_menu_buttons.menu_item_id = ui_menu_items.id
        JOIN ui_menus ON ui_menu_items.menu_id = ui_menus.id
        WHERE ui_menus.device_id = ?
    """, (device_id,))
    buttons_count = cursor.fetchone()[0]
    print(f"  UI menu buttons: {buttons_count}")

    if buttons_count > 0:
        cursor.execute("""
            SELECT b.button_value, b.description
            FROM ui_menu_buttons b
            JOIN ui_menu_items mi ON b.menu_item_id = mi.id
            JOIN ui_menus m ON mi.menu_id = m.id
            WHERE m.device_id = ?
            LIMIT 5
        """, (device_id,))
        for row in cursor.fetchall():
            print(f"    - Button: {row[0]} ({row[1]})")

    # Phase 4: Wiring and Testing
    print("\nPHASE 4: Wiring & Testing")
    print("-" * 40)

    cursor.execute("SELECT COUNT(*) FROM wire_configurations WHERE device_id = ?", (device_id,))
    wires_count = cursor.fetchone()[0]
    print(f"  Wire configurations: {wires_count}")

    if wires_count > 0:
        cursor.execute("""
            SELECT wire_number, wire_color, wire_function
            FROM wire_configurations WHERE device_id = ?
        """, (device_id,))
        for row in cursor.fetchall():
            print(f"    - Wire {row[0]}: {row[1]} ({row[2]})")

    cursor.execute("SELECT COUNT(*) FROM device_test_config WHERE device_id = ?", (device_id,))
    test_configs_count = cursor.fetchone()[0]
    print(f"  Test configurations: {test_configs_count}")

    # Phase 5: Custom Datatypes
    print("\nPHASE 5: Custom Datatypes")
    print("-" * 40)

    cursor.execute("SELECT COUNT(*) FROM custom_datatypes WHERE device_id = ?", (device_id,))
    datatypes_count = cursor.fetchone()[0]
    print(f"  Custom datatypes: {datatypes_count}")

    if datatypes_count > 0:
        cursor.execute("""
            SELECT datatype_id, datatype_xsi_type, bit_length
            FROM custom_datatypes WHERE device_id = ? LIMIT 5
        """, (device_id,))
        for row in cursor.fetchall():
            print(f"    - {row[0]}: {row[1]} ({row[2]} bits)")

    # Check vendor logo
    cursor.execute("SELECT vendor_logo_filename FROM devices WHERE id = ?", (device_id,))
    logo = cursor.fetchone()
    if logo and logo[0]:
        print(f"  Vendor logo: {logo[0]}")

    # Check stamp metadata
    cursor.execute("SELECT stamp_crc, checker_name, checker_version FROM iodd_files WHERE device_id = ?", (device_id,))
    stamp = cursor.fetchone()
    if stamp and (stamp[0] or stamp[1] or stamp[2]):
        print(f"  Stamp CRC: {stamp[0]}")
        print(f"  Checker: {stamp[1]} v{stamp[2]}")

    conn.close()

    print("\n" + "=" * 80)
    print("VERIFICATION COMPLETE!")
    print("=" * 80)

    return True

if __name__ == "__main__":
    success = test_captron_import()
    sys.exit(0 if success else 1)
