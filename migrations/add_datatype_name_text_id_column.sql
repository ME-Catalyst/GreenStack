-- Migration: Add datatype_name_text_id column to custom_datatypes table
-- Date: 2025-11-26
-- Purpose: Track Name child element textId for custom Datatype definitions
-- Related to: PQA Fix #6A - Datatype/Name child elements

-- Add column with default value NULL
ALTER TABLE custom_datatypes ADD COLUMN datatype_name_text_id TEXT;

-- Update comment: This column stores the textId for Name child elements inside
-- custom Datatype definitions. This allows the reconstructor to output
-- <Name textId="..."/> child elements when present in the original IODD.
