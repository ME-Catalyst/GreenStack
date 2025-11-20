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
        # Register XML namespaces to prevent duplication
        ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        ET.register_namespace('', 'http://www.io-link.com/IODD/2010/10')

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

            # Add ProfileHeader
            profile_header = self._create_profile_header()
            if profile_header is not None:
                root.append(profile_header)

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
        # Note: xmlns:xsi will be added automatically by ElementTree when xsi:type is used

        return root

    def _create_profile_header(self) -> ET.Element:
        """Create ProfileHeader with standard IO-Link profile information"""
        header = ET.Element('ProfileHeader')

        # Profile Identification
        profile_id = ET.SubElement(header, 'ProfileIdentification')
        profile_id.text = 'IO Device Profile'

        # Profile Revision
        profile_rev = ET.SubElement(header, 'ProfileRevision')
        profile_rev.text = '1.1'

        # Profile Name
        profile_name = ET.SubElement(header, 'ProfileName')
        profile_name.text = 'Device Profile for IO Devices'

        # Profile Source
        profile_source = ET.SubElement(header, 'ProfileSource')
        profile_source.text = 'IO-Link Consortium'

        # Profile Class ID
        profile_class = ET.SubElement(header, 'ProfileClassID')
        profile_class.text = 'Device'

        # ISO15745 Reference
        iso_ref = ET.SubElement(header, 'ISO15745Reference')
        iso_part = ET.SubElement(iso_ref, 'ISO15745Part')
        iso_part.text = '1'
        iso_edition = ET.SubElement(iso_ref, 'ISO15745Edition')
        iso_edition.text = '1'
        profile_tech = ET.SubElement(iso_ref, 'ProfileTechnology')
        profile_tech.text = 'IODD'

        return header

    def _create_profile_body(self, conn: sqlite3.Connection, device_id: int,
                            device: sqlite3.Row) -> ET.Element:
        """Create ProfileBody element"""
        profile_body = ET.Element('ProfileBody')

        # DeviceIdentity
        device_identity = ET.SubElement(profile_body, 'DeviceIdentity')
        device_identity.set('deviceId', str(device['device_id']))

        if device['vendor_id']:
            device_identity.set('vendorId', str(device['vendor_id']))

        if device['manufacturer']:
            device_identity.set('vendorName', device['manufacturer'])

        # VendorText - reference to text describing vendor
        vendor_text = ET.SubElement(device_identity, 'VendorText')
        vendor_text.set('textId', 'TI_VendorText')

        # VendorUrl - reference to vendor website
        vendor_url = ET.SubElement(device_identity, 'VendorUrl')
        vendor_url.set('textId', 'TI_VendorUrl')

        # VendorLogo - if logo file exists
        vendor_logo = ET.SubElement(device_identity, 'VendorLogo')
        if device['vendor_logo_filename']:
            vendor_logo.set('name', device['vendor_logo_filename'])
        else:
            # Use manufacturer name to create logo filename
            vendor_logo.set('name', f"{device['manufacturer'].replace(' ', '-')}-logo.png" if device['manufacturer'] else 'vendor-logo.png')

        # DeviceName
        device_name_elem = ET.SubElement(device_identity, 'DeviceName')
        device_name_elem.set('textId', 'TI_0')  # Standard device name text ID

        # DeviceFamily
        device_family = ET.SubElement(device_identity, 'DeviceFamily')
        device_family.set('textId', 'TI_DeviceFamily')

        # DeviceVariantCollection - device variants/models
        device_variant_coll = ET.SubElement(device_identity, 'DeviceVariantCollection')
        device_variant = ET.SubElement(device_variant_coll, 'DeviceVariant')
        if device['product_name']:
            device_variant.set('productId', device['product_name'])
        # Add variant name
        variant_name = ET.SubElement(device_variant, 'Name')
        variant_name.set('textId', 'TI_1')
        # Add variant description
        variant_desc = ET.SubElement(device_variant, 'Description')
        variant_desc.set('textId', 'TI_2')

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

        # ErrorTypeCollection
        error_type_collection = self._create_error_type_collection(conn, device_id)
        if error_type_collection is not None:
            device_function.append(error_type_collection)

        # EventCollection
        event_collection = self._create_event_collection(conn, device_id)
        if event_collection is not None:
            device_function.append(event_collection)

        # DatatypeCollection
        datatype_collection = self._create_datatype_collection(conn, device_id)
        if datatype_collection is not None:
            device_function.append(datatype_collection)

        # VariableCollection
        variable_collection = self._create_variable_collection(conn, device_id)
        if variable_collection is not None:
            device_function.append(variable_collection)

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

            # Strip direction suffix from ProcessData ID (e.g., "PD_ProcessDataA00In" -> "PD_ProcessDataA00")
            pd_id = pd['pd_id']
            if pd_id.endswith('In') or pd_id.endswith('Out'):
                # Remove "In" or "Out" suffix
                if pd_id.endswith('In'):
                    pd_id = pd_id[:-2]
                elif pd_id.endswith('Out'):
                    pd_id = pd_id[:-3]
            pd_elem.set('id', pd_id)

            # Direction (ProcessDataIn or ProcessDataOut) - create child element
            if pd['direction']:
                if pd['direction'] == 'input':
                    direction_elem = ET.SubElement(pd_elem, 'ProcessDataIn')
                    direction_elem.set('id', pd['pd_id'])  # Full ID with suffix
                    if pd['bit_length']:
                        direction_elem.set('bitLength', str(pd['bit_length']))

                    # Datatype goes inside ProcessDataIn
                    if pd['data_type']:
                        datatype = ET.SubElement(direction_elem, 'Datatype')
                        datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', pd['data_type'])
                        # Note: bitLength already set on ProcessDataIn element
                elif pd['direction'] == 'output':
                    direction_elem = ET.SubElement(pd_elem, 'ProcessDataOut')
                    direction_elem.set('id', pd['pd_id'])  # Full ID with suffix
                    if pd['bit_length']:
                        direction_elem.set('bitLength', str(pd['bit_length']))

                    # Datatype goes inside ProcessDataOut
                    if pd['data_type']:
                        datatype = ET.SubElement(direction_elem, 'Datatype')
                        datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', pd['data_type'])
                        # Note: bitLength already set on ProcessDataOut element

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

            if dt['datatype_xsi_type']:
                datatype_elem.set('type', dt['datatype_xsi_type'])

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

            if val['name']:
                name = ET.SubElement(value_elem, 'Name')
                name.set('textId', val['name'])

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

            if item['datatype_ref']:
                # Use DatatypeRef if there's a reference to a custom datatype
                datatype = ET.SubElement(record_elem, 'DatatypeRef')
                datatype.set('datatypeId', item['datatype_ref'])
            elif item['bit_length']:
                # Otherwise create a SimpleDatatype with bit_length
                datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                if item['bit_length']:
                    datatype.set('bitLength', str(item['bit_length']))

    def _create_user_interface(self, conn: sqlite3.Connection,
                              device_id: int) -> Optional[ET.Element]:
        """Create UserInterface element with menus and role menu sets"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM ui_menus WHERE device_id = ?
        """, (device_id,))
        menus = cursor.fetchall()

        if not menus:
            return None

        user_interface = ET.Element('UserInterface')

        # MenuCollection
        menu_collection = ET.SubElement(user_interface, 'MenuCollection')

        for menu in menus:
            menu_elem = ET.SubElement(menu_collection, 'Menu')
            menu_elem.set('id', menu['menu_id'])

            # Add Menu Name element with textId reference (reverse lookup from name)
            if menu['name']:
                cursor.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = ? AND text_value = ? AND language_code = 'en'
                    LIMIT 1
                """, (device_id, menu['name']))
                name_text_id_row = cursor.fetchone()
                if name_text_id_row:
                    name_elem = ET.SubElement(menu_elem, 'Name')
                    name_elem.set('textId', name_text_id_row['text_id'])

            # Get menu items for this menu
            cursor.execute("""
                SELECT * FROM ui_menu_items
                WHERE menu_id = ?
                ORDER BY item_order
            """, (menu['id'],))
            menu_items = cursor.fetchall()

            for item in menu_items:
                # VariableRef or RecordItemRef
                if item['variable_id']:
                    # VariableRef
                    var_ref = ET.SubElement(menu_elem, 'VariableRef')
                    var_ref.set('variableId', item['variable_id'])
                    if item['access_right_restriction']:
                        var_ref.set('accessRightRestriction', item['access_right_restriction'])
                    if item['display_format']:
                        var_ref.set('displayFormat', item['display_format'])
                    if item['unit_code']:
                        var_ref.set('unitCode', item['unit_code'])
                    if item['gradient']:
                        var_ref.set('gradient', str(item['gradient']))
                    if item['offset']:
                        var_ref.set('offset', str(item['offset']))
                elif item['record_item_ref']:
                    # RecordItemRef
                    record_ref = ET.SubElement(menu_elem, 'RecordItemRef')
                    record_ref.set('variableId', item['record_item_ref'])
                    if item['subindex']:
                        record_ref.set('subindex', str(item['subindex']))
                    if item['access_right_restriction']:
                        record_ref.set('accessRightRestriction', item['access_right_restriction'])
                    if item['display_format']:
                        record_ref.set('displayFormat', item['display_format'])
                    if item['unit_code']:
                        record_ref.set('unitCode', item['unit_code'])
                    if item['gradient']:
                        record_ref.set('gradient', str(item['gradient']))
                    if item['offset']:
                        record_ref.set('offset', str(item['offset']))
                elif item['button_value']:
                    # Button
                    button = ET.SubElement(menu_elem, 'Button')
                    button.set('buttonValue', item['button_value'])
                    if item['access_right_restriction']:
                        button.set('accessRightRestriction', item['access_right_restriction'])
                elif item['menu_ref']:
                    # MenuRef
                    menu_ref = ET.SubElement(menu_elem, 'MenuRef')
                    menu_ref.set('menuId', item['menu_ref'])

        # Role Menu Sets - get from ui_menu_roles table
        cursor.execute("""
            SELECT DISTINCT role_type FROM ui_menu_roles WHERE device_id = ?
        """, (device_id,))
        role_types = cursor.fetchall()

        for role_type_row in role_types:
            role_type = role_type_row['role_type']

            # Create role menu set element
            if role_type == 'observer':
                role_set = ET.SubElement(user_interface, 'ObserverRoleMenuSet')
            elif role_type == 'maintenance':
                role_set = ET.SubElement(user_interface, 'MaintenanceRoleMenuSet')
            elif role_type == 'specialist':
                role_set = ET.SubElement(user_interface, 'SpecialistRoleMenuSet')
            else:
                continue  # Unknown role type

            # Get menu types for this role
            cursor.execute("""
                SELECT menu_type, menu_id FROM ui_menu_roles
                WHERE device_id = ? AND role_type = ?
                ORDER BY menu_type
            """, (device_id, role_type))
            role_menus = cursor.fetchall()

            for role_menu in role_menus:
                menu_type = role_menu['menu_type']
                menu_id = role_menu['menu_id']

                if menu_type == 'IdentificationMenu':
                    id_menu = ET.SubElement(role_set, 'IdentificationMenu')
                    id_menu.set('menuId', menu_id)
                elif menu_type == 'ParameterMenu':
                    param_menu = ET.SubElement(role_set, 'ParameterMenu')
                    param_menu.set('menuId', menu_id)
                elif menu_type == 'ObservationMenu':
                    obs_menu = ET.SubElement(role_set, 'ObservationMenu')
                    obs_menu.set('menuId', menu_id)
                elif menu_type == 'DiagnosisMenu':
                    diag_menu = ET.SubElement(role_set, 'DiagnosisMenu')
                    diag_menu.set('menuId', menu_id)

        return user_interface

    def _create_variable_collection(self, conn: sqlite3.Connection,
                                    device_id: int) -> Optional[ET.Element]:
        """Create VariableCollection from parameters table

        NOTE: This is a simplified implementation. Full variable reconstruction would require
        storing all variable attributes (excludedFromDataStorage, fixedLengthRestriction,
        SingleValue elements, etc.) in a dedicated variables table with proper schema.
        Current parameters table only stores basic parameter info.
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM parameters WHERE device_id = ?
            ORDER BY param_index
        """, (device_id,))
        parameters = cursor.fetchall()

        if not parameters:
            return None

        collection = ET.Element('VariableCollection')

        # Create placeholder comment noting this is simplified
        collection.append(ET.Comment('Simplified variable collection - full reconstruction requires variable schema'))

        # For now, just create empty StdVariableRef elements for each parameter
        # This at least creates the VariableCollection structure
        for param in parameters:
            # Skip parameters that don't map to variables (indexes < 12 are typically system params)
            if param['param_index'] < 12:
                continue

            # Create a variable ID from the parameter name
            var_id = param['name'].replace(' ', '').replace('-', '_')
            if not var_id.startswith('V_'):
                var_id = f"V_{var_id}"

            var_ref = ET.SubElement(collection, 'StdVariableRef')
            var_ref.set('id', var_id)
            var_ref.set('excludedFromDataStorage', 'false')

        return collection

    def _create_error_type_collection(self, conn: sqlite3.Connection,
                                      device_id: int) -> Optional[ET.Element]:
        """Create ErrorTypeCollection from error_types table"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT code, additional_code FROM error_types
            WHERE device_id = ?
            ORDER BY additional_code
        """, (device_id,))
        error_types = cursor.fetchall()

        if not error_types:
            return None

        collection = ET.Element('ErrorTypeCollection')

        for error in error_types:
            error_ref = ET.SubElement(collection, 'StdErrorTypeRef')
            error_ref.set('code', str(error['code']))
            error_ref.set('additionalCode', str(error['additional_code']))

        return collection

    def _create_event_collection(self, conn: sqlite3.Connection,
                                 device_id: int) -> Optional[ET.Element]:
        """Create EventCollection from events table"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT code, name, description, event_type FROM events
            WHERE device_id = ?
            ORDER BY code
        """, (device_id,))
        events = cursor.fetchall()

        if not events:
            return None

        collection = ET.Element('EventCollection')

        for event in events:
            event_elem = ET.SubElement(collection, 'Event')
            event_elem.set('code', str(event['code']))
            if event['event_type']:
                event_elem.set('type', event['event_type'])

            # Lookup text IDs for name and description
            if event['name']:
                cursor.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = ? AND text_value = ? AND language_code = 'en'
                    LIMIT 1
                """, (device_id, event['name']))
                name_text_id_row = cursor.fetchone()
                if name_text_id_row:
                    name_elem = ET.SubElement(event_elem, 'Name')
                    name_elem.set('textId', name_text_id_row['text_id'])

            if event['description']:
                cursor.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = ? AND text_value = ? AND language_code = 'en'
                    LIMIT 1
                """, (device_id, event['description']))
                desc_text_id_row = cursor.fetchone()
                if desc_text_id_row:
                    desc_elem = ET.SubElement(event_elem, 'Description')
                    desc_elem.set('textId', desc_text_id_row['text_id'])

        return collection

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
            # ORDER BY id preserves original XML order (insertion order)
            cursor.execute("""
                SELECT text_id, text_value FROM iodd_text
                WHERE device_id = ? AND language_code = ?
                ORDER BY id
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
