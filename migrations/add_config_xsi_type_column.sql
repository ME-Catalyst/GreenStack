-- Migration: Add config_xsi_type column to device_test_config table
-- Date: 2025-11-26
-- Purpose: Track xsi:type attribute for Config7 test configurations
-- Related to: PQA Fix #4 - Config7 xsi:type attribute

-- Add column with default value NULL
ALTER TABLE device_test_config ADD COLUMN config_xsi_type TEXT;

-- Update comment: This column stores the xsi:type attribute for test configurations
-- (e.g., "IOLinkTestConfig7T" for Config7 elements). This allows the reconstructor
-- to output the correct xsi:type attribute for test configurations.
