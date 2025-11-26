#!/usr/bin/env python3
"""Analyze current PQA results from imported IODD dataset."""

import sqlite3
import json
import sys
from collections import Counter, defaultdict

# Force UTF-8 encoding for output
if sys.platform == 'win32':
    import codecs
    sys.stdout = codecs.getwriter('utf-8')(sys.stdout.buffer, 'strict')

def analyze_pqa_results():
    """Comprehensive analysis of PQA results."""
    conn = sqlite3.connect('greenstack.db')
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    print("="*80)
    print("PQA RESULTS ANALYSIS - IMPORTED IODD DATASET")
    print("="*80)

    # 1. Basic Statistics
    print("\n## 1. DATASET OVERVIEW\n")

    cursor.execute("SELECT COUNT(*) FROM devices")
    total_devices = cursor.fetchone()[0]
    print(f"Total Devices Imported: {total_devices}")

    cursor.execute("SELECT COUNT(*) FROM pqa_quality_metrics WHERE file_type = 'IODD'")
    analyzed_devices = cursor.fetchone()[0]
    print(f"Devices with PQA Analysis: {analyzed_devices}")
    print(f"Analysis Coverage: {analyzed_devices/total_devices*100:.1f}%" if total_devices > 0 else "N/A")

    # 2. Score Distribution
    print("\n## 2. SCORE STATISTICS\n")

    cursor.execute("""
        SELECT
            COUNT(*) as total,
            AVG(overall_score) as avg_overall,
            MIN(overall_score) as min_overall,
            MAX(overall_score) as max_overall,
            AVG(structural_score) as avg_structural,
            AVG(attribute_score) as avg_attribute,
            AVG(value_score) as avg_value,
            AVG(data_loss_percentage) as avg_data_loss,
            SUM(CASE WHEN critical_data_loss = 1 THEN 1 ELSE 0 END) as critical_count,
            SUM(CASE WHEN passed_threshold = 1 THEN 1 ELSE 0 END) as passed_count,
            SUM(CASE WHEN overall_score = 100.0 THEN 1 ELSE 0 END) as perfect_count
        FROM pqa_quality_metrics
        WHERE file_type = 'IODD'
    """)

    stats = cursor.fetchone()
    print(f"Total Analyzed: {stats['total']}")
    print(f"\nOverall Scores (Full Precision):")
    print(f"  Average: {stats['avg_overall']:.4f}%")
    print(f"  Range: {stats['min_overall']:.4f}% - {stats['max_overall']:.4f}%")
    print(f"\nComponent Scores (Full Precision):")
    print(f"  Structural (40%): {stats['avg_structural']:.4f}%")
    print(f"  Attribute (35%):  {stats['avg_attribute']:.4f}%")
    print(f"  Value (25%):      {stats['avg_value']:.4f}%")
    print(f"\nQuality Gates:")
    print(f"  Perfect Devices (100.0000%): {stats['perfect_count']} ({stats['perfect_count']/stats['total']*100:.2f}%)")
    print(f"  Near-Perfect (99.9-99.99%): {stats['passed_count'] - stats['perfect_count']} ({(stats['passed_count']-stats['perfect_count'])/stats['total']*100:.2f}%)")
    print(f"  Passed Threshold: {stats['passed_count']} ({stats['passed_count']/stats['total']*100:.2f}%)")
    print(f"  Failed Threshold: {stats['total'] - stats['passed_count']}")
    print(f"  Critical Data Loss: {stats['critical_count']}")
    print(f"  Avg Data Loss: {stats['avg_data_loss']:.4f}%")

    # Get threshold configuration
    cursor.execute('SELECT min_overall_score, max_data_loss_percentage FROM pqa_thresholds WHERE active = 1')
    threshold = cursor.fetchone()
    if threshold:
        print(f"\nActive Threshold Configuration:")
        print(f"  Min Overall Score: {threshold[0]}%")
        print(f"  Max Data Loss: {threshold[1]}%")

        # Check why devices failed
        cursor.execute('''
            SELECT
                SUM(CASE WHEN overall_score < ? THEN 1 ELSE 0 END) as failed_score,
                SUM(CASE WHEN data_loss_percentage > ? THEN 1 ELSE 0 END) as failed_data_loss,
                SUM(CASE WHEN overall_score >= ? AND data_loss_percentage > ? THEN 1 ELSE 0 END) as failed_only_data_loss
            FROM pqa_quality_metrics
            WHERE file_type = 'IODD' AND passed_threshold = 0
        ''', (threshold[0], threshold[1], threshold[0], threshold[1]))

        failures = cursor.fetchone()
        if failures and (stats['total'] - stats['passed_count']) > 0:
            print(f"\nFailure Breakdown:")
            print(f"  Failed due to low score (<{threshold[0]}%): {failures[0] or 0}")
            print(f"  Failed due to data loss (>{threshold[1]}%): {failures[1] or 0}")
            print(f"  Failed ONLY data loss (good score!): {failures[2] or 0}")

    # 3. Score Distribution Buckets
    print("\n## 3. SCORE DISTRIBUTION\n")

    cursor.execute("""
        SELECT
            CASE
                WHEN overall_score >= 98 THEN 'A+ (98-100%)'
                WHEN overall_score >= 95 THEN 'A  (95-98%)'
                WHEN overall_score >= 90 THEN 'A- (90-95%)'
                WHEN overall_score >= 85 THEN 'B+ (85-90%)'
                WHEN overall_score >= 80 THEN 'B  (80-85%)'
                WHEN overall_score >= 75 THEN 'B- (75-80%)'
                WHEN overall_score >= 70 THEN 'C  (70-75%)'
                WHEN overall_score >= 60 THEN 'D  (60-70%)'
                ELSE 'F  (<60%)'
            END as grade,
            COUNT(*) as count
        FROM pqa_quality_metrics
        WHERE file_type = 'IODD'
        GROUP BY grade
        ORDER BY MIN(overall_score) DESC
    """)

    print("Grade Distribution:")
    for row in cursor.fetchall():
        pct = row['count'] / stats['total'] * 100
        bar = '#' * int(pct / 2)
        print(f"  {row['grade']}: {row['count']:3d} devices ({pct:5.1f}%) {bar}")

    # 4. Worst Performing Devices
    print("\n## 4. WORST PERFORMING DEVICES (Bottom 10)\n")

    cursor.execute("""
        SELECT
            d.id,
            d.product_name,
            d.manufacturer,
            pqm.overall_score,
            pqm.structural_score,
            pqm.attribute_score,
            pqm.value_score,
            pqm.missing_elements,
            pqm.missing_attributes,
            pqm.data_loss_percentage
        FROM pqa_quality_metrics pqm
        JOIN devices d ON pqm.device_id = d.id
        WHERE pqm.file_type = 'IODD'
        ORDER BY pqm.overall_score ASC
        LIMIT 10
    """)

    print(f"{'ID':<5} {'Product':<40} {'Score':>6} {'Struct':>6} {'Attr':>6} {'Value':>6} {'Loss%':>6}")
    print("-" * 90)
    for row in cursor.fetchall():
        print(f"{row['id']:<5} {row['product_name'][:40]:<40} {row['overall_score']:>6.1f} "
              f"{row['structural_score']:>6.1f} {row['attribute_score']:>6.1f} "
              f"{row['value_score']:>6.1f} {row['data_loss_percentage']:>6.1f}")

    # 5. Common Diff Types
    print("\n## 5. MOST COMMON DIFF TYPES\n")

    cursor.execute("""
        SELECT
            diff_type,
            severity,
            COUNT(*) as count
        FROM pqa_diff_details
        GROUP BY diff_type, severity
        ORDER BY count DESC
        LIMIT 15
    """)

    print(f"{'Diff Type':<25} {'Severity':<10} {'Count':>8}")
    print("-" * 50)
    for row in cursor.fetchall():
        print(f"{row['diff_type']:<25} {row['severity']:<10} {row['count']:>8}")

    # 6. Most Common XPath Patterns
    print("\n## 6. MOST PROBLEMATIC ELEMENTS (Top 20)\n")

    cursor.execute("""
        SELECT
            xpath,
            diff_type,
            severity,
            COUNT(*) as occurrences
        FROM pqa_diff_details
        GROUP BY xpath, diff_type, severity
        ORDER BY occurrences DESC
        LIMIT 20
    """)

    print(f"{'XPath (truncated)':<60} {'Type':<20} {'Sev':<8} {'Count':>6}")
    print("-" * 100)
    for row in cursor.fetchall():
        xpath_short = row['xpath'][:58] + '..' if len(row['xpath']) > 60 else row['xpath']
        print(f"{xpath_short:<60} {row['diff_type']:<20} {row['severity']:<8} {row['occurrences']:>6}")

    # 7. Phase-Specific Scores
    print("\n## 7. PHASE-SPECIFIC SCORES (IODD Features)\n")

    cursor.execute("""
        SELECT
            AVG(phase1_score) as avg_phase1,
            AVG(phase2_score) as avg_phase2,
            AVG(phase3_score) as avg_phase3,
            AVG(phase4_score) as avg_phase4,
            AVG(phase5_score) as avg_phase5,
            SUM(CASE WHEN phase1_score = 100.0 THEN 1 ELSE 0 END) as p1_perfect,
            SUM(CASE WHEN phase2_score = 100.0 THEN 1 ELSE 0 END) as p2_perfect,
            SUM(CASE WHEN phase3_score = 100.0 THEN 1 ELSE 0 END) as p3_perfect,
            SUM(CASE WHEN phase4_score = 100.0 THEN 1 ELSE 0 END) as p4_perfect,
            SUM(CASE WHEN phase5_score = 100.0 THEN 1 ELSE 0 END) as p5_perfect
        FROM pqa_quality_metrics
        WHERE file_type = 'IODD'
    """)

    phases = cursor.fetchone()
    total = stats['total']

    def format_phase(score, perfect_count):
        status = "Perfect" if score == 100.0 else f"{perfect_count}/{total} perfect"
        indicator = "✓" if score == 100.0 else "⚠" if score >= 99.0 else "!"
        return f"{score:.4f}%  {indicator} {status}"

    print(f"Phase 1 (UI Rendering):          {format_phase(phases['avg_phase1'], phases['p1_perfect'])}")
    print(f"Phase 2 (Variants & Conditions): {format_phase(phases['avg_phase2'], phases['p2_perfect'])}")
    print(f"Phase 3 (Menu Buttons):          {format_phase(phases['avg_phase3'], phases['p3_perfect'])}")
    print(f"Phase 4 (Wiring & Test Config):  {format_phase(phases['avg_phase4'], phases['p4_perfect'])}")
    print(f"Phase 5 (Custom Datatypes):      {format_phase(phases['avg_phase5'], phases['p5_perfect'])}")

    # 8. Tickets Generated
    print("\n## 8. PQA TICKETS GENERATED\n")

    cursor.execute("""
        SELECT
            COUNT(*) as total_tickets,
            SUM(CASE WHEN priority = 'critical' THEN 1 ELSE 0 END) as critical,
            SUM(CASE WHEN priority = 'high' THEN 1 ELSE 0 END) as high,
            SUM(CASE WHEN priority = 'medium' THEN 1 ELSE 0 END) as medium,
            SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open_tickets
        FROM tickets
        WHERE category = 'parser_quality'
    """)

    tickets = cursor.fetchone()
    if tickets['total_tickets']:
        print(f"Total PQA Tickets: {tickets['total_tickets']}")
        print(f"  Critical: {tickets['critical']}")
        print(f"  High:     {tickets['high']}")
        print(f"  Medium:   {tickets['medium']}")
        print(f"  Open:     {tickets['open_tickets']}")
    else:
        print("No PQA tickets generated.")

    # 9. Example Critical Issues
    print("\n## 9. EXAMPLE CRITICAL ISSUES (Sample of 10)\n")

    cursor.execute("""
        SELECT
            pdd.xpath,
            pdd.expected_value,
            pdd.actual_value,
            pdd.description,
            d.product_name
        FROM pqa_diff_details pdd
        JOIN pqa_quality_metrics pqm ON pdd.metric_id = pqm.id
        JOIN devices d ON pqm.device_id = d.id
        WHERE pdd.severity = 'CRITICAL'
        LIMIT 10
    """)

    critical_issues = cursor.fetchall()
    if critical_issues:
        for i, issue in enumerate(critical_issues, 1):
            print(f"\n{i}. Device: {issue['product_name']}")
            print(f"   XPath: {issue['xpath']}")
            print(f"   Expected: {issue['expected_value']}")
            print(f"   Actual: {issue['actual_value']}")
            print(f"   Description: {issue['description']}")
    else:
        print("No critical issues found!")

    # 10. Summary Assessment
    print("\n" + "="*80)
    print("## 10. SUMMARY ASSESSMENT")
    print("="*80)

    if stats['avg_overall'] >= 95:
        grade = "EXCELLENT"
        status = "✅ Production Ready"
    elif stats['avg_overall'] >= 90:
        grade = "VERY GOOD"
        status = "✅ Production Acceptable"
    elif stats['avg_overall'] >= 85:
        grade = "GOOD"
        status = "⚠️ Minor Issues"
    elif stats['avg_overall'] >= 80:
        grade = "ACCEPTABLE"
        status = "⚠️ Needs Review"
    else:
        grade = "POOR"
        status = "🚨 Critical Issues"

    print(f"\nOverall Grade: {grade} ({stats['avg_overall']}%)")
    print(f"Status: {status}")
    print(f"\nKey Metrics:")
    print(f"  - {stats['passed_count']} of {stats['total']} devices pass threshold (≥95%)")
    print(f"  - {stats['critical_count']} devices with critical data loss")
    print(f"  - Average data loss: {stats['avg_data_loss']}%")

    conn.close()

if __name__ == '__main__':
    analyze_pqa_results()
