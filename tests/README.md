# Greenstack Test Suite

This directory contains the comprehensive test suite for Greenstack.

## Structure

```
tests/
├── __init__.py                 # Test package initialization
├── conftest.py                 # Pytest configuration and shared fixtures
├── test_parser.py              # Tests for IODD XML parser
├── test_api.py                 # Tests for REST API endpoints
├── test_storage.py             # Tests for database operations
├── fixtures/                   # Test data and sample files
│   ├── __init__.py
│   ├── sample_device.xml       # Valid IODD file for testing
│   ├── invalid.xml             # Invalid IODD structure
│   └── malformed.xml           # Malformed XML
└── README.md                   # This file
```

## Running Tests

### Run All Tests

```bash
# Using Make
make test

# Using pytest directly
pytest

# With verbose output
pytest -v
```

### Run Specific Test Files

```bash
# Test parser only
pytest tests/test_parser.py

# Test API only
pytest tests/test_api.py

# Test storage only
pytest tests/test_storage.py
```

### Run Specific Test Classes or Functions

```bash
# Run a specific test class
pytest tests/test_api.py::TestHealthEndpoints

# Run a specific test function
pytest tests/test_parser.py::TestIODDParser::test_parse_valid_iodd_file
```

### Run Tests by Markers

```bash
# Run only unit tests
pytest -m unit

# Run only integration tests
pytest -m integration

# Skip slow tests
pytest -m "not slow"
```

### Run with Coverage

```bash
# Using Make
make test-cov

# Using pytest directly
pytest --cov=. --cov-report=html --cov-report=term

# View coverage report
open htmlcov/index.html
```

## Test Markers

Tests are organized with the following markers:

- `@pytest.mark.unit` - Fast, isolated unit tests
- `@pytest.mark.integration` - Tests that involve multiple components
- `@pytest.mark.slow` - Tests that take significant time to run

## Fixtures

The `conftest.py` file provides shared fixtures:

### Path Fixtures
- `fixtures_dir` - Path to test fixtures directory
- `sample_iodd_path` - Path to valid IODD file
- `invalid_iodd_path` - Path to invalid IODD file
- `malformed_iodd_path` - Path to malformed XML file
- `sample_iodd_content` - Content of valid IODD file

### Database Fixtures
- `temp_db_path` - Temporary database file (auto-cleanup)
- `storage_manager` - StorageManager with temp database
- `greenstack` - IODDManager with temp database

### API Fixtures
- `test_client` - FastAPI TestClient
- `api_client_with_temp_db` - TestClient with isolated database

### Data Fixtures
- `sample_device_data` - Sample device information dict
- `sample_parameter_data` - Sample parameter information dict

## Writing New Tests

### Test File Naming

Test files should be named `test_*.py` and placed in the `tests/` directory.

### Test Function Naming

Test functions should be named `test_*` and clearly describe what they test:

```python
def test_parse_valid_iodd_file():
    """Test parsing of a valid IODD file."""
    # Test implementation
```

### Using Fixtures

```python
def test_with_fixtures(sample_iodd_content, storage_manager):
    """Test using multiple fixtures."""
    # Fixtures are automatically provided by pytest
    parser = IODDParser(sample_iodd_content)
    profile = parser.parse()

    device_id = storage_manager.store_device(...)
    assert device_id > 0
```

### Test Organization

Organize tests into classes by functionality:

```python
class TestDeviceManagement:
    """Test cases for device management."""

    def test_create_device(self):
        """Test device creation."""
        pass

    def test_update_device(self):
        """Test device updates."""
        pass
```

### Assertions

Use clear, specific assertions:

```python
# Good
assert device.product_name == "Expected Name"
assert len(devices) == 3
assert response.status_code == 200

# Avoid
assert device  # Too vague
assert True  # Meaningless
```

### Test Data

- Use fixtures for reusable test data
- Keep test data small and focused
- Use the `fixtures/` directory for sample files

## Coverage Goals

Target minimum coverage levels:

- **Overall**: 70%+
- **Core modules** (greenstack.py): 80%+
- **API endpoints** (api.py): 75%+
- **Critical paths**: 90%+

## Continuous Integration

Tests are automatically run on:

- Every push to feature branches
- Every pull request
- Main/master branch commits

See `.github/workflows/ci.yml` for CI configuration.

## Common Issues

### Database Locked

If you see "database is locked" errors:

```bash
# Clean up any stray .db files
find . -name "*.db" -delete
```

### Import Errors

If modules can't be imported:

```bash
# Ensure you're in the project root
cd /path/to/greenstack

# Install in development mode
pip install -e .
```

### Fixture Not Found

If pytest can't find a fixture, ensure `conftest.py` is in the `tests/` directory and the fixture is defined there.

## Contributing Tests

When adding new features:

1. Write tests first (TDD approach)
2. Ensure new tests pass
3. Maintain or improve coverage
4. Add docstrings to test functions
5. Use appropriate markers
6. Update this README if adding new test files or patterns

## Resources

- [Pytest Documentation](https://docs.pytest.org/)
- [FastAPI Testing](https://fastapi.tiangolo.com/tutorial/testing/)
- [Coverage.py](https://coverage.readthedocs.io/)

---

# Integration and Load Testing

## Integration Tests (`tests/integration/`)

Integration tests verify that GreenStack IoT components work together correctly.

### Setup

```bash
# Install integration test dependencies
pip install docker paho-mqtt influxdb-client redis psycopg2-binary

# Ensure Docker is running
docker --version
```

### Running Integration Tests

```bash
# Run all integration tests
pytest tests/integration/ -v

# Run specific test file
pytest tests/integration/test_mqtt_bridge.py -v

# Run with coverage
pytest tests/integration/ --cov=src --cov-report=html
```

### Available Tests

- **`test_mqtt_bridge.py`** - 20+ MQTT broker tests
  - Connection, publish/subscribe, QoS, retained messages, wildcards
- **`test_influx_ingestion.py`** - 15+ InfluxDB tests
  - Writes, queries, aggregations, MQTT-to-InfluxDB pipeline

### Fixtures

Integration tests use Docker containers as fixtures:

- `mqtt_broker` - Mosquitto MQTT broker
- `mqtt_client` - Connected MQTT client
- `influxdb_server` - InfluxDB 2.x server
- `influxdb_client` - Connected InfluxDB client
- `redis_server` - Redis cache server
- `redis_client` - Connected Redis client
- `postgres_server` - PostgreSQL database
- `postgres_connection` - Database connection

## Load Testing (`tests/load/`)

Performance testing using Locust.

### Setup

```bash
# Install Locust
pip install locust

# Set authentication credentials
export TEST_USERNAME=admin
export TEST_PASSWORD=your_password
```

### Running Load Tests

```bash
# Start Locust web interface
cd tests/load
locust -f locustfile.py --host=http://localhost:8000

# Open http://localhost:8089 in browser
# Configure users and spawn rate

# Run headless (no web UI)
locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 \
    --spawn-rate 10 \
    --run-time 5m \
    --headless

# Generate HTML report
locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 \
    --spawn-rate 10 \
    --run-time 5m \
    --headless \
    --html load_test_report.html
```

### User Scenarios

- **`GreenStackUser`** - Normal user behavior (mixed workload)
- **`HighLoadUser`** - Stress testing (aggressive, short wait times)
- **`APIOnlyUser`** - Pure API performance (no file uploads)

### Performance Baselines

| Scenario | Users | RPS | P95 Latency | Error Rate |
|----------|-------|-----|-------------|------------|
| Normal | 50 | 150 | < 300ms | < 0.5% |
| High Load | 100 | 250 | < 500ms | < 2% |
| Stress | 200 | 400 | < 1500ms | < 5% |

### Load Test Types

**Normal Load Test:**
```bash
locust -f locustfile.py --host=http://localhost:8000 \
    --users 50 --spawn-rate 5 --run-time 10m GreenStackUser
```

**Stress Test:**
```bash
locust -f locustfile.py --host=http://localhost:8000 \
    --users 200 --spawn-rate 20 --run-time 5m HighLoadUser
```

**Spike Test:**
```bash
locust -f locustfile.py --host=http://localhost:8000 \
    --users 500 --spawn-rate 100 --run-time 2m
```

**Endurance Test:**
```bash
locust -f locustfile.py --host=http://localhost:8000 \
    --users 100 --spawn-rate 10 --run-time 2h
```

### Monitoring During Load Tests

Use Grafana dashboards to monitor:
- Application Overview Dashboard (request rates, latency)
- System Health Dashboard (CPU, memory, containers)
- Database Performance Dashboard (connections, query time)

Access dashboards at http://localhost:3000

## Troubleshooting

### Docker Container Issues

```bash
# Check Docker is running
docker ps

# Start Docker service (Linux)
sudo systemctl start docker

# Clean up test containers
docker ps -a | grep test- | awk '{print $1}' | xargs docker rm -f
```

### Port Conflicts

Integration tests use these ports:
- MQTT: 11883
- InfluxDB: 18086
- Redis: 16379
- PostgreSQL: 15432

If ports are in use:
```bash
# Linux/Mac
lsof -i :11883

# Windows
netstat -ano | findstr :11883
```

### Test Timeouts

If tests timeout, increase wait times in `conftest.py`:
```python
time.sleep(2)  # Increase from 1 to 2 seconds
```

## CI/CD Integration

Add to `.github/workflows/ci.yml`:

```yaml
- name: Run integration tests
  run: |
    pytest tests/integration/ -v --cov=src

- name: Run load tests
  run: |
    cd tests/load
    locust -f locustfile.py --host=http://localhost:8000 \
      --users 50 --spawn-rate 5 --run-time 2m --headless
```

## Additional Resources

- [Locust Documentation](https://docs.locust.io/)
- [Docker Python SDK](https://docker-py.readthedocs.io/)
- [Paho MQTT Python](https://www.eclipse.org/paho/index.php?page=clients/python/index.php)
- [InfluxDB Python Client](https://github.com/influxdata/influxdb-client-python)
