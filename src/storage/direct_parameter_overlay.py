"""
DirectParameterOverlay storage handler

PQA Fix #131: Manages DirectParameterOverlay elements including their
record items, record item info, and single values.
"""

import logging
from .base import BaseSaver

logger = logging.getLogger(__name__)


class DirectParameterOverlaySaver(BaseSaver):
    """Handles DirectParameterOverlay storage for devices"""

    def save(self, device_id: int, overlays: list) -> None:
        """
        Save all DirectParameterOverlay elements for a device

        Args:
            device_id: Database ID of the device
            overlays: List of DirectParameterOverlay objects
        """
        if not overlays:
            logger.debug(f"No DirectParameterOverlay elements to save for device {device_id}")
            return

        logger.info(f"Saving {len(overlays)} DirectParameterOverlay elements for device {device_id}")

        # Delete existing - must delete child tables first (FK cascade is disabled)
        # Get existing overlay IDs for this device
        self._execute("SELECT id FROM direct_parameter_overlays WHERE device_id = ?", (device_id,))
        existing_ids = [row[0] for row in self._fetch_all()]

        if existing_ids:
            # Delete child tables first
            placeholders = ','.join('?' * len(existing_ids))

            # Get all record_item IDs to delete their single_values
            self._execute(
                f"SELECT id FROM direct_parameter_overlay_record_items WHERE overlay_id IN ({placeholders})",
                existing_ids
            )
            record_item_ids = [row[0] for row in self._fetch_all()]

            if record_item_ids:
                ri_placeholders = ','.join('?' * len(record_item_ids))
                self._execute(
                    f"DELETE FROM direct_parameter_overlay_record_item_single_values WHERE record_item_id IN ({ri_placeholders})",
                    record_item_ids
                )

            # Delete record_item_info
            self._execute(
                f"DELETE FROM direct_parameter_overlay_record_item_info WHERE overlay_id IN ({placeholders})",
                existing_ids
            )

            # Delete record_items
            self._execute(
                f"DELETE FROM direct_parameter_overlay_record_items WHERE overlay_id IN ({placeholders})",
                existing_ids
            )

        # Now delete the parent table
        self._delete_existing('direct_parameter_overlays', device_id)

        for idx, overlay in enumerate(overlays):
            # Insert DirectParameterOverlay
            query = """
                INSERT INTO direct_parameter_overlays (
                    device_id, overlay_id, access_rights, dynamic,
                    modifies_other_variables, excluded_from_data_storage,
                    name_text_id, datatype_xsi_type, datatype_bit_length, xml_order
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """

            self._execute(query, (
                device_id,
                getattr(overlay, 'overlay_id', None),
                getattr(overlay, 'access_rights', None),
                1 if getattr(overlay, 'dynamic', False) else 0,
                1 if getattr(overlay, 'modifies_other_variables', False) else 0,
                1 if getattr(overlay, 'excluded_from_data_storage', False) else 0,
                getattr(overlay, 'name_text_id', None),
                getattr(overlay, 'datatype_xsi_type', None),
                getattr(overlay, 'datatype_bit_length', None),
                idx  # xml_order
            ))

            overlay_db_id = self._get_lastrowid()

            # Save record_items if present
            record_items = getattr(overlay, 'record_items', [])
            if record_items:
                self._save_record_items(overlay_db_id, record_items)

            # Save record_item_info if present
            record_item_info = getattr(overlay, 'record_item_info', [])
            if record_item_info:
                self._save_record_item_info(overlay_db_id, record_item_info)

        logger.info(f"Saved {len(overlays)} DirectParameterOverlay elements for device {device_id}")

    def _save_record_items(self, overlay_id: int, record_items: list) -> None:
        """
        Save RecordItem elements for a DirectParameterOverlay

        Args:
            overlay_id: Database ID of the parent overlay
            record_items: List of DirectParameterOverlayRecordItem objects
        """
        for idx, ri in enumerate(record_items):
            # Insert RecordItem
            query = """
                INSERT INTO direct_parameter_overlay_record_items (
                    overlay_id, subindex, bit_offset, bit_length,
                    datatype_ref, simple_datatype, simple_datatype_id, name, name_text_id,
                    description, description_text_id, access_right_restriction, order_index
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """
            self._execute(query, (
                overlay_id,
                getattr(ri, 'subindex', 0),
                getattr(ri, 'bit_offset', None),
                getattr(ri, 'bit_length', None),
                getattr(ri, 'datatype_ref', None),
                getattr(ri, 'simple_datatype', None),
                getattr(ri, 'simple_datatype_id', None),  # PQA Fix #132
                getattr(ri, 'name', None),
                getattr(ri, 'name_text_id', None),
                getattr(ri, 'description', None),
                getattr(ri, 'description_text_id', None),
                getattr(ri, 'access_right_restriction', None),
                idx  # order_index
            ))

            record_item_id = self._get_lastrowid()

            # Save SingleValues for this RecordItem
            single_values = getattr(ri, 'single_values', [])
            if single_values:
                self._save_single_values(record_item_id, single_values)

    def _save_single_values(self, record_item_id: int, single_values: list) -> None:
        """
        Save SingleValue elements for a RecordItem's SimpleDatatype

        Args:
            record_item_id: Database ID of the parent record item
            single_values: List of DirectParameterOverlayRecordItemSingleValue objects
        """
        query = """
            INSERT INTO direct_parameter_overlay_record_item_single_values (
                record_item_id, value, name, name_text_id, order_index
            ) VALUES (?, ?, ?, ?, ?)
        """

        values_list = []
        for idx, sv in enumerate(single_values):
            values_list.append((
                record_item_id,
                getattr(sv, 'value', ''),
                getattr(sv, 'name', None),
                getattr(sv, 'name_text_id', None),
                idx  # order_index
            ))

        self._execute_many(query, values_list)

    def _save_record_item_info(self, overlay_id: int, record_item_info: list) -> None:
        """
        Save RecordItemInfo elements for a DirectParameterOverlay

        Args:
            overlay_id: Database ID of the parent overlay
            record_item_info: List of DirectParameterOverlayRecordItemInfo objects
        """
        query = """
            INSERT INTO direct_parameter_overlay_record_item_info (
                overlay_id, subindex, default_value, modifies_other_variables, order_index
            ) VALUES (?, ?, ?, ?, ?)
        """

        values_list = []
        for idx, rii in enumerate(record_item_info):
            modifies = getattr(rii, 'modifies_other_variables', False)
            values_list.append((
                overlay_id,
                getattr(rii, 'subindex', 0),
                getattr(rii, 'default_value', None),
                1 if modifies is True else 0,
                idx  # order_index
            ))

        self._execute_many(query, values_list)
