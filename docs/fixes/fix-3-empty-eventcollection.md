# Fix #3: Empty EventCollection Tracking

**Impact**: 101 missing_element diffs
**Status**: In Progress

## Problem

Original IODDs with empty `<EventCollection/>` elements are not being reconstructed because:
1. No database flag tracks "EventCollection exists but is empty"
2. Reconstruction returns `None` when no events found
3. Diff analyzer sees missing element

## Solution

### Step 1: Add Database Column
```sql
ALTER TABLE iodd_files ADD COLUMN has_event_collection BOOLEAN DEFAULT FALSE;
```

### Step 2: Update Parser
Extract EventCollection element presence (even if empty)

### Step 3: Update Storage
Save has_event_collection flag

### Step 4: Update Reconstruction
Output empty `<EventCollection/>` when flag=TRUE and no events

## Implementation Status

- [ ] Database migration
- [ ] Parser extraction
- [ ] Storage update
- [ ] Reconstruction update
- [ ] Test with device that has empty EventCollection
