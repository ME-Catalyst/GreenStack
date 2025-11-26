"""
PQA (Parser Quality Assurance) API Routes

REST endpoints for forensic reconstruction, diff analysis, and quality metrics.
"""

from fastapi import APIRouter, HTTPException, BackgroundTasks, Query
from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
import sqlite3
import logging

from ..utils.pqa_orchestrator import (
    UnifiedPQAOrchestrator, FileType, analyze_iodd_quality, analyze_eds_quality
)
from ..utils.forensic_reconstruction_v2 import reconstruct_iodd_xml
from ..utils.eds_reconstruction import reconstruct_eds_file

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/api/pqa", tags=["Parser Quality Assurance"])


# Pydantic Models
class AnalysisRequest(BaseModel):
    """Request to run PQA analysis"""
    device_id: int = Field(..., description="Device ID (IODD) or EDS file ID")
    file_type: str = Field(..., description="File type: 'IODD' or 'EDS'")
    original_content: Optional[str] = Field(None, description="Original file content (if not in archive)")


class QualityMetricsResponse(BaseModel):
    """Quality metrics response"""
    id: int
    device_id: int
    analysis_timestamp: str
    overall_score: float
    structural_score: float
    attribute_score: float
    value_score: float
    data_loss_percentage: float
    critical_data_loss: bool
    passed_threshold: bool
    phase1_score: float
    phase2_score: float
    phase3_score: float
    phase4_score: float
    phase5_score: float
    total_elements_original: int
    total_elements_reconstructed: int
    missing_elements: int
    extra_elements: int


class DiffDetailResponse(BaseModel):
    """Individual diff detail"""
    id: int
    diff_type: str
    severity: str
    xpath: str
    expected_value: Optional[str]
    actual_value: Optional[str]
    description: str
    phase: Optional[str]


class ThresholdConfig(BaseModel):
    """Quality threshold configuration"""
    id: Optional[int] = None
    threshold_name: str
    description: Optional[str] = None
    min_overall_score: float = 95.0
    min_structural_score: float = 98.0
    min_attribute_score: float = 95.0
    min_value_score: float = 90.0
    max_data_loss_percentage: float = 1.0
    allow_critical_data_loss: bool = False
    auto_ticket_on_fail: bool = True
    auto_analysis_on_import: bool = False
    email_notifications: bool = False
    active: bool = True


class DashboardSummary(BaseModel):
    """Dashboard summary statistics"""
    total_analyses: int
    passed_analyses: int
    failed_analyses: int
    average_score: float
    devices_analyzed: int
    critical_failures: int
    recent_analyses: List[Dict[str, Any]]


# Database helper
def get_db():
    """Get database connection"""
    conn = sqlite3.connect("greenstack.db")
    conn.row_factory = sqlite3.Row
    return conn


# ============================================================================
# ANALYSIS ENDPOINTS
# ============================================================================

@router.post("/analyze", response_model=Dict[str, Any])
async def run_pqa_analysis(
    request: AnalysisRequest,
    background_tasks: BackgroundTasks
):
    """
    Run comprehensive PQA analysis

    Workflow:
    1. Archive original file
    2. Reconstruct from database
    3. Perform diff analysis
    4. Save quality metrics
    5. Generate ticket if needed

    Returns immediate response with job queued for background processing.
    """
    try:
        # Validate file type
        if request.file_type.upper() not in ['IODD', 'EDS']:
            raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")

        # Check if device/file exists
        conn = get_db()
        cursor = conn.cursor()

        if request.file_type.upper() == 'IODD':
            cursor.execute("SELECT id, product_name FROM devices WHERE id = ?", (request.device_id,))
        else:
            cursor.execute("SELECT id, product_name FROM eds_files WHERE id = ?", (request.device_id,))

        device = cursor.fetchone()
        conn.close()

        if not device:
            raise HTTPException(status_code=404, detail=f"{request.file_type} file {request.device_id} not found")

        # Get original content
        if not request.original_content:
            # Try to retrieve from archive
            conn = get_db()
            cursor = conn.cursor()
            cursor.execute("""
                SELECT file_content FROM pqa_file_archive
                WHERE device_id = ? AND file_type = ?
                ORDER BY upload_timestamp DESC LIMIT 1
            """, (request.device_id, request.file_type.upper()))
            archive = cursor.fetchone()
            conn.close()

            if not archive:
                raise HTTPException(
                    status_code=400,
                    detail="original_content required - no archive found for this device"
                )

            original_content = archive['file_content'].decode('utf-8')
        else:
            original_content = request.original_content

        # Queue analysis in background
        file_type = FileType[request.file_type.upper()]

        def run_analysis():
            try:
                orchestrator = UnifiedPQAOrchestrator()
                metrics, diffs = orchestrator.run_full_analysis(
                    request.device_id,
                    file_type,
                    original_content
                )
                logger.info(f"PQA analysis completed for {request.file_type} {request.device_id}: {metrics.overall_score:.1f}%")
            except Exception as e:
                logger.error(f"PQA analysis failed: {e}")

        background_tasks.add_task(run_analysis)

        return {
            "status": "queued",
            "message": f"PQA analysis queued for {request.file_type} {request.device_id}",
            "device_id": request.device_id,
            "file_type": request.file_type
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error queueing PQA analysis: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/analyze-all", response_model=Dict[str, Any])
async def run_pqa_analysis_all(
    background_tasks: BackgroundTasks,
    file_type: Optional[str] = Query(None, description="Filter by file type: IODD or EDS. If not specified, analyzes all types")
):
    """
    Run PQA analysis on all devices/files

    This endpoint queues analysis for all IODD devices and/or EDS files.
    Analysis runs in background for optimal performance.

    Args:
        file_type: Optional filter - 'IODD', 'EDS', or None for both

    Returns:
        Summary of queued analyses
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        queued_count = 0
        iodd_count = 0
        eds_count = 0

        # Queue IODD analyses
        if not file_type or file_type.upper() == 'IODD':
            cursor.execute("SELECT id, product_name FROM devices")
            iodd_devices = cursor.fetchall()

            for device in iodd_devices:
                device_id = device['id']

                # Get XML content
                cursor.execute("""
                    SELECT file_content FROM iodd_assets
                    WHERE device_id = ? AND file_type = 'xml'
                    LIMIT 1
                """, (device_id,))
                xml_row = cursor.fetchone()

                if xml_row:
                    xml_content = xml_row['file_content']
                    if isinstance(xml_content, bytes):
                        xml_content = xml_content.decode('utf-8')

                    # Queue analysis using functools.partial to avoid closure issues
                    from functools import partial

                    def run_iodd_analysis(device_id: int, xml_content: str):
                        try:
                            orchestrator = UnifiedPQAOrchestrator()
                            orchestrator.run_full_analysis(device_id, FileType.IODD, xml_content)
                            logger.info(f"Completed PQA analysis for IODD device {device_id}")
                        except Exception as e:
                            logger.error(f"PQA analysis failed for IODD {device_id}: {e}", exc_info=True)

                    background_tasks.add_task(run_iodd_analysis, device_id, xml_content)
                    queued_count += 1
                    iodd_count += 1

        # Queue EDS analyses
        if not file_type or file_type.upper() == 'EDS':
            cursor.execute("SELECT id, product_name, eds_content FROM eds_files")
            eds_files = cursor.fetchall()

            for eds_file in eds_files:
                eds_id = eds_file['id']
                eds_content = eds_file['eds_content']

                if eds_content:
                    # Queue analysis
                    def run_eds_analysis(eds_id: int, eds_content: str):
                        try:
                            orchestrator = UnifiedPQAOrchestrator()
                            orchestrator.run_full_analysis(eds_id, FileType.EDS, eds_content)
                            logger.info(f"Completed PQA analysis for EDS file {eds_id}")
                        except Exception as e:
                            logger.error(f"PQA analysis failed for EDS {eds_id}: {e}", exc_info=True)

                    background_tasks.add_task(run_eds_analysis, eds_id, eds_content)
                    queued_count += 1
                    eds_count += 1

        conn.close()

        return {
            "status": "queued",
            "message": f"Queued {queued_count} analyses ({iodd_count} IODD, {eds_count} EDS)",
            "total_queued": queued_count,
            "iodd_queued": iodd_count,
            "eds_queued": eds_count
        }

    except Exception as e:
        logger.error(f"Error queuing bulk analyses: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/analyzed-devices", response_model=List[Dict[str, Any]])
async def get_analyzed_devices():
    """
    Get list of all devices that have been analyzed

    Returns a list of devices with their latest analysis metrics.
    Useful for the Analysis History list view.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Get all unique device/file combinations with analyses
        cursor.execute("""
            SELECT DISTINCT
                m.device_id,
                a.file_type
            FROM pqa_quality_metrics m
            JOIN pqa_file_archive a ON m.archive_id = a.id
        """)

        device_combos = cursor.fetchall()

        result = []
        for combo in device_combos:
            device_id = combo['device_id']
            file_type = combo['file_type']

            # Get latest metrics for this device/file_type
            cursor.execute("""
                SELECT
                    m.overall_score,
                    m.passed_threshold,
                    m.analysis_timestamp,
                    COUNT(*) OVER() as analysis_count
                FROM pqa_quality_metrics m
                JOIN pqa_file_archive a ON m.archive_id = a.id
                WHERE m.device_id = ? AND a.file_type = ?
                ORDER BY m.analysis_timestamp DESC
                LIMIT 1
            """, (device_id, file_type))

            latest = cursor.fetchone()

            if not latest:
                continue

            # Get device name
            if file_type == 'IODD':
                cursor.execute("SELECT product_name, manufacturer FROM devices WHERE id = ?", (device_id,))
            else:
                cursor.execute("SELECT product_name, vendor_name FROM eds_files WHERE id = ?", (device_id,))

            device_row = cursor.fetchone()

            # Count total analyses for this device/file_type
            cursor.execute("""
                SELECT COUNT(*) as count
                FROM pqa_quality_metrics m
                JOIN pqa_file_archive a ON m.archive_id = a.id
                WHERE m.device_id = ? AND a.file_type = ?
            """, (device_id, file_type))
            count_row = cursor.fetchone()

            # Get vendor name - column name differs between IODD and EDS tables
            vendor_name = None
            if device_row:
                if file_type == 'IODD':
                    vendor_name = device_row['manufacturer']
                else:
                    vendor_name = device_row['vendor_name']

            result.append({
                "id": device_id,
                "file_type": file_type,
                "product_name": device_row['product_name'] if device_row else f"Unknown Device {device_id}",
                "vendor_name": vendor_name,
                "latest_analysis": latest['analysis_timestamp'],
                "analysis_count": count_row['count'] if count_row else 0,
                "latest_score": latest['overall_score'],
                "passed": bool(latest['passed_threshold'])
            })

        # Sort by latest analysis timestamp descending
        result.sort(key=lambda x: x['latest_analysis'], reverse=True)

        conn.close()
        return result

    except Exception as e:
        logger.error(f"Error fetching analyzed devices: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{device_id}", response_model=QualityMetricsResponse)
async def get_latest_metrics(device_id: int, file_type: str = Query("IODD", description="IODD or EDS")):
    """Get latest quality metrics for a device"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.*, a.file_type
            FROM pqa_quality_metrics m
            JOIN pqa_file_archive a ON m.archive_id = a.id
            WHERE m.device_id = ? AND a.file_type = ?
            ORDER BY m.analysis_timestamp DESC
            LIMIT 1
        """, (device_id, file_type.upper()))

        metric = cursor.fetchone()
        conn.close()

        if not metric:
            raise HTTPException(status_code=404, detail=f"No metrics found for {file_type} {device_id}")

        return QualityMetricsResponse(
            id=metric['id'],
            device_id=metric['device_id'],
            analysis_timestamp=metric['analysis_timestamp'],
            overall_score=metric['overall_score'],
            structural_score=metric['structural_score'],
            attribute_score=metric['attribute_score'],
            value_score=metric['value_score'],
            data_loss_percentage=metric['data_loss_percentage'],
            critical_data_loss=bool(metric['critical_data_loss']),
            passed_threshold=bool(metric['passed_threshold']),
            phase1_score=metric['phase1_score'] or 0.0,
            phase2_score=metric['phase2_score'] or 0.0,
            phase3_score=metric['phase3_score'] or 0.0,
            phase4_score=metric['phase4_score'] or 0.0,
            phase5_score=metric['phase5_score'] or 0.0,
            total_elements_original=metric['total_elements_original'] or 0,
            total_elements_reconstructed=metric['total_elements_reconstructed'] or 0,
            missing_elements=metric['missing_elements'] or 0,
            extra_elements=metric['extra_elements'] or 0
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching metrics: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/by-id/{metric_id}", response_model=QualityMetricsResponse)
async def get_metrics_by_id(metric_id: int):
    """Get quality metrics by metric ID"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.*, a.file_type
            FROM pqa_quality_metrics m
            JOIN pqa_file_archive a ON m.archive_id = a.id
            WHERE m.id = ?
        """, (metric_id,))

        metric = cursor.fetchone()
        conn.close()

        if not metric:
            raise HTTPException(status_code=404, detail=f"Metric {metric_id} not found")

        return QualityMetricsResponse(
            id=metric['id'],
            device_id=metric['device_id'],
            analysis_timestamp=metric['analysis_timestamp'],
            overall_score=metric['overall_score'],
            structural_score=metric['structural_score'],
            attribute_score=metric['attribute_score'],
            value_score=metric['value_score'],
            data_loss_percentage=metric['data_loss_percentage'],
            critical_data_loss=bool(metric['critical_data_loss']),
            passed_threshold=bool(metric['passed_threshold']),
            phase1_score=metric['phase1_score'] or 0.0,
            phase2_score=metric['phase2_score'] or 0.0,
            phase3_score=metric['phase3_score'] or 0.0,
            phase4_score=metric['phase4_score'] or 0.0,
            phase5_score=metric['phase5_score'] or 0.0,
            total_elements_original=metric['total_elements_original'] or 0,
            total_elements_reconstructed=metric['total_elements_reconstructed'] or 0,
            missing_elements=metric['missing_elements'] or 0,
            extra_elements=metric['extra_elements'] or 0,
            file_type=metric['file_type']
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching metric {metric_id}: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/metrics/{device_id}/history", response_model=List[QualityMetricsResponse])
async def get_metrics_history(
    device_id: int,
    file_type: str = Query("IODD"),
    limit: int = Query(10, ge=1, le=100)
):
    """Get historical quality metrics for a device"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT m.*, a.file_type
            FROM pqa_quality_metrics m
            JOIN pqa_file_archive a ON m.archive_id = a.id
            WHERE m.device_id = ? AND a.file_type = ?
            ORDER BY m.analysis_timestamp DESC
            LIMIT ?
        """, (device_id, file_type.upper(), limit))

        metrics = cursor.fetchall()
        conn.close()

        return [
            QualityMetricsResponse(
                id=m['id'],
                device_id=m['device_id'],
                analysis_timestamp=m['analysis_timestamp'],
                overall_score=m['overall_score'],
                structural_score=m['structural_score'],
                attribute_score=m['attribute_score'],
                value_score=m['value_score'],
                data_loss_percentage=m['data_loss_percentage'],
                critical_data_loss=bool(m['critical_data_loss']),
                passed_threshold=bool(m['passed_threshold']),
                phase1_score=m['phase1_score'] or 0.0,
                phase2_score=m['phase2_score'] or 0.0,
                phase3_score=m['phase3_score'] or 0.0,
                phase4_score=m['phase4_score'] or 0.0,
                phase5_score=m['phase5_score'] or 0.0,
                total_elements_original=m['total_elements_original'] or 0,
                total_elements_reconstructed=m['total_elements_reconstructed'] or 0,
                missing_elements=m['missing_elements'] or 0,
                extra_elements=m['extra_elements'] or 0
            )
            for m in metrics
        ]

    except Exception as e:
        logger.error(f"Error fetching metrics history: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/diff/{metric_id}", response_model=List[DiffDetailResponse])
async def get_diff_details(metric_id: int, severity: Optional[str] = None):
    """Get detailed diff items for a quality metric"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        if severity:
            cursor.execute("""
                SELECT * FROM pqa_diff_details
                WHERE metric_id = ? AND severity = ?
                ORDER BY id
            """, (metric_id, severity.upper()))
        else:
            cursor.execute("""
                SELECT * FROM pqa_diff_details
                WHERE metric_id = ?
                ORDER BY severity, id
            """, (metric_id,))

        diffs = cursor.fetchall()
        conn.close()

        return [
            DiffDetailResponse(
                id=d['id'],
                diff_type=d['diff_type'],
                severity=d['severity'],
                xpath=d['xpath'],
                expected_value=d['expected_value'],
                actual_value=d['actual_value'],
                description=d['description'],
                phase=d['phase']
            )
            for d in diffs
        ]

    except Exception as e:
        logger.error(f"Error fetching diff details: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# RECONSTRUCTION ENDPOINTS
# ============================================================================

@router.get("/reconstruct/{device_id}", response_model=Dict[str, Any])
async def get_reconstructed_file(device_id: int, file_type: str = Query("IODD")):
    """Get reconstructed IODD/EDS file from database"""
    try:
        if file_type.upper() == 'IODD':
            reconstructed = reconstruct_iodd_xml(device_id)
        elif file_type.upper() == 'EDS':
            reconstructed = reconstruct_eds_file(device_id)
        else:
            raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")

        return {
            "device_id": device_id,
            "file_type": file_type,
            "content": reconstructed,
            "length": len(reconstructed)
        }

    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))
    except Exception as e:
        logger.error(f"Error reconstructing file: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/archive/{device_id}", response_model=Dict[str, Any])
async def get_archived_file(device_id: int, file_type: str = Query("IODD")):
    """Get archived original file"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT * FROM pqa_file_archive
            WHERE device_id = ? AND file_type = ?
            ORDER BY upload_timestamp DESC
            LIMIT 1
        """, (device_id, file_type.upper()))

        archive = cursor.fetchone()
        conn.close()

        if not archive:
            raise HTTPException(status_code=404, detail=f"No archive found for {file_type} {device_id}")

        return {
            "id": archive['id'],
            "device_id": archive['device_id'],
            "file_type": archive['file_type'],
            "filename": archive['filename'],
            "file_hash": archive['file_hash'],
            "content": archive['file_content'].decode('utf-8'),
            "file_size": archive['file_size'],
            "upload_timestamp": archive['upload_timestamp'],
            "parser_version": archive['parser_version']
        }

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching archive: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# THRESHOLD MANAGEMENT
# ============================================================================

@router.get("/thresholds", response_model=List[ThresholdConfig])
async def get_thresholds():
    """Get all quality thresholds"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("SELECT * FROM pqa_thresholds ORDER BY created_at DESC")
        thresholds = cursor.fetchall()
        conn.close()

        return [
            ThresholdConfig(
                id=t['id'],
                threshold_name=t['threshold_name'],
                description=t['description'],
                min_overall_score=t['min_overall_score'] if t['min_overall_score'] is not None else 95.0,
                min_structural_score=t['min_structural_score'] if t['min_structural_score'] is not None else 98.0,
                min_attribute_score=t['min_attribute_score'] if t['min_attribute_score'] is not None else 95.0,
                min_value_score=t['min_value_score'] if t['min_value_score'] is not None else 90.0,
                max_data_loss_percentage=t['max_data_loss_percentage'] if t['max_data_loss_percentage'] is not None else 1.0,
                allow_critical_data_loss=bool(t['allow_critical_data_loss']) if t['allow_critical_data_loss'] is not None else False,
                auto_ticket_on_fail=bool(t['auto_ticket_on_fail']) if t['auto_ticket_on_fail'] is not None else True,
                auto_analysis_on_import=bool(t['auto_analysis_on_import']) if t['auto_analysis_on_import'] is not None else False,
                email_notifications=bool(t['email_notifications']) if t['email_notifications'] is not None else False,
                active=bool(t['active']) if t['active'] is not None else True
            )
            for t in thresholds
        ]

    except Exception as e:
        logger.error(f"Error fetching thresholds: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/thresholds", response_model=Dict[str, Any])
async def create_threshold(threshold: ThresholdConfig):
    """Create new quality threshold configuration"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO pqa_thresholds (
                threshold_name, description, min_overall_score, min_structural_score,
                min_attribute_score, min_value_score, max_data_loss_percentage,
                allow_critical_data_loss, auto_ticket_on_fail, auto_analysis_on_import,
                email_notifications, active
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            threshold.threshold_name,
            threshold.description,
            threshold.min_overall_score,
            threshold.min_structural_score,
            threshold.min_attribute_score,
            threshold.min_value_score,
            threshold.max_data_loss_percentage,
            1 if threshold.allow_critical_data_loss else 0,
            1 if threshold.auto_ticket_on_fail else 0,
            1 if threshold.auto_analysis_on_import else 0,
            1 if threshold.email_notifications else 0,
            1 if threshold.active else 0
        ))

        threshold_id = cursor.lastrowid
        conn.commit()
        conn.close()

        return {"id": threshold_id, "message": "Threshold created successfully"}

    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Threshold name already exists")
    except Exception as e:
        logger.error(f"Error creating threshold: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.put("/thresholds/{threshold_id}", response_model=Dict[str, Any])
async def update_threshold(threshold_id: int, threshold: ThresholdConfig):
    """Update existing threshold configuration"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            UPDATE pqa_thresholds SET
                threshold_name = ?,
                description = ?,
                min_overall_score = ?,
                min_structural_score = ?,
                min_attribute_score = ?,
                min_value_score = ?,
                max_data_loss_percentage = ?,
                allow_critical_data_loss = ?,
                auto_ticket_on_fail = ?,
                auto_analysis_on_import = ?,
                email_notifications = ?,
                active = ?,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = ?
        """, (
            threshold.threshold_name,
            threshold.description,
            threshold.min_overall_score,
            threshold.min_structural_score,
            threshold.min_attribute_score,
            threshold.min_value_score,
            threshold.max_data_loss_percentage,
            1 if threshold.allow_critical_data_loss else 0,
            1 if threshold.auto_ticket_on_fail else 0,
            1 if threshold.auto_analysis_on_import else 0,
            1 if threshold.email_notifications else 0,
            1 if threshold.active else 0,
            threshold_id
        ))

        if cursor.rowcount == 0:
            conn.close()
            raise HTTPException(status_code=404, detail="Threshold not found")

        conn.commit()
        conn.close()

        return {"message": "Threshold updated successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error updating threshold: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/thresholds/{threshold_id}", response_model=Dict[str, Any])
async def delete_threshold(threshold_id: int):
    """Delete a quality threshold configuration"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Check if threshold exists
        cursor.execute("SELECT threshold_name FROM pqa_thresholds WHERE id = ?", (threshold_id,))
        threshold = cursor.fetchone()

        if not threshold:
            conn.close()
            raise HTTPException(status_code=404, detail="Threshold not found")

        # Don't allow deleting the default threshold
        if threshold['threshold_name'] == 'default':
            conn.close()
            raise HTTPException(status_code=400, detail="Cannot delete the default threshold")

        cursor.execute("DELETE FROM pqa_thresholds WHERE id = ?", (threshold_id,))
        conn.commit()
        conn.close()

        return {"message": "Threshold deleted successfully"}

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error deleting threshold: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# ============================================================================
# DASHBOARD ENDPOINTS
# ============================================================================

@router.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary(file_type: Optional[str] = Query(None, description="Filter by file type: IODD or EDS")):
    """
    Get PQA dashboard summary statistics

    Can be filtered by file_type to show IODD-only or EDS-only statistics,
    or show combined statistics if no filter is applied.
    """
    try:
        conn = get_db()
        cursor = conn.cursor()

        # Build WHERE clause for file_type filtering
        file_type_filter = ""
        params = []
        if file_type:
            file_type_upper = file_type.upper()
            if file_type_upper not in ['IODD', 'EDS']:
                raise HTTPException(status_code=400, detail="file_type must be 'IODD' or 'EDS'")
            file_type_filter = "WHERE file_type = ?"
            params.append(file_type_upper)

        # Total analyses
        cursor.execute(f"SELECT COUNT(*) FROM pqa_quality_metrics {file_type_filter}", params)
        total_analyses = cursor.fetchone()[0]

        # Passed/Failed
        cursor.execute(f"SELECT COUNT(*) FROM pqa_quality_metrics {file_type_filter} {'AND' if file_type_filter else 'WHERE'} passed_threshold = 1",
                      params)
        passed = cursor.fetchone()[0]
        failed = total_analyses - passed

        # Average score
        cursor.execute(f"SELECT AVG(overall_score) FROM pqa_quality_metrics {file_type_filter}", params)
        avg_score = cursor.fetchone()[0] or 0.0

        # Unique devices
        cursor.execute(f"SELECT COUNT(DISTINCT device_id) FROM pqa_quality_metrics {file_type_filter}", params)
        devices_analyzed = cursor.fetchone()[0]

        # Critical failures
        cursor.execute(f"SELECT COUNT(*) FROM pqa_quality_metrics {file_type_filter} {'AND' if file_type_filter else 'WHERE'} critical_data_loss = 1",
                      params)
        critical_failures = cursor.fetchone()[0]

        # Recent analyses
        cursor.execute(f"""
            SELECT
                id,
                device_id,
                overall_score,
                passed_threshold,
                analysis_timestamp,
                file_type
            FROM pqa_quality_metrics
            {file_type_filter}
            ORDER BY analysis_timestamp DESC
            LIMIT 10
        """, params)
        recent = cursor.fetchall()

        conn.close()

        return DashboardSummary(
            total_analyses=total_analyses,
            passed_analyses=passed,
            failed_analyses=failed,
            average_score=avg_score,
            devices_analyzed=devices_analyzed,
            critical_failures=critical_failures,
            recent_analyses=[
                {
                    "id": r['id'],
                    "device_id": r['device_id'],
                    "file_type": r['file_type'],
                    "overall_score": r['overall_score'],
                    "passed": bool(r['passed_threshold']),
                    "timestamp": r['analysis_timestamp']
                }
                for r in recent
            ]
        )

    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error fetching dashboard summary: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/trends")
async def get_quality_trends(days: int = Query(30, ge=1, le=365)):
    """Get quality score trends over time"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                DATE(analysis_timestamp) as date,
                AVG(overall_score) as avg_score,
                MIN(overall_score) as min_score,
                MAX(overall_score) as max_score,
                COUNT(*) as analysis_count
            FROM pqa_quality_metrics
            WHERE analysis_timestamp >= datetime('now', '-' || ? || ' days')
            GROUP BY DATE(analysis_timestamp)
            ORDER BY date
        """, (days,))

        trends = cursor.fetchall()
        conn.close()

        return [
            {
                "date": t['date'],
                "avg_score": t['avg_score'],
                "min_score": t['min_score'],
                "max_score": t['max_score'],
                "count": t['analysis_count']
            }
            for t in trends
        ]

    except Exception as e:
        logger.error(f"Error fetching trends: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/dashboard/failures")
async def get_quality_failures(limit: int = Query(20, ge=1, le=100)):
    """Get list of quality analysis failures"""
    try:
        conn = get_db()
        cursor = conn.cursor()

        cursor.execute("""
            SELECT
                m.*,
                a.file_type,
                a.filename
            FROM pqa_quality_metrics m
            JOIN pqa_file_archive a ON m.archive_id = a.id
            WHERE m.passed_threshold = 0
            ORDER BY m.analysis_timestamp DESC
            LIMIT ?
        """, (limit,))

        failures = cursor.fetchall()
        conn.close()

        return [
            {
                "id": f['id'],
                "device_id": f['device_id'],
                "file_type": f['file_type'],
                "filename": f['filename'],
                "overall_score": f['overall_score'],
                "data_loss_percentage": f['data_loss_percentage'],
                "critical_data_loss": bool(f['critical_data_loss']),
                "timestamp": f['analysis_timestamp'],
                "ticket_generated": bool(f['ticket_generated'])
            }
            for f in failures
        ]

    except Exception as e:
        logger.error(f"Error fetching failures: {e}")
        raise HTTPException(status_code=500, detail=str(e))
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
