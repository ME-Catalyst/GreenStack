"""
Admin Console API Routes
Provides system administration, monitoring, and management endpoints
"""

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse
import sqlite3
import os
import shutil
from datetime import datetime
from pathlib import Path
import tempfile
import json

router = APIRouter(prefix="/api/admin", tags=["Admin Console"])

DB_PATH = "iodd_manager.db"


@router.get("/stats/overview")
async def get_system_overview():
    """
    Get comprehensive system statistics and overview

    Returns:
        System-wide metrics including device counts, storage info, and health status
    """
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Device counts
    cursor.execute("SELECT COUNT(*) FROM devices")
    iodd_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eds_files")
    eds_count = cursor.fetchone()[0]

    # Parameter counts
    cursor.execute("SELECT COUNT(*) FROM parameters")
    iodd_param_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM eds_parameters")
    eds_param_count = cursor.fetchone()[0]

    # Ticket statistics
    cursor.execute("""
        SELECT
            COUNT(*) as total,
            SUM(CASE WHEN status = 'open' THEN 1 ELSE 0 END) as open,
            SUM(CASE WHEN status = 'in_progress' THEN 1 ELSE 0 END) as in_progress,
            SUM(CASE WHEN status = 'resolved' THEN 1 ELSE 0 END) as resolved,
            SUM(CASE WHEN status = 'closed' THEN 1 ELSE 0 END) as closed
        FROM tickets
    """)
    ticket_stats = cursor.fetchone()

    # Recent activity (last 7 days)
    cursor.execute("""
        SELECT COUNT(*) FROM devices
        WHERE import_date >= datetime('now', '-7 days')
    """)
    recent_iodd_imports = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM eds_files
        WHERE import_date >= datetime('now', '-7 days')
    """)
    recent_eds_imports = cursor.fetchone()[0]

    cursor.execute("""
        SELECT COUNT(*) FROM tickets
        WHERE created_at >= datetime('now', '-7 days')
    """)
    recent_tickets = cursor.fetchone()[0]

    # EDS diagnostics summary
    cursor.execute("""
        SELECT
            SUM(diagnostic_error_count + diagnostic_fatal_count) as total_issues,
            SUM(CASE WHEN has_parsing_issues = 1 THEN 1 ELSE 0 END) as files_with_issues
        FROM eds_files
    """)
    eds_diag = cursor.fetchone()

    # Database info
    cursor.execute("SELECT page_count * page_size as size FROM pragma_page_count(), pragma_page_size()")
    db_size = cursor.fetchone()[0]

    # Table counts
    cursor.execute("""
        SELECT name FROM sqlite_master
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    table_count = len(cursor.fetchall())

    conn.close()

    # File system info
    db_file_size = os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0

    # Check for attachments directory
    attachments_dir = Path("ticket_attachments")
    attachments_size = 0
    attachment_count = 0
    if attachments_dir.exists():
        for root, dirs, files in os.walk(attachments_dir):
            attachment_count += len(files)
            for file in files:
                attachments_size += os.path.getsize(os.path.join(root, file))

    return {
        "devices": {
            "iodd": iodd_count,
            "eds": eds_count,
            "total": iodd_count + eds_count
        },
        "parameters": {
            "iodd": iodd_param_count,
            "eds": eds_param_count,
            "total": iodd_param_count + eds_param_count
        },
        "tickets": {
            "total": ticket_stats[0] or 0,
            "open": ticket_stats[1] or 0,
            "in_progress": ticket_stats[2] or 0,
            "resolved": ticket_stats[3] or 0,
            "closed": ticket_stats[4] or 0
        },
        "recent_activity": {
            "iodd_imports": recent_iodd_imports,
            "eds_imports": recent_eds_imports,
            "new_tickets": recent_tickets
        },
        "diagnostics": {
            "total_issues": eds_diag[0] or 0,
            "files_with_issues": eds_diag[1] or 0
        },
        "storage": {
            "database_size_bytes": db_file_size,
            "database_size_mb": round(db_file_size / (1024 * 1024), 2),
            "attachments_size_bytes": attachments_size,
            "attachments_size_mb": round(attachments_size / (1024 * 1024), 2),
            "attachment_count": attachment_count,
            "total_size_mb": round((db_file_size + attachments_size) / (1024 * 1024), 2)
        },
        "database": {
            "table_count": table_count,
            "path": DB_PATH
        },
        "timestamp": datetime.now().isoformat()
    }


@router.get("/stats/devices-by-vendor")
async def get_devices_by_vendor():
    """Get device distribution by vendor"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # IODD devices by vendor
    cursor.execute("""
        SELECT manufacturer, COUNT(*) as count
        FROM devices
        GROUP BY manufacturer
        ORDER BY count DESC
        LIMIT 20
    """)
    iodd_vendors = [{"vendor": row[0], "count": row[1]} for row in cursor.fetchall()]

    # EDS devices by vendor
    cursor.execute("""
        SELECT vendor_name, COUNT(*) as count
        FROM eds_files
        GROUP BY vendor_name
        ORDER BY count DESC
        LIMIT 20
    """)
    eds_vendors = [{"vendor": row[0], "count": row[1]} for row in cursor.fetchall()]

    conn.close()

    return {
        "iodd": iodd_vendors,
        "eds": eds_vendors
    }


@router.get("/stats/database-health")
async def get_database_health():
    """Check database integrity and health"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Integrity check
    cursor.execute("PRAGMA integrity_check")
    integrity = cursor.fetchone()[0]

    # Foreign key check
    cursor.execute("PRAGMA foreign_key_check")
    fk_violations = cursor.fetchall()

    # Get index list
    cursor.execute("""
        SELECT name, tbl_name
        FROM sqlite_master
        WHERE type='index' AND name NOT LIKE 'sqlite_%'
        ORDER BY tbl_name, name
    """)
    indexes = cursor.fetchall()

    # Get table sizes
    cursor.execute("""
        SELECT
            name,
            (SELECT COUNT(*) FROM sqlite_master sm WHERE sm.tbl_name = m.name AND sm.type='index') as index_count
        FROM sqlite_master m
        WHERE type='table' AND name NOT LIKE 'sqlite_%'
        ORDER BY name
    """)
    tables = []
    for table_name, index_count in cursor.fetchall():
        cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
        row_count = cursor.fetchone()[0]
        tables.append({
            "name": table_name,
            "row_count": row_count,
            "index_count": index_count
        })

    conn.close()

    return {
        "integrity": integrity,
        "healthy": integrity == "ok" and len(fk_violations) == 0,
        "foreign_key_violations": len(fk_violations),
        "index_count": len(indexes),
        "tables": tables,
        "timestamp": datetime.now().isoformat()
    }


@router.post("/database/vacuum")
async def vacuum_database():
    """Optimize database by running VACUUM"""
    try:
        # Get size before
        size_before = os.path.getsize(DB_PATH)

        conn = sqlite3.connect(DB_PATH)
        conn.execute("VACUUM")
        conn.close()

        # Get size after
        size_after = os.path.getsize(DB_PATH)
        saved = size_before - size_after

        return {
            "success": True,
            "size_before_mb": round(size_before / (1024 * 1024), 2),
            "size_after_mb": round(size_after / (1024 * 1024), 2),
            "space_saved_mb": round(saved / (1024 * 1024), 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to vacuum database: {str(e)}")


@router.post("/database/backup")
async def backup_database():
    """Create a backup of the database"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_name = f"iodd_manager_backup_{timestamp}.db"
        backup_path = Path("backups") / backup_name

        # Create backups directory
        backup_path.parent.mkdir(exist_ok=True)

        # Copy database
        shutil.copy2(DB_PATH, backup_path)

        backup_size = os.path.getsize(backup_path)

        return {
            "success": True,
            "backup_file": backup_name,
            "backup_path": str(backup_path),
            "size_mb": round(backup_size / (1024 * 1024), 2),
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create backup: {str(e)}")


@router.get("/database/backup/download")
async def download_backup():
    """Download a database backup"""
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        temp_backup = tempfile.NamedTemporaryFile(delete=False, suffix='.db')

        # Copy database to temp file
        shutil.copy2(DB_PATH, temp_backup.name)
        temp_backup.close()

        return FileResponse(
            path=temp_backup.name,
            media_type="application/x-sqlite3",
            filename=f"iodd_manager_backup_{timestamp}.db"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to download backup: {str(e)}")


@router.get("/diagnostics/eds-summary")
async def get_eds_diagnostics_summary():
    """Get summary of EDS parsing diagnostics"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Get files with issues
    cursor.execute("""
        SELECT
            id, product_name, vendor_name,
            diagnostic_info_count, diagnostic_warn_count,
            diagnostic_error_count, diagnostic_fatal_count
        FROM eds_files
        WHERE has_parsing_issues = 1
        ORDER BY (diagnostic_error_count + diagnostic_fatal_count) DESC
        LIMIT 50
    """)

    files_with_issues = []
    for row in cursor.fetchall():
        files_with_issues.append({
            "id": row[0],
            "product_name": row[1],
            "vendor_name": row[2],
            "info": row[3],
            "warnings": row[4],
            "errors": row[5],
            "fatal": row[6],
            "total_issues": row[3] + row[4] + row[5] + row[6]
        })

    # Get diagnostics by severity
    cursor.execute("""
        SELECT severity, COUNT(*) as count
        FROM eds_diagnostics
        GROUP BY severity
        ORDER BY
            CASE severity
                WHEN 'FATAL' THEN 1
                WHEN 'ERROR' THEN 2
                WHEN 'WARN' THEN 3
                WHEN 'INFO' THEN 4
            END
    """)

    by_severity = [{"severity": row[0], "count": row[1]} for row in cursor.fetchall()]

    # Get most common diagnostic codes
    cursor.execute("""
        SELECT code, severity, COUNT(*) as count
        FROM eds_diagnostics
        GROUP BY code, severity
        ORDER BY count DESC
        LIMIT 10
    """)

    common_codes = []
    for row in cursor.fetchall():
        common_codes.append({
            "code": row[0],
            "severity": row[1],
            "count": row[2]
        })

    conn.close()

    return {
        "files_with_issues": files_with_issues,
        "by_severity": by_severity,
        "common_codes": common_codes,
        "total_files_with_issues": len(files_with_issues)
    }


@router.get("/system/info")
async def get_system_info():
    """Get system information"""
    import platform
    import sys

    return {
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "version": platform.version(),
            "machine": platform.machine(),
            "processor": platform.processor()
        },
        "python": {
            "version": sys.version,
            "implementation": platform.python_implementation(),
            "compiler": platform.python_compiler()
        },
        "application": {
            "name": "IODD Manager",
            "version": "2.1.0",
            "database_path": DB_PATH,
            "database_exists": os.path.exists(DB_PATH)
        },
        "timestamp": datetime.now().isoformat()
    }
