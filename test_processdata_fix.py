"""Test ProcessData reconstruction fix"""
import sys
sys.path.insert(0, 'F:\\github\\GreenStack')

from src.utils.forensic_reconstruction_v2 import IODDReconstructor
import re

reconstructor = IODDReconstructor()
xml = reconstructor.reconstruct_iodd(56)

# Extract ProcessDataCollection
pd_section = re.search(r'<ProcessDataCollection>.*?</ProcessDataCollection>', xml, re.DOTALL)

print('=== ProcessDataCollection ===')
if pd_section:
    print(pd_section.group(0))
else:
    print('NOT FOUND')
