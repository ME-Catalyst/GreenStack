# EDS Export ZIP Endpoint - Implementation Plan

## Endpoint Specification

**Route**: `GET /api/eds/{eds_id}/export-zip`

**Purpose**: Export a ZIP file containing the original EDS file and related assets (icon, metadata, etc.)

**Filename Format**: `{vendor_name}_{product_name}_{product_code}_v{major}.{minor}.zip`

Example: `Murrelektronik_MVK_Pro_ME_DIO8_IOL8_5P_54611_v1.8.zip`

## Implementation

Add to `eds_routes.py` after the existing `/icon` endpoint (around line 626):

```python
@router.get("/{eds_id}/export-zip")
async def export_eds_zip(eds_id: int):
    """
    Export EDS file and related assets as a ZIP file

    Returns:
        ZIP file containing:
        - Original EDS file
        - Icon file (if available)
        - Metadata JSON
    """
    conn = sqlite3.connect(get_db_path())
    cursor = conn.cursor()

    # Get EDS file data
    cursor.execute("""
        SELECT vendor_name, product_name, product_code, major_revision, minor_revision,
               eds_content, icon_filename, icon_data, catalog_number
        FROM eds_files WHERE id = ?
    """, (eds_id,))

    row = cursor.fetchone()
    if not row:
        conn.close()
        raise HTTPException(status_code=404, detail="EDS file not found")

    vendor, product, code, maj_rev, min_rev, eds_content, icon_name, icon_data, catalog = row

    # Create safe filename
    safe_vendor = re.sub(r'[^\w\s-]', '', vendor or 'Unknown').replace(' ', '_')
    safe_product = re.sub(r'[^\w\s-]', '', product or 'Unknown').replace(' ', '_')
    zip_filename = f"{safe_vendor}_{safe_product}_{code}_v{maj_rev}.{min_rev}.zip"

    # Create ZIP in memory
    zip_buffer = io.BytesIO()
    with zipfile.ZipFile(zip_buffer, 'w', zipfile.ZIP_DEFLATED) as zip_file:
        # Add EDS file
        eds_filename = f"{catalog or product}.eds"
        zip_file.writestr(eds_filename, eds_content.encode('utf-8'))

        # Add icon if available
        if icon_data:
            icon_ext = icon_name.split('.')[-1] if icon_name else 'ico'
            zip_file.writestr(f"{catalog or product}.{icon_ext}", icon_data)

        # Add metadata JSON
        metadata = {
            'eds_id': eds_id,
            'vendor_name': vendor,
            'product_name': product,
            'product_code': code,
            'revision': f"{maj_rev}.{min_rev}",
            'catalog_number': catalog,
            'export_date': datetime.now().isoformat()
        }
        zip_file.writestr('metadata.json', json.dumps(metadata, indent=2))

    conn.close()

    # Return ZIP file
    zip_buffer.seek(0)
    return StreamingResponse(
        zip_buffer,
        media_type="application/zip",
        headers={
            "Content-Disposition": f"attachment; filename={zip_filename}"
        }
    )
```

## Required Imports

Add to top of `eds_routes.py`:
```python
import io
import zipfile
import re
import json
from fastapi.responses import StreamingResponse
```

## Testing

```bash
curl -o test_export.zip http://localhost:8000/api/eds/1/export-zip
unzip -l test_export.zip
```

Expected output:
```
Archive:  test_export.zip
  Length      Date    Time    Name
---------  ---------- -----   ----
    68012  2025-11-13 16:00   54611.eds
     1406  2025-11-13 16:00   54611.ico
      256  2025-11-13 16:00   metadata.json
---------                     -------
    69674                     3 files
```
