# GreenStack Developer Guide

**Version**: 1.0.0
**Last Updated**: January 2025

## Table of Contents

- [Getting Started](#getting-started)
- [Development Environment Setup](#development-environment-setup)
- [Project Structure](#project-structure)
- [Running the Application](#running-the-application)
- [Testing](#testing)
- [Code Style & Standards](#code-style--standards)
- [Contributing](#contributing)
- [Debugging](#debugging)
- [Common Development Tasks](#common-development-tasks)
- [Troubleshooting](#troubleshooting)

---

## Getting Started

### Prerequisites

**Required**:
- **Python**: 3.11 or higher
- **pip**: Latest version (comes with Python)
- **Git**: For version control

**Optional but Recommended**:
- **Docker**: For containerized development
- **Docker Compose**: For multi-service setups
- **VS Code** or **PyCharm**: IDE with Python support

### Quick Start

```bash
# Clone the repository
git clone https://github.com/yourusername/greenstack.git
cd greenstack

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Linux/Mac:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Run the application
python -m uvicorn src.api:app --reload

# Access the API
# Swagger UI: http://localhost:8000/docs
# ReDoc: http://localhost:8000/redoc
```

---

## Development Environment Setup

### Python Virtual Environment

**Why Virtual Environment?**
- Isolates project dependencies
- Prevents version conflicts
- Maintains reproducible builds

**Setup**:
```bash
# Create virtual environment
python -m venv venv

# Activate
# Windows (PowerShell):
venv\Scripts\Activate.ps1
# Windows (CMD):
venv\Scripts\activate.bat
# Linux/Mac:
source venv/bin/activate

# Verify activation
which python  # Should point to venv/bin/python
python --version  # Should be 3.11+
```

### Installing Dependencies

**Production Dependencies**:
```bash
pip install -r requirements.txt
```

**Development Dependencies** (testing, linting, etc.):
```bash
pip install -r requirements-dev.txt
```

**Key Dependencies**:
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `sqlalchemy` - ORM for database
- `pydantic` - Data validation
- `pytest` - Testing framework
- `ruff` - Linting and formatting

### IDE Configuration

**VS Code** (`.vscode/settings.json`):
```json
{
  "python.defaultInterpreterPath": "${workspaceFolder}/venv/bin/python",
  "python.linting.enabled": true,
  "python.linting.ruffEnabled": true,
  "python.formatting.provider": "black",
  "python.testing.pytestEnabled": true,
  "python.testing.pytestArgs": ["tests"],
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.organizeImports": true
  }
}
```

**PyCharm**:
1. File → Settings → Project → Python Interpreter
2. Add Interpreter → Existing Environment → Select `venv/bin/python`
3. Enable pytest: Settings → Tools → Python Integrated Tools → Testing → pytest

### Environment Variables

**Create `.env` file**:
```bash
# Application
APP_ENV=development
APP_VERSION=1.0.0
DEBUG=true

# API
API_HOST=0.0.0.0
API_PORT=8000
ENABLE_DOCS=true

# Database
DATABASE_URL=sqlite:///./greenstack.db

# Security
SECRET_KEY=your-secret-key-here-change-in-production
ADMIN_USERNAME=admin
ADMIN_PASSWORD=changeme

# Rate Limiting
RATE_LIMIT=100/minute

# CORS
CORS_ORIGINS=http://localhost:3000,http://localhost:8080

# External Services
GRAFANA_URL=http://localhost:3000
NODERED_URL=http://localhost:1880
MQTT_BROKER=localhost:1883

# Monitoring
SENTRY_DSN=  # Optional: Sentry error tracking
ENVIRONMENT=development
```

**Load Environment Variables**:
```python
from dotenv import load_dotenv
load_dotenv()
```

---

## Project Structure

```
greenstack/
├── src/                        # Source code
│   ├── api.py                  # FastAPI application
│   ├── config.py               # Configuration management
│   ├── greenstack.py           # Main IODDManager class
│   ├── models/                 # Data models
│   │   ├── __init__.py
│   │   ├── device_profile.py
│   │   ├── enums.py
│   │   └── ...
│   ├── parsing/                # IODD/EDS parsers
│   │   ├── __init__.py
│   │   ├── iodd_parser.py
│   │   └── eds_parser.py
│   ├── storage/                # Database layer
│   │   ├── __init__.py
│   │   └── storage_manager.py
│   ├── generation/             # Code generators
│   │   ├── __init__.py
│   │   ├── nodered_generator.py
│   │   └── nodered_flows.py
│   ├── routes/                 # API routes
│   │   ├── __init__.py
│   │   ├── flow_routes.py
│   │   ├── eds_routes.py
│   │   ├── search_routes.py
│   │   └── ...
│   └── services/               # External service integrations
│       ├── __init__.py
│       ├── grafana_manager.py
│       ├── nodered_manager.py
│       └── mqtt_manager.py
├── tests/                      # Test suite
│   ├── unit/                   # Unit tests
│   │   ├── test_parsing.py
│   │   ├── test_storage.py
│   │   ├── test_generation.py
│   │   └── ...
│   ├── integration/            # Integration tests
│   └── fixtures/               # Test data
├── docs/                       # Documentation
│   ├── API_REFERENCE.md
│   ├── ARCHITECTURE.md
│   ├── DEVELOPER_GUIDE.md
│   └── DATABASE_SCHEMA.md
├── alembic/                    # Database migrations
│   ├── versions/
│   └── env.py
├── iodd_storage/               # IODD file storage
├── requirements.txt            # Production dependencies
├── requirements-dev.txt        # Development dependencies
├── pytest.ini                  # Pytest configuration
├── docker-compose.yml          # Docker Compose configuration
├── Dockerfile                  # Docker image definition
└── README.md                   # Project overview
```

### Key Directories

**`src/`**: All application source code
- Organized by functional area (parsing, storage, generation, etc.)
- Each module has clear responsibility
- Use relative imports within src/

**`tests/`**: Comprehensive test suite
- `unit/`: Fast, isolated unit tests
- `integration/`: Tests with external dependencies
- `fixtures/`: Sample IODD/EDS files for testing

**`docs/`**: Project documentation
- Markdown format for GitHub compatibility
- Mermaid diagrams for architecture

---

## Running the Application

### Development Server

**Using Uvicorn directly**:
```bash
# Basic
python -m uvicorn src.api:app --reload

# With custom host/port
python -m uvicorn src.api:app --reload --host 0.0.0.0 --port 8000

# With log level
python -m uvicorn src.api:app --reload --log-level debug
```

**Using Python script**:
```python
# run.py
import uvicorn

if __name__ == "__main__":
    uvicorn.run(
        "src.api:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
```

### Docker Development

**Build and run**:
```bash
# Build image
docker build -t greenstack:dev .

# Run container
docker run -p 8000:8000 -v $(pwd):/app greenstack:dev

# Or use docker-compose
docker-compose up --build
```

**Docker Compose** (`docker-compose.yml`):
```yaml
version: '3.8'

services:
  api:
    build: .
    ports:
      - "8000:8000"
    volumes:
      - .:/app
      - ./iodd_storage:/app/iodd_storage
    environment:
      - DATABASE_URL=sqlite:///./greenstack.db
      - DEBUG=true
    command: uvicorn src.api:app --reload --host 0.0.0.0

  prometheus:
    image: prom/prometheus:latest
    ports:
      - "9090:9090"
    volumes:
      - ./prometheus.yml:/etc/prometheus/prometheus.yml

  grafana:
    image: grafana/grafana:latest
    ports:
      - "3000:3000"
    environment:
      - GF_SECURITY_ADMIN_PASSWORD=admin
```

### Database Setup

**Initialize database**:
```bash
# SQLite (automatic on first run)
python -c "from src.storage import StorageManager; StorageManager()"

# PostgreSQL (production)
# 1. Create database
createdb greenstack

# 2. Run migrations
alembic upgrade head
```

**Database Migrations** (Alembic):
```bash
# Create new migration
alembic revision --autogenerate -m "Add new table"

# Apply migrations
alembic upgrade head

# Rollback
alembic downgrade -1

# View migration history
alembic history
```

---

## Testing

### Running Tests

**All tests**:
```bash
pytest
```

**Specific test file**:
```bash
pytest tests/unit/test_parsing.py
```

**Specific test function**:
```bash
pytest tests/unit/test_parsing.py::test_parse_iodd_basic
```

**With coverage**:
```bash
pytest --cov=src --cov-report=html
# Open htmlcov/index.html to view coverage report
```

**With verbose output**:
```bash
pytest -v
```

**Stop on first failure**:
```bash
pytest -x
```

### Test Organization

**Unit Tests** (`tests/unit/`):
- Test individual functions/classes in isolation
- Mock external dependencies
- Fast execution (<1 second per test)

**Example**:
```python
# tests/unit/test_parsing.py
import pytest
from src.parsing import IODDParser

def test_parse_device_info():
    """Test parsing device information from IODD"""
    xml_content = """
    <IODevice>
        <DeviceInfo deviceId="12345" vendorId="67890">
            <ProductName>Temperature Sensor</ProductName>
        </DeviceInfo>
    </IODevice>
    """
    parser = IODDParser(xml_content)
    profile = parser.parse()

    assert profile.device_info.device_id == 12345
    assert profile.device_info.vendor_id == 67890
    assert profile.device_info.product_name == "Temperature Sensor"
```

**Integration Tests** (`tests/integration/`):
- Test component interactions
- Use real database (test instance)
- May involve file I/O or network calls

**Fixtures** (`tests/fixtures/`):
- Sample IODD files
- Test data files
- Reusable test resources

### Test Configuration

**`pytest.ini`**:
```ini
[pytest]
testpaths = tests
python_files = test_*.py
python_classes = Test*
python_functions = test_*
addopts =
    -v
    --strict-markers
    --tb=short
markers =
    slow: marks tests as slow (deselect with '-m "not slow"')
    integration: marks tests as integration tests
    unit: marks tests as unit tests
```

---

## Code Style & Standards

### Python Style Guide

**Follow PEP 8** with these conventions:
- Line length: 100 characters (not 79)
- Use 4 spaces for indentation
- Use double quotes for strings
- Use type hints for function signatures

**Example**:
```python
from typing import List, Optional

def process_device(
    device_id: int,
    parameters: List[str],
    options: Optional[dict] = None
) -> dict:
    """
    Process device with given parameters.

    Args:
        device_id: Unique device identifier
        parameters: List of parameter names to process
        options: Optional processing options

    Returns:
        Dictionary with processing results

    Raises:
        ValueError: If device_id is invalid
    """
    if device_id < 0:
        raise ValueError("device_id must be non-negative")

    result = {"device_id": device_id, "parameters": []}
    # ... processing logic
    return result
```

### Linting and Formatting

**Ruff** (all-in-one linter and formatter):
```bash
# Check code
ruff check src/

# Fix auto-fixable issues
ruff check --fix src/

# Format code
ruff format src/
```

**Type Checking with mypy**:
```bash
mypy src/
```

**Pre-commit Hook** (`.pre-commit-config.yaml`):
```yaml
repos:
  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.0
    hooks:
      - id: ruff
        args: [--fix]
      - id: ruff-format
```

### Documentation Standards

**Docstrings** (Google style):
```python
def generate_flow(device_id: int, flow_type: str = "monitoring") -> dict:
    """
    Generate a Node-RED flow for a device.

    This function creates a complete Node-RED flow including MQTT nodes,
    function nodes for data processing, and dashboard UI components.

    Args:
        device_id: Database ID of the device
        flow_type: Type of flow to generate. Options:
            - "monitoring": Real-time monitoring with dashboards
            - "control": Parameter control with UI controls
            - "custom": Combined monitoring and control

    Returns:
        Dictionary containing:
            - flow: List of Node-RED node definitions
            - node_count: Number of nodes in the flow
            - device_name: Product name from IODD

    Raises:
        ValueError: If device_id is invalid
        FileNotFoundError: If device IODD not found

    Example:
        >>> generate_flow(1, "monitoring")
        {
            "flow": [...],
            "node_count": 15,
            "device_name": "Temperature Sensor Pro"
        }
    """
    pass
```

---

## Contributing

### Git Workflow

**Branching Strategy**:
```bash
# Create feature branch
git checkout -b feature/add-plc-generator

# Make changes and commit
git add .
git commit -m "feat: Add PLC code generator"

# Push to remote
git push origin feature/add-plc-generator

# Create pull request on GitHub
```

**Commit Message Convention**:
```
<type>(<scope>): <subject>

<body>

<footer>
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

**Examples**:
```
feat(flows): Add batch flow generation endpoint

Implement POST /api/flows/batch/generate endpoint that allows
generating Node-RED flows for multiple devices in a single request.

Closes #123
```

### Pull Request Process

1. **Create feature branch**
2. **Write tests** for new functionality
3. **Update documentation** if needed
4. **Run tests** and ensure they pass
5. **Run linter** and fix any issues
6. **Create pull request** with clear description
7. **Wait for review** and address feedback
8. **Merge** after approval

---

## Debugging

### VS Code Debug Configuration

**`.vscode/launch.json`**:
```json
{
  "version": "0.2.0",
  "configurations": [
    {
      "name": "Python: FastAPI",
      "type": "python",
      "request": "launch",
      "module": "uvicorn",
      "args": [
        "src.api:app",
        "--reload",
        "--host", "0.0.0.0",
        "--port", "8000"
      ],
      "jinja": true,
      "justMyCode": true
    },
    {
      "name": "Python: Current File",
      "type": "python",
      "request": "launch",
      "program": "${file}",
      "console": "integratedTerminal"
    },
    {
      "name": "Python: Pytest",
      "type": "python",
      "request": "launch",
      "module": "pytest",
      "args": ["-v"],
      "console": "integratedTerminal"
    }
  ]
}
```

### Logging

**Configure logging**:
```python
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Use in code
logger.info("Processing device %d", device_id)
logger.warning("Parameter not found: %s", param_name)
logger.error("Failed to parse IODD: %s", error)
```

### Debugging Tips

**Print debugging**:
```python
# Quick debug
print(f"Device: {device_id}, Profile: {profile}")

# Better: use logging
logger.debug(f"Device: {device_id}, Profile: {profile}")
```

**IPython debugger** (pdb):
```python
# Add breakpoint
import pdb; pdb.set_trace()

# Or use built-in breakpoint() (Python 3.7+)
breakpoint()
```

**FastAPI request debugging**:
```python
from fastapi import Request

@app.middleware("http")
async def log_requests(request: Request, call_next):
    logger.info(f"{request.method} {request.url}")
    response = await call_next(request)
    logger.info(f"Status: {response.status_code}")
    return response
```

---

## Common Development Tasks

### Adding a New API Endpoint

1. **Create route file** (if needed): `src/routes/my_routes.py`
2. **Define Pydantic models** for request/response
3. **Implement endpoint** with proper documentation
4. **Register router** in `src/api.py`
5. **Write tests** in `tests/unit/test_my_routes.py`

**Example**:
```python
# src/routes/my_routes.py
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(prefix="/api/my", tags=["My Feature"])

class MyRequest(BaseModel):
    name: str
    value: int

class MyResponse(BaseModel):
    result: str
    count: int

@router.post("/process", response_model=MyResponse)
async def process_data(request: MyRequest):
    """Process data and return result"""
    return MyResponse(
        result=f"Processed {request.name}",
        count=request.value * 2
    )

# src/api.py
from src.routes import my_routes
app.include_router(my_routes.router)
```

### Adding a New Database Table

1. **Update models** in `src/models/`
2. **Create Alembic migration**: `alembic revision --autogenerate -m "Add table"`
3. **Review migration** in `alembic/versions/`
4. **Apply migration**: `alembic upgrade head`
5. **Update StorageManager** in `src/storage/storage_manager.py`

### Adding a New Code Generator

1. **Create generator class** in `src/generation/`
2. **Inherit from `AdapterGenerator`**
3. **Implement `generate()` method**
4. **Add platform to API endpoint**
5. **Write tests**

**Example**:
```python
# src/generation/plc_generator.py
from src.generation import AdapterGenerator
from src.models import DeviceProfile

class PLCGenerator(AdapterGenerator):
    @property
    def platform_name(self) -> str:
        return "plc"

    def generate(self, profile: DeviceProfile) -> dict:
        """Generate PLC function block code"""
        return {
            'function_block.st': self._generate_fb(profile),
            'data_types.st': self._generate_types(profile)
        }

    def _generate_fb(self, profile: DeviceProfile) -> str:
        # Implementation
        pass
```

---

## Troubleshooting

### Common Issues

**1. Module not found errors**:
```bash
# Ensure you're in project root
pwd

# Ensure virtual environment is activated
which python  # Should show venv/bin/python

# Reinstall dependencies
pip install -r requirements.txt
```

**2. Database locked**:
```bash
# Close all connections and restart
rm greenstack.db
python -m uvicorn src.api:app --reload
```

**3. Port already in use**:
```bash
# Find process using port 8000
# Linux/Mac:
lsof -i :8000
# Windows:
netstat -ano | findstr :8000

# Kill process or use different port
python -m uvicorn src.api:app --reload --port 8001
```

**4. Import errors**:
```python
# Use absolute imports from project root
from src.models import DeviceProfile  # Good
from models import DeviceProfile      # Bad
```

**5. Test failures**:
```bash
# Run with verbose output
pytest -v

# Run single test to isolate issue
pytest tests/unit/test_parsing.py::test_specific_function -v

# Check test fixtures
ls tests/fixtures/
```

---

## Additional Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [Pydantic Documentation](https://docs.pydantic.dev/)
- [SQLAlchemy Documentation](https://docs.sqlalchemy.org/)
- [Pytest Documentation](https://docs.pytest.org/)
- [IO-Link Specification](https://io-link.com/en/Technology/Specification.php)

---

## Need Help?

- **GitHub Issues**: https://github.com/yourusername/greenstack/issues
- **Documentation**: `/docs` directory
- **API Docs**: http://localhost:8000/docs

---

**Happy Coding!**
