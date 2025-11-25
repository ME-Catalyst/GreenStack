"""
IODD Management System - Core Implementation
============================================
A comprehensive tool for managing IODD files and generating custom adapters

NOTE: This module has been refactored. Data models, parsing, and generation
classes are now in dedicated modules (src/models, src/parsing, src/generation).
This file maintains backward compatibility by re-exporting those classes.
"""

import hashlib
import json
import logging
import sqlite3
import xml.etree.ElementTree as ET
import zipfile
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from datetime import datetime
from enum import Enum
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union

from jinja2 import Environment, FileSystemLoader, Template

# ============================================================================
# Re-export from Modular Components (for backward compatibility)
# ============================================================================

# Re-export all models from src.models
from src.models import (
    AccessRights,
    CommunicationProfile,
    Constraint,
    CustomDatatype,
    DeviceFeatures,
    DeviceInfo,
    DeviceProfile,
    DeviceTestConfig,
    DeviceVariant,
    DocumentInfo,
    ErrorType,
    Event,
    IODDDataType,
    Menu,
    MenuButton,
    MenuItem,
    Parameter,
    ProcessData,
    ProcessDataCollection,
    ProcessDataCondition,
    ProcessDataUIInfo,
    RecordItem,
    SingleValue,
    TestEventTrigger,
    UserInterfaceMenus,
    VendorInfo,
    WireConfiguration,
)

# Re-export parser from src.parsing
from src.parsing import IODDParser

# Re-export generators from src.generation
from src.generation import AdapterGenerator, NodeREDGenerator

# Import modular storage system
from src.storage import StorageManager as ModularStorageManager

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# ============================================================================
# Data Models
# ============================================================================

class IODDDataType(Enum):
    """IODD standard data types"""
    BOOLEAN = "BooleanT"
    INTEGER = "IntegerT"
    UNSIGNED_INTEGER = "UIntegerT"
    FLOAT = "Float32T"
    STRING = "StringT"
    OCTET_STRING = "OctetStringT"
    TIME = "TimeT"
    RECORD = "RecordT"
    ARRAY = "ArrayT"

class AccessRights(Enum):
    """Parameter access rights"""
    READ_ONLY = "ro"
    WRITE_ONLY = "wo"
    READ_WRITE = "rw"

@dataclass
class VendorInfo:
    """Vendor information from IODD"""
    id: int
    name: str
    text: str
    url: Optional[str] = None

@dataclass
class DeviceInfo:
    """Device identification information"""
    vendor_id: int
    device_id: int
    product_name: str
    product_id: Optional[str] = None
    product_text: Optional[str] = None
    hardware_revision: Optional[str] = None
    firmware_revision: Optional[str] = None
    software_revision: Optional[str] = None

@dataclass
class Constraint:
    """Parameter constraint definition"""
    type: str  # min, max, enum
    value: Any

@dataclass
class Parameter:
    """Device parameter definition"""
    id: str
    index: int
    subindex: Optional[int]
    name: str
    data_type: IODDDataType
    access_rights: AccessRights
    default_value: Optional[Any] = None
    min_value: Optional[Any] = None
    max_value: Optional[Any] = None
    unit: Optional[str] = None
    description: Optional[str] = None
    constraints: List[Constraint] = field(default_factory=list)
    enumeration_values: Dict[str, str] = field(default_factory=dict)  # value -> label mapping
    bit_length: Optional[int] = None
    dynamic: bool = False
    excluded_from_data_storage: bool = False
    modifies_other_variables: bool = False
    unit_code: Optional[str] = None
    value_range_name: Optional[str] = None
    single_values: List[SingleValue] = field(default_factory=list)

@dataclass
class RecordItem:
    """Record item within process data"""
    subindex: int
    name: str
    bit_offset: int
    bit_length: int
    data_type: str
    default_value: Optional[str] = None
    single_values: List['SingleValue'] = field(default_factory=list)

@dataclass
class ProcessData:
    """Process data definition"""
    id: str
    name: str
    bit_length: int
    data_type: str
    record_items: List[RecordItem] = field(default_factory=list)
    description: Optional[str] = None
    # Phase 2: Conditional process data
    condition: Optional['ProcessDataCondition'] = None

@dataclass
class ProcessDataCollection:
    """Collection of process data inputs and outputs"""
    inputs: List[ProcessData] = field(default_factory=list)
    outputs: List[ProcessData] = field(default_factory=list)
    total_input_bits: int = 0
    total_output_bits: int = 0

@dataclass
class ErrorType:
    """Device error type definition"""
    code: int
    additional_code: int
    name: Optional[str] = None
    description: Optional[str] = None

@dataclass
class Event:
    """Device event definition"""
    code: int
    name: Optional[str] = None
    description: Optional[str] = None
    event_type: Optional[str] = None  # Notification, Warning, Error

@dataclass
class DocumentInfo:
    """IODD document metadata"""
    copyright: Optional[str] = None
    release_date: Optional[str] = None
    version: Optional[str] = None

@dataclass
class DeviceFeatures:
    """Device capabilities and features"""
    block_parameter: bool = False
    data_storage: bool = False
    profile_characteristic: Optional[str] = None
    access_locks_data_storage: bool = False
    access_locks_local_parameterization: bool = False
    access_locks_local_user_interface: bool = False
    access_locks_parameter: bool = False

@dataclass
class CommunicationProfile:
    """IO-Link communication network profile"""
    iolink_revision: Optional[str] = None
    compatible_with: Optional[str] = None
    bitrate: Optional[str] = None
    min_cycle_time: Optional[int] = None  # microseconds
    msequence_capability: Optional[int] = None
    sio_supported: bool = False
    connection_type: Optional[str] = None
    wire_config: Dict[str, str] = field(default_factory=dict)

@dataclass
class MenuItem:
    """User interface menu item reference"""
    variable_id: Optional[str] = None
    record_item_ref: Optional[str] = None
    subindex: Optional[int] = None
    access_right_restriction: Optional[str] = None
    display_format: Optional[str] = None
    unit_code: Optional[str] = None
    button_value: Optional[str] = None
    menu_ref: Optional[str] = None
    # Phase 1: UI rendering metadata
    gradient: Optional[float] = None
    offset: Optional[float] = None
    # Phase 3: Button configuration
    buttons: List['MenuButton'] = field(default_factory=list)

@dataclass
class Menu:
    """User interface menu definition"""
    id: str
    name: str
    items: List[MenuItem] = field(default_factory=list)
    sub_menus: List[str] = field(default_factory=list)

@dataclass
class UserInterfaceMenus:
    """Complete user interface menu structure"""
    menus: List[Menu] = field(default_factory=list)
    observer_role_menus: Dict[str, str] = field(default_factory=dict)
    maintenance_role_menus: Dict[str, str] = field(default_factory=dict)
    specialist_role_menus: Dict[str, str] = field(default_factory=dict)

@dataclass
class SingleValue:
    """Single value enumeration for parameters/process data"""
    value: str
    name: str
    description: Optional[str] = None

@dataclass
class ProcessDataUIInfo:
    """UI rendering metadata for process data record items"""
    process_data_id: str
    subindex: int
    gradient: Optional[float] = None
    offset: Optional[float] = None
    unit_code: Optional[str] = None
    display_format: Optional[str] = None

@dataclass
class DeviceVariant:
    """Device variant information"""
    product_id: str
    device_symbol: Optional[str] = None
    device_icon: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None

@dataclass
class ProcessDataCondition:
    """Conditional process data definition"""
    variable_id: str
    value: str

@dataclass
class MenuButton:
    """UI menu button configuration"""
    button_value: str
    description: Optional[str] = None
    action_started_message: Optional[str] = None

@dataclass
class WireConfiguration:
    """Wire connection configuration"""
    connection_type: str
    wire_number: int
    wire_color: Optional[str] = None
    wire_function: Optional[str] = None
    wire_description: Optional[str] = None

@dataclass
class TestEventTrigger:
    """Test event trigger configuration"""
    appear_value: str
    disappear_value: str

@dataclass
class DeviceTestConfig:
    """Device test configuration"""
    config_type: str
    param_index: int
    test_value: str
    event_triggers: List[TestEventTrigger] = field(default_factory=list)

@dataclass
class CustomDatatype:
    """Custom datatype definition"""
    datatype_id: str
    datatype_xsi_type: str
    bit_length: Optional[int] = None
    subindex_access_supported: bool = False
    single_values: List[SingleValue] = field(default_factory=list)
    record_items: List[RecordItem] = field(default_factory=list)

@dataclass
class DeviceProfile:
    """Complete device profile from IODD"""
    vendor_info: VendorInfo
    device_info: DeviceInfo
    parameters: List[Parameter]
    process_data: ProcessDataCollection
    error_types: List[ErrorType] = field(default_factory=list)
    events: List[Event] = field(default_factory=list)
    document_info: Optional[DocumentInfo] = None
    device_features: Optional[DeviceFeatures] = None
    communication_profile: Optional[CommunicationProfile] = None
    ui_menus: Optional[UserInterfaceMenus] = None
    iodd_version: str = ""
    schema_version: str = ""
    import_date: datetime = field(default_factory=datetime.now)
    raw_xml: Optional[str] = None
    all_text_data: Dict[str, Dict[str, str]] = field(default_factory=dict)  # Multi-language text data

    # Phase 1: UI Rendering metadata
    process_data_ui_info: List[ProcessDataUIInfo] = field(default_factory=list)
    menu_item_ui_attrs: Dict[str, Dict[str, Any]] = field(default_factory=dict)  # Store gradient/offset for menu items

    # Phase 2: Device Variants and Conditions
    device_variants: List[DeviceVariant] = field(default_factory=list)
    process_data_conditions: Dict[str, ProcessDataCondition] = field(default_factory=dict)  # pd_id -> condition

    # Phase 3: Button Configurations
    menu_buttons: Dict[str, List[MenuButton]] = field(default_factory=dict)  # menu_item_id -> buttons

    # Phase 4: Wiring and Testing
    wire_configurations: List[WireConfiguration] = field(default_factory=list)
    test_configurations: List[DeviceTestConfig] = field(default_factory=list)

    # Phase 5: Custom Datatypes
    custom_datatypes: List[CustomDatatype] = field(default_factory=list)
    vendor_logo_filename: Optional[str] = None
    stamp_crc: Optional[str] = None
    checker_name: Optional[str] = None
    checker_version: Optional[str] = None

# ============================================================================
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
        """Parse XML content into DeviceProfile

        Uses the enhanced IODDParser from src.parsing which handles:
        - Proper NULL handling for boolean attributes (dynamic, excludedFromDataStorage, etc.)
        - name_text_id and description_text_id extraction
        - StdVariableRef storage
        - All other PQA improvements
        """
        # IODDParser is imported from src.parsing at the top of this file
        parser = IODDParser(xml_content)
        return parser.parse()
    
    def calculate_checksum(self, content: str) -> str:
        """Calculate SHA256 checksum of content"""
        return hashlib.sha256(content.encode()).hexdigest()

# ============================================================================
# Storage Manager
# ============================================================================

class StorageManager:
    """Manage IODD data storage in SQLite database"""
    
    def __init__(self, db_path: str = "greenstack.db"):
        self.db_path = db_path
        self._init_database()
    
    def _init_database(self):
        """Initialize database schema"""
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Enable WAL mode for better concurrent write performance
        cursor.execute("PRAGMA journal_mode=WAL")
        cursor.execute("PRAGMA synchronous=NORMAL")  # Faster writes, still safe with WAL
        cursor.execute("PRAGMA cache_size=-64000")   # 64MB cache for better performance
        cursor.execute("PRAGMA temp_store=MEMORY")   # Use memory for temp tables

        # Create tables
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS devices (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                vendor_id INTEGER,
                device_id INTEGER,
                product_name TEXT,
                manufacturer TEXT,
                iodd_version TEXT,
                import_date TIMESTAMP,
                checksum TEXT UNIQUE,
                vendor_logo_filename TEXT
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iodd_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                file_name TEXT,
                xml_content TEXT,
                schema_version TEXT,
                stamp_crc TEXT,
                checker_name TEXT,
                checker_version TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iodd_text (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                text_id TEXT,
                language_code TEXT,
                text_value TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                param_index INTEGER,
                name TEXT,
                data_type TEXT,
                access_rights TEXT,
                default_value TEXT,
                min_value TEXT,
                max_value TEXT,
                unit TEXT,
                description TEXT,
                enumeration_values TEXT,
                bit_length INTEGER,
                dynamic INTEGER,
                excluded_from_data_storage INTEGER,
                modifies_other_variables INTEGER,
                unit_code TEXT,
                value_range_name TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS generated_adapters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                target_platform TEXT,
                version TEXT,
                generated_date TIMESTAMP,
                code_content TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS iodd_assets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                file_name TEXT,
                file_type TEXT,
                file_content BLOB,
                file_path TEXT,
                image_purpose TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS error_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                code INTEGER,
                additional_code INTEGER,
                name TEXT,
                description TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                code INTEGER,
                name TEXT,
                description TEXT,
                event_type TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                pd_id TEXT,
                name TEXT,
                direction TEXT,
                bit_length INTEGER,
                data_type TEXT,
                description TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_data_record_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_data_id INTEGER,
                subindex INTEGER,
                name TEXT,
                bit_offset INTEGER,
                bit_length INTEGER,
                data_type TEXT,
                default_value TEXT,
                FOREIGN KEY (process_data_id) REFERENCES process_data (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_data_single_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                record_item_id INTEGER,
                value TEXT,
                name TEXT,
                description TEXT,
                FOREIGN KEY (record_item_id) REFERENCES process_data_record_items (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS document_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                copyright TEXT,
                release_date TEXT,
                version TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_features (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                block_parameter INTEGER,
                data_storage INTEGER,
                profile_characteristic TEXT,
                access_locks_data_storage INTEGER,
                access_locks_local_parameterization INTEGER,
                access_locks_local_user_interface INTEGER,
                access_locks_parameter INTEGER,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS communication_profile (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                iolink_revision TEXT,
                compatible_with TEXT,
                bitrate TEXT,
                min_cycle_time TEXT,
                msequence_capability TEXT,
                sio_supported INTEGER,
                connection_type TEXT,
                wire_config TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ui_menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                menu_id TEXT,
                name TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ui_menu_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER,
                variable_id TEXT,
                record_item_ref TEXT,
                subindex INTEGER,
                access_right_restriction TEXT,
                display_format TEXT,
                unit_code TEXT,
                button_value TEXT,
                menu_ref TEXT,
                item_order INTEGER,
                gradient TEXT,
                offset TEXT,
                FOREIGN KEY (menu_id) REFERENCES ui_menus (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ui_menu_roles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                role_type TEXT,
                menu_type TEXT,
                menu_id TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        # Custom Datatypes
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_datatypes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                datatype_id TEXT,
                datatype_xsi_type TEXT,
                bit_length INTEGER,
                subindex_access_supported INTEGER,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_datatype_single_values (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datatype_id INTEGER,
                value TEXT,
                name TEXT,
                FOREIGN KEY (datatype_id) REFERENCES custom_datatypes (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS custom_datatype_record_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                datatype_id INTEGER,
                subindex INTEGER,
                bit_offset INTEGER,
                bit_length INTEGER,
                datatype_ref TEXT,
                name TEXT,
                FOREIGN KEY (datatype_id) REFERENCES custom_datatypes (id)
            )
        """)

        # Device Test Configuration
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_test_config (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                config_type TEXT,
                param_index INTEGER,
                test_value TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_test_event_triggers (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                test_config_id INTEGER,
                appear_value TEXT,
                disappear_value TEXT,
                FOREIGN KEY (test_config_id) REFERENCES device_test_config (id)
            )
        """)

        # Process Data Extensions
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_data_conditions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_data_id INTEGER,
                condition_variable_id TEXT,
                condition_value TEXT,
                FOREIGN KEY (process_data_id) REFERENCES process_data (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS process_data_ui_info (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_data_id INTEGER,
                subindex INTEGER,
                gradient TEXT,
                offset TEXT,
                unit_code TEXT,
                display_format TEXT,
                FOREIGN KEY (process_data_id) REFERENCES process_data (id)
            )
        """)

        # Wire Configurations
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS wire_configurations (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                connection_type TEXT,
                wire_number INTEGER,
                wire_color TEXT,
                wire_function TEXT,
                wire_description TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        # Device Variants
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS device_variants (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                product_id TEXT,
                device_symbol TEXT,
                device_icon TEXT,
                name TEXT,
                description TEXT,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
        """)

        # UI Menu Buttons
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS ui_menu_buttons (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_item_id INTEGER,
                button_value TEXT,
                description TEXT,
                action_started_message TEXT,
                FOREIGN KEY (menu_item_id) REFERENCES ui_menu_items (id)
            )
        """)

        # ========================================================================
        # EDS (EtherNet/IP) Tables
        # ========================================================================

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER,
                vendor_code INTEGER,
                vendor_name TEXT,
                product_code INTEGER,
                product_type INTEGER,
                product_type_str TEXT,
                product_name TEXT,
                catalog_number TEXT,
                major_revision INTEGER,
                minor_revision INTEGER,
                description TEXT,
                icon_filename TEXT,
                icon_data BLOB,
                eds_content TEXT,
                home_url TEXT,
                import_date TIMESTAMP,
                file_checksum TEXT UNIQUE,
                create_date TEXT,
                create_time TEXT,
                mod_date TEXT,
                mod_time TEXT,
                file_revision TEXT,
                class1 TEXT,
                class2 TEXT,
                class3 TEXT,
                class4 TEXT,
                diagnostic_info_count INTEGER DEFAULT 0,
                diagnostic_warn_count INTEGER DEFAULT 0,
                diagnostic_error_count INTEGER DEFAULT 0,
                diagnostic_fatal_count INTEGER DEFAULT 0,
                has_parsing_issues INTEGER DEFAULT 0,
                variant_type TEXT,
                version_folder TEXT,
                is_latest_version INTEGER DEFAULT 0,
                file_path_in_package TEXT,
                FOREIGN KEY (package_id) REFERENCES eds_packages (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_name TEXT,
                package_checksum TEXT UNIQUE,
                upload_date TIMESTAMP,
                readme_content TEXT,
                total_eds_files INTEGER,
                total_versions INTEGER,
                vendor_name TEXT,
                product_name TEXT
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_package_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER,
                eds_file_id INTEGER,
                FOREIGN KEY (package_id) REFERENCES eds_packages (id),
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_package_metadata (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER,
                file_path TEXT,
                file_type TEXT,
                content TEXT,
                FOREIGN KEY (package_id) REFERENCES eds_packages (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_parameters (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                param_number INTEGER,
                param_name TEXT,
                data_type TEXT,
                data_size INTEGER,
                default_value TEXT,
                min_value TEXT,
                max_value TEXT,
                description TEXT,
                link_path_size INTEGER,
                link_path TEXT,
                descriptor TEXT,
                help_string_1 TEXT,
                help_string_2 TEXT,
                help_string_3 TEXT,
                enum_values TEXT,
                units TEXT,
                scaling_multiplier TEXT,
                scaling_divisor TEXT,
                scaling_base TEXT,
                scaling_offset TEXT,
                link_scaling_multiplier TEXT,
                link_scaling_divisor TEXT,
                link_scaling_base TEXT,
                link_scaling_offset TEXT,
                decimal_places INTEGER,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_connections (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                connection_number INTEGER,
                connection_name TEXT,
                trigger_transport TEXT,
                connection_params TEXT,
                output_assembly TEXT,
                input_assembly TEXT,
                help_string TEXT,
                o_to_t_params TEXT,
                t_to_o_params TEXT,
                config_part1 TEXT,
                config_part2 TEXT,
                path TEXT,
                trigger_transport_comment TEXT,
                connection_params_comment TEXT,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_diagnostics (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                severity TEXT,
                code TEXT,
                message TEXT,
                section TEXT,
                line INTEGER,
                column INTEGER,
                context TEXT,
                created_at TIMESTAMP,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS tickets (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                ticket_number TEXT UNIQUE,
                device_type TEXT,
                device_id INTEGER,
                device_name TEXT,
                vendor_name TEXT,
                product_code INTEGER,
                title TEXT,
                description TEXT,
                eds_reference TEXT,
                status TEXT,
                priority TEXT,
                category TEXT,
                created_at TIMESTAMP,
                updated_at TIMESTAMP
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_assemblies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                assembly_number INTEGER,
                assembly_name TEXT,
                assembly_type TEXT,
                unknown_field1 TEXT,
                size INTEGER,
                unknown_field2 TEXT,
                path TEXT,
                help_string TEXT,
                is_variable INTEGER,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_variable_assemblies (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                assembly_name TEXT,
                assembly_number INTEGER,
                unknown_value1 TEXT,
                max_size INTEGER,
                description TEXT,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_ports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                port_number INTEGER,
                port_type TEXT,
                port_name TEXT,
                port_path TEXT,
                link_number INTEGER,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_modules (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                module_number INTEGER,
                module_name TEXT,
                device_type TEXT,
                catalog_number TEXT,
                major_revision INTEGER,
                minor_revision INTEGER,
                config_size INTEGER,
                config_data TEXT,
                input_size INTEGER,
                output_size INTEGER,
                module_description TEXT,
                slot_number INTEGER,
                module_class TEXT,
                vendor_code INTEGER,
                product_code INTEGER,
                raw_definition TEXT,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_groups (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                group_number INTEGER,
                group_name TEXT,
                parameter_count INTEGER,
                parameter_list TEXT,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_capacity (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                max_msg_connections INTEGER,
                max_io_producers INTEGER,
                max_io_consumers INTEGER,
                max_cx_per_config_tool INTEGER,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS eds_tspecs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                eds_file_id INTEGER,
                tspec_name TEXT,
                direction TEXT,
                data_size INTEGER,
                rate TEXT,
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
        """)

        conn.commit()
        conn.close()
    
    def save_device(self, profile: DeviceProfile) -> int:
        """Save device profile to database using modular storage system

        Smart import logic:
        - If device with same vendor_id + device_id exists, return existing device_id
        - New assets will be merged in save_assets() method
        """
        # Use modular storage manager for clean, maintainable code
        modular_storage = ModularStorageManager(self.db_path)
        device_id = modular_storage.save_device(profile)
        return device_id

    def save_device_old(self, profile: DeviceProfile) -> int:
        """OLD IMPLEMENTATION - Kept for reference during migration

        This 483-line monolithic function has been replaced by the modular
        storage system in src/storage/. Delete this method after confirming
        the new system works correctly.
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        # Calculate checksum
        checksum = hashlib.sha256(profile.raw_xml.encode()).hexdigest()

        # Check if device already exists by vendor_id and device_id
        cursor.execute(
            "SELECT id FROM devices WHERE vendor_id = ? AND device_id = ?",
            (profile.device_info.vendor_id, profile.device_info.device_id)
        )
        existing = cursor.fetchone()
        if existing:
            logger.info(f"Device already exists with ID: {existing[0]} (vendor_id={profile.device_info.vendor_id}, device_id={profile.device_info.device_id}). Will merge new assets.")
            conn.close()
            return existing[0]

        # Insert device
        cursor.execute("""
            INSERT INTO devices (vendor_id, device_id, product_name,
                               manufacturer, iodd_version, import_date, checksum)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (
            profile.device_info.vendor_id,
            profile.device_info.device_id,
            profile.device_info.product_name,
            profile.vendor_info.name,
            profile.iodd_version,
            profile.import_date,
            checksum
        ))

        device_id = cursor.lastrowid
        
        # Save IODD file content
        cursor.execute("""
            INSERT INTO iodd_files (device_id, file_name, xml_content, schema_version)
            VALUES (?, ?, ?, ?)
        """, (
            device_id,
            f"{profile.device_info.product_name}.xml",
            profile.raw_xml,
            profile.schema_version
        ))
        
        # Save parameters
        for param in profile.parameters:
            # Serialize enumeration values as JSON
            import json
            enum_json = json.dumps(param.enumeration_values) if param.enumeration_values else None

            cursor.execute("""
                INSERT INTO parameters (device_id, param_index, name, data_type,
                                      access_rights, default_value, min_value,
                                      max_value, unit, description, enumeration_values, bit_length,
                                      dynamic, excluded_from_data_storage, modifies_other_variables,
                                      unit_code, value_range_name, variable_id)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                device_id,
                param.index,
                param.name,
                param.data_type.value,
                param.access_rights.value,
                str(param.default_value) if param.default_value else None,
                str(param.min_value) if param.min_value else None,
                str(param.max_value) if param.max_value else None,
                param.unit,
                param.description,
                enum_json,
                param.bit_length,
                1 if param.dynamic else 0,
                1 if param.excluded_from_data_storage else 0,
                1 if param.modifies_other_variables else 0,
                param.unit_code,
                param.value_range_name,
                param.id  # Store the original IODD Variable ID
            ))

        # Save error types
        for error in profile.error_types:
            cursor.execute("""
                INSERT INTO error_types (device_id, code, additional_code, name, description)
                VALUES (?, ?, ?, ?, ?)
            """, (
                device_id,
                error.code,
                error.additional_code,
                error.name,
                error.description
            ))

        # Save events
        for event in profile.events:
            cursor.execute("""
                INSERT INTO events (device_id, code, name, description, event_type)
                VALUES (?, ?, ?, ?, ?)
            """, (
                device_id,
                event.code,
                event.name,
                event.description,
                event.event_type
            ))

        # Save process data inputs
        for pd in profile.process_data.inputs:
            cursor.execute("""
                INSERT INTO process_data (device_id, pd_id, name, direction, bit_length, data_type, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                device_id,
                pd.id,
                pd.name,
                'input',
                pd.bit_length,
                pd.data_type,
                pd.description
            ))
            pd_db_id = cursor.lastrowid

            # Save record items for this process data
            for item in pd.record_items:
                cursor.execute("""
                    INSERT INTO process_data_record_items (process_data_id, subindex, name, bit_offset, bit_length, data_type, default_value)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    pd_db_id,
                    item.subindex,
                    item.name,
                    item.bit_offset,
                    item.bit_length,
                    item.data_type,
                    item.default_value
                ))
                item_db_id = cursor.lastrowid

                # Save single values for this record item
                for single_val in item.single_values:
                    cursor.execute("""
                        INSERT INTO process_data_single_values (record_item_id, value, name, description)
                        VALUES (?, ?, ?, ?)
                    """, (
                        item_db_id,
                        single_val.value,
                        single_val.name,
                        single_val.description
                    ))

        # Save process data outputs
        for pd in profile.process_data.outputs:
            cursor.execute("""
                INSERT INTO process_data (device_id, pd_id, name, direction, bit_length, data_type, description)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                device_id,
                pd.id,
                pd.name,
                'output',
                pd.bit_length,
                pd.data_type,
                pd.description
            ))
            pd_db_id = cursor.lastrowid

            # Save record items for this process data
            for item in pd.record_items:
                cursor.execute("""
                    INSERT INTO process_data_record_items (process_data_id, subindex, name, bit_offset, bit_length, data_type, default_value)
                    VALUES (?, ?, ?, ?, ?, ?, ?)
                """, (
                    pd_db_id,
                    item.subindex,
                    item.name,
                    item.bit_offset,
                    item.bit_length,
                    item.data_type,
                    item.default_value
                ))
                item_db_id = cursor.lastrowid

                # Save single values for this record item
                for single_val in item.single_values:
                    cursor.execute("""
                        INSERT INTO process_data_single_values (record_item_id, value, name, description)
                        VALUES (?, ?, ?, ?)
                    """, (
                        item_db_id,
                        single_val.value,
                        single_val.name,
                        single_val.description
                    ))

        # Save document info
        if profile.document_info:
            cursor.execute("""
                INSERT INTO document_info (device_id, copyright, release_date, version)
                VALUES (?, ?, ?, ?)
            """, (
                device_id,
                profile.document_info.copyright,
                profile.document_info.release_date,
                profile.document_info.version
            ))

        # Save device features
        if profile.device_features:
            cursor.execute("""
                INSERT INTO device_features (device_id, block_parameter, data_storage, profile_characteristic,
                                            access_locks_data_storage, access_locks_local_parameterization,
                                            access_locks_local_user_interface, access_locks_parameter)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                device_id,
                1 if profile.device_features.block_parameter else 0,
                1 if profile.device_features.data_storage else 0,
                profile.device_features.profile_characteristic,
                1 if profile.device_features.access_locks_data_storage else 0,
                1 if profile.device_features.access_locks_local_parameterization else 0,
                1 if profile.device_features.access_locks_local_user_interface else 0,
                1 if profile.device_features.access_locks_parameter else 0
            ))

        # Save communication profile
        if profile.communication_profile:
            import json
            wire_config_json = json.dumps(profile.communication_profile.wire_config)
            cursor.execute("""
                INSERT INTO communication_profile (device_id, iolink_revision, compatible_with, bitrate,
                                                   min_cycle_time, msequence_capability, sio_supported,
                                                   connection_type, wire_config)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                device_id,
                profile.communication_profile.iolink_revision,
                profile.communication_profile.compatible_with,
                profile.communication_profile.bitrate,
                profile.communication_profile.min_cycle_time,
                profile.communication_profile.msequence_capability,
                1 if profile.communication_profile.sio_supported else 0,
                profile.communication_profile.connection_type,
                wire_config_json
            ))

        # Save UI menus
        if profile.ui_menus:
            import json
            for menu in profile.ui_menus.menus:
                cursor.execute("""
                    INSERT INTO ui_menus (device_id, menu_id, name)
                    VALUES (?, ?, ?)
                """, (device_id, menu.id, menu.name))
                menu_db_id = cursor.lastrowid

                # Save menu items
                for idx, item in enumerate(menu.items):
                    cursor.execute("""
                        INSERT INTO ui_menu_items (menu_id, variable_id, record_item_ref, subindex,
                                                   access_right_restriction, display_format, unit_code,
                                                   button_value, menu_ref, item_order, gradient, offset)
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        menu_db_id,
                        item.variable_id,
                        item.record_item_ref,
                        item.subindex,
                        item.access_right_restriction,
                        item.display_format,
                        item.unit_code,
                        item.button_value,
                        item.menu_ref,
                        idx,
                        item.gradient,
                        item.offset
                    ))
                    menu_item_db_id = cursor.lastrowid

                    # Save button configurations (Phase 3)
                    for button in item.buttons:
                        cursor.execute("""
                            INSERT INTO ui_menu_buttons (menu_item_id, button_value, description, action_started_message)
                            VALUES (?, ?, ?, ?)
                        """, (
                            menu_item_db_id,
                            button.button_value,
                            button.description,
                            button.action_started_message
                        ))

            # Save role menu mappings
            for menu_type, menu_id in profile.ui_menus.observer_role_menus.items():
                cursor.execute("""
                    INSERT INTO ui_menu_roles (device_id, role_type, menu_type, menu_id)
                    VALUES (?, ?, ?, ?)
                """, (device_id, 'observer', menu_type, menu_id))

            for menu_type, menu_id in profile.ui_menus.maintenance_role_menus.items():
                cursor.execute("""
                    INSERT INTO ui_menu_roles (device_id, role_type, menu_type, menu_id)
                    VALUES (?, ?, ?, ?)
                """, (device_id, 'maintenance', menu_type, menu_id))

            for menu_type, menu_id in profile.ui_menus.specialist_role_menus.items():
                cursor.execute("""
                    INSERT INTO ui_menu_roles (device_id, role_type, menu_type, menu_id)
                    VALUES (?, ?, ?, ?)
                """, (device_id, 'specialist', menu_type, menu_id))

        # Save multi-language text data
        if profile.all_text_data:
            for text_id, languages in profile.all_text_data.items():
                for language_code, text_value in languages.items():
                    cursor.execute("""
                        INSERT INTO iodd_text (device_id, text_id, language_code, text_value)
                        VALUES (?, ?, ?, ?)
                    """, (device_id, text_id, language_code, text_value))
            logger.info(f"Saved {sum(len(langs) for langs in profile.all_text_data.values())} text entries across {len(profile.all_text_data)} text IDs")

        # ===== PHASE 1: Save Process Data UI Info =====
        if profile.process_data_ui_info:
            # First, get process data IDs mapping
            pd_id_map = {}
            cursor.execute("SELECT id, pd_id FROM process_data WHERE device_id = ?", (device_id,))
            for row in cursor.fetchall():
                pd_id_map[row[1]] = row[0]

            for ui_info in profile.process_data_ui_info:
                process_data_db_id = pd_id_map.get(ui_info.process_data_id)
                if process_data_db_id:
                    cursor.execute("""
                        INSERT INTO process_data_ui_info (process_data_id, subindex, gradient, offset, unit_code, display_format)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        process_data_db_id,
                        ui_info.subindex,
                        ui_info.gradient,
                        ui_info.offset,
                        ui_info.unit_code,
                        ui_info.display_format
                    ))
            logger.info(f"Saved {len(profile.process_data_ui_info)} process data UI info entries")

        # ===== PHASE 2: Save Device Variants =====
        if profile.device_variants:
            for variant in profile.device_variants:
                cursor.execute("""
                    INSERT INTO device_variants (device_id, product_id, device_symbol, device_icon, name, description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    device_id,
                    variant.product_id,
                    variant.device_symbol,
                    variant.device_icon,
                    variant.name,
                    variant.description
                ))
            logger.info(f"Saved {len(profile.device_variants)} device variants")

        # ===== PHASE 2: Save Process Data Conditions =====
        # Get process data with conditions
        cursor.execute("SELECT id, pd_id FROM process_data WHERE device_id = ?", (device_id,))
        pd_id_map = {row[1]: row[0] for row in cursor.fetchall()}

        for pd in profile.process_data.inputs + profile.process_data.outputs:
            if pd.condition:
                process_data_db_id = pd_id_map.get(pd.id)
                if process_data_db_id:
                    cursor.execute("""
                        INSERT INTO process_data_conditions (process_data_id, condition_variable_id, condition_value)
                        VALUES (?, ?, ?)
                    """, (
                        process_data_db_id,
                        pd.condition.variable_id,
                        pd.condition.value
                    ))

        # ===== PHASE 4: Save Wire Configurations =====
        if profile.wire_configurations:
            for wire in profile.wire_configurations:
                cursor.execute("""
                    INSERT INTO wire_configurations (device_id, connection_type, wire_number, wire_color, wire_function, wire_description)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (
                    device_id,
                    wire.connection_type,
                    wire.wire_number,
                    wire.wire_color,
                    wire.wire_function,
                    wire.wire_description
                ))
            logger.info(f"Saved {len(profile.wire_configurations)} wire configurations")

        # ===== PHASE 4: Save Test Configurations =====
        if profile.test_configurations:
            for test_config in profile.test_configurations:
                cursor.execute("""
                    INSERT INTO device_test_config (device_id, config_type, param_index, test_value)
                    VALUES (?, ?, ?, ?)
                """, (
                    device_id,
                    test_config.config_type,
                    test_config.param_index,
                    test_config.test_value
                ))
                test_config_db_id = cursor.lastrowid

                # Save event triggers
                for trigger in test_config.event_triggers:
                    cursor.execute("""
                        INSERT INTO device_test_event_triggers (test_config_id, appear_value, disappear_value)
                        VALUES (?, ?, ?)
                    """, (
                        test_config_db_id,
                        trigger.appear_value,
                        trigger.disappear_value
                    ))
            logger.info(f"Saved {len(profile.test_configurations)} test configurations")

        # ===== PHASE 5: Save Custom Datatypes =====
        if profile.custom_datatypes:
            for datatype in profile.custom_datatypes:
                cursor.execute("""
                    INSERT INTO custom_datatypes (device_id, datatype_id, datatype_xsi_type, bit_length, subindex_access_supported)
                    VALUES (?, ?, ?, ?, ?)
                """, (
                    device_id,
                    datatype.datatype_id,
                    datatype.datatype_xsi_type,
                    datatype.bit_length,
                    1 if datatype.subindex_access_supported else 0
                ))
                datatype_db_id = cursor.lastrowid

                # Save single values
                for single_val in datatype.single_values:
                    cursor.execute("""
                        INSERT INTO custom_datatype_single_values (datatype_id, value, name)
                        VALUES (?, ?, ?)
                    """, (
                        datatype_db_id,
                        single_val.value,
                        single_val.name
                    ))

                # Save record items
                for record_item in datatype.record_items:
                    cursor.execute("""
                        INSERT INTO custom_datatype_record_items (datatype_id, subindex, bit_offset, bit_length, datatype_ref, name)
                        VALUES (?, ?, ?, ?, ?, ?)
                    """, (
                        datatype_db_id,
                        record_item.subindex,
                        record_item.bit_offset,
                        record_item.bit_length,
                        record_item.data_type,
                        record_item.name
                    ))
            logger.info(f"Saved {len(profile.custom_datatypes)} custom datatypes")

        # ===== PHASE 5: Update device with vendor logo =====
        if profile.vendor_logo_filename:
            cursor.execute("""
                UPDATE devices SET vendor_logo_filename = ? WHERE id = ?
            """, (profile.vendor_logo_filename, device_id))

        # ===== PHASE 5: Update iodd_files with stamp metadata =====
        if profile.stamp_crc or profile.checker_name or profile.checker_version:
            cursor.execute("""
                UPDATE iodd_files SET stamp_crc = ?, checker_name = ?, checker_version = ?
                WHERE device_id = ?
            """, (profile.stamp_crc, profile.checker_name, profile.checker_version, device_id))

        conn.commit()
        conn.close()

        logger.info(f"Saved device with ID: {device_id}")
        return device_id

    def save_assets(self, device_id: int, assets: List[Dict[str, Any]]) -> None:
        """Save asset files for a device

        Smart merge logic:
        - Only adds assets that don't already exist (by file_name)
        - Prevents duplicate assets when re-importing the same device

        Args:
            device_id: The device ID to associate assets with
            assets: List of dicts with keys: file_name, file_type, file_content, file_path, image_purpose (optional)
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        added_count = 0
        skipped_count = 0

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
                asset.get('image_purpose')
            ))
            added_count += 1

        conn.commit()
        conn.close()

        if added_count > 0:
            logger.info(f"Added {added_count} new asset file(s) for device {device_id}")

    def save_text_data(self, device_id: int, all_text_data: Dict[str, Dict[str, str]]) -> None:
        """Save multi-language text data to iodd_text table

        Args:
            device_id: The device ID to associate text with
            all_text_data: Dict[text_id, Dict[language_code, text_value]]
                Example: {
                    'TN_DeviceName': {'en': 'Sensor', 'de': 'Sensor'},
                    'TN_M_Ident': {'en': 'Identification', 'de': 'Identifikation'}
                }
        """
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()

        text_count = 0

        for text_id, languages in all_text_data.items():
            for language_code, text_value in languages.items():
                cursor.execute("""
                    INSERT INTO iodd_text (device_id, text_id, language_code, text_value)
                    VALUES (?, ?, ?, ?)
                """, (device_id, text_id, language_code, text_value))
                text_count += 1

        conn.commit()
        conn.close()

        logger.info(f"Saved {text_count} text entries across {len(all_text_data)} text IDs for device {device_id}")

    def get_assets(self, device_id: int) -> List[Dict[str, Any]]:
        """Retrieve all asset files for a device

        Returns:
            List of dicts with keys: id, file_name, file_type, file_content, file_path
        """
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM iodd_assets WHERE device_id = ?", (device_id,))
        assets = [dict(row) for row in cursor.fetchall()]

        conn.close()
        return assets

    def get_device(self, device_id: int) -> Optional[Dict[str, Any]]:
        """Retrieve device information from database"""
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute("SELECT * FROM devices WHERE id = ?", (device_id,))
        device = cursor.fetchone()
        
        if device:
            # Get parameters
            cursor.execute("SELECT * FROM parameters WHERE device_id = ?", (device_id,))
            parameters = cursor.fetchall()
            
            result = dict(device)
            result['parameters'] = [dict(p) for p in parameters]
            
            conn.close()
            return result
        
        conn.close()
        return None

# ============================================================================
# Adapter Generators
# ============================================================================

class AdapterGenerator(ABC):
    """Abstract base class for adapter generators"""
    
    @abstractmethod
    def generate(self, profile: DeviceProfile) -> Dict[str, str]:
        """Generate adapter code for the device profile"""
        pass
    
    @property
    @abstractmethod
    def platform_name(self) -> str:
        """Return the platform name"""
        pass
    
    def validate(self, code: Dict[str, str]) -> bool:
        """Validate generated code"""
        return all(code.values())

class NodeREDGenerator(AdapterGenerator):
    """Generate Node-RED nodes from IODD profiles"""

    @property
    def platform_name(self) -> str:
        return "node-red"
    
    def generate(self, profile: DeviceProfile) -> Dict[str, str]:
        """Generate Node-RED node package"""
        logger.info(f"Generating Node-RED node for {profile.device_info.product_name}")
        
        safe_name = self._make_safe_name(profile.device_info.product_name)
        
        return {
            'package.json': self._generate_package_json(profile, safe_name),
            f'{safe_name}.js': self._generate_node_js(profile, safe_name),
            f'{safe_name}.html': self._generate_node_html(profile, safe_name),
            'README.md': self._generate_readme(profile, safe_name)
        }
    
    def _make_safe_name(self, name: str) -> str:
        """Convert name to safe identifier"""
        import re
        safe = re.sub(r'[^a-zA-Z0-9]', '-', name.lower())
        safe = re.sub(r'-+', '-', safe).strip('-')
        return safe
    
    def _generate_package_json(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate package.json for Node-RED node"""
        package = {
            "name": f"node-red-contrib-{safe_name}",
            "version": "1.0.0",
            "description": f"Node-RED node for {profile.device_info.product_name} IO-Link device",
            "keywords": ["node-red", "io-link", profile.vendor_info.name, safe_name],
            "node-red": {
                "nodes": {
                    safe_name: f"{safe_name}.js"
                }
            },
            "author": "Greenstack",
            "license": "MIT"
        }
        return json.dumps(package, indent=2)
    
    def _generate_node_js(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate Node.js code for the node"""
        template = Template("""
module.exports = function(RED) {
    function {{ node_name }}Node(config) {
        RED.nodes.createNode(this, config);
        var node = this;
        
        // Configuration
        this.deviceId = {{ device_id }};
        this.vendorId = {{ vendor_id }};
        this.productName = "{{ product_name }}";
        
        // Parameters
        {% for param in parameters %}
        this.param_{{ param.name | replace(' ', '_') }} = config.param_{{ param.name | replace(' ', '_') }};
        {% endfor %}
        
        // Process Data Configuration
        this.processDataIn = {
            totalBits: {{ process_data.total_input_bits }},
            data: [
                {% for pd in process_data.inputs %}
                { index: {{ pd.index }}, name: "{{ pd.name }}", bits: {{ pd.bit_length }} },
                {% endfor %}
            ]
        };
        
        this.processDataOut = {
            totalBits: {{ process_data.total_output_bits }},
            data: [
                {% for pd in process_data.outputs %}
                { index: {{ pd.index }}, name: "{{ pd.name }}", bits: {{ pd.bit_length }} },
                {% endfor %}
            ]
        };
        
        // Handle input messages
        node.on('input', function(msg) {
            try {
                // Parse IO-Link communication
                if (msg.topic === 'read') {
                    // Read parameter
                    var paramIndex = msg.payload.index;
                    // TODO: Implement IO-Link read
                    node.send({
                        payload: {
                            index: paramIndex,
                            value: 0 // Placeholder
                        }
                    });
                } else if (msg.topic === 'write') {
                    // Write parameter
                    var paramIndex = msg.payload.index;
                    var value = msg.payload.value;
                    // TODO: Implement IO-Link write
                    node.send({
                        payload: {
                            index: paramIndex,
                            value: value,
                            status: 'written'
                        }
                    });
                } else if (msg.topic === 'processdata') {
                    // Handle process data
                    // TODO: Implement process data handling
                    node.send({
                        payload: {
                            inputs: node.processDataIn,
                            outputs: node.processDataOut
                        }
                    });
                }
                
                node.status({fill:"green", shape:"dot", text:"connected"});
            } catch(err) {
                node.error(err);
                node.status({fill:"red", shape:"ring", text:"error"});
            }
        });
        
        node.on('close', function() {
            // Cleanup
        });
    }
    
    RED.nodes.registerType("{{ node_name }}", {{ node_name }}Node);
}
""")
        
        return template.render(
            node_name=safe_name,
            device_id=profile.device_info.device_id,
            vendor_id=profile.device_info.vendor_id,
            product_name=profile.device_info.product_name,
            parameters=profile.parameters[:10],  # Limit to first 10 parameters for simplicity
            process_data=profile.process_data
        )
    
    def _generate_node_html(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate HTML configuration interface for the node"""
        template = Template("""
<script type="text/javascript">
    RED.nodes.registerType('{{ node_name }}', {
        category: 'IO-Link',
        color: '#3FADB5',
        defaults: {
            name: {value: ""},
            {% for param in parameters %}
            {% if param.access_rights.value in ['rw', 'wo'] %}
            param_{{ param.name | replace(' ', '_') }}: {value: "{{ param.default_value or '' }}"},
            {% endif %}
            {% endfor %}
        },
        inputs: 1,
        outputs: 1,
        icon: "serial.png",
        label: function() {
            return this.name || "{{ product_name }}";
        },
        paletteLabel: "{{ product_name }}"
    });
</script>

<script type="text/x-red" data-template-name="{{ node_name }}">
    <div class="form-row">
        <label for="node-input-name"><i class="fa fa-tag"></i> Name</label>
        <input type="text" id="node-input-name" placeholder="Name">
    </div>
    
    <h4>Device Information</h4>
    <div class="form-row">
        <label>Product:</label>
        <span>{{ product_name }}</span>
    </div>
    <div class="form-row">
        <label>Vendor:</label>
        <span>{{ vendor_name }}</span>
    </div>
    <div class="form-row">
        <label>Device ID:</label>
        <span>{{ device_id }}</span>
    </div>
    
    <h4>Configurable Parameters</h4>
    {% for param in parameters %}
    {% if param.access_rights.value in ['rw', 'wo'] %}
    <div class="form-row">
        <label for="node-input-param_{{ param.name | replace(' ', '_') }}">
            <i class="fa fa-cog"></i> {{ param.name }}
        </label>
        <input type="text" id="node-input-param_{{ param.name | replace(' ', '_') }}" 
               placeholder="{{ param.default_value or '' }}">
        {% if param.description %}
        <div class="form-tips">{{ param.description }}</div>
        {% endif %}
    </div>
    {% endif %}
    {% endfor %}
</script>

<script type="text/x-red" data-help-name="{{ node_name }}">
    <p>Node-RED node for {{ product_name }} IO-Link device.</p>
    
    <h3>Inputs</h3>
    <dl class="message-properties">
        <dt>topic <span class="property-type">string</span></dt>
        <dd>Command type: "read", "write", or "processdata"</dd>
        <dt>payload <span class="property-type">object</span></dt>
        <dd>Command parameters (index, value)</dd>
    </dl>
    
    <h3>Outputs</h3>
    <dl class="message-properties">
        <dt>payload <span class="property-type">object</span></dt>
        <dd>Response data from the device</dd>
    </dl>
    
    <h3>Device Parameters</h3>
    <ul>
    {% for param in parameters %}
        <li><b>{{ param.name }}</b> (Index: {{ param.index }}, Type: {{ param.data_type.value }}, Access: {{ param.access_rights.value }})</li>
    {% endfor %}
    </ul>
    
    <h3>Process Data</h3>
    <p>Input: {{ process_data.total_input_bits }} bits</p>
    <p>Output: {{ process_data.total_output_bits }} bits</p>
</script>
""")
        
        return template.render(
            node_name=safe_name,
            product_name=profile.device_info.product_name,
            vendor_name=profile.vendor_info.name,
            device_id=profile.device_info.device_id,
            parameters=profile.parameters[:10],  # Limit for UI simplicity
            process_data=profile.process_data
        )
    
    def _generate_readme(self, profile: DeviceProfile, safe_name: str) -> str:
        """Generate README.md for the node package"""
        template = Template("""
# node-red-contrib-{{ safe_name }}

Node-RED node for {{ product_name }} IO-Link device.

## Installation

```bash
npm install node-red-contrib-{{ safe_name }}
```

## Device Information

- **Product**: {{ product_name }}
- **Vendor**: {{ vendor_name }}
- **Vendor ID**: {{ vendor_id }}
- **Device ID**: {{ device_id }}
- **IODD Version**: {{ iodd_version }}

## Usage

This node provides access to the {{ product_name }} IO-Link device parameters and process data.

### Supported Operations

1. **Read Parameter**: Send a message with `topic: "read"` and `payload.index: <parameter_index>`
2. **Write Parameter**: Send a message with `topic: "write"`, `payload.index: <parameter_index>` and `payload.value: <value>`
3. **Process Data**: Send a message with `topic: "processdata"` to get current process data configuration

## Parameters

The device supports {{ param_count }} parameters with various access rights.

## Process Data

- **Input**: {{ input_bits }} bits
- **Output**: {{ output_bits }} bits

## License

MIT
""")
        
        return template.render(
            safe_name=safe_name,
            product_name=profile.device_info.product_name,
            vendor_name=profile.vendor_info.name,
            vendor_id=profile.device_info.vendor_id,
            device_id=profile.device_info.device_id,
            iodd_version=profile.iodd_version,
            param_count=len(profile.parameters),
            input_bits=profile.process_data.total_input_bits,
            output_bits=profile.process_data.total_output_bits
        )

# ============================================================================
# Main Greenstack
# ============================================================================

class IODDManager:
    """Main IODD management system"""
    
    def __init__(self, storage_path: str = "./iodd_storage", db_path: str = "greenstack.db"):
        self.ingester = IODDIngester(Path(storage_path))
        self.storage = StorageManager(db_path)
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
