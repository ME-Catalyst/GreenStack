#!/usr/bin/env python3
"""Test script to import all IODD files and identify any schema errors"""

import glob
import requests
import time
from pathlib import Path

API_BASE = "http://localhost:8000"
TEST_FILES_DIR = "F:/github/GreenStack/test-data/iodd-files"

def test_import_all_iodd_files():
    """Import all IODD files and report results"""

    # Get all zip files
    files = glob.glob(f"{TEST_FILES_DIR}/*.zip") + glob.glob(f"{TEST_FILES_DIR}/*.ZIP")
    files = sorted(files)

    print(f"\n{'='*80}")
    print(f"Testing {len(files)} IODD files")
    print(f"{'='*80}\n")

    results = {
        'success': [],
        'failed': []
    }

    for i, filepath in enumerate(files, 1):
        filename = Path(filepath).name
        print(f"[{i}/{len(files)}] Testing: {filename}...", end=" ")

        try:
            with open(filepath, 'rb') as f:
                files_data = {'file': (filename, f, 'application/zip')}
                response = requests.post(
                    f"{API_BASE}/api/iodd/upload",
                    files=files_data,
                    timeout=30
                )

                if response.status_code == 200:
                    print("[OK] SUCCESS")
                    results['success'].append(filename)
                else:
                    error_detail = response.json().get('detail', response.text)
                    print(f"[FAIL] ({response.status_code})")
                    print(f"   Error: {error_detail}")
                    results['failed'].append({
                        'file': filename,
                        'status': response.status_code,
                        'error': error_detail
                    })

        except requests.exceptions.RequestException as e:
            print(f"[FAIL] REQUEST ERROR")
            print(f"   Error: {str(e)}")
            results['failed'].append({
                'file': filename,
                'status': 'connection_error',
                'error': str(e)
            })
        except Exception as e:
            print(f"[FAIL] ERROR")
            print(f"   Error: {str(e)}")
            results['failed'].append({
                'file': filename,
                'status': 'unknown_error',
                'error': str(e)
            })

        # Small delay between requests
        time.sleep(0.1)

    # Print summary
    print(f"\n{'='*80}")
    print(f"SUMMARY")
    print(f"{'='*80}\n")
    print(f"Total files: {len(files)}")
    print(f"Successful imports: {len(results['success'])} ({len(results['success'])/len(files)*100:.1f}%)")
    print(f"Failed imports: {len(results['failed'])} ({len(results['failed'])/len(files)*100:.1f}%)")

    if results['failed']:
        print(f"\n{'='*80}")
        print(f"FAILED IMPORTS DETAILS")
        print(f"{'='*80}\n")
        for failure in results['failed']:
            print(f"File: {failure['file']}")
            print(f"Status: {failure['status']}")
            print(f"Error: {failure['error']}")
            print()

    return results

if __name__ == "__main__":
    results = test_import_all_iodd_files()
