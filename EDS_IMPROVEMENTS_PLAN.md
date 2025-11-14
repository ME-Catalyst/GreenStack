# EDS Improvements - Implementation Plan

## Overview

Two major improvements to the EDS feature:
1. **Revision Consolidation**: Group multiple revisions of the same device, show latest by default
2. **eds_pie Integration**: Enhance parsing with industry-standard library

---

## Part 1: Revision Consolidation

### Problem
Currently, if a device has 5 different revisions (v1.0, v1.1, v1.2, v2.0, v2.1), the list view shows 5 separate entries. This clutters the UI and makes it hard to find the device you want.

### Solution
**List View**: Show only ONE card per unique device (vendor + product code)
- Display latest revision by default
- Show revision count badge (e.g., "5 revisions")
- Click to expand/view all revisions in detail view

**Detail View**: Add revision selector dropdown
- Default: Latest revision
- Dropdown shows all available revisions sorted (newest first)
- Changing revision reloads data for that specific revision

### Implementation Steps

#### Backend Changes

**1. Add revision grouping endpoint** (`eds_routes.py`)
```python
@router.get("/grouped")
async def get_eds_grouped():
    """
    Get EDS files grouped by device (vendor_code + product_code).
    Returns latest revision for each device plus revision count.
    """
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Group by vendor_code + product_code, get latest revision
    cursor.execute("""
        WITH ranked AS (
            SELECT *,
                   ROW_NUMBER() OVER (
                       PARTITION BY vendor_code, product_code
                       ORDER BY major_revision DESC, minor_revision DESC
                   ) as rn,
                   COUNT(*) OVER (
                       PARTITION BY vendor_code, product_code
                   ) as revision_count
            FROM eds_files
        )
        SELECT * FROM ranked WHERE rn = 1
        ORDER BY vendor_name, product_name
    """)

    # Return results with revision_count included
    ...
```

**2. Add revisions list endpoint** (`eds_routes.py`)
```python
@router.get("/{vendor_code}/{product_code}/revisions")
async def get_device_revisions(vendor_code: int, product_code: int):
    """
    Get all revisions for a specific device.
    Returns list sorted by revision (newest first).
    """
    cursor.execute("""
        SELECT id, major_revision, minor_revision, import_date,
               vendor_name, product_name, catalog_number
        FROM eds_files
        WHERE vendor_code = ? AND product_code = ?
        ORDER BY major_revision DESC, minor_revision DESC
    """, (vendor_code, product_code))
    ...
```

#### Frontend Changes

**1. Update EDS list view** (`App.jsx`)
- Change API call from `/api/eds` to `/api/eds/grouped`
- Display revision count badge on each card
- Show "v{major}.{minor}" and "(5 revisions)" badge

**2. Add revision selector to detail view** (`EDSDetailsView.jsx`)
```jsx
const [availableRevisions, setAvailableRevisions] = useState([]);
const [selectedRevision, setSelectedRevision] = useState(null);

useEffect(() => {
    // Fetch all revisions for this device
    axios.get(`${API_BASE}/api/eds/${vendorCode}/${productCode}/revisions`)
        .then(res => {
            setAvailableRevisions(res.data);
            setSelectedRevision(selectedEds.id); // Default to current
        });
}, [vendorCode, productCode]);

// Revision selector dropdown in header
<Select value={selectedRevision} onValueChange={loadRevision}>
    {availableRevisions.map(rev => (
        <SelectItem value={rev.id} key={rev.id}>
            v{rev.major_revision}.{rev.minor_revision}
            {rev.import_date && ` (${new Date(rev.import_date).toLocaleDateString()})`}
        </SelectItem>
    ))}
</Select>
```

### Database Schema
No changes needed! Existing schema already has:
- `vendor_code` and `product_code` for grouping
- `major_revision` and `minor_revision` for sorting
- `import_date` for additional context

### UI Mockup

**List View - Before**:
```
┌─────────────────────────┐
│ Cube67+ BN-E V2 (v1.0) │
│ 56535                   │
└─────────────────────────┘
┌─────────────────────────┐
│ Cube67+ BN-E V2 (v1.1) │
│ 56535                   │
└─────────────────────────┘
┌─────────────────────────┐
│ Cube67+ BN-E V2 (v2.0) │
│ 56535                   │
└─────────────────────────┘
```

**List View - After**:
```
┌──────────────────────────────────┐
│ Cube67+ BN-E V2 (v2.0)          │
│ 56535          [3 revisions] 🔽 │
└──────────────────────────────────┘
```

**Detail View Header**:
```
[← Back]  Cube67+ BN-E V2  [Revision: v2.0 ▼]  [Export JSON] [Export ZIP]
```

---

## Part 2: eds_pie Integration

### What is eds_pie?

**Library**: https://github.com/omidbimo/eds_pie
**License**: MIT
**Purpose**: Industry-standard EDS parser for ODVA's CIP® protocol family

### Advantages Over Current Parser

#### 1. **Robust Parsing**
- Handles complex nested structures automatically
- Proper section/entry/field hierarchy
- Built-in validation and error handling

#### 2. **Protocol-Aware**
- Knows about CIP object classes
- Understands EtherNet/IP vs DeviceNet differences
- Built-in CIP type system

#### 3. **Structured Access**
- Navigate with `.getentry('Device', 'ProdType')`
- No regex needed for complex queries
- Automatic type conversion

#### 4. **Additional Features**
- Export to XML/JSON
- Modify and save EDS files
- CIP class ID to section name mapping
- Comprehensive field metadata

### Current Parser vs eds_pie Comparison

| Feature | Current Parser | eds_pie |
|---------|----------------|---------|
| Basic parsing | ✅ Regex-based | ✅ Object-based |
| Section extraction | ✅ Manual | ✅ Automatic |
| Entry parsing | ✅ Custom code | ✅ Built-in |
| Field typing | ❌ Manual | ✅ CIP types |
| CIP awareness | ❌ None | ✅ Full |
| Validation | ⚠️ Basic | ✅ Comprehensive |
| Error handling | ⚠️ Basic | ✅ Robust |
| Modification support | ❌ No | ✅ Yes |
| Export formats | ❌ No | ✅ XML/JSON |

### Integration Strategy

#### Option 1: Parallel Parser (Recommended for Phase 1)
- Keep current parser as fallback
- Add eds_pie as enhanced parser
- Use eds_pie when available, fall back to current parser
- Gradual migration path

#### Option 2: Full Replacement (Phase 2)
- Replace current parser entirely with eds_pie
- Rewrite extraction logic using eds_pie API
- More comprehensive but higher risk

### Implementation Plan

#### Phase 1: Integration & Enhancement

**1. Install eds_pie**
```bash
# Copy eds_pie.py and dependencies into project
cp /tmp/eds_pie/eds_pie.py ./
cp /tmp/eds_pie/cip_eds_types.py ./
cp /tmp/eds_pie/*.json ./
```

**2. Create wrapper module** (`eds_pie_parser.py`)
```python
"""
Enhanced EDS parser using eds_pie library.
Provides same interface as current parser but with better parsing.
"""
from eds_pie import eds_pie
import logging

def parse_eds_with_pie(content: str) -> Dict[str, Any]:
    """
    Parse EDS content using eds_pie library.
    Returns data in same format as current parser for compatibility.
    """
    try:
        eds = eds_pie.parse(content, showprogress=False)

        return {
            'device': extract_device_info(eds),
            'parameters': extract_parameters(eds),
            'connections': extract_connections(eds),
            'capacity': extract_capacity(eds),
            'ports': extract_ports(eds),
            # ... additional extractions
        }
    except Exception as e:
        logging.error(f"eds_pie parsing failed: {e}")
        return None  # Fallback to current parser

def extract_device_info(eds) -> Dict[str, Any]:
    """Extract device information using eds_pie API."""
    device_section = eds.getsection('Device')
    return {
        'vendor_name': device_section.getvalue('VendName'),
        'vendor_code': device_section.getvalue('VendCode'),
        'product_name': device_section.getvalue('ProdName'),
        'product_code': device_section.getvalue('ProdCode'),
        'major_revision': device_section.getvalue('MajRev'),
        'minor_revision': device_section.getvalue('MinRev'),
        # ... more fields
    }

def extract_parameters(eds) -> List[Dict[str, Any]]:
    """Extract parameters with full CIP type information."""
    params = []

    # eds_pie can enumerate all Assembly/Parameter objects
    for section in eds.sections:
        if section.name.startswith('Param') or 'Assembly' in section.name:
            param = {
                'name': section.getvalue('Name'),
                'type': section.getvalue('Type'),
                'path': section.getvalue('Path'),
                # eds_pie provides type info from cip_eds_types
                'cip_type': get_cip_type_info(section.getvalue('Type')),
                ...
            }
            params.append(param)

    return params
```

**3. Update main parser** (`eds_parser.py`)
```python
# Add at top
try:
    from eds_pie_parser import parse_eds_with_pie
    HAS_EDS_PIE = True
except ImportError:
    HAS_EDS_PIE = False

def parse_eds_file(content: str, ...):
    """
    Parse EDS file with automatic fallback.
    Tries eds_pie first, falls back to current parser.
    """
    # Try eds_pie if available
    if HAS_EDS_PIE:
        result = parse_eds_with_pie(content)
        if result:
            logging.info("Parsed with eds_pie successfully")
            return result
        logging.warning("eds_pie failed, using fallback parser")

    # Fall back to current parser
    parser = EDSParser(content)
    return current_parsing_logic(parser)
```

#### Phase 2: Enhanced Features

**1. CIP Object Browser**
- Show all CIP objects in device
- Display class IDs and descriptions
- Link to ODVA specifications

**2. Advanced Validation**
- Validate against CIP specification
- Check for required fields
- Warn about deprecated features

**3. EDS Editor**
- Modify parameter values
- Add/remove connections
- Save modified EDS files

**4. Format Conversion**
- Export to XML for tools that need it
- Export to JSON for web apps
- Import from other formats

### Testing Strategy

**1. Parallel Testing**
```python
# In test script
current_result = current_parser.parse(eds_content)
pie_result = eds_pie_parser.parse(eds_content)

# Compare results
compare_parsing_results(current_result, pie_result)
```

**2. Validation**
- Parse all 13 test EDS files with both parsers
- Compare parameter counts, connection counts, capacity values
- Ensure no regressions

**3. Performance**
- Measure parsing time for both parsers
- Check memory usage
- Ensure eds_pie doesn't slow down imports

### Risks & Mitigation

**Risk 1**: eds_pie might parse differently than current parser
- **Mitigation**: Parallel testing, gradual rollout, fallback mechanism

**Risk 2**: eds_pie might not handle all vendor variations
- **Mitigation**: Keep current parser as fallback, log failures for review

**Risk 3**: Additional dependency to maintain
- **Mitigation**: Vendor the files (copy into project), don't rely on external updates

---

## Implementation Timeline

### Phase 1: Revision Consolidation (Priority 1)
**Week 1**:
- ✅ Design UI/UX
- ✅ Implement backend grouping endpoint
- ✅ Update frontend list view
- ✅ Add revision selector to detail view
- ✅ Testing & refinement

**Deliverables**:
- Cleaner list view showing latest revisions
- Revision dropdown in detail view
- Updated API endpoints

### Phase 2: eds_pie Integration (Priority 2)
**Week 2**:
- ✅ Vendor eds_pie files into project
- ✅ Create wrapper module
- ✅ Implement parallel parsing
- ✅ Testing with all EDS files

**Week 3**:
- ✅ Add CIP type information to parameters
- ✅ Enhance validation
- ✅ Documentation

**Deliverables**:
- Enhanced parser with fallback
- Better type information
- Improved error handling

### Phase 3: Advanced Features (Future)
**Month 2**:
- CIP Object Browser
- EDS Editor
- Format conversion tools

---

## Success Metrics

### Revision Consolidation
- ✅ List view shows N unique devices instead of M revisions (M > N)
- ✅ Users can switch between revisions smoothly
- ✅ Latest revision is default
- ✅ No data loss or confusion

### eds_pie Integration
- ✅ Parsing accuracy >= current parser (100%)
- ✅ Parsing speed within 2x of current parser
- ✅ No regressions in data quality
- ✅ Additional CIP information available

---

## Files to Modify

### Revision Consolidation
1. `eds_routes.py` - Add grouping and revision endpoints
2. `App.jsx` - Update list view to use grouped data
3. `EDSDetailsView.jsx` - Add revision selector dropdown

### eds_pie Integration
1. **New**: `eds_pie.py` (vendored from GitHub)
2. **New**: `cip_eds_types.py` (vendored)
3. **New**: `*.json` files (vendored)
4. **New**: `eds_pie_parser.py` (wrapper module)
5. `eds_parser.py` - Add fallback logic
6. `requirements.txt` - Document vendored dependencies

---

## Next Steps

1. **User Approval**: Review this plan and approve approach
2. **Start Implementation**: Begin with revision consolidation (higher priority, lower risk)
3. **Test eds_pie**: Run parallel tests to validate approach
4. **Iterate**: Gather feedback and refine

**Question for you**: Should we:
- A) Implement revision consolidation first, then eds_pie later?
- B) Implement both simultaneously?
- C) Focus only on revision consolidation for now?

My recommendation: **Option A** - Revision consolidation is a clear UX win with minimal risk, while eds_pie needs more testing and validation.
