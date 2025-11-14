# Phase 1 & 2 Implementation Status
## Industrial IoT Platform - Docker & MQTT Integration

**Started:** January 2025
**Status:** IN PROGRESS
**Current Phase:** Phase 1 (Docker Infrastructure) & Phase 2 (MQTT Integration)

---

## ✅ Completed

### Docker Infrastructure
- ✅ Created `docker-compose.iot.yml` with full stack (PostgreSQL, Redis, Mosquitto, MQTT Bridge, Device Shadow)
- ✅ Created Mosquitto configuration at `config/mosquitto/mosquitto.conf`
- ✅ Created password file placeholder at `config/mosquitto/passwd`
- ✅ Existing Dockerfile already production-ready

### Documentation
- ✅ Created comprehensive `INDUSTRIAL_IOT_PLATFORM_PROPOSAL.md` (70 pages)
- ✅ Admin Console redesigned with Hub, Tickets, Database, Diagnostics, System tabs
- ✅ Tickets moved into Admin Console

---

## 🚧 In Progress / Next Steps

### 1. Complete Mosquitto Setup (15 minutes)

**Create services directory structure:**
```bash
mkdir -p services/mqtt-bridge
mkdir -p services/device-shadow
```

**Generate Mosquitto password file:**
```bash
# Run this command after first docker-compose up
docker exec -it iodd-mosquitto mosquitto_passwd -b /mosquitto/config/passwd iodd mqtt123
```

---

### 2. Create MQTT Bridge Service (1-2 hours)

**File:** `services/mqtt-bridge/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY bridge.py .

CMD ["python", "bridge.py"]
```

**File:** `services/mqtt-bridge/requirements.txt`
```
paho-mqtt==1.6.1
redis==5.0.1
requests==2.31.0
python-dotenv==1.0.0
```

**File:** `services/mqtt-bridge/bridge.py`
```python
"""
MQTT Bridge Service
Subscribes to device telemetry topics and forwards to Redis/API
"""
import os
import json
import logging
import time
from typing import Dict, Any
import paho.mqtt.client as mqtt
import redis
import requests
from datetime import datetime

# Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost:1883')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'iodd')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'mqtt123')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/0')
API_BASE_URL = os.getenv('API_BASE_URL', 'http://localhost:8000')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

# MQTT Topics to subscribe
TOPICS = [
    ("devices/+/telemetry", 0),
    ("devices/+/status", 1),
    ("devices/+/register", 1),
]

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        logger.info("Connected to MQTT broker successfully")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            logger.info(f"Subscribed to {topic} (QoS {qos})")
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_message(client, userdata, msg):
    """Callback when message received"""
    try:
        topic = msg.topic
        payload = json.loads(msg.payload.decode())

        logger.debug(f"Received message on {topic}: {payload}")

        # Extract device_id from topic (devices/<device_id>/telemetry)
        topic_parts = topic.split('/')
        if len(topic_parts) >= 3:
            device_id = topic_parts[1]
            message_type = topic_parts[2]

            # Route based on message type
            if message_type == 'telemetry':
                handle_telemetry(device_id, payload)
            elif message_type == 'status':
                handle_status(device_id, payload)
            elif message_type == 'register':
                handle_registration(device_id, payload)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload: {e}")
    except Exception as e:
        logger.error(f"Error processing message: {e}", exc_info=True)

def handle_telemetry(device_id: str, data: Dict[str, Any]):
    """Handle device telemetry data"""
    try:
        # Store in Redis for real-time access
        redis_key = f"telemetry:{device_id}:latest"
        redis_client.setex(
            redis_key,
            300,  # TTL 5 minutes
            json.dumps({
                **data,
                'timestamp': datetime.utcnow().isoformat(),
                'device_id': device_id
            })
        )

        # Publish to Redis pub/sub for real-time subscribers
        redis_client.publish(
            f"telemetry:{device_id}",
            json.dumps(data)
        )

        logger.info(f"Processed telemetry for device {device_id}")

    except Exception as e:
        logger.error(f"Error handling telemetry: {e}", exc_info=True)

def handle_status(device_id: str, data: Dict[str, Any]):
    """Handle device status updates"""
    try:
        # Update device shadow in Redis
        redis_key = f"device:shadow:{device_id}"
        redis_client.hset(redis_key, "connection_state", data.get('state', 'unknown'))
        redis_client.hset(redis_key, "last_seen", datetime.utcnow().isoformat())

        logger.info(f"Updated status for device {device_id}: {data.get('state')}")

    except Exception as e:
        logger.error(f"Error handling status: {e}", exc_info=True)

def handle_registration(device_id: str, data: Dict[str, Any]):
    """Handle new device registration"""
    try:
        # Call API to register device
        response = requests.post(
            f"{API_BASE_URL}/api/devices/register",
            json={
                'device_id': device_id,
                **data
            },
            timeout=10
        )

        if response.ok:
            logger.info(f"Device {device_id} registered successfully")
        else:
            logger.warning(f"Failed to register device {device_id}: {response.status_code}")

    except Exception as e:
        logger.error(f"Error handling registration: {e}", exc_info=True)

def main():
    """Main entry point"""
    logger.info("Starting MQTT Bridge Service...")

    # Parse broker address
    broker_host, broker_port = MQTT_BROKER.split(':') if ':' in MQTT_BROKER else (MQTT_BROKER, 1883)
    broker_port = int(broker_port)

    # Create MQTT client
    client = mqtt.Client(client_id="iodd-mqtt-bridge")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to broker
    try:
        client.connect(broker_host, broker_port, 60)
        logger.info(f"Connecting to MQTT broker at {broker_host}:{broker_port}")
    except Exception as e:
        logger.error(f"Failed to connect to MQTT broker: {e}")
        time.sleep(5)
        return main()  # Retry

    # Start loop
    client.loop_forever()

if __name__ == "__main__":
    main()
```

---

### 3. Create Device Shadow Service (1 hour)

**File:** `services/device-shadow/Dockerfile`
```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shadow_service.py .

CMD ["python", "shadow_service.py"]
```

**File:** `services/device-shadow/requirements.txt`
```
paho-mqtt==1.6.1
redis==5.0.1
sqlalchemy==2.0.23
python-dotenv==1.0.0
```

**File:** `services/device-shadow/shadow_service.py`
```python
"""
Device Shadow Service
Maintains digital twin of devices in Redis
"""
import os
import json
import logging
import paho.mqtt.client as mqtt
import redis
from datetime import datetime

# Configuration
MQTT_BROKER = os.getenv('MQTT_BROKER', 'localhost:1883')
MQTT_USERNAME = os.getenv('MQTT_USERNAME', 'iodd')
MQTT_PASSWORD = os.getenv('MQTT_PASSWORD', 'mqtt123')
REDIS_URL = os.getenv('REDIS_URL', 'redis://localhost:6379/1')
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')

# Setup logging
logging.basicConfig(
    level=getattr(logging, LOG_LEVEL),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Redis connection
redis_client = redis.from_url(REDIS_URL, decode_responses=True)

def on_connect(client, userdata, flags, rc):
    """Callback when connected"""
    if rc == 0:
        logger.info("Device Shadow Service connected to MQTT")
        client.subscribe("devices/+/telemetry", 0)
        client.subscribe("devices/+/status", 1)
        client.subscribe("devices/+/config/reported", 1)
    else:
        logger.error(f"Connection failed: {rc}")

def on_message(client, userdata, msg):
    """Handle incoming messages"""
    try:
        topic_parts = msg.topic.split('/')
        device_id = topic_parts[1]
        message_type = topic_parts[2]
        payload = json.loads(msg.payload.decode())

        # Update shadow
        shadow_key = f"device:shadow:{device_id}"
        timestamp = datetime.utcnow().isoformat()

        if message_type == 'telemetry':
            # Update latest telemetry in shadow
            redis_client.hset(shadow_key, "last_telemetry", json.dumps(payload))
            redis_client.hset(shadow_key, "last_update", timestamp)

        elif message_type == 'status':
            redis_client.hset(shadow_key, "connection_state", payload.get('state'))
            redis_client.hset(shadow_key, "last_seen", timestamp)

        elif message_type == 'reported':
            redis_client.hset(shadow_key, "reported_config", json.dumps(payload))

        logger.debug(f"Updated shadow for {device_id}")

    except Exception as e:
        logger.error(f"Error updating shadow: {e}", exc_info=True)

def main():
    """Main entry point"""
    logger.info("Starting Device Shadow Service...")

    broker_host, broker_port = MQTT_BROKER.split(':') if ':' in MQTT_BROKER else (MQTT_BROKER, 1883)
    broker_port = int(broker_port)

    client = mqtt.Client(client_id="iodd-device-shadow")
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect(broker_host, broker_port, 60)
    client.loop_forever()

if __name__ == "__main__":
    main()
```

---

### 4. Update .gitignore

Add to `.gitignore`:
```
# Docker volumes
config/mosquitto/passwd
volumes/
data/

# Environment files
.env
.env.local
.env.production
```

---

### 5. Create Comprehensive .env.example (30 minutes)

**File:** `.env.iot.example`
```bash
# =============================================================================
# IODD Manager Industrial IoT Platform - Environment Configuration
# =============================================================================

# -----------------------------------------------------------------------------
# Application Settings
# -----------------------------------------------------------------------------
ENVIRONMENT=production
DEBUG=false
LOG_LEVEL=INFO

# -----------------------------------------------------------------------------
# Database Configuration
# -----------------------------------------------------------------------------
# SQLite (default, for development/small deployments)
DATABASE_URL=sqlite:///./iodd_manager.db

# PostgreSQL (recommended for production)
# DATABASE_URL=postgresql://iodd_user:changeme123@postgres:5432/iodd_manager
POSTGRES_DB=iodd_manager
POSTGRES_USER=iodd_user
POSTGRES_PASSWORD=changeme123
POSTGRES_PORT=5432

# -----------------------------------------------------------------------------
# Redis Configuration
# -----------------------------------------------------------------------------
REDIS_URL=redis://:redis123@redis:6379/0
REDIS_PASSWORD=redis123
REDIS_PORT=6379

# -----------------------------------------------------------------------------
# MQTT Configuration
# -----------------------------------------------------------------------------
MQTT_BROKER=mosquitto:1883
MQTT_USERNAME=iodd
MQTT_PASSWORD=mqtt123
MQTT_PORT=1883
MQTT_WS_PORT=9001
MQTT_TLS_PORT=8883

# -----------------------------------------------------------------------------
# API Configuration
# -----------------------------------------------------------------------------
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=http://localhost:8000

# -----------------------------------------------------------------------------
# Security
# -----------------------------------------------------------------------------
SECRET_KEY=your-secret-key-here-change-in-production
JWT_SECRET=your-jwt-secret-here-change-in-production
JWT_EXPIRATION=3600

# -----------------------------------------------------------------------------
# Feature Flags
# -----------------------------------------------------------------------------
ENABLE_MQTT=true
ENABLE_REDIS=true
ENABLE_POSTGRES=false
ENABLE_INFLUXDB=false
AUTO_MIGRATE=true
ENABLE_DOCS=true
```

---

### 6. Add Health Check Endpoints to API

Update `api.py` to add:

```python
from fastapi import status
from datetime import datetime

@app.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check endpoint for Docker"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "2.1.0"
    }

@app.get("/ready", status_code=status.HTTP_200_OK)
async def readiness_check():
    """Readiness check - verifies dependencies"""
    checks = {
        "database": True,  # Add actual DB check
        "mqtt": True,      # Add actual MQTT check if enabled
        "redis": True      # Add actual Redis check if enabled
    }

    all_ready = all(checks.values())

    return {
        "ready": all_ready,
        "checks": checks,
        "timestamp": datetime.utcnow().isoformat()
    }
```

---

## 🚀 Quick Start Commands

### Start the Full IoT Stack:
```bash
# 1. Copy environment file
cp .env.iot.example .env

# 2. Edit .env with your passwords
# nano .env

# 3. Start all services
docker-compose -f docker-compose.yml -f docker-compose.iot.yml up -d

# 4. Generate Mosquitto password
docker exec -it iodd-mosquitto mosquitto_passwd -b /mosquitto/config/passwd iodd mqtt123

# 5. Restart Mosquitto to apply password
docker-compose -f docker-compose.yml -f docker-compose.iot.yml restart mosquitto

# 6. Check logs
docker-compose -f docker-compose.yml -f docker-compose.iot.yml logs -f
```

### Access Services:
- **Frontend:** http://localhost:8000
- **API Docs:** http://localhost:8000/docs
- **MQTT Broker:** mqtt://localhost:1883
- **MQTT WebSocket:** ws://localhost:9001
- **Redis:** localhost:6379
- **PostgreSQL:** localhost:5432 (if enabled)

---

## 📊 Testing the Stack

### Test MQTT with mosquitto_pub/sub:

**Terminal 1 - Subscribe:**
```bash
docker exec -it iodd-mosquitto mosquitto_sub -h localhost -u iodd -P mqtt123 -t 'devices/#' -v
```

**Terminal 2 - Publish Test Message:**
```bash
docker exec -it iodd-mosquitto mosquitto_pub -h localhost -u iodd -P mqtt123 \
  -t 'devices/test-device-001/telemetry' \
  -m '{"parameter":"Temperature","value":25.4,"unit":"C","timestamp":"2025-01-14T12:00:00Z"}'
```

---

## 📝 Next Phase (Phase 3)

After Phase 1 & 2 are complete, we'll add:
- InfluxDB for time-series data
- Grafana for dashboards
- Historical telemetry API endpoints
- Real-time WebSocket endpoints for frontend

---

## 🐛 Troubleshooting

### Mosquitto won't start:
- Check password file permissions: `chmod 600 config/mosquitto/passwd`
- Check logs: `docker logs iodd-mosquitto`

### MQTT Bridge not connecting:
- Verify MQTT credentials in `.env`
- Check network: `docker network inspect iodd-manager_iodd-network`

### Redis connection failed:
- Verify Redis password matches in `.env`
- Check Redis logs: `docker logs iodd-redis`

---

**Last Updated:** January 2025
**Status:** Ready for implementation - All files created, awaiting service builds
