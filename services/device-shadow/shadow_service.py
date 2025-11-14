"""
Device Shadow Service
Maintains digital twin of devices in Redis
"""
import os
import json
import logging
import time
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
    logger.info(f"Connected to Redis at {REDIS_URL}")
except Exception as e:
    logger.error(f"Failed to connect to Redis: {e}")
    redis_client = None

def on_connect(client, userdata, flags, rc):
    """Callback when connected"""
    if rc == 0:
        logger.info("Device Shadow Service connected to MQTT")
        client.subscribe("devices/+/telemetry", 0)
        client.subscribe("devices/+/status", 1)
        client.subscribe("devices/+/config/reported", 1)
        client.subscribe("devices/+/config/desired", 1)
        logger.info("Subscribed to device shadow topics")
    else:
        logger.error(f"Connection failed: {rc}")

def on_disconnect(client, userdata, rc):
    """Callback when disconnected"""
    if rc != 0:
        logger.warning(f"Unexpected disconnect. Return code: {rc}")

def on_message(client, userdata, msg):
    """Handle incoming messages"""
    try:
        if not redis_client:
            logger.warning("Redis not available, skipping shadow update")
            return

        topic_parts = msg.topic.split('/')
        device_id = topic_parts[1]
        message_type = topic_parts[2] if len(topic_parts) >= 3 else None

        payload = json.loads(msg.payload.decode())
        shadow_key = f"device:shadow:{device_id}"
        timestamp = datetime.utcnow().isoformat()

        if message_type == 'telemetry':
            # Update latest telemetry in shadow
            redis_client.hset(shadow_key, "last_telemetry", json.dumps(payload))
            redis_client.hset(shadow_key, "last_update", timestamp)

            # Store individual parameters for quick access
            for param_name, value in payload.items():
                if param_name not in ['timestamp', 'device_id']:
                    param_data = {
                        'value': value,
                        'timestamp': timestamp
                    }
                    redis_client.hset(shadow_key, f"param:{param_name}", json.dumps(param_data))

        elif message_type == 'status':
            state = payload.get('state', 'unknown')
            redis_client.hset(shadow_key, "connection_state", state)
            redis_client.hset(shadow_key, "last_seen", timestamp)
            redis_client.hset(shadow_key, "online", str(state.lower() == 'connected').lower())

        elif message_type == 'reported' and len(topic_parts) >= 4:
            # Reported configuration state
            redis_client.hset(shadow_key, "reported_config", json.dumps(payload))
            redis_client.hset(shadow_key, "config_reported_at", timestamp)

        elif message_type == 'desired' and len(topic_parts) >= 4:
            # Desired configuration state
            redis_client.hset(shadow_key, "desired_config", json.dumps(payload))
            redis_client.hset(shadow_key, "config_desired_at", timestamp)

        # Set TTL on shadow (24 hours)
        redis_client.expire(shadow_key, 86400)

        logger.debug(f"Updated shadow for {device_id} ({message_type})")

    except json.JSONDecodeError as e:
        logger.error(f"Failed to decode JSON from {msg.topic}: {e}")
    except Exception as e:
        logger.error(f"Error updating shadow: {e}", exc_info=True)

def main():
    """Main entry point"""
    logger.info("Starting Device Shadow Service...")
    logger.info(f"MQTT Broker: {MQTT_BROKER}")
    logger.info(f"Redis URL: {REDIS_URL}")

    # Parse broker address
    broker_parts = MQTT_BROKER.split(':')
    broker_host = broker_parts[0]
    broker_port = int(broker_parts[1]) if len(broker_parts) > 1 else 1883

    # Create MQTT client
    client = mqtt.Client(client_id="iodd-device-shadow", clean_session=False)
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
                logger.error(f"Failed to connect after {max_retries} attempts: {e}")
                return
            logger.warning(f"Failed to connect, retrying in 5 seconds... ({e})")
            time.sleep(5)

    # Start loop
    try:
        logger.info("Device Shadow Service is running...")
        client.loop_forever()
    except KeyboardInterrupt:
        logger.info("Shutting down Device Shadow Service...")
        client.disconnect()
    except Exception as e:
        logger.error(f"Unexpected error: {e}", exc_info=True)

if __name__ == "__main__":
    main()
