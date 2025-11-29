"""
Forensic XML Reconstruction Engine v2 (Aligned with Actual Schema)

Reconstructs IODD XML files from database tables for Parser Quality Assurance.
This version is aligned with the actual GreenStack database schema.
"""

import logging
import re
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

    # Known IODD schema namespaces and XSD files
    SCHEMA_CONFIGS = {
        '1.1': {
            'namespace': 'http://www.io-link.com/IODD/2010/10',
            'xsd': 'IODD1.1.xsd'
        },
        '1.0.1': {
            'namespace': 'http://www.io-link.com/IODD/2009/11',
            'xsd': 'IODD1.0.1.xsd'
        },
        '1.0': {  # PQA Fix #81: IODD 1.0 uses 2008/03 namespace
            'namespace': 'http://www.io-link.com/IODD/2008/03',
            'xsd': 'IODD1.0.xsd'
        },
    }

    DEFAULT_SCHEMA_VERSION = '1.1'

    @staticmethod
    def _format_number(value) -> str:
        """Format a numeric value for XML output, preserving original precision.

        Handles:
        - Integers: returns as-is without decimal point (e.g., 24)
        - Floats with integer value: returns without decimal (e.g., 24.0 -> 24)
        - Floats with decimal: preserves decimal, removes trailing zeros (e.g., 0.10 -> 0.1)
        - Leading zero preservation: .1 stays as .1, 0.1 stays as 0.1 based on original
        """
        if value is None:
            return ''

        # If it's an integer, return as integer string
        if isinstance(value, int):
            return str(value)

        # If it's a float
        if isinstance(value, float):
            # Check if it's a whole number - keep .0 suffix for floats (PQA Fix)
            if value == int(value):
                return f"{int(value)}.0"
            # Format with enough precision and strip trailing zeros
            formatted = f'{value:.10g}'  # Uses scientific notation for very large/small numbers
            return formatted

        # Otherwise return string representation
        return str(value)

    def __init__(self, db_path: str = "greenstack.db"):
        self.db_path = db_path
        # Default namespace registration (will be updated per-device)
        ET.register_namespace('xsi', 'http://www.w3.org/2001/XMLSchema-instance')
        # Default to 1.1 - this will be updated dynamically per device
        self._current_namespace = self.SCHEMA_CONFIGS['1.1']['namespace']
        ET.register_namespace('', self._current_namespace)

    def get_connection(self) -> sqlite3.Connection:
        """Get database connection with Row factory"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _get_schema_version(self, conn: sqlite3.Connection, device_id: int) -> str:
        """Get schema version for a device from iodd_files table

        Args:
            conn: Database connection
            device_id: Device ID

        Returns:
            Schema version string (e.g., '1.1', '1.0.1', '1.0')
        """
        cursor = conn.cursor()
        cursor.execute("SELECT schema_version FROM iodd_files WHERE device_id = ?", (device_id,))
        row = cursor.fetchone()
        if row and row['schema_version']:
            return row['schema_version']
        return self.DEFAULT_SCHEMA_VERSION

    def _get_schema_config(self, schema_version: str) -> dict:
        """Get schema configuration for a version

        Args:
            schema_version: Version string

        Returns:
            Dict with 'namespace' and 'xsd' keys
        """
        # PQA Fix #99: Normalize schema version (e.g., "1.00" -> "1.0", "1.10" -> "1.1")
        normalized_version = schema_version
        if schema_version and schema_version not in self.SCHEMA_CONFIGS:
            # Try normalizing: remove trailing zeros after decimal point
            # "1.00" -> "1.0", "1.10" -> "1.1", "1.0.10" -> "1.0.1"
            parts = schema_version.split('.')
            if len(parts) >= 2:
                # Remove trailing zeros from each part
                normalized_parts = [parts[0]]  # Keep major version as is
                for part in parts[1:]:
                    # Convert to int and back to string to remove leading zeros
                    try:
                        normalized_parts.append(str(int(part)))
                    except ValueError:
                        normalized_parts.append(part)
                normalized_version = '.'.join(normalized_parts)

        if normalized_version in self.SCHEMA_CONFIGS:
            return self.SCHEMA_CONFIGS[normalized_version]

        # Fallback to default
        logger.warning(f"Unknown schema version '{schema_version}' (normalized: '{normalized_version}'), falling back to {self.DEFAULT_SCHEMA_VERSION}")
        return self.SCHEMA_CONFIGS[self.DEFAULT_SCHEMA_VERSION]

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
            profile_header = self._create_profile_header(conn, device_id)
            if profile_header is not None:
                root.append(profile_header)

            # Add ProfileBody
            profile_body = self._create_profile_body(conn, device_id, device)
            if profile_body is not None:
                root.append(profile_body)

            # Add CommNetworkProfile (direct child of IODevice, not ProfileBody)
            comm_network_profile = self._create_comm_network_profile(conn, device_id)
            if comm_network_profile is not None:
                root.append(comm_network_profile)

            # Add Stamp (direct child of IODevice, contains CRC and Checker info)
            stamp = self._create_stamp(conn, device_id)
            if stamp is not None:
                root.append(stamp)

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

    def _lookup_textid(self, conn: sqlite3.Connection, device_id: int,
                       text_value: str, fallback_patterns: list) -> str:
        """
        Look up the original textId from iodd_text table by text value.
        Falls back to trying common prefix patterns if exact match not found.

        Args:
            conn: Database connection
            device_id: Device ID
            text_value: The text value to look up
            fallback_patterns: List of pattern prefixes to try (e.g., ['TI_', 'TN_'])

        Returns:
            The original textId or a generated fallback
        """
        cursor = conn.cursor()

        # First try exact match on text_value
        cursor.execute("""
            SELECT text_id FROM iodd_text
            WHERE device_id = ? AND text_value = ?
            LIMIT 1
        """, (device_id, text_value))
        row = cursor.fetchone()
        if row:
            return row['text_id']

        # Try each fallback pattern
        for pattern in fallback_patterns:
            cursor.execute("""
                SELECT text_id FROM iodd_text
                WHERE device_id = ? AND text_id LIKE ?
                LIMIT 1
            """, (device_id, pattern + '%'))
            row = cursor.fetchone()
            if row:
                return row['text_id']

        # Final fallback: generate using first pattern
        return fallback_patterns[0] if fallback_patterns else 'TN_Unknown'

    def _create_root_element(self, conn: sqlite3.Connection, device_id: int,
                            device: sqlite3.Row) -> ET.Element:
        """Create root IODevice element with correct namespace based on schema version"""
        root = ET.Element('IODevice')

        # Get schema configuration for this device
        schema_version = self._get_schema_version(conn, device_id)
        schema_config = self._get_schema_config(schema_version)
        namespace = schema_config['namespace']
        xsd_file = schema_config['xsd']

        # Store namespace for potential use in child elements
        self._current_namespace = namespace
        # Re-register default namespace for this device
        ET.register_namespace('', namespace)

        # Add namespaces
        root.set('xmlns', namespace)
        # Note: xmlns:xsi gets added automatically by ElementTree when we use {http://www.w3.org/2001/XMLSchema-instance}
        root.set('{http://www.w3.org/2001/XMLSchema-instance}schemaLocation',
                 f'{namespace} {xsd_file}')

        logger.debug(f"Using schema version {schema_version} with namespace {namespace} for device {device_id}")
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

    def _create_profile_header(self, conn: sqlite3.Connection, device_id: int) -> ET.Element:
        """Create ProfileHeader with standard IO-Link profile information

        PQA Fix #54: Use stored ProfileHeader values from iodd_files table
        instead of hardcoded defaults.
        """
        header = ET.Element('ProfileHeader')

        # Query stored ProfileHeader values from iodd_files
        cursor = conn.execute("""
            SELECT profile_identification, profile_revision, profile_name
            FROM iodd_files WHERE device_id = ?
        """, (device_id,))
        row = cursor.fetchone()

        # Use stored values or fall back to defaults
        stored_identification = row['profile_identification'] if row and row['profile_identification'] else None
        stored_revision = row['profile_revision'] if row and row['profile_revision'] else None
        stored_name = row['profile_name'] if row and row['profile_name'] else None

        # Profile Identification
        profile_id = ET.SubElement(header, 'ProfileIdentification')
        profile_id.text = stored_identification or 'IO Device Profile'

        # Profile Revision
        profile_rev = ET.SubElement(header, 'ProfileRevision')
        profile_rev.text = stored_revision or '1.1'

        # Profile Name
        profile_name = ET.SubElement(header, 'ProfileName')
        profile_name.text = stored_name or 'Device Profile for IO Devices'

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
        # PQA Fix #62: Use original string format if available (preserves leading zeros)
        device_id_str = device['device_id_str'] if 'device_id_str' in device.keys() and device['device_id_str'] else str(device['device_id'])
        device_identity.set('deviceId', device_id_str)

        if device['vendor_id']:
            device_identity.set('vendorId', str(device['vendor_id']))

        if device['manufacturer']:
            device_identity.set('vendorName', device['manufacturer'])

        # PQA Fix #85: Add additionalDeviceIds attribute if present
        if 'additional_device_ids' in device.keys() and device['additional_device_ids']:
            device_identity.set('additionalDeviceIds', device['additional_device_ids'])

        # VendorText - use stored textId (PQA Fix #24), fallback to lookup
        vendor_text = ET.SubElement(device_identity, 'VendorText')
        vendor_text_id = device['vendor_text_text_id'] if 'vendor_text_text_id' in device.keys() and device['vendor_text_text_id'] else None
        if not vendor_text_id:
            vendor_text_id = self._lookup_textid(conn, device_id, None, ['TI_VendorText', 'TN_VendorText', 'T_VendorText'])
        vendor_text.set('textId', vendor_text_id)

        # VendorUrl - use stored textId (PQA Fix #24), fallback to lookup
        vendor_url = ET.SubElement(device_identity, 'VendorUrl')
        vendor_url_id = device['vendor_url_text_id'] if 'vendor_url_text_id' in device.keys() and device['vendor_url_text_id'] else None
        if not vendor_url_id:
            vendor_url_id = self._lookup_textid(conn, device_id, None, ['TI_VendorUrl', 'TN_VendorUrl', 'T_VendorUrl'])
        vendor_url.set('textId', vendor_url_id)

        # VendorLogo - PQA Fix #83: Only output when present in original IODD
        if device['vendor_logo_filename']:
            vendor_logo = ET.SubElement(device_identity, 'VendorLogo')
            vendor_logo.set('name', device['vendor_logo_filename'])

        # DeviceName - PQA Fix #55: Only output when present in original IODD
        device_name_id = device['device_name_text_id'] if 'device_name_text_id' in device.keys() else None
        if device_name_id:
            device_name_elem = ET.SubElement(device_identity, 'DeviceName')
            device_name_elem.set('textId', device_name_id)

        # DeviceFamily - use stored textId (PQA Fix #24), fallback to lookup
        device_family = ET.SubElement(device_identity, 'DeviceFamily')
        device_family_id = device['device_family_text_id'] if 'device_family_text_id' in device.keys() and device['device_family_text_id'] else None
        if not device_family_id:
            device_family_id = self._lookup_textid(conn, device_id, None, ['TI_DeviceFamily', 'TN_DeviceFamily', 'T_DeviceFamily'])
        device_family.set('textId', device_family_id)

        # DeviceVariantCollection - device variants/models
        device_variant_coll = ET.SubElement(device_identity, 'DeviceVariantCollection')

        # Query variant data from database (including PQA textId fields)
        # PQA Fix #40: Added ProductName/ProductText fields
        # PQA Fix #58: Added hardware_revision, firmware_revision
        cursor = conn.cursor()
        cursor.execute("""
            SELECT product_id, device_symbol, device_icon, name, description,
                   name_text_id, description_text_id,
                   product_name_text_id, product_text_text_id,
                   has_name, has_description, has_product_name, has_product_text,
                   hardware_revision, firmware_revision
            FROM device_variants
            WHERE device_id = ?
            LIMIT 1
        """, (device_id,))
        variant_row = cursor.fetchone()

        device_variant = ET.SubElement(device_variant_coll, 'DeviceVariant')

        # PQA Fix #78: Always output productId attribute, even if empty
        if variant_row and 'product_id' in variant_row.keys():
            device_variant.set('productId', variant_row['product_id'] or '')
        elif device['product_name']:
            device_variant.set('productId', device['product_name'])

        # Add deviceSymbol and deviceIcon attributes (Phase 1 Task 4)
        if variant_row and variant_row['device_symbol']:
            device_variant.set('deviceSymbol', variant_row['device_symbol'])
        if variant_row and variant_row['device_icon']:
            device_variant.set('deviceIcon', variant_row['device_icon'])

        # PQA Fix #58: Add hardware/firmware revision attributes
        # Output even when empty string (but not when NULL/None)
        if variant_row and 'hardware_revision' in variant_row.keys() and variant_row['hardware_revision'] is not None:
            device_variant.set('hardwareRevision', variant_row['hardware_revision'])
        if variant_row and 'firmware_revision' in variant_row.keys() and variant_row['firmware_revision'] is not None:
            device_variant.set('firmwareRevision', variant_row['firmware_revision'])

        # PQA Fix #40: Output correct element type based on what was present in original
        has_name = variant_row['has_name'] if variant_row and 'has_name' in variant_row.keys() else False
        has_description = variant_row['has_description'] if variant_row and 'has_description' in variant_row.keys() else False
        has_product_name = variant_row['has_product_name'] if variant_row and 'has_product_name' in variant_row.keys() else False
        has_product_text = variant_row['has_product_text'] if variant_row and 'has_product_text' in variant_row.keys() else False

        # Output Name element if it was present
        if has_name:
            variant_name = ET.SubElement(device_variant, 'Name')
            name_text_id = variant_row['name_text_id'] if variant_row and variant_row['name_text_id'] else None
            if name_text_id:
                variant_name.set('textId', name_text_id)
            else:
                variant_name.set('textId', 'TN_Variant')

        # Output Description element if it was present
        if has_description:
            variant_desc = ET.SubElement(device_variant, 'Description')
            desc_text_id = variant_row['description_text_id'] if variant_row and variant_row['description_text_id'] else None
            if desc_text_id:
                variant_desc.set('textId', desc_text_id)
            else:
                variant_desc.set('textId', 'TD_Variant')

        # Output ProductName element if it was present (alternative to Name)
        if has_product_name:
            product_name_elem = ET.SubElement(device_variant, 'ProductName')
            pn_text_id = variant_row['product_name_text_id'] if variant_row and variant_row['product_name_text_id'] else None
            if pn_text_id:
                product_name_elem.set('textId', pn_text_id)
            else:
                product_name_elem.set('textId', 'TN_Product_Name')

        # Output ProductText element if it was present (alternative to Description)
        if has_product_text:
            product_text_elem = ET.SubElement(device_variant, 'ProductText')
            pt_text_id = variant_row['product_text_text_id'] if variant_row and variant_row['product_text_text_id'] else None
            if pt_text_id:
                product_text_elem.set('textId', pt_text_id)
            else:
                product_text_elem.set('textId', 'TD_Product_Descr')

        # Legacy fallback: if none of the flags are set (old data), output Name/Description
        if not has_name and not has_description and not has_product_name and not has_product_text:
            # Fallback for legacy data without the new flags
            variant_name = ET.SubElement(device_variant, 'Name')
            name_text_id = variant_row['name_text_id'] if variant_row and 'name_text_id' in variant_row.keys() and variant_row['name_text_id'] else None
            if name_text_id:
                variant_name.set('textId', name_text_id)
            elif variant_row and variant_row['product_id']:
                variant_name.set('textId', f"TN_Variant_{variant_row['product_id']}")
            else:
                variant_name.set('textId', 'TN_Variant')

            variant_desc = ET.SubElement(device_variant, 'Description')
            desc_text_id = variant_row['description_text_id'] if variant_row and 'description_text_id' in variant_row.keys() and variant_row['description_text_id'] else None
            if desc_text_id:
                variant_desc.set('textId', desc_text_id)
            elif variant_row and variant_row['product_id']:
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

        # Always emit blockParameter attribute (even when false, for PQA accuracy)
        features.set('blockParameter', 'true' if features_row['block_parameter'] else 'false')
        # PQA Fix #57: Only output dataStorage if it was present in original IODD
        has_data_storage = features_row['has_data_storage'] if 'has_data_storage' in features_row.keys() else False
        if has_data_storage:
            features.set('dataStorage', 'true' if features_row['data_storage'] else 'false')
        if features_row['profile_characteristic']:
            features.set('profileCharacteristic', str(features_row['profile_characteristic']))

        # Only add SupportedAccessLocks if it was present in the original IODD
        has_access_locks = features_row['has_supported_access_locks'] if 'has_supported_access_locks' in features_row.keys() else None
        if has_access_locks:
            access_locks = ET.SubElement(features, 'SupportedAccessLocks')
            access_locks.set('localUserInterface', 'false' if not features_row['access_locks_local_user_interface'] else 'true')
            access_locks.set('dataStorage', 'false' if not features_row['access_locks_data_storage'] else 'true')
            access_locks.set('parameter', 'false' if not features_row['access_locks_parameter'] else 'true')
            access_locks.set('localParameterization', 'false' if not features_row['access_locks_local_parameterization'] else 'true')

        return features

    def _create_process_data_collection(self, conn: sqlite3.Connection,
                                       device_id: int) -> Optional[ET.Element]:
        """Create ProcessDataCollection element

        PQA Fix #34: Group ProcessDataIn and ProcessDataOut by wrapper_id so they
        appear as children of the same ProcessData element.
        """
        cursor = conn.cursor()
        # Order by original XML order (min id per wrapper), then direction (input before output)
        # PQA Fix #34b: Use MIN(id) per wrapper_id to preserve original document order
        cursor.execute("""
            SELECT pd.*, w.min_id FROM process_data pd
            JOIN (
                SELECT COALESCE(wrapper_id, pd_id) as wid, MIN(id) as min_id
                FROM process_data WHERE device_id = ?
                GROUP BY COALESCE(wrapper_id, pd_id)
            ) w ON COALESCE(pd.wrapper_id, pd.pd_id) = w.wid
            WHERE pd.device_id = ?
            ORDER BY w.min_id,
                     CASE pd.direction WHEN 'input' THEN 0 ELSE 1 END,
                     pd.id
        """, (device_id, device_id))
        process_data_rows = cursor.fetchall()

        if not process_data_rows:
            return None

        collection = ET.Element('ProcessDataCollection')

        # PQA Fix #34: Group by wrapper_id - create one ProcessData per unique wrapper
        wrapper_elements = {}  # Maps wrapper_id -> ProcessData element
        wrapper_order = []  # Preserve order of first occurrence

        for pd in process_data_rows:
            # Determine the wrapper_id for this row
            wrapper_id = pd['wrapper_id'] if 'wrapper_id' in pd.keys() and pd['wrapper_id'] else None
            if not wrapper_id:
                # Fallback: derive wrapper_id from pd_id
                pd_id = pd['pd_id']
                if pd_id.startswith('PI_'):
                    wrapper_id = 'P_' + pd_id[3:]
                elif pd_id.startswith('PO_'):
                    wrapper_id = 'P_' + pd_id[3:]
                else:
                    wrapper_id = pd_id
                # Strip direction suffixes
                wrapper_id = re.sub(r'In(_?\d*)$', r'\1', wrapper_id)
                wrapper_id = re.sub(r'Out(_?\d*)$', r'\1', wrapper_id)
                wrapper_id = re.sub(r'_IN(_?\d*)$', r'\1', wrapper_id)
                wrapper_id = re.sub(r'_OUT(_?\d*)$', r'\1', wrapper_id)

            # Get or create ProcessData element for this wrapper
            if wrapper_id in wrapper_elements:
                pd_elem = wrapper_elements[wrapper_id]
            else:
                pd_elem = ET.Element('ProcessData')
                pd_elem.set('id', wrapper_id)
                wrapper_elements[wrapper_id] = pd_elem
                wrapper_order.append(wrapper_id)

                # Check for Condition element (only add once per wrapper)
                cursor.execute("""
                    SELECT condition_variable_id, condition_value, condition_subindex
                    FROM process_data_conditions
                    WHERE process_data_id = ?
                """, (pd['id'],))
                condition = cursor.fetchone()
                if condition and condition['condition_variable_id']:
                    condition_elem = ET.SubElement(pd_elem, 'Condition')
                    condition_elem.set('variableId', condition['condition_variable_id'])
                    condition_elem.set('value', str(condition['condition_value']))
                    cond_subindex = condition['condition_subindex'] if 'condition_subindex' in condition.keys() else None
                    if cond_subindex:
                        condition_elem.set('subindex', cond_subindex)

            # Add ProcessDataIn or ProcessDataOut as child of the wrapper
            self._add_process_data_direction_element(conn, pd_elem, pd)

        # Add wrapper elements to collection in order of first occurrence
        for wrapper_id in wrapper_order:
            collection.append(wrapper_elements[wrapper_id])

        return collection

    def _add_process_data_direction_element(self, conn: sqlite3.Connection,
                                            pd_elem: ET.Element, pd) -> None:
        """Add ProcessDataIn or ProcessDataOut element to ProcessData wrapper

        PQA Fix #34: Helper method to reduce duplication when creating direction elements.
        """
        if not pd['direction']:
            return

        if pd['direction'] == 'input':
            direction_elem = ET.SubElement(pd_elem, 'ProcessDataIn')
        else:
            direction_elem = ET.SubElement(pd_elem, 'ProcessDataOut')

        direction_elem.set('id', pd['pd_id'])
        if pd['bit_length']:
            direction_elem.set('bitLength', str(pd['bit_length']))

        # Add Name element with textId (PQA accuracy)
        name_text_id = pd['name_text_id'] if 'name_text_id' in pd.keys() else None
        if name_text_id:
            name_elem = ET.SubElement(direction_elem, 'Name')
            name_elem.set('textId', name_text_id)

        # PQA Fix #53: Use DatatypeRef or inline Datatype based on original
        uses_datatype_ref = pd['uses_datatype_ref'] if 'uses_datatype_ref' in pd.keys() else False
        datatype_ref_id = pd['datatype_ref_id'] if 'datatype_ref_id' in pd.keys() else None

        if uses_datatype_ref and datatype_ref_id:
            # Use DatatypeRef to reference custom datatype
            datatype_ref = ET.SubElement(direction_elem, 'DatatypeRef')
            datatype_ref.set('datatypeId', datatype_ref_id)
        elif pd['data_type']:
            # Use inline Datatype
            datatype = ET.SubElement(direction_elem, 'Datatype')
            datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', pd['data_type'])
            # PQA Fix #77: Only output bitLength on Datatype if original had it
            datatype_has_bit_length = pd.get('datatype_has_bit_length', False) if hasattr(pd, 'get') else pd['datatype_has_bit_length'] if 'datatype_has_bit_length' in pd.keys() else False
            if pd['bit_length'] and datatype_has_bit_length:
                datatype.set('bitLength', str(pd['bit_length']))
            # PQA Fix #98: Add count attribute for ArrayT types
            array_count = pd.get('array_count') if hasattr(pd, 'get') else pd['array_count'] if 'array_count' in pd.keys() else None
            if array_count is not None:
                datatype.set('count', str(array_count))
            # Add subindexAccessSupported attribute (PQA accuracy)
            subindex_access = pd['subindex_access_supported'] if 'subindex_access_supported' in pd.keys() else None
            if subindex_access is not None:
                datatype.set('subindexAccessSupported', 'true' if subindex_access else 'false')
            # PQA Fix #72: Add Name element inside Datatype when present
            dt_name_text_id = pd['datatype_name_text_id'] if 'datatype_name_text_id' in pd.keys() else None
            if dt_name_text_id:
                dt_name_elem = ET.SubElement(datatype, 'Name')
                dt_name_elem.set('textId', dt_name_text_id)
            # Add RecordItem elements for RecordT types
            if pd['data_type'] == 'RecordT':
                self._add_process_data_record_items(conn, datatype, pd['id'])
            # PQA Fix #6B: Add SimpleDatatype child element for ArrayT types
            elif pd['data_type'] == 'ArrayT':
                array_elem_type = pd['array_element_type'] if 'array_element_type' in pd.keys() else None
                if array_elem_type:
                    simple_dt = ET.SubElement(datatype, 'SimpleDatatype')
                    simple_dt.set('{http://www.w3.org/2001/XMLSchema-instance}type', array_elem_type)
                    if pd['array_element_bit_length']:
                        simple_dt.set('bitLength', str(pd['array_element_bit_length']))
                    if pd['array_element_fixed_length']:
                        simple_dt.set('fixedLength', str(pd['array_element_fixed_length']))
                    # Add ValueRange to SimpleDatatype if present
                    ae_min = pd['array_element_min_value'] if 'array_element_min_value' in pd.keys() else None
                    ae_max = pd['array_element_max_value'] if 'array_element_max_value' in pd.keys() else None
                    if ae_min is not None or ae_max is not None:
                        vr_elem = ET.SubElement(simple_dt, 'ValueRange')
                        ae_vr_xsi_type = pd['array_element_value_range_xsi_type'] if 'array_element_value_range_xsi_type' in pd.keys() else None
                        if ae_vr_xsi_type:
                            vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', ae_vr_xsi_type)
                        if ae_min is not None:
                            vr_elem.set('lowerValue', str(ae_min))
                        if ae_max is not None:
                            vr_elem.set('upperValue', str(ae_max))
                        ae_vr_name_text_id = pd['array_element_value_range_name_text_id'] if 'array_element_value_range_name_text_id' in pd.keys() else None
                        if ae_vr_name_text_id:
                            vr_name_elem = ET.SubElement(vr_elem, 'Name')
                            vr_name_elem.set('textId', ae_vr_name_text_id)
                    # Add SingleValues to ArrayT SimpleDatatype if present
                    self._add_process_data_direct_single_values(conn, simple_dt, pd['id'])
            else:
                # PQA Fix #71: Add direct SingleValue children for non-RecordT types
                self._add_process_data_direct_single_values(conn, datatype, pd['id'])


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

        # PQA Fix #60b: Use original string format if available, else format number
        if ui_info['gradient'] is not None:
            gradient_str = ui_info.get('gradient_str') if hasattr(ui_info, 'get') else ui_info['gradient_str'] if 'gradient_str' in ui_info.keys() else None
            ui_elem.set('gradient', gradient_str if gradient_str else self._format_number(ui_info['gradient']))
        if ui_info['offset'] is not None:
            offset_str = ui_info.get('offset_str') if hasattr(ui_info, 'get') else ui_info['offset_str'] if 'offset_str' in ui_info.keys() else None
            ui_elem.set('offset', offset_str if offset_str else self._format_number(ui_info['offset']))
        if ui_info['unit_code']:
            ui_elem.set('unitCode', ui_info['unit_code'])
        if ui_info['display_format']:
            ui_elem.set('displayFormat', ui_info['display_format'])

    def _add_process_data_direct_single_values(self, conn: sqlite3.Connection, parent: ET.Element,
                                                process_data_id: int) -> None:
        """PQA Fix #71: Add direct SingleValue children to ProcessData Datatype
        
        For non-RecordT types (like BooleanT) that have SingleValue enumerations directly under Datatype.
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT value, name, name_text_id, xsi_type
            FROM process_data_single_values
            WHERE process_data_id = ?
            ORDER BY id
        """, (process_data_id,))
        single_values = cursor.fetchall()
        
        for sv in single_values:
            sv_elem = ET.SubElement(parent, 'SingleValue')
            # Add xsi:type if present
            if sv['xsi_type']:
                sv_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', sv['xsi_type'])
            sv_elem.set('value', sv['value'])
            if sv['name_text_id']:
                name_elem = ET.SubElement(sv_elem, 'Name')
                name_elem.set('textId', sv['name_text_id'])

    def _add_process_data_record_items(self, conn: sqlite3.Connection, parent: ET.Element,
                                       process_data_id: int) -> None:
        """Add RecordItem elements to ProcessData Datatype

        Queries process_data_record_items table and creates RecordItem child elements.
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM process_data_record_items
            WHERE process_data_id = ? ORDER BY subindex
        """, (process_data_id,))
        items = cursor.fetchall()

        if not items:
            return

        # Get device_id for text lookups
        cursor.execute("""
            SELECT device_id FROM process_data WHERE id = ?
        """, (process_data_id,))
        device_row = cursor.fetchone()
        device_id = device_row['device_id'] if device_row else None

        for item in items:
            record_elem = ET.SubElement(parent, 'RecordItem')
            record_elem.set('subindex', str(item['subindex']))
            if item['bit_offset'] is not None:
                record_elem.set('bitOffset', str(item['bit_offset']))
            # PQA: Add accessRightRestriction attribute if present
            access_right = item['access_right_restriction'] if 'access_right_restriction' in item.keys() else None
            if access_right:
                record_elem.set('accessRightRestriction', access_right)

            # Add SimpleDatatype or DatatypeRef based on data_type
            if item['data_type']:
                base_types = {'UIntegerT', 'IntegerT', 'StringT', 'BooleanT', 'Float32T', 'OctetStringT'}
                if item['data_type'] in base_types:
                    simple_dt = ET.SubElement(record_elem, 'SimpleDatatype')
                    simple_dt.set('{http://www.w3.org/2001/XMLSchema-instance}type', item['data_type'])
                    # BooleanT doesn't have bitLength (it's inherently 1 bit)
                    # Float32T is always 32 bits, so bitLength is typically omitted
                    if item['bit_length'] and item['data_type'] not in ('BooleanT', 'Float32T'):
                        simple_dt.set('bitLength', str(item['bit_length']))
                    # PQA: Add optional SimpleDatatype attributes
                    fixed_len = item['fixed_length'] if 'fixed_length' in item.keys() else None
                    if fixed_len:
                        simple_dt.set('fixedLength', str(fixed_len))
                    encoding = item['encoding'] if 'encoding' in item.keys() else None
                    if encoding:
                        simple_dt.set('encoding', encoding)
                    dt_id = item['datatype_id'] if 'datatype_id' in item.keys() else None
                    if dt_id:
                        simple_dt.set('id', dt_id)

                    # PQA Fix #95: Add Name element inside SimpleDatatype when present
                    sdt_name_text_id = item['simpledatatype_name_text_id'] if 'simpledatatype_name_text_id' in item.keys() else None
                    if sdt_name_text_id:
                        sdt_name_elem = ET.SubElement(simple_dt, 'Name')
                        sdt_name_elem.set('textId', sdt_name_text_id)

                    # Add SingleValue elements for this SimpleDatatype (PQA reconstruction)
                    # PQA Fix #61: Include xsi_type in query
                    cursor.execute("""
                        SELECT value, name, name_text_id, xsi_type
                        FROM process_data_single_values
                        WHERE record_item_id = ?
                    """, (item['id'],))
                    single_values = cursor.fetchall()
                    for sv in single_values:
                        sv_elem = ET.SubElement(simple_dt, 'SingleValue')
                        # PQA Fix #61: Add xsi:type attribute if present
                        sv_xsi_type = sv['xsi_type'] if 'xsi_type' in sv.keys() else None
                        if sv_xsi_type:
                            sv_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', sv_xsi_type)
                        sv_elem.set('value', str(sv['value']))
                        sv_name_text_id = sv['name_text_id'] if 'name_text_id' in sv.keys() else None
                        if sv_name_text_id:
                            sv_name_elem = ET.SubElement(sv_elem, 'Name')
                            sv_name_elem.set('textId', sv_name_text_id)
                        elif sv['name'] and device_id:
                            # Fallback: lookup text_id from iodd_text
                            cursor.execute("""
                                SELECT text_id FROM iodd_text
                                WHERE device_id = ? AND text_value = ?
                                LIMIT 1
                            """, (device_id, sv['name']))
                            tid_row = cursor.fetchone()
                            if tid_row:
                                sv_name_elem = ET.SubElement(sv_elem, 'Name')
                                sv_name_elem.set('textId', tid_row['text_id'])

                    # Add ValueRange element if present (PQA reconstruction)
                    min_val = item['min_value'] if 'min_value' in item.keys() else None
                    max_val = item['max_value'] if 'max_value' in item.keys() else None
                    if min_val is not None or max_val is not None:
                        vr_elem = ET.SubElement(simple_dt, 'ValueRange')
                        vr_xsi_type = item['value_range_xsi_type'] if 'value_range_xsi_type' in item.keys() else None
                        if vr_xsi_type:
                            vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', vr_xsi_type)
                        if min_val is not None:
                            vr_elem.set('lowerValue', str(min_val))
                        if max_val is not None:
                            vr_elem.set('upperValue', str(max_val))
                        # PQA Fix #30: Add Name child element with textId
                        vr_name_text_id = item['value_range_name_text_id'] if 'value_range_name_text_id' in item.keys() else None
                        if vr_name_text_id:
                            vr_name_elem = ET.SubElement(vr_elem, 'Name')
                            vr_name_elem.set('textId', vr_name_text_id)
                else:
                    # Custom datatype reference
                    dt_ref = ET.SubElement(record_elem, 'DatatypeRef')
                    dt_ref.set('datatypeId', item['data_type'])

            # Add Name element with textId (use stored textId directly for PQA accuracy)
            name_text_id = item['name_text_id'] if 'name_text_id' in item.keys() else None
            if name_text_id:
                name_elem = ET.SubElement(record_elem, 'Name')
                name_elem.set('textId', name_text_id)
            elif item['name'] and device_id:
                # Fallback: try reverse-lookup from iodd_text (less accurate)
                name_elem = ET.SubElement(record_elem, 'Name')
                cursor.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = ? AND text_value = ? AND language_code = 'en'
                    LIMIT 1
                """, (device_id, item['name']))
                text_row = cursor.fetchone()
                if text_row:
                    name_elem.set('textId', text_row['text_id'])
                else:
                    # Last resort: generate text ID from name
                    clean_name = item['name'].replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
                    name_elem.set('textId', f'TN_RI_{clean_name[:20]}')

            # Add Description element with textId (PQA reconstruction)
            desc_text_id = item['description_text_id'] if 'description_text_id' in item.keys() else None
            if desc_text_id:
                desc_elem = ET.SubElement(record_elem, 'Description')
                desc_elem.set('textId', desc_text_id)

    def _add_variable_record_items(self, conn: sqlite3.Connection, parameter_id: int,
                                   datatype_elem: ET.Element, device_id: int) -> None:
        """Add RecordItem elements to Variable/Datatype for RecordT types

        Queries parameter_record_items table and creates RecordItem child elements.
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM parameter_record_items
            WHERE parameter_id = ? ORDER BY order_index
        """, (parameter_id,))
        items = cursor.fetchall()

        if not items:
            return

        for item in items:
            record_elem = ET.SubElement(datatype_elem, 'RecordItem')
            # PQA Fix #127b: Set RecordItem attributes in correct order (accessRightRestriction, bitOffset, subindex)
            # to match original IODD files and avoid incorrect_attribute errors
            access_right = item['access_right_restriction'] if 'access_right_restriction' in item.keys() else None
            if access_right:
                record_elem.set('accessRightRestriction', access_right)
            if item['bit_offset'] is not None:
                record_elem.set('bitOffset', str(item['bit_offset']))
            record_elem.set('subindex', str(item['subindex']))

            # Add SimpleDatatype or DatatypeRef based on stored data
            if item['datatype_ref']:
                # Custom datatype reference (e.g., DT_xxx)
                dt_ref = ET.SubElement(record_elem, 'DatatypeRef')
                dt_ref.set('datatypeId', item['datatype_ref'])
            elif item['simple_datatype']:
                # Simple datatype (e.g., UIntegerT)
                simple_dt = ET.SubElement(record_elem, 'SimpleDatatype')
                simple_dt.set('{http://www.w3.org/2001/XMLSchema-instance}type', item['simple_datatype'])
                if item['bit_length']:
                    simple_dt.set('bitLength', str(item['bit_length']))
                # PQA: Add optional SimpleDatatype attributes
                fixed_len = item['fixed_length'] if 'fixed_length' in item.keys() else None
                if fixed_len:
                    simple_dt.set('fixedLength', str(fixed_len))
                encoding = item['encoding'] if 'encoding' in item.keys() else None
                if encoding:
                    simple_dt.set('encoding', encoding)
                dt_id = item['datatype_id'] if 'datatype_id' in item.keys() else None
                if dt_id:
                    simple_dt.set('id', dt_id)

                # Add SingleValue children for this RecordItem's SimpleDatatype
                # PQA Fix #61: Include xsi_type in query
                cursor.execute("""
                    SELECT value, name, name_text_id, order_index, xsi_type
                    FROM record_item_single_values
                    WHERE record_item_id = ?
                    ORDER BY order_index
                """, (item['id'],))
                ri_single_values = cursor.fetchall()

                for sv in ri_single_values:
                    sv_elem = ET.SubElement(simple_dt, 'SingleValue')
                    # PQA Fix #61: Add xsi:type attribute if present
                    sv_xsi_type = sv['xsi_type'] if 'xsi_type' in sv.keys() else None
                    if sv_xsi_type:
                        sv_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', sv_xsi_type)
                    sv_elem.set('value', sv['value'])
                    if sv['name_text_id']:
                        sv_name_elem = ET.SubElement(sv_elem, 'Name')
                        sv_name_elem.set('textId', sv['name_text_id'])

                # Add ValueRange element if present (PQA reconstruction)
                min_val = item['min_value'] if 'min_value' in item.keys() else None
                max_val = item['max_value'] if 'max_value' in item.keys() else None
                if min_val is not None or max_val is not None:
                    vr_elem = ET.SubElement(simple_dt, 'ValueRange')
                    vr_xsi_type = item['value_range_xsi_type'] if 'value_range_xsi_type' in item.keys() else None
                    if vr_xsi_type:
                        vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', vr_xsi_type)
                    if min_val is not None:
                        vr_elem.set('lowerValue', str(min_val))
                    if max_val is not None:
                        vr_elem.set('upperValue', str(max_val))
                    # PQA Fix #30: Add Name child element with textId
                    vr_name_text_id = item['value_range_name_text_id'] if 'value_range_name_text_id' in item.keys() else None
                    if vr_name_text_id:
                        vr_name_elem = ET.SubElement(vr_elem, 'Name')
                        vr_name_elem.set('textId', vr_name_text_id)

            # Add Name element with textId
            if item['name']:
                name_elem = ET.SubElement(record_elem, 'Name')
                # Use stored text_id if available
                if item['name_text_id']:
                    name_elem.set('textId', item['name_text_id'])
                else:
                    # Try to find text ID from iodd_text
                    cursor.execute("""
                        SELECT text_id FROM iodd_text
                        WHERE device_id = ? AND text_value = ? AND language_code = 'en'
                        LIMIT 1
                    """, (device_id, item['name']))
                    text_row = cursor.fetchone()
                    if text_row:
                        name_elem.set('textId', text_row['text_id'])
                    else:
                        # Generate text ID from name
                        clean_name = item['name'].replace(' ', '_').replace(',', '').replace('(', '').replace(')', '')
                        name_elem.set('textId', f'TN_RI_{clean_name[:20]}')

            # Add Description element with textId (PQA reconstruction)
            description_text_id = item['description_text_id'] if 'description_text_id' in item.keys() else None
            if description_text_id:
                desc_elem = ET.SubElement(record_elem, 'Description')
                desc_elem.set('textId', description_text_id)

    def _add_variable_single_values(self, conn: sqlite3.Connection, parameter_id: int,
                                    datatype_elem: ET.Element) -> None:
        """Add SingleValue elements to Variable/Datatype

        Queries parameter_single_values table and creates SingleValue child elements.
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM parameter_single_values
            WHERE parameter_id = ? ORDER BY order_index
        """, (parameter_id,))
        items = cursor.fetchall()

        if not items:
            return

        for item in items:
            sv_elem = ET.SubElement(datatype_elem, 'SingleValue')
            sv_elem.set('value', str(item['value']))

            # Add xsi:type if present
            if item['xsi_type']:
                sv_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', item['xsi_type'])

            # Add Name element with textId
            if item['text_id']:
                name_elem = ET.SubElement(sv_elem, 'Name')
                name_elem.set('textId', item['text_id'])

    def _add_variable_record_item_info(self, conn: sqlite3.Connection, parameter_id: int,
                                       variable_elem: ET.Element) -> None:
        """Add RecordItemInfo elements to Variable

        Queries variable_record_item_info table and creates RecordItemInfo child elements.
        """
        cursor = conn.cursor()
        cursor.execute("""
            SELECT * FROM variable_record_item_info
            WHERE parameter_id = ? ORDER BY order_index
        """, (parameter_id,))
        items = cursor.fetchall()

        if not items:
            return

        for item in items:
            ri_info_elem = ET.SubElement(variable_elem, 'RecordItemInfo')
            ri_info_elem.set('subindex', str(item['subindex']))
            if item['default_value'] is not None:
                ri_info_elem.set('defaultValue', str(item['default_value']))
            # Only output boolean attributes if they were explicitly set (not NULL)
            # This avoids generating extra attributes that weren't in the original IODD
            excluded = item['excluded_from_data_storage'] if 'excluded_from_data_storage' in item.keys() else None
            modifies = item['modifies_other_variables'] if 'modifies_other_variables' in item.keys() else None
            if excluded is not None:
                ri_info_elem.set('excludedFromDataStorage', 'true' if excluded else 'false')
            if modifies is not None:
                ri_info_elem.set('modifiesOtherVariables', 'true' if modifies else 'false')

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
            # PQA Fix #45: Output subindexAccessSupported even when false
            if dt['subindex_access_supported'] is not None:
                datatype_elem.set('subindexAccessSupported', 'true' if dt['subindex_access_supported'] else 'false')

            # Add bitLength attribute if present
            if dt['bit_length']:
                datatype_elem.set('bitLength', str(dt['bit_length']))

            # PQA Fix #98: Add count attribute for ArrayT types
            if 'array_count' in dt.keys() and dt['array_count'] is not None:
                datatype_elem.set('count', str(dt['array_count']))

            # PQA Fix #59: Add fixedLength and encoding for StringT/OctetStringT
            if 'string_fixed_length' in dt.keys() and dt['string_fixed_length']:
                datatype_elem.set('fixedLength', str(dt['string_fixed_length']))
            if 'string_encoding' in dt.keys() and dt['string_encoding']:
                datatype_elem.set('encoding', dt['string_encoding'])

            # PQA Fix #96: Add SimpleDatatype child element for ArrayT types
            # PQA Fix #138: Add SingleValue elements to SimpleDatatype child for ArrayT
            if dt['datatype_xsi_type'] == 'ArrayT':
                array_elem_type = dt['array_element_type'] if 'array_element_type' in dt.keys() else None
                array_elem_bit_length = dt['array_element_bit_length'] if 'array_element_bit_length' in dt.keys() else None
                if array_elem_type:
                    simple_dt_elem = ET.SubElement(datatype_elem, 'SimpleDatatype')
                    simple_dt_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', array_elem_type)
                    if array_elem_bit_length:
                        simple_dt_elem.set('bitLength', str(array_elem_bit_length))
                    # Add SingleValue elements to SimpleDatatype child, not Datatype parent
                    self._add_single_values(conn, simple_dt_elem, dt['id'])
            else:
                # Add SingleValue enumerations as direct children for non-ArrayT types
                self._add_single_values(conn, datatype_elem, dt['id'])

            # PQA Fix #30b: Add ValueRange at Datatype level if present
            dt_min_value = dt['min_value'] if 'min_value' in dt.keys() else None
            dt_max_value = dt['max_value'] if 'max_value' in dt.keys() else None
            if dt_min_value is not None or dt_max_value is not None:
                vr_elem = ET.SubElement(datatype_elem, 'ValueRange')
                vr_xsi_type = dt['value_range_xsi_type'] if 'value_range_xsi_type' in dt.keys() else None
                if vr_xsi_type:
                    vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', vr_xsi_type)
                if dt_min_value is not None:
                    vr_elem.set('lowerValue', str(dt_min_value))
                if dt_max_value is not None:
                    vr_elem.set('upperValue', str(dt_max_value))
                vr_name_text_id = dt['value_range_name_text_id'] if 'value_range_name_text_id' in dt.keys() else None
                if vr_name_text_id:
                    vr_name_elem = ET.SubElement(vr_elem, 'Name')
                    vr_name_elem.set('textId', vr_name_text_id)

            # PQA Fix #6A: Add Name child element if present
            dt_name_text_id = dt['datatype_name_text_id'] if 'datatype_name_text_id' in dt.keys() else None
            if dt_name_text_id:
                name_elem = ET.SubElement(datatype_elem, 'Name')
                name_elem.set('textId', dt_name_text_id)

            # Add RecordItem structures
            self._add_record_items(conn, datatype_elem, dt['id'])

            collection.append(datatype_elem)

        return collection

    def _add_single_values(self, conn: sqlite3.Connection, parent: ET.Element,
                          datatype_id: int) -> None:
        """Add SingleValue enumeration values (Phase 3 Task 10a - direct children, no wrapper)"""
        cursor = conn.cursor()
        # PQA Fix #38: Order by xml_order to preserve original IODD order
        # Fallback to numeric/alphabetic sort for legacy data without xml_order
        cursor.execute("""
            SELECT * FROM custom_datatype_single_values
            WHERE datatype_id = ?
            ORDER BY COALESCE(xml_order, 999999),
                CASE
                    WHEN value GLOB '[0-9]*' AND value NOT GLOB '*[^0-9]*'
                    THEN CAST(value AS INTEGER)
                    ELSE 999999
                END, value
        """, (datatype_id,))
        values = cursor.fetchall()

        if not values:
            return

        # Add SingleValue elements directly to parent (no wrapper list)
        for val in values:
            value_elem = ET.SubElement(parent, 'SingleValue')

            # Add xsi:type attribute if stored (PQA improvement)
            xsi_type = val['xsi_type'] if 'xsi_type' in val.keys() else None
            if xsi_type:
                value_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', xsi_type)

            value_elem.set('value', str(val['value']))

            if val['name']:
                name = ET.SubElement(value_elem, 'Name')
                # Use stored text_id if available (PQA improvement)
                stored_text_id = val['text_id'] if 'text_id' in val.keys() else None
                if stored_text_id:
                    name.set('textId', stored_text_id)
                else:
                    # Fallback: try to find from iodd_text table
                    cursor2 = conn.cursor()
                    cursor2.execute("""
                        SELECT text_id FROM iodd_text
                        WHERE device_id = (SELECT device_id FROM custom_datatypes WHERE id = ?)
                        AND text_value = ?
                        LIMIT 1
                    """, (datatype_id, val['name']))
                    text_id_row = cursor2.fetchone()
                    if text_id_row:
                        name.set('textId', text_id_row['text_id'])
                    else:
                        # Final fallback: generate a text ID from the name
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
            # PQA: Add accessRightRestriction attribute if present
            access_right = item['access_right_restriction'] if 'access_right_restriction' in item.keys() else None
            if access_right:
                record_elem.set('accessRightRestriction', access_right)

            if item['name']:
                name = ET.SubElement(record_elem, 'Name')
                # Use stored name_text_id if available (PQA improvement)
                stored_text_id = item['name_text_id'] if 'name_text_id' in item.keys() else None
                if stored_text_id:
                    name.set('textId', stored_text_id)
                else:
                    # Fallback: try to find from iodd_text table
                    cursor2 = conn.cursor()
                    cursor2.execute("""
                        SELECT text_id FROM iodd_text
                        WHERE device_id = (SELECT device_id FROM custom_datatypes WHERE id = ?)
                        AND text_value = ?
                        LIMIT 1
                    """, (datatype_id, item['name']))
                    text_id_row = cursor2.fetchone()
                    if text_id_row:
                        name.set('textId', text_id_row['text_id'])
                    else:
                        # Final fallback: generate a text ID from the name
                        clean_name = item['name'].replace(' ', '').replace('-', '_')
                        name.set('textId', 'TN_RI_' + clean_name)

            # Add Description element with textId (PQA reconstruction)
            desc_text_id = item['description_text_id'] if 'description_text_id' in item.keys() else None
            if desc_text_id:
                desc_elem = ET.SubElement(record_elem, 'Description')
                desc_elem.set('textId', desc_text_id)

            # Determine whether to use DatatypeRef or SimpleDatatype
            # Base types (ending in 'T' like UIntegerT, IntegerT, StringT) use SimpleDatatype
            # Custom datatype references (like D_OutputFunction, D_Percentage) use DatatypeRef
            base_types = {'UIntegerT', 'IntegerT', 'StringT', 'BooleanT', 'Float32T', 'OctetStringT'}

            if item['datatype_ref']:
                if item['datatype_ref'] in base_types:
                    # Base type - use SimpleDatatype with xsi:type
                    datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                    datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', item['datatype_ref'])
                    # PQA Fix: Add SimpleDatatype@id attribute if present
                    simple_dt_id = item['simple_datatype_id'] if 'simple_datatype_id' in item.keys() else None
                    if simple_dt_id:
                        datatype.set('id', simple_dt_id)
                    if item['bit_length']:
                        datatype.set('bitLength', str(item['bit_length']))
                    # PQA Fix #69: Add fixedLength and encoding attributes
                    fixed_len = item['fixed_length'] if 'fixed_length' in item.keys() else None
                    if fixed_len:
                        datatype.set('fixedLength', str(fixed_len))
                    enc = item['encoding'] if 'encoding' in item.keys() else None
                    if enc:
                        datatype.set('encoding', enc)
                    # PQA Fix #21: Add SingleValue elements inside SimpleDatatype
                    self._add_custom_datatype_record_item_single_values(conn, item['id'], datatype)
                    # Add ValueRange element if present (PQA reconstruction)
                    min_val = item['min_value'] if 'min_value' in item.keys() else None
                    max_val = item['max_value'] if 'max_value' in item.keys() else None
                    if min_val is not None or max_val is not None:
                        vr_elem = ET.SubElement(datatype, 'ValueRange')
                        vr_xsi_type = item['value_range_xsi_type'] if 'value_range_xsi_type' in item.keys() else None
                        if vr_xsi_type:
                            vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', vr_xsi_type)
                        if min_val is not None:
                            vr_elem.set('lowerValue', str(min_val))
                        if max_val is not None:
                            vr_elem.set('upperValue', str(max_val))
                        # PQA Fix #30: Add Name child element with textId
                        vr_name_text_id = item['value_range_name_text_id'] if 'value_range_name_text_id' in item.keys() else None
                        if vr_name_text_id:
                            vr_name_elem = ET.SubElement(vr_elem, 'Name')
                            vr_name_elem.set('textId', vr_name_text_id)
                else:
                    # Custom datatype reference - use DatatypeRef
                    datatype = ET.SubElement(record_elem, 'DatatypeRef')
                    datatype.set('datatypeId', item['datatype_ref'])
            elif item['bit_length']:
                # Fallback: create SimpleDatatype with bit_length
                datatype = ET.SubElement(record_elem, 'SimpleDatatype')
                xsi_type = item['xsi_type'] if 'xsi_type' in item.keys() else None
                if xsi_type:
                    datatype.set('{http://www.w3.org/2001/XMLSchema-instance}type', xsi_type)
                # PQA Fix: Add SimpleDatatype@id attribute if present
                simple_dt_id = item['simple_datatype_id'] if 'simple_datatype_id' in item.keys() else None
                if simple_dt_id:
                    datatype.set('id', simple_dt_id)
                if item['bit_length']:
                    datatype.set('bitLength', str(item['bit_length']))
                # PQA Fix #21: Add SingleValue elements inside SimpleDatatype
                self._add_custom_datatype_record_item_single_values(conn, item['id'], datatype)
                # Add ValueRange element if present (PQA reconstruction)
                min_val = item['min_value'] if 'min_value' in item.keys() else None
                max_val = item['max_value'] if 'max_value' in item.keys() else None
                if min_val is not None or max_val is not None:
                    vr_elem = ET.SubElement(datatype, 'ValueRange')
                    vr_xsi_type = item['value_range_xsi_type'] if 'value_range_xsi_type' in item.keys() else None
                    if vr_xsi_type:
                        vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', vr_xsi_type)
                    if min_val is not None:
                        vr_elem.set('lowerValue', str(min_val))
                    if max_val is not None:
                        vr_elem.set('upperValue', str(max_val))
                    # PQA Fix #30: Add Name child element with textId
                    vr_name_text_id = item['value_range_name_text_id'] if 'value_range_name_text_id' in item.keys() else None
                    if vr_name_text_id:
                        vr_name_elem = ET.SubElement(vr_elem, 'Name')
                        vr_name_elem.set('textId', vr_name_text_id)

    def _add_custom_datatype_record_item_single_values(self, conn: sqlite3.Connection,
                                                       record_item_id: int,
                                                       parent: ET.Element) -> None:
        """PQA Fix #21: Add SingleValue elements to RecordItem/SimpleDatatype for custom datatypes"""
        cursor = conn.cursor()
        # PQA Fix #74: Order by xml_order to preserve original IODD order
        cursor.execute("""
            SELECT value, name, name_text_id, xsi_type
            FROM custom_datatype_record_item_single_values
            WHERE record_item_id = ?
            ORDER BY COALESCE(xml_order, id)
        """, (record_item_id,))
        single_values = cursor.fetchall()

        for sv in single_values:
            sv_elem = ET.SubElement(parent, 'SingleValue')
            # Add xsi:type attribute if present
            if sv['xsi_type']:
                sv_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', sv['xsi_type'])
            sv_elem.set('value', str(sv['value']))
            # Add Name element with textId
            if sv['name_text_id']:
                name_elem = ET.SubElement(sv_elem, 'Name')
                name_elem.set('textId', sv['name_text_id'])

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

            # Add Menu Name element with textId reference
            # Use stored name_text_id if available, otherwise fallback to reverse lookup
            name_text_id = menu['name_text_id'] if 'name_text_id' in menu.keys() and menu['name_text_id'] else None
            if name_text_id:
                name_elem = ET.SubElement(menu_elem, 'Name')
                name_elem.set('textId', name_text_id)
            elif menu['name']:
                # Fallback: reverse lookup from name (may match wrong textId)
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
                    # PQA Fix #29: Output buttonValue attribute when present
                    if item['button_value'] if 'button_value' in item.keys() else None:
                        var_ref.set('buttonValue', item['button_value'])
                    # Use 'is not None' to handle 0 values correctly
                    # PQA: Use original string format if available, otherwise format the float
                    if item['gradient'] is not None:
                        gradient_str = item['gradient_str'] if 'gradient_str' in item.keys() and item['gradient_str'] else None
                        var_ref.set('gradient', gradient_str if gradient_str else self._format_number(item['gradient']))
                    if item['offset'] is not None:
                        offset_str = item['offset_str'] if 'offset_str' in item.keys() and item['offset_str'] else None
                        var_ref.set('offset', offset_str if offset_str else self._format_number(item['offset']))
                    # Add Button children if any
                    cursor2 = conn.cursor()
                    cursor2.execute("""
                        SELECT * FROM ui_menu_buttons
                        WHERE menu_item_id = ?
                        ORDER BY id
                    """, (item['id'],))
                    button_rows = cursor2.fetchall()
                    for btn in button_rows:
                        button_elem = ET.SubElement(var_ref, 'Button')
                        button_elem.set('buttonValue', str(btn['button_value']))
                        # Use description_text_id for PQA reconstruction
                        desc_text_id = btn['description_text_id'] if 'description_text_id' in btn.keys() else None
                        if desc_text_id:
                            desc_elem = ET.SubElement(button_elem, 'Description')
                            desc_elem.set('textId', desc_text_id)
                        # Use action_started_message_text_id for PQA reconstruction
                        action_text_id = btn['action_started_message_text_id'] if 'action_started_message_text_id' in btn.keys() else None
                        if action_text_id:
                            action_elem = ET.SubElement(button_elem, 'ActionStartedMessage')
                            action_elem.set('textId', action_text_id)
                elif item['record_item_ref']:
                    # RecordItemRef
                    record_ref = ET.SubElement(menu_elem, 'RecordItemRef')
                    record_ref.set('variableId', item['record_item_ref'])
                    if item['subindex'] is not None:
                        record_ref.set('subindex', str(item['subindex']))
                    if item['access_right_restriction']:
                        record_ref.set('accessRightRestriction', item['access_right_restriction'])
                    if item['display_format']:
                        record_ref.set('displayFormat', item['display_format'])
                    if item['unit_code']:
                        record_ref.set('unitCode', item['unit_code'])
                    # Use 'is not None' to handle 0 values correctly
                    # PQA: Use original string format if available, otherwise format the float
                    if item['gradient'] is not None:
                        gradient_str = item['gradient_str'] if 'gradient_str' in item.keys() and item['gradient_str'] else None
                        record_ref.set('gradient', gradient_str if gradient_str else self._format_number(item['gradient']))
                    if item['offset'] is not None:
                        offset_str = item['offset_str'] if 'offset_str' in item.keys() and item['offset_str'] else None
                        record_ref.set('offset', offset_str if offset_str else self._format_number(item['offset']))
                    # PQA Fix #129: Add Button children for RecordItemRef if any
                    cursor2 = conn.cursor()
                    cursor2.execute("""
                        SELECT * FROM ui_menu_buttons
                        WHERE menu_item_id = ?
                        ORDER BY id
                    """, (item['id'],))
                    button_rows = cursor2.fetchall()
                    for btn in button_rows:
                        button_elem = ET.SubElement(record_ref, 'Button')
                        button_elem.set('buttonValue', str(btn['button_value']))
                        # Use description_text_id for PQA reconstruction
                        desc_text_id = btn['description_text_id'] if 'description_text_id' in btn.keys() else None
                        if desc_text_id:
                            desc_elem = ET.SubElement(button_elem, 'Description')
                            desc_elem.set('textId', desc_text_id)
                        # Use action_started_message_text_id for PQA reconstruction
                        action_text_id = btn['action_started_message_text_id'] if 'action_started_message_text_id' in btn.keys() else None
                        if action_text_id:
                            action_elem = ET.SubElement(button_elem, 'ActionStartedMessage')
                            action_elem.set('textId', action_text_id)
                elif item['menu_ref']:
                    # MenuRef
                    menu_ref = ET.SubElement(menu_elem, 'MenuRef')
                    menu_ref.set('menuId', item['menu_ref'])
                    # Add Condition child element if present
                    cond_var_id = item['condition_variable_id'] if 'condition_variable_id' in item.keys() else None
                    cond_value = item['condition_value'] if 'condition_value' in item.keys() else None
                    cond_subindex = item['condition_subindex'] if 'condition_subindex' in item.keys() else None
                    if cond_var_id:
                        condition_elem = ET.SubElement(menu_ref, 'Condition')
                        condition_elem.set('variableId', cond_var_id)
                        if cond_value is not None:
                            condition_elem.set('value', str(cond_value))
                        if cond_subindex is not None:
                            condition_elem.set('subindex', str(cond_subindex))

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

            # Get menu types for this role (PQA Fix #27: include has_xsi_type)
            cursor.execute("""
                SELECT menu_type, menu_id, has_xsi_type FROM ui_menu_roles
                WHERE device_id = ? AND role_type = ?
                ORDER BY menu_type
            """, (device_id, role_type))
            role_menus = cursor.fetchall()

            for role_menu in role_menus:
                menu_type = role_menu['menu_type']
                # PQA Fix #28: Handle namespace prefix in menu_type (legacy data)
                if '}' in menu_type:
                    menu_type = menu_type.split('}')[1]
                menu_id = role_menu['menu_id']
                has_xsi_type = role_menu['has_xsi_type'] if 'has_xsi_type' in role_menu.keys() else 0

                menu_elem = None
                if menu_type == 'IdentificationMenu':
                    menu_elem = ET.SubElement(role_set, 'IdentificationMenu')
                elif menu_type == 'ParameterMenu':
                    menu_elem = ET.SubElement(role_set, 'ParameterMenu')
                elif menu_type == 'ObservationMenu':
                    menu_elem = ET.SubElement(role_set, 'ObservationMenu')
                elif menu_type == 'DiagnosisMenu':
                    menu_elem = ET.SubElement(role_set, 'DiagnosisMenu')

                if menu_elem is not None:
                    # PQA Fix #27: Add xsi:type if present in original
                    if has_xsi_type:
                        menu_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'UIMenuRefT')
                    menu_elem.set('menuId', menu_id)

        # PQA Fix #31: Add ProcessDataRefCollection if UI info exists
        # PQA Fix #42: Order by pd_ref_order to preserve original ProcessDataRef order
        # PQA Fix #41: Order by xml_order within each ProcessDataRef to preserve original element order
        # Fallback: direction-based order for legacy data without pd_ref_order
        cursor.execute("""
            SELECT pdui.*, pd.pd_id, pd.direction
            FROM process_data_ui_info pdui
            JOIN process_data pd ON pdui.process_data_id = pd.id
            WHERE pd.device_id = ?
            ORDER BY COALESCE(pdui.pd_ref_order, CASE pd.direction WHEN 'output' THEN 0 ELSE 1 END),
                     pd.pd_id,
                     COALESCE(pdui.xml_order, pdui.subindex)
        """, (device_id,))
        ui_info_rows = cursor.fetchall()

        if ui_info_rows:
            pdrc = ET.SubElement(user_interface, 'ProcessDataRefCollection')
            current_pd_id = None
            current_pd_ref = None

            for ui_info in ui_info_rows:
                pd_id = ui_info['pd_id']

                # Create new ProcessDataRef for each unique process data
                if pd_id != current_pd_id:
                    current_pd_ref = ET.SubElement(pdrc, 'ProcessDataRef')
                    current_pd_ref.set('processDataId', pd_id)
                    current_pd_id = pd_id

                # Add ProcessDataRecordItemInfo
                item_info = ET.SubElement(current_pd_ref, 'ProcessDataRecordItemInfo')
                item_info.set('subindex', str(ui_info['subindex']))
                # PQA Fix #60b: Use original string format if available, else format number
                if ui_info['gradient'] is not None:
                    gradient_str = ui_info['gradient_str'] if 'gradient_str' in ui_info.keys() and ui_info['gradient_str'] else None
                    item_info.set('gradient', gradient_str if gradient_str else self._format_number(ui_info['gradient']))
                if ui_info['offset'] is not None:
                    offset_str = ui_info['offset_str'] if 'offset_str' in ui_info.keys() and ui_info['offset_str'] else None
                    item_info.set('offset', offset_str if offset_str else self._format_number(ui_info['offset']))
                if ui_info['unit_code']:
                    item_info.set('unitCode', ui_info['unit_code'])
                if ui_info['display_format']:
                    item_info.set('displayFormat', ui_info['display_format'])

        return user_interface

    def _create_comm_network_profile(self, conn: sqlite3.Connection,
                                      device_id: int) -> Optional[ET.Element]:
        """Create CommNetworkProfile element with TransportLayers and Test sections"""
        cursor = conn.cursor()

        # Get communication profile data
        cursor.execute("SELECT * FROM communication_profile WHERE device_id = ?", (device_id,))
        comm_profile = cursor.fetchone()

        if not comm_profile:
            return None

        # Create CommNetworkProfile element
        comm_elem = ET.Element('CommNetworkProfile')
        comm_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', 'IOLinkCommNetworkProfileT')

        if comm_profile['iolink_revision']:
            comm_elem.set('iolinkRevision', comm_profile['iolink_revision'])

        # PQA Fix #49: Add compatibleWith attribute if present
        compatible_with = comm_profile['compatible_with'] if 'compatible_with' in comm_profile.keys() else None
        if compatible_with:
            comm_elem.set('compatibleWith', compatible_with)

        # Create TransportLayers
        transport_layers = ET.SubElement(comm_elem, 'TransportLayers')

        # Create PhysicalLayer
        physical_layer = ET.SubElement(transport_layers, 'PhysicalLayer')

        # PQA Fix #44: Add physics attribute if present
        physics = comm_profile['physics'] if 'physics' in comm_profile.keys() else None
        if physics:
            physical_layer.set('physics', physics)
        if comm_profile['bitrate']:
            # PQA Fix: Use the original attribute name (baudrate or bitrate)
            uses_baudrate = comm_profile['uses_baudrate'] if 'uses_baudrate' in comm_profile.keys() else True
            attr_name = 'baudrate' if uses_baudrate else 'bitrate'
            physical_layer.set(attr_name, comm_profile['bitrate'])
        if comm_profile['min_cycle_time']:
            physical_layer.set('minCycleTime', str(comm_profile['min_cycle_time']))
        if comm_profile['sio_supported'] is not None:
            physical_layer.set('sioSupported', 'true' if comm_profile['sio_supported'] else 'false')
        if comm_profile['msequence_capability']:
            physical_layer.set('mSequenceCapability', str(comm_profile['msequence_capability']))

        # Get wire configurations for Connection element
        cursor.execute("""
            SELECT * FROM wire_configurations
            WHERE device_id = ?
            ORDER BY wire_number
        """, (device_id,))
        wire_configs = cursor.fetchall()

        if wire_configs or comm_profile['connection_type']:
            connection = ET.SubElement(physical_layer, 'Connection')

            # Get connection type from wire_configurations if available, else from comm_profile
            conn_type = wire_configs[0]['connection_type'] if wire_configs and wire_configs[0]['connection_type'] else comm_profile['connection_type']
            if conn_type:
                # Add 'T' suffix if not present (e.g., M12-4Connection -> M12-4ConnectionT)
                if not conn_type.endswith('T'):
                    conn_type = conn_type + 'T'
                connection.set('{http://www.w3.org/2001/XMLSchema-instance}type', conn_type)

            # PQA Fix #19: Add connectionSymbol attribute if present
            # First check wire_configurations, then fallback to communication_profile
            conn_symbol = None
            if wire_configs and 'connection_symbol' in wire_configs[0].keys() and wire_configs[0]['connection_symbol']:
                conn_symbol = wire_configs[0]['connection_symbol']
            elif 'connection_symbol' in comm_profile.keys() and comm_profile['connection_symbol']:
                conn_symbol = comm_profile['connection_symbol']  # PQA Fix #19b: Fallback
            if conn_symbol:
                connection.set('connectionSymbol', conn_symbol)

            # PQA Fix #26: Use stored product_ref_id from communication_profile, fallback to device_variants
            # PQA Fix #100: Check 'is not None' to output ProductRef even with empty productId
            product_ref_id = comm_profile['product_ref_id'] if 'product_ref_id' in comm_profile.keys() else None
            if product_ref_id is None:
                # Fallback to device_variants
                cursor.execute("SELECT product_id FROM device_variants WHERE device_id = ? LIMIT 1", (device_id,))
                variant_row = cursor.fetchone()
                if variant_row:
                    product_ref_id = variant_row['product_id']
            if product_ref_id is not None:
                product_ref = ET.SubElement(connection, 'ProductRef')
                product_ref.set('productId', product_ref_id)

            # PQA Fix #39: Add Connection/Description element if present
            conn_desc_text_id = comm_profile['connection_description_text_id'] if 'connection_description_text_id' in comm_profile.keys() and comm_profile['connection_description_text_id'] else None
            if conn_desc_text_id:
                description_elem = ET.SubElement(connection, 'Description')
                description_elem.set('textId', conn_desc_text_id)

            # Add wire elements
            for wire in wire_configs:
                wire_elem_name = f"Wire{wire['wire_number']}"
                wire_elem = ET.SubElement(connection, wire_elem_name)
                # PQA Fix #25: Add xsi:type attribute if present (e.g., Wire1T, Wire3T)
                wire_xsi_type = wire['xsi_type'] if 'xsi_type' in wire.keys() and wire['xsi_type'] else None
                if wire_xsi_type:
                    wire_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', wire_xsi_type)
                if wire['wire_color']:
                    wire_elem.set('color', wire['wire_color'])
                if wire['wire_function']:
                    wire_elem.set('function', wire['wire_function'])
                # PQA Fix #22: Add Name element with textId
                name_text_id = wire['name_text_id'] if 'name_text_id' in wire.keys() else None
                if name_text_id:
                    name_elem = ET.SubElement(wire_elem, 'Name')
                    name_elem.set('textId', name_text_id)

        # PQA Fix #84: Create Test section if it was present in original IODD
        has_test_element = comm_profile['has_test_element'] if 'has_test_element' in comm_profile.keys() else False
        cursor.execute("""
            SELECT * FROM device_test_config
            WHERE device_id = ?
            ORDER BY config_type
        """, (device_id,))
        test_configs = cursor.fetchall()

        if has_test_element:
            test_elem = ET.SubElement(comm_elem, 'Test')
            # PQA Fix #23: Only add xsi:type if it was present in original
            test_xsi_type = comm_profile['test_xsi_type'] if 'test_xsi_type' in comm_profile.keys() and comm_profile['test_xsi_type'] else None
            if test_xsi_type:
                test_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', test_xsi_type)

            for config in test_configs:
                config_elem = ET.SubElement(test_elem, config['config_type'])
                config_elem.set('index', str(config['param_index']))
                # PQA Fix #4: Add xsi:type attribute if present
                if config['config_xsi_type']:
                    config_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', config['config_xsi_type'])
                if config['test_value']:
                    config_elem.set('testValue', config['test_value'])

                # Get event triggers for this config (for Config7)
                cursor.execute("""
                    SELECT * FROM device_test_event_triggers
                    WHERE test_config_id = ?
                """, (config['id'],))
                event_triggers = cursor.fetchall()

                for trigger in event_triggers:
                    trigger_elem = ET.SubElement(config_elem, 'EventTrigger')
                    trigger_elem.set('appearValue', trigger['appear_value'])
                    trigger_elem.set('disappearValue', trigger['disappear_value'])

        return comm_elem

    def _create_stamp(self, conn: sqlite3.Connection,
                      device_id: int) -> Optional[ET.Element]:
        """Create Stamp element with CRC and Checker info"""
        cursor = conn.cursor()

        # Get stamp data from iodd_files table
        cursor.execute("""
            SELECT stamp_crc, checker_name, checker_version
            FROM iodd_files WHERE device_id = ?
        """, (device_id,))
        row = cursor.fetchone()

        if not row:
            return None

        stamp_crc = row['stamp_crc'] if 'stamp_crc' in row.keys() else None
        checker_name = row['checker_name'] if 'checker_name' in row.keys() else None
        checker_version = row['checker_version'] if 'checker_version' in row.keys() else None

        # Only create Stamp if there's any data
        if not stamp_crc and not checker_name:
            return None

        stamp = ET.Element('Stamp')

        if stamp_crc:
            stamp.set('crc', str(stamp_crc))

        # Add Checker element if checker info exists
        if checker_name or checker_version:
            checker = ET.SubElement(stamp, 'Checker')
            if checker_name:
                checker.set('name', checker_name)
            if checker_version:
                checker.set('version', checker_version)

        return stamp

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
            ORDER BY COALESCE(xml_order, param_index)
        """, (device_id,))
        parameters = cursor.fetchall()

        if not parameters and not device:
            return None

        collection = ET.Element('VariableCollection')

        # Query stored StdVariableRef elements in original order
        cursor.execute("""
            SELECT id, variable_id, default_value, fixed_length_restriction, excluded_from_data_storage, order_index
            FROM std_variable_refs
            WHERE device_id = ?
            ORDER BY order_index
        """, (device_id,))
        std_var_refs = cursor.fetchall()

        if std_var_refs:
            # Use stored StdVariableRef data for accurate reconstruction
            for ref in std_var_refs:
                std_ref = ET.SubElement(collection, 'StdVariableRef')

                # Set excludedFromDataStorage first (attribute ordering matters for PQA)
                if ref['excluded_from_data_storage'] is not None:
                    std_ref.set('excludedFromDataStorage', 'true' if ref['excluded_from_data_storage'] else 'false')

                # Set id attribute
                std_ref.set('id', ref['variable_id'])

                if ref['default_value'] is not None:
                    std_ref.set('defaultValue', ref['default_value'])

                if ref['fixed_length_restriction'] is not None:
                    std_ref.set('fixedLengthRestriction', str(ref['fixed_length_restriction']))

                # Add SingleValue and StdSingleValueRef children
                cursor.execute("""
                    SELECT value, name_text_id, is_std_ref, order_index
                    FROM std_variable_ref_single_values
                    WHERE std_variable_ref_id = ?
                    ORDER BY order_index
                """, (ref['id'],))
                single_values = cursor.fetchall()

                for sv in single_values:
                    if sv['is_std_ref']:
                        # StdSingleValueRef - just value attribute
                        sv_elem = ET.SubElement(std_ref, 'StdSingleValueRef')
                        sv_elem.set('value', sv['value'])
                    else:
                        # SingleValue - with Name child
                        sv_elem = ET.SubElement(std_ref, 'SingleValue')
                        sv_elem.set('value', sv['value'])
                        if sv['name_text_id']:
                            name_elem = ET.SubElement(sv_elem, 'Name')
                            name_elem.set('textId', sv['name_text_id'])

                # PQA Fix #5: Add StdValueRangeRef and ValueRange children
                cursor.execute("""
                    SELECT lower_value, upper_value, is_std_ref, order_index
                    FROM std_variable_ref_value_ranges
                    WHERE std_variable_ref_id = ?
                    ORDER BY order_index
                """, (ref['id'],))
                value_ranges = cursor.fetchall()

                for vr in value_ranges:
                    if vr['is_std_ref']:
                        # StdValueRangeRef - lowerValue and upperValue attributes
                        vr_elem = ET.SubElement(std_ref, 'StdValueRangeRef')
                        vr_elem.set('lowerValue', vr['lower_value'])
                        vr_elem.set('upperValue', vr['upper_value'])
                    else:
                        # ValueRange - lowerValue and upperValue attributes
                        vr_elem = ET.SubElement(std_ref, 'ValueRange')
                        vr_elem.set('lowerValue', vr['lower_value'])
                        vr_elem.set('upperValue', vr['upper_value'])

                # Add StdRecordItemRef children
                cursor2 = conn.cursor()
                cursor2.execute("""
                    SELECT id, subindex, default_value, order_index
                    FROM std_record_item_refs
                    WHERE std_variable_ref_id = ?
                    ORDER BY order_index
                """, (ref['id'],))
                record_item_refs = cursor2.fetchall()

                for ri in record_item_refs:
                    ri_elem = ET.SubElement(std_ref, 'StdRecordItemRef')
                    ri_elem.set('subindex', str(ri['subindex']))
                    if ri['default_value'] is not None:
                        ri_elem.set('defaultValue', ri['default_value'])
                    
                    # PQA Fix #76: Add SingleValue/StdSingleValueRef children
                    cursor3 = conn.cursor()
                    cursor3.execute("""
                        SELECT value, name_text_id, is_std_ref, order_index
                        FROM std_record_item_ref_single_values
                        WHERE std_record_item_ref_id = ?
                        ORDER BY order_index
                    """, (ri['id'],))
                    ri_single_values = cursor3.fetchall()
                    
                    for ri_sv in ri_single_values:
                        if ri_sv['is_std_ref']:
                            # StdSingleValueRef element
                            ri_sv_elem = ET.SubElement(ri_elem, 'StdSingleValueRef')
                            ri_sv_elem.set('value', ri_sv['value'])
                        else:
                            # SingleValue element with optional Name child
                            ri_sv_elem = ET.SubElement(ri_elem, 'SingleValue')
                            ri_sv_elem.set('value', ri_sv['value'])
                            if ri_sv['name_text_id']:
                                ri_sv_name = ET.SubElement(ri_sv_elem, 'Name')
                                ri_sv_name.set('textId', ri_sv['name_text_id'])
        # No fallback - devices must be re-imported if std_variable_refs is empty

        # Phase 3 Task 9c: Create Variable elements from parameters
        # Note: StdVariableRef elements are handled separately above, so we reconstruct
        # all Variable elements from the parameters table here
        for param in parameters:
            # Use stored variable_id if available, otherwise generate from name
            var_id = param['variable_id'] if param['variable_id'] else \
                     'V_' + param['name'].replace(' ', '').replace('"', '').replace('-', '_').replace('/', '_')

            # PQA Fix #127: Create StdDirectParameterRef instead of Variable when flag is set
            is_std_direct = param['is_std_direct_parameter_ref'] if 'is_std_direct_parameter_ref' in param.keys() else 0
            element_name = 'StdDirectParameterRef' if is_std_direct else 'Variable'
            variable = ET.SubElement(collection, element_name)
            variable.set('id', var_id)
            # PQA Fix #127: Only Variable elements have index attribute, not StdDirectParameterRef
            if not is_std_direct:
                variable.set('index', str(param['param_index']))

            # Access rights
            if param['access_rights']:
                variable.set('accessRights', param['access_rights'])

            # defaultValue attribute
            if param['default_value'] is not None:
                variable.set('defaultValue', str(param['default_value']))

            # Dynamic attribute - only output if explicitly set in original IODD (not NULL)
            dynamic_val = param['dynamic'] if 'dynamic' in param.keys() else None
            if dynamic_val is not None:
                variable.set('dynamic', 'true' if dynamic_val else 'false')

            # Excluded from data storage - only output if explicitly set in original IODD (not NULL)
            excluded_val = param['excluded_from_data_storage'] if 'excluded_from_data_storage' in param.keys() else None
            if excluded_val is not None:
                variable.set('excludedFromDataStorage', 'true' if excluded_val else 'false')

            # Modifies other variables - only output if explicitly set in original IODD (not NULL)
            modifies_val = param['modifies_other_variables'] if 'modifies_other_variables' in param.keys() else None
            if modifies_val is not None:
                variable.set('modifiesOtherVariables', 'true' if modifies_val else 'false')

            # Determine if we should use DatatypeRef or Datatype based on datatype_ref column
            # Variables with datatype_ref use DatatypeRef element (e.g., D_Percentage, D_Colors)
            # Base types (UIntegerT, IntegerT, StringT, etc.) use Datatype element
            datatype_ref = param['datatype_ref'] if 'datatype_ref' in param.keys() else None

            if datatype_ref:
                # Use DatatypeRef for variables that reference custom datatypes
                datatyperef_elem = ET.SubElement(variable, 'DatatypeRef')
                datatyperef_elem.set('datatypeId', datatype_ref)
            else:
                # Create Datatype element for base types
                datatype_elem = ET.SubElement(variable, 'Datatype')
                if param['data_type']:
                    datatype_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', param['data_type'])

                # Handle ArrayT specific attributes and SimpleDatatype child
                if param['data_type'] == 'ArrayT':
                    # Set subindexAccessSupported attribute
                    if param['subindex_access_supported'] is not None:
                        datatype_elem.set('subindexAccessSupported', 'true' if param['subindex_access_supported'] else 'false')
                    # Set count attribute
                    if param['array_count']:
                        datatype_elem.set('count', str(param['array_count']))
                    # Add SimpleDatatype child element
                    if param['array_element_type']:
                        simple_dt = ET.SubElement(datatype_elem, 'SimpleDatatype')
                        simple_dt.set('{http://www.w3.org/2001/XMLSchema-instance}type', param['array_element_type'])
                        if param['array_element_bit_length']:
                            simple_dt.set('bitLength', str(param['array_element_bit_length']))
                        if param['array_element_fixed_length']:
                            simple_dt.set('fixedLength', str(param['array_element_fixed_length']))
                        # Add SingleValues to SimpleDatatype for ArrayT (PQA reconstruction)
                        self._add_variable_single_values(conn, param['id'], simple_dt)
                        # PQA Fix #30c: Add ValueRange to ArrayT SimpleDatatype if present
                        ae_min = param['array_element_min_value'] if 'array_element_min_value' in param.keys() else None
                        ae_max = param['array_element_max_value'] if 'array_element_max_value' in param.keys() else None
                        if ae_min is not None or ae_max is not None:
                            vr_elem = ET.SubElement(simple_dt, 'ValueRange')
                            ae_vr_xsi_type = param['array_element_value_range_xsi_type'] if 'array_element_value_range_xsi_type' in param.keys() else None
                            if ae_vr_xsi_type:
                                vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', ae_vr_xsi_type)
                            if ae_min is not None:
                                vr_elem.set('lowerValue', str(ae_min))
                            if ae_max is not None:
                                vr_elem.set('upperValue', str(ae_max))
                            ae_vr_name_text_id = param['array_element_value_range_name_text_id'] if 'array_element_value_range_name_text_id' in param.keys() else None
                            if ae_vr_name_text_id:
                                vr_name_elem = ET.SubElement(vr_elem, 'Name')
                                vr_name_elem.set('textId', ae_vr_name_text_id)

                # Handle RecordT specific attributes
                elif param['data_type'] == 'RecordT':
                    if param['subindex_access_supported'] is not None:
                        datatype_elem.set('subindexAccessSupported', 'true' if param['subindex_access_supported'] else 'false')
                    if param['bit_length']:
                        datatype_elem.set('bitLength', str(param['bit_length']))
                    # Add RecordItems
                    self._add_variable_record_items(conn, param['id'], datatype_elem, device_id)

                # Handle other types
                else:
                    if param['bit_length']:
                        datatype_elem.set('bitLength', str(param['bit_length']))

                    # PQA Fix #20: Add string encoding/fixedLength for StringT/OctetStringT from stored values
                    if param['data_type'] in ('StringT', 'OctetStringT'):
                        # Use stored encoding if available
                        encoding = param['string_encoding'] if 'string_encoding' in param.keys() and param['string_encoding'] else None
                        if encoding:
                            datatype_elem.set('encoding', encoding)
                        elif param['data_type'] == 'StringT':
                            datatype_elem.set('encoding', 'UTF-8')  # Default for StringT only if not stored
                        # Use stored fixedLength if available
                        fixed_length = param['string_fixed_length'] if 'string_fixed_length' in param.keys() and param['string_fixed_length'] else None
                        if fixed_length:
                            datatype_elem.set('fixedLength', str(fixed_length))

                    # PQA Fix #70: Add direct Datatype/Name element if present
                    dt_name_text_id = param['datatype_name_text_id'] if 'datatype_name_text_id' in param.keys() else None
                    if dt_name_text_id:
                        dt_name_elem = ET.SubElement(datatype_elem, 'Name')
                        dt_name_elem.set('textId', dt_name_text_id)

                    # Add SingleValues for enumerated types
                    self._add_variable_single_values(conn, param['id'], datatype_elem)

                    # Add ValueRange if min/max defined
                    if param['min_value'] is not None or param['max_value'] is not None:
                        value_range = ET.SubElement(datatype_elem, 'ValueRange')
                        # Add xsi:type attribute (e.g., UIntegerValueRangeT)
                        vr_xsi_type = param['value_range_xsi_type'] if 'value_range_xsi_type' in param.keys() else None
                        if vr_xsi_type:
                            value_range.set('{http://www.w3.org/2001/XMLSchema-instance}type', vr_xsi_type)
                        if param['min_value'] is not None:
                            value_range.set('lowerValue', str(param['min_value']))
                        if param['max_value'] is not None:
                            value_range.set('upperValue', str(param['max_value']))
                        # Add Name child element with textId
                        vr_name_text_id = param['value_range_name_text_id'] if 'value_range_name_text_id' in param.keys() else None
                        if vr_name_text_id:
                            vr_name_elem = ET.SubElement(value_range, 'Name')
                            vr_name_elem.set('textId', vr_name_text_id)

            # Add Name element using stored textId or fallback to lookup
            name_text_id = param['name_text_id'] if 'name_text_id' in param.keys() else None
            if name_text_id:
                name_elem = ET.SubElement(variable, 'Name')
                name_elem.set('textId', name_text_id)
            else:
                # Fallback: look up or generate text ID
                cursor2 = conn.cursor()
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
                    name_elem = ET.SubElement(variable, 'Name')
                    name_elem.set('textId', f'TN_{var_id}')

            # Add Description element using stored textId or fallback to lookup
            description_text_id = param['description_text_id'] if 'description_text_id' in param.keys() else None
            if description_text_id:
                desc_elem = ET.SubElement(variable, 'Description')
                desc_elem.set('textId', description_text_id)
            elif param['description']:
                # Fallback: look up text ID
                cursor2 = conn.cursor()
                cursor2.execute("""
                    SELECT text_id FROM iodd_text
                    WHERE device_id = ? AND text_value LIKE ? AND text_id LIKE 'TD_V_%'
                    LIMIT 1
                """, (device_id, f"%{param['description'][:50]}%"))
                desc_text_row = cursor2.fetchone()

                if desc_text_row:
                    desc_elem = ET.SubElement(variable, 'Description')
                    desc_elem.set('textId', desc_text_row['text_id'])

            # Add RecordItemInfo elements for RecordT types
            if param['data_type'] == 'RecordT':
                self._add_variable_record_item_info(conn, param['id'], variable)

        # PQA Fix #131: Reconstruct DirectParameterOverlay elements
        cursor.execute("""
            SELECT * FROM direct_parameter_overlays
            WHERE device_id = ?
            ORDER BY xml_order
        """, (device_id,))
        overlays = cursor.fetchall()

        for overlay in overlays:
            overlay_elem = ET.SubElement(collection, 'DirectParameterOverlay')
            overlay_elem.set('id', overlay['overlay_id'])

            if overlay['access_rights']:
                overlay_elem.set('accessRights', overlay['access_rights'])
            if overlay['dynamic']:
                overlay_elem.set('dynamic', 'true')
            if overlay['modifies_other_variables']:
                overlay_elem.set('modifiesOtherVariables', 'true')
            if overlay['excluded_from_data_storage']:
                overlay_elem.set('excludedFromDataStorage', 'true')

            # Add Datatype child
            if overlay['datatype_xsi_type']:
                datatype_elem = ET.SubElement(overlay_elem, 'Datatype')
                datatype_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', overlay['datatype_xsi_type'])
                if overlay['datatype_bit_length'] is not None:
                    datatype_elem.set('bitLength', str(overlay['datatype_bit_length']))

                # Add RecordItem children
                cursor2 = conn.cursor()
                cursor2.execute("""
                    SELECT * FROM direct_parameter_overlay_record_items
                    WHERE overlay_id = ?
                    ORDER BY order_index
                """, (overlay['id'],))
                record_items = cursor2.fetchall()

                for ri in record_items:
                    ri_elem = ET.SubElement(datatype_elem, 'RecordItem')
                    ri_elem.set('subindex', str(ri['subindex']))
                    if ri['bit_offset'] is not None:
                        ri_elem.set('bitOffset', str(ri['bit_offset']))
                    if ri['access_right_restriction']:
                        ri_elem.set('accessRightRestriction', ri['access_right_restriction'])

                    # Add SimpleDatatype or DatatypeRef
                    if ri['simple_datatype']:
                        simple_dt = ET.SubElement(ri_elem, 'SimpleDatatype')
                        simple_dt.set('{http://www.w3.org/2001/XMLSchema-instance}type', ri['simple_datatype'])
                        # PQA Fix #132: Add SimpleDatatype@id attribute
                        if ri['simple_datatype_id']:
                            simple_dt.set('id', ri['simple_datatype_id'])
                        if ri['bit_length'] is not None:
                            simple_dt.set('bitLength', str(ri['bit_length']))

                        # PQA Fix #137: Add ValueRange child
                        if ri['min_value'] is not None or ri['max_value'] is not None:
                            vr_elem = ET.SubElement(simple_dt, 'ValueRange')
                            if ri['value_range_xsi_type']:
                                vr_elem.set('{http://www.w3.org/2001/XMLSchema-instance}type', ri['value_range_xsi_type'])
                            if ri['min_value'] is not None:
                                vr_elem.set('lowerValue', ri['min_value'])
                            if ri['max_value'] is not None:
                                vr_elem.set('upperValue', ri['max_value'])
                            # Add ValueRange/Name child
                            if ri['value_range_name_text_id']:
                                vr_name = ET.SubElement(vr_elem, 'Name')
                                vr_name.set('textId', ri['value_range_name_text_id'])

                        # Add SingleValue children
                        cursor3 = conn.cursor()
                        cursor3.execute("""
                            SELECT * FROM direct_parameter_overlay_record_item_single_values
                            WHERE record_item_id = ?
                            ORDER BY order_index
                        """, (ri['id'],))
                        single_values = cursor3.fetchall()

                        for sv in single_values:
                            sv_elem = ET.SubElement(simple_dt, 'SingleValue')
                            sv_elem.set('value', sv['value'])
                            if sv['name_text_id']:
                                sv_name = ET.SubElement(sv_elem, 'Name')
                                sv_name.set('textId', sv['name_text_id'])

                    elif ri['datatype_ref']:
                        dt_ref = ET.SubElement(ri_elem, 'DatatypeRef')
                        dt_ref.set('datatypeId', ri['datatype_ref'])

                    # Add Name child
                    if ri['name_text_id']:
                        ri_name = ET.SubElement(ri_elem, 'Name')
                        ri_name.set('textId', ri['name_text_id'])

                    # Add Description child
                    if ri['description_text_id']:
                        ri_desc = ET.SubElement(ri_elem, 'Description')
                        ri_desc.set('textId', ri['description_text_id'])

            # Add RecordItemInfo children
            cursor2 = conn.cursor()
            cursor2.execute("""
                SELECT * FROM direct_parameter_overlay_record_item_info
                WHERE overlay_id = ?
                ORDER BY order_index
            """, (overlay['id'],))
            record_item_info = cursor2.fetchall()

            for rii in record_item_info:
                rii_elem = ET.SubElement(overlay_elem, 'RecordItemInfo')
                rii_elem.set('subindex', str(rii['subindex']))
                if rii['default_value'] is not None:
                    rii_elem.set('defaultValue', rii['default_value'])
                if rii['modifies_other_variables']:
                    rii_elem.set('modifiesOtherVariables', 'true' if rii['modifies_other_variables'] else 'false')

            # Add Name child
            if overlay['name_text_id']:
                overlay_name = ET.SubElement(overlay_elem, 'Name')
                overlay_name.set('textId', overlay['name_text_id'])

        return collection

    def _create_error_type_collection(self, conn: sqlite3.Connection,
                                      device_id: int) -> Optional[ET.Element]:
        """Create ErrorTypeCollection from error_types table

        PQA Fix #37: Properly distinguish between:
        - ErrorType: Custom errors with Name/Description children
        - StdErrorTypeRef: Standard IO-Link error references with only attributes
        """
        cursor = conn.cursor()

        # PQA Fix #56: Check if original IODD had ErrorTypeCollection (even if empty)
        cursor.execute("""
            SELECT has_error_type_collection FROM devices WHERE id = ?
        """, (device_id,))
        device_row = cursor.fetchone()
        has_collection = device_row['has_error_type_collection'] if device_row and 'has_error_type_collection' in device_row.keys() else False

        cursor.execute("""
            SELECT code, additional_code, has_code_attr, xml_order,
                   is_custom, name_text_id, description_text_id
            FROM error_types
            WHERE device_id = ?
            ORDER BY COALESCE(xml_order, additional_code)
        """, (device_id,))
        error_types = cursor.fetchall()

        if not error_types:
            # PQA Fix #56: Output empty ErrorTypeCollection if original had one
            if has_collection:
                return ET.Element('ErrorTypeCollection')
            return None

        collection = ET.Element('ErrorTypeCollection')

        for error in error_types:
            is_custom = error['is_custom'] if 'is_custom' in error.keys() else False

            if is_custom:
                # PQA Fix #37: Custom ErrorType with Name and Description children
                error_elem = ET.SubElement(collection, 'ErrorType')
                error_elem.set('code', str(error['code']))
                error_elem.set('additionalCode', str(error['additional_code']))

                # Add Name element with textId
                name_text_id = error['name_text_id'] if 'name_text_id' in error.keys() else None
                if name_text_id:
                    name_elem = ET.SubElement(error_elem, 'Name')
                    name_elem.set('textId', name_text_id)

                # Add Description element with textId
                desc_text_id = error['description_text_id'] if 'description_text_id' in error.keys() else None
                if desc_text_id:
                    desc_elem = ET.SubElement(error_elem, 'Description')
                    desc_elem.set('textId', desc_text_id)
            else:
                # StdErrorTypeRef has code (optional) and additionalCode
                error_ref = ET.SubElement(collection, 'StdErrorTypeRef')
                # PQA: Only output code attribute if it was in the original
                has_code = error['has_code_attr'] if 'has_code_attr' in error.keys() else True
                if has_code:
                    error_ref.set('code', str(error['code']))
                error_ref.set('additionalCode', str(error['additional_code']))

        return collection

    def _create_event_collection(self, conn: sqlite3.Connection,
                                 device_id: int) -> Optional[ET.Element]:
        """Create EventCollection from events table

        Distinguishes between StdEventRef (standard IO-Link events) and
        Event (device-specific events) based on event_type being NULL.
        Preserves original order using order_index column (or id as fallback).
        Uses stored textIds directly instead of reverse-lookup for accuracy.
        """
        cursor = conn.cursor()
        # Order by order_index (if available) or id to preserve original XML order
        # PQA Fix #46: Include mode column
        cursor.execute("""
            SELECT code, name, description, event_type,
                   name_text_id, description_text_id, order_index, mode
            FROM events
            WHERE device_id = ?
            ORDER BY COALESCE(order_index, id)
        """, (device_id,))
        events = cursor.fetchall()

        # PQA Fix: Check if original had EventCollection element (even if empty)
        cursor.execute("""
            SELECT has_event_collection
            FROM devices
            WHERE id = ?
        """, (device_id,))
        device_row = cursor.fetchone()
        has_event_collection = device_row['has_event_collection'] if device_row else False

        if not events:
            # If original had EventCollection element, output empty element
            if has_event_collection:
                return ET.Element('EventCollection')
            else:
                return None

        collection = ET.Element('EventCollection')

        for event in events:
            # Check for stored textIds - if name_text_id is NULL, this is a StdEventRef
            name_text_id = event['name_text_id'] if 'name_text_id' in event.keys() else None
            mode = event['mode'] if 'mode' in event.keys() else None  # PQA Fix #46

            # StdEventRef: standard IO-Link events have no type and no name_text_id
            # (Parser stores NULL for name_text_id on StdEventRef elements)
            is_std_event = (event['event_type'] is None and name_text_id is None)

            if is_std_event:
                std_ref = ET.SubElement(collection, 'StdEventRef')
                std_ref.set('code', str(event['code']))
                # PQA Fix #46: Add mode attribute if present
                if mode:
                    std_ref.set('mode', mode)
            else:
                # Event: device-specific events with type, name, description
                event_elem = ET.SubElement(collection, 'Event')
                event_elem.set('code', str(event['code']))
                if event['event_type']:
                    event_elem.set('type', event['event_type'])
                # PQA Fix #46: Add mode attribute if present
                if mode:
                    event_elem.set('mode', mode)

                # Use stored textIds directly (no reverse-lookup needed)
                if name_text_id:
                    name_elem = ET.SubElement(event_elem, 'Name')
                    name_elem.set('textId', name_text_id)

                desc_text_id = event['description_text_id'] if 'description_text_id' in event.keys() else None
                if desc_text_id:
                    desc_elem = ET.SubElement(event_elem, 'Description')
                    desc_elem.set('textId', desc_text_id)

        return collection

    def _create_text_collection(self, conn: sqlite3.Connection,
                               device_id: int) -> Optional[ET.Element]:
        """Create ExternalTextCollection with multi-language texts

        IODD structure:
        - PrimaryLanguage (usually English) - only ONE
        - Language (secondary languages) - zero or more
        """
        cursor = conn.cursor()
        # Get languages ordered by language_order (PQA: preserve original Language element order)
        cursor.execute("""
            SELECT DISTINCT language_code, MIN(language_order) as lang_order
            FROM iodd_text WHERE device_id = ?
            GROUP BY language_code
            ORDER BY lang_order, language_code
        """, (device_id,))
        languages = [row['language_code'] for row in cursor.fetchall()]

        if not languages:
            return None

        collection = ET.Element('ExternalTextCollection')

        # Determine primary language: the one with language_order=0, or 'en', or first
        cursor.execute("""
            SELECT DISTINCT language_code FROM iodd_text
            WHERE device_id = ? AND language_order = 0
        """, (device_id,))
        primary_row = cursor.fetchone()
        if primary_row:
            primary_lang_code = primary_row['language_code']
        elif 'en' in languages:
            primary_lang_code = 'en'
        else:
            primary_lang_code = languages[0]

        # Create PrimaryLanguage element
        primary_elem = ET.SubElement(collection, 'PrimaryLanguage')
        primary_elem.set('{http://www.w3.org/XML/1998/namespace}lang', primary_lang_code)

        # Get all texts for primary language
        # PQA Fix #66: Include is_text_redefine column
        cursor.execute("""
            SELECT text_id, text_value, is_text_redefine FROM iodd_text
            WHERE device_id = ? AND language_code = ?
            ORDER BY xml_order, id
        """, (device_id, primary_lang_code))
        texts = cursor.fetchall()

        for text in texts:
            # PQA Fix #66: Output TextRedefine instead of Text if appropriate
            is_redefine = text['is_text_redefine'] if 'is_text_redefine' in text.keys() and text['is_text_redefine'] else False
            elem_name = 'TextRedefine' if is_redefine else 'Text'
            text_elem = ET.SubElement(primary_elem, elem_name)
            text_elem.set('id', text['text_id'])
            text_elem.set('value', text['text_value'] or '')

        # Create Language elements for secondary languages
        for lang_code in languages:
            if lang_code == primary_lang_code:
                continue  # Skip primary language

            lang_elem = ET.SubElement(collection, 'Language')
            lang_elem.set('{http://www.w3.org/XML/1998/namespace}lang', lang_code)

            # PQA Fix #66: Include is_text_redefine column
            cursor.execute("""
                SELECT text_id, text_value, is_text_redefine FROM iodd_text
                WHERE device_id = ? AND language_code = ?
                ORDER BY xml_order, id
            """, (device_id, lang_code))
            texts = cursor.fetchall()

            for text in texts:
                # PQA Fix #66: Output TextRedefine instead of Text if appropriate
                is_redefine = text['is_text_redefine'] if 'is_text_redefine' in text.keys() and text['is_text_redefine'] else False
                elem_name = 'TextRedefine' if is_redefine else 'Text'
                text_elem = ET.SubElement(lang_elem, elem_name)
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
