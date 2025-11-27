-- PQA Fix #6B: Add ArrayT SimpleDatatype columns to process_data table
-- These store the SimpleDatatype child element attributes for ArrayT process data

ALTER TABLE process_data ADD COLUMN array_element_type TEXT;
ALTER TABLE process_data ADD COLUMN array_element_bit_length INTEGER;
ALTER TABLE process_data ADD COLUMN array_element_fixed_length INTEGER;
ALTER TABLE process_data ADD COLUMN array_element_min_value TEXT;
ALTER TABLE process_data ADD COLUMN array_element_max_value TEXT;
ALTER TABLE process_data ADD COLUMN array_element_value_range_xsi_type TEXT;
ALTER TABLE process_data ADD COLUMN array_element_value_range_name_text_id TEXT;
