"""
Test script to debug delete-all functionality.

This will:
1. Check current device count
2. Call the delete-all API endpoint
3. Check device count after deletion
4. Query database directly to verify
"""
import sqlite3
import requests
import time

DB_PATH = 'F:/github/GreenStack/greenstack.db'
API_URL = 'http://localhost:8000'

def check_device_count():
    """Check device count directly in database"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM devices")
    device_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ui_menus")
    menu_count = cursor.fetchone()[0]

    cursor.execute("SELECT COUNT(*) FROM ui_menu_items")
    menu_item_count = cursor.fetchone()[0]

    conn.close()

    return {
        'devices': device_count,
        'menus': menu_count,
        'menu_items': menu_item_count
    }

def main():
    print("="*80)
    print("DELETE-ALL FUNCTIONALITY TEST")
    print("="*80)

    # Step 1: Check current counts
    print("\n[1/4] Checking current database counts...")
    before = check_device_count()
    print(f"  Devices: {before['devices']}")
    print(f"  Menus: {before['menus']}")
    print(f"  Menu Items: {before['menu_items']}")

    if before['devices'] == 0:
        print("\n⚠️  Database is already empty. Upload some devices first.")
        return

    # Step 2: Call delete-all API
    print("\n[2/4] Calling DELETE /api/admin/database/delete-all...")
    try:
        response = requests.post(f"{API_URL}/api/admin/database/delete-all", timeout=30)
        print(f"  Status Code: {response.status_code}")
        print(f"  Response: {response.json()}")

        if response.status_code != 200:
            print(f"\n❌ API returned error: {response.text}")
            return

    except requests.exceptions.ConnectionError:
        print("\n❌ ERROR: Could not connect to backend server at http://localhost:8000")
        print("   Make sure backend is running: python -m src.api")
        return
    except Exception as e:
        print(f"\n❌ ERROR calling API: {e}")
        return

    # Step 3: Wait a moment for commit
    print("\n[3/4] Waiting 2 seconds for database commit...")
    time.sleep(2)

    # Step 4: Check counts after deletion
    print("\n[4/4] Checking database counts after deletion...")
    after = check_device_count()
    print(f"  Devices: {after['devices']}")
    print(f"  Menus: {after['menus']}")
    print(f"  Menu Items: {after['menu_items']}")

    # Verify deletion
    print("\n" + "="*80)
    if after['devices'] == 0 and after['menus'] == 0 and after['menu_items'] == 0:
        print("✅ DELETE-ALL WORKING CORRECTLY")
        print("   All devices, menus, and menu items were deleted from database.")
    else:
        print("❌ DELETE-ALL FAILED")
        print(f"   Expected: 0 devices, 0 menus, 0 menu items")
        print(f"   Actual: {after['devices']} devices, {after['menus']} menus, {after['menu_items']} menu items")
        print("\n   DEBUGGING INFO:")

        # Check if connection is seeing changes
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Check for WAL mode
        cursor.execute("PRAGMA journal_mode")
        journal_mode = cursor.fetchone()[0]
        print(f"   Database journal mode: {journal_mode}")

        # Check for open transactions
        cursor.execute("PRAGMA wal_checkpoint(FULL)")
        checkpoint = cursor.fetchall()
        print(f"   WAL checkpoint result: {checkpoint}")

        # Try to see if there are orphaned records
        if after['menu_items'] > 0:
            cursor.execute("""
                SELECT menu_id, variable_id, COUNT(*)
                FROM ui_menu_items
                GROUP BY menu_id, variable_id
                HAVING COUNT(*) > 1
                LIMIT 5
            """)
            duplicates = cursor.fetchall()
            if duplicates:
                print(f"\n   Found duplicate menu items: {duplicates}")

        conn.close()

    print("="*80)

if __name__ == '__main__':
    main()
