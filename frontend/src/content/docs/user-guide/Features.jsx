import React from 'react';
import { Sparkles, Server, Globe, Database, Zap, Shield, Palette, BarChart3, Package, Code, FileText, Settings, AlertCircle } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'user-guide/features',
  title: 'Features Overview',
  description: 'Comprehensive overview of GreenStack features and capabilities',
  category: 'user-guide',
  order: 1,
  keywords: ['features', 'capabilities', 'overview', 'functionality'],
  lastUpdated: '2025-01-17',
};

export default function Features({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Features Overview"
        description="Industrial device configuration management for IODD and EDS files with modern web interface"
        icon={<Sparkles className="w-12 h-12 text-brand-green" />}
      />

      {/* Core Features */}
      <DocsSection title="Device Configuration Management">
        <DocsParagraph>
          GreenStack specializes in parsing, storing, and visualizing industrial device configuration files
          for IO-Link (IODD) and EtherNet/IP (EDS) protocols.
        </DocsParagraph>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Server className="w-6 h-6 text-brand-green" />
                <Badge>Core</Badge>
              </div>
              <CardTitle className="text-base">IO-Link IODD Support</CardTitle>
              <CardDescription>Complete device description file parsing</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Full IODD 1.0/1.1 XML parsing</li>
                <li>• Parameter extraction and organization</li>
                <li>• Menu structure parsing</li>
                <li>• Error/event code mapping</li>
                <li>• Process data visualization</li>
                <li>• Multi-language text support</li>
                <li>• Nested ZIP package support</li>
                <li>• Asset file management (icons, PDFs)</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Server className="w-6 h-6 text-brand-green" />
                <Badge>Core</Badge>
              </div>
              <CardTitle className="text-base">EtherNet/IP EDS Support</CardTitle>
              <CardDescription>Complete EDS file parsing and management</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• INI file parsing with section handling</li>
                <li>• Assembly configuration parsing</li>
                <li>• Port and module data extraction</li>
                <li>• Connection parameter mapping</li>
                <li>• Parameter categorization</li>
                <li>• Multi-revision support</li>
                <li>• Icon file extraction and display</li>
                <li>• Device grouping by vendor/product</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Web Interface */}
      <DocsSection title="Modern Web Interface">
        <DocsParagraph>
          React-based dashboard with responsive design, interactive visualizations, and smooth animations.
        </DocsParagraph>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Package className="w-6 h-6 text-brand-green" />
                <Badge variant="secondary">UI/UX</Badge>
              </div>
              <CardTitle className="text-base">Device Library</CardTitle>
              <CardDescription>Browse and manage device configurations</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Card-based device grid with thumbnails</li>
                <li>• Real-time search and filtering</li>
                <li>• Sort by vendor, product, or date</li>
                <li>• Bulk selection and deletion</li>
                <li>• Drag-and-drop file upload</li>
                <li>• Detailed device view with tabs</li>
                <li>• Parameter browsing by category</li>
                <li>• Export to JSON/ZIP</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <BarChart3 className="w-6 h-6 text-brand-green" />
                <Badge variant="secondary">UI/UX</Badge>
              </div>
              <CardTitle className="text-base">Analytics Dashboard</CardTitle>
              <CardDescription>Visual insights into your device library</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Manufacturer distribution charts</li>
                <li>• Device type breakdowns (IODD vs EDS)</li>
                <li>• Parameter count statistics</li>
                <li>• I/O configuration analysis</li>
                <li>• Storage usage metrics</li>
                <li>• Recent activity tracking</li>
                <li>• Interactive 3D visualizations</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Palette className="w-6 h-6 text-brand-green" />
                <Badge variant="secondary">UI/UX</Badge>
              </div>
              <CardTitle className="text-base">Theme System</CardTitle>
              <CardDescription>4 built-in themes with dark/light modes</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Default, Blue, Purple, Orange themes</li>
                <li>• Dark/light mode toggle</li>
                <li>• System preference detection</li>
                <li>• Smooth theme transitions</li>
                <li>• localStorage persistence</li>
                <li>• Consistent brand colors</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <AlertCircle className="w-6 h-6 text-brand-green" />
                <Badge variant="secondary">UI/UX</Badge>
              </div>
              <CardTitle className="text-base">Ticket System</CardTitle>
              <CardDescription>Track issues and feature requests</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Create tickets for devices</li>
                <li>• Priority levels (Low/Medium/High/Critical)</li>
                <li>• Status tracking (Open/In Progress/Resolved)</li>
                <li>• File attachments support</li>
                <li>• Comment threads</li>
                <li>• Device linkage</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Backend & API */}
      <DocsSection title="Backend & API">
        <DocsParagraph>
          FastAPI-powered backend with SQLite database and comprehensive REST API.
        </DocsParagraph>

        <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3 my-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Code className="w-6 h-6 text-brand-green" />
                <Badge variant="outline">Backend</Badge>
              </div>
              <CardTitle className="text-base">FastAPI Framework</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• Python 3.10+ async/await</li>
                <li>• Auto-generated OpenAPI docs</li>
                <li>• Type validation with Pydantic</li>
                <li>• Hot reload in development</li>
                <li>• CORS support</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Database className="w-6 h-6 text-brand-green" />
                <Badge variant="outline">Backend</Badge>
              </div>
              <CardTitle className="text-base">Database</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• SQLite with foreign keys</li>
                <li>• 30+ normalized tables</li>
                <li>• Full-text search indexes</li>
                <li>• BLOB storage for assets</li>
                <li>• Database health monitoring</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Shield className="w-6 h-6 text-brand-green" />
                <Badge variant="outline">Backend</Badge>
              </div>
              <CardTitle className="text-base">API Features</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-1 text-sm text-muted-foreground">
                <li>• RESTful endpoints (40+)</li>
                <li>• File upload/download</li>
                <li>• Bulk operations</li>
                <li>• Advanced search & filtering</li>
                <li>• Health check endpoint</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        <DocsCallout type="info" title="Interactive API Documentation">
          <DocsParagraph>
            Full Swagger/OpenAPI documentation is available at <code>http://localhost:8000/docs</code> when
            the server is running. Test all endpoints directly from your browser.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Admin Features */}
      <DocsSection title="Administration & Management">
        <DocsParagraph>
          Comprehensive admin console for system monitoring and database management.
        </DocsParagraph>

        <div className="grid gap-6 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Settings className="w-6 h-6 text-brand-green" />
                <Badge>Admin</Badge>
              </div>
              <CardTitle className="text-base">System Monitoring</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Real-time statistics overview</li>
                <li>• Database health checks</li>
                <li>• Foreign key integrity validation</li>
                <li>• Storage usage tracking</li>
                <li>• Recent activity logs</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <div className="flex items-center gap-2 mb-2">
                <Database className="w-6 h-6 text-brand-green" />
                <Badge>Admin</Badge>
              </div>
              <CardTitle className="text-base">Database Management</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Bulk deletion operations</li>
                <li>• Database export/backup</li>
                <li>• Integrity repair tools</li>
                <li>• Table statistics</li>
                <li>• Orphaned record cleanup</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Documentation */}
      <DocsSection title="Built-in Documentation">
        <DocsParagraph>
          Comprehensive in-platform documentation with search and navigation.
        </DocsParagraph>

        <div className="grid gap-6 md:grid-cols-3 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">User Guide</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Features overview</li>
                <li>• Web interface guide</li>
                <li>• Device management</li>
                <li>• Advanced features</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">API Reference</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Endpoint documentation</li>
                <li>• Request/response examples</li>
                <li>• OpenAPI specification</li>
                <li>• Authentication guide</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Developer Docs</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Architecture overview</li>
                <li>• Setup instructions</li>
                <li>• Contributing guide</li>
                <li>• Code examples</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Technical Stack */}
      <DocsSection title="Technical Stack">
        <div className="grid gap-6 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Frontend Technologies</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• React 18 with hooks</li>
                <li>• Vite for fast builds</li>
                <li>• Tailwind CSS for styling</li>
                <li>• Radix UI components</li>
                <li>• Axios for API calls</li>
                <li>• Lucide React icons</li>
                <li>• Chart.js for analytics</li>
                <li>• Three.js for 3D visualizations</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Backend Technologies</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• FastAPI framework</li>
                <li>• Python 3.10+</li>
                <li>• SQLite database</li>
                <li>• Uvicorn ASGI server</li>
                <li>• Pydantic for validation</li>
                <li>• lxml for XML parsing</li>
                <li>• configparser for INI files</li>
                <li>• PIL for image processing</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Current Limitations */}
      <DocsSection title="Current Limitations">
        <DocsParagraph className="mb-4">
          GreenStack is actively developed. Some features are planned for future releases:
        </DocsParagraph>

        <div className="space-y-3">
          <Card className="border-yellow-500/20">
            <CardHeader>
              <CardTitle className="text-base text-yellow-600 dark:text-yellow-400">Not Yet Implemented</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• User authentication and authorization</li>
                <li>• Multi-user support with permissions</li>
                <li>• Real-time device connectivity (IO-Link, EtherNet/IP)</li>
                <li>• Live telemetry monitoring</li>
                <li>• MQTT broker integration</li>
                <li>• Advanced rate limiting (use reverse proxy)</li>
              </ul>
            </CardContent>
          </Card>
        </div>

        <DocsCallout type="warning" title="Production Deployment">
          <DocsParagraph>
            For production use, deploy behind a reverse proxy (nginx, Traefik) for authentication,
            rate limiting, and SSL/TLS termination. GreenStack focuses on device configuration
            management, not security infrastructure.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* What Makes It Unique */}
      <DocsSection title="What Makes GreenStack Unique">
        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card className="border-brand-green/20">
            <CardHeader>
              <CardTitle className="text-base">Dual Protocol Support</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="text-sm">
                Unlike most tools that support only one protocol, GreenStack handles both IODD (IO-Link)
                and EDS (EtherNet/IP) files in a single unified platform.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card className="border-brand-green/20">
            <CardHeader>
              <CardTitle className="text-base">Modern UX</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="text-sm">
                Industrial tools don't have to look dated. GreenStack delivers a modern, responsive
                interface with 3D visualizations and smooth animations that rivals consumer applications.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card className="border-brand-green/20">
            <CardHeader>
              <CardTitle className="text-base">Self-Contained</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="text-sm">
                No complex setup or external dependencies. GreenStack runs entirely on your local machine
                with SQLite - perfect for engineers who need quick access to device configurations.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card className="border-brand-green/20">
            <CardHeader>
              <CardTitle className="text-base">Open Source</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="text-sm">
                MIT licensed with clean, well-documented code. Customize it, extend it, integrate it
                with your existing tools. No vendor lock-in, no licensing fees.
              </DocsParagraph>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Learn More">
        <div className="grid grid-cols-1 md:grid-cols-3 gap-3 my-6">
          <DocsLink href="/docs/user-guide/getting-started" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Getting Started</h5>
            <p className="text-sm text-muted-foreground">Quick start guide</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/device-management" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Device Management</h5>
            <p className="text-sm text-muted-foreground">Upload and manage devices</p>
          </DocsLink>

          <DocsLink href="/docs/api/overview" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Reference</h5>
            <p className="text-sm text-muted-foreground">Explore the REST API</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
