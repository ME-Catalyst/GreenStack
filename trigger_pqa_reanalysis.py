"""
Trigger PQA Re-analysis for Devices with Updated Baselines
"""
import sqlite3
import sys
import os

# Add src to path so we can import the PQA orchestrator
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from utils.pqa_orchestrator import UnifiedPQAOrchestrator

print("=" * 80)
print("TRIGGERING PQA RE-ANALYSIS")
print("=" * 80)

# Find devices that need re-analysis (have archive but no metrics)
conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

cursor.execute("""
    SELECT DISTINCT a.device_id, d.vendor_id, d.device_id as device_num, d.product_name
    FROM pqa_file_archive a
    JOIN devices d ON a.device_id = d.id
    WHERE NOT EXISTS (
        SELECT 1 FROM pqa_quality_metrics m WHERE m.archive_id = a.id
    )
    ORDER BY a.device_id
    LIMIT 133
""")

devices_to_analyze = cursor.fetchall()

if not devices_to_analyze:
    print("\n[OK] No devices need re-analysis. All current!")
    conn.close()
    exit(0)

print(f"\n[!] Found {len(devices_to_analyze)} devices needing PQA re-analysis")
print("\nDevices to analyze:")
for i, (device_id, vendor_id, device_num, product) in enumerate(devices_to_analyze[:10]):
    print(f"  {i+1}. Device {device_id} ({vendor_id}-{device_num}): {product}")
if len(devices_to_analyze) > 10:
    print(f"  ... and {len(devices_to_analyze) - 10} more devices")

print(f"\n[STEP 1] Initializing PQA Orchestrator...")
orchestrator = UnifiedPQAOrchestrator('greenstack.db')

print(f"[STEP 2] Running PQA analysis for {len(devices_to_analyze)} devices...")
print("This may take several minutes...\n")

success_count = 0
error_count = 0

for i, (device_id, vendor_id, device_num, product) in enumerate(devices_to_analyze):
    try:
        print(f"[{i+1}/{len(devices_to_analyze)}] Analyzing device {device_id} ({vendor_id}-{device_num})...", end=" ")

        # Run PQA analysis
        from utils.pqa_orchestrator import FileType
        result = orchestrator.run_full_analysis(device_id, FileType.IODD)

        if result and 'overall_score' in result:
            score = result['overall_score']
            print(f"Score: {score:.2f}%")
            success_count += 1
        else:
            print("FAILED (no result)")
            error_count += 1

    except Exception as e:
        print(f"ERROR: {str(e)}")
        error_count += 1

conn.close()

print("\n" + "=" * 80)
print("RE-ANALYSIS COMPLETE")
print("=" * 80)
print(f"\nSummary:")
print(f"  [+] Successfully analyzed: {success_count} devices")
print(f"  [!] Errors: {error_count} devices")
print(f"\nExpected Results:")
print(f"  [+] Many devices should now show 100% scores")
print(f"  [+] Check PQA dashboard to verify improvements")
print("\n" + "=" * 80)
