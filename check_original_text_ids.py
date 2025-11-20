"""Check Text IDs in the ORIGINAL file used for PQA comparison"""
import sqlite3
import re

conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

# Get the most recent original file used for PQA comparison
# The PQA system archives both original and reconstructed files
# We need the one that came first (the original)
cursor.execute("""
    SELECT file_content, filename FROM pqa_file_archive
    WHERE device_id = 56 AND file_type = 'IODD'
    ORDER BY id ASC
    LIMIT 1
""")

row = cursor.fetchone()
conn.close()

if not row:
    print("No original file found in PQA archive")
    exit(1)

content, filename = row
if isinstance(content, bytes):
    content = content.decode('utf-8')

print(f'File: {filename}')
print(f'File size: {len(content)} characters')

# Extract Text IDs from the file
matches = re.findall(r'<Text id="([^"]+)"', content)

print(f'\n=== First 30 Text IDs from ORIGINAL file ===')
for i, text_id in enumerate(matches[:30], 1):
    print(f'{i}: {text_id}')

print(f'\n... Total Text elements in original: {len(matches)}')

# Check for specific IDs we know about
print(f'\n=== Checking for specific IDs ===')
print(f'TI_VendorText in original: {"YES" if "TI_VendorText" in matches else "NO"}')
print(f'TI_VendorUrl in original: {"YES" if "TI_VendorUrl" in matches else "NO"}')
print(f'TI_DeviceFamily in original: {"YES" if "TI_DeviceFamily" in matches else "NO"}')
print(f'TI_0 in original: {"YES" if "TI_0" in matches else "NO"}')
print(f'TI_1 in original: {"YES" if "TI_1" in matches else "NO"}')
