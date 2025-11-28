"""
Examine the XML structure of V_ParaConfigFaultCollection to understand
how SingleValues are nested within ArrayT Datatype
"""
import sys
sys.path.insert(0, 'src')

import sqlite3
from xml.etree import ElementTree as ET

# Get original IODD XML from archive
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

device_id = 130

cursor.execute('SELECT file_content FROM pqa_file_archive WHERE device_id = ? LIMIT 1', (device_id,))
row = cursor.fetchone()
original_xml = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]

conn.close()

# Parse XML
root = ET.fromstring(original_xml)

# Define namespaces
ns = {'iodd': 'http://www.io-link.com/IODD/2010/10',
      'xsi': 'http://www.w3.org/2001/XMLSchema-instance'}

# Find V_ParaConfigFaultCollection
variables = root.findall('.//iodd:VariableCollection/iodd:Variable', ns)
for var in variables:
    var_id = var.get('id')
    if var_id == 'V_ParaConfigFaultCollection':
        print(f'Found Variable: {var_id}')
        print()

        # Print the full XML structure
        print('Full XML structure:')
        print('=' * 80)
        xml_str = ET.tostring(var, encoding='unicode')
        # Pretty print with indentation
        import xml.dom.minidom
        dom = xml.dom.minidom.parseString(xml_str)
        print(dom.toprettyxml(indent='  '))
        print('=' * 80)
        print()

        # Analyze structure
        datatype = var.find('iodd:Datatype', ns)
        if datatype is not None:
            xsi_type = datatype.get('{http://www.w3.org/2001/XMLSchema-instance}type')
            print(f'Datatype xsi:type: {xsi_type}')
            print()

            # Find SimpleDatatype within ArrayT
            simple_dt = datatype.find('.//iodd:SimpleDatatype', ns)
            if simple_dt is not None:
                print('Found SimpleDatatype inside ArrayT:')
                print(f'  type: {simple_dt.get("type")}')
                print(f'  bitLength: {simple_dt.get("bitLength")}')

                # Find SingleValues
                single_values = simple_dt.findall('iodd:SingleValue', ns)
                print(f'  SingleValue count: {len(single_values)}')
                print()

                if len(single_values) > 0:
                    print('First 5 SingleValues:')
                    for i, sv in enumerate(single_values[:5]):
                        value = sv.get('value')
                        name_elem = sv.find('iodd:Name', ns)
                        text_id = name_elem.get('textId') if name_elem is not None else None
                        print(f'  {i+1}. value={value}, textId={text_id}')

        break
