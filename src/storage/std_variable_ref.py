"""
Storage for StdVariableRef elements from IODD VariableCollection

Preserves the original order and attributes of standard variable references
for accurate PQA reconstruction.
"""

import logging
from typing import List, Optional

from .base import BaseSaver

logger = logging.getLogger(__name__)


class StdVariableRefSaver(BaseSaver):
    """
    Saves StdVariableRef elements from IODD VariableCollection

    Preserves:
    - variable_id (e.g., V_VendorName, V_ProductName)
    - defaultValue attribute
    - fixedLengthRestriction attribute
    - excludedFromDataStorage attribute
    - Original order in the IODD file
    - SingleValue and StdSingleValueRef children
    """

    def save(self, device_id: int, std_variable_refs: List) -> Optional[int]:
        """
        Save StdVariableRef elements for a device

        Args:
            device_id: The device ID to associate data with
            std_variable_refs: List of StdVariableRef objects from parser

        Returns:
            None (inserts multiple records)
        """
        if not std_variable_refs:
            logger.warning(f"!!! STD_VARIABLE_REF SAVER: No StdVariableRef data to save for device {device_id}")
            return None

        logger.warning(f"!!! STD_VARIABLE_REF SAVER: Saving {len(std_variable_refs)} StdVariableRefs for device {device_id}")

        # Delete existing records for this device (cascade will delete single values)
        self._delete_existing('std_variable_refs', device_id)

        # Insert each StdVariableRef and its children
        for ref in std_variable_refs:
            # Insert the StdVariableRef record
            query = """
                INSERT INTO std_variable_refs
                (device_id, variable_id, default_value, fixed_length_restriction,
                 excluded_from_data_storage, order_index)
                VALUES (?, ?, ?, ?, ?, ?)
            """
            self.cursor.execute(query, (
                device_id,
                ref.variable_id,
                ref.default_value,
                ref.fixed_length_restriction,
                1 if ref.excluded_from_data_storage else (0 if ref.excluded_from_data_storage is False else None),
                ref.order_index
            ))

            # Get the inserted ID
            std_var_ref_id = self.cursor.lastrowid

            # Insert SingleValue children if any
            if hasattr(ref, 'single_values') and ref.single_values:
                sv_query = """
                    INSERT INTO std_variable_ref_single_values
                    (std_variable_ref_id, value, name_text_id, is_std_ref, order_index)
                    VALUES (?, ?, ?, ?, ?)
                """
                sv_values = [
                    (std_var_ref_id, sv.value, sv.name_text_id, 1 if sv.is_std_ref else 0, sv.order_index)
                    for sv in ref.single_values
                ]
                self._execute_many(sv_query, sv_values)

            # PQA Fix #5: Insert ValueRange/StdValueRangeRef children if any
            if hasattr(ref, 'value_ranges') and ref.value_ranges:
                vr_query = """
                    INSERT INTO std_variable_ref_value_ranges
                    (std_variable_ref_id, lower_value, upper_value, is_std_ref, order_index)
                    VALUES (?, ?, ?, ?, ?)
                """
                vr_values = [
                    (std_var_ref_id, vr.lower_value, vr.upper_value, 1 if vr.is_std_ref else 0, vr.order_index)
                    for vr in ref.value_ranges
                ]
                self._execute_many(vr_query, vr_values)

            # Insert StdRecordItemRef children if any
            if hasattr(ref, 'record_item_refs') and ref.record_item_refs:
                ri_query = """
                    INSERT INTO std_record_item_refs
                    (std_variable_ref_id, subindex, default_value, order_index)
                    VALUES (?, ?, ?, ?)
                """
                for idx, ri in enumerate(ref.record_item_refs):
                    self._execute(ri_query, (std_var_ref_id, ri.subindex, ri.default_value, idx))
                    ri_ref_id = self._get_lastrowid()
                    
                    # PQA Fix #76: Insert SingleValue children for this StdRecordItemRef
                    if hasattr(ri, 'single_values') and ri.single_values:
                        ri_sv_query = """
                            INSERT INTO std_record_item_ref_single_values
                            (std_record_item_ref_id, value, name_text_id, is_std_ref, order_index)
                            VALUES (?, ?, ?, ?, ?)
                        """
                        ri_sv_values = [
                            (ri_ref_id, sv.value, sv.name_text_id, 1 if sv.is_std_ref else 0, sv.order_index)
                            for sv in ri.single_values
                        ]
                        self._execute_many(ri_sv_query, ri_sv_values)

        logger.debug(f"Saved {len(std_variable_refs)} StdVariableRef records for device {device_id}")
        return None
