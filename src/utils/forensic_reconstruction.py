"""
Forensic XML Reconstruction Engine

Reconstructs IODD XML files from database tables for Parser Quality Assurance.
This module enables validation of parser accuracy by comparing original IODD files
against database-reconstructed XML.
"""

import logging
import sqlite3
from typing import Dict, List, Optional
from xml.etree import ElementTree as ET
from xml.dom import minidom

logger = logging.getLogger(__name__)


class ForensicReconstructor:
    """
    Reconstructs IODD XML from database tables for quality validation
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

        Raises:
            ValueError: If device not found
        """
        conn = self.get_connection()
        try:
            # Verify device exists
            device = self._get_device(conn, device_id)
            if not device:
                raise ValueError(f"Device {device_id} not found")

            # Build XML tree
            root = self._create_root_element(conn, device_id)

            # Add ProfileBody section
            profile_body = self._reconstruct_profile_body(conn, device_id)
            if profile_body is not None:
                root.append(profile_body)

            # Add ExternalTextCollection
            text_collection = self._reconstruct_text_collection(conn, device_id)
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

    def _create_root_element(self, conn: sqlite3.Connection, device_id: int) -> ET.Element:
        """
        Create root IODevice element with namespace and attributes

        Based on document_info table
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM document_info WHERE device_id = ?
        """, (device_id,))
        doc_info = cursor.fetchone()

        # Create root with namespace
        root = ET.Element('IODevice')

        if doc_info:
            # Add xmlns if present
            if doc_info['xmlns']:
                root.set('xmlns', doc_info['xmlns'])
            if doc_info['xmlns_xsi']:
                root.set('xmlns:xsi', doc_info['xmlns_xsi'])

        return root

    def _reconstruct_profile_body(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """
        Reconstruct ProfileBody section containing DeviceIdentity and DeviceFunction
        """
        profile_body = ET.Element('ProfileBody')

        # Add DeviceIdentity
        device_identity = self._reconstruct_device_identity(conn, device_id)
        if device_identity is not None:
            profile_body.append(device_identity)

        # Add DeviceFunction
        device_function = self._reconstruct_device_function(conn, device_id)
        if device_function is not None:
            profile_body.append(device_function)

        return profile_body if len(profile_body) > 0 else None

    def _reconstruct_device_identity(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct DeviceIdentity section"""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()

        if not device:
            return None

        device_identity = ET.Element('DeviceIdentity')

        if device['vendor_id']:
            vendor_id = ET.SubElement(device_identity, 'VendorId')
            vendor_id.text = str(device['vendor_id'])

        if device['vendor_name']:
            vendor_name = ET.SubElement(device_identity, 'VendorName')
            vendor_name.set('textId', 'TI_VendorName')

        if device['vendor_text']:
            vendor_text = ET.SubElement(device_identity, 'VendorText')
            vendor_text.set('textId', 'TI_VendorText')

        if device['vendor_url']:
            vendor_url = ET.SubElement(device_identity, 'VendorUrl')
            vendor_url.text = device['vendor_url']

        if device['device_name']:
            device_name_elem = ET.SubElement(device_identity, 'DeviceName')
            device_name_elem.set('textId', 'TI_DeviceName')

        if device['device_id']:
            device_id_elem = ET.SubElement(device_identity, 'DeviceId')
            device_id_elem.text = str(device['device_id'])

        return device_identity

    def _reconstruct_device_function(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct DeviceFunction section containing Process Data"""
        device_function = ET.Element('DeviceFunction')

        # Add Features
        features = self._reconstruct_features(conn, device_id)
        if features is not None:
            device_function.append(features)

        # Add ProcessDataCollection
        process_data_collection = self._reconstruct_process_data_collection(conn, device_id)
        if process_data_collection is not None:
            device_function.append(process_data_collection)

        # Add VariableCollection (Phase 2)
        variable_collection = self._reconstruct_variable_collection(conn, device_id)
        if variable_collection is not None:
            device_function.append(variable_collection)

        # Add ProcessDataConditionCollection (Phase 2)
        condition_collection = self._reconstruct_condition_collection(conn, device_id)
        if condition_collection is not None:
            device_function.append(condition_collection)

        # Add MenuCollection (Phase 3)
        menu_collection = self._reconstruct_menu_collection(conn, device_id)
        if menu_collection is not None:
            device_function.append(menu_collection)

        # Add UserInterface (all phases)
        user_interface = self._reconstruct_user_interface(conn, device_id)
        if user_interface is not None:
            device_function.append(user_interface)

        # Add DatatypeCollection (Phase 5)
        datatype_collection = self._reconstruct_datatype_collection(conn, device_id)
        if datatype_collection is not None:
            device_function.append(datatype_collection)

        return device_function if len(device_function) > 0 else None

    def _reconstruct_features(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct Features section"""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()

        if not device:
            return None

        features = ET.Element('Features')

        if device['supports_code']:
            features.set('blockParameter', 'true')
        if device['supports_datastore']:
            features.set('dataStorage', 'true')

        return features if features.attrib else None

    def _reconstruct_process_data_collection(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """
        Reconstruct ProcessDataCollection section

        This includes all process data variables (input/output)
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM process_data
            WHERE device_id = ?
            ORDER BY id
        """, (device_id,))
        process_data_rows = cursor.fetchall()

        if not process_data_rows:
            return None

        collection = ET.Element('ProcessDataCollection')

        for pd in process_data_rows:
            pd_elem = ET.Element('ProcessData')
            pd_elem.set('id', pd['pd_id'])

            if pd['name']:
                name = ET.SubElement(pd_elem, 'Name')
                name.set('textId', pd['name'])

            # Add Datatype
            if pd['datatype']:
                datatype = ET.SubElement(pd_elem, 'Datatype')
                datatype.set('type', pd['datatype'])

                if pd['bit_length']:
                    datatype.set('bitLength', str(pd['bit_length']))

            # Add ProcessDataIn/ProcessDataOut
            if pd['direction']:
                direction_elem = ET.SubElement(pd_elem, pd['direction'])
                if pd['bit_offset'] is not None:
                    direction_elem.set('bitOffset', str(pd['bit_offset']))

            # Phase 1: UI Rendering Metadata
            if pd['ui_rendering_config_id']:
                self._add_ui_rendering(conn, pd_elem, pd['ui_rendering_config_id'])

            collection.append(pd_elem)

        return collection

    def _add_ui_rendering(self, conn: sqlite3.Connection, parent: ET.Element, config_id: int) -> None:
        """Add UI rendering metadata (Phase 1)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ui_rendering_configs WHERE id = ?
        """, (config_id,))
        config = cursor.fetchone()

        if not config:
            return

        ui_elem = ET.SubElement(parent, 'UIRendering')

        if config['widget_type']:
            ui_elem.set('widgetType', config['widget_type'])
        if config['display_format']:
            ui_elem.set('displayFormat', config['display_format'])
        if config['unit_symbol']:
            ui_elem.set('unit', config['unit_symbol'])
        if config['gradient_start']:
            ui_elem.set('gradientStart', config['gradient_start'])
        if config['gradient_end']:
            ui_elem.set('gradientEnd', config['gradient_end'])

    def _reconstruct_variable_collection(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct VariableCollection (Phase 2)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM device_variables WHERE device_id = ?
        """, (device_id,))
        variables = cursor.fetchall()

        if not variables:
            return None

        collection = ET.Element('VariableCollection')

        for var in variables:
            var_elem = ET.Element('Variable')
            var_elem.set('id', var['variable_id'])

            if var['variable_name']:
                name = ET.SubElement(var_elem, 'Name')
                name.set('textId', var['variable_name'])

            if var['datatype']:
                datatype = ET.SubElement(var_elem, 'Datatype')
                datatype.set('type', var['datatype'])

            if var['default_value'] is not None:
                default = ET.SubElement(var_elem, 'DefaultValue')
                default.text = str(var['default_value'])

            collection.append(var_elem)

        return collection

    def _reconstruct_condition_collection(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct ProcessDataConditionCollection (Phase 2)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM process_data_conditions WHERE device_id = ?
        """, (device_id,))
        conditions = cursor.fetchall()

        if not conditions:
            return None

        collection = ET.Element('ProcessDataConditionCollection')

        for cond in conditions:
            cond_elem = ET.Element('ProcessDataCondition')
            cond_elem.set('id', cond['condition_id'])

            if cond['variable_id']:
                cond_elem.set('variableId', cond['variable_id'])

            if cond['operator']:
                cond_elem.set('operator', cond['operator'])

            if cond['value'] is not None:
                value = ET.SubElement(cond_elem, 'Value')
                value.text = str(cond['value'])

            collection.append(cond_elem)

        return collection

    def _reconstruct_menu_collection(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct MenuCollection (Phase 3)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM menu_buttons WHERE device_id = ? ORDER BY display_order
        """, (device_id,))
        buttons = cursor.fetchall()

        if not buttons:
            return None

        collection = ET.Element('MenuCollection')
        menu = ET.SubElement(collection, 'Menu')
        menu.set('id', 'M_Main')

        for button in buttons:
            button_elem = ET.SubElement(menu, 'MenuButton')
            button_elem.set('id', button['button_id'])

            if button['button_name']:
                name = ET.SubElement(button_elem, 'Name')
                name.set('textId', button['button_name'])

            if button['button_icon']:
                button_elem.set('icon', button['button_icon'])

            if button['linked_parameter']:
                button_elem.set('linkedParameter', button['linked_parameter'])

        return collection

    def _reconstruct_user_interface(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct UserInterface section (consolidates all UI elements)"""
        user_interface = ET.Element('UserInterface')

        # Phase 2: Add device variants
        variants = self._reconstruct_device_variants(conn, device_id)
        if variants is not None:
            user_interface.append(variants)

        # Phase 3: Observer Role Menus
        observer_menu = self._reconstruct_observer_menu(conn, device_id)
        if observer_menu is not None:
            user_interface.append(observer_menu)

        # Phase 4: Add identification images/diagrams
        self._add_identification(conn, user_interface, device_id)

        return user_interface if len(user_interface) > 0 else None

    def _reconstruct_device_variants(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct DeviceVariantCollection (Phase 2)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM device_variants WHERE device_id = ?
        """, (device_id,))
        variants = cursor.fetchall()

        if not variants:
            return None

        collection = ET.Element('DeviceVariantCollection')

        for variant in variants:
            var_elem = ET.Element('DeviceVariant')
            var_elem.set('id', variant['variant_id'])

            if variant['variant_name']:
                name = ET.SubElement(var_elem, 'Name')
                name.set('textId', variant['variant_name'])

            if variant['product_id']:
                var_elem.set('productId', variant['product_id'])

            collection.append(var_elem)

        return collection

    def _reconstruct_observer_menu(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct ObserverRoleMenu (Phase 3)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM menu_buttons WHERE device_id = ? AND menu_type = 'observer'
        """, (device_id,))
        buttons = cursor.fetchall()

        if not buttons:
            return None

        observer_menu = ET.Element('ObserverRoleMenu')

        for button in buttons:
            item = ET.SubElement(observer_menu, 'MenuItem')
            item.set('id', button['button_id'])

            if button['button_name']:
                item.set('textId', button['button_name'])

        return observer_menu

    def _add_identification(self, conn: sqlite3.Connection, parent: ET.Element, device_id: int) -> None:
        """Add Identification section with images/diagrams (Phase 4)"""
        cursor = conn.cursor()

        # Add device images
        cursor.execute("""
            SELECT * FROM device_images WHERE device_id = ?
        """, (device_id,))
        images = cursor.fetchall()

        if images:
            identification = ET.SubElement(parent, 'Identification')

            for img in images:
                image_elem = ET.SubElement(identification, 'Image')
                if img['image_type']:
                    image_elem.set('type', img['image_type'])
                if img['image_url']:
                    image_elem.text = img['image_url']

    def _reconstruct_datatype_collection(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Reconstruct DatatypeCollection (Phase 5: Custom Datatypes)"""
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

            if dt['value_type']:
                datatype_elem.set('type', dt['value_type'])

            if dt['bit_length']:
                datatype_elem.set('bitLength', str(dt['bit_length']))

            # Add SingleValue enumerations
            if dt['value_type'] == 'SingleValue':
                self._add_single_values(conn, datatype_elem, dt['id'])

            # Add RecordItem structures
            if dt['value_type'] == 'RecordItem':
                self._add_record_items(conn, datatype_elem, dt['id'])

            collection.append(datatype_elem)

        return collection

    def _add_single_values(self, conn: sqlite3.Connection, parent: ET.Element, datatype_id: int) -> None:
        """Add SingleValue enumeration items (Phase 5)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM datatype_single_values WHERE datatype_id = ? ORDER BY value
        """, (datatype_id,))
        values = cursor.fetchall()

        value_list = ET.SubElement(parent, 'SingleValueList')

        for val in values:
            value_elem = ET.SubElement(value_list, 'SingleValue')
            value_elem.set('value', str(val['value']))

            if val['value_text']:
                name = ET.SubElement(value_elem, 'Name')
                name.set('textId', val['value_text'])

    def _add_record_items(self, conn: sqlite3.Connection, parent: ET.Element, datatype_id: int) -> None:
        """Add RecordItem structure fields (Phase 5)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM datatype_record_items WHERE datatype_id = ? ORDER BY subindex
        """, (datatype_id,))
        items = cursor.fetchall()

        record_list = ET.SubElement(parent, 'RecordItemList')

        for item in items:
            record_elem = ET.SubElement(record_list, 'RecordItem')
            record_elem.set('subindex', str(item['subindex']))

            if item['record_item_name']:
                name = ET.SubElement(record_elem, 'Name')
                name.set('textId', item['record_item_name'])

            if item['simple_datatype']:
                datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                datatype.set('type', item['simple_datatype'])

                if item['bit_length']:
                    datatype.set('bitLength', str(item['bit_length']))

    def _reconstruct_text_collection(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """
        Reconstruct ExternalTextCollection

        This contains all multi-language text entries
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT DISTINCT language FROM external_texts WHERE device_id = ?
        """, (device_id,))
        languages = cursor.fetchall()

        if not languages:
            return None

        collection = ET.Element('ExternalTextCollection')

        for lang_row in languages:
            lang = lang_row['language']
            primary_lang = ET.SubElement(collection, 'PrimaryLanguage')
            primary_lang.set('xml:lang', lang)

            # Get all texts for this language
            cursor.execute("""
                SELECT * FROM external_texts WHERE device_id = ? AND language = ?
            """, (device_id, lang))
            texts = cursor.fetchall()

            for text in texts:
                text_elem = ET.SubElement(primary_lang, 'Text')
                text_elem.set('id', text['text_id'])
                text_elem.set('value', text['text_value'] or '')

        return collection

    def _prettify_xml(self, elem: ET.Element) -> str:
        """
        Convert XML element to pretty-printed string

        Args:
            elem: XML element tree

        Returns:
            Formatted XML string
        """
        rough_string = ET.tostring(elem, encoding='unicode')
        reparsed = minidom.parseString(rough_string)
        return reparsed.toprettyxml(indent="  ")


# Convenience function
def reconstruct_iodd_xml(device_id: int, db_path: str = "greenstack.db") -> str:
    """
    Reconstruct IODD XML for a device

    Args:
        device_id: ID of device to reconstruct
        db_path: Path to database file

    Returns:
        Reconstructed IODD XML as string
    """
    reconstructor = ForensicReconstructor(db_path)
    return reconstructor.reconstruct_iodd(device_id)
