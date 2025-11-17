import React from 'react';
import { Bug, Terminal, Eye, FileText, Activity, Zap } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsMermaid from '../../../components/docs/DocsMermaid';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'troubleshooting/debugging',
  title: 'Debugging Guide',
  description: 'Learn how to debug and troubleshoot issues in Greenstack using logs, tools, and best practices',
  category: 'troubleshooting',
  order: 2,
  keywords: ['debugging', 'debug', 'troubleshoot', 'logs', 'errors', 'diagnostics'],
  lastUpdated: '2025-01-17',
};

export default function DebuggingGuide({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Debugging Guide"
        description="Comprehensive guide to debugging and troubleshooting Greenstack"
        icon={<Bug className="w-12 h-12 text-brand-green" />}
      />

      {/* Debugging Workflow */}
      <DocsSection title="Debugging Workflow" icon={<Activity />}>
        <DocsParagraph>
          Follow this systematic approach when debugging issues in Greenstack.
        </DocsParagraph>

        <DocsMermaid chart={`
graph TB
    Start["🐛 Issue Encountered"] --> Identify["1️⃣ Identify Component"]
    Identify --> Frontend{"Frontend<br/>Issue?"}
    Identify --> Backend{"Backend<br/>Issue?"}
    Identify --> Database{"Database<br/>Issue?"}

    Frontend --> BrowserConsole["Check Browser Console<br/>F12 → Console Tab"]
    Frontend --> NetworkTab["Check Network Tab<br/>F12 → Network"]
    BrowserConsole --> FrontendLogs["Review React Logs"]
    NetworkTab --> APIResponse["Check API Responses"]

    Backend --> BackendLogs["View Backend Logs<br/>docker compose logs backend"]
    Backend --> APITest["Test API Directly<br/>curl or Postman"]
    BackendLogs --> ErrorStack["Analyze Stack Trace"]
    APITest --> ResponseCode["Check Status Code"]

    Database --> DBLogs["Check Database Logs"]
    Database --> DBQuery["Run Direct Queries<br/>psql or sqlite3"]
    DBLogs --> DBConnection["Test Connection"]
    DBQuery --> DataIntegrity["Verify Data Integrity"]

    FrontendLogs --> Solution{"Solution<br/>Found?"}
    APIResponse --> Solution
    ErrorStack --> Solution
    ResponseCode --> Solution
    DBConnection --> Solution
    DataIntegrity --> Solution

    Solution -->|Yes| Implement["🔧 Implement Fix"]
    Solution -->|No| DeepDive["🔍 Deep Dive"]

    DeepDive --> EnableDebug["Enable Debug Mode"]
    DeepDive --> AddLogging["Add Logging Statements"]
    DeepDive --> UseDebugger["Use Debugger (pdb/DevTools)"]

    EnableDebug --> Solution
    AddLogging --> Solution
    UseDebugger --> Solution

    Implement --> Test["✅ Test Fix"]
    Test --> Verify{"Issue<br/>Resolved?"}
    Verify -->|Yes| Document["📝 Document Solution"]
    Verify -->|No| DeepDive

    Document --> Done["🎉 Done!"]

    style Start fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Frontend fill:#1a1f3a,stroke:#51cf66,stroke-width:2px,color:#fff
    style Backend fill:#1a1f3a,stroke:#51cf66,stroke-width:2px,color:#fff
    style Database fill:#1a1f3a,stroke:#51cf66,stroke-width:2px,color:#fff
    style Solution fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Verify fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
    style Done fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
`} className="my-6" />
      </DocsSection>

      {/* Backend Debugging */}
      <DocsSection title="Backend Debugging" icon={<Terminal />}>
        <DocsParagraph>
          Tools and techniques for debugging the FastAPI backend.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Viewing Backend Logs</CardTitle>
              <CardDescription>Access logs to identify errors and trace requests</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Docker Compose logs (real-time)
docker compose logs -f backend

# Last 100 lines
docker compose logs --tail=100 backend

# Filter by error level
docker compose logs backend | grep ERROR

# Save logs to file
docker compose logs backend > backend-logs.txt

# Non-Docker setup (if running uvicorn directly)
# Logs will appear in terminal where uvicorn is running`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Enable Debug Mode</CardTitle>
              <CardDescription>Get more detailed error messages and stack traces</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Set environment variable
export LOG_LEVEL=debug

# Or in .env file
LOG_LEVEL=debug
ENVIRONMENT=development

# Restart backend to apply changes
docker compose restart backend`}
              </DocsCodeBlock>

              <DocsCallout type="warning" title="Production Warning">
                <DocsParagraph>
                  Never enable debug mode in production. It exposes sensitive information
                  and reduces performance. Always use <code>LOG_LEVEL=info</code> or
                  <code>LOG_LEVEL=warning</code> in production.
                </DocsParagraph>
              </DocsCallout>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Using Python Debugger (pdb)</CardTitle>
              <CardDescription>Interactive debugging with breakpoints</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Add breakpoints in your Python code:
              </DocsParagraph>
              <DocsCodeBlock language="python">
{`# Add this line where you want to pause execution
import pdb; pdb.set_trace()

# Example: Debug IODD parsing
def parse_iodd(content: str):
    import pdb; pdb.set_trace()  # Execution pauses here
    result = parser.parse(content)
    return result

# Common pdb commands:
# n - next line
# s - step into function
# c - continue execution
# p variable_name - print variable
# l - list code around current line
# q - quit debugger`}
              </DocsCodeBlock>

              <DocsParagraph className="mb-3 mt-4">
                For Docker environments, attach to the running container:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Attach to container with interactive terminal
docker attach greenstack-backend

# Or use docker exec for a new shell
docker exec -it greenstack-backend bash`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Testing API Endpoints</CardTitle>
              <CardDescription>Isolate backend issues by testing APIs directly</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Test with curl
curl -X GET http://localhost:8000/health
curl -X GET http://localhost:8000/api/iodds

# Test file upload
curl -X POST http://localhost:8000/api/iodds/upload \\
  -F "file=@device.xml" \\
  -v  # Verbose output shows headers and status

# Test with different methods
curl -X DELETE http://localhost:8000/api/iodds/123

# View response headers
curl -I http://localhost:8000/api/iodds`}
              </DocsCodeBlock>

              <DocsParagraph className="mb-3 mt-4">
                Or use the interactive API documentation:
              </DocsParagraph>
              <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                <li>Swagger UI: <code>http://localhost:8000/docs</code></li>
                <li>ReDoc: <code>http://localhost:8000/redoc</code></li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Common Backend Issues</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <Badge variant="outline" className="mb-2">500 Internal Server Error</Badge>
                  <p className="text-sm text-muted-foreground">
                    Check backend logs for Python exceptions and stack traces.
                  </p>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">422 Unprocessable Entity</Badge>
                  <p className="text-sm text-muted-foreground">
                    Request validation failed. Check request body matches expected schema.
                  </p>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">404 Not Found</Badge>
                  <p className="text-sm text-muted-foreground">
                    Endpoint doesn't exist or resource not in database. Verify URL and IDs.
                  </p>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">503 Service Unavailable</Badge>
                  <p className="text-sm text-muted-foreground">
                    Backend can't reach database or dependency. Check health endpoint.
                  </p>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Frontend Debugging */}
      <DocsSection title="Frontend Debugging" icon={<Eye />}>
        <DocsParagraph>
          Tools and techniques for debugging the React frontend.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Browser Developer Tools</CardTitle>
              <CardDescription>Essential tools built into your browser</CardDescription>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-foreground mb-2">Console Tab (F12 → Console)</h4>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>View JavaScript errors and warnings</li>
                    <li>See console.log() output</li>
                    <li>Execute JavaScript code interactively</li>
                    <li>Filter messages by level (errors, warnings, info)</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-foreground mb-2">Network Tab (F12 → Network)</h4>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Monitor API requests and responses</li>
                    <li>Check HTTP status codes</li>
                    <li>Inspect request/response headers and body</li>
                    <li>Measure request timing and performance</li>
                  </ul>
                </div>

                <div>
                  <h4 className="font-semibold text-foreground mb-2">React DevTools</h4>
                  <DocsParagraph>
                    Install the <DocsLink href="https://react.dev/learn/react-developer-tools" external>React Developer Tools</DocsLink> browser extension.
                  </DocsParagraph>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground mt-2">
                    <li>Inspect React component tree</li>
                    <li>View and edit component props and state</li>
                    <li>Track component re-renders</li>
                    <li>Profile performance issues</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Adding Debug Logging</CardTitle>
              <CardDescription>Insert console.log statements strategically</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="javascript">
{`// Log function entry and parameters
const uploadIODD = async (file) => {
  console.log('[uploadIODD] Starting upload', { file });

  try {
    const result = await api.uploadFile(file);
    console.log('[uploadIODD] Upload successful', { result });
    return result;
  } catch (error) {
    console.error('[uploadIODD] Upload failed', { error });
    throw error;
  }
};

// Log component rendering
const DeviceList = ({ devices }) => {
  console.log('[DeviceList] Rendering with devices:', devices);

  useEffect(() => {
    console.log('[DeviceList] Component mounted');
    return () => console.log('[DeviceList] Component unmounted');
  }, []);

  // Component JSX...
};

// Log state changes
const [count, setCount] = useState(0);
useEffect(() => {
  console.log('[State Change] count:', count);
}, [count]);`}
              </DocsCodeBlock>

              <DocsCallout type="info" title="Production Best Practice">
                <DocsParagraph>
                  Remove or disable console.log statements in production builds for better
                  performance. Use a logging library with environment-based log levels.
                </DocsParagraph>
              </DocsCallout>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Debugging API Calls</CardTitle>
              <CardDescription>Trace API requests and responses</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="javascript">
{`// Add request/response interceptors
import axios from 'axios';

axios.interceptors.request.use(
  (config) => {
    console.log('[API Request]', {
      url: config.url,
      method: config.method,
      data: config.data,
    });
    return config;
  },
  (error) => {
    console.error('[API Request Error]', error);
    return Promise.reject(error);
  }
);

axios.interceptors.response.use(
  (response) => {
    console.log('[API Response]', {
      url: response.config.url,
      status: response.status,
      data: response.data,
    });
    return response;
  },
  (error) => {
    console.error('[API Response Error]', {
      url: error.config?.url,
      status: error.response?.status,
      message: error.message,
      data: error.response?.data,
    });
    return Promise.reject(error);
  }
);`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Common Frontend Issues</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <Badge variant="outline" className="mb-2">White Screen / Blank Page</Badge>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Check Console for JavaScript errors</li>
                    <li>Verify build files are present</li>
                    <li>Check browser compatibility</li>
                    <li>Clear cache and try incognito mode</li>
                  </ul>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">Component Not Rendering</Badge>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Check component props are correct</li>
                    <li>Verify conditional rendering logic</li>
                    <li>Inspect with React DevTools</li>
                    <li>Check for null/undefined data</li>
                  </ul>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">State Not Updating</Badge>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Ensure state updates are immutable</li>
                    <li>Check useEffect dependencies</li>
                    <li>Verify setState is called correctly</li>
                    <li>Look for stale closures in callbacks</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Database Debugging */}
      <DocsSection title="Database Debugging" icon={<FileText />}>
        <DocsParagraph>
          Debugging database connections, queries, and data issues.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Connecting to Database</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-4">
                <div>
                  <h4 className="font-semibold text-foreground mb-2">SQLite</h4>
                  <DocsCodeBlock language="bash">
{`# Open database shell
sqlite3 greenstack.db

# List tables
.tables

# View table schema
.schema devices

# Query data
SELECT * FROM devices LIMIT 10;

# Check database integrity
PRAGMA integrity_check;

# Exit
.quit`}
                  </DocsCodeBlock>
                </div>

                <div>
                  <h4 className="font-semibold text-foreground mb-2">PostgreSQL</h4>
                  <DocsCodeBlock language="bash">
{`# Connect via Docker
docker compose exec db psql -U greenstack -d greenstack

# List tables
\\dt

# View table schema
\\d devices

# Query data
SELECT * FROM devices LIMIT 10;

# Check connections
SELECT * FROM pg_stat_activity;

# Exit
\\q`}
                  </DocsCodeBlock>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Query Performance Analysis</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="sql">
{`-- PostgreSQL: Explain query plan
EXPLAIN ANALYZE
SELECT * FROM devices
WHERE product_name LIKE '%sensor%';

-- Check slow queries
SELECT query, mean_exec_time
FROM pg_stat_statements
ORDER BY mean_exec_time DESC
LIMIT 10;

-- SQLite: Query plan
EXPLAIN QUERY PLAN
SELECT * FROM devices
WHERE product_name LIKE '%sensor%';`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Common Database Issues</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-3">
                <div>
                  <Badge variant="outline" className="mb-2">Connection Refused</Badge>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Database service not running</li>
                    <li>Wrong connection credentials</li>
                    <li>Network/firewall blocking connection</li>
                    <li>Wrong host/port in DATABASE_URL</li>
                  </ul>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">Slow Queries</Badge>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Missing indexes on queried columns</li>
                    <li>Large dataset without pagination</li>
                    <li>Complex joins or subqueries</li>
                    <li>Database needs vacuum/optimization</li>
                  </ul>
                </div>
                <div>
                  <Badge variant="outline" className="mb-2">Data Corruption</Badge>
                  <ul className="list-disc ml-6 space-y-1 text-sm text-muted-foreground">
                    <li>Improper shutdown during write</li>
                    <li>Disk errors or out of space</li>
                    <li>Concurrent writes to SQLite</li>
                    <li>Alembic migration conflicts</li>
                  </ul>
                </div>
              </div>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Debugging Tools */}
      <DocsSection title="Debugging Tools" icon={<Zap />}>
        <DocsParagraph>
          Additional tools and resources for debugging Greenstack.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Postman / Insomnia</CardTitle>
              <CardDescription>API testing tools</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Test API endpoints with custom headers, body, and authentication.
                Save requests for reuse and team sharing.
              </p>
              <DocsLink href="https://www.postman.com/" external>
                Get Postman →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Docker Desktop</CardTitle>
              <CardDescription>Container management GUI</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                View container logs, stats, and environment variables through a GUI.
                Easier than command-line for beginners.
              </p>
              <DocsLink href="https://www.docker.com/products/docker-desktop/" external>
                Get Docker Desktop →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">VS Code Debugger</CardTitle>
              <CardDescription>Integrated debugging</CardDescription>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground mb-3">
                Set breakpoints, inspect variables, and step through code directly
                in VS Code for both Python and JavaScript.
              </p>
              <DocsLink href="https://code.visualstudio.com/docs/editor/debugging" external>
                Learn More →
              </DocsLink>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Browser Extensions</CardTitle>
              <CardDescription>Development helpers</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• React Developer Tools</li>
                <li>• Redux DevTools (if using Redux)</li>
                <li>• JSON Viewer</li>
                <li>• Web Developer Toolbar</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Best Practices */}
      <DocsSection title="Debugging Best Practices">
        <div className="space-y-4 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">1. Reproduce the Issue</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Before debugging, ensure you can consistently reproduce the issue.
                Document the exact steps to trigger the problem.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">2. Isolate the Problem</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Narrow down where the issue occurs. Is it frontend, backend, or database?
                Test components individually to isolate the problematic code.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">3. Check Logs First</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Always check logs before adding more debug code. Error messages and
                stack traces often reveal the root cause immediately.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">4. Use Version Control</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Commit working code before debugging. This lets you easily revert
                debug changes and compare working vs broken code.
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">5. Document Your Findings</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Keep notes on what you tried and what worked. This helps future
                debugging and can be shared with the community.
              </p>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/troubleshooting/common-issues" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Common Issues</h5>
            <p className="text-sm text-muted-foreground">Solutions to frequent problems</p>
          </DocsLink>

          <DocsLink href="/docs/troubleshooting/faq" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">FAQ</h5>
            <p className="text-sm text-muted-foreground">Frequently asked questions</p>
          </DocsLink>

          <DocsLink href="/docs/deployment/monitoring" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Monitoring & Logging</h5>
            <p className="text-sm text-muted-foreground">Production monitoring setup</p>
          </DocsLink>

          <DocsLink href="/docs/developer/testing" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Testing Guide</h5>
            <p className="text-sm text-muted-foreground">Write tests to catch bugs early</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
