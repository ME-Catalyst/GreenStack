"""
Integration Test Fixtures for GreenStack IoT Components

Provides pytest fixtures for:
- MQTT Broker (Mosquitto)
- InfluxDB Time-Series Database
- Redis Cache
- PostgreSQL Database
"""

import pytest
import docker
import time
import os
from typing import Generator
import paho.mqtt.client as mqtt
from influxdb_client import InfluxDBClient
import redis
import psycopg2


# ============================================================================
# Docker Client Setup
# ============================================================================

@pytest.fixture(scope="session")
def docker_client():
    """Provide Docker client for container management"""
    return docker.from_env()


# ============================================================================
# MQTT Broker Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def mqtt_broker(docker_client) -> Generator[dict, None, None]:
    """
    Start Mosquitto MQTT broker for testing

    Yields:
        dict: Broker connection info {host, port, username, password}
    """
    # Start Mosquitto container
    container = docker_client.containers.run(
        "eclipse-mosquitto:2.0",
        name="test-mosquitto",
        detach=True,
        ports={'1883/tcp': 11883},  # Use non-standard port for testing
        remove=True,
        command=[
            "mosquitto",
            "-c", "/mosquitto-no-auth.conf"
        ],
        volumes={
            # Use default config with no auth for testing
        }
    )

    # Wait for broker to be ready
    time.sleep(2)

    broker_info = {
        "host": "localhost",
        "port": 11883,
        "username": None,
        "password": None
    }

    yield broker_info

    # Cleanup
    container.stop()


@pytest.fixture
def mqtt_client(mqtt_broker) -> Generator[mqtt.Client, None, None]:
    """
    Provide connected MQTT client

    Args:
        mqtt_broker: MQTT broker fixture

    Yields:
        mqtt.Client: Connected MQTT client
    """
    client = mqtt.Client()
    client.connect(mqtt_broker["host"], mqtt_broker["port"], 60)
    client.loop_start()

    yield client

    client.loop_stop()
    client.disconnect()


# ============================================================================
# InfluxDB Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def influxdb_server(docker_client) -> Generator[dict, None, None]:
    """
    Start InfluxDB server for testing

    Yields:
        dict: InfluxDB connection info {url, token, org, bucket}
    """
    # Start InfluxDB container
    container = docker_client.containers.run(
        "influxdb:2.7",
        name="test-influxdb",
        detach=True,
        ports={'8086/tcp': 18086},
        environment={
            "DOCKER_INFLUXDB_INIT_MODE": "setup",
            "DOCKER_INFLUXDB_INIT_USERNAME": "admin",
            "DOCKER_INFLUXDB_INIT_PASSWORD": "adminpassword",
            "DOCKER_INFLUXDB_INIT_ORG": "test-org",
            "DOCKER_INFLUXDB_INIT_BUCKET": "test-bucket",
            "DOCKER_INFLUXDB_INIT_ADMIN_TOKEN": "test-token-12345",
        },
        remove=True
    )

    # Wait for InfluxDB to be ready
    time.sleep(10)

    influx_info = {
        "url": "http://localhost:18086",
        "token": "test-token-12345",
        "org": "test-org",
        "bucket": "test-bucket"
    }

    yield influx_info

    # Cleanup
    container.stop()


@pytest.fixture
def influxdb_client(influxdb_server) -> Generator[InfluxDBClient, None, None]:
    """
    Provide connected InfluxDB client

    Args:
        influxdb_server: InfluxDB server fixture

    Yields:
        InfluxDBClient: Connected InfluxDB client
    """
    client = InfluxDBClient(
        url=influxdb_server["url"],
        token=influxdb_server["token"],
        org=influxdb_server["org"]
    )

    yield client

    client.close()


# ============================================================================
# Redis Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def redis_server(docker_client) -> Generator[dict, None, None]:
    """
    Start Redis server for testing

    Yields:
        dict: Redis connection info {host, port, password}
    """
    # Start Redis container
    container = docker_client.containers.run(
        "redis:7-alpine",
        name="test-redis",
        detach=True,
        ports={'6379/tcp': 16379},
        remove=True
    )

    # Wait for Redis to be ready
    time.sleep(2)

    redis_info = {
        "host": "localhost",
        "port": 16379,
        "password": None,
        "db": 0
    }

    yield redis_info

    # Cleanup
    container.stop()


@pytest.fixture
def redis_client(redis_server) -> Generator[redis.Redis, None, None]:
    """
    Provide connected Redis client

    Args:
        redis_server: Redis server fixture

    Yields:
        redis.Redis: Connected Redis client
    """
    client = redis.Redis(
        host=redis_server["host"],
        port=redis_server["port"],
        db=redis_server["db"],
        decode_responses=True
    )

    # Clear database before test
    client.flushdb()

    yield client

    # Cleanup
    client.flushdb()
    client.close()


# ============================================================================
# PostgreSQL Fixtures
# ============================================================================

@pytest.fixture(scope="session")
def postgres_server(docker_client) -> Generator[dict, None, None]:
    """
    Start PostgreSQL server for testing

    Yields:
        dict: PostgreSQL connection info
    """
    # Start PostgreSQL container
    container = docker_client.containers.run(
        "postgres:15-alpine",
        name="test-postgres",
        detach=True,
        ports={'5432/tcp': 15432},
        environment={
            "POSTGRES_USER": "test_user",
            "POSTGRES_PASSWORD": "test_password",
            "POSTGRES_DB": "test_greenstack"
        },
        remove=True
    )

    # Wait for PostgreSQL to be ready
    time.sleep(5)

    pg_info = {
        "host": "localhost",
        "port": 15432,
        "user": "test_user",
        "password": "test_password",
        "database": "test_greenstack"
    }

    yield pg_info

    # Cleanup
    container.stop()


@pytest.fixture
def postgres_connection(postgres_server):
    """
    Provide PostgreSQL database connection

    Args:
        postgres_server: PostgreSQL server fixture

    Yields:
        psycopg2.connection: Database connection
    """
    conn = psycopg2.connect(
        host=postgres_server["host"],
        port=postgres_server["port"],
        user=postgres_server["user"],
        password=postgres_server["password"],
        database=postgres_server["database"]
    )

    yield conn

    conn.close()


# ============================================================================
# Test Data Fixtures
# ============================================================================

@pytest.fixture
def sample_telemetry_data():
    """Provide sample device telemetry data"""
    return {
        "device_id": "sensor-001",
        "temperature": 22.5,
        "humidity": 45.0,
        "pressure": 1013.25,
        "timestamp": "2025-11-18T12:00:00Z"
    }


@pytest.fixture
def sample_device_shadow():
    """Provide sample device shadow state"""
    return {
        "device_id": "device-001",
        "reported": {
            "status": "online",
            "firmware_version": "1.2.3",
            "uptime": 3600
        },
        "desired": {
            "sample_rate": 1000,
            "enabled": True
        },
        "metadata": {
            "last_update": "2025-11-18T12:00:00Z"
        }
    }


# ============================================================================
# Helper Functions
# ============================================================================

def wait_for_mqtt_message(client: mqtt.Client, topic: str, timeout: int = 5) -> str:
    """
    Wait for a message on a specific MQTT topic

    Args:
        client: MQTT client
        topic: Topic to subscribe to
        timeout: Timeout in seconds

    Returns:
        str: Received message payload
    """
    received_messages = []

    def on_message(client, userdata, msg):
        received_messages.append(msg.payload.decode())

    client.on_message = on_message
    client.subscribe(topic)

    # Wait for message
    start_time = time.time()
    while not received_messages and (time.time() - start_time) < timeout:
        time.sleep(0.1)

    client.unsubscribe(topic)

    return received_messages[0] if received_messages else None


def wait_for_container_health(container, timeout: int = 30) -> bool:
    """
    Wait for Docker container to become healthy

    Args:
        container: Docker container object
        timeout: Timeout in seconds

    Returns:
        bool: True if healthy, False if timeout
    """
    start_time = time.time()
    while (time.time() - start_time) < timeout:
        container.reload()
        status = container.attrs.get("State", {}).get("Health", {}).get("Status")
        if status == "healthy":
            return True
        if container.status != "running":
            return False
        time.sleep(1)
    return False
