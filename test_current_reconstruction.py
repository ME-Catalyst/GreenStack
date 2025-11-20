"""Test current IODD reconstruction for Device #56"""
import sys
sys.path.insert(0, 'F:\\github\\GreenStack')

from src.utils.forensic_reconstruction_v2 import IODDReconstructor
import re

reconstructor = IODDReconstructor()
reconstructed_xml = reconstructor.reconstruct_iodd(56)

print(f'Reconstructed XML length: {len(reconstructed_xml)} characters\n')

# Extract Text IDs
matches = re.findall(r'<Text id="([^"]+)"', reconstructed_xml)

print('=== First 30 Text IDs from CURRENT reconstruction ===')
for i, text_id in enumerate(matches[:30], 1):
    print(f'{i}: {text_id}')

print(f'\n... Total Text elements: {len(matches)}')

# Check for specific IDs
print(f'\n=== Checking for specific IDs ===')
print(f'TI_VendorText in reconstruction: {"YES" if "TI_VendorText" in matches else "NO"}')
print(f'TI_VendorUrl in reconstruction: {"YES" if "TI_VendorUrl" in matches else "NO"}')
print(f'TI_DeviceFamily in reconstruction: {"YES" if "TI_DeviceFamily" in matches else "NO"}')
print(f'TI_0 in reconstruction: {"YES" if "TI_0" in matches else "NO"}')
print(f'TI_1 in reconstruction: {"YES" if "TI_1" in matches else "NO"}')

# Check the order - are they in the right sequence?
if len(matches) >= 3:
    print(f'\n=== Order Check ===')
    print(f'Position 1: {matches[0]} (Expected: TI_VendorText)')
    print(f'Position 2: {matches[1]} (Expected: TI_VendorUrl)')
    print(f'Position 3: {matches[2]} (Expected: TI_DeviceFamily)')
