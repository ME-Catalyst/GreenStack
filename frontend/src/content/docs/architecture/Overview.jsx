import React from 'react';
import { Boxes, Database, Server, Shield, Zap, GitBranch } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsList, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsTabs from '../../../components/docs/DocsTabs';
import { ThreeTierArchitecture } from '../../../components/docs/DocsDiagram';

export const metadata = {
  id: 'architecture/overview',
  title: 'System Architecture',
  description: 'Comprehensive overview of Greenstack system architecture, components, and design patterns',
  category: 'architecture',
  order: 1,
  keywords: ['architecture', 'system design', 'components', 'technology stack', 'data flow', 'security'],
  lastUpdated: '2025-01-17',
};

export default function Architecture() {
  return (
    <DocsPage>
      <DocsHero
        title="System Architecture"
        description="Comprehensive overview of Greenstack's architecture, technology stack, and design patterns"
        icon={<Boxes className="w-12 h-12 text-brand-green" />}
      />

      <DocsSection title="Overview">
        <DocsParagraph>
          Greenstack is a comprehensive intelligent device management platform for importing, managing, and analyzing
          IO-Link Device Description (IODD) and EtherNet/IP (EDS) device configurations. The system provides a REST API
          backend, modern React frontend with advanced UX features, and complete database storage for device data.
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4 my-6">
          <div className="border border-border rounded-lg p-4 text-center">
            <Server className="w-8 h-8 text-brand-green mx-auto mb-3" />
            <h4 className="font-semibold text-foreground mb-1">FastAPI Backend</h4>
            <p className="text-xs text-muted-foreground">
              High-performance async API with automatic validation
            </p>
          </div>

          <div className="border border-border rounded-lg p-4 text-center">
            <Boxes className="w-8 h-8 text-brand-green mx-auto mb-3" />
            <h4 className="font-semibold text-foreground mb-1">React Frontend</h4>
            <p className="text-xs text-muted-foreground">
              Modern UI with dark/light theme and advanced features
            </p>
          </div>

          <div className="border border-border rounded-lg p-4 text-center">
            <Database className="w-8 h-8 text-brand-green mx-auto mb-3" />
            <h4 className="font-semibold text-foreground mb-1">SQLite/PostgreSQL</h4>
            <p className="text-xs text-muted-foreground">
              Flexible database with migration support
            </p>
          </div>

          <div className="border border-border rounded-lg p-4 text-center">
            <Shield className="w-8 h-8 text-brand-green mx-auto mb-3" />
            <h4 className="font-semibold text-foreground mb-1">Secure by Design</h4>
            <p className="text-xs text-muted-foreground">
              Multi-layered security with input validation
            </p>
          </div>
        </div>

        <DocsCallout type="info" title="Core Capabilities">
          <DocsList
            items={[
              'Import and parse IODD XML files and EDS device descriptions',
              'Multi-file and nested ZIP import support',
              'Interactive device configuration interface with smart controls',
              'RESTful API for comprehensive device management',
              'Web-based dashboard with analytics and data visualization',
              'Dark/light theme with system preference detection',
              'Comprehensive keyboard shortcuts for power users',
            ]}
          />
        </DocsCallout>
      </DocsSection>

      <DocsSection title="High-Level Architecture">
        <DocsParagraph>
          Greenstack follows a classic three-tier architecture with clear separation between presentation,
          business logic, and data layers.
        </DocsParagraph>

        {/* Interactive Architecture Diagram */}
        <ThreeTierArchitecture />

        <DocsCallout type="tip" title="Request Flow">
          <DocsParagraph>
            A typical request flows: User Action → React Component → API Endpoint → Business Logic →
            Database/Storage → Response → UI Update. This ensures clear separation of concerns and maintainability.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      <DocsSection title="Technology Stack">
        <DocsParagraph>
          Greenstack is built with modern, production-ready technologies chosen for performance, developer experience,
          and long-term maintainability.
        </DocsParagraph>

        <DocsTabs
          tabs={[
            {
              label: 'Backend',
              content: (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border border-border rounded-lg p-4">
                      <h5 className="font-semibold text-foreground mb-2">Core Framework</h5>
                      <DocsList
                        items={[
                          <span><strong>Python 3.10+</strong>: Modern async/await support</span>,
                          <span><strong>FastAPI 0.100+</strong>: High-performance async web framework</span>,
                          <span><strong>Uvicorn</strong>: ASGI server for production</span>,
                          <span><strong>Pydantic</strong>: Data validation and serialization</span>,
                        ]}
                        className="text-sm"
                      />
                    </div>

                    <div className="border border-border rounded-lg p-4">
                      <h5 className="font-semibold text-foreground mb-2">Data & Parsing</h5>
                      <DocsList
                        items={[
                          <span><strong>SQLAlchemy</strong>: Powerful ORM for database operations</span>,
                          <span><strong>Alembic</strong>: Database migration management</span>,
                          <span><strong>lxml</strong>: Fast XML parsing and processing</span>,
                          <span><strong>SQLite/PostgreSQL</strong>: Flexible database options</span>,
                        ]}
                        className="text-sm"
                      />
                    </div>
                  </div>

                  <DocsCodeBlock language="bash" title="Backend Dependencies">
{`# Core framework
fastapi==0.100+
uvicorn[standard]
pydantic

# Database
sqlalchemy
alembic
psycopg2-binary  # PostgreSQL driver

# XML parsing
lxml

# Utilities
python-dotenv
python-multipart`}
                  </DocsCodeBlock>
                </div>
              ),
            },
            {
              label: 'Frontend',
              content: (
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="border border-border rounded-lg p-4">
                      <h5 className="font-semibold text-foreground mb-2">UI Framework</h5>
                      <DocsList
                        items={[
                          <span><strong>React 18.2</strong>: Modern UI library with hooks</span>,
                          <span><strong>Vite 4.5</strong>: Lightning-fast build tool</span>,
                          <span><strong>React Router</strong>: Client-side routing</span>,
                          <span><strong>Axios</strong>: HTTP client for API calls</span>,
                        ]}
                        className="text-sm"
                      />
                    </div>

                    <div className="border border-border rounded-lg p-4">
                      <h5 className="font-semibold text-foreground mb-2">Styling & Components</h5>
                      <DocsList
                        items={[
                          <span><strong>Tailwind CSS</strong>: Utility-first CSS framework</span>,
                          <span><strong>shadcn/ui</strong>: High-quality component library</span>,
                          <span><strong>Lucide React</strong>: Beautiful icon set</span>,
                          <span><strong>Framer Motion</strong>: Animation library</span>,
                        ]}
                        className="text-sm"
                      />
                    </div>
                  </div>

                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mt-4">
                    <div className="border border-border rounded-lg p-4">
                      <h5 className="font-semibold text-foreground mb-2">Data Visualization</h5>
                      <DocsList
                        items={[
                          <span><strong>Chart.js</strong>: Interactive charts</span>,
                          <span><strong>react-chartjs-2</strong>: React wrapper for Chart.js</span>,
                          <span><strong>Three.js</strong>: 3D graphics (optional)</span>,
                        ]}
                        className="text-sm"
                      />
                    </div>

                    <div className="border border-border rounded-lg p-4">
                      <h5 className="font-semibold text-foreground mb-2">State Management</h5>
                      <DocsList
                        items={[
                          <span><strong>Context API</strong>: Global state (theme)</span>,
                          <span><strong>React Hooks</strong>: Local component state</span>,
                          <span><strong>Custom Hooks</strong>: Reusable logic (keyboard shortcuts)</span>,
                        ]}
                        className="text-sm"
                      />
                    </div>
                  </div>

                  <DocsCodeBlock language="json" title="Frontend Dependencies (package.json)">
{`{
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.x",
    "axios": "^1.6.0",
    "chart.js": "^4.x",
    "react-chartjs-2": "^5.x",
    "framer-motion": "^10.x",
    "lucide-react": "^0.x"
  },
  "devDependencies": {
    "vite": "^4.5.0",
    "tailwindcss": "^3.x",
    "@vitejs/plugin-react": "^4.x"
  }
}`}
                  </DocsCodeBlock>
                </div>
              ),
            },
            {
              label: 'Development',
              content: (
                <div className="space-y-4">
                  <div className="border border-border rounded-lg p-4">
                    <h5 className="font-semibold text-foreground mb-2">Development Tools</h5>
                    <DocsList
                      items={[
                        <span><strong>Git</strong>: Version control with feature branch workflow</span>,
                        <span><strong>Black</strong>: Python code formatter</span>,
                        <span><strong>Ruff</strong>: Fast Python linter</span>,
                        <span><strong>ESLint</strong>: JavaScript linter</span>,
                        <span><strong>Prettier</strong>: Code formatter for JavaScript</span>,
                        <span><strong>pytest</strong>: Python testing framework</span>,
                        <span><strong>Vitest</strong>: Fast unit testing for Vite</span>,
                      ]}
                    />
                  </div>

                  <div className="border border-border rounded-lg p-4">
                    <h5 className="font-semibold text-foreground mb-2">DevOps & Deployment</h5>
                    <DocsList
                      items={[
                        <span><strong>Docker</strong>: Containerization platform</span>,
                        <span><strong>Docker Compose</strong>: Multi-container orchestration</span>,
                        <span><strong>Nginx</strong>: Reverse proxy and static file server</span>,
                        <span><strong>Systemd</strong>: Service management</span>,
                        <span><strong>Let's Encrypt</strong>: Free SSL certificates</span>,
                      ]}
                    />
                  </div>
                </div>
              ),
            },
          ]}
          className="my-6"
        />
      </DocsSection>

      <DocsSection title="Data Flow">
        <DocsParagraph>
          Understanding how data flows through the system is crucial for development and troubleshooting.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-3">IODD Import Workflow</h5>
            <div className="space-y-3 text-sm">
              <div className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-green text-white flex items-center justify-center text-xs font-bold">1</span>
                <div>
                  <p className="font-semibold text-foreground">User Upload</p>
                  <p className="text-muted-foreground">User uploads IODD/ZIP file via web interface</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-green text-white flex items-center justify-center text-xs font-bold">2</span>
                <div>
                  <p className="font-semibold text-foreground">File Validation</p>
                  <p className="text-muted-foreground">API validates file size, type, and checks for ZIP nesting</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-green text-white flex items-center justify-center text-xs font-bold">3</span>
                <div>
                  <p className="font-semibold text-foreground">XML Parsing</p>
                  <p className="text-muted-foreground">IODD Parser extracts device info, parameters, menus, and assets</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-green text-white flex items-center justify-center text-xs font-bold">4</span>
                <div>
                  <p className="font-semibold text-foreground">Database Storage</p>
                  <p className="text-muted-foreground">Data stored in structured tables with proper relationships</p>
                </div>
              </div>

              <div className="flex items-start gap-3">
                <span className="flex-shrink-0 w-6 h-6 rounded-full bg-brand-green text-white flex items-center justify-center text-xs font-bold">5</span>
                <div>
                  <p className="font-semibold text-foreground">Success Response</p>
                  <p className="text-muted-foreground">Frontend displays device in library with full details available</p>
                </div>
              </div>
            </div>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-3">Device Details Request</h5>
            <DocsParagraph className="text-sm text-muted-foreground mb-3">
              When viewing device details, the frontend makes parallel API requests for optimal performance:
            </DocsParagraph>
            <DocsList
              items={[
                <span><code>GET /api/iodd/{'<id>'}</code> - Device basic information</span>,
                <span><code>GET /api/iodd/{'<id>'}/parameters</code> - All device parameters</span>,
                <span><code>GET /api/iodd/{'<id>'}/config-schema</code> - Enriched menu structure</span>,
                <span><code>GET /api/iodd/{'<id>'}/assets</code> - Embedded images and documents</span>,
              ]}
              className="text-sm"
            />
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Database Architecture">
        <DocsParagraph>
          Greenstack uses a normalized relational database schema designed for efficient querying and data integrity.
        </DocsParagraph>

        <div className="my-6 space-y-4">
          <DocsCallout type="info" title="Design Principles">
            <DocsList
              items={[
                'Normalized to 3NF to minimize data redundancy',
                'Foreign keys enforce referential integrity',
                'Indexes optimize common query patterns',
                'JSON columns provide flexibility for complex data',
                'Timestamps track creation and modification',
              ]}
            />
          </DocsCallout>

          <div className="border border-border rounded-lg p-4 bg-surface">
            <h5 className="font-semibold text-foreground mb-3">Core Tables</h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div className="border border-border rounded p-3 bg-background">
                <div className="font-semibold text-foreground mb-2">iodd_devices</div>
                <DocsList
                  items={[
                    'Device identification (vendor_id, device_id)',
                    'Product info (name, manufacturer)',
                    'IODD version and import date',
                    'Full XML content stored',
                  ]}
                  className="text-xs"
                />
              </div>

              <div className="border border-border rounded p-3 bg-background">
                <div className="font-semibold text-foreground mb-2">parameters</div>
                <DocsList
                  items={[
                    'Parameter index and name',
                    'Data type and access rights',
                    'Default values',
                    'Enumeration values (JSON)',
                  ]}
                  className="text-xs"
                />
              </div>

              <div className="border border-border rounded p-3 bg-background">
                <div className="font-semibold text-foreground mb-2">ui_menus</div>
                <DocsList
                  items={[
                    'Menu structure and hierarchy',
                    'Menu items with variable references',
                    'Access right restrictions',
                  ]}
                  className="text-xs"
                />
              </div>

              <div className="border border-border rounded p-3 bg-background">
                <div className="font-semibold text-foreground mb-2">iodd_assets</div>
                <DocsList
                  items={[
                    'Embedded images and documents',
                    'BLOB storage for binary data',
                    'Content type and file name',
                  ]}
                  className="text-xs"
                />
              </div>
            </div>
          </div>

          <DocsCodeBlock language="sql" title="Example Index Strategy">
{`-- Composite index for device lookup
CREATE INDEX idx_device_vendor ON iodd_devices(vendor_id, device_id);

-- Foreign key indexes for join performance
CREATE INDEX idx_params_device ON parameters(device_id);
CREATE INDEX idx_menu_device ON ui_menus(device_id);
CREATE INDEX idx_assets_device ON iodd_assets(device_id);

-- Partial index for active devices
CREATE INDEX idx_active_devices ON iodd_devices(import_date)
WHERE deleted_at IS NULL;`}
          </DocsCodeBlock>
        </div>
      </DocsSection>

      <DocsSection title="Security Architecture">
        <DocsParagraph>
          Greenstack implements defense-in-depth security with multiple layers of protection.
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-3 flex items-center gap-2">
              <Shield className="w-5 h-5 text-brand-green" />
              Implemented (v2.0)
            </h5>
            <DocsList
              items={[
                'CORS configuration (localhost origins)',
                'File size limits (configurable)',
                'File type validation (.xml, .zip, .iodd, .eds)',
                'SQL injection protection (parameterized queries)',
                'Path traversal protection (sanitized paths)',
                'Input validation (Pydantic models)',
                'XSS prevention (React auto-escaping)',
                'Secure headers (FastAPI middleware)',
              ]}
              className="text-sm"
            />
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-3 flex items-center gap-2">
              <Shield className="w-5 h-5 text-yellow-500" />
              Planned (v3.0)
            </h5>
            <DocsList
              items={[
                'JWT authentication for user sessions',
                'Role-based access control (RBAC)',
                'API key authentication',
                'Data encryption at rest',
                'Comprehensive audit logging',
                'Rate limiting per user/IP',
                'Two-factor authentication (2FA)',
              ]}
              className="text-sm"
            />
          </div>
        </div>

        <DocsCallout type="warning" title="Production Security">
          <DocsParagraph>
            For production deployments, always configure CORS to specific domains, disable debug mode, and restrict
            API documentation access. See the <DocsLink href="/docs/user-guide/configuration" external={false}>
            Configuration Guide</DocsLink> for security best practices.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      <DocsSection title="Performance Optimization">
        <DocsParagraph>
          Greenstack is optimized for performance through caching, efficient database queries, and frontend optimizations.
        </DocsParagraph>

        <DocsTabs
          tabs={[
            {
              label: 'Caching',
              content: (
                <div className="space-y-4">
                  <div className="border border-border rounded-lg p-4">
                    <h5 className="font-semibold text-foreground mb-2">Multi-Tier Caching Strategy</h5>
                    <DocsList
                      items={[
                        <span><strong>L1: Browser Cache</strong> - Static assets cached for 24h</span>,
                        <span><strong>L2: Application Cache</strong> - In-memory LRU cache for API responses</span>,
                        <span><strong>L3: React Memoization</strong> - useMemo and useCallback to prevent re-renders</span>,
                        <span><strong>L4: Database Query Cache</strong> - SQLAlchemy query result caching</span>,
                      ]}
                    />
                  </div>

                  <DocsCodeBlock language="python" title="API Response Caching Example">
{`from functools import lru_cache

# Device list cached for 5 minutes
@lru_cache(maxsize=32, ttl=300)
def get_all_devices():
    return db.query(Device).all()

# Device details cached for 30 minutes
@lru_cache(maxsize=128, ttl=1800)
def get_device_details(device_id):
    return db.query(Device).filter_by(id=device_id).first()`}
                  </DocsCodeBlock>
                </div>
              ),
            },
            {
              label: 'Database',
              content: (
                <div className="space-y-4">
                  <div className="border border-border rounded-lg p-4">
                    <h5 className="font-semibold text-foreground mb-2">Query Optimization Techniques</h5>
                    <DocsList
                      items={[
                        'Strategic indexes on frequently queried columns',
                        'Eager loading to prevent N+1 query problems',
                        'Connection pooling for better resource utilization',
                        'Pagination for large result sets',
                        'Query result caching for expensive operations',
                      ]}
                    />
                  </div>

                  <DocsCallout type="success" title="Performance Metrics">
                    <div className="grid grid-cols-2 gap-3 text-sm mt-2">
                      <div>
                        <div className="font-semibold">Device List API</div>
                        <div className="text-muted-foreground">~50ms (target: &lt;100ms)</div>
                      </div>
                      <div>
                        <div className="font-semibold">Device Details API</div>
                        <div className="text-muted-foreground">~120ms (target: &lt;200ms)</div>
                      </div>
                      <div>
                        <div className="font-semibold">Config Schema API</div>
                        <div className="text-muted-foreground">~250ms (target: &lt;300ms)</div>
                      </div>
                      <div>
                        <div className="font-semibold">Page Load (TTI)</div>
                        <div className="text-muted-foreground">~1.5s (target: &lt;2s)</div>
                      </div>
                    </div>
                  </DocsCallout>
                </div>
              ),
            },
            {
              label: 'Frontend',
              content: (
                <div className="space-y-4">
                  <div className="border border-border rounded-lg p-4">
                    <h5 className="font-semibold text-foreground mb-2">Frontend Optimizations</h5>
                    <DocsList
                      items={[
                        <span><strong>Code Splitting</strong>: Separate bundles for different routes</span>,
                        <span><strong>Lazy Loading</strong>: Components load on demand</span>,
                        <span><strong>Virtual Scrolling</strong>: Efficient rendering of large lists</span>,
                        <span><strong>Debounced Search</strong>: Reduces API calls during typing</span>,
                        <span><strong>Optimized Re-renders</strong>: React.memo and useMemo prevent unnecessary updates</span>,
                      ]}
                    />
                  </div>

                  <DocsCodeBlock language="javascript" title="React Optimization Example">
{`// Memoize expensive computations
const filteredDevices = useMemo(() => {
  return devices.filter(d => d.manufacturer === selectedMfg);
}, [devices, selectedMfg]);

// Cache callback functions
const handleClick = useCallback(() => {
  navigate(\`/device/\${id}\`);
}, [id]);

// Prevent unnecessary re-renders
const DeviceCard = React.memo(({ device }) => {
  return <div>{device.name}</div>;
});`}
                  </DocsCodeBlock>
                </div>
              ),
            },
          ]}
          className="my-6"
        />
      </DocsSection>

      <DocsSection title="Development Workflow">
        <DocsParagraph>
          Greenstack follows Git Flow with feature branches, automated testing, and CI/CD pipelines.
        </DocsParagraph>

        <div className="my-6 space-y-4">
          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-3 flex items-center gap-2">
              <GitBranch className="w-5 h-5 text-brand-green" />
              Branch Strategy
            </h5>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
              <div>
                <div className="font-semibold text-foreground mb-1">main</div>
                <p className="text-muted-foreground">Production-ready code, tagged releases</p>
              </div>
              <div>
                <div className="font-semibold text-foreground mb-1">develop</div>
                <p className="text-muted-foreground">Integration branch for features</p>
              </div>
              <div>
                <div className="font-semibold text-foreground mb-1">feature/*</div>
                <p className="text-muted-foreground">New features (merge to develop)</p>
              </div>
              <div>
                <div className="font-semibold text-foreground mb-1">hotfix/*</div>
                <p className="text-muted-foreground">Critical fixes (merge to main & develop)</p>
              </div>
            </div>
          </div>

          <div className="border border-border rounded-lg p-4">
            <h5 className="font-semibold text-foreground mb-3">CI/CD Pipeline Stages</h5>
            <div className="space-y-2 text-sm">
              <div className="flex items-center gap-3">
                <span className="flex-shrink-0 w-20 text-muted-foreground">~30s</span>
                <div className="flex-1 p-2 border border-border rounded bg-surface">Lint & Format</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="flex-shrink-0 w-20 text-muted-foreground">~45s</span>
                <div className="flex-1 p-2 border border-border rounded bg-surface">Type Checking</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="flex-shrink-0 w-20 text-muted-foreground">~2min</span>
                <div className="flex-1 p-2 border border-border rounded bg-surface">Unit Tests</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="flex-shrink-0 w-20 text-muted-foreground">~5min</span>
                <div className="flex-1 p-2 border border-border rounded bg-surface">Integration Tests</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="flex-shrink-0 w-20 text-muted-foreground">~1min</span>
                <div className="flex-1 p-2 border border-border rounded bg-surface">Security Scanning</div>
              </div>
              <div className="flex items-center gap-3">
                <span className="flex-shrink-0 w-20 text-muted-foreground">~2min</span>
                <div className="flex-1 p-2 border border-border rounded bg-surface">Build & Package</div>
              </div>
            </div>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Additional Resources">
        <DocsParagraph>
          Explore related documentation for deeper technical details:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/api/overview" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Documentation</h5>
            <p className="text-sm text-muted-foreground">Complete REST API reference with 142 endpoints</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/configuration" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Configuration Guide</h5>
            <p className="text-sm text-muted-foreground">Environment variables and deployment configuration</p>
          </DocsLink>

          <DocsLink href="/docs/components/overview" external={false} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Component Gallery</h5>
            <p className="text-sm text-muted-foreground">35+ React components with live examples</p>
          </DocsLink>

          <DocsLink href="https://github.com/ME-Catalyst/greenstack" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">GitHub Repository</h5>
            <p className="text-sm text-muted-foreground">Source code and issue tracker</p>
          </DocsLink>
        </div>

        <DocsCallout type="info" title="Detailed Architecture Documentation">
          <DocsParagraph>
            For comprehensive architecture diagrams, detailed component interactions, and in-depth technical analysis,
            see the complete <code>ARCHITECTURE.md</code> file in the docs/architecture directory.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>
    </DocsPage>
  );
}
