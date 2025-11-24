"""
Verify setup.bat functionality
"""
import subprocess
import os
from pathlib import Path

print("=" * 80)
print("SETUP.BAT FUNCTIONALITY VERIFICATION")
print("=" * 80)

# Test 1: Check for processes on port 8000
print("\n[1] Checking for processes on port 8000...")
try:
    result = subprocess.run(
        'netstat -ano | findstr ":8000"',
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0 and result.stdout:
        print("    [!] Found processes on port 8000:")
        for line in result.stdout.strip().split('\n'):
            print(f"        {line}")
    else:
        print("    [OK] No processes on port 8000")
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 2: Check for __pycache__ directories
print("\n[2] Checking for Python cache directories...")
cache_dirs = list(Path("F:/github/GreenStack/src").rglob("__pycache__"))
if cache_dirs:
    print(f"    [!] Found {len(cache_dirs)} cache directories:")
    for cache_dir in cache_dirs[:5]:  # Show first 5
        print(f"        {cache_dir}")
    if len(cache_dirs) > 5:
        print(f"        ... and {len(cache_dirs) - 5} more")
else:
    print("    [OK] No cache directories found")

# Test 3: Check Python version
print("\n[3] Checking Python installation...")
try:
    result = subprocess.run(
        'python --version',
        shell=True,
        capture_output=True,
        text=True
    )
    if result.returncode == 0:
        print(f"    [OK] {result.stdout.strip()}")
    else:
        print("    [ERROR] Python check failed")
except Exception as e:
    print(f"    [ERROR] {e}")

# Test 4: Check database file
print("\n[4] Checking database file...")
db_path = Path("F:/github/GreenStack/greenstack.db")
if db_path.exists():
    size_mb = db_path.stat().st_size / (1024 * 1024)
    print(f"    [OK] Database exists: {size_mb:.2f} MB")
else:
    print("    [WARN] Database not found (will be created on first run)")

# Test 5: Check requirements.txt
print("\n[5] Checking requirements.txt...")
req_path = Path("F:/github/GreenStack/requirements.txt")
if req_path.exists():
    with open(req_path) as f:
        lines = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    print(f"    [OK] Found {len(lines)} dependencies")
else:
    print("    [ERROR] requirements.txt not found")

# Test 6: Verify setup.bat file
print("\n[6] Verifying setup.bat structure...")
setup_path = Path("F:/github/GreenStack/scripts/setup.bat")
if setup_path.exists():
    with open(setup_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    checks = {
        "Backend cleanup": "Cleaning up existing backend instances" in content,
        "Cache cleanup": "Clearing Python bytecode cache" in content,
        "Python check": "Checking Python installation" in content,
        "Dependencies": "Installing Python dependencies" in content,
        "Redis check": "Ensuring Redis" in content,
        "Stats update": "Updating codebase statistics" in content,
        "Launch app": "python -m src.start" in content,
        "Error handling": "Application stopped gracefully" in content,
        "Pause on exit": "pause" in content
    }

    print("    Setup.bat contains:")
    all_passed = True
    for check_name, passed in checks.items():
        status = "[OK]" if passed else "[FAIL]"
        print(f"        {status} {check_name}")
        if not passed:
            all_passed = False

    if all_passed:
        print("    [OK] All checks passed")
else:
    print("    [ERROR] setup.bat not found!")

print("\n" + "=" * 80)
print("VERIFICATION COMPLETE")
print("=" * 80)
