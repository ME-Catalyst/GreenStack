"""
Create curated IODD datasets for targeted testing

Usage examples:
  # Create quick test dataset (first 20 files)
  python create_dataset.py --quick-test --output datasets/quick-test

  # Create dataset from specific vendor
  python create_dataset.py --vendor 303 --limit 50 --output datasets/vendor-303

  # Create dataset with ArrayT datatypes
  python create_dataset.py --with-pattern "ArrayT" --output datasets/arrayt-test
"""
import argparse
import shutil
from pathlib import Path
import re
import logging

logging.basicConfig(level=logging.INFO, format='%(message)s')
logger = logging.getLogger(__name__)

SOURCE_DIR = Path('test-data/iodd-extracted')
DATASETS_DIR = Path('test-data/datasets')

def find_iodd_files(**kwargs):
    """Find IODD files matching criteria"""
    all_files = list(SOURCE_DIR.rglob('*.xml'))

    logger.info(f"Searching {len(all_files)} total IODD files...")

    matched = all_files

    # Filter by vendor ID
    if kwargs.get('vendor'):
        vendor = str(kwargs['vendor'])
        matched = [f for f in matched if f'-{vendor}-' in f.name or f'_{vendor}_' in f.name]
        logger.info(f"  Filtered by vendor {vendor}: {len(matched)} files")

    # Filter by pattern in filename or content
    if kwargs.get('pattern'):
        pattern = kwargs['pattern']
        if kwargs.get('content_search'):
            # Search file content (slower)
            content_matched = []
            for f in matched:
                try:
                    if re.search(pattern, f.read_text(), re.IGNORECASE):
                        content_matched.append(f)
                except:
                    pass
            matched = content_matched
            logger.info(f"  Filtered by content pattern '{pattern}': {len(matched)} files")
        else:
            # Search filename only (faster)
            matched = [f for f in matched if re.search(pattern, f.name, re.IGNORECASE)]
            logger.info(f"  Filtered by filename pattern '{pattern}': {len(matched)} files")

    # Limit results
    if kwargs.get('limit'):
        matched = matched[:kwargs['limit']]
        logger.info(f"  Limited to {len(matched)} files")

    return matched

def create_quick_test_dataset(output_dir, limit=20):
    """Create a quick test dataset with diverse files"""
    logger.info(f"Creating quick-test dataset with {limit} files...")

    # Get a sampling of files from different vendors
    all_files = list(SOURCE_DIR.rglob('*.xml'))

    # Try to get diverse sample
    vendors_seen = set()
    selected = []

    for f in all_files:
        # Extract vendor from filename (common patterns)
        vendor_match = re.search(r'[-_](\d{3})[-_]', f.name)
        if vendor_match:
            vendor = vendor_match.group(1)
            if vendor not in vendors_seen or len(selected) >= limit:
                selected.append(f)
                vendors_seen.add(vendor)

        if len(selected) >= limit:
            break

    # Fill remaining slots if needed
    if len(selected) < limit:
        for f in all_files:
            if f not in selected:
                selected.append(f)
            if len(selected) >= limit:
                break

    logger.info(f"Selected {len(selected)} files from {len(vendors_seen)} different vendors")
    return selected

def copy_to_dataset(files, output_dir, create_symlinks=False):
    """Copy files to dataset directory"""
    output_path = DATASETS_DIR / output_dir
    output_path.mkdir(parents=True, exist_ok=True)

    logger.info(f"\nCopying {len(files)} files to {output_path}...")

    copied = 0
    for f in files:
        dest = output_path / f.name
        try:
            if create_symlinks:
                if not dest.exists():
                    dest.symlink_to(f.absolute())
                    copied += 1
            else:
                shutil.copy2(f, dest)
                copied += 1
        except Exception as e:
            logger.warning(f"  Failed to copy {f.name}: {e}")

    logger.info(f"Successfully copied {copied} files")

    # Create manifest
    manifest_path = output_path / 'manifest.txt'
    with open(manifest_path, 'w') as mf:
        mf.write(f"# Dataset: {output_dir}\n")
        mf.write(f"# Created: {Path.cwd()}\n")
        mf.write(f"# File count: {copied}\n\n")
        for f in sorted(files, key=lambda x: x.name):
            mf.write(f"{f.name}\n")

    logger.info(f"Created manifest: {manifest_path}")
    return output_path

def main():
    parser = argparse.ArgumentParser(description='Create IODD test datasets')
    parser.add_argument('--output', required=True, help='Output dataset directory name')
    parser.add_argument('--quick-test', action='store_true', help='Create quick test dataset (20 diverse files)')
    parser.add_argument('--vendor', type=int, help='Filter by vendor ID')
    parser.add_argument('--pattern', help='Filter by filename pattern (regex)')
    parser.add_argument('--content-pattern', help='Filter by file content pattern (slower)')
    parser.add_argument('--limit', type=int, help='Limit number of files')
    parser.add_argument('--symlinks', action='store_true', help='Create symlinks instead of copies (faster, Windows requires admin)')

    args = parser.parse_args()

    if args.quick_test:
        files = create_quick_test_dataset(args.output, args.limit or 20)
    else:
        kwargs = {}
        if args.vendor:
            kwargs['vendor'] = args.vendor
        if args.pattern:
            kwargs['pattern'] = args.pattern
        if args.content_pattern:
            kwargs['pattern'] = args.content_pattern
            kwargs['content_search'] = True
        if args.limit:
            kwargs['limit'] = args.limit

        files = find_iodd_files(**kwargs)

    if not files:
        logger.error("No files matched criteria!")
        return 1

    output_path = copy_to_dataset(files, args.output, args.symlinks)

    logger.info(f"\n✓ Dataset created: {output_path}")
    logger.info(f"  Files: {len(files)}")
    logger.info(f"\nTo import:")
    logger.info(f"  python import_dataset.py {args.output}")

    return 0

if __name__ == '__main__':
    exit(main())
