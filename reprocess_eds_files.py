"""
Reprocess all EDS files with the corrected EDSDiffAnalyzer
"""
import sqlite3
from src.utils.pqa_orchestrator import UnifiedPQAOrchestrator, FileType
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def reprocess_all_eds_files():
    """Reprocess all EDS files to get accurate PQA metrics"""

    conn = sqlite3.connect('greenstack.db')
    cursor = conn.cursor()

    # Get all EDS files with content
    cursor.execute("SELECT id, eds_content, product_name FROM eds_files WHERE eds_content IS NOT NULL")
    eds_files = cursor.fetchall()

    total_files = len(eds_files)
    print(f"\n[START] Found {total_files} EDS files to reprocess")
    print("="*80)

    orchestrator = UnifiedPQAOrchestrator()
    processed = 0
    errors = 0

    for eds_id, eds_content, product_name in eds_files:
        try:
            print(f"\n[{processed+1}/{total_files}] Processing EDS file {eds_id}: {product_name}")

            metrics, diffs = orchestrator.run_full_analysis(
                file_id=eds_id,
                file_type=FileType.EDS,
                original_content=eds_content
            )

            print(f"  Overall Score: {metrics.overall_score:.2f}%")
            print(f"  Sections: {metrics.total_sections_original} -> {metrics.total_sections_reconstructed}")
            print(f"  Keys: {metrics.total_keys_original}")
            print(f"  Diffs: {len(diffs)}")

            processed += 1

        except Exception as e:
            logger.error(f"  [ERROR] Failed to process EDS file {eds_id}: {e}")
            errors += 1

    conn.close()

    print("\n" + "="*80)
    print(f"[COMPLETE] Processed {processed} files successfully, {errors} errors")
    print("="*80)

    return processed, errors

if __name__ == "__main__":
    processed, errors = reprocess_all_eds_files()

    if errors == 0:
        print("\n[SUCCESS] All EDS files reprocessed successfully!")
    else:
        print(f"\n[WARNING] {errors} files had errors during reprocessing")
