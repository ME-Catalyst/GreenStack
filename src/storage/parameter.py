"""
Parameter storage handler

Manages device parameters including access rights, data types, and constraints.
"""

import logging
import json
from .base import BaseSaver

logger = logging.getLogger(__name__)


class ParameterSaver(BaseSaver):
    """Handles parameter storage for devices"""

    def save(self, device_id: int, parameters: list) -> None:
        """
        Save all parameters for a device

        Args:
            device_id: Database ID of the device
            parameters: List of Parameter objects
        """
        if not parameters:
            logger.debug(f"No parameters to save for device {device_id}")
            return

        # Delete existing parameters
        self._delete_existing('parameters', device_id)

        # Prepare bulk insert
        query = """
            INSERT INTO parameters (
                device_id, param_index, name, data_type,
                access_rights, default_value, min_value,
                max_value, unit, description, enumeration_values, bit_length,
                dynamic, excluded_from_data_storage, modifies_other_variables,
                unit_code, value_range_name, variable_id
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """

        params_list = []
        for param in parameters:
            # Serialize enumeration values as JSON
            enum_json = None
            if hasattr(param, 'enumeration_values') and param.enumeration_values:
                enum_json = json.dumps(param.enumeration_values)

            params_list.append((
                device_id,
                getattr(param, 'index', None),
                getattr(param, 'name', None),
                getattr(param.data_type, 'value', None) if hasattr(param, 'data_type') and hasattr(param.data_type, 'value') else getattr(param, 'data_type', None),
                getattr(param.access_rights, 'value', None) if hasattr(param, 'access_rights') and hasattr(param.access_rights, 'value') else getattr(param, 'access_rights', None),
                str(param.default_value) if hasattr(param, 'default_value') and param.default_value is not None else None,
                str(param.min_value) if hasattr(param, 'min_value') and param.min_value is not None else None,
                str(param.max_value) if hasattr(param, 'max_value') and param.max_value is not None else None,
                getattr(param, 'unit', None),
                getattr(param, 'description', None),
                enum_json,
                getattr(param, 'bit_length', None),
                1 if getattr(param, 'dynamic', False) else 0,
                1 if getattr(param, 'excluded_from_data_storage', False) else 0,
                1 if getattr(param, 'modifies_other_variables', False) else 0,
                getattr(param, 'unit_code', None),
                getattr(param, 'value_range_name', None),
                getattr(param, 'id', None),  # variable_id is stored as param.id
            ))

        # Bulk insert
        self._execute_many(query, params_list)
        logger.info(f"Saved {len(params_list)} parameters for device {device_id}")
