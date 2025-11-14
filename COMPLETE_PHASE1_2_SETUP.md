# Complete Phase 1 & 2 Setup Guide
## Ready-to-Deploy Industrial IoT Platform

This document contains ALL the code needed to complete Phase 1 & 2 implementation. Simply copy each file as shown below.

---

## 📁 File 1: services/mqtt-bridge/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY bridge.py .

# Run the bridge
CMD ["python", "-u", "bridge.py"]
```

---

## 📁 File 2: services/mqtt-bridge/requirements.txt

```
paho-mqtt==1.6.1
redis==5.0.1
requests==2.31.0
python-dotenv==1.0.0
```

---

## 📁 File 3: services/mqtt-bridge/bridge.py

```python
"""
MQTT Bridge Service for IODD Manager IoT Platform
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

# Configuration from environment
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
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

# MQTT Topics to subscribe
TOPICS = [
    ("devices/+/telemetry", 0),
    ("devices/+/status", 1),
    ("devices/+/register", 1),
    ("devices/+/config/reported", 1),
]

def on_connect(client, userdata, flags, rc):
    """Callback when connected to MQTT broker"""
    if rc == 0:
        logger.info("✓ Connected to MQTT broker successfully")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            logger.info(f"  Subscribed to {topic} (QoS {qos})")
    else:
        logger.error(f"✗ Failed to connect to MQTT broker. Return code: {rc}")
        error_messages = {
            1: "Connection refused - incorrect protocol version",
            2: "Connection refused - invalid client identifier",
            3: "Connection refused - server unavailable",
            4: "Connection refused - bad username or password",
            5: "Connection refused - not authorized"
        }
        logger.error(f"  Reason: {error_messages.get(rc, 'Unknown error')}")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected from MQTT broker"""
    if rc != 0:
        logger.warning(f"Unexpected disconnection from MQTT broker (code: {rc}). Reconnecting...")
    else:
        logger.info("Disconnected from MQTT broker")

def on_message(client, userdata, msg):
    """Callback when message received"""
    try:
        topic = msg.topic
        payload = json.loads(msg.payload.decode())

        logger.debug(f"📩 Received: {topic} -> {payload}")

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
            elif message_type == 'config' and len(topic_parts) >= 4 and topic_parts[3] == 'reported':
                handle_config_reported(device_id, payload)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload from {msg.topic}: {e}")
    except Exception as e:
        logger.error(f"Error processing message from {msg.topic}: {e}", exc_info=True)

def handle_telemetry(device_id: str, data: Dict[str, Any]):
    """Handle device telemetry data"""
    if not redis_client:
        logger.warning("Redis not available, skipping telemetry storage")
        return

    try:
        timestamp = data.get('timestamp', datetime.utcnow().isoformat())

        # Store latest telemetry in Redis with 5-minute TTL
        redis_key = f"telemetry:{device_id}:latest"
        telemetry_data = {
            **data,
            'timestamp': timestamp,
            'device_id': device_id,
            'received_at': datetime.utcnow().isoformat()
        }

        redis_client.setex(
            redis_key,
            300,  # TTL 5 minutes
            json.dumps(telemetry_data)
        )

        # Publish to Redis pub/sub for real-time subscribers
        redis_client.publish(
            f"telemetry:{device_id}",
            json.dumps(telemetry_data)
        )

        # Update device activity timestamp
        redis_client.setex(f"device:{device_id}:last_seen", 600, datetime.utcnow().isoformat())

        logger.info(f"✓ Processed telemetry for device {device_id}")

    except Exception as e:
        logger.error(f"Error handling telemetry for {device_id}: {e}", exc_info=True)

def handle_status(device_id: str, data: Dict[str, Any]):
    """Handle device status updates"""
    if not redis_client:
        logger.warning("Redis not available, skipping status update")
        return

    try:
        state = data.get('state', 'unknown')

        # Update device shadow in Redis
        redis_key = f"device:shadow:{device_id}"
        redis_client.hset(redis_key, "connection_state", state)
        redis_client.hset(redis_key, "last_seen", datetime.utcnow().isoformat())

        if 'online' in state.lower():
            redis_client.hset(redis_key, "online", "true")
        else:
            redis_client.hset(redis_key, "online", "false")

        logger.info(f"✓ Updated status for device {device_id}: {state}")

    except Exception as e:
        logger.error(f"Error handling status for {device_id}: {e}", exc_info=True)

def handle_registration(device_id: str, data: Dict[str, Any]):
    """Handle new device registration"""
    try:
        logger.info(f"📝 Device registration request: {device_id}")

        # Store in Redis temporarily
        if redis_client:
            redis_client.setex(
                f"device:registration:{device_id}",
                3600,  # 1 hour TTL
                json.dumps(data)
            )

        # Try to call API to register device (optional, may not exist yet)
        try:
            response = requests.post(
                f"{API_BASE_URL}/api/devices/register",
                json={'device_id': device_id, **data},
                timeout=10
            )

            if response.ok:
                logger.info(f"✓ Device {device_id} registered successfully via API")
            else:
                logger.warning(f"API registration failed for {device_id}: {response.status_code}")
        except requests.exceptions.RequestException as e:
            logger.debug(f"API not available for registration (expected in early setup): {e}")

    except Exception as e:
        logger.error(f"Error handling registration for {device_id}: {e}", exc_info=True)

def handle_config_reported(device_id: str, data: Dict[str, Any]):
    """Handle device reporting its configuration"""
    if not redis_client:
        return

    try:
        redis_key = f"device:shadow:{device_id}"
        redis_client.hset(redis_key, "reported_config", json.dumps(data))
        redis_client.hset(redis_key, "config_updated_at", datetime.utcnow().isoformat())

        logger.info(f"✓ Updated reported config for device {device_id}")

    except Exception as e:
        logger.error(f"Error handling config report for {device_id}: {e}", exc_info=True)

def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("🚀 Starting MQTT Bridge Service")
    logger.info("=" * 60)
    logger.info(f"MQTT Broker: {MQTT_BROKER}")
    logger.info(f"Redis URL: {REDIS_URL.split('@')[1] if '@' in REDIS_URL else REDIS_URL}")
    logger.info(f"API Base URL: {API_BASE_URL}")
    logger.info("=" * 60)

    # Parse broker address
    if ':' in MQTT_BROKER:
        broker_host, broker_port = MQTT_BROKER.rsplit(':', 1)
        broker_port = int(broker_port)
    else:
        broker_host = MQTT_BROKER
        broker_port = 1883

    # Create MQTT client
    client = mqtt.Client(client_id="iodd-mqtt-bridge", clean_session=False)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Enable detailed logging for debugging
    # client.enable_logger(logger)

    # Connect to broker with retry logic
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            logger.info(f"Attempting to connect to MQTT broker at {broker_host}:{broker_port}...")
            client.connect(broker_host, broker_port, 60)
            break
        except Exception as e:
            retry_count += 1
            logger.error(f"Connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count < max_retries:
                wait_time = min(5 * retry_count, 30)  # Exponential backoff, max 30s
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("Max retries reached. Exiting.")
                return

    # Start MQTT loop
    logger.info("🔄 Starting MQTT message loop...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        client.disconnect()
        logger.info("MQTT Bridge Service stopped")

if __name__ == "__main__":
    main()
```

---

## 📁 File 4: services/device-shadow/Dockerfile

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY shadow_service.py .

# Run the service
CMD ["python", "-u", "shadow_service.py"]
```

---

## 📁 File 5: services/device-shadow/requirements.txt

```
paho-mqtt==1.6.1
redis==5.0.1
python-dotenv==1.0.0
```

---

## 📁 File 6: services/device-shadow/shadow_service.py

```python
"""
Device Shadow Service for IODD Manager IoT Platform
Maintains digital twin of devices in Redis
"""
import os
import json
import logging
import time
from typing import Dict, Any
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
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info("Connected to Redis successfully")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

def on_connect(client, userdata, flags, rc):
    """Callback when connected"""
    if rc == 0:
        logger.info("✓ Device Shadow Service connected to MQTT")

        # Subscribe to relevant topics
        topics = [
            ("devices/+/telemetry", 0),
            ("devices/+/status", 1),
            ("devices/+/config/reported", 1),
            ("devices/+/commands/ack", 1),
        ]

        for topic, qos in topics:
            client.subscribe(topic, qos)
            logger.info(f"  Subscribed to {topic} (QoS {qos})")
    else:
        logger.error(f"✗ Connection failed with code: {rc}")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected"""
    if rc != 0:
        logger.warning(f"Unexpected disconnection (code: {rc}). Reconnecting...")

def on_message(client, userdata, msg):
    """Handle incoming messages and update shadow"""
    if not redis_client:
        return

    try:
        topic_parts = msg.topic.split('/')
        if len(topic_parts) < 3:
            return

        device_id = topic_parts[1]
        message_type = topic_parts[2]

        payload = json.loads(msg.payload.decode())
        timestamp = datetime.utcnow().isoformat()

        shadow_key = f"device:shadow:{device_id}"

        logger.debug(f"Updating shadow for {device_id}: {message_type}")

        # Update shadow based on message type
        if message_type == 'telemetry':
            # Store latest telemetry parameters in shadow
            redis_client.hset(shadow_key, "last_telemetry", json.dumps(payload))
            redis_client.hset(shadow_key, "last_telemetry_time", timestamp)
            redis_client.hset(shadow_key, "last_update", timestamp)

            # Extract and store individual parameters for quick access
            if isinstance(payload, dict):
                for param_name, value in payload.items():
                    if param_name not in ['timestamp', 'device_id']:
                        redis_client.hset(
                            shadow_key,
                            f"param:{param_name}",
                            json.dumps({'value': value, 'timestamp': timestamp})
                        )

        elif message_type == 'status':
            state = payload.get('state', 'unknown')
            redis_client.hset(shadow_key, "connection_state", state)
            redis_client.hset(shadow_key, "last_seen", timestamp)
            redis_client.hset(shadow_key, "online", str(state.lower() == 'connected').lower())

        elif message_type == 'config' and len(topic_parts) >= 4:
            if topic_parts[3] == 'reported':
                redis_client.hset(shadow_key, "reported_config", json.dumps(payload))
                redis_client.hset(shadow_key, "config_reported_at", timestamp)

        elif message_type == 'commands' and len(topic_parts) >= 4:
            if topic_parts[3] == 'ack':
                # Store command acknowledgment
                cmd_id = payload.get('command_id', 'unknown')
                redis_client.hset(shadow_key, f"cmd_ack:{cmd_id}", json.dumps(payload))

        # Set TTL on shadow (24 hours for inactive devices)
        redis_client.expire(shadow_key, 86400)

        logger.debug(f"✓ Updated shadow for {device_id}")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON: {e}")
    except Exception as e:
        logger.error(f"Error updating shadow: {e}", exc_info=True)

def publish_desired_config(client):
    """Periodically check for desired config and publish to devices"""
    if not redis_client:
        return

    try:
        # Find all device shadows
        shadow_keys = redis_client.keys("device:shadow:*")

        for shadow_key in shadow_keys:
            try:
                device_id = shadow_key.split(':', 2)[2]

                # Check if there's a desired config
                desired_config = redis_client.hget(shadow_key, "desired_config")
                if desired_config:
                    # Publish to MQTT
                    topic = f"devices/{device_id}/config/desired"
                    client.publish(topic, desired_config, qos=1)
                    logger.info(f"Published desired config to {device_id}")

                    # Clear desired config after publishing
                    redis_client.hdel(shadow_key, "desired_config")

            except Exception as e:
                logger.error(f"Error publishing desired config: {e}")

    except Exception as e:
        logger.error(f"Error in publish_desired_config: {e}")

def main():
    """Main entry point"""
    logger.info("=" * 60)
    logger.info("👥 Starting Device Shadow Service")
    logger.info("=" * 60)
    logger.info(f"MQTT Broker: {MQTT_BROKER}")
    logger.info(f"Redis URL: {REDIS_URL.split('@')[1] if '@' in REDIS_URL else REDIS_URL}")
    logger.info("=" * 60)

    # Parse broker address
    if ':' in MQTT_BROKER:
        broker_host, broker_port = MQTT_BROKER.rsplit(':', 1)
        broker_port = int(broker_port)
    else:
        broker_host = MQTT_BROKER
        broker_port = 1883

    # Create MQTT client
    client = mqtt.Client(client_id="iodd-device-shadow", clean_session=False)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Connect with retry logic
    max_retries = 5
    retry_count = 0

    while retry_count < max_retries:
        try:
            logger.info(f"Connecting to MQTT broker at {broker_host}:{broker_port}...")
            client.connect(broker_host, broker_port, 60)
            break
        except Exception as e:
            retry_count += 1
            logger.error(f"Connection attempt {retry_count}/{max_retries} failed: {e}")
            if retry_count < max_retries:
                wait_time = min(5 * retry_count, 30)
                logger.info(f"Retrying in {wait_time} seconds...")
                time.sleep(wait_time)
            else:
                logger.error("Max retries reached. Exiting.")
                return

    logger.info("🔄 Starting message loop...")
    try:
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Received shutdown signal")
        client.disconnect()
        logger.info("Device Shadow Service stopped")

if __name__ == "__main__":
    main()
```

---

## 📁 File 7: .env.iot

Create this file in the root directory:

```bash
# =============================================================================
# IODD Manager Industrial IoT Platform - Environment Configuration
# =============================================================================

# -----------------------------------------------------------------------------
# Application
# -----------------------------------------------------------------------------
ENVIRONMENT=development
DEBUG=false
LOG_LEVEL=INFO

# -----------------------------------------------------------------------------
# Database
# -----------------------------------------------------------------------------
# Use SQLite for now (PostgreSQL optional)
DATABASE_URL=sqlite:///./iodd_manager.db

# PostgreSQL (uncomment to use)
# DATABASE_URL=postgresql://iodd_user:SecurePass123@postgres:5432/iodd_manager
POSTGRES_DB=iodd_manager
POSTGRES_USER=iodd_user
POSTGRES_PASSWORD=SecurePass123
POSTGRES_PORT=5432

# -----------------------------------------------------------------------------
# Redis
# -----------------------------------------------------------------------------
REDIS_URL=redis://:Redis123@redis:6379/0
REDIS_PASSWORD=Redis123
REDIS_PORT=6379

# -----------------------------------------------------------------------------
# MQTT
# -----------------------------------------------------------------------------
MQTT_BROKER=mosquitto:1883
MQTT_USERNAME=iodd
MQTT_PASSWORD=Mqtt123
MQTT_PORT=1883
MQTT_WS_PORT=9001
MQTT_TLS_PORT=8883

# -----------------------------------------------------------------------------
# API
# -----------------------------------------------------------------------------
API_HOST=0.0.0.0
API_PORT=8000
API_BASE_URL=http://iodd-manager:8000
```

---

## 🚀 Deployment Steps

### Step 1: Create all service files

Copy all the files above into their respective locations.

### Step 2: Create .env file

```bash
cp .env.iot .env
```

### Step 3: Update .gitignore

Add to `.gitignore`:
```
# IoT Platform
.env
.env.*
!.env.iot
config/mosquitto/passwd
volumes/
```

### Step 4: Start the platform

```bash
# Start all services
docker-compose -f docker-compose.yml -f docker-compose.iot.yml up -d

# Watch logs
docker-compose -f docker-compose.yml -f docker-compose.iot.yml logs -f
```

### Step 5: Generate MQTT password

```bash
# Generate password file
docker exec -it iodd-mosquitto mosquitto_passwd -b /mosquitto/config/passwd iodd Mqtt123

# Restart Mosquitto
docker-compose -f docker-compose.yml -f docker-compose.iot.yml restart mosquitto
```

### Step 6: Verify services

```bash
# Check all containers are running
docker-compose -f docker-compose.yml -f docker-compose.iot.yml ps

# Test MQTT
docker exec -it iodd-mosquitto mosquitto_sub -h localhost -u iodd -P Mqtt123 -t 'devices/#' -v
```

---

## 🧪 Test the Platform

### Terminal 1 - Subscribe to all device messages:
```bash
docker exec -it iodd-mosquitto mosquitto_sub -h localhost -u iodd -P Mqtt123 -t 'devices/#' -v
```

### Terminal 2 - Publish test telemetry:
```bash
docker exec -it iodd-mosquitto mosquitto_pub -h localhost -u iodd -P Mqtt123 \
  -t 'devices/test-device-001/telemetry' \
  -m '{
    "temperature": 25.4,
    "pressure": 101.3,
    "humidity": 45.2,
    "timestamp": "2025-01-14T12:00:00Z"
  }'
```

### Terminal 3 - Check Redis for stored data:
```bash
# Access Redis CLI
docker exec -it iodd-redis redis-cli -a Redis123

# Check latest telemetry
GET telemetry:test-device-001:latest

# Check device shadow
HGETALL device:shadow:test-device-001

# Exit
EXIT
```

---

## ✅ Success Criteria

After deployment, you should see:
- ✅ 7 containers running (iodd-manager, postgres, redis, mosquitto, mqtt-bridge, device-shadow)
- ✅ MQTT Bridge logs showing "Connected to MQTT broker successfully"
- ✅ Device Shadow logs showing "Device Shadow Service connected to MQTT"
- ✅ Test messages appearing in subscriber terminal
- ✅ Data stored in Redis

---

## 🎯 What You Can Do Now

1. **Real-time device communication** via MQTT
2. **Device status tracking** in Redis
3. **Telemetry storage** with automatic expiration
4. **Digital twins** for all devices
5. **Pub/sub messaging** for real-time updates

---

## 📚 Next Steps (Phase 3)

Once Phase 1 & 2 are working:
- Add InfluxDB for time-series storage
- Add Grafana for dashboards
- Add historical data API endpoints
- Add WebSocket support for frontend
- Create device simulator

---

**Status:** Ready to deploy!
**Created:** January 2025
