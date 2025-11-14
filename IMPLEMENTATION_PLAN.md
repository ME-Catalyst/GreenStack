# Implementation Plan: Parameter Schema & Ticket System

## Current Status

### ✅ COMPLETED
1. Assembly parser fixes (simplified format, hex parsing)
2. Assembly insertion in package upload endpoint
3. Delete operations (foreign key CASCADE)
4. Ticket system database schema design

### 🚧 IN PROGRESS
1. Parameter schema expansion
2. Ticket system implementation

---

## Part 1: Parameter Schema Expansion

### Issue Analysis
**Current parser mapping is WRONG for your EDS format:**

```
Your EDS Format:
Index 0:  reserved (0)
Index 1-2: Link Path Size, Link Path
Index 3:  Descriptor
Index 4:  Data Type (0xC8)
Index 5:  Data Size (4)
Index 6:  Name ("RPI Range")
Index 7:  Units ("Microsecond")
Index 8:  Help String
Index 9:  Min value (4000)
Index 10: Max value (100000)
Index 11: Default value (10000)
Index 12-15: Scaling (mult, div, base, offset)
Index 16-19: Link scaling (mult, div, base, offset)
Index 20: Decimal places

Current Parser (WRONG):
- Skips index 0 properly ❌ NO - doesn't skip it
- Maps units to help_string_1 ❌
- Has min/max/default BACKWARDS ❌ (9=default, 10=max, 11=min)
- Doesn't capture scaling ❌
- Doesn't capture decimal places ❌
```

### Files to Modify

#### 1. Database Migration (`alembic/versions/010_expand_parameter_schema.py`)
**Status**: Created but needs renumbering

**Actions**:
- Rename from `008_` to `010_`
- Change `revision = '010'` and `down_revision = '009'`
- Run: `python -m alembic upgrade head`

**New columns to add**:
- `units` TEXT
- `scaling_multiplier` TEXT
- `scaling_divisor` TEXT
- `scaling_base` TEXT
- `scaling_offset` TEXT
- `link_scaling_multiplier` TEXT
- `link_scaling_divisor` TEXT
- `link_scaling_base` TEXT
- `link_scaling_offset` TEXT
- `decimal_places` INTEGER

#### 2. Parser Fix (`eds_parser.py` lines 163-222)

**Current code to replace**:
```python
# Line 190: Parse comma-separated values
values = [v.strip().strip('"') for v in param_data.split(',')]

# Lines 192-220: WRONG mapping
params.append({
    'param_number': param_num,
    'link_path_size': values[0],  # WRONG - this is reserved field
    'link_path': values[1],
    'descriptor': values[2],
    'data_type': self._parse_int(values[5]),  # Index 5
    'data_size': self._parse_int(values[4]),  # Index 4 - actually index 5!
    'param_name': values[6],
    'help_string_1': values[7],  # This is actually UNITS
    'help_string_2': values[8],
    'default_value': values[9],  # WRONG - this is MIN
    'max_value': values[10],
    'min_value': values[11],  # WRONG - this is DEFAULT
})
```

**Correct mapping**:
```python
params.append({
    'param_number': param_num,
    # Skip index 0 (reserved)
    'link_path_size': values[1] if len(values) > 1 else None,
    'link_path': values[2] if len(values) > 2 else None,
    'descriptor': values[3] if len(values) > 3 else None,
    'data_type': self._parse_hex(values[4]) if len(values) > 4 else None,
    'data_size': self._parse_int(values[5]) if len(values) > 5 else None,
    'param_name': values[6] if len(values) > 6 else f'Param{param_num}',
    'units': values[7] if len(values) > 7 else '',  # NEW
    'help_string_1': values[8] if len(values) > 8 else '',  # Correct now
    'min_value': values[9] if len(values) > 9 else None,  # FIXED
    'max_value': values[10] if len(values) > 10 else None,  # FIXED
    'default_value': values[11] if len(values) > 11 else None,  # FIXED
    'scaling_multiplier': values[12] if len(values) > 12 else None,  # NEW
    'scaling_divisor': values[13] if len(values) > 13 else None,  # NEW
    'scaling_base': values[14] if len(values) > 14 else None,  # NEW
    'scaling_offset': values[15] if len(values) > 15 else None,  # NEW
    'link_scaling_multiplier': values[16] if len(values) > 16 else None,  # NEW
    'link_scaling_divisor': values[17] if len(values) > 17 else None,  # NEW
    'link_scaling_base': values[18] if len(values) > 18 else None,  # NEW
    'link_scaling_offset': values[19] if len(values) > 19 else None,  # NEW
    'decimal_places': self._parse_int(values[20]) if len(values) > 20 else None,  # NEW
    'help_string_2': '',  # Not used in this format
    'help_string_3': '',  # Not used in this format
})
```

#### 3. Update API endpoints to insert new fields

**Files to modify**:
- `eds_routes.py` - `/upload` endpoint (line 173)
- `eds_routes.py` - `/upload-package` endpoint (line 1147)

Add new fields to INSERT statements:
```python
cursor.execute("""
    INSERT INTO eds_parameters (
        eds_file_id, param_number, param_name, data_type,
        data_size, default_value, min_value, max_value,
        description, link_path_size, link_path, descriptor,
        help_string_1, help_string_2, help_string_3, enum_values,
        units, scaling_multiplier, scaling_divisor, scaling_base, scaling_offset,
        link_scaling_multiplier, link_scaling_divisor, link_scaling_base, link_scaling_offset,
        decimal_places
    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
""", (
    eds_id, param.get('param_number'), param.get('param_name'),
    param.get('data_type'), param.get('data_size'),
    param.get('default_value'), param.get('min_value'), param.get('max_value'),
    param.get('help_string_1', ''), param.get('link_path_size'),
    param.get('link_path'), param.get('descriptor'),
    param.get('help_string_1'), param.get('help_string_2'), param.get('help_string_3'),
    param.get('enum_values'),
    param.get('units'),  # NEW
    param.get('scaling_multiplier'),  # NEW
    param.get('scaling_divisor'),  # NEW
    param.get('scaling_base'),  # NEW
    param.get('scaling_offset'),  # NEW
    param.get('link_scaling_multiplier'),  # NEW
    param.get('link_scaling_divisor'),  # NEW
    param.get('link_scaling_base'),  # NEW
    param.get('link_scaling_offset'),  # NEW
    param.get('decimal_places')  # NEW
))
```

---

## Part 2: Ticket/Bug System

### Database Schema (Already Created)

**Tables**:
1. `tickets` - Main ticket records
2. `ticket_comments` - Comment threads
3. `ticket_attachments` - File attachments

### Implementation Steps

#### 1. Ticket API Routes (`ticket_routes.py` - NEW FILE)

Create comprehensive REST API:

```python
# GET /api/tickets - List all tickets (with filters)
# GET /api/tickets/{id} - Get single ticket with comments
# POST /api/tickets - Create new ticket
# PATCH /api/tickets/{id} - Update ticket (status, priority, etc.)
# DELETE /api/tickets/{id} - Delete ticket
# POST /api/tickets/{id}/comments - Add comment
# GET /api/tickets/export/csv - Export to CSV
```

#### 2. Frontend Components

**TicketButton.jsx**:
- Floating action button on device detail pages
- Opens modal for ticket creation
- Props: `deviceType` ('EDS' | 'IODD'), `deviceId`, `deviceName`

**TicketModal.jsx**:
- Form fields: title, description, eds_reference, priority, category
- Markdown editor for description
- Auto-populate device info
- Submit → API POST → Close & show success

**TicketList.jsx**:
- Table/card view of all tickets
- Filters: status, priority, category, device type, date range
- Sort by: created date, updated date, priority
- Actions: view, edit status, delete
- Export CSV button

**TicketDetail.jsx**:
- Full ticket view with all details
- Device link (click to go back to device)
- Comment thread
- Status/priority badges
- Edit form for updates

#### 3. CSV Export Format

```csv
Ticket Number,Device Type,Device Name,Vendor,Product Code,Title,Description,EDS Reference,Status,Priority,Category,Created At,Updated At,Resolved At,All Comments
TICKET-0001,EDS,Cube67+,Murrelektronik,56535,"Wrong parameter min/max","The min and max values...","Param2",open,high,data_issue,2025-01-14 10:30:00,2025-01-14 11:00:00,,"Comment 1: Need to check EDS source | Comment 2: Confirmed bug"
```

### UI/UX Design

**Ticket Button** (on device detail pages):
- Position: Fixed bottom-right corner
- Icon: Bug icon with "Report Issue" text
- Color: Orange/red for visibility
- Hover: Slight scale/glow effect

**Ticket Modal**:
- Modal overlay (semi-transparent)
- Title: "Report Issue - [Device Name]"
- Device info auto-populated (read-only display)
- Form validation (title & description required)
- Submit button: "Create Ticket"
- Cancel button

**Status Colors**:
- open: blue
- in_progress: yellow
- resolved: green
- closed: gray
- wont_fix: red

**Priority Colors**:
- low: gray
- medium: blue
- high: orange
- critical: red

---

## Testing Plan

### Parameter Schema
1. Reset EDS database
2. Upload 56535 package
3. Check parameter for ID=1:
   - Verify units field = "Microsecond"
   - Verify min=4000, max=100000, default=10000
   - Verify scaling fields captured

### Ticket System
1. Create ticket from EDS device page
2. Create ticket from IODD device page
3. Add comments to ticket
4. Change ticket status/priority
5. Export tickets to CSV
6. Verify CSV contains all data

---

## File Structure

```
backend/
├── alembic/versions/
│   ├── 010_expand_parameter_schema.py ✅ Created
│   └── 011_create_ticket_system.py ✅ Created
├── ticket_routes.py 🚧 To create
├── eds_parser.py 🚧 To fix (lines 163-222)
└── eds_routes.py 🚧 To update (parameter inserts)

frontend/src/components/
├── TicketButton.jsx 🚧 To create
├── TicketModal.jsx 🚧 To create
├── TicketList.jsx 🚧 To create
└── TicketDetail.jsx 🚧 To create
```

---

## Priority Order

1. **HIGHEST**: Test assemblies (upload 56535, verify tab works)
2. **HIGH**: Fix parameter parser (min/max/default order)
3. **HIGH**: Run parameter schema migration
4. **MEDIUM**: Implement ticket API
5. **MEDIUM**: Create ticket UI components
6. **LOW**: CSV export functionality
