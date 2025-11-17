"""
Forensic XML Reconstruction Engine v2 (Aligned with Actual Schema)

Reconstructs IODD XML files from database tables for Parser Quality Assurance.
This version is aligned with the actual GreenStack database schema.
"""

import logging
import sqlite3
from typing import Dict, List, Optional, Tuple
from xml.etree import ElementTree as ET
from xml.dom import minidom

logger = logging.getLogger(__name__)


class IODDReconstructor:
    """
    Reconstructs IODD XML from GreenStack database

    Aligned with actual schema: devices, document_info, process_data,
    iodd_text, device_features, ui_menus, etc.
    """

    def __init__(self, db_path: str = "greenstack.db"):
        self.db_path = db_path

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with Row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def reconstruct_iodd(self, device_id: int) -> str:
        """
        Forensically reconstruct IODD XML from database

        Args:
            device_id: ID of device to reconstruct

        Returns:
            Reconstructed IODD XML as string
        """
        conn = self.get_connection()
        try:
            # Verify device exists
            device = self._get_device(conn, device_id)
            if not device:
                raise ValueError(f"Device {device_id} not found")

            # Build XML tree
            root = self._create_root_element(conn, device_id, device)

            # Add ProfileBody
            profile_body = self._create_profile_body(conn, device_id, device)
            if profile_body is not None:
                root.append(profile_body)

            # Add ExternalTextCollection
            text_collection = self._create_text_collection(conn, device_id)
            if text_collection is not None:
                root.append(text_collection)

            # Pretty print
            return self._prettify_xml(root)

        finally:
            conn.close()

    def _get_device(self, conn: sqlite3.Connection, device_id: int) -> Optional[sqlite3.Row]:
        """Get device record"""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        return cursor.fetchone()

    def _create_root_element(self, conn: sqlite3.Connection, device_id: int,
                            device: sqlite3.Row) -> ET.Element:
        """Create root IODevice element"""
        root = ET.Element('IODevice')

        # Add standard namespaces
        root.set('xmlns', 'http://www.io-link.com/IODD/2010/10')
        root.set('xmlns:xsi', 'http://www.w3.org/2001/XMLSchema-instance')

        return root

    def _create_profile_body(self, conn: sqlite3.Connection, device_id: int,
                            device: sqlite3.Row) -> ET.Element:
        """Create ProfileBody element"""
        profile_body = ET.Element('ProfileBody')

        # DeviceIdentity
        device_identity = ET.SubElement(profile_body, 'DeviceIdentity')
        device_identity.set('deviceId', str(device['device_id']))

        if device['vendor_id']:
            ET.SubElement(device_identity, 'vendorId').text = str(device['vendor_id'])

        vendor_name = ET.SubElement(device_identity, 'VendorName')
        vendor_name.set('textId', 'TI_VendorName')

        device_name_elem = ET.SubElement(device_identity, 'DeviceName')
        device_name_elem.set('textId', 'TI_DeviceName')

        # DeviceFunction
        device_function = ET.SubElement(profile_body, 'DeviceFunction')

        # Features
        features = self._create_features(conn, device_id)
        if features is not None:
            device_function.append(features)

        # ProcessDataCollection
        process_data_collection = self._create_process_data_collection(conn, device_id)
        if process_data_collection is not None:
            device_function.append(process_data_collection)

        # DatatypeCollection
        datatype_collection = self._create_datatype_collection(conn, device_id)
        if datatype_collection is not None:
            device_function.append(datatype_collection)

        # UserInterface
        user_interface = self._create_user_interface(conn, device_id)
        if user_interface is not None:
            device_function.append(user_interface)

        return profile_body

    def _create_features(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Create Features element"""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM device_features WHERE device_id = ?", (device_id,))
        features_row = cursor.fetchone()

        if not features_row:
            return None

        features = ET.Element('Features')

        if features_row['block_parameter']:
            features.set('blockParameter', 'true')
        if features_row['data_storage']:
            features.set('dataStorage', 'true')

        return features

    def _create_process_data_collection(self, conn: sqlite3.Connection,
                                       device_id: int) -> Optional[ET.Element]:
        """Create ProcessDataCollection element"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM process_data WHERE device_id = ? ORDER BY id
        """, (device_id,))
        process_data_rows = cursor.fetchall()

        if not process_data_rows:
            return None

        collection = ET.Element('ProcessDataCollection')

        for pd in process_data_rows:
            pd_elem = ET.Element('ProcessData')
            pd_elem.set('id', pd['pd_id'])

            # Name
            if pd['name']:
                name = ET.SubElement(pd_elem, 'Name')
                name.set('textId', pd['name'])

            # Datatype
            if pd['data_type']:
                datatype = ET.SubElement(pd_elem, 'Datatype')
                datatype.set('type', pd['data_type'])

                if pd['bit_length']:
                    datatype.set('bitLength', str(pd['bit_length']))

            # Direction (ProcessDataIn or ProcessDataOut)
            if pd['direction']:
                direction_elem = ET.SubElement(pd_elem, pd['direction'])

            # Add UI info if available
            self._add_ui_info(conn, pd_elem, pd['id'])

            collection.append(pd_elem)

        return collection

    def _add_ui_info(self, conn: sqlite3.Connection, parent: ET.Element,
                    process_data_id: int) -> None:
        """Add UI rendering info to process data"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM process_data_ui_info WHERE process_data_id = ?
        """, (process_data_id,))
        ui_info = cursor.fetchone()

        if not ui_info:
            return

        ui_elem = ET.SubElement(parent, 'UIInfo')

        if ui_info['gradient'] is not None:
            ui_elem.set('gradient', str(ui_info['gradient']))
        if ui_info['offset'] is not None:
            ui_elem.set('offset', str(ui_info['offset']))
        if ui_info['unit_code']:
            ui_elem.set('unitCode', ui_info['unit_code'])
        if ui_info['display_format']:
            ui_elem.set('displayFormat', ui_info['display_format'])

    def _create_datatype_collection(self, conn: sqlite3.Connection,
                                   device_id: int) -> Optional[ET.Element]:
        """Create DatatypeCollection for custom datatypes"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM custom_datatypes WHERE device_id = ?
        """, (device_id,))
        datatypes = cursor.fetchall()

        if not datatypes:
            return None

        collection = ET.Element('DatatypeCollection')

        for dt in datatypes:
            datatype_elem = ET.Element('Datatype')
            datatype_elem.set('id', dt['datatype_id'])

            if dt['base_datatype']:
                datatype_elem.set('type', dt['base_datatype'])

            # Add SingleValue enumerations
            self._add_single_values(conn, datatype_elem, dt['id'])

            # Add RecordItem structures
            self._add_record_items(conn, datatype_elem, dt['id'])

            collection.append(datatype_elem)

        return collection

    def _add_single_values(self, conn: sqlite3.Connection, parent: ET.Element,
                          datatype_id: int) -> None:
        """Add SingleValue enumeration values"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM custom_datatype_single_values
            WHERE datatype_id = ? ORDER BY value
        """, (datatype_id,))
        values = cursor.fetchall()

        if not values:
            return

        value_list = ET.SubElement(parent, 'SingleValueList')

        for val in values:
            value_elem = ET.SubElement(value_list, 'SingleValue')
            value_elem.set('value', str(val['value']))

            if val['text_id']:
                name = ET.SubElement(value_elem, 'Name')
                name.set('textId', val['text_id'])

    def _add_record_items(self, conn: sqlite3.Connection, parent: ET.Element,
                         datatype_id: int) -> None:
        """Add RecordItem structure fields"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM custom_datatype_record_items
            WHERE datatype_id = ? ORDER BY subindex
        """, (datatype_id,))
        items = cursor.fetchall()

        if not items:
            return

        record_list = ET.SubElement(parent, 'RecordItemList')

        for item in items:
            record_elem = ET.SubElement(record_list, 'RecordItem')
            record_elem.set('subindex', str(item['subindex']))

            if item['name']:
                name = ET.SubElement(record_elem, 'Name')
                name.set('textId', item['name'])

            if item['simple_datatype']:
                datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                datatype.set('type', item['simple_datatype'])

                if item['bit_length']:
                    datatype.set('bitLength', str(item['bit_length']))

    def _create_user_interface(self, conn: sqlite3.Connection,
                              device_id: int) -> Optional[ET.Element]:
        """Create UserInterface element with menus"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ui_menus WHERE device_id = ?
        """, (device_id,))
        menus = cursor.fetchall()

        if not menus:
            return None

        user_interface = ET.Element('UserInterface')

        for menu in menus:
            menu_elem = ET.SubElement(user_interface, 'Menu')
            menu_elem.set('id', menu['menu_id'])

            if menu['name']:
                menu_elem.set('name', menu['name'])

        return user_interface

    def _create_text_collection(self, conn: sqlite3.Connection,
                               device_id: int) -> Optional[ET.Element]:
        """Create ExternalTextCollection with multi-language texts"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT language_code FROM iodd_text WHERE device_id = ?
        """, (device_id,))
        languages = cursor.fetchall()

        if not languages:
            return None

        collection = ET.Element('ExternalTextCollection')

        for lang_row in languages:
            lang = lang_row['language_code']
            primary_lang = ET.SubElement(collection, 'PrimaryLanguage')
            primary_lang.set('xml:lang', lang)

            # Get all texts for this language
            cursor.execute("""
                SELECT text_id, text_value FROM iodd_text
                WHERE device_id = ? AND language_code = ?
                ORDER BY text_id
            """, (device_id, lang))
            texts = cursor.fetchall()

            for text in texts:
                text_elem = ET.SubElement(primary_lang, 'Text')
                text_elem.set('id', text['text_id'])
                text_elem.set('value', text['text_value'] or '')

        return collection

    def _prettify_xml(self, elem: ET.Element) -> str:
        """Convert XML element to pretty-printed string"""
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


def reconstruct_iodd_xml(device_id: int, db_path: str = "greenstack.db") -> str:
    """
    Reconstruct IODD XML for a device

    Args:
        device_id: ID of device to reconstruct
        db_path: Path to database file

    Returns:
        Reconstructed IODD XML as string
    """
    reconstructor = IODDReconstructor(db_path)
    return reconstructor.reconstruct_iodd(device_id)
