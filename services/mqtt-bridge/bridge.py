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
try:
    redis_client = redis.from_url(REDIS_URL, decode_responses=True)
    redis_client.ping()
    logger.info(f"Connected to Redis at {REDIS_URL}")
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
        logger.info("Connected to MQTT broker successfully")
        for topic, qos in TOPICS:
            client.subscribe(topic, qos)
            logger.info(f"Subscribed to {topic} (QoS {qos})")
    else:
        logger.error(f"Failed to connect to MQTT broker. Return code: {rc}")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected from MQTT broker"""
    if rc != 0:
        logger.warning(f"Unexpected disconnect from MQTT broker. Return code: {rc}")
        logger.info("Attempting to reconnect...")

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
            elif message_type == 'reported' and len(topic_parts) >= 4:
                handle_config_reported(device_id, payload)

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON payload from {msg.topic}: {e}")
    except Exception as e:
        logger.error(f"Error processing message from {msg.topic}: {e}", exc_info=True)

def handle_telemetry(device_id: str, data: Dict[str, Any]):
    """Handle device telemetry data"""
    try:
        if not redis_client:
            logger.warning("Redis not available, skipping telemetry storage")
            return

        timestamp = datetime.utcnow().isoformat()

        # Store in Redis for real-time access
        redis_key = f"telemetry:{device_id}:latest"
        telemetry_data = {
            **data,
            'timestamp': timestamp,
            'device_id': device_id
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

        # Store in time-series list (keep last 100 readings)
        redis_list_key = f"telemetry:{device_id}:history"
        redis_client.lpush(redis_list_key, json.dumps(telemetry_data))
        redis_client.ltrim(redis_list_key, 0, 99)  # Keep only last 100
        redis_client.expire(redis_list_key, 3600)  # 1 hour TTL

        logger.info(f"Processed telemetry for device {device_id}: {data.get('parameter', 'unknown')}")

    except Exception as e:
        logger.error(f"Error handling telemetry for {device_id}: {e}", exc_info=True)

def handle_status(device_id: str, data: Dict[str, Any]):
    """Handle device status updates"""
    try:
        if not redis_client:
            logger.warning("Redis not available, skipping status update")
            return

        # Update device shadow in Redis
        redis_key = f"device:shadow:{device_id}"
        redis_client.hset(redis_key, "connection_state", data.get('state', 'unknown'))
        redis_client.hset(redis_key, "last_seen", datetime.utcnow().isoformat())
        redis_client.expire(redis_key, 86400)  # 24 hour TTL

        logger.info(f"Updated status for device {device_id}: {data.get('state')}")

    except Exception as e:
        logger.error(f"Error handling status for {device_id}: {e}", exc_info=True)

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

            # Store registration info in Redis
            if redis_client:
                redis_key = f"device:info:{device_id}"
                redis_client.hset(redis_key, "registered", datetime.utcnow().isoformat())
                for key, value in data.items():
                    redis_client.hset(redis_key, key, str(value))
                redis_client.expire(redis_key, 86400)  # 24 hour TTL
        else:
            logger.warning(f"Failed to register device {device_id}: {response.status_code} - {response.text}")

    except requests.exceptions.RequestException as e:
        logger.error(f"Error calling registration API for {device_id}: {e}")
    except Exception as e:
        logger.error(f"Error handling registration for {device_id}: {e}", exc_info=True)

def handle_config_reported(device_id: str, data: Dict[str, Any]):
    """Handle device configuration reported state"""
    try:
        if not redis_client:
            return

        redis_key = f"device:shadow:{device_id}"
        redis_client.hset(redis_key, "reported_config", json.dumps(data))
        redis_client.hset(redis_key, "config_updated", datetime.utcnow().isoformat())
        redis_client.expire(redis_key, 86400)

        logger.info(f"Updated reported config for device {device_id}")

    except Exception as e:
        logger.error(f"Error handling config reported for {device_id}: {e}", exc_info=True)

def main():
    """Main entry point"""
    logger.info("Starting MQTT Bridge Service...")
    logger.info(f"MQTT Broker: {MQTT_BROKER}")
    logger.info(f"Redis URL: {REDIS_URL}")
    logger.info(f"API Base URL: {API_BASE_URL}")

    # Parse broker address
    broker_parts = MQTT_BROKER.split(':')
    broker_host = broker_parts[0]
    broker_port = int(broker_parts[1]) if len(broker_parts) > 1 else 1883

    # Create MQTT client
    client = mqtt.Client(client_id="iodd-mqtt-bridge", clean_session=False)
    client.username_pw_set(MQTT_USERNAME, MQTT_PASSWORD)
    client.on_connect = on_connect
    client.on_disconnect = on_disconnect
    client.on_message = on_message

    # Enable automatic reconnection
    client.reconnect_delay_set(min_delay=1, max_delay=120)

    # Connect to broker
    retry_count = 0
    max_retries = 10

    while retry_count < max_retries:
        try:
            logger.info(f"Connecting to MQTT broker at {broker_host}:{broker_port} (attempt {retry_count + 1}/{max_retries})")
            client.connect(broker_host, broker_port, 60)
            break
        except Exception as e:
            retry_count += 1
            if retry_count >= max_retries:
                logger.error(f"Failed to connect to MQTT broker after {max_retries} attempts: {e}")
                return
            logger.warning(f"Failed to connect, retrying in 5 seconds... ({e})")
            time.sleep(5)

    # Start loop
    try:
        logger.info("MQTT Bridge Service is running...")
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down MQTT Bridge Service...")
        client.disconnect()
    except Exception as e:
        logger.error(f"Unexpected error in main loop: {e}", exc_info=True)

if __name__ == "__main__":
    main()
