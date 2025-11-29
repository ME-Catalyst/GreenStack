"""
Import IODD files from a specific dataset

Usage:
  python import_dataset.py datasets/quick-test
  python import_dataset.py datasets/my-test --fresh --pqa
"""
import argparse
import sys
import logging
from pathlib import Path
from src.parsing import IODDParser
from src.storage import StorageManager

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def import_dataset(dataset_path, fresh=False):
    """Import all IODD files from a dataset"""

    dataset_dir = Path('test-data/datasets') / dataset_path if not Path(dataset_path).exists() else Path(dataset_path)

    if not dataset_dir.exists():
        logger.error(f"Dataset not found: {dataset_dir}")
        return False

    # Find all XML files in dataset
    iodd_files = list(dataset_dir.glob('*.xml'))

    if not iodd_files:
        logger.error(f"No IODD files found in {dataset_dir}")
        return False

    logger.info(f"Found {len(iodd_files)} IODD files in dataset")
    logger.info(f"Dataset: {dataset_dir}")

    # Fresh database if requested
    if fresh:
        import os
        logger.info("Deleting existing database...")
        for f in ['greenstack.db', 'greenstack.db-shm', 'greenstack.db-wal']:
            if os.path.exists(f):
                os.remove(f)
                logger.info(f"  Deleted {f}")

    # Import files
    storage_manager = StorageManager('greenstack.db')

    success = 0
    failed = 0
    errors = []

    for idx, iodd_file in enumerate(iodd_files, 1):
        try:
            logger.info(f"[{idx}/{len(iodd_files)}] Importing {iodd_file.name}...")
            parser = IODDParser(str(iodd_file))
            device_id = storage_manager.save_device(parser)
            success += 1
            logger.info(f"  ✓ Saved as device {device_id}")
        except Exception as e:
            failed += 1
            error_msg = f"{iodd_file.name}: {str(e)}"
            errors.append(error_msg)
            logger.error(f"  ✗ Failed: {e}")

    # Summary
    logger.info(f"\n{'='*60}")
    logger.info(f"Import Summary")
    logger.info(f"{'='*60}")
    logger.info(f"  Success: {success}")
    logger.info(f"  Failed:  {failed}")
    logger.info(f"  Total:   {len(iodd_files)}")

    if errors:
        logger.info(f"\nErrors:")
        for err in errors:
            logger.info(f"  - {err}")

    return failed == 0

def main():
    parser = argparse.ArgumentParser(description='Import IODD dataset')
    parser.add_argument('dataset', help='Dataset directory name (under test-data/datasets/)')
    parser.add_argument('--fresh', action='store_true', help='Delete existing database first')
    parser.add_argument('--pqa', action='store_true', help='Run PQA analysis after import')

    args = parser.parse_args()

    # Import dataset
    success = import_dataset(args.dataset, args.fresh)

    # Run PQA if requested
    if success and args.pqa:
        logger.info(f"\n{'='*60}")
        logger.info("Running PQA Analysis...")
        logger.info(f"{'='*60}\n")
        import subprocess
        result = subprocess.run([sys.executable, 'run_pqa_analysis.py'],
                              capture_output=False)
        if result.returncode != 0:
            logger.error("PQA analysis failed")
            return 1

    return 0 if success else 1

if __name__ == '__main__':
    exit(main())
