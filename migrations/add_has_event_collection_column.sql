-- Migration: Add has_event_collection column to devices table
-- Date: 2025-11-26
-- Purpose: Track if original IODD had EventCollection element (even if empty)
-- Related to: PQA Fix #3 - Empty EventCollection tracking

-- Add column with default value FALSE
ALTER TABLE devices ADD COLUMN has_event_collection INTEGER DEFAULT 0;

-- Update comment: This column tracks whether the original IODD XML contained
-- an <EventCollection> element, even if it was empty. This allows the
-- reconstructor to output empty EventCollection elements when appropriate.
