"""
Unit Tests for Adapter Generation (src/generation)
====================================================

Tests the adapter generator classes for Node-RED and other platforms.
"""

import json
import pytest

from src.generation import AdapterGenerator, NodeREDGenerator
from src.models import (
    AccessRights,
    CommunicationProfile,
    DeviceFeatures,
    DeviceInfo,
    DeviceProfile,
    IODDDataType,
    Parameter,
    ProcessData,
    ProcessDataCollection,
    VendorInfo,
)


@pytest.fixture
def sample_device_profile():
    """Create a sample device profile for testing generators."""
    vendor = VendorInfo(
        id=1234,
        name="Test Vendor Inc.",
        text="Leading IO-Link manufacturer",
        url="https://testvendor.com"
    )

    device = DeviceInfo(
        vendor_id=1234,
        device_id=5678,
        product_name="Temperature Sensor Pro",
        product_text="High-precision temperature sensor",
        hardware_revision="1.0",
        firmware_revision="2.3.1"
    )

    parameters = [
        Parameter(
            id="V_Temp",
            index=100,
            subindex=1,
            name="Temperature Value",
            description="Current temperature reading",
            data_type=IODDDataType.FLOAT,
            bit_length=32,
            access_rights=AccessRights.READ_ONLY,
            default_value=None
        ),
        Parameter(
            id="V_SetPoint",
            index=101,
            subindex=1,
            name="Set Point",
            description="Temperature setpoint",
            data_type=IODDDataType.FLOAT,
            bit_length=32,
            access_rights=AccessRights.READ_WRITE,
            default_value=25.0
        ),
        Parameter(
            id="V_Status",
            index=36,
            subindex=0,
            name="Device Status",
            description="Current device status",
            data_type=IODDDataType.UNSIGNED_INTEGER,
            bit_length=8,
            access_rights=AccessRights.READ_ONLY,
            default_value=0
        )
    ]

    process_data_in = [
        ProcessData(
            id="PDI_Temp",
            index=1,
            subindex=1,
            name="Temperature",
            bit_offset=0,
            bit_length=16,
            data_type=IODDDataType.UNSIGNED_INTEGER
        )
    ]

    process_data_out = [
        ProcessData(
            id="PDO_Control",
            index=1,
            subindex=1,
            name="Control",
            bit_offset=0,
            bit_length=8,
            data_type=IODDDataType.UNSIGNED_INTEGER
        )
    ]

    process_data_collection = ProcessDataCollection(
        inputs=process_data_in,
        outputs=process_data_out,
        total_input_bits=16,
        total_output_bits=8
    )

    features = DeviceFeatures(
        block_parameter=True,
        data_storage=True,
        profile_charset="UTF-8"
    )

    comm = CommunicationProfile(
        profile_type="IOLink",
        iolink_revision="1.1",
        min_cycle_time=5000,
        supported_bitrates=["COM2", "COM3"]
    )

    return DeviceProfile(
        vendor_info=vendor,
        device_info=device,
        parameters=parameters,
        process_data=process_data_collection,
        errors=[],
        events=[],
        ui_menus=[],
        device_features=features,
        communication_profile=comm,
        iodd_version="1.1",
        custom_datatypes=[],
        device_variants=[],
        documents=[]
    )


class TestAdapterGenerator:
    """Test the abstract AdapterGenerator base class."""

    def test_adapter_generator_is_abstract(self):
        """Test that AdapterGenerator cannot be instantiated directly."""
        with pytest.raises(TypeError):
            AdapterGenerator()

    def test_subclass_must_implement_generate(self):
        """Test that subclasses must implement generate method."""
        class IncompleteGenerator(AdapterGenerator):
            @property
            def platform_name(self) -> str:
                return "test"

        with pytest.raises(TypeError):
            IncompleteGenerator()


class TestNodeREDGenerator:
    """Test the NodeREDGenerator class."""

    def test_node_red_generator_instantiation(self):
        """Test that NodeREDGenerator can be instantiated."""
        generator = NodeREDGenerator()
        assert generator is not None
        assert generator.platform_name == "node-red"

    def test_generate_returns_dict(self, sample_device_profile):
        """Test that generate returns a dictionary of files."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        assert isinstance(result, dict)
        assert len(result) > 0

    def test_generate_creates_package_json(self, sample_device_profile):
        """Test that package.json is generated."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        assert 'package.json' in result
        package_json = json.loads(result['package.json'])

        assert 'name' in package_json
        assert 'version' in package_json
        assert 'description' in package_json
        assert 'node-red' in package_json

    def test_package_json_contains_correct_info(self, sample_device_profile):
        """Test that package.json contains device information."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        package_json = json.loads(result['package.json'])

        assert 'node-red-contrib' in package_json['name']
        assert 'Temperature Sensor Pro' in package_json['description']
        assert 'keywords' in package_json
        assert 'node-red' in package_json['keywords']
        assert 'io-link' in package_json['keywords']

    def test_generate_creates_node_js(self, sample_device_profile):
        """Test that Node.js file is generated."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        # Find the .js file
        js_files = [k for k in result.keys() if k.endswith('.js')]
        assert len(js_files) == 1

        js_content = result[js_files[0]]
        assert 'module.exports' in js_content
        assert 'RED.nodes.createNode' in js_content
        assert 'RED.nodes.registerType' in js_content

    def test_node_js_contains_device_ids(self, sample_device_profile):
        """Test that Node.js file contains device IDs."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        js_files = [k for k in result.keys() if k.endswith('.js')]
        js_content = result[js_files[0]]

        assert '1234' in js_content  # vendor_id
        assert '5678' in js_content  # device_id

    def test_node_js_contains_parameters(self, sample_device_profile):
        """Test that Node.js file references parameters."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        js_files = [k for k in result.keys() if k.endswith('.js')]
        js_content = result[js_files[0]]

        # Check that parameters are referenced
        assert 'param_' in js_content or 'parameters' in js_content

    def test_node_js_contains_process_data(self, sample_device_profile):
        """Test that Node.js file contains process data configuration."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        js_files = [k for k in result.keys() if k.endswith('.js')]
        js_content = result[js_files[0]]

        assert 'processDataIn' in js_content
        assert 'processDataOut' in js_content
        assert '16' in js_content  # total_input_bits
        assert '8' in js_content   # total_output_bits

    def test_generate_creates_node_html(self, sample_device_profile):
        """Test that HTML file is generated."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        # Find the .html file
        html_files = [k for k in result.keys() if k.endswith('.html')]
        assert len(html_files) == 1

        html_content = result[html_files[0]]
        assert 'RED.nodes.registerType' in html_content
        assert '<script' in html_content

    def test_node_html_contains_device_info(self, sample_device_profile):
        """Test that HTML file contains device information."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        html_files = [k for k in result.keys() if k.endswith('.html')]
        html_content = result[html_files[0]]

        assert 'Temperature Sensor Pro' in html_content
        assert 'Test Vendor Inc.' in html_content

    def test_node_html_contains_configurable_parameters(self, sample_device_profile):
        """Test that HTML file has inputs for configurable parameters."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        html_files = [k for k in result.keys() if k.endswith('.html')]
        html_content = result[html_files[0]]

        # Should have form inputs for read-write parameters
        assert 'form-row' in html_content or 'input' in html_content

    def test_generate_creates_readme(self, sample_device_profile):
        """Test that README.md is generated."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        assert 'README.md' in result
        readme = result['README.md']

        assert '# node-red-contrib' in readme
        assert 'Temperature Sensor Pro' in readme

    def test_readme_contains_installation_instructions(self, sample_device_profile):
        """Test that README contains installation instructions."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        readme = result['README.md']

        assert 'Installation' in readme or 'install' in readme
        assert 'npm install' in readme

    def test_readme_contains_device_information(self, sample_device_profile):
        """Test that README contains device information."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        readme = result['README.md']

        assert 'Vendor' in readme or 'vendor' in readme
        assert 'Device' in readme or 'device' in readme
        assert '1234' in readme  # vendor_id
        assert '5678' in readme  # device_id

    def test_readme_contains_usage_information(self, sample_device_profile):
        """Test that README contains usage information."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        readme = result['README.md']

        assert 'Usage' in readme or 'usage' in readme
        assert 'read' in readme.lower()
        assert 'write' in readme.lower()

    def test_make_safe_name(self):
        """Test the _make_safe_name method."""
        generator = NodeREDGenerator()

        assert generator._make_safe_name("Simple Name") == "simple-name"
        assert generator._make_safe_name("Name With Spaces") == "name-with-spaces"
        assert generator._make_safe_name("Name_With_Underscores") == "name-with-underscores"
        assert generator._make_safe_name("Name123") == "name123"
        assert generator._make_safe_name("Multiple---Dashes") == "multiple-dashes"

    def test_make_safe_name_removes_special_characters(self):
        """Test that _make_safe_name removes special characters."""
        generator = NodeREDGenerator()

        result = generator._make_safe_name("Name@#$%^&*()With!Special")
        assert '@' not in result
        assert '#' not in result
        assert '$' not in result
        assert result.replace('-', '').isalnum()

    def test_validate_generated_code(self, sample_device_profile):
        """Test that generated code passes validation."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        # Validate should return True if all files have content
        assert generator.validate(result)

    def test_all_files_have_content(self, sample_device_profile):
        """Test that all generated files have non-empty content."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        for filename, content in result.items():
            assert content, f"File {filename} is empty"
            assert len(content) > 0, f"File {filename} has no content"

    def test_generated_package_json_is_valid_json(self, sample_device_profile):
        """Test that generated package.json is valid JSON."""
        generator = NodeREDGenerator()
        result = generator.generate(sample_device_profile)

        # Should not raise an exception
        try:
            package = json.loads(result['package.json'])
            assert isinstance(package, dict)
        except json.JSONDecodeError:
            pytest.fail("Generated package.json is not valid JSON")

    def test_generate_with_minimal_profile(self):
        """Test generation with minimal device profile."""
        vendor = VendorInfo(id=1, name="Minimal Vendor", text="Minimal description")
        device = DeviceInfo(vendor_id=1, device_id=1, product_name="Minimal Device")
        pd_collection = ProcessDataCollection([], [], 0, 0)

        minimal_profile = DeviceProfile(
            vendor_info=vendor,
            device_info=device,
            parameters=[],
            process_data=pd_collection,
            errors=[],
            events=[],
            ui_menus=[],
            device_features=None,
            communication_profile=None,
            iodd_version="1.0",
            custom_datatypes=[],
            device_variants=[],
            documents=[]
        )

        generator = NodeREDGenerator()
        result = generator.generate(minimal_profile)

        # Should still generate all required files
        assert 'package.json' in result
        assert any(k.endswith('.js') for k in result.keys())
        assert any(k.endswith('.html') for k in result.keys())
        assert 'README.md' in result

    def test_generate_handles_special_characters_in_product_name(self):
        """Test that generator handles special characters in product name."""
        vendor = VendorInfo(id=1, name="Test Vendor", text="Test description")
        device = DeviceInfo(
            vendor_id=1,
            device_id=1,
            product_name="Product@#$%Name!"
        )
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
            iodd_version="1.0",
            custom_datatypes=[],
            device_variants=[],
            documents=[]
        )

        generator = NodeREDGenerator()
        result = generator.generate(profile)

        # Should successfully generate without errors
        assert len(result) > 0

        # Package name should be safe
        package = json.loads(result['package.json'])
        assert '@' not in package['name']
        assert '#' not in package['name']
