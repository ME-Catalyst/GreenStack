"""Test menu reconstruction for Device #56"""
import sys
sys.path.insert(0, 'F:\\github\\GreenStack')

from src.utils.forensic_reconstruction_v2 import IODDReconstructor
import re

reconstructor = IODDReconstructor()
xml = reconstructor.reconstruct_iodd(56)

# Extract UserInterface section
ui_section = re.search(r'<UserInterface>.*?</UserInterface>', xml, re.DOTALL)

print('=== UserInterface Section ===')
if ui_section:
    print('FOUND')
    print(f'Length: {len(ui_section.group(0))} characters\n')
    # Show first 2000 chars
    print(ui_section.group(0)[:2000])

    # Check for specific elements
    print('\n=== Element Checks ===')
    print(f'MenuCollection: {"YES" if "<MenuCollection>" in xml else "NO"}')
    print(f'ObserverRoleMenuSet: {"YES" if "<ObserverRoleMenuSet>" in xml else "NO"}')
    print(f'MaintenanceRoleMenuSet: {"YES" if "<MaintenanceRoleMenuSet>" in xml else "NO"}')
    print(f'SpecialistRoleMenuSet: {"YES" if "<SpecialistRoleMenuSet>" in xml else "NO"}')

    # Count menus
    menu_count = len(re.findall(r'<Menu id=', xml))
    print(f'\nTotal Menu elements: {menu_count}')
else:
    print('NOT FOUND')
