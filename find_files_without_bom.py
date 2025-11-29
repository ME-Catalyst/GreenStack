"""Find IODD files without UTF-8 BOM for testing"""
from pathlib import Path
import random

SOURCE_DIR = Path('test-data/iodd-extracted')

def has_bom(file_path):
    """Check if file has UTF-8 BOM"""
    try:
        with open(file_path, 'rb') as f:
            first_bytes = f.read(3)
            return first_bytes == b'\xef\xbb\xbf'
    except:
        return True  # If error, skip file

# Find all XML files
all_files = list(SOURCE_DIR.rglob('*.xml'))
print(f"Total IODD files: {len(all_files)}")

# Filter out files with BOM
files_without_bom = []
files_with_bom = []

for f in all_files:
    if has_bom(f):
        files_with_bom.append(f)
    else:
        files_without_bom.append(f)

print(f"Files without BOM: {len(files_without_bom)}")
print(f"Files with BOM: {len(files_with_bom)}")

if files_without_bom:
    # Sample 20 files for quick test
    sample_size = min(20, len(files_without_bom))
    sample = random.sample(files_without_bom, sample_size)

    print(f"\nSelected {sample_size} files for quick-test dataset:")
    for f in sample:
        print(f"  {f.name}")

    # Save file list
    with open('files_without_bom.txt', 'w') as out:
        for f in sample:
            out.write(f"{f}\n")

    print(f"\nFile list saved to files_without_bom.txt")
else:
    print("\nNo files without BOM found!")
