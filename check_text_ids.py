"""Check Text IDs in archived reconstruction for Device #56"""
import sqlite3

conn = sqlite3.connect('greenstack.db')
cursor = conn.cursor()

# Get the archived reconstructed file
cursor.execute("""
    SELECT file_content FROM pqa_file_archive
    WHERE device_id = 56 AND file_type = 'IODD'
    ORDER BY id DESC LIMIT 1
""")

row = cursor.fetchone()
if row:
    content = row[0].decode('utf-8') if isinstance(row[0], bytes) else row[0]

    lines = content.split('\n')
    text_lines = [l for l in lines if '<Text id=' in l]

    print('=== First 30 Text elements from archived reconstructed file ===')
    for i, line in enumerate(text_lines[:30], 1):
        print(f'{i}: {line.strip()}')

    print(f'\n... Total text elements: {len(text_lines)}')

    # Check what IDs are actually in database
    cursor.execute("""
        SELECT text_id, text_value FROM iodd_text
        WHERE device_id = 56
        ORDER BY text_id
        LIMIT 30
    """)

    print('\n=== First 30 Text IDs stored in database ===')
    for i, (text_id, text_value) in enumerate(cursor.fetchall(), 1):
        print(f'{i}: {text_id} = {text_value[:50]}...' if len(text_value) > 50 else f'{i}: {text_id} = {text_value}')
else:
    print("No archived file found for Device #56")

conn.close()
