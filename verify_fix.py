"""
Verification script to confirm save_assets fix is properly loaded
Run this AFTER restarting the backend to verify the fix is active
"""
import sys
sys.path.insert(0, '.')

print("=" * 70)
print("GREENSTACK SAVE_ASSETS FIX VERIFICATION")
print("=" * 70)
print()

# Test 1: Import StorageManager from src.storage
print("[1/5] Testing modular StorageManager import...")
try:
    from src.storage import StorageManager
    print("  [OK] Import successful")
except Exception as e:
    print(f"  [FAIL] Import failed: {e}")
    sys.exit(1)

# Test 2: Check if save_assets method exists
print("\n[2/5] Checking save_assets method exists...")
if hasattr(StorageManager, 'save_assets'):
    print("  [OK] save_assets method found")
else:
    print("  [FAIL] save_assets method NOT FOUND")
    sys.exit(1)

# Test 3: Verify method signature
print("\n[3/5] Verifying save_assets signature...")
import inspect
sig = inspect.signature(StorageManager.save_assets)
params = list(sig.parameters.keys())
expected_params = ['self', 'device_id', 'assets']
if params == expected_params:
    print(f"  [OK] Signature correct: {sig}")
else:
    print(f"  [FAIL] Signature mismatch. Expected {expected_params}, got {params}")
    sys.exit(1)

# Test 4: Test instantiation
print("\n[4/5] Testing StorageManager instantiation...")
try:
    sm = StorageManager('test.db')
    if hasattr(sm, 'save_assets'):
        print("  [OK] Instance has save_assets method")
    else:
        print("  [FAIL] Instance missing save_assets method")
        sys.exit(1)
except Exception as e:
    print(f"  [FAIL] Instantiation failed: {e}")
    sys.exit(1)

# Test 5: Test with CachedStorageManager wrapper
print("\n[5/5] Testing with CachedStorageManager wrapper...")
try:
    from src.cached_storage import CachedStorageManager
    cached_sm = CachedStorageManager(sm)
    if hasattr(cached_sm, 'save_assets'):
        print("  [OK] CachedStorageManager has save_assets (via __getattr__)")
    else:
        print("  [FAIL] CachedStorageManager missing save_assets")
        sys.exit(1)
except Exception as e:
    print(f"  [FAIL] CachedStorageManager test failed: {e}")
    sys.exit(1)

# All tests passed
print()
print("=" * 70)
print("[SUCCESS] ALL TESTS PASSED - save_assets fix is correctly loaded!")
print("=" * 70)
print()
print("The backend should now work correctly after restart.")
print("If you still see errors, make sure to:")
print("  1. Stop the running backend (Ctrl+C or close terminal)")
print("  2. Run: scripts\\setup.bat")
print("  3. Try uploading again")
