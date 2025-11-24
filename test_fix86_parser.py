"""
Test script to verify Fix #86-92 is working in the parser.

This directly parses an IODD file and checks for menu duplicate issues.
"""
import sys
import zipfile
from pathlib import Path
from collections import Counter

# Add src to path
sys.path.insert(0, str(Path(__file__).parent / 'src'))

from src.parsing import IODDParser


def test_parser_menu_duplicates(zip_path):
    """Parse IODD and check for menu item duplicates"""
    print(f"\n{'='*80}")
    print(f"Testing: {Path(zip_path).name}")
    print(f"{'='*80}\n")

    # Extract XML from package
    with zipfile.ZipFile(zip_path, 'r') as zf:
        xml_files = [f for f in zf.namelist() if f.endswith('.xml') and not f.startswith('__MACOSX')]
        if not xml_files:
            print("ERROR: No XML file found in package")
            return False

        xml_content = zf.read(xml_files[0]).decode('utf-8')
        print(f"Parsing XML file: {xml_files[0]}")

    # Parse with IODDParser
    parser = IODDParser(xml_content)
    device = parser.parse()

    if not device:
        print("ERROR: Parser returned None")
        return False

    # Check menus
    if not hasattr(device, 'ui_menus') or not device.ui_menus:
        print("No UI menus found in device")
        return True

    print(f"\nFound {len(device.ui_menus.menus)} menus")

    has_duplicates = False

    for menu in device.ui_menus.menus:
        print(f"\n--- Menu: {menu.id} ---")
        print(f"  Total items: {len(menu.items)}")

        # Check for duplicate variable_ids
        var_ids = [item.variable_id for item in menu.items if item.variable_id]
        if var_ids:
            var_counts = Counter(var_ids)
            duplicates = {vid: count for vid, count in var_counts.items() if count > 1}

            if duplicates:
                print(f"  [!] DUPLICATES FOUND in VariableRef:")
                for vid, count in duplicates.items():
                    print(f"      variable_id={vid}: {count} occurrences (should be 1)")
                has_duplicates = True
            else:
                print(f"  [OK] No duplicate variable_ids ({len(set(var_ids))} unique)")

        # Check for duplicate record_item_refs
        rec_refs = [(item.record_item_ref, item.subindex) for item in menu.items
                    if item.record_item_ref]
        if rec_refs:
            rec_counts = Counter(rec_refs)
            duplicates = {ref: count for ref, count in rec_counts.items() if count > 1}

            if duplicates:
                print(f"  [!] DUPLICATES FOUND in RecordItemRef:")
                for (ref, subindex), count in duplicates.items():
                    print(f"      record_item_ref={ref}, subindex={subindex}: {count} occurrences")
                has_duplicates = True
            else:
                print(f"  [OK] No duplicate record_item_refs ({len(set(rec_refs))} unique)")

        # Check for duplicate menu_refs
        menu_refs = [item.menu_ref for item in menu.items if item.menu_ref]
        if menu_refs:
            menu_counts = Counter(menu_refs)
            duplicates = {mref: count for mref, count in menu_counts.items() if count > 1}

            if duplicates:
                print(f"  [!] DUPLICATES FOUND in MenuRef:")
                for mref, count in duplicates.items():
                    print(f"      menu_ref={mref}: {count} occurrences")
                has_duplicates = True
            else:
                print(f"  [OK] No duplicate menu_refs ({len(set(menu_refs))} unique)")

    print(f"\n{'='*80}")
    if has_duplicates:
        print("[FAIL] PARSER HAS BUGS - Duplicates found in menu items")
        print("       Fix #86-92 is NOT working correctly")
    else:
        print("[PASS] PARSER WORKING CORRECTLY - No duplicates found")
        print("       Fix #86-92 is working as expected")
    print(f"{'='*80}\n")

    return not has_duplicates


if __name__ == '__main__':
    # Test with SL-x-TRIO (the main outlier file with menu duplicates)
    # Vendor 1270 = Schrempp, Device 16 = SL-x-TRIO
    test_files = [
        'test-data/iodd-files/Schrempp-SL-1-TRIO-IOLINK-20200716-IODD1.1 (1).zip',
    ]

    all_passed = True
    for test_file in test_files:
        if Path(test_file).exists():
            passed = test_parser_menu_duplicates(test_file)
            all_passed = all_passed and passed
        else:
            print(f"File not found: {test_file}")
            # Try to find it with glob
            import glob
            matches = glob.glob('test-data/iodd-files/*SL*TRIO*.zip')
            if matches:
                print(f"Found alternative: {matches[0]}")
                passed = test_parser_menu_duplicates(matches[0])
                all_passed = all_passed and passed

    sys.exit(0 if all_passed else 1)
