# GreenStack API Reference

**Version**: 1.0.0
**Base URL**: `http://localhost:8000` (development)
**Documentation**: `/docs` (Swagger UI), `/redoc` (ReDoc)

## Table of Contents

- [Overview](#overview)
- [Authentication & Rate Limiting](#authentication--rate-limiting)
- [IODD Management](#iodd-management)
- [EDS Management](#eds-management)
- [Node-RED Flow Generation](#node-red-flow-generation)
- [Code Generation](#code-generation)
- [Search & Discovery](#search--discovery)
- [Configuration Export](#configuration-export)
- [Service Management](#service-management)
- [Health & Monitoring](#health--monitoring)
- [Response Formats](#response-formats)
- [Error Handling](#error-handling)

---

## Overview

GreenStack provides a RESTful API for managing industrial device configurations,
with support for:

- **IO-Link (IODD)**: Device description parsing and management
- **EtherNet/IP (EDS)**: Electronic data sheet processing
- **Node-RED Integration**: Automatic flow generation
- **Multi-platform Code Generation**: Adapters for Node-RED, Python, and PLCs

## Authentication & Rate Limiting

### Rate Limits

- **Default**: 100 requests per minute per IP address
- **Configurable**: Set via `RATE_LIMIT` environment variable

### Rate Limit Headers

```http
X-RateLimit-Limit: 100
X-RateLimit-Remaining: 95
X-RateLimit-Reset: 1640000000
```

### Authentication

Currently uses IP-based rate limiting. For production deployments, configure
authentication via environment variables:

- `ADMIN_USERNAME`
- `ADMIN_PASSWORD`
- `SECRET_KEY`

---

## IODD Management

### Upload IODD File

Upload and parse an IO-Link Device Description file.

```http
POST /api/upload
Content-Type: multipart/form-data
```

**Request**:
```bash
curl -X POST "http://localhost:8000/api/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@device.iodd"
```

**Response** (200 OK):
```json
{
  "device_id": 1,
  "product_name": "Temperature Sensor Pro",
  "vendor": "Acme Sensors Inc.",
  "parameters_count": 25,
  "message": "IODD file successfully imported"
}
```

**Supported Formats**:
- `.iodd` - Single IODD XML file
- `.zip` - IODD package with assets
- Nested `.zip` - Multiple IODD devices

---

### List All Devices

Retrieve all imported devices.

```http
GET /api/devices
```

**Response** (200 OK):
```json
{
  "devices": [
    {
      "id": 1,
      "vendor_id": 1234,
      "device_id": 5678,
      "product_name": "Temperature Sensor Pro",
      "manufacturer": "Acme Sensors Inc.",
      "iodd_version": "1.1",
      "import_date": "2025-01-15T10:30:00Z",
      "parameter_count": 25
    }
  ],
  "total": 1
}
```

---

### Get Device Details

Retrieve detailed information about a specific device.

```http
GET /api/devices/{device_id}
```

**Response** (200 OK):
```json
{
  "device_info": {
    "vendor_id": 1234,
    "device_id": 5678,
    "product_name": "Temperature Sensor Pro",
    "product_text": "High-precision temperature sensor",
    "hardware_revision": "1.0",
    "firmware_revision": "2.3.1"
  },
  "vendor_info": {
    "name": "Acme Sensors Inc.",
    "url": "https://acmesensors.com"
  },
  "parameters": [...],
  "process_data": {...},
  "communication_profile": {...}
}
```

---

### Get Device Parameters

Retrieve all parameters for a device.

```http
GET /api/devices/{device_id}/parameters
```

**Response** (200 OK):
```json
{
  "parameters": [
    {
      "index": 100,
      "name": "Temperature Value",
      "data_type": "Float32T",
      "access_rights": "ro",
      "default_value": null,
      "min_value": "-40.0",
      "max_value": "125.0",
      "unit": "°C",
      "description": "Current temperature reading"
    }
  ],
  "total": 25
}
```

---

### Delete Device

Remove a device from the database.

```http
DELETE /api/devices/{device_id}
```

**Response** (200 OK):
```json
{
  "message": "Device deleted successfully",
  "device_id": 1
}
```

---

## EDS Management

### Upload EDS File

Upload and parse an EtherNet/IP Electronic Data Sheet.

```http
POST /api/eds/upload
Content-Type: multipart/form-data
```

**Request**:
```bash
curl -X POST "http://localhost:8000/api/eds/upload" \
  -H "accept: application/json" \
  -H "Content-Type: multipart/form-data" \
  -F "file=@device.eds"
```

**Response** (200 OK):
```json
{
  "eds_id": 1,
  "product_name": "CompactLogix 5370",
  "vendor_name": "Rockwell Automation",
  "catalog_number": "1756-L73",
  "message": "EDS file successfully imported"
}
```

---

### List EDS Devices

```http
GET /api/eds/devices
```

**Response** (200 OK):
```json
{
  "devices": [
    {
      "id": 1,
      "vendor_id": 1,
      "product_name": "CompactLogix 5370",
      "catalog_number": "1756-L73",
      "major_revision": 20,
      "minor_revision": 11
    }
  ],
  "total": 1
}
```

---

## Node-RED Flow Generation

### Generate Flow for Device

Generate a Node-RED flow from an IODD device profile.

```http
GET /api/flows/{device_id}/generate?flow_type=monitoring
```

**Query Parameters**:
- `flow_type` (optional): Type of flow to generate
  - `monitoring` - Real-time monitoring with dashboards (default)
  - `control` - Parameter control with UI controls
  - `custom` - Combined monitoring and control

**Response** (200 OK):
```json
{
  "flow": [
    {
      "id": "abc123def456",
      "type": "tab",
      "label": "Temperature Sensor Pro Monitor",
      "disabled": false
    },
    {
      "id": "xyz789",
      "type": "mqtt in",
      "z": "abc123def456",
      "topic": "iolink/1234/5678/process_data",
      "qos": "1",
      "datatype": "json"
    }
  ],
  "device_id": 1,
  "device_name": "Temperature Sensor Pro",
  "flow_type": "monitoring",
  "node_count": 15
}
```

---

### Export Flow as JSON File

Download a Node-RED flow as a JSON file.

```http
GET /api/flows/{device_id}/export?flow_type=monitoring
```

**Response** (200 OK):
```http
Content-Type: application/json
Content-Disposition: attachment; filename=temperature_sensor_pro_monitoring_flow.json

[
  {"id": "abc123", "type": "tab", "label": "Device Monitor"},
  ...
]
```

---

### List Flow Types

Get available flow types with descriptions.

```http
GET /api/flows/types
```

**Response** (200 OK):
```json
{
  "flow_types": [
    {
      "type": "monitoring",
      "name": "Monitoring Flow",
      "description": "Real-time monitoring of process data with dashboard visualization"
    },
    {
      "type": "control",
      "name": "Control Flow",
      "description": "Parameter control and adjustment with UI controls"
    },
    {
      "type": "custom",
      "name": "Custom Flow",
      "description": "Comprehensive flow with both monitoring and control capabilities"
    }
  ]
}
```

---

### Batch Flow Generation

Generate flows for multiple devices at once.

```http
POST /api/flows/batch/generate
Content-Type: application/json
```

**Request**:
```json
{
  "device_ids": [1, 2, 3],
  "flow_type": "monitoring"
}
```

**Response** (200 OK):
```json
{
  "success": false,
  "flow": [...],
  "total_nodes": 45,
  "successful": [
    {
      "device_id": 1,
      "device_name": "Sensor A",
      "node_count": 15
    },
    {
      "device_id": 2,
      "device_name": "Sensor B",
      "node_count": 15
    }
  ],
  "failed": [
    {
      "device_id": 3,
      "error": "Device not found"
    }
  ]
}
```

---

## Code Generation

### Generate Adapter Code

Generate platform-specific adapter code from a device profile.

```http
POST /api/generate
Content-Type: application/json
```

**Request**:
```json
{
  "device_id": 1,
  "platform": "node-red",
  "options": {}
}
```

**Supported Platforms**:
- `node-red` - Node-RED custom node package
- `python` - Python adapter class
- `plc` - PLC function block

**Response** (200 OK):
```json
{
  "device_id": 1,
  "platform": "node-red",
  "files": {
    "package.json": "{...}",
    "temperature-sensor-pro.js": "module.exports = ...",
    "temperature-sensor-pro.html": "<script>...</script>",
    "README.md": "# node-red-contrib-temperature-sensor-pro\n..."
  },
  "generated_at": "2025-01-15T10:30:00Z"
}
```

---

## Search & Discovery

### Search Devices

Search for devices by vendor, product name, or parameters.

```http
GET /api/search?query=temperature&type=product
```

**Query Parameters**:
- `query` (required): Search term
- `type` (optional): Search type (`vendor`, `product`, `parameter`)
- `limit` (optional): Maximum results (default: 50)
- `offset` (optional): Pagination offset (default: 0)

**Response** (200 OK):
```json
{
  "results": [
    {
      "device_id": 1,
      "product_name": "Temperature Sensor Pro",
      "vendor": "Acme Sensors Inc.",
      "match_type": "product_name",
      "relevance": 0.95
    }
  ],
  "total": 1,
  "query": "temperature",
  "type": "product"
}
```

---

## Configuration Export

### Export Device Configuration

Export a device configuration in various formats.

```http
GET /api/config-export/{device_id}?format=json
```

**Query Parameters**:
- `format` (optional): Export format
  - `json` - JSON format (default)
  - `csv` - CSV format
  - `xml` - XML format

**Response** (200 OK):
```http
Content-Type: application/json
Content-Disposition: attachment; filename=device_1_config.json

{
  "device_info": {...},
  "parameters": [...],
  "process_data": {...}
}
```

---

## Service Management

### Service Status

Get status of all managed services.

```http
GET /api/services/status
```

**Response** (200 OK):
```json
{
  "services": {
    "grafana": {
      "status": "running",
      "url": "http://localhost:3000",
      "healthy": true
    },
    "nodered": {
      "status": "running",
      "url": "http://localhost:1880",
      "healthy": true
    },
    "mqtt": {
      "status": "stopped",
      "url": null,
      "healthy": false
    }
  }
}
```

---

### Start Service

Start a managed service.

```http
POST /api/services/{service_name}/start
```

**Supported Services**:
- `grafana` - Grafana dashboarding
- `nodered` - Node-RED flow editor
- `mqtt` - MQTT broker

**Response** (200 OK):
```json
{
  "service": "grafana",
  "status": "started",
  "message": "Grafana service started successfully"
}
```

---

### Stop Service

```http
POST /api/services/{service_name}/stop
```

---

## Health & Monitoring

### Health Check

Simple health check endpoint.

```http
GET /health
```

**Response** (200 OK):
```json
{
  "status": "healthy",
  "timestamp": "2025-01-15T10:30:00Z",
  "version": "1.0.0"
}
```

---

### Metrics

Prometheus-format metrics for monitoring.

```http
GET /metrics
```

**Response** (200 OK):
```
# HELP iodd_uploads_total Total number of IODD file uploads
# TYPE iodd_uploads_total counter
iodd_uploads_total{status="success"} 45.0
iodd_uploads_total{status="failed"} 2.0

# HELP iodd_parse_duration_seconds Time spent parsing IODD files
# TYPE iodd_parse_duration_seconds histogram
iodd_parse_duration_seconds_bucket{le="0.1"} 30.0
iodd_parse_duration_seconds_bucket{le="0.5"} 42.0
...
```

---

## Response Formats

### Success Response

```json
{
  "data": {...},
  "message": "Operation successful"
}
```

### Pagination

```json
{
  "results": [...],
  "total": 100,
  "limit": 20,
  "offset": 0,
  "has_more": true
}
```

---

## Error Handling

### Error Response Format

```json
{
  "error": "Not Found",
  "detail": "Device with ID 999 not found",
  "timestamp": "2025-01-15T10:30:00Z"
}
```

### HTTP Status Codes

- `200 OK` - Request successful
- `201 Created` - Resource created
- `400 Bad Request` - Invalid request parameters
- `404 Not Found` - Resource not found
- `422 Unprocessable Entity` - Validation error
- `429 Too Many Requests` - Rate limit exceeded
- `500 Internal Server Error` - Server error

### Common Error Codes

| Status | Error | Description |
|--------|-------|-------------|
| 400 | `invalid_file_format` | Uploaded file format not supported |
| 400 | `parse_error` | Failed to parse IODD/EDS file |
| 404 | `device_not_found` | Device ID does not exist |
| 404 | `profile_unavailable` | Device profile data not available |
| 429 | `rate_limit_exceeded` | Too many requests |
| 500 | `internal_error` | Unexpected server error |

---

## Examples

### Complete Workflow: Upload to Node-RED Export

```bash
# 1. Upload IODD file
curl -X POST "http://localhost:8000/api/upload" \
  -F "file=@temperature_sensor.iodd" \
  > upload_response.json

# Extract device_id from response
DEVICE_ID=$(jq -r '.device_id' upload_response.json)

# 2. List device parameters
curl "http://localhost:8000/api/devices/${DEVICE_ID}/parameters"

# 3. Generate Node-RED flow
curl "http://localhost:8000/api/flows/${DEVICE_ID}/generate?flow_type=monitoring" \
  > flow_preview.json

# 4. Export flow as downloadable file
curl "http://localhost:8000/api/flows/${DEVICE_ID}/export?flow_type=monitoring" \
  -o sensor_monitoring_flow.json

# 5. Import into Node-RED
# Import sensor_monitoring_flow.json via Node-RED UI
```

---

## SDK & Client Libraries

### Python

```python
import requests

# Upload IODD
with open('device.iodd', 'rb') as f:
    response = requests.post(
        'http://localhost:8000/api/upload',
        files={'file': f}
    )
    device_id = response.json()['device_id']

# Generate flow
flow_response = requests.get(
    f'http://localhost:8000/api/flows/{device_id}/generate',
    params={'flow_type': 'monitoring'}
)
flow_data = flow_response.json()
```

### JavaScript

```javascript
// Upload IODD
const formData = new FormData();
formData.append('file', fileInput.files[0]);

const uploadResponse = await fetch('http://localhost:8000/api/upload', {
  method: 'POST',
  body: formData
});
const { device_id } = await uploadResponse.json();

// Generate flow
const flowResponse = await fetch(
  `http://localhost:8000/api/flows/${device_id}/generate?flow_type=monitoring`
);
const flowData = await flowResponse.json();
```

---

## Support & Resources

- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **GitHub**: https://github.com/yourusername/greenstack
- **Issues**: https://github.com/yourusername/greenstack/issues

---

**Last Updated**: January 2025
**API Version**: 1.0.0
