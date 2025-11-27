"""
Comprehensive PQA Issue Analysis
Identifies all issues preventing 100% PQA scores across all devices
"""
import sqlite3
from collections import defaultdict

conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

print("=" * 80)
print("COMPREHENSIVE PQA ISSUE ANALYSIS")
print("=" * 80)

# Get all imperfect devices
cursor.execute("""
    SELECT
        m.id as metric_id,
        m.device_id,
        d.vendor_id,
        d.device_id as device_num,
        d.product_name,
        m.overall_score,
        m.structural_score,
        m.attribute_score,
        m.value_score,
        m.missing_elements,
        m.missing_attributes,
        m.incorrect_attributes
    FROM pqa_quality_metrics m
    JOIN devices d ON m.device_id = d.id
    WHERE m.overall_score < 100.0
    ORDER BY m.overall_score ASC
    LIMIT 50
""")

imperfect_devices = cursor.fetchall()

print(f"\nFound {len(imperfect_devices)} devices with <100% scores (showing worst 50)")
print("\n" + "=" * 80)
print("TOP ISSUES BY CATEGORY")
print("=" * 80)

# Categorize issues by type
issue_categories = defaultdict(lambda: defaultdict(int))
xpath_patterns = defaultdict(int)

for device in imperfect_devices:
    metric_id = device[0]
    device_id = device[1]
    product = device[4]

    # Get diff details for this device
    cursor.execute("""
        SELECT diff_type, xpath, expected_value, actual_value, description
        FROM pqa_diff_details
        WHERE metric_id = ?
    """, (metric_id,))

    diffs = cursor.fetchall()

    for diff in diffs:
        diff_type, xpath, expected, actual, desc = diff

        # Extract element name from XPath
        if '/' in xpath:
            parts = xpath.split('/')
            for part in reversed(parts):
                if part and not part.startswith('@'):
                    element = part.split('[')[0]  # Remove index
                    issue_categories[diff_type][element] += 1
                    xpath_patterns[xpath] += 1
                    break

# Print categorized issues
print("\n### MISSING ELEMENTS ###")
if 'missing_element' in issue_categories:
    for element, count in sorted(issue_categories['missing_element'].items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {element:40} : {count:5} occurrences")
else:
    print("  None")

print("\n### MISSING ATTRIBUTES ###")
if 'missing_attribute' in issue_categories:
    for element, count in sorted(issue_categories['missing_attribute'].items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {element:40} : {count:5} occurrences")
else:
    print("  None")

print("\n### INCORRECT ATTRIBUTES ###")
if 'incorrect_attribute' in issue_categories:
    for element, count in sorted(issue_categories['incorrect_attribute'].items(), key=lambda x: x[1], reverse=True)[:20]:
        print(f"  {element:40} : {count:5} occurrences")
else:
    print("  None")

print("\n" + "=" * 80)
print("DETAILED ANALYSIS OF WORST 5 DEVICES")
print("=" * 80)

for i, device in enumerate(imperfect_devices[:5]):
    metric_id, device_id, vendor_id, device_num, product, overall, struct, attr, value, missing_els, missing_attrs, incorrect_attrs = device

    print(f"\n### DEVICE {i+1}: ID={device_id}, vendor={vendor_id}, device={device_num} ###")
    print(f"Product: {product}")
    print(f"Scores: Overall={overall:.2f}%, Structural={struct:.2f}%, Attribute={attr:.2f}%, Value={value:.2f}%")
    print(f"Issues: {missing_els} missing elements, {missing_attrs} missing attrs, {incorrect_attrs} incorrect attrs")

    # Get specific issues
    cursor.execute("""
        SELECT diff_type, xpath, expected_value, actual_value, description
        FROM pqa_diff_details
        WHERE metric_id = ?
        ORDER BY diff_type
        LIMIT 20
    """, (metric_id,))

    diffs = cursor.fetchall()

    # Group by diff type
    by_type = defaultdict(list)
    for diff in diffs:
        by_type[diff[0]].append(diff)

    for diff_type in ['missing_element', 'missing_attribute', 'incorrect_attribute', 'incorrect_value']:
        if diff_type in by_type:
            print(f"\n  {diff_type.upper()} (showing first 5):")
            for diff in by_type[diff_type][:5]:
                xpath = diff[1]
                expected = diff[2] if diff[2] else 'N/A'
                actual = diff[3] if diff[3] else 'N/A'
                desc = diff[4] if diff[4] else ''
                print(f"    XPath: {xpath}")
                if expected != 'N/A' or actual != 'N/A':
                    print(f"      Expected: {expected[:100]}")
                    print(f"      Actual:   {actual[:100]}")
                if desc:
                    print(f"      Desc: {desc[:150]}")
                print()

print("\n" + "=" * 80)
print("SUMMARY OF ROOT CAUSES")
print("=" * 80)

# Analyze patterns
print("\nBased on the analysis, the main issues preventing 100% scores are:")
print("\n1. MISSING ELEMENTS:")
if 'missing_element' in issue_categories:
    top_missing = sorted(issue_categories['missing_element'].items(), key=lambda x: x[1], reverse=True)[:5]
    for element, count in top_missing:
        print(f"   - {element}: {count} devices affected")

print("\n2. MISSING ATTRIBUTES:")
if 'missing_attribute' in issue_categories:
    top_missing_attrs = sorted(issue_categories['missing_attribute'].items(), key=lambda x: x[1], reverse=True)[:5]
    for element, count in top_missing_attrs:
        print(f"   - {element}: {count} devices affected")

print("\n3. INCORRECT ATTRIBUTES:")
if 'incorrect_attribute' in issue_categories:
    top_incorrect = sorted(issue_categories['incorrect_attribute'].items(), key=lambda x: x[1], reverse=True)[:5]
    for element, count in top_incorrect:
        print(f"   - {element}: {count} devices affected")

conn.close()

print("\n" + "=" * 80)
print("ANALYSIS COMPLETE")
print("=" * 80)
