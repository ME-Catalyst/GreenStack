import React from 'react';
import { Code, Database, FileCode, Server, GitBranch, Package, Cpu, Settings } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsTabs, { DocsTab } from '../../../components/docs/DocsTabs';
import DocsAccordion, { DocsAccordionItem } from '../../../components/docs/DocsAccordion';
import DocsFlowchart from '../../../components/docs/DocsFlowchart';

export const metadata = {
  id: 'developer/backend',
  title: 'Backend Development Guide',
  description: 'Comprehensive guide to developing and extending the Greenstack backend API',
  category: 'developer',
  order: 3,
  keywords: ['backend', 'api', 'python', 'fastapi', 'development', 'parsers', 'services'],
  lastUpdated: '2025-01-17',
};

export default function BackendDevelopment() {
  return (
    <DocsPage>
      <DocsHero
        title="Backend Development Guide"
        description="Comprehensive guide to developing and extending the Greenstack backend API"
        icon={<Server className="w-12 h-12 text-brand-green" />}
      />

      <DocsSection title="Backend Architecture">
        <DocsParagraph>
          Greenstack's backend is built with FastAPI, a modern Python web framework. The architecture follows
          a modular design with clear separation of concerns:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <Server className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">API Layer</h4>
            <p className="text-sm text-muted-foreground mt-1">FastAPI routes and endpoints</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <FileCode className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Parsers</h4>
            <p className="text-sm text-muted-foreground mt-1">EDS file parsing logic</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Database className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Database</h4>
            <p className="text-sm text-muted-foreground mt-1">SQLAlchemy + Alembic migrations</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Settings className="w-6 h-6 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground">Configuration</h4>
            <p className="text-sm text-muted-foreground mt-1">Environment-based config</p>
          </div>
        </div>

        <DocsParagraph>
          The backend codebase is organized as follows:
        </DocsParagraph>

        <DocsCodeBlock language="plaintext">
{`src/
├── api.py                 # FastAPI application entry point
├── config.py              # Configuration management
├── routes/               # API route handlers
│   ├── eds_routes.py     # EDS file endpoints
│   ├── admin_routes.py   # Admin endpoints
│   ├── search_routes.py  # Search endpoints
│   ├── theme_routes.py   # Theme management
│   ├── service_routes.py # Service integration
│   ├── ticket_routes.py  # Ticket system
│   ├── mqtt_routes.py    # MQTT management
│   └── config_export_routes.py
├── parsers/              # File parsers
│   ├── eds_parser.py     # EDS file parser
│   ├── eds_package_parser.py
│   └── eds_diagnostics.py
└── utils/                # Utility modules
    └── parsing_quality.py

alembic/
└── versions/             # Database migrations
    ├── 001_initial_schema.py
    ├── 004_add_eds_tables.py
    ├── 013_create_ticket_system.py
    └── ...`}
        </DocsCodeBlock>
      </DocsSection>

      <DocsSection title="EDS Parser System">
        <DocsParagraph>
          The EDS parser is a core component that extracts device information from Electronic Data Sheet files.
        </DocsParagraph>

        <DocsAccordion>
          <DocsAccordionItem title="EDSParser Class" defaultOpen>
            <DocsParagraph>
              The <code className="text-brand-green">EDSParser</code> class in <code>src/parsers/eds_parser.py</code> provides comprehensive parsing of EDS files:
            </DocsParagraph>

            <DocsCodeBlock language="python" copy>
{`from src.parsers.eds_parser import EDSParser

# Initialize parser with EDS content
parser = EDSParser(eds_file_content)

# Extract device metadata
file_info = parser.get_file_info()
device_info = parser.get_device_info()

# Parse assemblies (I/O configuration)
assemblies = parser.get_assemblies()

# Parse parameters (configuration options)
parameters = parser.get_parameters()

# Parse modules (modular device support)
modules = parser.get_modules()

print(f"Device: {device_info['product_name']}")
print(f"Vendor: {device_info['vendor_name']}")
print(f"Assemblies: {len(assemblies)}")
print(f"Parameters: {len(parameters)}")`}
            </DocsCodeBlock>

            <DocsCallout type="info" title="Parser Architecture">
              <DocsParagraph>
                The parser uses a section-based approach, dividing the EDS file into sections like [File], [Device], [Assembly], and [Param]. Each section is parsed independently with specialized logic.
              </DocsParagraph>
            </DocsCallout>
          </DocsAccordionItem>

          <DocsAccordionItem title="Key Parser Methods">
            <div className="space-y-4">
              <div>
                <h5 className="font-semibold text-foreground mb-2">get_file_info()</h5>
                <DocsParagraph>
                  Extracts file metadata including filename, description, creation date, and revision.
                </DocsParagraph>
                <DocsCodeBlock language="python">
{`file_info = parser.get_file_info()
# Returns: {
#   'filename': 'device.eds',
#   'description': 'CompactLogix 5380 Controller',
#   'create_date': '02-15-2024',
#   'revision': '1.2'
# }`}
                </DocsCodeBlock>
              </div>

              <div>
                <h5 className="font-semibold text-foreground mb-2">get_device_info()</h5>
                <DocsParagraph>
                  Extracts device-specific information like vendor, product name, catalog number, and revision.
                </DocsParagraph>
                <DocsCodeBlock language="python">
{`device_info = parser.get_device_info()
# Returns: {
#   'vendor_id': '1',
#   'vendor_name': 'Rockwell Automation',
#   'product_name': 'CompactLogix 5380',
#   'catalog_number': '5069-L306ER',
#   'major_revision': '1',
#   'minor_revision': '2'
# }`}
                </DocsCodeBlock>
              </div>

              <div>
                <h5 className="font-semibold text-foreground mb-2">get_assemblies()</h5>
                <DocsParagraph>
                  Parses I/O assembly definitions that describe the data exchange format.
                </DocsParagraph>
                <DocsCodeBlock language="python">
{`assemblies = parser.get_assemblies()
# Returns: [
#   {
#     'instance': '100',
#     'type': 'Input',
#     'size': '32',
#     'path': '20 04 24 64 30 03'
#   },
#   ...
# ]`}
                </DocsCodeBlock>
              </div>

              <div>
                <h5 className="font-semibold text-foreground mb-2">get_parameters()</h5>
                <DocsParagraph>
                  Extracts configuration parameters with data types, ranges, and default values.
                </DocsParagraph>
                <DocsCodeBlock language="python">
{`parameters = parser.get_parameters()
# Returns: [
#   {
#     'instance': '1',
#     'name': 'IP Address',
#     'data_type': 'STRING',
#     'data_size': '20',
#     'default': '192.168.1.1',
#     'min': None,
#     'max': None,
#     'access': 'ReadWrite'
#   },
#   ...
# ]`}
                </DocsCodeBlock>
              </div>
            </div>
          </DocsAccordionItem>

          <DocsAccordionItem title="Adding Parser Features">
            <DocsParagraph>
              To extend the parser with new functionality, follow this pattern:
            </DocsParagraph>

            <DocsCodeBlock language="python" copy>
{`class EDSParser:
    def __init__(self, content: str):
        self.content = content
        self.sections = {}
        self._parse_sections()

    def get_custom_section(self) -> Dict[str, Any]:
        """Extract custom section data."""
        if 'CustomSection' not in self.sections:
            return {}

        section_content = self.sections['CustomSection']
        data = self._parse_key_value(section_content)

        return {
            'field1': data.get('Field1'),
            'field2': data.get('Field2'),
            # Process and return structured data
        }

    def _parse_key_value(self, content: str) -> Dict[str, str]:
        """Parse key-value pairs from section content."""
        result = {}
        for line in content.split('\\n'):
            if '=' in line:
                key, value = line.split('=', 1)
                result[key.strip()] = value.strip()
        return result`}
            </DocsCodeBlock>
          </DocsAccordionItem>
        </DocsAccordion>
      </DocsSection>

      <DocsSection title="API Routes Development">
        <DocsParagraph>
          API routes are organized by feature domain in the <code>src/routes/</code> directory.
        </DocsParagraph>

        <DocsTabs>
          <DocsTab label="Creating Routes" icon={<GitBranch className="w-4 h-4" />}>
            <DocsParagraph>
              To create a new API route, follow the FastAPI pattern:
            </DocsParagraph>

            <DocsCodeBlock language="python" copy>
{`from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from pydantic import BaseModel

router = APIRouter(prefix="/api/myfeature", tags=["myfeature"])

# Define request/response models
class MyFeatureRequest(BaseModel):
    name: str
    description: Optional[str] = None

class MyFeatureResponse(BaseModel):
    id: int
    name: str
    description: Optional[str]
    created_at: str

# Create endpoint
@router.post("/", response_model=MyFeatureResponse)
async def create_feature(request: MyFeatureRequest):
    """Create a new feature."""
    # Implementation
    return MyFeatureResponse(
        id=1,
        name=request.name,
        description=request.description,
        created_at="2025-01-17T10:00:00Z"
    )

# List endpoint
@router.get("/", response_model=List[MyFeatureResponse])
async def list_features(skip: int = 0, limit: int = 100):
    """List all features."""
    # Implementation
    return []

# Get single item
@router.get("/{feature_id}", response_model=MyFeatureResponse)
async def get_feature(feature_id: int):
    """Get a specific feature by ID."""
    # Implementation
    if not feature_exists(feature_id):
        raise HTTPException(status_code=404, detail="Feature not found")
    return MyFeatureResponse(...)

# Update endpoint
@router.put("/{feature_id}", response_model=MyFeatureResponse)
async def update_feature(feature_id: int, request: MyFeatureRequest):
    """Update a feature."""
    # Implementation
    return MyFeatureResponse(...)

# Delete endpoint
@router.delete("/{feature_id}")
async def delete_feature(feature_id: int):
    """Delete a feature."""
    # Implementation
    return {"success": True, "deleted_id": feature_id}`}
            </DocsCodeBlock>

            <DocsCallout type="tip" title="Register Routes">
              <DocsParagraph>
                Register new routes in <code>src/api.py</code>:
              </DocsParagraph>
              <DocsCodeBlock language="python">
{`from src.routes import myfeature_routes

app.include_router(myfeature_routes.router)`}
              </DocsCodeBlock>
            </DocsCallout>
          </DocsTab>

          <DocsTab label="Database Operations" icon={<Database className="w-4 h-4" />}>
            <DocsParagraph>
              Greenstack uses SQLAlchemy for database operations. Use the connection pooling pattern:
            </DocsParagraph>

            <DocsCodeBlock language="python" copy>
{`import sqlite3
from src.config import get_database_path

def get_db_connection():
    """Get database connection."""
    conn = sqlite3.connect(get_database_path())
    conn.row_factory = sqlite3.Row  # Enable dict-like access
    return conn

@router.get("/items")
async def get_items():
    """Query database items."""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "SELECT id, name, description FROM items WHERE active = ?",
            (True,)
        )
        items = [dict(row) for row in cursor.fetchall()]
        return items
    finally:
        conn.close()

@router.post("/items")
async def create_item(request: ItemRequest):
    """Insert new database item."""
    conn = get_db_connection()
    try:
        cursor = conn.execute(
            "INSERT INTO items (name, description) VALUES (?, ?)",
            (request.name, request.description)
        )
        conn.commit()
        return {"id": cursor.lastrowid}
    finally:
        conn.close()`}
            </DocsCodeBlock>

            <DocsCallout type="warning" title="SQL Injection Prevention">
              <DocsParagraph>
                Always use parameterized queries (the <code>?</code> placeholder) to prevent SQL injection attacks.
                Never construct SQL with string concatenation.
              </DocsParagraph>
            </DocsCallout>
          </DocsTab>

          <DocsTab label="Error Handling" icon={<Code className="w-4 h-4" />}>
            <DocsParagraph>
              Implement consistent error handling across all endpoints:
            </DocsParagraph>

            <DocsCodeBlock language="python" copy>
{`from fastapi import HTTPException
import logging

logger = logging.getLogger(__name__)

@router.get("/{item_id}")
async def get_item(item_id: int):
    """Get item with proper error handling."""
    try:
        conn = get_db_connection()
        try:
            cursor = conn.execute(
                "SELECT * FROM items WHERE id = ?",
                (item_id,)
            )
            item = cursor.fetchone()

            if not item:
                raise HTTPException(
                    status_code=404,
                    detail=f"Item {item_id} not found"
                )

            return dict(item)

        finally:
            conn.close()

    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Log unexpected errors
        logger.error(f"Error fetching item {item_id}: {e}")
        raise HTTPException(
            status_code=500,
            detail="Internal server error"
        )`}
            </DocsCodeBlock>
          </DocsTab>
        </DocsTabs>
      </DocsSection>

      <DocsSection title="Database Schema & Migrations">
        <DocsParagraph>
          Greenstack uses Alembic for database schema management. All schema changes are versioned as migrations.
        </DocsParagraph>

        <DocsAccordion>
          <DocsAccordionItem title="Current Schema Overview" defaultOpen>
            <DocsParagraph>
              The database schema includes the following major tables:
            </DocsParagraph>

            <div className="space-y-4 my-6">
              <div className="border border-border rounded-lg p-4">
                <h5 className="font-semibold text-foreground mb-2">eds_files</h5>
                <p className="text-sm text-muted-foreground">Main EDS file storage with metadata</p>
                <ul className="text-xs text-foreground mt-2 space-y-1">
                  <li>• id (PRIMARY KEY)</li>
                  <li>• filename, vendor, product_name, catalog_number</li>
                  <li>• upload_date, content_hash</li>
                </ul>
              </div>

              <div className="border border-border rounded-lg p-4">
                <h5 className="font-semibold text-foreground mb-2">eds_parameters</h5>
                <p className="text-sm text-muted-foreground">Device configuration parameters</p>
                <ul className="text-xs text-foreground mt-2 space-y-1">
                  <li>• id, eds_file_id (FOREIGN KEY)</li>
                  <li>• name, data_type, data_size</li>
                  <li>• default_value, min_value, max_value</li>
                </ul>
              </div>

              <div className="border border-border rounded-lg p-4">
                <h5 className="font-semibold text-foreground mb-2">eds_assemblies</h5>
                <p className="text-sm text-muted-foreground">I/O assembly definitions</p>
                <ul className="text-xs text-foreground mt-2 space-y-1">
                  <li>• id, eds_file_id (FOREIGN KEY)</li>
                  <li>• instance, type, size, path</li>
                </ul>
              </div>

              <div className="border border-border rounded-lg p-4">
                <h5 className="font-semibold text-foreground mb-2">tickets</h5>
                <p className="text-sm text-muted-foreground">Ticket tracking system</p>
                <ul className="text-xs text-foreground mt-2 space-y-1">
                  <li>• id, title, description, status</li>
                  <li>• priority, created_at, updated_at</li>
                </ul>
              </div>
            </div>
          </DocsAccordionItem>

          <DocsAccordionItem title="Creating Migrations">
            <DocsParagraph>
              To create a new database migration:
            </DocsParagraph>

            <DocsCodeBlock language="bash" copy>
{`# Create a new migration
alembic revision -m "add_new_feature_table"

# This creates a new file in alembic/versions/`}
            </DocsCodeBlock>

            <DocsParagraph>
              Edit the generated migration file:
            </DocsParagraph>

            <DocsCodeBlock language="python" copy>
{`"""add_new_feature_table

Revision ID: 015_add_feature
Revises: 014_add_performance_indexes
Create Date: 2025-01-17 10:00:00
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers
revision = '015_add_feature'
down_revision = '014_add_performance_indexes'

def upgrade():
    """Create new table."""
    op.create_table(
        'features',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('name', sa.String(255), nullable=False),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )

    # Add index
    op.create_index('ix_features_name', 'features', ['name'])

def downgrade():
    """Rollback changes."""
    op.drop_index('ix_features_name', table_name='features')
    op.drop_table('features')`}
            </DocsCodeBlock>

            <DocsParagraph>
              Apply the migration:
            </DocsParagraph>

            <DocsCodeBlock language="bash" copy>
{`# Apply all pending migrations
alembic upgrade head

# Rollback one migration
alembic downgrade -1

# View migration history
alembic history`}
            </DocsCodeBlock>
          </DocsAccordionItem>
        </DocsAccordion>
      </DocsSection>

      <DocsSection title="Configuration Management">
        <DocsParagraph>
          Backend configuration is managed through <code>src/config.py</code> using environment variables.
        </DocsParagraph>

        <DocsCodeBlock language="python" copy>
{`import os
from pathlib import Path

class Config:
    """Application configuration."""

    # Environment
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')
    DEBUG = os.getenv('DEBUG', 'true').lower() == 'true'

    # API Settings
    API_HOST = os.getenv('API_HOST', '0.0.0.0')
    API_PORT = int(os.getenv('API_PORT', '8000'))

    # Database
    DATABASE_URL = os.getenv(
        'IODD_DATABASE_URL',
        'sqlite:///./greenstack.db'
    )

    # File Storage
    UPLOAD_DIR = Path(os.getenv('UPLOAD_DIR', './uploads'))
    MAX_UPLOAD_SIZE = int(os.getenv('MAX_UPLOAD_SIZE', '52428800'))  # 50MB

    @classmethod
    def get_database_path(cls) -> str:
        """Get absolute database path."""
        if cls.DATABASE_URL.startswith('sqlite:///'):
            return cls.DATABASE_URL.replace('sqlite:///', '')
        return cls.DATABASE_URL

# Usage in routes
from src.config import Config

if Config.DEBUG:
    print("Debug mode enabled")`}
        </DocsCodeBlock>
      </DocsSection>

      <DocsSection title="Testing Backend Code">
        <DocsParagraph>
          Write tests for backend functionality using pytest:
        </DocsParagraph>

        <DocsCodeBlock language="python" copy>
{`import pytest
from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_create_item():
    """Test creating a new item."""
    response = client.post(
        "/api/items",
        json={"name": "Test Item", "description": "Test"}
    )
    assert response.status_code == 201
    data = response.json()
    assert data["name"] == "Test Item"
    assert "id" in data

def test_get_item():
    """Test retrieving an item."""
    # Create item first
    create_response = client.post(
        "/api/items",
        json={"name": "Test Item"}
    )
    item_id = create_response.json()["id"]

    # Get item
    response = client.get(f"/api/items/{item_id}")
    assert response.status_code == 200
    assert response.json()["name"] == "Test Item"

def test_get_nonexistent_item():
    """Test 404 for missing item."""
    response = client.get("/api/items/99999")
    assert response.status_code == 404`}
        </DocsCodeBlock>

        <DocsCodeBlock language="bash" copy>
{`# Run tests
pytest tests/

# Run with coverage
pytest --cov=src tests/`}
        </DocsCodeBlock>
      </DocsSection>

      <DocsSection title="Best Practices">
        <div className="space-y-4">
          <DocsCallout type="success" title="Code Organization">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Keep routes focused on HTTP layer - delegate business logic to service modules</li>
              <li>Use type hints for all function parameters and return values</li>
              <li>Write docstrings for all public functions and classes</li>
              <li>Keep functions small and focused on a single responsibility</li>
            </ul>
          </DocsCallout>

          <DocsCallout type="info" title="Performance">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Use database connection pooling for concurrent requests</li>
              <li>Add indexes for frequently queried columns</li>
              <li>Implement pagination for list endpoints (default limit: 100 items)</li>
              <li>Cache expensive computations using functools.lru_cache</li>
            </ul>
          </DocsCallout>

          <DocsCallout type="warning" title="Security">
            <ul className="list-disc list-inside space-y-1 text-sm">
              <li>Always validate user input with Pydantic models</li>
              <li>Use parameterized SQL queries to prevent injection</li>
              <li>Sanitize file uploads and validate file types</li>
              <li>Implement rate limiting for public endpoints</li>
            </ul>
          </DocsCallout>
        </div>
      </DocsSection>

      <DocsSection title="Next Steps">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a href="/docs/developer/frontend" className="border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <Code className="w-8 h-8 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Frontend Development</h4>
            <p className="text-sm text-muted-foreground">Learn React frontend development</p>
          </a>

          <a href="/docs/api/endpoints" className="border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <FileCode className="w-8 h-8 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground mb-1">API Reference</h4>
            <p className="text-sm text-muted-foreground">Complete endpoint documentation</p>
          </a>

          <a href="/docs/developer/contributing" className="border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <GitBranch className="w-8 h-8 text-brand-green mb-2" />
            <h4 className="font-semibold text-foreground mb-1">Contributing</h4>
            <p className="text-sm text-muted-foreground">Contribute to Greenstack</p>
          </a>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
