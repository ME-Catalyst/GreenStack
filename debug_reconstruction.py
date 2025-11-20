"""Debug reconstruction error"""
import sys
sys.path.insert(0, r'F:\github\GreenStack')

from src.utils.forensic_reconstruction_v2 import IODDReconstructor
import xml.etree.ElementTree as ET

reconstructor = IODDReconstructor()

try:
    # Try to reconstruct
    xml_str = reconstructor.reconstruct_iodd(56)
    print("SUCCESS!")
    print(xml_str[:500])
except Exception as e:
    print(f"ERROR: {e}")
    print(f"Type: {type(e)}")

    # Get the raw XML to see what's being generated
    import sqlite3
    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()

    # Recreate the reconstruction but capture the rough string
    cursor.execute("SELECT * FROM devices WHERE id = 56")
    device = cursor.fetchone()

    # Make device a Row object
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM devices WHERE id = 56")
    device = cursor.fetchone()

    # Create IODevice element
    root = ET.Element('IODevice')
    root.set('xmlns', 'http://www.io-link.com/IODD/2010/10')
    root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

    # Create ExternalTextCollection
    text_collection = reconstructor._create_text_collection(conn, 56)
    if text_collection is not None:
        root.append(text_collection)

    # Create ProfileBody
    profile_body = reconstructor._create_profile_body(conn, 56, device)
    root.append(profile_body)

    # Convert to string
    rough_string = ET.tostring(root, encoding='unicode')
    print("\n=== Checking for duplicate attributes ===")
    print("First 200 chars:")
    print(rough_string[:200])
    print("\nAround position 108:")
    print(rough_string[90:130])

    conn.close()
