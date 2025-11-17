# Parser Quality Assurance (PQA) System Architecture

## Executive Summary

The Parser Quality Assurance (PQA) system is a comprehensive framework for validating IODD/EDS parser accuracy through forensic XML reconstruction, differential analysis, and automated quality metrics. The system ensures maximum data fidelity by comparing original source files against database-reconstructed XML.

## System Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    PQA System Architecture                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────┐    ┌──────────────┐    ┌──────────────┐     │
│  │   Original   │───▶│    Parser    │───▶│   Database   │     │
│  │  IODD/EDS    │    │  (greenstack)│    │   (SQLite)   │     │
│  └──────────────┘    └──────────────┘    └──────────────┘     │
│         │                                         │             │
│         │                                         │             │
│         ▼                                         ▼             │
│  ┌──────────────┐                        ┌──────────────┐     │
│  │   Archive    │                        │ Reconstructor│     │
│  │   Storage    │                        │    Engine    │     │
│  └──────────────┘                        └──────────────┘     │
│                                                   │             │
│                                                   ▼             │
│                                          ┌──────────────┐     │
│                                          │ Reconstructed│     │
│                                          │     XML      │     │
│                                          └──────────────┘     │
│         │                                         │             │
│         └────────────────┬────────────────────────┘             │
│                          ▼                                      │
│                  ┌──────────────┐                              │
│                  │  Diff Engine │                              │
│                  │   (DeepDiff) │                              │
│                  └──────────────┘                              │
│                          │                                      │
│                          ▼                                      │
│                  ┌──────────────┐                              │
│                  │Quality Metrics│                             │
│                  │   Analyzer   │                              │
│                  └──────────────┘                              │
│                          │                                      │
│         ┌────────────────┼────────────────┐                    │
│         ▼                ▼                ▼                    │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐               │
│  │  Ticket  │    │Dashboard │    │  Alerts  │               │
│  │Generator │    │   API    │    │  System  │               │
│  └──────────┘    └──────────┘    └──────────┘               │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Core Components

### 1. Archive Storage System
**Purpose**: Store original IODD/EDS files for comparison

**Database Schema**:
```sql
CREATE TABLE pqa_file_archive (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    file_type TEXT NOT NULL,  -- 'IODD' or 'EDS'
    filename TEXT NOT NULL,
    file_hash TEXT NOT NULL,  -- SHA256 of original file
    file_content BLOB NOT NULL,  -- Original XML/EDS content
    file_size INTEGER NOT NULL,
    upload_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,
    parser_version TEXT,  -- Version of parser used
    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE
);

CREATE INDEX idx_pqa_archive_device ON pqa_file_archive(device_id);
CREATE INDEX idx_pqa_archive_hash ON pqa_file_archive(file_hash);
```

### 2. Forensic XML Reconstruction Engine
**Purpose**: Rebuild XML from database tables to detect data loss

**Key Features**:
- Table-to-XML mapping for all 23+ database tables
- Attribute ordering preservation
- Namespace handling
- Comment/metadata reconstruction
- Multi-language text reassembly

**Reconstruction Algorithm**:
```python
def reconstruct_iodd(device_id: int) -> str:
    """
    Forensically reconstruct IODD XML from database.
    Returns: XML string matching original structure
    """
    # 1. Fetch all device data from database
    device = get_device(device_id)
    document_info = get_document_info(device_id)

    # 2. Build XML tree structure
    root = create_iolink_device_element(document_info)

    # 3. Reconstruct ProfileBody
    profile_body = reconstruct_profile_body(device_id)

    # 4. Reconstruct DeviceIdentity
    device_identity = reconstruct_device_identity(device)

    # 5. Reconstruct DeviceFunction
    device_function = reconstruct_device_function(device_id)

    # 6. Reconstruct ProcessDataCollection (5 phases)
    process_data = reconstruct_process_data_collection(device_id)

    # 7. Reconstruct ExternalTextCollection
    text_collection = reconstruct_text_collection(device_id)

    # 8. Reconstruct UserInterface (menus, buttons, variants)
    user_interface = reconstruct_user_interface(device_id)

    # 9. Pretty print with preserved formatting
    return prettify_xml(root)
```

### 3. Differential Analysis Engine
**Purpose**: Compare original vs reconstructed XML

**Comparison Metrics**:

| Metric | Description | Severity |
|--------|-------------|----------|
| **Structural Diff** | XML element tree differences | CRITICAL |
| **Attribute Diff** | Missing/changed attributes | HIGH |
| **Value Diff** | Changed element values | MEDIUM |
| **Ordering Diff** | Different element order | LOW |
| **Formatting Diff** | Whitespace/formatting changes | INFO |

**Implementation**:
```python
def analyze_differences(original_xml: str, reconstructed_xml: str) -> Dict:
    """
    Deep comparison of original vs reconstructed XML.
    Returns comprehensive diff report.
    """
    # Parse both XML documents
    original_tree = etree.fromstring(original_xml)
    reconstructed_tree = etree.fromstring(reconstructed_xml)

    # Normalize for comparison (remove formatting differences)
    original_normalized = normalize_xml(original_tree)
    reconstructed_normalized = normalize_xml(reconstructed_tree)

    # DeepDiff comparison
    diff = DeepDiff(
        original_normalized,
        reconstructed_normalized,
        ignore_order=False,
        report_repetition=True,
        verbose_level=2
    )

    # Categorize differences
    return {
        'added_elements': diff.get('dictionary_item_added', []),
        'removed_elements': diff.get('dictionary_item_removed', []),
        'changed_values': diff.get('values_changed', {}),
        'type_changes': diff.get('type_changes', {}),
        'repetition_changes': diff.get('repetition_change', [])
    }
```

### 4. Quality Metrics Database
**Purpose**: Store comprehensive quality analysis results

**Schema**:
```sql
CREATE TABLE pqa_quality_metrics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    device_id INTEGER NOT NULL,
    archive_id INTEGER NOT NULL,
    analysis_timestamp DATETIME DEFAULT CURRENT_TIMESTAMP,

    -- Overall Scores (0-100)
    overall_score REAL NOT NULL,
    structural_score REAL NOT NULL,
    attribute_score REAL NOT NULL,
    value_score REAL NOT NULL,

    -- Element Counts
    total_elements_original INTEGER,
    total_elements_reconstructed INTEGER,
    missing_elements INTEGER,
    extra_elements INTEGER,

    -- Attribute Counts
    total_attributes_original INTEGER,
    total_attributes_reconstructed INTEGER,
    missing_attributes INTEGER,
    incorrect_attributes INTEGER,

    -- Data Loss Metrics
    data_loss_percentage REAL,  -- % of data not recoverable
    critical_data_loss BOOLEAN,  -- Any critical field missing?

    -- Phase Coverage (0-100 each)
    phase1_score REAL,  -- UI Rendering Metadata
    phase2_score REAL,  -- Variants & Conditions
    phase3_score REAL,  -- Menu Buttons
    phase4_score REAL,  -- Wiring & Test Config
    phase5_score REAL,  -- Custom Datatypes

    -- Performance
    reconstruction_time_ms INTEGER,
    comparison_time_ms INTEGER,

    -- Status
    passed_threshold BOOLEAN,
    requires_review BOOLEAN,
    ticket_generated BOOLEAN,

    FOREIGN KEY (device_id) REFERENCES devices(id) ON DELETE CASCADE,
    FOREIGN KEY (archive_id) REFERENCES pqa_file_archive(id) ON DELETE CASCADE
);

CREATE TABLE pqa_diff_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    metric_id INTEGER NOT NULL,
    diff_type TEXT NOT NULL,  -- 'missing_element', 'changed_value', etc.
    severity TEXT NOT NULL,   -- 'CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO'
    xpath TEXT NOT NULL,      -- XPath to affected element
    expected_value TEXT,
    actual_value TEXT,
    description TEXT,
    FOREIGN KEY (metric_id) REFERENCES pqa_quality_metrics(id) ON DELETE CASCADE
);

CREATE TABLE pqa_thresholds (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    threshold_name TEXT UNIQUE NOT NULL,
    min_overall_score REAL DEFAULT 95.0,
    min_structural_score REAL DEFAULT 98.0,
    min_attribute_score REAL DEFAULT 95.0,
    max_data_loss_percentage REAL DEFAULT 1.0,
    auto_ticket_on_fail BOOLEAN DEFAULT TRUE,
    active BOOLEAN DEFAULT TRUE,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

### 5. Quality Scoring Algorithm

**Overall Score Calculation**:
```python
def calculate_quality_score(diff_analysis: Dict, original_stats: Dict, reconstructed_stats: Dict) -> Dict:
    """
    Calculate comprehensive quality metrics.

    Scoring Formula:
    - Structural Score: (1 - (missing_elements + extra_elements) / total_elements) * 100
    - Attribute Score: (1 - (missing_attrs + wrong_attrs) / total_attrs) * 100
    - Value Score: (1 - changed_values / total_values) * 100
    - Overall Score: weighted_average([structural, attribute, value])
    """

    # Weights for overall score
    WEIGHTS = {
        'structural': 0.40,  # Most important - structure must match
        'attribute': 0.35,   # Attributes critical for functionality
        'value': 0.25        # Values important but less critical
    }

    # Calculate individual scores
    structural_score = calculate_structural_score(diff_analysis, original_stats)
    attribute_score = calculate_attribute_score(diff_analysis, original_stats)
    value_score = calculate_value_score(diff_analysis, original_stats)

    # Weighted overall score
    overall_score = (
        structural_score * WEIGHTS['structural'] +
        attribute_score * WEIGHTS['attribute'] +
        value_score * WEIGHTS['value']
    )

    # Phase-specific scores
    phase_scores = calculate_phase_scores(diff_analysis)

    return {
        'overall_score': overall_score,
        'structural_score': structural_score,
        'attribute_score': attribute_score,
        'value_score': value_score,
        'phase_scores': phase_scores,
        'data_loss_percentage': calculate_data_loss(diff_analysis),
        'critical_data_loss': has_critical_data_loss(diff_analysis)
    }
```

### 6. Auto-Ticket Generation System

**Trigger Conditions**:
- Overall score < threshold (default: 95%)
- Critical data loss detected
- Missing required elements
- Phase score < 80%

**Ticket Schema**:
```python
@dataclass
class PQATicket:
    title: str  # "Parser Quality Issue: [Device Name] - Score 78%"
    description: str  # Detailed analysis
    severity: str  # CRITICAL, HIGH, MEDIUM, LOW
    device_id: int
    metric_id: int
    diff_summary: Dict
    recommended_actions: List[str]

def generate_pqa_ticket(metric: PQAMetric, diff_details: List[PQADiff]) -> Ticket:
    """
    Auto-generate ticket for parser quality issues.
    """
    # Categorize issues by severity
    critical_issues = [d for d in diff_details if d.severity == 'CRITICAL']
    high_issues = [d for d in diff_details if d.severity == 'HIGH']

    # Build description
    description = f"""
## Parser Quality Analysis Results

**Device**: {metric.device.device_name}
**Overall Score**: {metric.overall_score:.1f}% ❌
**Analysis Date**: {metric.analysis_timestamp}

### Score Breakdown
- Structural: {metric.structural_score:.1f}%
- Attributes: {metric.attribute_score:.1f}%
- Values: {metric.value_score:.1f}%
- Data Loss: {metric.data_loss_percentage:.2f}%

### Critical Issues ({len(critical_issues)})
{format_issue_list(critical_issues)}

### High Priority Issues ({len(high_issues)})
{format_issue_list(high_issues)}

### Recommended Actions
{generate_recommended_actions(metric, diff_details)}

### Phase Coverage
- Phase 1 (UI Metadata): {metric.phase1_score:.1f}%
- Phase 2 (Variants): {metric.phase2_score:.1f}%
- Phase 3 (Menu Buttons): {metric.phase3_score:.1f}%
- Phase 4 (Wiring/Test): {metric.phase4_score:.1f}%
- Phase 5 (Custom Types): {metric.phase5_score:.1f}%
    """

    return create_ticket(
        title=f"Parser Quality Issue: {metric.device.device_name} - Score {metric.overall_score:.0f}%",
        description=description,
        severity='critical' if metric.critical_data_loss else 'high',
        category='parser_quality',
        device_id=metric.device_id,
        metadata={
            'metric_id': metric.id,
            'overall_score': metric.overall_score,
            'data_loss_percentage': metric.data_loss_percentage
        }
    )
```

### 7. API Endpoints

```python
# Quality Analysis API
POST   /api/pqa/analyze/{device_id}           # Run quality analysis
GET    /api/pqa/metrics/{device_id}           # Get latest metrics
GET    /api/pqa/metrics/{device_id}/history   # Get all historical metrics
GET    /api/pqa/diff/{metric_id}              # Get detailed diff
GET    /api/pqa/reconstruct/{device_id}       # Get reconstructed XML

# Threshold Management
GET    /api/pqa/thresholds                    # List all thresholds
POST   /api/pqa/thresholds                    # Create threshold
PUT    /api/pqa/thresholds/{id}               # Update threshold
DELETE /api/pqa/thresholds/{id}               # Delete threshold

# Archive Management
GET    /api/pqa/archive/{device_id}           # Get archived original
POST   /api/pqa/archive/{device_id}           # Store original file

# Dashboard Data
GET    /api/pqa/dashboard/summary             # System-wide quality metrics
GET    /api/pqa/dashboard/trends              # Quality trends over time
GET    /api/pqa/dashboard/failures            # List of failed analyses
```

### 8. Admin Dashboard Components

**Key Visualizations**:

1. **Quality Score Distribution**
   - Histogram of all device scores
   - Color-coded by threshold passing

2. **Trend Analysis**
   - Quality scores over time
   - Parser version impact analysis

3. **Phase Coverage Heatmap**
   - 5 phases × all devices
   - Color-coded performance

4. **Data Loss Radar Chart**
   - Multi-dimensional data loss visualization
   - Per-category breakdown

5. **Failure Investigation Table**
   - Sortable/filterable list
   - Drill-down to diff details

6. **Recent Tickets**
   - Auto-generated PQA tickets
   - Resolution tracking

## Implementation Phases

### Phase 1: Foundation (Week 1-2)
- ✅ Database schema (pqa_file_archive, pqa_quality_metrics, pqa_diff_details, pqa_thresholds)
- ✅ Archive storage implementation
- ✅ Basic reconstruction engine

### Phase 2: Analysis Engine (Week 3-4)
- ✅ Complete XML reconstruction for all tables
- ✅ DeepDiff integration
- ✅ Quality scoring algorithm
- ✅ Phase-specific analysis

### Phase 3: Automation (Week 5)
- ✅ Auto-analysis on import
- ✅ Ticket generation system
- ✅ Threshold configuration

### Phase 4: Dashboard (Week 6)
- ✅ Admin console integration
- ✅ Quality metrics visualizations
- ✅ Trend analysis
- ✅ Diff viewer UI

## Success Metrics

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| Overall Parser Score | >98% | <95% |
| Structural Accuracy | >99% | <98% |
| Data Loss | <0.5% | >1% |
| Phase Coverage | 100% | <95% |
| Auto-Detection Rate | >95% | <90% |

## Risk Mitigation

**Risk 1**: XML reconstruction order differences
- **Mitigation**: Implement canonical ordering algorithm

**Risk 2**: Parser version changes affecting baselines
- **Mitigation**: Version-specific thresholds, trend analysis

**Risk 3**: Performance impact on large files
- **Mitigation**: Async analysis, caching, incremental diffs

**Risk 4**: False positives from insignificant differences
- **Mitigation**: Configurable ignore patterns, normalization rules

## Future Enhancements

1. **Machine Learning Integration**
   - Pattern detection in parser failures
   - Predictive quality scoring

2. **A/B Testing Framework**
   - Compare parser versions
   - Regression detection

3. **Community Contributions**
   - Public diff database
   - Crowd-sourced parser improvements

4. **Real-time Monitoring**
   - WebSocket-based live analysis
   - Push notifications for failures

## Conclusion

The PQA system transforms Greenstack from a simple parser into a **self-validating, forensically-accurate data capture platform**. By comparing every parsed device against its original source, we ensure maximum data fidelity and provide actionable insights for continuous parser improvement.

**Key Benefits**:
- ✅ 100% transparency in data capture
- ✅ Automated quality assurance
- ✅ Forensic-grade reconstruction
- ✅ Continuous improvement feedback loop
- ✅ Production-ready confidence

---

*Document Version: 1.0*
*Last Updated: 2025-01-17*
*Author: Claude Code*
