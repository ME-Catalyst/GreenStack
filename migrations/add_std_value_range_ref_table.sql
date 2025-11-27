-- PQA Fix #5: Add table for StdValueRangeRef elements
-- These are value range children of StdVariableRef elements

CREATE TABLE IF NOT EXISTS std_variable_ref_value_ranges (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    std_variable_ref_id INTEGER NOT NULL,
    lower_value TEXT NOT NULL,
    upper_value TEXT NOT NULL,
    is_std_ref INTEGER NOT NULL DEFAULT 1,  -- 1 for StdValueRangeRef, 0 for ValueRange
    order_index INTEGER NOT NULL DEFAULT 0,
    FOREIGN KEY (std_variable_ref_id) REFERENCES std_variable_refs(id) ON DELETE CASCADE
);

CREATE INDEX IF NOT EXISTS idx_std_var_ref_value_ranges_ref_id
    ON std_variable_ref_value_ranges(std_variable_ref_id);
