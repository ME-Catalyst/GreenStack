"""
Event storage handler

Manages device events and error types.
"""

import logging
from .base import BaseSaver

logger = logging.getLogger(__name__)


class EventSaver(BaseSaver):
    """Handles event and error type storage"""

    def save(self, device_id: int, events: list) -> None:
        """
        Save all events for a device

        Args:
            device_id: Database ID of the device
            events: List of Event objects
        """
        if not events:
            logger.debug(f"No events to save for device {device_id}")
            return

        # Delete existing
        self._delete_existing('events', device_id)

        # Prepare bulk insert
        query = """
            INSERT INTO events (
                device_id, code, name, description, event_type
            ) VALUES (?, ?, ?, ?, ?)
        """

        params_list = []
        for event in events:
            params_list.append((
                device_id,
                getattr(event, 'code', None),
                getattr(event, 'name', None),
                getattr(event, 'description', None),
                getattr(event, 'event_type', None),
            ))

        if params_list:
            self._execute_many(query, params_list)
            logger.info(f"Saved {len(params_list)} events for device {device_id}")


class ErrorTypeSaver(BaseSaver):
    """Handles error type storage"""

    def save(self, device_id: int, error_types: list) -> None:
        """
        Save all error types for a device

        Args:
            device_id: Database ID of the device
            error_types: List of ErrorType objects
        """
        if not error_types:
            logger.debug(f"No error types to save for device {device_id}")
            return

        # Delete existing
        self._delete_existing('error_types', device_id)

        # Prepare bulk insert
        query = """
            INSERT INTO error_types (
                device_id, code, additional_code, name, description
            ) VALUES (?, ?, ?, ?, ?)
        """

        params_list = []
        for error in error_types:
            params_list.append((
                device_id,
                getattr(error, 'code', None),
                getattr(error, 'additional_code', None),
                getattr(error, 'name', None),
                getattr(error, 'description', None),
            ))

        if params_list:
            self._execute_many(query, params_list)
            logger.info(f"Saved {len(params_list)} error types for device {device_id}")
