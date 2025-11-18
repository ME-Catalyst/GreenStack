"""
GreenStack Load Testing Suite

Performance and load testing scenarios using Locust.

Run with:
    locust -f locustfile.py --host=http://localhost:8000

Web UI will be available at:
    http://localhost:8089
"""

from locust import HttpUser, task, between, SequentialTaskSet
import random
import json
import os
from datetime import datetime


class IODDUploadTasks(SequentialTaskSet):
    """Sequential tasks for IODD file upload workflow"""

    @task
    def upload_iodd_file(self):
        """Upload an IODD file"""
        # Simulate IODD file upload
        files = {'file': ('test-device.iodd', b'<IODevice></IODevice>', 'application/xml')}

        with self.client.post(
            "/api/iodd/upload",
            files=files,
            headers={"Authorization": f"Bearer {self.user.token}"},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Upload failed with status {response.status_code}")

    @task
    def list_uploaded_files(self):
        """List uploaded IODD files"""
        with self.client.get(
            "/api/iodd",
            headers={"Authorization": f"Bearer {self.user.token}"},
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"List failed with status {response.status_code}")


class DeviceSearchTasks(SequentialTaskSet):
    """Sequential tasks for device search workflow"""

    @task(3)
    def search_by_vendor(self):
        """Search devices by vendor"""
        vendors = ["Balluff", "IFM", "Sick", "Turck", "Pepperl+Fuchs"]
        vendor = random.choice(vendors)

        with self.client.get(
            f"/api/devices/search?vendor={vendor}",
            headers={"Authorization": f"Bearer {self.user.token}"},
            name="/api/devices/search?vendor=[vendor]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Search failed with status {response.status_code}")

    @task(2)
    def search_by_keyword(self):
        """Search devices by keyword"""
        keywords = ["temperature", "pressure", "sensor", "analog", "digital"]
        keyword = random.choice(keywords)

        with self.client.get(
            f"/api/devices/search?q={keyword}",
            headers={"Authorization": f"Bearer {self.user.token}"},
            name="/api/devices/search?q=[keyword]",
            catch_response=True
        ) as response:
            if response.status_code == 200:
                response.success()
            else:
                response.failure(f"Search failed with status {response.status_code}")

    @task(1)
    def get_device_details(self):
        """Get device details"""
        device_id = random.randint(1, 100)

        with self.client.get(
            f"/api/devices/{device_id}",
            headers={"Authorization": f"Bearer {self.user.token}"},
            name="/api/devices/[id]",
            catch_response=True
        ) as response:
            if response.status_code in [200, 404]:
                response.success()
            else:
                response.failure(f"Get device failed with status {response.status_code}")


class AdapterGenerationTasks(SequentialTaskSet):
    """Sequential tasks for adapter generation workflow"""

    @task
    def generate_node_red_adapter(self):
        """Generate Node-RED adapter"""
        payload = {
            "device_id": random.randint(1, 100),
            "platform": "node-red",
            "options": {
                "include_comments": True,
                "format": "json"
            }
        }

        with self.client.post(
            "/api/adapters/generate",
            json=payload,
            headers={"Authorization": f"Bearer {self.user.token}"},
            name="/api/adapters/generate (node-red)",
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Generation failed with status {response.status_code}")

    @task
    def generate_python_adapter(self):
        """Generate Python adapter"""
        payload = {
            "device_id": random.randint(1, 100),
            "platform": "python",
            "options": {
                "async": True,
                "type_hints": True
            }
        }

        with self.client.post(
            "/api/adapters/generate",
            json=payload,
            headers={"Authorization": f"Bearer {self.user.token}"},
            name="/api/adapters/generate (python)",
            catch_response=True
        ) as response:
            if response.status_code in [200, 201]:
                response.success()
            else:
                response.failure(f"Generation failed with status {response.status_code}")


class GreenStackUser(HttpUser):
    """
    Simulated GreenStack user with mixed workload

    Simulates typical user behavior:
    - Authenticates once
    - Performs device searches (most common)
    - Occasionally uploads IODD files
    - Sometimes generates adapters
    """

    wait_time = between(1, 5)  # Wait 1-5 seconds between tasks
    token = None

    def on_start(self):
        """Called when a user starts - authenticate"""
        # Get credentials from environment or use defaults
        username = os.getenv("TEST_USERNAME", "admin")
        password = os.getenv("TEST_PASSWORD", "admin")

        # Authenticate
        response = self.client.post("/api/auth/login", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            self.token = response.json().get("access_token")
        else:
            print(f"Authentication failed: {response.status_code}")

    @task(10)
    def search_devices(self):
        """Search for devices (most common task)"""
        search_terms = [
            "temperature",
            "pressure",
            "sensor",
            "analog",
            "digital",
            "Balluff",
            "IFM",
            "Sick"
        ]
        term = random.choice(search_terms)

        self.client.get(
            f"/api/devices/search?q={term}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/devices/search"
        )

    @task(5)
    def view_device_details(self):
        """View device details"""
        device_id = random.randint(1, 100)

        self.client.get(
            f"/api/devices/{device_id}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/devices/[id]"
        )

    @task(3)
    def list_iodd_files(self):
        """List IODD files"""
        self.client.get(
            "/api/iodd",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(2)
    def generate_adapter(self):
        """Generate adapter code"""
        platforms = ["node-red", "python", "plc"]
        platform = random.choice(platforms)

        payload = {
            "device_id": random.randint(1, 100),
            "platform": platform
        }

        self.client.post(
            "/api/adapters/generate",
            json=payload,
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/adapters/generate"
        )

    @task(1)
    def upload_iodd(self):
        """Upload IODD file (least common task)"""
        files = {'file': ('test-device.iodd', b'<IODevice></IODevice>', 'application/xml')}

        self.client.post(
            "/api/iodd/upload",
            files=files,
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(1)
    def check_health(self):
        """Check API health"""
        self.client.get("/api/health", name="/api/health")


class HighLoadUser(HttpUser):
    """
    Aggressive user simulating high load conditions

    Used for stress testing - generates more requests with less wait time
    """

    wait_time = between(0.1, 0.5)  # Very short wait times
    token = None

    def on_start(self):
        """Authenticate on start"""
        username = os.getenv("TEST_USERNAME", "admin")
        password = os.getenv("TEST_PASSWORD", "admin")

        response = self.client.post("/api/auth/login", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            self.token = response.json().get("access_token")

    @task
    def rapid_search(self):
        """Perform rapid device searches"""
        term = random.choice(["sensor", "device", "analog"])
        self.client.get(
            f"/api/devices/search?q={term}",
            headers={"Authorization": f"Bearer {self.token}"},
            name="/api/devices/search (rapid)"
        )


class APIOnlyUser(HttpUser):
    """
    User that only hits API endpoints without file uploads

    Useful for testing pure API performance
    """

    wait_time = between(1, 3)
    token = None

    def on_start(self):
        """Authenticate on start"""
        username = os.getenv("TEST_USERNAME", "admin")
        password = os.getenv("TEST_PASSWORD", "admin")

        response = self.client.post("/api/auth/login", json={
            "username": username,
            "password": password
        })

        if response.status_code == 200:
            self.token = response.json().get("access_token")

    @task(5)
    def list_devices(self):
        """List all devices"""
        self.client.get(
            "/api/devices",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(3)
    def search_devices(self):
        """Search devices"""
        self.client.get(
            "/api/devices/search?q=sensor",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(2)
    def get_statistics(self):
        """Get system statistics"""
        self.client.get(
            "/api/stats",
            headers={"Authorization": f"Bearer {self.token}"}
        )

    @task(1)
    def check_health(self):
        """Health check"""
        self.client.get("/api/health")


# ============================================================================
# Custom Locust Events for Advanced Metrics
# ============================================================================

from locust import events

@events.request.add_listener
def on_request(request_type, name, response_time, response_length, exception, context, **kwargs):
    """
    Custom request handler to track additional metrics

    This could be used to:
    - Log slow requests to file
    - Send metrics to external monitoring
    - Track custom business metrics
    """
    if exception:
        print(f"Request failed: {name} - {exception}")

    # Log very slow requests
    if response_time > 5000:  # 5 seconds
        print(f"SLOW REQUEST: {name} took {response_time}ms")


@events.test_start.add_listener
def on_test_start(environment, **kwargs):
    """Called when test starts"""
    print("=" * 80)
    print(f"Load test started at {datetime.now()}")
    print(f"Target host: {environment.host}")
    print("=" * 80)


@events.test_stop.add_listener
def on_test_stop(environment, **kwargs):
    """Called when test stops"""
    print("=" * 80)
    print(f"Load test completed at {datetime.now()}")
    print("=" * 80)

    # Print summary statistics
    stats = environment.stats
    print(f"\nTotal requests: {stats.total.num_requests}")
    print(f"Total failures: {stats.total.num_failures}")
    print(f"Average response time: {stats.total.avg_response_time:.2f}ms")
    print(f"Max response time: {stats.total.max_response_time:.2f}ms")
    print(f"Requests per second: {stats.total.total_rps:.2f}")
