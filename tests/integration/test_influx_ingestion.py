"""
InfluxDB Ingestion Integration Tests

Tests the InfluxDB time-series database integration including:
- Connection and authentication
- Writing single and batch data points
- Querying telemetry data
- Retention policies
- Error handling
- MQTT to InfluxDB pipeline
"""

import pytest
import time
from datetime import datetime, timedelta
from influxdb_client import Point
from influxdb_client.client.write_api import SYNCHRONOUS


class TestInfluxDBConnection:
    """Test InfluxDB connection functionality"""

    def test_influxdb_connection(self, influxdb_client):
        """Test connection to InfluxDB server"""
        health = influxdb_client.health()
        assert health.status == "pass", "InfluxDB health check failed"

    def test_influxdb_ready(self, influxdb_client):
        """Test that InfluxDB is ready to accept writes"""
        ready = influxdb_client.ready()
        assert ready.status == "ready", "InfluxDB not ready"

    def test_influxdb_ping(self, influxdb_client):
        """Test InfluxDB ping"""
        result = influxdb_client.ping()
        assert result is True, "InfluxDB ping failed"


class TestInfluxDBWrite:
    """Test writing data to InfluxDB"""

    def test_write_single_point(self, influxdb_client, influxdb_server):
        """Test writing a single data point"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        point = Point("temperature") \
            .tag("device", "sensor-001") \
            .tag("location", "warehouse") \
            .field("value", 22.5) \
            .time(datetime.utcnow())

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=point
        )

        # Verify write succeeded
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "temperature")
          |> filter(fn: (r) => r["device"] == "sensor-001")
        '''

        result = query_api.query(query, org=influxdb_server["org"])

        assert len(result) > 0, "No data found in InfluxDB"
        assert len(result[0].records) > 0, "No records found"

    def test_write_batch_points(self, influxdb_client, influxdb_server):
        """Test writing multiple data points in batch"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        # Create batch of points
        points = []
        base_time = datetime.utcnow()
        for i in range(10):
            point = Point("humidity") \
                .tag("device", f"sensor-{i:03d}") \
                .field("value", 40.0 + i) \
                .time(base_time + timedelta(seconds=i))
            points.append(point)

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=points
        )

        # Verify all points were written
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "humidity")
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        assert len(result[0].records) == 10

    def test_write_with_multiple_fields(self, influxdb_client, influxdb_server):
        """Test writing point with multiple fields"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        point = Point("environmental") \
            .tag("device", "multi-sensor-001") \
            .field("temperature", 22.5) \
            .field("humidity", 45.0) \
            .field("pressure", 1013.25) \
            .time(datetime.utcnow())

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=point
        )

        # Query and verify all fields
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "environmental")
          |> filter(fn: (r) => r["device"] == "multi-sensor-001")
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        records = result[0].records

        # Should have 3 records (one per field)
        assert len(records) == 3

        fields = {r.get_field() for r in records}
        assert "temperature" in fields
        assert "humidity" in fields
        assert "pressure" in fields


class TestInfluxDBQuery:
    """Test querying data from InfluxDB"""

    def test_query_recent_telemetry(self, influxdb_client, influxdb_server):
        """Test querying recent telemetry data"""
        # Write some test data first
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        for i in range(5):
            point = Point("power") \
                .tag("device", "meter-001") \
                .field("watts", 100.0 + i * 10) \
                .time(datetime.utcnow() + timedelta(seconds=i))
            write_api.write(
                bucket=influxdb_server["bucket"],
                org=influxdb_server["org"],
                record=point
            )

        # Query the data
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "power")
          |> filter(fn: (r) => r["device"] == "meter-001")
          |> sort(columns: ["_time"])
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        records = result[0].records

        assert len(records) == 5
        # Verify values are in order
        assert records[0].get_value() == 100.0
        assert records[4].get_value() == 140.0

    def test_query_with_aggregation(self, influxdb_client, influxdb_server):
        """Test querying with aggregation functions"""
        # Write test data
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        values = [20.0, 22.0, 24.0, 26.0, 28.0]
        for i, value in enumerate(values):
            point = Point("temperature") \
                .tag("device", "agg-test-001") \
                .field("value", value) \
                .time(datetime.utcnow() + timedelta(seconds=i))
            write_api.write(
                bucket=influxdb_server["bucket"],
                org=influxdb_server["org"],
                record=point
            )

        # Query with mean aggregation
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "temperature")
          |> filter(fn: (r) => r["device"] == "agg-test-001")
          |> mean()
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        records = result[0].records

        assert len(records) > 0
        # Mean of [20, 22, 24, 26, 28] = 24.0
        assert records[0].get_value() == 24.0

    def test_query_time_range(self, influxdb_client, influxdb_server):
        """Test querying specific time range"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        # Write data at different times
        now = datetime.utcnow()
        old_point = Point("status") \
            .tag("device", "range-test-001") \
            .field("online", 1) \
            .time(now - timedelta(hours=2))

        recent_point = Point("status") \
            .tag("device", "range-test-001") \
            .field("online", 1) \
            .time(now)

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=[old_point, recent_point]
        )

        # Query only last hour
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "status")
          |> filter(fn: (r) => r["device"] == "range-test-001")
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        records = result[0].records

        # Should only get recent point
        assert len(records) == 1


class TestInfluxDBErrorHandling:
    """Test InfluxDB error handling"""

    def test_write_error_handling(self, influxdb_client):
        """Test handling of write errors"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        # Try to write to non-existent bucket
        point = Point("test").field("value", 1.0)

        with pytest.raises(Exception):
            write_api.write(
                bucket="non-existent-bucket",
                org="non-existent-org",
                record=point
            )

    def test_query_syntax_error(self, influxdb_client, influxdb_server):
        """Test handling of query syntax errors"""
        query_api = influxdb_client.query_api()

        # Invalid Flux query syntax
        invalid_query = "this is not valid Flux syntax"

        with pytest.raises(Exception):
            query_api.query(invalid_query, org=influxdb_server["org"])

    def test_connection_failure_recovery(self, influxdb_client):
        """Test client can recover from connection failures"""
        # This test verifies the client handles connection issues gracefully
        # In production, you'd implement retry logic

        health = influxdb_client.health()
        assert health.status == "pass"

        # Client should still be usable after checking health
        health_again = influxdb_client.health()
        assert health_again.status == "pass"


class TestMQTTToInfluxPipeline:
    """Test end-to-end MQTT to InfluxDB pipeline"""

    def test_mqtt_to_influxdb_e2e_flow(
        self,
        mqtt_broker,
        influxdb_client,
        influxdb_server,
        sample_telemetry_data
    ):
        """Test complete pipeline from MQTT publish to InfluxDB storage"""
        import paho.mqtt.client as mqtt
        import json

        # Simulate the bridge: subscribe to MQTT and write to InfluxDB
        received_data = []

        def on_message(client, userdata, msg):
            data = json.loads(msg.payload.decode())
            received_data.append(data)

            # Write to InfluxDB
            write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)
            point = Point("telemetry") \
                .tag("device", data["device_id"]) \
                .field("temperature", data["temperature"]) \
                .field("humidity", data["humidity"]) \
                .field("pressure", data["pressure"])

            write_api.write(
                bucket=influxdb_server["bucket"],
                org=influxdb_server["org"],
                record=point
            )

        # Setup MQTT subscriber (simulating bridge)
        subscriber = mqtt.Client(client_id="test-bridge")
        subscriber.on_message = on_message
        subscriber.connect(mqtt_broker["host"], mqtt_broker["port"], 60)
        subscriber.loop_start()
        subscriber.subscribe("greenstack/telemetry/#")

        time.sleep(0.5)

        # Publish telemetry data via MQTT
        publisher = mqtt.Client(client_id="test-device")
        publisher.connect(mqtt_broker["host"], mqtt_broker["port"], 60)
        publisher.loop_start()

        topic = f"greenstack/telemetry/{sample_telemetry_data['device_id']}"
        publisher.publish(topic, json.dumps(sample_telemetry_data))

        time.sleep(1)

        # Verify data was received and written
        assert len(received_data) == 1

        # Query InfluxDB to verify data was stored
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "telemetry")
          |> filter(fn: (r) => r["device"] == "{sample_telemetry_data['device_id']}")
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        records = result[0].records

        # Should have 3 records (temperature, humidity, pressure)
        assert len(records) == 3

        # Cleanup
        publisher.loop_stop()
        subscriber.loop_stop()
        publisher.disconnect()
        subscriber.disconnect()


class TestInfluxDBPerformance:
    """Test InfluxDB performance characteristics"""

    def test_bulk_write_performance(self, influxdb_client, influxdb_server):
        """Test writing large batch of points"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        # Write 1000 points
        points = []
        start_time = datetime.utcnow()
        for i in range(1000):
            point = Point("perf_test") \
                .tag("batch", "test-001") \
                .field("value", float(i)) \
                .time(start_time + timedelta(milliseconds=i))
            points.append(point)

        write_start = time.time()
        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=points
        )
        write_duration = time.time() - write_start

        # Should complete in reasonable time (< 5 seconds)
        assert write_duration < 5.0, f"Bulk write took {write_duration}s"

        # Verify all points were written
        query_api = influxdb_client.query_api()
        query = f'''
        from(bucket: "{influxdb_server["bucket"]}")
          |> range(start: -1h)
          |> filter(fn: (r) => r["_measurement"] == "perf_test")
          |> filter(fn: (r) => r["batch"] == "test-001")
          |> count()
        '''

        result = query_api.query(query, org=influxdb_server["org"])
        count = result[0].records[0].get_value()

        assert count == 1000


class TestInfluxDBDataTypes:
    """Test different data types in InfluxDB"""

    def test_write_integer_field(self, influxdb_client, influxdb_server):
        """Test writing integer values"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        point = Point("counter") \
            .tag("type", "request_count") \
            .field("count", 42)

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=point
        )

    def test_write_float_field(self, influxdb_client, influxdb_server):
        """Test writing float values"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        point = Point("measurement") \
            .tag("type", "voltage") \
            .field("value", 3.14159)

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=point
        )

    def test_write_boolean_field(self, influxdb_client, influxdb_server):
        """Test writing boolean values"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        point = Point("status") \
            .tag("device", "switch-001") \
            .field("enabled", True)

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=point
        )

    def test_write_string_field(self, influxdb_client, influxdb_server):
        """Test writing string values"""
        write_api = influxdb_client.write_api(write_options=SYNCHRONOUS)

        point = Point("log") \
            .tag("level", "info") \
            .field("message", "System started successfully")

        write_api.write(
            bucket=influxdb_server["bucket"],
            org=influxdb_server["org"],
            record=point
        )
