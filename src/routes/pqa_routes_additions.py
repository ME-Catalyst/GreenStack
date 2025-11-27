"""
New PQA Dashboard Endpoints - To be appended to pqa_routes.py

These endpoints provide enhanced metrics for the granular dashboard:
- Score distribution
- Diff type breakdown
- XPath pattern analysis
- Device drill-down details
"""

# Add these endpoints to the end of pqa_routes.py (before the final closing)


@router.get("/dashboard/score-distribution")
async def get_score_distribution(file_type: Optional[str] = Query(None, description="Filter by IODD or EDS")):
    """
    Get score distribution across buckets for histogram visualization

    Returns counts of devices in different score ranges:
    - Perfect (100.0000%)
    - Near-Perfect (99.900-99.999%)
    - Excellent (99.500-99.899%)
    - Good (99.000-99.499%)
    - Acceptable (95.000-98.999%)
    - Below Threshold (<95%)
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Build filter
        file_type_filter = ""
        params = []
        if file_type:
            file_type_upper = file_type.upper()
            if file_type_upper not in ['IODD', 'EDS']:
                raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")
            file_type_filter = "WHERE file_type = ?"
            params.append(file_type_upper)

        # Get distribution counts
        cursor.execute(f"""
            SELECT
                SUM(CASE WHEN overall_score = 100.0 THEN 1 ELSE 0 END) as perfect,
                SUM(CASE WHEN overall_score >= 99.900 AND overall_score < 100.0 THEN 1 ELSE 0 END) as near_perfect,
                SUM(CASE WHEN overall_score >= 99.500 AND overall_score < 99.900 THEN 1 ELSE 0 END) as excellent,
                SUM(CASE WHEN overall_score >= 99.000 AND overall_score < 99.500 THEN 1 ELSE 0 END) as good,
                SUM(CASE WHEN overall_score >= 95.000 AND overall_score < 99.000 THEN 1 ELSE 0 END) as acceptable,
                SUM(CASE WHEN overall_score < 95.000 THEN 1 ELSE 0 END) as below_threshold,
                COUNT(*) as total
            FROM pqa_quality_metrics
            {file_type_filter}
        """, params)

        counts = cursor.fetchone()
        conn.close()

        total = counts['total'] or 1  # Avoid division by zero

        return {
            "buckets": [
                {
                    "range": "100.0000%",
                    "label": "Perfect",
                    "count": counts['perfect'],
                    "percentage": round(counts['perfect'] / total * 100, 2)
                },
                {
                    "range": "99.900-99.999%",
                    "label": "Near-Perfect",
                    "count": counts['near_perfect'],
                    "percentage": round(counts['near_perfect'] / total * 100, 2)
                },
                {
                    "range": "99.500-99.899%",
                    "label": "Excellent",
                    "count": counts['excellent'],
                    "percentage": round(counts['excellent'] / total * 100, 2)
                },
                {
                    "range": "99.000-99.499%",
                    "label": "Good",
                    "count": counts['good'],
                    "percentage": round(counts['good'] / total * 100, 2)
                },
                {
                    "range": "95.000-98.999%",
                    "label": "Acceptable",
                    "count": counts['acceptable'],
                    "percentage": round(counts['acceptable'] / total * 100, 2)
                },
                {
                    "range": "<95.000%",
                    "label": "Below Threshold",
                    "count": counts['below_threshold'],
                    "percentage": round(counts['below_threshold'] / total * 100, 2)
                }
            ],
            "total": total,
            "perfect_count": counts['perfect'],
            "near_perfect_count": counts['near_perfect']
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching score distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/diff-distribution")
async def get_diff_distribution(file_type: Optional[str] = Query(None, description="Filter by IODD or EDS")):
    """
    Get distribution of diff types for pie chart visualization

    Returns counts of each diff type grouped by severity:
    - missing_attribute
    - missing_element
    - incorrect_attribute
    - value_changed
    - extra_element
    - type_changed
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Build filter - need to join with metrics to filter by file_type
        file_type_filter = ""
        params = []
        if file_type:
            file_type_upper = file_type.upper()
            if file_type_upper not in ['IODD', 'EDS']:
                raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")
            file_type_filter = "WHERE pqm.file_type = ?"
            params.append(file_type_upper)

        # Get diff type counts
        cursor.execute(f"""
            SELECT
                pdd.diff_type,
                pdd.severity,
                COUNT(*) as count
            FROM pqa_diff_details pdd
            JOIN pqa_quality_metrics pqm ON pdd.metric_id = pqm.id
            {file_type_filter}
            GROUP BY pdd.diff_type, pdd.severity
            ORDER BY count DESC
        """, params)

        diffs = cursor.fetchall()

        # Get total diffs and device count
        cursor.execute(f"""
            SELECT
                COUNT(DISTINCT pdd.id) as total_diffs,
                COUNT(DISTINCT pqm.device_id) as devices_analyzed
            FROM pqa_diff_details pdd
            JOIN pqa_quality_metrics pqm ON pdd.metric_id = pqm.id
            {file_type_filter}
        """, params)

        totals = cursor.fetchone()
        conn.close()

        diff_list = [
            {
                "type": d['diff_type'],
                "severity": d['severity'],
                "count": d['count'],
                "label": f"{d['diff_type']} ({d['severity']})"
            }
            for d in diffs
        ]

        return {
            "diff_types": diff_list,
            "total_diffs": totals['total_diffs'] or 0,
            "devices_analyzed": totals['devices_analyzed'] or 0,
            "avg_diffs_per_device": round(
                (totals['total_diffs'] or 0) / (totals['devices_analyzed'] or 1), 2
            )
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching diff distribution: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/xpath-patterns")
async def get_xpath_patterns(
    limit: int = Query(20, ge=1, le=100),
    severity: Optional[str] = Query(None, description="Filter by severity: CRITICAL, HIGH, MEDIUM, LOW"),
    file_type: Optional[str] = Query(None, description="Filter by IODD or EDS")
):
    """
    Get most common XPath patterns with issues

    Returns aggregated patterns showing:
    - XPath pattern
    - Diff type
    - Severity
    - Count of occurrences
    - Example affected device IDs
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Build filters
        filters = []
        params = []

        if severity:
            severity_upper = severity.upper()
            if severity_upper not in ['CRITICAL', 'HIGH', 'MEDIUM', 'LOW', 'INFO']:
                raise HTTPException(status_code=400, detail="Invalid severity")
            filters.append("pdd.severity = ?")
            params.append(severity_upper)

        if file_type:
            file_type_upper = file_type.upper()
            if file_type_upper not in ['IODD', 'EDS']:
                raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")
            filters.append("pqm.file_type = ?")
            params.append(file_type_upper)

        where_clause = "WHERE " + " AND ".join(filters) if filters else ""

        # Get XPath patterns
        cursor.execute(f"""
            SELECT
                pdd.xpath,
                pdd.diff_type,
                pdd.severity,
                COUNT(*) as occurrences,
                GROUP_CONCAT(DISTINCT pqm.device_id) as device_ids,
                MIN(pdd.expected_value) as example_expected,
                MIN(pdd.actual_value) as example_actual,
                MIN(pdd.description) as description
            FROM pqa_diff_details pdd
            JOIN pqa_quality_metrics pqm ON pdd.metric_id = pqm.id
            {where_clause}
            GROUP BY pdd.xpath, pdd.diff_type, pdd.severity
            ORDER BY occurrences DESC
            LIMIT ?
        """, params + [limit])

        patterns = cursor.fetchall()
        conn.close()

        return {
            "patterns": [
                {
                    "xpath": p['xpath'],
                    "diff_type": p['diff_type'],
                    "severity": p['severity'],
                    "count": p['occurrences'],
                    "affected_devices": [int(id) for id in (p['device_ids'] or '').split(',')[:10] if id],  # Limit to 10 IDs
                    "example_expected": p['example_expected'],
                    "example_actual": p['example_actual'],
                    "description": p['description']
                }
                for p in patterns
            ],
            "total_patterns": len(patterns)
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching XPath patterns: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/device/{device_id}/analysis")
async def get_device_analysis(device_id: int):
    """
    Get detailed PQA analysis for a specific device

    Returns:
    - Device metadata (product name, manufacturer)
    - Latest PQA scores
    - All diffs with details
    - Grouped diff summary
    - Recommended fixes
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get device info
        cursor.execute("""
            SELECT product_name, manufacturer, device_id
            FROM devices
            WHERE id = ?
        """, (device_id,))

        device = cursor.fetchone()
        if not device:
            conn.close()
            raise HTTPException(status_code=404, detail="Device not found")

        # Get latest PQA metrics
        cursor.execute("""
            SELECT *
            FROM pqa_quality_metrics
            WHERE device_id = ?
            ORDER BY analysis_timestamp DESC
            LIMIT 1
        """, (device_id,))

        metrics = cursor.fetchone()
        if not metrics:
            conn.close()
            return {
                "device_id": device_id,
                "product_name": device['product_name'],
                "manufacturer": device['manufacturer'],
                "has_analysis": False,
                "message": "No PQA analysis found for this device"
            }

        # Get all diffs for this device
        cursor.execute("""
            SELECT *
            FROM pqa_diff_details
            WHERE metric_id = ?
            ORDER BY
                CASE severity
                    WHEN 'CRITICAL' THEN 1
                    WHEN 'HIGH' THEN 2
                    WHEN 'MEDIUM' THEN 3
                    WHEN 'LOW' THEN 4
                    ELSE 5
                END,
                xpath
        """, (metrics['id'],))

        diffs = cursor.fetchall()
        conn.close()

        # Group diffs by type
        grouped_diffs = {}
        for diff in diffs:
            diff_type = diff['diff_type']
            if diff_type not in grouped_diffs:
                grouped_diffs[diff_type] = 0
            grouped_diffs[diff_type] += 1

        # Generate recommended fixes based on common patterns
        recommended_fixes = []
        for diff in diffs[:5]:  # Top 5 issues
            if diff['diff_type'] == 'missing_attribute' and 'fixedLength' in diff['xpath']:
                recommended_fixes.append("Add fixedLength attribute storage to CustomDatatypeSaver")
            elif diff['diff_type'] == 'missing_attribute' and 'encoding' in diff['xpath']:
                recommended_fixes.append("Add encoding attribute to StringT datatype handling")
            elif diff['diff_type'] == 'missing_element' and 'EventCollection' in diff['xpath']:
                recommended_fixes.append("Output empty EventCollection element when no events exist")

        # Remove duplicates
        recommended_fixes = list(dict.fromkeys(recommended_fixes))

        return {
            "device_id": device_id,
            "product_name": device['product_name'],
            "manufacturer": device['manufacturer'],
            "has_analysis": True,
            "analysis_timestamp": metrics['analysis_timestamp'],
            "scores": {
                "overall": metrics['overall_score'],
                "structural": metrics['structural_score'],
                "attribute": metrics['attribute_score'],
                "value": metrics['value_score'],
                "data_loss": metrics['data_loss_percentage']
            },
            "phases": {
                "phase1": metrics['phase1_score'],
                "phase2": metrics['phase2_score'],
                "phase3": metrics['phase3_score'],
                "phase4": metrics['phase4_score'],
                "phase5": metrics['phase5_score']
            },
            "diff_count": len(diffs),
            "grouped_diffs": grouped_diffs,
            "diffs": [
                {
                    "xpath": d['xpath'],
                    "diff_type": d['diff_type'],
                    "severity": d['severity'],
                    "expected": d['expected_value'],
                    "actual": d['actual_value'],
                    "description": d['description']
                }
                for d in diffs
            ],
            "recommended_fixes": recommended_fixes,
            "passed_threshold": bool(metrics['passed_threshold']),
            "critical_data_loss": bool(metrics['critical_data_loss'])
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching device analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/phase-breakdown")
async def get_phase_breakdown(
    phase: Optional[int] = Query(None, ge=1, le=5, description="Filter by phase (1-5)"),
    file_type: Optional[str] = Query(None, description="Filter by IODD or EDS")
):
    """
    Get detailed breakdown of phase-specific scores

    Shows:
    - Average score per phase
    - Count of perfect devices per phase
    - Count of devices with issues per phase
    - Common issues in each phase
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Build filter
        file_type_filter = ""
        params = []
        if file_type:
            file_type_upper = file_type.upper()
            if file_type_upper not in ['IODD', 'EDS']:
                raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")
            file_type_filter = "WHERE file_type = ?"
            params.append(file_type_upper)

        # Get phase statistics
        cursor.execute(f"""
            SELECT
                AVG(phase1_score) as avg_phase1,
                AVG(phase2_score) as avg_phase2,
                AVG(phase3_score) as avg_phase3,
                AVG(phase4_score) as avg_phase4,
                AVG(phase5_score) as avg_phase5,
                SUM(CASE WHEN phase1_score = 100.0 THEN 1 ELSE 0 END) as perfect_phase1,
                SUM(CASE WHEN phase2_score = 100.0 THEN 1 ELSE 0 END) as perfect_phase2,
                SUM(CASE WHEN phase3_score = 100.0 THEN 1 ELSE 0 END) as perfect_phase3,
                SUM(CASE WHEN phase4_score = 100.0 THEN 1 ELSE 0 END) as perfect_phase4,
                SUM(CASE WHEN phase5_score = 100.0 THEN 1 ELSE 0 END) as perfect_phase5,
                COUNT(*) as total
            FROM pqa_quality_metrics
            {file_type_filter}
        """, params)

        stats = cursor.fetchone()
        conn.close()

        total = stats['total'] or 1

        phases = [
            {
                "phase": 1,
                "name": "UI Rendering (gradient, offset, displayFormat)",
                "avg_score": stats['avg_phase1'],
                "perfect_count": stats['perfect_phase1'],
                "perfect_percentage": round(stats['perfect_phase1'] / total * 100, 2),
                "issues_count": total - stats['perfect_phase1']
            },
            {
                "phase": 2,
                "name": "Variants & Conditions (DeviceVariant, ProcessDataCondition)",
                "avg_score": stats['avg_phase2'],
                "perfect_count": stats['perfect_phase2'],
                "perfect_percentage": round(stats['perfect_phase2'] / total * 100, 2),
                "issues_count": total - stats['perfect_phase2']
            },
            {
                "phase": 3,
                "name": "Menu Buttons (RoleMenuSets, ObserverRoleMenu)",
                "avg_score": stats['avg_phase3'],
                "perfect_count": stats['perfect_phase3'],
                "perfect_percentage": round(stats['perfect_phase3'] / total * 100, 2),
                "issues_count": total - stats['perfect_phase3']
            },
            {
                "phase": 4,
                "name": "Wiring & Test Config (WireConfiguration, TestConfiguration)",
                "avg_score": stats['avg_phase4'],
                "perfect_count": stats['perfect_phase4'],
                "perfect_percentage": round(stats['perfect_phase4'] / total * 100, 2),
                "issues_count": total - stats['perfect_phase4']
            },
            {
                "phase": 5,
                "name": "Custom Datatypes (RecordT, ArrayT, DatatypeCollection)",
                "avg_score": stats['avg_phase5'],
                "perfect_count": stats['perfect_phase5'],
                "perfect_percentage": round(stats['perfect_phase5'] / total * 100, 2),
                "issues_count": total - stats['perfect_phase5']
            }
        ]

        if phase:
            # Return only requested phase
            phases = [p for p in phases if p['phase'] == phase]

        return {
            "phases": phases,
            "total_devices": total
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching phase breakdown: {e}")
        raise HTTPException(status_code=500, detail=str(e))
