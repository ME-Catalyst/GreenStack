import React from 'react';
import { Code, Server, Database, Zap, Shield, Book } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsTabs, { DocsTab } from '../../../components/docs/DocsTabs';

export const metadata = {
  id: 'api/overview',
  title: 'API Overview',
  description: 'Complete REST API reference for Greenstack - 142 endpoints across 8 categories',
  category: 'api',
  order: 1,
  keywords: ['api', 'rest', 'endpoints', 'reference', 'http', 'fastapi'],
  lastUpdated: '2025-01-17',
};

export default function ApiOverview() {
  return (
    <DocsPage>
      <DocsHero
        title="API Overview"
        description="Complete REST API reference for Greenstack - 142 endpoints across 8 categories"
        icon={<Code className="w-12 h-12 text-brand-green" />}
      />

      <DocsSection title="Introduction">
        <DocsParagraph>
          Greenstack provides a comprehensive REST API built with FastAPI. The API enables programmatic access
          to all platform features including device management, configuration export, service control, and more.
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 my-6">
          <div className="border border-border rounded-lg p-4">
            <Server className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">142 Endpoints</h4>
            <p className="text-sm text-muted-foreground">Comprehensive API coverage across all features</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Zap className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">FastAPI Framework</h4>
            <p className="text-sm text-muted-foreground">High-performance async Python framework</p>
          </div>

          <div className="border border-border rounded-lg p-4">
            <Book className="w-8 h-8 text-brand-green mb-3" />
            <h4 className="font-semibold text-foreground mb-1">OpenAPI/Swagger</h4>
            <p className="text-sm text-muted-foreground">Auto-generated interactive documentation</p>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Base URL">
        <DocsParagraph>
          All API endpoints are relative to the base URL of your Greenstack installation:
        </DocsParagraph>

        <DocsCodeBlock language="text" copy>
{`# Development
http://localhost:8000

# Production (example)
https://greenstack.yourdomain.com`}
        </DocsCodeBlock>

        <DocsCallout type="info" title="Interactive Documentation">
          <DocsParagraph>
            Visit <code className="text-xs bg-surface px-1 py-0.5 rounded">/docs</code> on your Greenstack instance
            for interactive Swagger UI documentation, or <code className="text-xs bg-surface px-1 py-0.5 rounded">/redoc</code> for
            ReDoc-style documentation.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      <DocsSection title="API Categories">
        <DocsParagraph>
          The Greenstack API is organized into 8 main categories:
        </DocsParagraph>

        <div className="space-y-4 my-6">
          {/* EDS Files */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">EDS Files</h4>
                <code className="text-xs text-muted-foreground">/api/eds</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">18 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Manage EDS (Electronic Data Sheet) files for EtherNet/IP devices including upload, parsing,
              package management, assemblies, ports, and modules.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Upload</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Parse</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Diagnostics</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Export</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Revisions</span>
            </div>
          </div>

          {/* Admin Console */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Admin Console</h4>
                <code className="text-xs text-muted-foreground">/api/admin</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">14 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              System administration, monitoring, database management, backups, diagnostics, and bulk data operations.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Statistics</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Health</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Backup</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Vacuum</span>
            </div>
          </div>

          {/* Tickets */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Tickets</h4>
                <code className="text-xs text-muted-foreground">/api/tickets</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">13 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Complete ticket/bug tracking system with comments, attachments, filtering, and CSV export.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">CRUD</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Comments</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Attachments</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Export</span>
            </div>
          </div>

          {/* MQTT */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">MQTT</h4>
                <code className="text-xs text-muted-foreground">/</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">10 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              MQTT broker management including publish/subscribe, connection control, and WebSocket streaming.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Publish</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Subscribe</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Status</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">WebSocket</span>
            </div>
          </div>

          {/* Theme Management */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Theme Management</h4>
                <code className="text-xs text-muted-foreground">/api/themes</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">7 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              User theme customization with presets, custom themes, and persistence.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Presets</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Custom</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Activate</span>
            </div>
          </div>

          {/* Services */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Services</h4>
                <code className="text-xs text-muted-foreground">/api/services</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">7 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Manage application services (MQTT, InfluxDB, Node-RED, Grafana) with lifecycle control and health monitoring.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Start/Stop</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Config</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Health</span>
            </div>
          </div>

          {/* Configuration Export */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Configuration Export</h4>
                <code className="text-xs text-muted-foreground">/api/config-export</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">5 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Export device configurations in JSON and CSV formats with batch export support.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">JSON</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">CSV</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Batch</span>
            </div>
          </div>

          {/* Search */}
          <div className="border border-border rounded-lg p-4">
            <div className="flex items-start justify-between mb-2">
              <div>
                <h4 className="font-semibold text-foreground mb-1">Search</h4>
                <code className="text-xs text-muted-foreground">/api/search</code>
              </div>
              <span className="text-xs px-2 py-1 bg-brand-green/10 text-brand-green rounded">2 endpoints</span>
            </div>
            <p className="text-sm text-muted-foreground mb-2">
              Global search across all device data with autocomplete suggestions.
            </p>
            <div className="flex flex-wrap gap-1">
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Search</span>
              <span className="text-xs px-2 py-0.5 bg-surface border border-border rounded">Suggestions</span>
            </div>
          </div>
        </div>
      </DocsSection>

      <DocsSection title="Quick Start">
        <DocsParagraph>
          Here's a quick example of using the Greenstack API:
        </DocsParagraph>

        <DocsTabs>
          <DocsTab label="cURL">
            <DocsCodeBlock language="bash" copy>
{`# Get all EDS files
curl http://localhost:8000/api/eds

# Upload an EDS file
curl -X POST "http://localhost:8000/api/eds/upload" \\
  -H "Content-Type: multipart/form-data" \\
  -F "file=@device.eds"

# Get device details
curl http://localhost:8000/api/eds/1

# Export configuration
curl http://localhost:8000/api/config-export/eds/1/json -o config.json`}
            </DocsCodeBlock>
          </DocsTab>

          <DocsTab label="Python">
            <DocsCodeBlock language="python" copy>
{`import requests

# Base URL
base_url = "http://localhost:8000"

# Get all EDS files
response = requests.get(f"{base_url}/api/eds")
devices = response.json()

# Upload an EDS file
with open("device.eds", "rb") as f:
    response = requests.post(
        f"{base_url}/api/eds/upload",
        files={"file": f}
    )
    result = response.json()
    print(f"Uploaded device: {result['product_name']}")

# Export configuration
response = requests.get(f"{base_url}/api/config-export/eds/1/json")
config = response.json()
with open("config.json", "w") as f:
    json.dump(config, f, indent=2)`}
            </DocsCodeBlock>
          </DocsTab>

          <DocsTab label="JavaScript">
            <DocsCodeBlock language="javascript" copy>
{`// Base URL
const baseUrl = "http://localhost:8000";

// Get all EDS files
const devices = await fetch(\`\${baseUrl}/api/eds\`)
  .then(res => res.json());

// Upload an EDS file
const formData = new FormData();
formData.append("file", fileInput.files[0]);

const result = await fetch(\`\${baseUrl}/api/eds/upload\`, {
  method: "POST",
  body: formData
}).then(res => res.json());

console.log(\`Uploaded: \${result.product_name}\`);

// Export configuration
const config = await fetch(\`\${baseUrl}/api/config-export/eds/1/json\`)
  .then(res => res.json());`}
            </DocsCodeBlock>
          </DocsTab>
        </DocsTabs>
      </DocsSection>

      <DocsSection title="Response Format">
        <DocsParagraph>
          All API responses follow consistent JSON formatting:
        </DocsParagraph>

        <DocsCodeBlock language="json" copy>
{`// Success response (200-299)
{
  "data": { /* response data */ },
  "message": "Operation successful"
}

// Error response (400-599)
{
  "detail": "Error description",
  "status_code": 400
}`}
        </DocsCodeBlock>
      </DocsSection>

      <DocsSection title="HTTP Status Codes">
        <DocsParagraph>
          The API uses standard HTTP status codes:
        </DocsParagraph>

        <div className="overflow-x-auto my-4">
          <table className="w-full text-sm border-collapse">
            <thead>
              <tr className="border-b border-border">
                <th className="text-left py-2 px-3 font-semibold text-foreground">Code</th>
                <th className="text-left py-2 px-3 font-semibold text-foreground">Status</th>
                <th className="text-left py-2 px-3 font-semibold text-foreground">Description</th>
              </tr>
            </thead>
            <tbody>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-brand-green">200</code></td>
                <td className="py-2 px-3">OK</td>
                <td className="py-2 px-3 text-muted-foreground">Request successful</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-brand-green">201</code></td>
                <td className="py-2 px-3">Created</td>
                <td className="py-2 px-3 text-muted-foreground">Resource created successfully</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-brand-green">204</code></td>
                <td className="py-2 px-3">No Content</td>
                <td className="py-2 px-3 text-muted-foreground">Request successful, no content returned</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-yellow-500">400</code></td>
                <td className="py-2 px-3">Bad Request</td>
                <td className="py-2 px-3 text-muted-foreground">Invalid request parameters</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-yellow-500">404</code></td>
                <td className="py-2 px-3">Not Found</td>
                <td className="py-2 px-3 text-muted-foreground">Resource not found</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-yellow-500">409</code></td>
                <td className="py-2 px-3">Conflict</td>
                <td className="py-2 px-3 text-muted-foreground">Resource already exists</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-red-500">500</code></td>
                <td className="py-2 px-3">Internal Server Error</td>
                <td className="py-2 px-3 text-muted-foreground">Server error occurred</td>
              </tr>
              <tr className="border-b border-border">
                <td className="py-2 px-3"><code className="text-red-500">503</code></td>
                <td className="py-2 px-3">Service Unavailable</td>
                <td className="py-2 px-3 text-muted-foreground">Service temporarily unavailable</td>
              </tr>
            </tbody>
          </table>
        </div>
      </DocsSection>

      <DocsSection title="Rate Limiting">
        <DocsCallout type="info" title="No Rate Limits">
          <DocsParagraph>
            The Greenstack API currently does not enforce rate limiting. However, it's recommended to
            implement reasonable request throttling in your applications to avoid overloading the server.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      <DocsSection title="Next Steps">
        <DocsParagraph>
          Explore detailed endpoint documentation for each API category:
        </DocsParagraph>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/api/eds-reference" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">EDS API Reference</h4>
            <p className="text-sm text-muted-foreground">18 endpoints for EDS file management</p>
          </DocsLink>

          <DocsLink href="/docs/api/admin-reference" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Admin API Reference</h4>
            <p className="text-sm text-muted-foreground">14 endpoints for system administration</p>
          </DocsLink>

          <DocsLink href="/docs/api/tickets-reference" external={false} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Tickets API Reference</h4>
            <p className="text-sm text-muted-foreground">13 endpoints for ticket management</p>
          </DocsLink>

          <DocsLink href="http://localhost:8000/docs" external={true} className="block border border-border rounded-lg p-3 hover:border-brand-green transition-colors">
            <h4 className="font-semibold text-foreground mb-1">Interactive Swagger UI</h4>
            <p className="text-sm text-muted-foreground">Try the API in your browser</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
