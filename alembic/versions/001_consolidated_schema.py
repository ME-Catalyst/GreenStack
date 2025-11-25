"""Consolidated database schema migration

Revision ID: 001_consolidated
Revises: None
Create Date: 2025-11-25

This migration consolidates all 98 previous migrations into a single
comprehensive schema definition. It creates all tables, columns, and
indexes required for the current version of GreenStack.

Previous migrations (001-098) are archived in alembic/versions/archive/
and can be referenced for historical context.
"""

from alembic import op
import sqlalchemy as sa


# revision identifiers
revision = '001_consolidated'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    """Create all tables and indexes for GreenStack database"""

    # Get connection for direct SQL execution
    conn = op.get_bind()

    # Execute table creation statements

    # Table: communication_profile
    conn.execute(sa.text("""
CREATE TABLE communication_profile (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	iolink_revision TEXT, 
	compatible_with TEXT, 
	bitrate TEXT, 
	min_cycle_time TEXT, 
	msequence_capability TEXT, 
	sio_supported INTEGER, 
	connection_type TEXT, 
	wire_config TEXT, connection_symbol VARCHAR(255), test_xsi_type VARCHAR(100), product_ref_id VARCHAR(255), connection_description_text_id VARCHAR(100), physics VARCHAR(50), uses_baudrate INTEGER DEFAULT '1', has_test_element INTEGER DEFAULT '0' NOT NULL, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_communication_profile_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: custom_datatype_record_item_single_values
    conn.execute(sa.text("""
CREATE TABLE custom_datatype_record_item_single_values (
	id INTEGER NOT NULL, 
	record_item_id INTEGER NOT NULL, 
	value VARCHAR(255), 
	name TEXT, 
	name_text_id VARCHAR(255), 
	xsi_type VARCHAR(100), xml_order INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_cdri_sv_record_item_id FOREIGN KEY(record_item_id) REFERENCES custom_datatype_record_items (id) ON DELETE CASCADE
)
    """))

    # Table: custom_datatype_record_items
    conn.execute(sa.text("""
CREATE TABLE custom_datatype_record_items (
	id INTEGER NOT NULL, 
	datatype_id INTEGER NOT NULL, 
	subindex INTEGER, 
	bit_offset INTEGER, 
	bit_length INTEGER, 
	datatype_ref TEXT, 
	name TEXT, name_text_id VARCHAR(255), description_text_id VARCHAR(255), min_value VARCHAR(255), max_value VARCHAR(255), value_range_xsi_type VARCHAR(255), access_right_restriction VARCHAR(50), fixed_length INTEGER, encoding VARCHAR(50), value_range_name_text_id TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_custom_datatype_record_items_datatype_id FOREIGN KEY(datatype_id) REFERENCES custom_datatypes (id) ON DELETE CASCADE
)
    """))

    # Table: custom_datatype_single_values
    conn.execute(sa.text("""
CREATE TABLE custom_datatype_single_values (
	id INTEGER NOT NULL, 
	datatype_id INTEGER NOT NULL, 
	value TEXT NOT NULL, 
	name TEXT, text_id VARCHAR(255), xsi_type VARCHAR(100), xml_order INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_custom_datatype_single_values_datatype_id FOREIGN KEY(datatype_id) REFERENCES custom_datatypes (id) ON DELETE CASCADE
)
    """))

    # Table: custom_datatypes
    conn.execute(sa.text("""
CREATE TABLE custom_datatypes (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	datatype_id TEXT NOT NULL, 
	datatype_xsi_type TEXT, 
	bit_length INTEGER, 
	subindex_access_supported INTEGER, value_range_lower TEXT, value_range_upper TEXT, value_range_xsi_type TEXT, value_range_name_text_id TEXT, min_value TEXT, max_value TEXT, string_fixed_length INTEGER, string_encoding VARCHAR(50), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_custom_datatypes_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))

    # Table: device_features
    conn.execute(sa.text("""
CREATE TABLE device_features (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	block_parameter INTEGER, 
	data_storage INTEGER, 
	profile_characteristic TEXT, 
	access_locks_data_storage INTEGER, 
	access_locks_local_parameterization INTEGER, 
	access_locks_local_user_interface INTEGER, 
	access_locks_parameter INTEGER, has_supported_access_locks INTEGER DEFAULT NULL, has_data_storage INTEGER DEFAULT '0', 
	PRIMARY KEY (id), 
	CONSTRAINT fk_device_features_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: device_test_config
    conn.execute(sa.text("""
CREATE TABLE device_test_config (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	config_type TEXT, 
	param_index INTEGER, 
	test_value TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_device_test_config_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))

    # Table: device_test_event_triggers
    conn.execute(sa.text("""
CREATE TABLE device_test_event_triggers (
	id INTEGER NOT NULL, 
	test_config_id INTEGER NOT NULL, 
	appear_value TEXT, 
	disappear_value TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_device_test_event_triggers_test_config_id FOREIGN KEY(test_config_id) REFERENCES device_test_config (id) ON DELETE CASCADE
)
    """))

    # Table: device_variants
    conn.execute(sa.text("""
CREATE TABLE device_variants (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	product_id TEXT NOT NULL, 
	device_symbol TEXT, 
	device_icon TEXT, 
	name TEXT, 
	description TEXT, name_text_id VARCHAR(255), description_text_id VARCHAR(255), product_name_text_id VARCHAR(255), product_text_text_id VARCHAR(255), has_name BOOLEAN, has_description BOOLEAN, has_product_name BOOLEAN, has_product_text BOOLEAN, hardware_revision VARCHAR(50), firmware_revision VARCHAR(50), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_device_variants_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))

    # Table: devices
    conn.execute(sa.text("""
CREATE TABLE devices (
	id INTEGER NOT NULL, 
	vendor_id INTEGER, 
	device_id INTEGER, 
	product_name TEXT, 
	manufacturer TEXT, 
	iodd_version TEXT, 
	import_date DATETIME, 
	checksum TEXT, vendor_logo_filename TEXT, device_name_text_id VARCHAR(255), vendor_text_text_id VARCHAR(255), vendor_url_text_id VARCHAR(255), device_family_text_id VARCHAR(255), has_error_type_collection INTEGER DEFAULT '0', device_id_str VARCHAR(50), additional_device_ids TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_devices_checksum UNIQUE (checksum)
)
    """))

    # Table: document_info
    conn.execute(sa.text("""
CREATE TABLE document_info (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	copyright TEXT, 
	release_date TEXT, 
	version TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_document_info_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: eds_assemblies
    conn.execute(sa.text("""
CREATE TABLE eds_assemblies (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER NOT NULL, 
	assembly_number INTEGER NOT NULL, 
	assembly_name TEXT, 
	assembly_type INTEGER, 
	unknown_field1 INTEGER, 
	size INTEGER, 
	unknown_field2 INTEGER, 
	path TEXT, 
	help_string TEXT, 
	is_variable BOOLEAN DEFAULT '0' NOT NULL, object_name TEXT, object_class_code INTEGER, revision INTEGER, max_instance INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_capacity
    conn.execute(sa.text("""
CREATE TABLE eds_capacity (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER, 
	max_msg_connections INTEGER, 
	max_io_producers INTEGER, 
	max_io_consumers INTEGER, 
	max_cx_per_config_tool INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_eds_capacity_eds_file_id FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE, 
	CONSTRAINT uq_eds_capacity_file_id UNIQUE (eds_file_id)
)
    """))

    # Table: eds_connections
    conn.execute(sa.text("""
CREATE TABLE eds_connections (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER, 
	connection_number INTEGER, 
	connection_name TEXT, 
	trigger_transport TEXT, 
	connection_params TEXT, 
	output_assembly TEXT, 
	input_assembly TEXT, 
	help_string TEXT, o_to_t_params TEXT, t_to_o_params TEXT, config_part1 TEXT, config_part2 TEXT, path TEXT, trigger_transport_comment TEXT, connection_params_comment TEXT, object_name TEXT, object_class_code INTEGER, revision INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_eds_connections_eds_file_id FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_diagnostics
    conn.execute(sa.text("""
CREATE TABLE eds_diagnostics (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER NOT NULL, 
	severity TEXT NOT NULL, 
	code TEXT NOT NULL, 
	message TEXT NOT NULL, 
	section TEXT, 
	line INTEGER, 
	"column" INTEGER, 
	context TEXT, 
	created_at TEXT NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_dlr_config
    conn.execute(sa.text("""
CREATE TABLE eds_dlr_config (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	revision INTEGER, 
	object_name TEXT, 
	object_class_code INTEGER, 
	network_topology INTEGER, 
	enable_switch BOOLEAN, 
	beacon_interval INTEGER, 
	beacon_timeout INTEGER, 
	vlan_id INTEGER, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, max_inst INTEGER, num_static_instances INTEGER, max_dynamic_instances INTEGER, additional_attributes JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_enum_values
    conn.execute(sa.text("""
CREATE TABLE eds_enum_values (
	id INTEGER NOT NULL, 
	parameter_id INTEGER NOT NULL, 
	enum_name TEXT NOT NULL, 
	enum_value INTEGER, 
	enum_display TEXT, 
	is_default BOOLEAN DEFAULT 0, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parameter_id) REFERENCES eds_parameters (id) ON DELETE CASCADE
)
    """))

    # Table: eds_ethernet_link
    conn.execute(sa.text("""
CREATE TABLE eds_ethernet_link (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	revision INTEGER, 
	object_name TEXT, 
	object_class_code INTEGER, 
	interface_speed INTEGER, 
	interface_flags INTEGER, 
	physical_address TEXT, 
	interface_label TEXT, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, max_inst INTEGER, num_static_instances INTEGER, max_dynamic_instances INTEGER, interface_labels JSON, additional_attributes JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_file_metadata
    conn.execute(sa.text("""
CREATE TABLE eds_file_metadata (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	home_url TEXT, 
	revision TEXT, 
	license_key TEXT, 
	icon_contents TEXT, 
	file_format INTEGER, 
	file_revision TEXT, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_files
    conn.execute(sa.text("""
CREATE TABLE eds_files (
	id INTEGER NOT NULL, 
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
	import_date DATETIME, 
	file_checksum TEXT, create_date TEXT, create_time TEXT, mod_date TEXT, mod_time TEXT, file_revision TEXT, class1 TEXT, class2 TEXT, class3 TEXT, class4 TEXT, package_id INTEGER, variant_type TEXT, version_folder TEXT, is_latest_version BOOLEAN, file_path_in_package TEXT, diagnostic_info_count INTEGER DEFAULT '0', diagnostic_warn_count INTEGER DEFAULT '0', diagnostic_error_count INTEGER DEFAULT '0', diagnostic_fatal_count INTEGER DEFAULT '0', has_parsing_issues BOOLEAN DEFAULT '0', icon TEXT, icon_contents_ref INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT uq_eds_files_checksum UNIQUE (file_checksum)
)
    """))

    # Table: eds_groups
    conn.execute(sa.text("""
CREATE TABLE eds_groups (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER NOT NULL, 
	group_number INTEGER NOT NULL, 
	group_name TEXT NOT NULL, 
	parameter_count INTEGER, 
	parameter_list TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_lldp_management
    conn.execute(sa.text("""
CREATE TABLE eds_lldp_management (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	revision INTEGER, 
	object_name TEXT, 
	object_class_code INTEGER, 
	msg_tx_interval INTEGER, 
	msg_tx_hold INTEGER, 
	chassis_id_subtype INTEGER, 
	chassis_id TEXT, 
	port_id_subtype INTEGER, 
	port_id TEXT, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, max_inst INTEGER, num_static_instances INTEGER, max_dynamic_instances INTEGER, additional_attributes JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_modules
    conn.execute(sa.text("""
CREATE TABLE eds_modules (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER NOT NULL, 
	module_number INTEGER NOT NULL, 
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
	PRIMARY KEY (id), 
	FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_object_metadata
    conn.execute(sa.text("""
CREATE TABLE eds_object_metadata (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	section_name TEXT NOT NULL, 
	object_name TEXT, 
	object_class_code INTEGER, 
	revision INTEGER, 
	additional_data TEXT, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_package_files
    conn.execute(sa.text("""
CREATE TABLE eds_package_files (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER,
                eds_file_id INTEGER,
                FOREIGN KEY (package_id) REFERENCES eds_packages (id),
                FOREIGN KEY (eds_file_id) REFERENCES eds_files (id)
            )
    """))

    # Table: eds_package_metadata
    conn.execute(sa.text("""
CREATE TABLE eds_package_metadata (
	id INTEGER NOT NULL, 
	package_id INTEGER NOT NULL, 
	file_path TEXT NOT NULL, 
	file_type TEXT, 
	content BLOB, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_eds_package_metadata_package_id FOREIGN KEY(package_id) REFERENCES eds_packages (id) ON DELETE CASCADE
)
    """))

    # Table: eds_packages
    conn.execute(sa.text("""
CREATE TABLE eds_packages (
	id INTEGER NOT NULL, 
	package_name TEXT NOT NULL, 
	package_checksum TEXT NOT NULL, 
	upload_date DATETIME NOT NULL, 
	readme_content TEXT, 
	total_eds_files INTEGER, 
	total_versions INTEGER, 
	vendor_name TEXT, 
	product_name TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (package_checksum)
)
    """))

    # Table: eds_parameters
    conn.execute(sa.text("""
CREATE TABLE eds_parameters (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER, 
	param_number INTEGER, 
	param_name TEXT, 
	param_type TEXT, 
	data_type INTEGER, 
	data_size INTEGER, 
	default_value TEXT, 
	min_value TEXT, 
	max_value TEXT, 
	description TEXT, link_path_size TEXT, link_path TEXT, descriptor TEXT, help_string_1 TEXT, help_string_2 TEXT, help_string_3 TEXT, enum_values TEXT, units TEXT, scaling_multiplier TEXT, scaling_divisor TEXT, scaling_base TEXT, scaling_offset TEXT, link_scaling_multiplier TEXT, link_scaling_divisor TEXT, link_scaling_base TEXT, link_scaling_offset TEXT, decimal_places INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_eds_parameters_eds_file_id FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_ports
    conn.execute(sa.text("""
CREATE TABLE eds_ports (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER, 
	port_number INTEGER, 
	port_type TEXT, 
	port_name TEXT, 
	port_path TEXT, 
	link_number INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_eds_ports_eds_file_id FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_qos_config
    conn.execute(sa.text("""
CREATE TABLE eds_qos_config (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	revision INTEGER, 
	object_name TEXT, 
	object_class_code INTEGER, 
	qos_tag_enable BOOLEAN, 
	dscp_urgent INTEGER, 
	dscp_scheduled INTEGER, 
	dscp_high INTEGER, 
	dscp_low INTEGER, 
	dscp_explicit INTEGER, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, max_inst INTEGER, num_static_instances INTEGER, max_dynamic_instances INTEGER, additional_attributes JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_tcpip_interface
    conn.execute(sa.text("""
CREATE TABLE eds_tcpip_interface (
	id INTEGER NOT NULL, 
	file_id INTEGER NOT NULL, 
	revision INTEGER, 
	object_name TEXT, 
	object_class_code INTEGER, 
	interface_config INTEGER, 
	host_name TEXT, 
	ttl_value INTEGER, 
	mcast_config INTEGER, 
	select_acd BOOLEAN, 
	encap_timeout INTEGER, 
	created_at TEXT DEFAULT CURRENT_TIMESTAMP, max_inst INTEGER, num_static_instances INTEGER, max_dynamic_instances INTEGER, additional_attributes JSON, 
	PRIMARY KEY (id), 
	FOREIGN KEY(file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_tspecs
    conn.execute(sa.text("""
CREATE TABLE eds_tspecs (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER, 
	tspec_name TEXT, 
	direction TEXT, 
	data_size INTEGER, 
	rate INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_eds_tspecs_eds_file_id FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: eds_variable_assemblies
    conn.execute(sa.text("""
CREATE TABLE eds_variable_assemblies (
	id INTEGER NOT NULL, 
	eds_file_id INTEGER NOT NULL, 
	assembly_name TEXT NOT NULL, 
	assembly_number INTEGER NOT NULL, 
	unknown_value1 INTEGER, 
	max_size INTEGER, 
	description TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(eds_file_id) REFERENCES eds_files (id) ON DELETE CASCADE
)
    """))

    # Table: error_types
    conn.execute(sa.text("""
CREATE TABLE error_types (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                code INTEGER,
                additional_code INTEGER,
                name TEXT,
                description TEXT, has_code_attr BOOLEAN DEFAULT 1, xml_order INTEGER, is_custom BOOLEAN, name_text_id VARCHAR(255), description_text_id VARCHAR(255),
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
    """))

    # Table: events
    conn.execute(sa.text("""
CREATE TABLE events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                code INTEGER,
                name TEXT,
                description TEXT,
                event_type TEXT, name_text_id VARCHAR(255), description_text_id VARCHAR(255), order_index INTEGER, mode VARCHAR(100),
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
    """))

    # Table: generated_adapters
    conn.execute(sa.text("""
CREATE TABLE generated_adapters (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	target_platform TEXT, 
	version TEXT, 
	generated_date DATETIME, 
	code_content TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_generated_adapters_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: iodd_assets
    conn.execute(sa.text("""
CREATE TABLE iodd_assets (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	file_name TEXT NOT NULL, 
	file_type TEXT, 
	file_content BLOB NOT NULL, 
	file_path TEXT, 
	image_purpose TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_iodd_assets_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: iodd_build_format
    conn.execute(sa.text("""
CREATE TABLE iodd_build_format (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	indent_char VARCHAR(10) NOT NULL, 
	indent_size INTEGER NOT NULL, 
	xml_declaration TEXT, 
	namespace_prefix VARCHAR(50), 
	schema_location TEXT, 
	newline_style VARCHAR(10) NOT NULL, 
	has_trailing_newline BOOLEAN NOT NULL, 
	attribute_quoting VARCHAR(10) NOT NULL, 
	extracted_at DATETIME, 
	PRIMARY KEY (id), 
	UNIQUE (device_id), 
	FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))

    # Table: iodd_files
    conn.execute(sa.text("""
CREATE TABLE iodd_files (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	file_name TEXT, 
	xml_content TEXT, 
	schema_version TEXT, stamp_crc TEXT, checker_name TEXT, checker_version TEXT, profile_identification VARCHAR(255), profile_revision VARCHAR(50), profile_name VARCHAR(255), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_iodd_files_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: iodd_text
    conn.execute(sa.text("""
CREATE TABLE iodd_text (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	text_id TEXT NOT NULL, 
	language_code TEXT NOT NULL, 
	text_value TEXT NOT NULL, text_category TEXT, context TEXT, xml_order INTEGER, language_order INTEGER, is_text_redefine INTEGER DEFAULT '0', 
	PRIMARY KEY (id), 
	CONSTRAINT fk_iodd_text_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE, 
	CONSTRAINT uq_device_text_language UNIQUE (device_id, text_id, language_code)
)
    """))

    # Table: parameter_record_items
    conn.execute(sa.text("""
CREATE TABLE parameter_record_items (
	id INTEGER NOT NULL, 
	parameter_id INTEGER NOT NULL, 
	subindex INTEGER NOT NULL, 
	bit_offset INTEGER, 
	bit_length INTEGER, 
	datatype_ref VARCHAR(100), 
	simple_datatype VARCHAR(50), 
	name TEXT, 
	name_text_id VARCHAR(255), 
	description TEXT, 
	description_text_id VARCHAR(255), 
	default_value TEXT, 
	order_index INTEGER NOT NULL, min_value VARCHAR(255), max_value VARCHAR(255), value_range_xsi_type VARCHAR(255), access_right_restriction VARCHAR(50), fixed_length INTEGER, encoding VARCHAR(50), datatype_id VARCHAR(100), value_range_name_text_id TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parameter_id) REFERENCES parameters (id) ON DELETE CASCADE
)
    """))

    # Table: parameter_single_values
    conn.execute(sa.text("""
CREATE TABLE parameter_single_values (
	id INTEGER NOT NULL, 
	parameter_id INTEGER NOT NULL, 
	value TEXT NOT NULL, 
	name TEXT, 
	text_id VARCHAR(255), 
	xsi_type VARCHAR(100), 
	order_index INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parameter_id) REFERENCES parameters (id) ON DELETE CASCADE
)
    """))

    # Table: parameters
    conn.execute(sa.text("""
CREATE TABLE "parameters" (
	id INTEGER NOT NULL, 
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
	is_array INTEGER, 
	array_count INTEGER, 
	array_element_type TEXT, 
	string_encoding TEXT, 
	string_fixed_length INTEGER, 
	subindex_access_supported INTEGER, 
	unit_code TEXT, 
	value_range_name TEXT, 
	single_values TEXT, 
	variable_id TEXT, 
	array_element_bit_length INTEGER, 
	array_element_fixed_length INTEGER, 
	name_text_id VARCHAR(255), 
	description_text_id VARCHAR(255), 
	datatype_ref VARCHAR(100), 
	value_range_xsi_type VARCHAR(50), 
	value_range_name_text_id VARCHAR(100), 
	dynamic INTEGER, 
	excluded_from_data_storage INTEGER, 
	modifies_other_variables INTEGER, xml_order INTEGER, array_element_min_value TEXT, array_element_max_value TEXT, array_element_value_range_xsi_type TEXT, array_element_value_range_name_text_id TEXT, array_element_value_range_lower TEXT, array_element_value_range_upper TEXT, datatype_name_text_id VARCHAR(255), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_parameters_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: pqa_analysis_queue
    conn.execute(sa.text("""
CREATE TABLE pqa_analysis_queue (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	archive_id INTEGER NOT NULL, 
	status TEXT NOT NULL, 
	priority INTEGER, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	started_at DATETIME, 
	completed_at DATETIME, 
	error_message TEXT, 
	metric_id INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_pqa_queue_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE, 
	CONSTRAINT fk_pqa_queue_archive_id FOREIGN KEY(archive_id) REFERENCES pqa_file_archive (id) ON DELETE CASCADE, 
	CONSTRAINT fk_pqa_queue_metric_id FOREIGN KEY(metric_id) REFERENCES pqa_quality_metrics (id) ON DELETE SET NULL
)
    """))

    # Table: pqa_diff_details
    conn.execute(sa.text("""
CREATE TABLE pqa_diff_details (
	id INTEGER NOT NULL, 
	metric_id INTEGER NOT NULL, 
	diff_type TEXT NOT NULL, 
	severity TEXT NOT NULL, 
	xpath TEXT NOT NULL, 
	expected_value TEXT, 
	actual_value TEXT, 
	description TEXT, 
	phase TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_pqa_diff_metric_id FOREIGN KEY(metric_id) REFERENCES pqa_quality_metrics (id) ON DELETE CASCADE
)
    """))

    # Table: pqa_file_archive
    conn.execute(sa.text("""
CREATE TABLE pqa_file_archive (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	file_type TEXT NOT NULL, 
	filename TEXT NOT NULL, 
	file_hash TEXT NOT NULL, 
	file_content BLOB NOT NULL, 
	file_size INTEGER NOT NULL, 
	upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
	parser_version TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_pqa_archive_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))

    # Table: pqa_quality_metrics
    conn.execute(sa.text("""
CREATE TABLE pqa_quality_metrics (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	archive_id INTEGER NOT NULL, 
	analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP, 
	overall_score FLOAT NOT NULL, 
	structural_score FLOAT NOT NULL, 
	attribute_score FLOAT NOT NULL, 
	value_score FLOAT NOT NULL, 
	total_elements_original INTEGER, 
	total_elements_reconstructed INTEGER, 
	missing_elements INTEGER, 
	extra_elements INTEGER, 
	total_attributes_original INTEGER, 
	total_attributes_reconstructed INTEGER, 
	missing_attributes INTEGER, 
	incorrect_attributes INTEGER, 
	data_loss_percentage FLOAT, 
	critical_data_loss BOOLEAN, 
	phase1_score FLOAT, 
	phase2_score FLOAT, 
	phase3_score FLOAT, 
	phase4_score FLOAT, 
	phase5_score FLOAT, 
	reconstruction_time_ms INTEGER, 
	comparison_time_ms INTEGER, 
	passed_threshold BOOLEAN, 
	requires_review BOOLEAN, 
	ticket_generated BOOLEAN, file_type TEXT, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_pqa_metrics_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE, 
	CONSTRAINT fk_pqa_metrics_archive_id FOREIGN KEY(archive_id) REFERENCES pqa_file_archive (id) ON DELETE CASCADE
)
    """))

    # Table: pqa_thresholds
    conn.execute(sa.text("""
CREATE TABLE pqa_thresholds (
	id INTEGER NOT NULL, 
	threshold_name TEXT NOT NULL, 
	description TEXT, 
	min_overall_score FLOAT, 
	min_structural_score FLOAT, 
	min_attribute_score FLOAT, 
	min_value_score FLOAT, 
	max_data_loss_percentage FLOAT, 
	allow_critical_data_loss BOOLEAN, 
	min_phase1_score FLOAT, 
	min_phase2_score FLOAT, 
	min_phase3_score FLOAT, 
	min_phase4_score FLOAT, 
	min_phase5_score FLOAT, 
	auto_ticket_on_fail BOOLEAN, 
	auto_analysis_on_import BOOLEAN, 
	email_notifications BOOLEAN, 
	active BOOLEAN, 
	created_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	updated_at DATETIME DEFAULT CURRENT_TIMESTAMP, 
	PRIMARY KEY (id), 
	UNIQUE (threshold_name)
)
    """))

    # Table: process_data
    conn.execute(sa.text("""
CREATE TABLE process_data (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                device_id INTEGER,
                pd_id TEXT,
                name TEXT,
                direction TEXT,
                bit_length INTEGER,
                data_type TEXT,
                description TEXT, name_text_id VARCHAR(255), subindex_access_supported BOOLEAN, wrapper_id VARCHAR(255), uses_datatype_ref INTEGER DEFAULT '0', datatype_ref_id VARCHAR(100), datatype_name_text_id TEXT, datatype_has_bit_length INTEGER DEFAULT '0' NOT NULL,
                FOREIGN KEY (device_id) REFERENCES devices (id)
            )
    """))

    # Table: process_data_conditions
    conn.execute(sa.text("""
CREATE TABLE process_data_conditions (
	id INTEGER NOT NULL, 
	process_data_id INTEGER NOT NULL, 
	condition_variable_id TEXT NOT NULL, 
	condition_value TEXT NOT NULL, condition_subindex VARCHAR(50), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_process_data_conditions_process_data_id FOREIGN KEY(process_data_id) REFERENCES process_data (id) ON DELETE CASCADE
)
    """))

    # Table: process_data_record_items
    conn.execute(sa.text("""
CREATE TABLE process_data_record_items (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                process_data_id INTEGER,
                subindex INTEGER,
                name TEXT,
                bit_offset INTEGER,
                bit_length INTEGER,
                data_type TEXT,
                default_value TEXT, name_text_id VARCHAR(255), description_text_id VARCHAR(255), min_value VARCHAR(255), max_value VARCHAR(255), value_range_xsi_type VARCHAR(255), access_right_restriction VARCHAR(50), fixed_length INTEGER, encoding VARCHAR(50), datatype_id VARCHAR(100), value_range_name_text_id TEXT,
                FOREIGN KEY (process_data_id) REFERENCES process_data (id)
            )
    """))

    # Table: process_data_single_values
    conn.execute(sa.text("""
CREATE TABLE process_data_single_values (
	id INTEGER NOT NULL, 
	record_item_id INTEGER, 
	value TEXT, 
	name TEXT, 
	description TEXT, name_text_id VARCHAR(255), xsi_type VARCHAR(100), process_data_id INTEGER, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_single_values_record_item_id FOREIGN KEY(record_item_id) REFERENCES process_data_record_items (id)
)
    """))

    # Table: process_data_ui_info
    conn.execute(sa.text("""
CREATE TABLE process_data_ui_info (
	id INTEGER NOT NULL, 
	process_data_id INTEGER NOT NULL, 
	subindex INTEGER NOT NULL, 
	gradient FLOAT, 
	"offset" FLOAT, 
	unit_code TEXT, 
	display_format TEXT, xml_order INTEGER, pd_ref_order INTEGER, gradient_str VARCHAR(50), offset_str VARCHAR(50), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_process_data_ui_info_process_data_id FOREIGN KEY(process_data_id) REFERENCES process_data (id) ON DELETE CASCADE
)
    """))

    # Table: record_item_single_values
    conn.execute(sa.text("""
CREATE TABLE record_item_single_values (
	id INTEGER NOT NULL, 
	record_item_id INTEGER NOT NULL, 
	value VARCHAR(255) NOT NULL, 
	name TEXT, 
	name_text_id VARCHAR(255), 
	order_index INTEGER NOT NULL, xsi_type VARCHAR(100), 
	PRIMARY KEY (id), 
	FOREIGN KEY(record_item_id) REFERENCES parameter_record_items (id) ON DELETE CASCADE
)
    """))

    # Table: std_record_item_ref_single_values
    conn.execute(sa.text("""
CREATE TABLE std_record_item_ref_single_values (
	id INTEGER NOT NULL, 
	std_record_item_ref_id INTEGER NOT NULL, 
	value TEXT NOT NULL, 
	name_text_id TEXT, 
	is_std_ref INTEGER NOT NULL, 
	order_index INTEGER, 
	PRIMARY KEY (id)
)
    """))

    # Table: std_record_item_refs
    conn.execute(sa.text("""
CREATE TABLE std_record_item_refs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        std_variable_ref_id INTEGER NOT NULL,
        subindex INTEGER NOT NULL,
        default_value TEXT,
        order_index INTEGER DEFAULT 0,
        FOREIGN KEY (std_variable_ref_id) REFERENCES std_variable_refs(id) ON DELETE CASCADE
    )
    """))

    # Table: std_variable_ref_single_values
    conn.execute(sa.text("""
CREATE TABLE std_variable_ref_single_values (
	id INTEGER NOT NULL, 
	std_variable_ref_id INTEGER NOT NULL, 
	value VARCHAR(255) NOT NULL, 
	name_text_id VARCHAR(255), 
	is_std_ref BOOLEAN NOT NULL, 
	order_index INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(std_variable_ref_id) REFERENCES std_variable_refs (id) ON DELETE CASCADE
)
    """))

    # Table: std_variable_refs
    conn.execute(sa.text("""
CREATE TABLE std_variable_refs (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	variable_id VARCHAR(100) NOT NULL, 
	default_value TEXT, 
	fixed_length_restriction INTEGER, 
	excluded_from_data_storage BOOLEAN, 
	order_index INTEGER NOT NULL, 
	PRIMARY KEY (id), 
	FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))

    # Table: ticket_attachments
    conn.execute(sa.text("""
CREATE TABLE ticket_attachments (
	id INTEGER NOT NULL, 
	ticket_id INTEGER NOT NULL, 
	filename TEXT NOT NULL, 
	file_path TEXT NOT NULL, 
	file_size INTEGER, 
	content_type TEXT, 
	uploaded_at TEXT NOT NULL, 
	uploaded_by TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ticket_id) REFERENCES tickets (id) ON DELETE CASCADE
)
    """))

    # Table: ticket_comments
    conn.execute(sa.text("""
CREATE TABLE ticket_comments (
	id INTEGER NOT NULL, 
	ticket_id INTEGER NOT NULL, 
	comment_text TEXT NOT NULL, 
	created_at TEXT NOT NULL, 
	created_by TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(ticket_id) REFERENCES tickets (id) ON DELETE CASCADE
)
    """))

    # Table: tickets
    conn.execute(sa.text("""
CREATE TABLE tickets (
	id INTEGER NOT NULL, 
	ticket_number TEXT NOT NULL, 
	device_type TEXT NOT NULL, 
	device_id INTEGER, 
	device_name TEXT, 
	vendor_name TEXT, 
	product_code INTEGER, 
	title TEXT NOT NULL, 
	description TEXT, 
	eds_reference TEXT, 
	status TEXT NOT NULL, 
	priority TEXT NOT NULL, 
	category TEXT, 
	created_at TEXT NOT NULL, 
	updated_at TEXT NOT NULL, 
	resolved_at TEXT, 
	created_by TEXT, 
	assigned_to TEXT, 
	PRIMARY KEY (id), 
	UNIQUE (ticket_number)
)
    """))

    # Table: ui_menu_buttons
    conn.execute(sa.text("""
CREATE TABLE ui_menu_buttons (
	id INTEGER NOT NULL, 
	menu_item_id INTEGER NOT NULL, 
	button_value TEXT NOT NULL, 
	description TEXT, 
	action_started_message TEXT, description_text_id VARCHAR(100), action_started_message_text_id VARCHAR(100), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_ui_menu_buttons_menu_item_id FOREIGN KEY(menu_item_id) REFERENCES ui_menu_items (id) ON DELETE CASCADE
)
    """))

    # Table: ui_menu_items
    conn.execute(sa.text("""
CREATE TABLE ui_menu_items (
	id INTEGER NOT NULL, 
	menu_id INTEGER, 
	variable_id TEXT, 
	record_item_ref TEXT, 
	subindex INTEGER, 
	access_right_restriction TEXT, 
	display_format TEXT, 
	unit_code TEXT, 
	button_value TEXT, 
	menu_ref TEXT, 
	item_order INTEGER, gradient FLOAT, "offset" FLOAT, condition_variable_id VARCHAR(255), condition_value VARCHAR(255), gradient_str VARCHAR(50), offset_str VARCHAR(50), condition_subindex VARCHAR(50), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_ui_menu_items_menu_id FOREIGN KEY(menu_id) REFERENCES ui_menus (id)
)
    """))

    # Table: ui_menu_roles
    conn.execute(sa.text("""
CREATE TABLE ui_menu_roles (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	role_type TEXT, 
	menu_type TEXT, 
	menu_id TEXT, has_xsi_type INTEGER DEFAULT 0, 
	PRIMARY KEY (id), 
	CONSTRAINT fk_ui_menu_roles_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: ui_menus
    conn.execute(sa.text("""
CREATE TABLE ui_menus (
	id INTEGER NOT NULL, 
	device_id INTEGER, 
	menu_id TEXT, 
	name TEXT, name_text_id VARCHAR(255), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_ui_menus_device_id FOREIGN KEY(device_id) REFERENCES devices (id)
)
    """))

    # Table: user_themes
    conn.execute(sa.text("""
CREATE TABLE user_themes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            preset_id TEXT,
            is_active BOOLEAN DEFAULT 0,
            theme_data TEXT NOT NULL,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    """))

    # Table: variable_record_item_info
    conn.execute(sa.text("""
CREATE TABLE "variable_record_item_info" (
	id INTEGER NOT NULL, 
	parameter_id INTEGER NOT NULL, 
	subindex INTEGER NOT NULL, 
	default_value TEXT, 
	order_index INTEGER NOT NULL, 
	excluded_from_data_storage INTEGER, 
	modifies_other_variables INTEGER, 
	PRIMARY KEY (id), 
	FOREIGN KEY(parameter_id) REFERENCES parameters (id) ON DELETE CASCADE
)
    """))

    # Table: wire_configurations
    conn.execute(sa.text("""
CREATE TABLE wire_configurations (
	id INTEGER NOT NULL, 
	device_id INTEGER NOT NULL, 
	connection_type TEXT, 
	wire_number INTEGER, 
	wire_color TEXT, 
	wire_function TEXT, 
	wire_description TEXT, connection_symbol VARCHAR(255), name_text_id VARCHAR(255), xsi_type VARCHAR(50), 
	PRIMARY KEY (id), 
	CONSTRAINT fk_wire_configurations_device_id FOREIGN KEY(device_id) REFERENCES devices (id) ON DELETE CASCADE
)
    """))


    # Create indexes
    conn.execute(sa.text("""CREATE INDEX idx_cdri_sv_record_item_id ON custom_datatype_record_item_single_values (record_item_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_custom_datatype_record_items_datatype_id ON custom_datatype_record_items (datatype_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_custom_datatype_single_values_datatype_id ON custom_datatype_single_values (datatype_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_custom_datatypes_device_id ON custom_datatypes (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_custom_datatypes_datatype_id ON custom_datatypes (datatype_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_device_test_config_device_id ON device_test_config (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_device_test_event_triggers_test_config_id ON device_test_event_triggers (test_config_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_device_variants_device_id ON device_variants (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_device_variants_product_id ON device_variants (product_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_devices_vendor_id ON devices (vendor_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_devices_device_id ON devices (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_devices_vendor_id ON devices(vendor_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_devices_device_id ON devices(device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_devices_product_name ON devices(product_name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_devices_manufacturer ON devices(manufacturer)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_assemblies_eds_file_id ON eds_assemblies (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_assemblies_number ON eds_assemblies (assembly_number)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_assemblies_assembly_number ON eds_assemblies(assembly_number)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_assemblies_assembly_name ON eds_assemblies(assembly_name)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_capacity_eds_file_id ON eds_capacity (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_capacity_eds_file_id ON eds_capacity(eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_connections_eds_file_id ON eds_connections (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_connections_eds_file_id ON eds_connections(eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_connections_connection_number ON eds_connections(connection_number)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_diagnostics_eds_file_id ON eds_diagnostics (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_diagnostics_severity ON eds_diagnostics (severity)"""))
    conn.execute(sa.text("""CREATE INDEX idx_dlr_file ON eds_dlr_config (file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_enum_param ON eds_enum_values (parameter_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_enum_name ON eds_enum_values (enum_name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_ethernet_file ON eds_ethernet_link (file_id)"""))
    conn.execute(sa.text("""CREATE UNIQUE INDEX idx_file_meta ON eds_file_metadata (file_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_files_vendor_code ON eds_files (vendor_code)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_files_product_code ON eds_files (product_code)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_files_vendor_name ON eds_files (vendor_name)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_files_package_id ON eds_files (package_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_files_variant_type ON eds_files (variant_type)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_files_is_latest_version ON eds_files (is_latest_version)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_files_vendor_name ON eds_files(vendor_name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_files_product_name ON eds_files(product_name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_files_vendor_code ON eds_files(vendor_code)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_files_product_code ON eds_files(product_code)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_groups_eds_file_id ON eds_groups (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_lldp_file ON eds_lldp_management (file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_modules_eds_file_id ON eds_modules (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_obj_meta_file ON eds_object_metadata (file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_obj_meta_section ON eds_object_metadata (section_name)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_package_metadata_package_id ON eds_package_metadata (package_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_packages_package_name ON eds_packages (package_name)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_parameters_eds_file_id ON eds_parameters (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_parameters_eds_file_id ON eds_parameters(eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_parameters_param_name ON eds_parameters(param_name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_parameters_param_number ON eds_parameters(param_number)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_parameters_data_type ON eds_parameters(data_type)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_parameters_eds_file_id_param_number ON eds_parameters(eds_file_id, param_number)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_ports_eds_file_id ON eds_ports (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_ports_eds_file_id ON eds_ports(eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_qos_file ON eds_qos_config (file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tcpip_file ON eds_tcpip_interface (file_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_eds_tspecs_eds_file_id ON eds_tspecs (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_variable_assemblies_eds_file_id ON eds_variable_assemblies (eds_file_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_eds_variable_assemblies_number ON eds_variable_assemblies (assembly_number)"""))
    conn.execute(sa.text("""CREATE INDEX ix_generated_adapters_device_id ON generated_adapters (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_generated_adapters_platform ON generated_adapters (target_platform)"""))
    conn.execute(sa.text("""CREATE INDEX ix_iodd_assets_device_id ON iodd_assets (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_iodd_assets_file_type ON iodd_assets (file_type)"""))
    conn.execute(sa.text("""CREATE INDEX ix_iodd_assets_image_purpose ON iodd_assets (image_purpose)"""))
    conn.execute(sa.text("""CREATE INDEX ix_iodd_build_format_device_id ON iodd_build_format (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_iodd_files_device_id ON iodd_files(device_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_iodd_files_device_id
        ON iodd_files (device_id)
    """))
    conn.execute(sa.text("""CREATE INDEX idx_iodd_text_device_language ON iodd_text (device_id, language_code)"""))
    conn.execute(sa.text("""CREATE INDEX idx_iodd_text_text_id ON iodd_text (text_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_iodd_text_device_id ON iodd_text (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_parameter_record_items_parameter_id ON parameter_record_items (parameter_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_parameter_single_values_parameter_id ON parameter_single_values (parameter_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_parameters_access_rights ON parameters (access_rights)"""))
    conn.execute(sa.text("""CREATE INDEX idx_parameters_device_id ON parameters (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_parameters_device_id_name ON parameters (device_id, name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_parameters_param_index ON parameters (param_index)"""))
    conn.execute(sa.text("""CREATE INDEX idx_parameters_data_type ON parameters (data_type)"""))
    conn.execute(sa.text("""CREATE INDEX ix_parameters_device_id ON parameters (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_parameters_name ON parameters (name)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_queue_status ON pqa_analysis_queue (status)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_queue_priority ON pqa_analysis_queue (priority)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_queue_device ON pqa_analysis_queue (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_diff_metric ON pqa_diff_details (metric_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_diff_severity ON pqa_diff_details (severity)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_diff_type ON pqa_diff_details (diff_type)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_diff_phase ON pqa_diff_details (phase)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_archive_device ON pqa_file_archive (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_archive_hash ON pqa_file_archive (file_hash)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_archive_timestamp ON pqa_file_archive (upload_timestamp)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_metrics_device ON pqa_quality_metrics (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_metrics_archive ON pqa_quality_metrics (archive_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_metrics_timestamp ON pqa_quality_metrics (analysis_timestamp)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_metrics_score ON pqa_quality_metrics (overall_score)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_metrics_passed ON pqa_quality_metrics (passed_threshold)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_metrics_file_type ON pqa_quality_metrics (file_type)"""))
    conn.execute(sa.text("""CREATE INDEX idx_pqa_threshold_active ON pqa_thresholds (active)"""))
    conn.execute(sa.text("""CREATE INDEX idx_process_data_conditions_process_data_id ON process_data_conditions (process_data_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_process_data_conditions_variable_id ON process_data_conditions (condition_variable_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_process_data_ui_info_process_data_id ON process_data_ui_info (process_data_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_ri_sv_record_item_id ON record_item_single_values (record_item_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_std_var_ref_sv_ref_id ON std_variable_ref_single_values (std_variable_ref_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_std_variable_refs_device_id ON std_variable_refs (device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_ticket_attachments_ticket_id ON ticket_attachments(ticket_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_ticket_comments_ticket_id ON ticket_comments(ticket_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_status ON tickets(status)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_priority ON tickets(priority)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_device_type ON tickets(device_type)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_category ON tickets(category)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_created_at ON tickets(created_at)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_status_priority ON tickets(status, priority)"""))
    conn.execute(sa.text("""CREATE INDEX idx_tickets_device_type_device_id ON tickets(device_type, device_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_ui_menu_buttons_menu_item_id ON ui_menu_buttons (menu_item_id)"""))
    conn.execute(sa.text("""CREATE INDEX ix_variable_record_item_info_parameter_id ON variable_record_item_info (parameter_id)"""))
    conn.execute(sa.text("""CREATE INDEX idx_wire_configurations_device_id ON wire_configurations (device_id)"""))


def downgrade():
    """Drop all tables"""
    conn = op.get_bind()

    conn.execute(sa.text("DROP TABLE IF EXISTS wire_configurations"))
    conn.execute(sa.text("DROP TABLE IF EXISTS variable_record_item_info"))
    conn.execute(sa.text("DROP TABLE IF EXISTS user_themes"))
    conn.execute(sa.text("DROP TABLE IF EXISTS ui_menus"))
    conn.execute(sa.text("DROP TABLE IF EXISTS ui_menu_roles"))
    conn.execute(sa.text("DROP TABLE IF EXISTS ui_menu_items"))
    conn.execute(sa.text("DROP TABLE IF EXISTS ui_menu_buttons"))
    conn.execute(sa.text("DROP TABLE IF EXISTS tickets"))
    conn.execute(sa.text("DROP TABLE IF EXISTS ticket_comments"))
    conn.execute(sa.text("DROP TABLE IF EXISTS ticket_attachments"))
    conn.execute(sa.text("DROP TABLE IF EXISTS std_variable_refs"))
    conn.execute(sa.text("DROP TABLE IF EXISTS std_variable_ref_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS std_record_item_refs"))
    conn.execute(sa.text("DROP TABLE IF EXISTS std_record_item_ref_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS record_item_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS process_data_ui_info"))
    conn.execute(sa.text("DROP TABLE IF EXISTS process_data_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS process_data_record_items"))
    conn.execute(sa.text("DROP TABLE IF EXISTS process_data_conditions"))
    conn.execute(sa.text("DROP TABLE IF EXISTS process_data"))
    conn.execute(sa.text("DROP TABLE IF EXISTS pqa_thresholds"))
    conn.execute(sa.text("DROP TABLE IF EXISTS pqa_quality_metrics"))
    conn.execute(sa.text("DROP TABLE IF EXISTS pqa_file_archive"))
    conn.execute(sa.text("DROP TABLE IF EXISTS pqa_diff_details"))
    conn.execute(sa.text("DROP TABLE IF EXISTS pqa_analysis_queue"))
    conn.execute(sa.text("DROP TABLE IF EXISTS parameters"))
    conn.execute(sa.text("DROP TABLE IF EXISTS parameter_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS parameter_record_items"))
    conn.execute(sa.text("DROP TABLE IF EXISTS iodd_text"))
    conn.execute(sa.text("DROP TABLE IF EXISTS iodd_files"))
    conn.execute(sa.text("DROP TABLE IF EXISTS iodd_build_format"))
    conn.execute(sa.text("DROP TABLE IF EXISTS iodd_assets"))
    conn.execute(sa.text("DROP TABLE IF EXISTS generated_adapters"))
    conn.execute(sa.text("DROP TABLE IF EXISTS events"))
    conn.execute(sa.text("DROP TABLE IF EXISTS error_types"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_variable_assemblies"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_tspecs"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_tcpip_interface"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_qos_config"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_ports"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_parameters"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_packages"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_package_metadata"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_package_files"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_object_metadata"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_modules"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_lldp_management"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_groups"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_files"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_file_metadata"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_ethernet_link"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_enum_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_dlr_config"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_diagnostics"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_connections"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_capacity"))
    conn.execute(sa.text("DROP TABLE IF EXISTS eds_assemblies"))
    conn.execute(sa.text("DROP TABLE IF EXISTS document_info"))
    conn.execute(sa.text("DROP TABLE IF EXISTS devices"))
    conn.execute(sa.text("DROP TABLE IF EXISTS device_variants"))
    conn.execute(sa.text("DROP TABLE IF EXISTS device_test_event_triggers"))
    conn.execute(sa.text("DROP TABLE IF EXISTS device_test_config"))
    conn.execute(sa.text("DROP TABLE IF EXISTS device_features"))
    conn.execute(sa.text("DROP TABLE IF EXISTS custom_datatypes"))
    conn.execute(sa.text("DROP TABLE IF EXISTS custom_datatype_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS custom_datatype_record_items"))
    conn.execute(sa.text("DROP TABLE IF EXISTS custom_datatype_record_item_single_values"))
    conn.execute(sa.text("DROP TABLE IF EXISTS communication_profile"))

