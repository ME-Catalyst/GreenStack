"""Test ErrorTypeCollection and EventCollection reconstruction"""
import sys
sys.path.insert(0, 'F:\\github\\GreenStack')

from src.utils.forensic_reconstruction_v2 import IODDReconstructor
import re

reconstructor = IODDReconstructor()
xml = reconstructor.reconstruct_iodd(56)

print(f'Reconstructed XML length: {len(xml)} characters\n')

# Check for ErrorTypeCollection
error_section = re.search(r'<ErrorTypeCollection>.*?</ErrorTypeCollection>', xml, re.DOTALL)
print('=== ErrorTypeCollection ===')
if error_section:
    print('FOUND')
    print(error_section.group(0))
else:
    print('NOT FOUND')

# Check for EventCollection
event_section = re.search(r'<EventCollection>.*?</EventCollection>', xml, re.DOTALL)
print('\n=== EventCollection ===')
if event_section:
    print('FOUND')
    print(event_section.group(0))
else:
    print('NOT FOUND')
