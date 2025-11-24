"""
Custom Datatype storage handler

Manages custom datatypes including single values and record items.
"""

import logging
from .base import BaseSaver

logger = logging.getLogger(__name__)


class CustomDatatypeSaver(BaseSaver):
    """Handles custom datatype storage"""

    def save(self, device_id: int, custom_datatypes: list) -> None:
        """
        Save all custom datatypes for a device

        Args:
            device_id: Database ID of the device
            custom_datatypes: List of CustomDatatype objects
        """
        if not custom_datatypes:
            logger.debug(f"No custom datatypes to save for device {device_id}")
            return

        # Delete existing - must delete child tables first (FK cascade is disabled)
        # Get existing datatype IDs for this device
        self._execute("SELECT id FROM custom_datatypes WHERE device_id = ?", (device_id,))
        existing_ids = [row[0] for row in self._fetch_all()]

        if existing_ids:
            # Delete child tables first (record_item_single_values, record_items, single_values)
            placeholders = ','.join('?' * len(existing_ids))

            # Get record_item IDs for single value deletion
            self._execute(f"SELECT id FROM custom_datatype_record_items WHERE datatype_id IN ({placeholders})", existing_ids)
            record_item_ids = [row[0] for row in self._fetch_all()]

            if record_item_ids:
                ri_placeholders = ','.join('?' * len(record_item_ids))
                self._execute(f"DELETE FROM custom_datatype_record_item_single_values WHERE record_item_id IN ({ri_placeholders})", record_item_ids)

            self._execute(f"DELETE FROM custom_datatype_record_items WHERE datatype_id IN ({placeholders})", existing_ids)
            self._execute(f"DELETE FROM custom_datatype_single_values WHERE datatype_id IN ({placeholders})", existing_ids)

        # Now delete the parent table
        self._delete_existing('custom_datatypes', device_id)

        # Save each custom datatype
        for datatype in custom_datatypes:
            datatype_db_id = self._save_datatype(device_id, datatype)
            if datatype_db_id:
                self._save_single_values(datatype_db_id, datatype)
                self._save_record_items(datatype_db_id, datatype)

        logger.info(f"Saved {len(custom_datatypes)} custom datatypes for device {device_id}")

    def _save_datatype(self, device_id: int, datatype) -> int:
        """Save main custom datatype entry"""
        # PQA Fix #59: Added string_fixed_length, string_encoding
        query = """
            INSERT INTO custom_datatypes (
                device_id, datatype_id, datatype_xsi_type,
                bit_length, subindex_access_supported,
                min_value, max_value, value_range_xsi_type, value_range_name_text_id,
                string_fixed_length, string_encoding
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # PQA Fix: Preserve None for subindex_access_supported (don't output if not in original)
        subindex_val = getattr(datatype, 'subindex_access_supported', None)
        subindex_db_val = None if subindex_val is None else (1 if subindex_val else 0)

        params = (
            device_id,
            getattr(datatype, 'datatype_id', None),
            getattr(datatype, 'datatype_xsi_type', None),
            getattr(datatype, 'bit_length', None),
            subindex_db_val,
            getattr(datatype, 'min_value', None),  # PQA Fix #30b
            getattr(datatype, 'max_value', None),  # PQA Fix #30b
            getattr(datatype, 'value_range_xsi_type', None),  # PQA Fix #30b
            getattr(datatype, 'value_range_name_text_id', None),  # PQA Fix #30b
            getattr(datatype, 'string_fixed_length', None),  # PQA Fix #59
            getattr(datatype, 'string_encoding', None),  # PQA Fix #59
        )

        self._execute(query, params)
        return self._get_lastrowid()

    def _save_single_values(self, datatype_db_id: int, datatype):
        """Save single values for a custom datatype"""
        if not hasattr(datatype, 'single_values') or not datatype.single_values:
            return

        # PQA Fix #38: Added xml_order for proper reconstruction ordering
        query = """
            INSERT INTO custom_datatype_single_values (
                datatype_id, value, name, text_id, xsi_type, xml_order
            ) VALUES (?, ?, ?, ?, ?, ?)
        """

        params_list = []
        for single_val in datatype.single_values:
            params_list.append((
                datatype_db_id,
                getattr(single_val, 'value', None),
                getattr(single_val, 'name', None),
                getattr(single_val, 'text_id', None),  # PQA: preserve original textId
                getattr(single_val, 'xsi_type', None),  # PQA: preserve xsi:type
                getattr(single_val, 'xml_order', None),  # PQA Fix #38: preserve original order
            ))

        if params_list:
            self._execute_many(query, params_list)

    def _save_record_items(self, datatype_db_id: int, datatype):
        """Save record items for a custom datatype"""
        if not hasattr(datatype, 'record_items') or not datatype.record_items:
            return

        # PQA Fix #69: Added fixed_length and encoding columns
        query = """
            INSERT INTO custom_datatype_record_items (
                datatype_id, subindex, bit_offset, bit_length,
                datatype_ref, name, name_text_id, description_text_id,
                min_value, max_value, value_range_xsi_type, value_range_name_text_id, access_right_restriction,
                fixed_length, encoding
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        # PQA Fix #21: Save one at a time to get record_item_id for SingleValues
        for record_item in datatype.record_items:
            params = (
                datatype_db_id,
                getattr(record_item, 'subindex', None),
                getattr(record_item, 'bit_offset', None),
                getattr(record_item, 'bit_length', None),
                getattr(record_item, 'data_type', getattr(record_item, 'datatype_ref', None)),
                getattr(record_item, 'name', None),
                getattr(record_item, 'name_text_id', None),  # PQA: preserve original textId
                getattr(record_item, 'description_text_id', None),  # PQA: Description textId
                getattr(record_item, 'min_value', None),  # PQA: ValueRange
                getattr(record_item, 'max_value', None),  # PQA: ValueRange
                getattr(record_item, 'value_range_xsi_type', None),  # PQA: ValueRange
                getattr(record_item, 'value_range_name_text_id', None),  # PQA Fix #30: ValueRange/Name
                getattr(record_item, 'access_right_restriction', None),  # PQA: RecordItem attribute
                getattr(record_item, 'fixed_length', None),  # PQA Fix #69: SimpleDatatype@fixedLength
                getattr(record_item, 'encoding', None),  # PQA Fix #69: SimpleDatatype@encoding
            )
            self._execute(query, params)
            record_item_id = self._get_lastrowid()

            # PQA Fix #21: Save SingleValues for this RecordItem
            self._save_record_item_single_values(record_item_id, record_item)

    def _save_record_item_single_values(self, record_item_id: int, record_item):
        """PQA Fix #21: Save single values inside RecordItem/SimpleDatatype"""
        single_values = getattr(record_item, 'single_values', [])
        if not single_values:
            return

        query = """
            INSERT INTO custom_datatype_record_item_single_values (
                record_item_id, value, name, name_text_id, xsi_type
            ) VALUES (?, ?, ?, ?, ?)
        """

        params_list = []
        for sv in single_values:
            params_list.append((
                record_item_id,
                getattr(sv, 'value', None),
                getattr(sv, 'name', None),
                getattr(sv, 'text_id', None),
                getattr(sv, 'xsi_type', None),
            ))

        if params_list:
            self._execute_many(query, params_list)
