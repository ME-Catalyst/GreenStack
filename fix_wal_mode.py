"""
Force SQLite to checkpoint WAL and verify true database state
"""
import sqlite3
import os

DB_PATH = 'F:/github/GreenStack/greenstack.db'

print("=" * 80)
print("SQLite WAL Mode Investigation")
print("=" * 80)

# Check for WAL files
wal_file = f"{DB_PATH}-wal"
shm_file = f"{DB_PATH}-shm"

print(f"\n[1] File Check:")
print(f"    Database: {os.path.exists(DB_PATH)} ({os.path.getsize(DB_PATH) if os.path.exists(DB_PATH) else 0} bytes)")
print(f"    WAL file: {os.path.exists(wal_file)} ({os.path.getsize(wal_file) if os.path.exists(wal_file) else 0} bytes)")
print(f"    SHM file: {os.path.exists(shm_file)}")

# Connect and check journal mode
conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()

print(f"\n[2] Database Configuration:")
cursor.execute("PRAGMA journal_mode")
journal_mode = cursor.fetchone()[0]
print(f"    Journal Mode: {journal_mode}")

# Force checkpoint
print(f"\n[3] Forcing WAL Checkpoint...")
cursor.execute("PRAGMA wal_checkpoint(TRUNCATE)")
result = cursor.fetchone()
print(f"    Checkpoint Result: {result}")

# Check actual device count
cursor.execute("SELECT COUNT(*) FROM devices")
device_count = cursor.fetchone()[0]
print(f"\n[4] Current Device Count: {device_count}")

if device_count > 0:
    # Get device ID range
    cursor.execute("SELECT MIN(id), MAX(id) FROM devices")
    min_id, max_id = cursor.fetchone()
    print(f"    Device ID Range: {min_id} to {max_id}")

    # Check for gaps
    cursor.execute("SELECT COUNT(DISTINCT id) FROM devices")
    unique_ids = cursor.fetchone()[0]
    expected_count = max_id - min_id + 1
    print(f"    Unique IDs: {unique_ids}, Expected if sequential: {expected_count}")

    if unique_ids != expected_count:
        print(f"    [WARNING] Gap in IDs detected - not sequential!")

conn.close()

print("=" * 80)
