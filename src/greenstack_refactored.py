"""
IODD Management System - Refactored Core Implementation
========================================================
A comprehensive tool for managing IODD files and generating custom adapters

This module now imports models, parsing, and generation classes from dedicated modules.
"""

import hashlib
import json
import logging
import sqlite3
import zipfile
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

# Import from modular components
from src.models import DeviceProfile
from src.parsing import IODDParser
from src.generation import AdapterGenerator, NodeREDGenerator

# Import modular storage system
from src.storage import StorageManager as ModularStorageManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# IODD Ingester
# ============================================================================

class IODDIngester:
    """Ingest and process IODD files and packages"""

    def __init__(self, storage_path: Path = Path("./iodd_storage")):
        self.storage_path = storage_path
        self.storage_path.mkdir(exist_ok=True)
        self.asset_files = []  # Store asset files during ingestion

    def ingest_file(self, file_path: Union[str, Path], _depth: int = 0) -> Tuple[DeviceProfile, List[Dict[str, Any]]]:
        """Ingest a single IODD file or package

        Args:
            file_path: Path to the IODD file or package
            _depth: Internal parameter to track nesting depth (0 = root level)

        Returns:
            Tuple of (DeviceProfile, list of asset files)
            Asset files are dicts with keys: file_name, file_type, file_content, file_path
        """
        file_path = Path(file_path)
        logger.info(f"Ingesting IODD file: {file_path}")
        self.asset_files = []  # Reset asset files

        if file_path.suffix.lower() in ['.iodd', '.zip']:
            # Check if this is a nested ZIP (only at root level)
            if _depth == 0 and self._is_nested_zip(file_path):
                # This is a nested ZIP containing multiple device packages
                # Return None to signal the caller to handle it differently
                return None, []
            return self._ingest_package(file_path)
        elif file_path.suffix.lower() == '.xml':
            return self._ingest_xml(file_path)
        else:
            raise ValueError(f"Unsupported file type: {file_path.suffix}")

    def _is_nested_zip(self, zip_path: Path) -> bool:
        """Check if a ZIP file contains other ZIP files (nested structure)

        Args:
            zip_path: Path to the ZIP file to check

        Returns:
            True if ZIP contains other ZIP files, False otherwise
        """
        try:
            with zipfile.ZipFile(zip_path, 'r') as zip_file:
                file_list = zip_file.namelist()

                # Check if there are any .zip files
                zip_files = [f for f in file_list if f.lower().endswith('.zip') and not f.startswith('__MACOSX/')]

                # Check if there are any XML files at root level
                xml_files = [f for f in file_list if f.lower().endswith('.xml') and '/' not in f]

                # It's a nested ZIP if it has ZIP files but no XML files at root
                # (if it has both, treat it as a regular package with the XML taking priority)
                return len(zip_files) > 0 and len(xml_files) == 0
        except Exception as e:
            logger.warning(f"Error checking if ZIP is nested: {e}")
            return False

    def ingest_nested_package(self, package_path: Path) -> List[Tuple[DeviceProfile, List[Dict[str, Any]]]]:
        """Ingest a nested IODD package containing multiple device packages

        Args:
            package_path: Path to the parent ZIP file

        Returns:
            List of tuples, each containing (DeviceProfile, list of asset files)
        """
        logger.info(f"Processing nested ZIP package: {package_path}")
        results = []

        with zipfile.ZipFile(package_path, 'r') as parent_zip:
            # Find all ZIP files in the parent package
            zip_files = [f for f in parent_zip.namelist()
                        if f.lower().endswith('.zip') and not f.startswith('__MACOSX/')]

            if not zip_files:
                raise ValueError("No child ZIP files found in nested package")

            logger.info(f"Found {len(zip_files)} child package(s) in nested ZIP")

            # Process each child ZIP
            import os
            import tempfile

            for zip_file_name in zip_files:
                try:
                    logger.info(f"Processing child package: {zip_file_name}")

                    # Extract child ZIP to temporary file
                    child_zip_data = parent_zip.read(zip_file_name)

                    # Create temporary file for the child ZIP
                    with tempfile.NamedTemporaryFile(suffix='.zip', delete=False) as tmp_file:
                        tmp_file.write(child_zip_data)
                        tmp_zip_path = tmp_file.name

                    try:
                        # Process the child ZIP at depth 1 (prevent further nesting)
                        profile, assets = self.ingest_file(Path(tmp_zip_path), _depth=1)

                        if profile:  # Only add if successfully parsed
                            results.append((profile, assets))
                            logger.info(f"Successfully processed {zip_file_name}: {profile.device_info.product_name}")
                        else:
                            logger.warning(f"Skipped {zip_file_name}: could not parse device profile")

                    finally:
                        # Clean up temporary file
                        try:
                            os.unlink(tmp_zip_path)
                        except:
                            pass

                except Exception as e:
                    logger.error(f"Error processing child package {zip_file_name}: {e}")
                    # Continue with next package instead of failing entirely
                    continue

        if not results:
            raise ValueError("No valid device packages found in nested ZIP")

        logger.info(f"Successfully processed {len(results)} device(s) from nested package")
        return results

    def _ingest_package(self, package_path: Path) -> Tuple[DeviceProfile, List[Dict[str, Any]]]:
        """Ingest IODD package (zip file)

        Returns:
            Tuple of (DeviceProfile, list of asset files)
        """
        asset_files = []

        with zipfile.ZipFile(package_path, 'r') as zip_file:
            # Find main IODD XML file
            xml_files = [f for f in zip_file.namelist() if f.endswith('.xml')]
            if not xml_files:
                raise ValueError("No XML files found in IODD package")

            # Extract and parse main XML
            main_xml = xml_files[0]  # Assuming first XML is main IODD
            xml_content = zip_file.read(main_xml).decode('utf-8')

            # Store all files from the package
            for file_info in zip_file.filelist:
                if file_info.is_dir():
                    continue

                file_name = file_info.filename
                file_content = zip_file.read(file_name)

                # Determine file type
                file_ext = Path(file_name).suffix.lower()
                if file_ext in ['.png', '.jpg', '.jpeg', '.gif', '.svg']:
                    file_type = 'image'
                elif file_ext == '.xml':
                    file_type = 'xml'
                else:
                    file_type = 'other'

                # Detect image purpose from filename
                # Standard IODD naming conventions:
                # *logo.png = manufacturer logo
                # *icon.png = low res thumbnail
                # *pic.png = full res device image (symbol-pic, etc.)
                # *con-pic.png = connection pinout
                image_purpose = None
                if file_type == 'image':
                    file_name_lower = Path(file_name).stem.lower()
                    # Check for specific suffixes (most specific patterns first)
                    if file_name_lower.endswith('logo'):
                        image_purpose = 'logo'
                    elif file_name_lower.endswith('con-pic') or 'connection' in file_name_lower:
                        image_purpose = 'connection'
                    elif file_name_lower.endswith('symbol-pic') or (file_name_lower.endswith('-pic') and not file_name_lower.endswith('con-pic')):
                        # Full resolution device images end with -pic (symbol-pic, device-pic, etc.)
                        image_purpose = 'device-pic'
                    elif 'icon' in file_name_lower:
                        # Thumbnails contain icon
                        image_purpose = 'icon'

                asset_files.append({
                    'file_name': file_name,
                    'file_type': file_type,
                    'file_content': file_content,
                    'file_path': file_name,
                    'image_purpose': image_purpose
                })

                logger.debug(f"Extracted asset: {file_name} ({file_type})")

            # NOTE: Filesystem extraction removed - assets now stored as BLOBs in database
            # No need to persist extracted files to iodd_storage directory
            # The zipfile is opened in memory and assets are read directly from it

        profile = self._parse_xml_content(xml_content)
        return profile, asset_files

    def _ingest_xml(self, xml_path: Path) -> Tuple[DeviceProfile, List[Dict[str, Any]]]:
        """Ingest standalone IODD XML file

        Returns:
            Tuple of (DeviceProfile, empty list since no assets)
        """
        with open(xml_path, 'r', encoding='utf-8') as f:
            xml_content = f.read()

        # For standalone XML, also store it as an asset
        with open(xml_path, 'rb') as f:
            file_content = f.read()

        asset_files = [{
            'file_name': xml_path.name,
            'file_type': 'xml',
            'file_content': file_content,
            'file_path': xml_path.name
        }]

        profile = self._parse_xml_content(xml_content)
        return profile, asset_files

    def _parse_xml_content(self, xml_content: str) -> DeviceProfile:
        """Parse XML content into DeviceProfile"""
        parser = IODDParser(xml_content)
        return parser.parse()

    def calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content"""
        return hashlib.sha256(content.encode()).hexdigest()

# ============================================================================
# Storage Manager (Legacy - kept for backward compatibility)
# ============================================================================

# NOTE: The old StorageManager class from the original greenstack.py is kept here
# for backward compatibility. New code should use src.storage.StorageManager instead.
# This class will be deprecated in a future version.

# Placeholder for the legacy StorageManager - we'll keep this import to redirect
# to the legacy implementation in greenstack.py.backup if needed
StorageManager = None  # This can be populated with the full legacy class if needed

# ============================================================================
# Main Greenstack Manager
# ============================================================================

class IODDManager:
    """Main IODD management system"""

    def __init__(self, storage_path: str = "./iodd_storage", db_path: str = "greenstack.db"):
        self.ingester = IODDIngester(Path(storage_path))
        # Use ModularStorageManager or legacy StorageManager based on what's available
        # For now, we'll need to import the legacy StorageManager separately if used
        # self.storage = StorageManager(db_path)  # Legacy
        # OR use the modular storage:
        # self.storage = ModularStorageManager(db_path)  # New modular system

        self.generators = {
            'node-red': NodeREDGenerator()
        }

    def import_iodd(self, file_path: str) -> Union[int, List[int]]:
        """Import an IODD file or package

        Returns:
            int: device_id for single device import
            List[int]: list of device_ids for nested ZIP import
        """
        # Try to ingest as single file first
        profile, assets = self.ingester.ingest_file(file_path)

        # Check if this is a nested ZIP (profile will be None)
        if profile is None:
            logger.info("Detected nested ZIP package, processing multiple devices...")
            device_packages = self.ingester.ingest_nested_package(Path(file_path))

            device_ids = []
            for pkg_profile, pkg_assets in device_packages:
                device_id = self.storage.save_device(pkg_profile)
                self.storage.save_assets(device_id, pkg_assets)
                device_ids.append(device_id)
                logger.info(f"Successfully imported IODD for {pkg_profile.device_info.product_name} with {len(pkg_assets)} asset file(s)")

            logger.info(f"Nested ZIP import complete: {len(device_ids)} device(s) imported")
            return device_ids
        else:
            # Single device import
            device_id = self.storage.save_device(profile)
            self.storage.save_assets(device_id, assets)
            logger.info(f"Successfully imported IODD for {profile.device_info.product_name} with {len(assets)} asset file(s)")
            return device_id

    def generate_adapter(self, device_id: int, platform: str, output_path: str = "./generated"):
        """Generate adapter for a specific platform"""
        # Get device from storage
        device_data = self.storage.get_device(device_id)
        if not device_data:
            raise ValueError(f"Device with ID {device_id} not found")

        # Get generator
        if platform not in self.generators:
            raise ValueError(f"Platform {platform} not supported")

        generator = self.generators[platform]

        # For now, we need to reconstruct the profile (in a real system, we'd store it properly)
        # This is a simplified version - you'd want to properly deserialize from the database
        logger.info(f"Generating {platform} adapter for device {device_id}")

        # Create output directory
        output_dir = Path(output_path) / platform / f"device_{device_id}"
        output_dir.mkdir(parents=True, exist_ok=True)

        # Generate files (this would use the actual profile in a complete implementation)
        # For demonstration, we'll create a basic structure
        files = {
            'package.json': json.dumps({
                "name": f"node-red-contrib-device-{device_id}",
                "version": "1.0.0",
                "description": f"Generated node for device {device_id}"
            }, indent=2),
            'README.md': f"# Device {device_id}\n\nGenerated Node-RED adapter"
        }

        # Save generated files
        for filename, content in files.items():
            file_path = output_dir / filename
            with open(file_path, 'w') as f:
                f.write(content)

        logger.info(f"Generated adapter files in {output_dir}")
        return str(output_dir)

    def list_devices(self) -> List[Dict[str, Any]]:
        """List all imported devices"""
        conn = sqlite3.connect(self.storage.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM devices ORDER BY import_date DESC")
        devices = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return devices

# ============================================================================
# CLI Interface
# ============================================================================

def main():
    """Command-line interface for Greenstack"""
    import argparse

    parser = argparse.ArgumentParser(description='IODD Management System')
    subparsers = parser.add_subparsers(dest='command', help='Commands')

    # Import command
    import_parser = subparsers.add_parser('import', help='Import IODD file')
    import_parser.add_argument('file', help='Path to IODD file or package')

    # Generate command
    generate_parser = subparsers.add_parser('generate', help='Generate adapter')
    generate_parser.add_argument('device_id', type=int, help='Device ID')
    generate_parser.add_argument('--platform', default='node-red',
                                help='Target platform (default: node-red)')
    generate_parser.add_argument('--output', default='./generated',
                                help='Output directory')

    # List command
    list_parser = subparsers.add_parser('list', help='List imported devices')

    args = parser.parse_args()

    # Initialize manager
    manager = IODDManager()

    if args.command == 'import':
        try:
            device_id = manager.import_iodd(args.file)
            logger.info("Successfully imported device with ID: %d", device_id)
        except Exception as e:
            logger.error("Error importing IODD: %s", e)

    elif args.command == 'generate':
        try:
            output_dir = manager.generate_adapter(args.device_id, args.platform, args.output)
            logger.info("Generated adapter in: %s", output_dir)
        except Exception as e:
            logger.error("Error generating adapter: %s", e)

    elif args.command == 'list':
        devices = manager.list_devices()
        if devices:
            logger.info("\nImported Devices:")
            logger.info("-" * 80)
            for device in devices:
                logger.info("ID: %d | %s | Vendor: %s | Imported: %s",
                           device['id'], device['product_name'],
                           device['manufacturer'], device['import_date'])
        else:
            logger.info("No devices imported yet")

    else:
        parser.print_help()

if __name__ == "__main__":
    main()
