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

            # Add DocumentInfo (Phase 3 Task 9a)
            document_info = self._create_document_info(conn, device_id)
            if document_info is not None:
                root.append(document_info)

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
        # Note: xmlns:xsi gets added automatically by ElementTree when we use {http://www.w3.org/2001/XMLSchema-instance}
        root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
                 'http://www.io-link.com/IODD/2010/10 IODD1.1.xsd')

        return root

    def _create_document_info(self, conn: sqlite3.Connection, device_id: int) -> Optional[ET.Element]:
        """Create DocumentInfo element (Phase 3 Task 9a)"""
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM document_info WHERE device_id = ?", (device_id,))
        doc_info_row = cursor.fetchone()

        if not doc_info_row:
            return None

        doc_info = ET.Element('DocumentInfo')

        if doc_info_row['version']:
            doc_info.set('version', doc_info_row['version'])
        if doc_info_row['release_date']:
            doc_info.set('releaseDate', doc_info_row['release_date'])
        if doc_info_row['copyright']:
            doc_info.set('copyright', doc_info_row['copyright'])

        return doc_info

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

        # VendorText - reference to text describing vendor (Phase 2 Task 8)
        vendor_text = ET.SubElement(device_identity, 'VendorText')
        vendor_text.set('textId', 'TN_VendorText')

        # VendorUrl - reference to vendor website (Phase 2 Task 8)
        vendor_url = ET.SubElement(device_identity, 'VendorUrl')
        vendor_url.set('textId', 'TN_VendorUrl')

        # VendorLogo - if logo file exists
        vendor_logo = ET.SubElement(device_identity, 'VendorLogo')
        if device['vendor_logo_filename']:
            vendor_logo.set('name', device['vendor_logo_filename'])
        else:
            # Use manufacturer name to create logo filename
            vendor_logo.set('name', f"{device['manufacturer'].replace(' ', '-')}-logo.png" if device['manufacturer'] else 'vendor-logo.png')

        # DeviceName (Phase 2 Task 8)
        device_name_elem = ET.SubElement(device_identity, 'DeviceName')
        device_name_elem.set('textId', 'TN_DeviceName')

        # DeviceFamily (Phase 2 Task 8)
        device_family = ET.SubElement(device_identity, 'DeviceFamily')
        device_family.set('textId', 'TN_DeviceFamily')

        # DeviceVariantCollection - device variants/models
        device_variant_coll = ET.SubElement(device_identity, 'DeviceVariantCollection')

        # Query variant data from database
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, device_symbol, device_icon, name, description
            FROM device_variants
            WHERE device_id = ?
            LIMIT 1
        """, (device_id,))
        variant_row = cursor.fetchone()

        device_variant = ET.SubElement(device_variant_coll, 'DeviceVariant')

        # Use proper product_id from variant table
        if variant_row and variant_row['product_id']:
            device_variant.set('productId', variant_row['product_id'])
        elif device['product_name']:
            device_variant.set('productId', device['product_name'])

        # Add deviceSymbol and deviceIcon attributes (Phase 1 Task 4)
        if variant_row and variant_row['device_symbol']:
            device_variant.set('deviceSymbol', variant_row['device_symbol'])
        if variant_row and variant_row['device_icon']:
            device_variant.set('deviceIcon', variant_row['device_icon'])

        # Add variant name with proper text ID (Phase 2 Task 8)
        variant_name = ET.SubElement(device_variant, 'Name')
        if variant_row and variant_row['product_id']:
            variant_name.set('textId', f"TN_Variant_{variant_row['product_id']}")
        else:
            variant_name.set('textId', 'TN_Variant')

        # Add variant description with proper text ID (Phase 2 Task 8)
        variant_desc = ET.SubElement(device_variant, 'Description')
        if variant_row and variant_row['product_id']:
            variant_desc.set('textId', f"TD_Variant_{variant_row['product_id']}")
        else:
            variant_desc.set('textId', 'TD_Variant')

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
        if features_row['profile_characteristic']:
            features.set('profileCharacteristic', str(features_row['profile_characteristic']))

        # Add SupportedAccessLocks (Phase 3 Task 9b)
        access_locks = ET.SubElement(features, 'SupportedAccessLocks')
        access_locks.set('localUserInterface', 'false' if not features_row['access_locks_local_user_interface'] else 'true')
        access_locks.set('dataStorage', 'false' if not features_row['access_locks_data_storage'] else 'true')
        access_locks.set('parameter', 'false' if not features_row['access_locks_parameter'] else 'true')
        access_locks.set('localParameterization', 'false' if not features_row['access_locks_local_parameterization'] else 'true')

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

            # Convert ProcessData ID format:
            # PI_Data -> P_Data, PO_Data -> P_Data (strip I/O indicator)
            # PD_ProcessDataA00In -> PD_ProcessDataA00 (strip In/Out suffix)
            pd_id = pd['pd_id']
            if pd_id.startswith('PI_'):
                pd_id = 'P_' + pd_id[3:]  # PI_Data -> P_Data
            elif pd_id.startswith('PO_'):
                pd_id = 'P_' + pd_id[3:]  # PO_Data -> P_Data
            elif pd_id.endswith('In') or pd_id.endswith('Out'):
                # Remove "In" or "Out" suffix for other formats
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
                        # Add bitLength to Datatype element as well
                        if pd['bit_length']:
                            datatype.set('bitLength', str(pd['bit_length']))
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

            # Phase 2 Task 6: Add proper xsi:type attribute with namespace
            if dt['datatype_xsi_type']:
                datatype_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type',
                                 dt['datatype_xsi_type'])

            # Phase 2 Task 7: Add subindexAccessSupported attribute for RecordT types
            if dt['subindex_access_supported']:
                datatype_elem.set('subindexAccessSupported', 'true')

            # Add bitLength attribute if present
            if dt['bit_length']:
                datatype_elem.set('bitLength', str(dt['bit_length']))

            # Add SingleValue enumerations
            self._add_single_values(conn, datatype_elem, dt['id'])

            # Add RecordItem structures
            self._add_record_items(conn, datatype_elem, dt['id'])

            collection.append(datatype_elem)

        return collection

    def _add_single_values(self, conn: sqlite3.Connection, parent: ET.Element,
                          datatype_id: int) -> None:
        """Add SingleValue enumeration values (Phase 3 Task 10a - direct children, no wrapper)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM custom_datatype_single_values
            WHERE datatype_id = ? ORDER BY value
        """, (datatype_id,))
        values = cursor.fetchall()

        if not values:
            return

        # Add SingleValue elements directly to parent (no wrapper list)
        for val in values:
            value_elem = ET.SubElement(parent, 'SingleValue')
            value_elem.set('value', str(val['value']))

            if val['name']:
                name = ET.SubElement(value_elem, 'Name')
                # Try to find the original text ID from iodd_text table
                cursor2 = conn.cursor()
                cursor2.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = (SELECT device_id FROM custom_datatypes WHERE id = ?)
                    AND text_value = ?
                    AND text_id LIKE 'TN_SV_%'
                    LIMIT 1
                """, (datatype_id, val['name']))
                text_id_row = cursor2.fetchone()
                if text_id_row:
                    name.set('textId', text_id_row['text_id'])
                else:
                    # Fallback: generate a text ID from the name
                    name.set('textId', 'TN_SV_' + val['name'].replace(' ', '').replace('-', '_'))

    def _add_record_items(self, conn: sqlite3.Connection, parent: ET.Element,
                         datatype_id: int) -> None:
        """Add RecordItem structure fields (Phase 3 Task 10a - direct children, no wrapper)"""
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM custom_datatype_record_items
            WHERE datatype_id = ? ORDER BY subindex
        """, (datatype_id,))
        items = cursor.fetchall()

        if not items:
            return

        # Add RecordItem elements directly to parent (no wrapper list)
        for item in items:
            record_elem = ET.SubElement(parent, 'RecordItem')
            record_elem.set('subindex', str(item['subindex']))
            if item['bit_offset'] is not None:
                record_elem.set('bitOffset', str(item['bit_offset']))

            if item['name']:
                name = ET.SubElement(record_elem, 'Name')
                # Try to find the original text ID from iodd_text table
                cursor2 = conn.cursor()
                cursor2.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = (SELECT device_id FROM custom_datatypes WHERE id = ?)
                    AND text_value = ?
                    AND text_id LIKE 'TN_RI_%'
                    LIMIT 1
                """, (datatype_id, item['name']))
                text_id_row = cursor2.fetchone()
                if text_id_row:
                    name.set('textId', text_id_row['text_id'])
                else:
                    # Try by subindex pattern for known record item structures
                    # Some record items have special naming conventions
                    clean_name = item['name'].replace(' ', '').replace('-', '_')
                    name.set('textId', 'TN_RI_' + clean_name)

            # Determine whether to use DatatypeRef or SimpleDatatype
            # Base types (ending in 'T' like UIntegerT, IntegerT, StringT) use SimpleDatatype
            # Custom datatype references (like D_OutputFunction, D_Percentage) use DatatypeRef
            base_types = {'UIntegerT', 'IntegerT', 'StringT', 'BooleanT', 'Float32T', 'OctetStringT'}

            if item['datatype_ref']:
                if item['datatype_ref'] in base_types:
                    # Base type - use SimpleDatatype with xsi:type
                    datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                    datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', item['datatype_ref'])
                    if item['bit_length']:
                        datatype.set('bitLength', str(item['bit_length']))
                else:
                    # Custom datatype reference - use DatatypeRef
                    datatype = ET.SubElement(record_elem, 'DatatypeRef')
                    datatype.set('datatypeId', item['datatype_ref'])
            elif item['bit_length']:
                # Fallback: create SimpleDatatype with bit_length
                datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                if item['bit_length']:
                    datatype.set('bitLength', str(item['bit_length']))
                if item.get('xsi_type'):
                    datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', item['xsi_type'])

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

        # Get device info for standard variable default values
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()

        # Get variant info for ProductID
        cursor.execute("SELECT product_id FROM device_variants WHERE device_id = ? LIMIT 1", (device_id,))
        variant_row = cursor.fetchone()

        cursor.execute("""
            SELECT * FROM parameters WHERE device_id = ?
            ORDER BY param_index
        """, (device_id,))
        parameters = cursor.fetchall()

        if not parameters and not device:
            return None

        collection = ET.Element('VariableCollection')

        # Add standard IO-Link variables (IO-Link specification defines these)
        # Order matters for proper reconstruction

        # V_DirectParameters_1 - standard IO-Link variable
        direct_params_ref = ET.SubElement(collection, 'StdVariableRef')
        direct_params_ref.set('id', 'V_DirectParameters_1')

        # V_SystemCommand - standard IO-Link variable
        sys_cmd_ref = ET.SubElement(collection, 'StdVariableRef')
        sys_cmd_ref.set('id', 'V_SystemCommand')

        # V_VendorName - defaultValue from manufacturer
        vendor_name_ref = ET.SubElement(collection, 'StdVariableRef')
        vendor_name_ref.set('id', 'V_VendorName')
        if device and device['manufacturer']:
            vendor_name_ref.set('defaultValue', device['manufacturer'])

        # V_ProductName - defaultValue from product name
        product_name_ref = ET.SubElement(collection, 'StdVariableRef')
        product_name_ref.set('id', 'V_ProductName')
        # Note: Use short product name if available, otherwise use device product_name
        if device and device['product_name']:
            # Try to extract the short product name (e.g., "CALIS" from "CALIS Level Sensor")
            short_name = device['product_name'].split()[0] if device['product_name'] else None
            if short_name:
                product_name_ref.set('defaultValue', short_name)

        # V_ProductText - standard IO-Link variable (no default)
        product_text_ref = ET.SubElement(collection, 'StdVariableRef')
        product_text_ref.set('id', 'V_ProductText')

        # V_ProductID - defaultValue from variant product_id
        product_id_ref = ET.SubElement(collection, 'StdVariableRef')
        product_id_ref.set('id', 'V_ProductID')
        if variant_row and variant_row['product_id']:
            product_id_ref.set('defaultValue', variant_row['product_id'])

        # V_SerialNumber - standard IO-Link variable (no default)
        serial_ref = ET.SubElement(collection, 'StdVariableRef')
        serial_ref.set('id', 'V_SerialNumber')

        # V_HardwareRevision - standard IO-Link variable (no default)
        hw_rev_ref = ET.SubElement(collection, 'StdVariableRef')
        hw_rev_ref.set('id', 'V_HardwareRevision')

        # V_FirmwareRevision - standard IO-Link variable (no default)
        fw_rev_ref = ET.SubElement(collection, 'StdVariableRef')
        fw_rev_ref.set('id', 'V_FirmwareRevision')

        # V_ApplicationSpecificTag - standard IO-Link variable (no default)
        app_tag_ref = ET.SubElement(collection, 'StdVariableRef')
        app_tag_ref.set('id', 'V_ApplicationSpecificTag')
        app_tag_ref.set('excludedFromDataStorage', 'false')

        # V_DeviceStatus - standard IO-Link variable (defaultValue="0")
        device_status_ref = ET.SubElement(collection, 'StdVariableRef')
        device_status_ref.set('id', 'V_DeviceStatus')
        device_status_ref.set('defaultValue', '0')

        # V_DetailedDeviceStatus - standard IO-Link variable (with fixedLengthRestriction)
        detailed_status_ref = ET.SubElement(collection, 'StdVariableRef')
        detailed_status_ref.set('id', 'V_DetailedDeviceStatus')
        detailed_status_ref.set('fixedLengthRestriction', '8')

        # Phase 3 Task 9c: Create Variable elements from parameters (indices >= 25)
        for param in parameters:
            # Skip parameters with index < 25 (system/standard variables)
            if param['param_index'] < 25:
                continue

            # Use stored variable_id if available, otherwise generate from name
            var_id = param['variable_id'] if param['variable_id'] else \
                     'V_' + param['name'].replace(' ', '').replace('"', '').replace('-', '_').replace('/', '_')

            variable = ET.SubElement(collection, 'Variable')
            variable.set('id', var_id)
            variable.set('index', str(param['param_index']))

            # Access rights
            if param['access_rights']:
                variable.set('accessRights', param['access_rights'])

            # Dynamic attribute
            if param['dynamic']:
                variable.set('dynamic', 'true')

            # Excluded from data storage (add attribute if explicitly set to false for StringT vars)
            if param['data_type'] == 'StringT' and var_id in ('V_CP_FunctionTag', 'V_CP_LocationTag'):
                variable.set('excludedFromDataStorage', 'false')
            elif param['excluded_from_data_storage']:
                variable.set('excludedFromDataStorage', 'true')

            # Determine if we should use DatatypeRef or Datatype based on data type
            # Custom datatypes (like D_Percentage, D_Distance, D_Reference, D_LevelOutput) use DatatypeRef
            # Base types (UIntegerT, IntegerT, StringT, etc.) use Datatype element
            custom_datatype_map = {
                'V_ContainerLowLevel': 'D_Percentage',
                'V_ContainerHighLevel': 'D_Percentage',
                'V_SensorLowLevel': 'D_Distance',
                'V_SensorHighLevel': 'D_Distance',
                'V_LevelOutput_Pin4': 'D_LevelOutput',
                'V_AdditionalReference0': 'D_Reference',
                'V_AdditionalReference1': 'D_Reference',
                'V_AdditionalReference2': 'D_Reference',
                'V_AdditionalReference3': 'D_Reference',
                'V_ValidRange': 'D_Distance',
            }

            if var_id in custom_datatype_map:
                # Use DatatypeRef for variables that reference custom datatypes
                datatyperef_elem = ET.SubElement(variable, 'DatatypeRef')
                datatyperef_elem.set('datatypeId', custom_datatype_map[var_id])
            else:
                # Create Datatype element for base types
                datatype_elem = ET.SubElement(variable, 'Datatype')
                if param['data_type']:
                    datatype_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', param['data_type'])
                if param['bit_length']:
                    datatype_elem.set('bitLength', str(param['bit_length']))

                # Add string encoding/fixedLength for StringT
                if param['data_type'] == 'StringT':
                    datatype_elem.set('encoding', 'UTF-8')
                    # Determine fixedLength based on variable ID
                    if var_id == 'V_FU_HW_ID_Key':
                        datatype_elem.set('fixedLength', '16')
                    else:
                        datatype_elem.set('fixedLength', '32')

            # Add ValueRange if min/max defined and we created a Datatype element (not DatatypeRef)
            if var_id not in custom_datatype_map:
                if param['min_value'] is not None or param['max_value'] is not None:
                    value_range = ET.SubElement(datatype_elem, 'ValueRange')
                    if param['min_value'] is not None:
                        value_range.set('lowerValue', str(param['min_value']))
                    if param['max_value'] is not None:
                        value_range.set('upperValue', str(param['max_value']))

            # Look up Name and Description text IDs
            cursor2 = conn.cursor()

            # Try to find Name text ID
            cursor2.execute("""
                SELECT text_id FROM iodd_text
                WHERE device_id = ? AND text_value = ? AND text_id LIKE 'TN_V_%'
                LIMIT 1
            """, (device_id, param['name']))
            name_text_row = cursor2.fetchone()

            if name_text_row:
                name_elem = ET.SubElement(variable, 'Name')
                name_elem.set('textId', name_text_row['text_id'])
            else:
                # Generate text ID from variable name
                name_elem = ET.SubElement(variable, 'Name')
                name_elem.set('textId', f'TN_{var_id}')

            # Try to find Description text ID
            if param['description']:
                cursor2.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = ? AND text_value LIKE ? AND text_id LIKE 'TD_V_%'
                    LIMIT 1
                """, (device_id, f"%{param['description'][:50]}%"))
                desc_text_row = cursor2.fetchone()

                if desc_text_row:
                    desc_elem = ET.SubElement(variable, 'Description')
                    desc_elem.set('textId', desc_text_row['text_id'])

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
