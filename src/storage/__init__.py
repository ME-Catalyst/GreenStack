"""
Storage Module

Modular storage system for device profiles with specialized savers.

This module replaces the monolithic 483-line save_device() function with
a clean orchestrator pattern using single-responsibility saver classes.
"""

import logging
import sqlite3
import hashlib
from typing import Optional, List, Dict, Any

from .device import DeviceSaver
from .iodd_file import IODDFileSaver
from .parameter import ParameterSaver
from .event import EventSaver, ErrorTypeSaver
from .process_data import ProcessDataSaver
from .document import DocumentSaver, DeviceFeaturesSaver, DeviceVariantsSaver
from .communication import CommunicationSaver, WireConfigSaver
from .menu import MenuSaver
from .text import TextSaver
from .custom_datatype import CustomDatatypeSaver
from .test_config import TestConfigSaver
from .std_variable_ref import StdVariableRefSaver
from .build_format import BuildFormatSaver

logger = logging.getLogger(__name__)


class StorageManager:
    """
    Orchestrates device profile storage using specialized savers

    Replaces the monolithic save_device() function with a modular architecture
    where each saver handles a specific domain of data.
    """

    def __init__(self, db_path: str):
        """
        Initialize storage manager

        Args:
            db_path: Path to SQLite database file
        """
        self.db_path = db_path

    def save_device(self, profile) -> int:
        """
        Save complete device profile to database

        Implements smart import logic:
        - If device with same vendor_id + device_id exists, returns existing device_id
        - New assets will be merged separately via save_assets()

        Args:
            profile: DeviceProfile object with all device data

        Returns:
            int: Database ID of saved device (new or existing)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        try:
            # Initialize all savers with shared cursor
            device_saver = DeviceSaver(cursor)
            iodd_file_saver = IODDFileSaver(cursor)
            parameter_saver = ParameterSaver(cursor)
            event_saver = EventSaver(cursor)
            error_type_saver = ErrorTypeSaver(cursor)
            process_data_saver = ProcessDataSaver(cursor)
            document_saver = DocumentSaver(cursor)
            features_saver = DeviceFeaturesSaver(cursor)
            variants_saver = DeviceVariantsSaver(cursor)
            communication_saver = CommunicationSaver(cursor)
            wire_config_saver = WireConfigSaver(cursor)
            menu_saver = MenuSaver(cursor)
            text_saver = TextSaver(cursor)
            custom_datatype_saver = CustomDatatypeSaver(cursor)
            test_config_saver = TestConfigSaver(cursor)
            std_variable_ref_saver = StdVariableRefSaver(cursor)
            build_format_saver = BuildFormatSaver(cursor)

            # Save core device info (may return existing device ID)
            # The save method returns existing ID if device already exists
            device_id = device_saver.save(None, profile)

            # Check if device exists with same checksum (file unchanged)
            # If DeviceSaver found an existing device, check if the XML changed
            cursor.execute(
                "SELECT id FROM devices WHERE vendor_id = ? AND device_id = ? AND checksum = ?",
                (profile.device_info.vendor_id, profile.device_info.device_id,
                 hashlib.sha256(profile.raw_xml.encode()).hexdigest())
            )
            existing_with_same_checksum = cursor.fetchone()

            if existing_with_same_checksum:
                # Device exists with same checksum (file unchanged), skip saving data
                logger.info(f"Device {device_id} already exists with same checksum, skipping data save")
                conn.commit()  # MUST commit before closing to persist the device record
                conn.close()
                return device_id

            # Save all related data in logical order
            iodd_file_saver.save(device_id, profile)
            parameter_saver.save(device_id, getattr(profile, 'parameters', []))
            error_type_saver.save(device_id, getattr(profile, 'error_types', []))
            event_saver.save(device_id, getattr(profile, 'events', []))
            process_data_saver.save(device_id, profile)
            document_saver.save(device_id, getattr(profile, 'document_info', None))
            features_saver.save(device_id, getattr(profile, 'device_features', None))
            variants_saver.save(device_id, getattr(profile, 'device_variants', []))
            communication_saver.save(device_id, getattr(profile, 'communication_profile', None))
            wire_config_saver.save(device_id, getattr(profile, 'wire_configurations', []))
            menu_saver.save(device_id, getattr(profile, 'ui_menus', None))
            # PQA Fix #66: Pass text_redefine_ids to distinguish TextRedefine elements
            text_saver.save(device_id, getattr(profile, 'all_text_data', {}), getattr(profile, 'text_xml_order', {}), getattr(profile, 'language_order', {}), getattr(profile, 'text_redefine_ids', set()))
            custom_datatype_saver.save(device_id, getattr(profile, 'custom_datatypes', []))
            test_config_saver.save(device_id, getattr(profile, 'test_configurations', []))
            std_variable_ref_saver.save(device_id, getattr(profile, 'std_variable_refs', []))

            # Extract and save build format metadata from raw XML
            if hasattr(profile, 'raw_xml') and profile.raw_xml:
                build_format_saver.extract_and_save(device_id, profile.raw_xml)

            conn.commit()
            logger.info(f"Successfully saved device profile with ID: {device_id}")
            return device_id

        except Exception as e:
            conn.rollback()
            logger.error(f"Error saving device profile: {e}")
            raise

        finally:
            conn.close()

    def save_assets(self, device_id: int, assets: List[Dict[str, Any]]) -> None:
        """Save asset files for a device

        Smart merge logic:
        - Only adds assets that don't already exist (by file_name)
        - Prevents duplicate assets when re-importing the same device

        Args:
            device_id: The device ID to associate assets with
            assets: List of dicts with keys: file_name, file_type, file_content, file_path, image_purpose (optional)
        """
        if not assets:
            logger.debug(f"No assets to save for device {device_id}")
            return

        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        added_count = 0
        skipped_count = 0

        try:
            for asset in assets:
                # Check if asset with same file_name already exists for this device
                cursor.execute(
                    "SELECT id FROM iodd_assets WHERE device_id = ? AND file_name = ?",
                    (device_id, asset['file_name'])
                )
                existing = cursor.fetchone()

                if existing:
                    logger.debug(f"Asset '{asset['file_name']}' already exists for device {device_id}, skipping")
                    skipped_count += 1
                    continue

                # Insert new asset
                cursor.execute("""
                    INSERT INTO iodd_assets (device_id, file_name, file_type, file_content, file_path, image_purpose)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    device_id,
                    asset['file_name'],
                    asset['file_type'],
                    asset['file_content'],
                    asset['file_path'],
                    asset.get('image_purpose')  # Optional image_purpose field
                ))
                added_count += 1

            conn.commit()
            if added_count > 0:
                logger.info(f"Saved {added_count} asset file(s) for device {device_id}")
            if skipped_count > 0:
                logger.info(f"Skipped {skipped_count} duplicate asset file(s) for device {device_id}")
        except Exception as e:
            conn.rollback()
            logger.error(f"Error saving assets for device {device_id}: {e}")
            raise
        finally:
            conn.close()

    def get_assets(self, device_id: int) -> List[Dict[str, Any]]:
        """Retrieve all asset files for a device

        Returns:
            List of dicts with keys: id, file_name, file_type, file_content, file_path
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM iodd_assets WHERE device_id = ?", (device_id,))
            assets = [dict(row) for row in cursor.fetchall()]
            return assets
        finally:
            conn.close()

    def get_device(self, device_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve device information from database

        Args:
            device_id: Database ID of the device

        Returns:
            Dictionary with device info and parameters, or None if not found
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        try:
            cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
            device = cursor.fetchone()

            if device:
                # Get parameters
                cursor.execute("SELECT * FROM parameters WHERE device_id = ?", (device_id,))
                parameters = cursor.fetchall()

                result = dict(device)
                result['parameters'] = [dict(p) for p in parameters]
                return result

            return None
        finally:
            conn.close()


# Export main class and savers for external use
__all__ = [
    'StorageManager',
    'DeviceSaver',
    'IODDFileSaver',
    'ParameterSaver',
    'EventSaver',
    'ErrorTypeSaver',
    'ProcessDataSaver',
    'DocumentSaver',
    'DeviceFeaturesSaver',
    'DeviceVariantsSaver',
    'CommunicationSaver',
    'WireConfigSaver',
    'MenuSaver',
    'TextSaver',
    'CustomDatatypeSaver',
    'TestConfigSaver',
    'StdVariableRefSaver',
    'BuildFormatSaver',
]
