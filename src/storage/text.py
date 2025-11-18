"""
Multi-language Text storage handler

Manages IODD text entries in multiple languages.
"""

import logging
from .base import BaseSaver

logger = logging.getLogger(__name__)


class TextSaver(BaseSaver):
    """Handles multi-language text storage"""

    def save(self, device_id: int, all_text_data: dict) -> None:
        """
        Save all multi-language text entries for a device

        Args:
            device_id: Database ID of the device
            all_text_data: Dict mapping text_id to language_code to text_value
                          Example: {'TID123': {'en': 'Hello', 'de': 'Hallo'}}
        """
        if not all_text_data:
            logger.debug(f"No text data to save for device {device_id}")
            return

        # Delete existing
        self._delete_existing('iodd_text', device_id)

        query = """
            INSERT INTO iodd_text (device_id, text_id, language_code, text_value)
            VALUES (?, ?, ?, ?)
        """

        params_list = []
        for text_id, languages in all_text_data.items():
            for language_code, text_value in languages.items():
                params_list.append((
                    device_id,
                    text_id,
                    language_code,
                    text_value,
                ))

        if params_list:
            self._execute_many(query, params_list)
            text_id_count = len(all_text_data)
            entry_count = len(params_list)
            logger.info(f"Saved {entry_count} text entries across {text_id_count} text IDs for device {device_id}")
