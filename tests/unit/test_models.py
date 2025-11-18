"""
Unit Tests for Data Models (src/models)
========================================

Tests all dataclass models and enums used throughout the application.
"""

import pytest
from datetime import datetime

from src.models import (
    # Enums
    IODDDataType,
    AccessRights,

    # Core Models
    VendorInfo,
    DeviceInfo,
    Parameter,
    ProcessData,
    ProcessDataCollection,
    DeviceProfile,

    # Additional Models
    ErrorType,
    Event,
    DocumentInfo,
    DeviceFeatures,
    CommunicationProfile,
    Menu,
    MenuItem,
    CustomDatatype,
    Constraint,
    DeviceVariant,  # Changed from ProductVariant
)


class TestEnums:
    """Test enumeration types."""

    def test_iodd_data_type_enum(self):
        """Test IODDDataType enum values."""
        assert IODDDataType.BOOLEAN.value == "BooleanT"
        assert IODDDataType.INTEGER.value == "IntegerT"
        assert IODDDataType.UNSIGNED_INTEGER.value == "UIntegerT"
        assert IODDDataType.FLOAT.value == "Float32T"
        assert IODDDataType.STRING.value == "StringT"
        assert IODDDataType.OCTET_STRING.value == "OctetStringT"

    def test_access_rights_enum(self):
        """Test AccessRights enum values."""
        assert AccessRights.READ_ONLY.value == "ro"
        assert AccessRights.WRITE_ONLY.value == "wo"
        assert AccessRights.READ_WRITE.value == "rw"

    def test_enum_membership(self):
        """Test that enum values can be looked up."""
        # Test IODDDataType membership
        assert "BooleanT" in [t.value for t in IODDDataType]
        assert "InvalidType" not in [t.value for t in IODDDataType]

        # Test AccessRights membership
        assert "ro" in [r.value for r in AccessRights]
        assert "invalid" not in [r.value for r in AccessRights]


class TestVendorInfo:
    """Test VendorInfo dataclass."""

    def test_create_vendor_info(self):
        """Test creating a VendorInfo instance."""
        vendor = VendorInfo(
            id=42,
            name="ACME Corp",
            text="Leading industrial sensor manufacturer",
            url="https://www.acme.com"
        )

        assert vendor.id == 42
        assert vendor.name == "ACME Corp"
        assert vendor.text == "Leading industrial sensor manufacturer"
        assert vendor.url == "https://www.acme.com"

    def test_vendor_info_defaults(self):
        """Test VendorInfo with minimal required fields."""
        vendor = VendorInfo(id=1, name="Test Vendor", text="Test description")

        assert vendor.id == 1
        assert vendor.name == "Test Vendor"
        assert vendor.text == "Test description"
        assert vendor.url is None


class TestDeviceInfo:
    """Test DeviceInfo dataclass."""

    def test_create_device_info(self):
        """Test creating a DeviceInfo instance."""
        device = DeviceInfo(
            vendor_id=42,
            device_id=1234,
            product_name="Sensor Pro 3000",
            product_text="High-precision temperature sensor",
            product_id="SP3000",
            hardware_revision="2.1",
            firmware_revision="1.5.3",
            device_family="Temperature Sensors"
        )

        assert device.vendor_id == 42
        assert device.device_id == 1234
        assert device.product_name == "Sensor Pro 3000"
        assert device.hardware_revision == "2.1"
        assert device.firmware_revision == "1.5.3"

    def test_device_info_minimal(self):
        """Test DeviceInfo with only required fields."""
        device = DeviceInfo(
            vendor_id=10,
            device_id=20,
            product_name="Basic Sensor"
        )

        assert device.vendor_id == 10
        assert device.device_id == 20
        assert device.product_name == "Basic Sensor"
        assert device.product_text is None
        assert device.hardware_revision is None


class TestParameter:
    """Test Parameter dataclass."""

    def test_create_parameter(self):
        """Test creating a Parameter instance."""
        param = Parameter(
            id="V_Temp",
            index=100,
            subindex=1,
            name="Temperature",
            description="Current temperature reading",
            data_type=IODDDataType.FLOAT,
            bit_length=32,
            access_rights=AccessRights.READ_ONLY,
            default_value=25.0
        )

        assert param.id == "V_Temp"
        assert param.index == 100
        assert param.subindex == 1
        assert param.name == "Temperature"
        assert param.data_type == IODDDataType.FLOAT
        assert param.bit_length == 32
        assert param.access_rights == AccessRights.READ_ONLY
        assert param.default_value == 25.0

    def test_parameter_read_write(self):
        """Test parameter with read-write access."""
        param = Parameter(
            id="V_SetPoint",
            index=101,
            subindex=0,
            name="Set Point",
            description="Temperature setpoint",
            data_type=IODDDataType.FLOAT,
            bit_length=32,
            access_rights=AccessRights.READ_WRITE,
            default_value=20.0
        )

        assert param.access_rights == AccessRights.READ_WRITE

    def test_parameter_integer(self):
        """Test parameter with integer type."""
        param = Parameter(
            id="V_Count",
            index=50,
            subindex=0,
            name="Counter",
            description="Event counter",
            data_type=IODDDataType.UNSIGNED_INTEGER,
            bit_length=16,
            access_rights=AccessRights.READ_ONLY,
            default_value=0
        )

        assert param.data_type == IODDDataType.UNSIGNED_INTEGER
        assert param.bit_length == 16


class TestProcessData:
    """Test ProcessData dataclass."""

    def test_create_process_data(self):
        """Test creating a ProcessData instance."""
        pd = ProcessData(
            id="PDI_Status",
            index=1,
            subindex=0,
            name="Status Byte",
            bit_offset=0,
            bit_length=8,
            data_type=IODDDataType.UNSIGNED_INTEGER
        )

        assert pd.id == "PDI_Status"
        assert pd.index == 1
        assert pd.bit_offset == 0
        assert pd.bit_length == 8
        assert pd.data_type == IODDDataType.UNSIGNED_INTEGER

    def test_process_data_multi_byte(self):
        """Test process data with multi-byte length."""
        pd = ProcessData(
            id="PDI_Value",
            index=2,
            subindex=0,
            name="Measurement Value",
            bit_offset=8,
            bit_length=16,
            data_type=IODDDataType.UNSIGNED_INTEGER
        )

        assert pd.bit_length == 16
        assert pd.bit_offset == 8


class TestProcessDataCollection:
    """Test ProcessDataCollection dataclass."""

    def test_create_process_data_collection(self):
        """Test creating a ProcessDataCollection."""
        inputs = [
            ProcessData("PDI_1", 1, 0, "Status", 0, 8, IODDDataType.UNSIGNED_INTEGER),
            ProcessData("PDI_2", 2, 0, "Value", 8, 16, IODDDataType.UNSIGNED_INTEGER)
        ]

        outputs = [
            ProcessData("PDO_1", 1, 0, "Control", 0, 8, IODDDataType.UNSIGNED_INTEGER)
        ]

        pd_collection = ProcessDataCollection(
            inputs=inputs,
            outputs=outputs,
            total_input_bits=24,  # 8 + 16
            total_output_bits=8
        )

        assert len(pd_collection.inputs) == 2
        assert len(pd_collection.outputs) == 1
        assert pd_collection.total_input_bits == 24
        assert pd_collection.total_output_bits == 8

    def test_empty_process_data_collection(self):
        """Test ProcessDataCollection with no data."""
        pd_collection = ProcessDataCollection(
            inputs=[],
            outputs=[],
            total_input_bits=0,
            total_output_bits=0
        )

        assert len(pd_collection.inputs) == 0
        assert len(pd_collection.outputs) == 0


class TestErrorType:
    """Test ErrorType dataclass."""

    def test_create_error_type(self):
        """Test creating an ErrorType instance."""
        error = ErrorType(
            code="0x8001",
            name="Communication Error",
            description="Lost connection to device"
        )

        assert error.code == "0x8001"
        assert error.name == "Communication Error"
        assert error.description == "Lost connection to device"


class TestEvent:
    """Test Event dataclass."""

    def test_create_event(self):
        """Test creating an Event instance."""
        event = Event(
            code="0x4001",
            event_type="Notification",
            name="Power On",
            description="Device powered on successfully"
        )

        assert event.code == "0x4001"
        assert event.event_type == "Notification"
        assert event.name == "Power On"


class TestDocumentInfo:
    """Test DocumentInfo dataclass."""

    def test_create_document_info(self):
        """Test creating a DocumentInfo instance."""
        doc = DocumentInfo(
            title="User Manual",
            document_type="PDF",
            file_path="docs/manual.pdf",
            language="en",
            version="1.0"
        )

        assert doc.title == "User Manual"
        assert doc.document_type == "PDF"
        assert doc.file_path == "docs/manual.pdf"
        assert doc.language == "en"


class TestDeviceFeatures:
    """Test DeviceFeatures dataclass."""

    def test_create_device_features(self):
        """Test creating a DeviceFeatures instance."""
        features = DeviceFeatures(
            block_parameter=True,
            data_storage=True,
            profile_charset="UTF-8"
        )

        assert features.block_parameter is True
        assert features.data_storage is True
        assert features.profile_charset == "UTF-8"


class TestCommunicationProfile:
    """Test CommunicationProfile dataclass."""

    def test_create_communication_profile(self):
        """Test creating a CommunicationProfile instance."""
        comm = CommunicationProfile(
            profile_type="IOLink",
            iolink_revision="1.1",
            min_cycle_time=5000,
            supported_bitrates=["COM1", "COM2", "COM3"]
        )

        assert comm.profile_type == "IOLink"
        assert comm.iolink_revision == "1.1"
        assert comm.min_cycle_time == 5000
        assert len(comm.supported_bitrates) == 3


class TestMenu:
    """Test Menu and MenuItem dataclasses."""

    def test_create_menu_item(self):
        """Test creating a MenuItem instance."""
        item = MenuItem(
            variable_id="V_Temperature",
            subindex=1,
            name="Temperature Reading"
        )

        assert item.variable_id == "V_Temperature"
        assert item.subindex == 1
        assert item.name == "Temperature Reading"

    def test_create_menu(self):
        """Test creating a Menu instance."""
        items = [
            MenuItem("V_Temp", 1, "Temperature"),
            MenuItem("V_SetPoint", 0, "Set Point")
        ]

        menu = Menu(
            id="M_Main",
            name="Main Menu",
            items=items
        )

        assert menu.id == "M_Main"
        assert menu.name == "Main Menu"
        assert len(menu.items) == 2


class TestDeviceProfile:
    """Test complete DeviceProfile dataclass."""

    def test_create_minimal_device_profile(self):
        """Test creating a minimal DeviceProfile."""
        vendor = VendorInfo(id=1, name="Test Vendor", text="Test description")
        device = DeviceInfo(vendor_id=1, device_id=1, product_name="Test Device")
        pd_collection = ProcessDataCollection([], [], 0, 0)

        profile = DeviceProfile(
            vendor_info=vendor,
            device_info=device,
            parameters=[],
            process_data=pd_collection,
            errors=[],
            events=[],
            ui_menus=[],
            device_features=None,
            communication_profile=None,
            iodd_version="1.1",
            custom_datatypes=[],
            device_variants=[],
            documents=[]
        )

        assert profile.vendor_info.name == "Test Vendor"
        assert profile.device_info.product_name == "Test Device"
        assert len(profile.parameters) == 0
        assert profile.iodd_version == "1.1"

    def test_create_full_device_profile(self):
        """Test creating a complete DeviceProfile with all fields."""
        vendor = VendorInfo(
            id=42,
            name="ACME Corp",
            text="Industrial sensors",
            url="https://acme.com"
        )

        device = DeviceInfo(
            vendor_id=42,
            device_id=1234,
            product_name="Sensor Pro",
            hardware_revision="1.0",
            firmware_revision="2.0"
        )

        params = [
            Parameter(
                id="V_Temp",
                index=100,
                subindex=0,
                name="Temperature",
                description="Temperature reading",
                data_type=IODDDataType.FLOAT,
                bit_length=32,
                access_rights=AccessRights.READ_ONLY,
                default_value=0.0
            )
        ]

        pd_collection = ProcessDataCollection(
            inputs=[ProcessData("PDI_1", 1, 0, "Input", 0, 16, IODDDataType.UNSIGNED_INTEGER)],
            outputs=[ProcessData("PDO_1", 1, 0, "Output", 0, 8, IODDDataType.UNSIGNED_INTEGER)],
            total_input_bits=16,
            total_output_bits=8
        )

        errors = [ErrorType("0x8001", "Comm Error", "Communication failed")]
        events = [Event("0x4001", "Notification", "Power On", "Device started")]

        features = DeviceFeatures(block_parameter=True, data_storage=True)
        comm = CommunicationProfile(profile_type="IOLink", iolink_revision="1.1")

        profile = DeviceProfile(
            vendor_info=vendor,
            device_info=device,
            parameters=params,
            process_data=pd_collection,
            errors=errors,
            events=events,
            ui_menus=[],
            device_features=features,
            communication_profile=comm,
            iodd_version="1.1",
            custom_datatypes=[],
            device_variants=[],
            documents=[]
        )

        assert profile.vendor_info.name == "ACME Corp"
        assert profile.device_info.vendor_id == 42
        assert len(profile.parameters) == 1
        assert len(profile.errors) == 1
        assert len(profile.events) == 1
        assert profile.device_features.block_parameter is True
        assert profile.communication_profile.profile_type == "IOLink"
