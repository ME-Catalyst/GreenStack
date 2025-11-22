"""
Multi-language Text storage handler

Manages IODD text entries in multiple languages.
"""

import logging
from .base import BaseSaver

logger = logging.getLogger(__name__)


class TextSaver(BaseSaver):
    """Handles multi-language text storage"""

    def save(self, device_id: int, all_text_data: dict, text_xml_order: dict = None, language_order: dict = None) -> None:
        """
        Save all multi-language text entries for a device

        Args:
            device_id: Database ID of the device
            all_text_data: Dict mapping text_id to language_code to text_value
                          Example: {'TID123': {'en': 'Hello', 'de': 'Hallo'}}
            text_xml_order: Dict mapping text_id to Dict of language_code to xml_order
                          Example: {'TID123': {'en': 0, 'de': 1}, 'TID456': {'en': 1, 'de': 0}}
            language_order: Dict mapping language_code to order of Language element
                          Example: {'en': 0, 'de': 1, 'fr': 2}
        """
        if not all_text_data:
            logger.debug(f"No text data to save for device {device_id}")
            return

        if text_xml_order is None:
            text_xml_order = {}
        if language_order is None:
            language_order = {}

        # Delete existing
        self._delete_existing('iodd_text', device_id)

        query = """
            INSERT INTO iodd_text (device_id, text_id, language_code, text_value, xml_order, language_order)
            VALUES (?, ?, ?, ?, ?, ?)
        """

        params_list = []
        for text_id, languages in all_text_data.items():
            text_orders = text_xml_order.get(text_id, {})  # PQA: Get order per language
            for language_code, text_value in languages.items():
                xml_order = text_orders.get(language_code)  # PQA: Order for this specific language
                lang_order = language_order.get(language_code)  # PQA: Order of Language element
                params_list.append((
                    device_id,
                    text_id,
                    language_code,
                    text_value,
                    xml_order,
                    lang_order,
                ))

        if params_list:
            self._execute_many(query, params_list)
            text_id_count = len(all_text_data)
            entry_count = len(params_list)
            logger.info(f"Saved {entry_count} text entries across {text_id_count} text IDs for device {device_id}")
