"""
PQA Automated Scheduler

Handles automated PQA analysis scheduling:
- Run on server startup for unanalyzed devices
- Daily scheduled runs
- Re-analysis of failed/old analyses
"""

import logging
import sqlite3
import threading
import time
from datetime import datetime, timedelta
from typing import Optional

from .pqa_orchestrator import UnifiedPQAOrchestrator, FileType

logger = logging.getLogger(__name__)


class PQAScheduler:
    """
    Automated PQA Analysis Scheduler

    Runs PQA analyses automatically on:
    - Server startup (for unanalyzed devices)
    - Daily schedule
    - Manual triggers
    """

    def __init__(self, db_path: str = "greenstack.db", enabled: bool = True):
        self.db_path = db_path
        self.enabled = enabled
        self.orchestrator = UnifiedPQAOrchestrator(db_path)
        self._stop_flag = threading.Event()
        self._scheduler_thread: Optional[threading.Thread] = None
        self._startup_complete = False

    def start(self):
        """Start the PQA scheduler"""
        if not self.enabled:
            logger.info("PQA scheduler is disabled")
            return

        logger.info("Starting PQA scheduler...")

        # Run startup analysis in background thread
        startup_thread = threading.Thread(target=self._run_startup_analysis, daemon=True)
        startup_thread.start()

        # Start daily scheduler thread
        self._scheduler_thread = threading.Thread(target=self._daily_scheduler_loop, daemon=True)
        self._scheduler_thread.start()

        logger.info("PQA scheduler started successfully")

    def stop(self):
        """Stop the PQA scheduler"""
        logger.info("Stopping PQA scheduler...")
        self._stop_flag.set()
        if self._scheduler_thread:
            self._scheduler_thread.join(timeout=5)
        logger.info("PQA scheduler stopped")

    def _run_startup_analysis(self):
        """Run PQA analysis for all unanalyzed devices on server startup"""
        try:
            logger.info("Running PQA startup analysis for unanalyzed devices...")

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            analyzed_count = 0
            failed_count = 0

            # Find IODD devices without PQA analysis
            cursor.execute("""
                SELECT d.id, d.product_name
                FROM devices d
                LEFT JOIN pqa_quality_metrics pqm ON d.id = pqm.device_id
                WHERE pqm.id IS NULL
            """)
            unanalyzed_iodds = cursor.fetchall()

            logger.info(f"Found {len(unanalyzed_iodds)} unanalyzed IODD devices")

            for device in unanalyzed_iodds:
                if self._stop_flag.is_set():
                    break

                device_id = device['id']

                try:
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

                        # Run analysis
                        self.orchestrator.run_full_analysis(device_id, FileType.IODD, xml_content)
                        analyzed_count += 1
                        logger.info(f"Startup PQA: Analyzed IODD device {device_id} ({device['product_name']})")
                    else:
                        logger.warning(f"No XML content found for IODD device {device_id}")

                except Exception as e:
                    failed_count += 1
                    logger.error(f"Startup PQA failed for IODD {device_id}: {e}", exc_info=True)

            # Find EDS files without PQA analysis
            cursor.execute("""
                SELECT e.id, e.product_name
                FROM eds_files e
                LEFT JOIN pqa_quality_metrics pqm ON e.id = pqm.device_id AND pqm.id IN (
                    SELECT id FROM pqa_file_archive WHERE file_type = 'EDS'
                )
                WHERE pqm.id IS NULL
            """)
            unanalyzed_eds = cursor.fetchall()

            logger.info(f"Found {len(unanalyzed_eds)} unanalyzed EDS files")

            for eds_file in unanalyzed_eds:
                if self._stop_flag.is_set():
                    break

                eds_id = eds_file['id']

                try:
                    # Get EDS content
                    cursor.execute("SELECT eds_content FROM eds_files WHERE id = ?", (eds_id,))
                    content_row = cursor.fetchone()

                    if content_row and content_row['eds_content']:
                        eds_content = content_row['eds_content']

                        # Run analysis
                        self.orchestrator.run_full_analysis(eds_id, FileType.EDS, eds_content)
                        analyzed_count += 1
                        logger.info(f"Startup PQA: Analyzed EDS file {eds_id} ({eds_file['product_name']})")
                    else:
                        logger.warning(f"No EDS content found for file {eds_id}")

                except Exception as e:
                    failed_count += 1
                    logger.error(f"Startup PQA failed for EDS {eds_id}: {e}", exc_info=True)

            conn.close()

            self._startup_complete = True
            logger.info(f"Startup PQA analysis complete: {analyzed_count} analyzed, {failed_count} failed")

        except Exception as e:
            logger.error(f"Startup PQA analysis error: {e}", exc_info=True)

    def _daily_scheduler_loop(self):
        """Background thread for daily PQA scheduling"""
        logger.info("Daily PQA scheduler thread started")

        # Calculate next run time (tomorrow at 2 AM)
        next_run = self._get_next_daily_run_time()
        logger.info(f"Next daily PQA run scheduled for: {next_run}")

        while not self._stop_flag.is_set():
            try:
                # Check if it's time to run
                now = datetime.now()
                if now >= next_run:
                    logger.info("Starting daily PQA analysis...")
                    self._run_daily_analysis()

                    # Schedule next run
                    next_run = self._get_next_daily_run_time()
                    logger.info(f"Next daily PQA run scheduled for: {next_run}")

                # Sleep for 1 hour before checking again
                self._stop_flag.wait(timeout=3600)

            except Exception as e:
                logger.error(f"Daily scheduler error: {e}", exc_info=True)
                self._stop_flag.wait(timeout=3600)  # Wait an hour before retrying

    def _get_next_daily_run_time(self) -> datetime:
        """Calculate next daily run time (2 AM tomorrow)"""
        now = datetime.now()
        next_run = now.replace(hour=2, minute=0, second=0, microsecond=0)

        # If 2 AM today has passed, schedule for tomorrow
        if next_run <= now:
            next_run += timedelta(days=1)

        return next_run

    def _run_daily_analysis(self):
        """Run daily PQA analysis - re-analyze all devices"""
        try:
            logger.info("Running daily PQA analysis for all devices...")

            conn = sqlite3.connect(self.db_path)
            conn.row_factory = sqlite3.Row
            cursor = conn.cursor()

            analyzed_count = 0
            failed_count = 0

            # Analyze all IODD devices
            cursor.execute("SELECT id, product_name FROM devices")
            iodd_devices = cursor.fetchall()

            logger.info(f"Daily PQA: Analyzing {len(iodd_devices)} IODD devices")

            for device in iodd_devices:
                if self._stop_flag.is_set():
                    break

                device_id = device['id']

                try:
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

                        # Run analysis
                        self.orchestrator.run_full_analysis(device_id, FileType.IODD, xml_content)
                        analyzed_count += 1

                except Exception as e:
                    failed_count += 1
                    logger.error(f"Daily PQA failed for IODD {device_id}: {e}")

            # Analyze all EDS files
            cursor.execute("SELECT id, product_name, eds_content FROM eds_files")
            eds_files = cursor.fetchall()

            logger.info(f"Daily PQA: Analyzing {len(eds_files)} EDS files")

            for eds_file in eds_files:
                if self._stop_flag.is_set():
                    break

                eds_id = eds_file['id']
                eds_content = eds_file['eds_content']

                if eds_content:
                    try:
                        # Run analysis
                        self.orchestrator.run_full_analysis(eds_id, FileType.EDS, eds_content)
                        analyzed_count += 1

                    except Exception as e:
                        failed_count += 1
                        logger.error(f"Daily PQA failed for EDS {eds_id}: {e}")

            conn.close()

            logger.info(f"Daily PQA analysis complete: {analyzed_count} analyzed, {failed_count} failed")

        except Exception as e:
            logger.error(f"Daily PQA analysis error: {e}", exc_info=True)


# Global scheduler instance
_scheduler: Optional[PQAScheduler] = None


def init_pqa_scheduler(db_path: str = "greenstack.db", enabled: bool = True) -> PQAScheduler:
    """Initialize the global PQA scheduler"""
    global _scheduler

    if _scheduler is None:
        _scheduler = PQAScheduler(db_path, enabled)
        _scheduler.start()

    return _scheduler


def get_pqa_scheduler() -> Optional[PQAScheduler]:
    """Get the global PQA scheduler instance"""
    return _scheduler


def shutdown_pqa_scheduler():
    """Shutdown the global PQA scheduler"""
    global _scheduler

    if _scheduler:
        _scheduler.stop()
        _scheduler = None
