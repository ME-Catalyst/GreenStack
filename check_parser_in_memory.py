"""
Check if the running backend has the Fix #86-92 code loaded in memory
"""
import sys
sys.path.insert(0, 'F:/github/GreenStack')

import inspect
from src.parsing import IODDParser

print("=" * 80)
print("PARSER CODE VERIFICATION - Fix #86-92")
print("=" * 80)

# Get the _extract_ui_menus method source
method = IODDParser._extract_ui_menus
source = inspect.getsource(method)

print("\n[1] Checking _extract_ui_menus() method...")

# Check for the fix indicators
has_menu_collection_check = "menu_collection = ui_elem.find" in source
has_direct_child_selectors = "menu_collection.findall('iodd:Menu'" in source
has_old_descendant_selectors = "ui_elem.findall('.//iodd:Menu'" in source

print(f"\n[2] Fix #86-92 Indicators:")
print(f"    Has menu_collection extraction: {has_menu_collection_check}")
print(f"    Uses direct child selectors: {has_direct_child_selectors}")
print(f"    Uses old descendant selectors: {has_old_descendant_selectors}")

if has_menu_collection_check and has_direct_child_selectors and not has_old_descendant_selectors:
    print(f"\n[PASS] Fix #86-92 IS loaded in memory!")
    print(f"       Parser code is correct.")
else:
    print(f"\n[FAIL] Fix #86-92 NOT loaded in memory!")
    print(f"       Parser is using OLD code with descendant selectors.")

# Show the critical lines
print(f"\n[3] Critical Code Section:")
lines = source.split('\n')
for i, line in enumerate(lines[5:25], start=6):  # Show lines 6-25
    if 'menu' in line.lower() or 'find' in line.lower():
        print(f"    {i:3d}: {line}")

print("=" * 80)
