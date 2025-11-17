import React from 'react';
import { AlertTriangle, Database, Globe, Server, FileX, Zap } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'troubleshooting/common-issues',
  title: 'Common Issues & Solutions',
  description: 'Solutions to frequently encountered problems when using Greenstack',
  category: 'troubleshooting',
  order: 1,
  keywords: ['troubleshooting', 'issues', 'problems', 'solutions', 'errors', 'fixes'],
  lastUpdated: '2025-01-17',
};

export default function CommonIssues({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Common Issues & Solutions"
        description="Quick solutions to frequently encountered problems"
        icon={<AlertTriangle className="w-12 h-12 text-brand-green" />}
      />

      {/* Backend Issues */}
      <DocsSection title="Backend Issues" icon={<Server />}>
        <DocsParagraph>
          Common problems related to the FastAPI backend server.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                Backend won't start - "Port 8000 already in use"
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Another application is using port 8000.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solution 1:</strong> Find and stop the process using port 8000
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Windows
netstat -ano | findstr :8000
taskkill /PID <process_id> /F

# Linux/Mac
lsof -ti:8000 | xargs kill -9`}
              </DocsCodeBlock>

              <DocsParagraph className="mb-3 mt-4">
                <strong>Solution 2:</strong> Change the port Greenstack uses
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Run on port 8001 instead
uvicorn src.api:app --host 0.0.0.0 --port 8001

# Update frontend .env file
VITE_API_URL=http://localhost:8001`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                "ModuleNotFoundError: No module named 'fastapi'"
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Python dependencies not installed or wrong Python environment active.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solution:</strong> Install dependencies and verify Python version
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Check Python version (must be 3.10+)
python --version

# Install dependencies
pip install -r requirements.txt

# Or install individual package
pip install fastapi uvicorn sqlalchemy

# If using virtual environment, activate it first
# Windows
.venv\\Scripts\\activate
# Linux/Mac
source .venv/bin/activate`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                "Could not import module: ModuleNotFoundError"
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Running backend from wrong directory or PYTHONPATH not set.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solution:</strong> Run from project root with correct path
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Ensure you're in the project root directory
cd /path/to/greenstack

# Run backend (not from src/ directory)
uvicorn src.api:app --host 0.0.0.0 --port 8000

# Or set PYTHONPATH
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
python -m uvicorn src.api:app --host 0.0.0.0 --port 8000`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="warning">WARNING</Badge>
                Slow API response times
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Causes:</strong> Large database, missing indexes, inefficient queries, or debug mode.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Ensure not running with <code>--reload</code> flag in production</li>
                <li>Use <code>--workers 4</code> for multi-process handling</li>
                <li>Enable database query logging to identify slow queries</li>
                <li>Add indexes to frequently queried columns</li>
                <li>Consider switching from SQLite to PostgreSQL for large datasets</li>
              </ul>

              <DocsCodeBlock language="bash">
{`# Production startup (no reload, multiple workers)
uvicorn src.api:app --host 0.0.0.0 --port 8000 --workers 4

# Check slow queries in logs
docker compose logs backend | grep "Slow query"`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Frontend Issues */}
      <DocsSection title="Frontend Issues" icon={<Globe />}>
        <DocsParagraph>
          Common problems related to the React frontend application.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                "Cannot connect to backend" or CORS errors
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Backend not running, wrong API URL, or CORS misconfiguration.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>

              <div className="mb-3">
                <strong className="text-sm">1. Verify backend is running:</strong>
                <DocsCodeBlock language="bash">
{`# Check if backend responds
curl http://localhost:8000/health

# Should return: {"status":"healthy",...}`}
                </DocsCodeBlock>
              </div>

              <div className="mb-3">
                <strong className="text-sm">2. Check frontend API URL configuration:</strong>
                <DocsCodeBlock language="bash">
{`# frontend/.env
VITE_API_URL=http://localhost:8000

# Rebuild frontend after changing .env
npm run build`}
                </DocsCodeBlock>
              </div>

              <div>
                <strong className="text-sm">3. Verify CORS settings in backend:</strong>
                <DocsCodeBlock language="python">
{`# src/api.py
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:5173", "http://localhost"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)`}
                </DocsCodeBlock>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                "npm install" fails or takes forever
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Causes:</strong> Network issues, corrupted cache, or package conflicts.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Clear npm cache
npm cache clean --force

# Delete node_modules and package-lock.json
rm -rf node_modules package-lock.json

# Reinstall
npm install

# If still failing, try different registry
npm install --registry=https://registry.npmjs.org/

# Or use yarn instead
yarn install`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                Frontend build fails with "JavaScript heap out of memory"
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Node.js default memory limit too low for large builds.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solution:</strong> Increase Node.js memory limit
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Windows (PowerShell)
$env:NODE_OPTIONS="--max-old-space-size=4096"
npm run build

# Linux/Mac
NODE_OPTIONS="--max-old-space-size=4096" npm run build

# Or add to package.json scripts
"build": "NODE_OPTIONS='--max-old-space-size=4096' vite build"`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="warning">WARNING</Badge>
                Blank page after deployment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Causes:</strong> Incorrect base URL, JavaScript errors, or missing files.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Check browser console for JavaScript errors (F12)</li>
                <li>Verify all build files were deployed</li>
                <li>Check <code>vite.config.js</code> base path configuration</li>
                <li>Ensure correct MIME types for .js and .css files</li>
                <li>Clear browser cache and try incognito mode</li>
              </ul>

              <DocsCodeBlock language="javascript">
{`// vite.config.js - if deploying to subdirectory
export default defineConfig({
  base: '/greenstack/', // Match your deployment path
  // ...
});`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Database Issues */}
      <DocsSection title="Database Issues" icon={<Database />}>
        <DocsParagraph>
          Common database-related problems and solutions.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                "Database is locked" (SQLite)
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Multiple processes trying to write to SQLite simultaneously.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Use PostgreSQL for production instead of SQLite</li>
                <li>Reduce backend workers to 1 if using SQLite</li>
                <li>Ensure only one backend instance is running</li>
                <li>Check for stale database locks (restart backend)</li>
              </ul>

              <DocsCodeBlock language="bash">
{`# For development with SQLite, use single worker
uvicorn src.api:app --host 0.0.0.0 --port 8000 --workers 1

# For production, switch to PostgreSQL
DATABASE_URL=postgresql://user:pass@localhost:5432/greenstack`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                Alembic migration errors
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Database schema out of sync with migrations.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Check current migration version
alembic current

# Upgrade to latest migration
alembic upgrade head

# If migrations are corrupted, reset (WARNING: deletes data)
rm greenstack.db
alembic upgrade head

# Or manually sync specific migration
alembic upgrade <revision_id>`}
              </DocsCodeBlock>

              <DocsCallout type="warning" title="Data Loss Warning">
                <DocsParagraph>
                  Deleting the database file will remove all uploaded IODDs and data.
                  Always backup your database before resetting migrations.
                </DocsParagraph>
              </DocsCallout>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="warning">WARNING</Badge>
                Database file growing too large
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Causes:</strong> Many large IODDs, no cleanup, or SQLite fragmentation.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Vacuum SQLite database to reclaim space
sqlite3 greenstack.db "VACUUM;"

# Check database size
ls -lh greenstack.db

# For large deployments, migrate to PostgreSQL
# PostgreSQL handles large datasets better than SQLite`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* File Upload Issues */}
      <DocsSection title="File Upload Issues" icon={<FileX />}>
        <DocsParagraph>
          Problems related to IODD file uploads.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                "Invalid XML" or parsing errors
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Causes:</strong> Malformed XML, wrong file type, or unsupported IODD version.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Validate XML syntax using an XML validator</li>
                <li>Ensure file is actually an IODD/EDS file, not plain XML</li>
                <li>Check file encoding is UTF-8</li>
                <li>Try opening file in text editor to check for corruption</li>
                <li>Verify IODD version is supported (check backend logs)</li>
              </ul>

              <DocsCodeBlock language="bash">
{`# Validate XML syntax
xmllint --noout device.xml

# Check file encoding
file -i device.xml

# View backend parsing errors
docker compose logs backend | grep "parse error"`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="destructive">ERROR</Badge>
                Upload fails with "File too large"
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> File exceeds maximum upload size limit.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solution:</strong> Increase upload size limit
              </DocsParagraph>
              <DocsCodeBlock language="python">
{`# src/api.py - Increase max upload size
from fastapi import FastAPI, UploadFile

app = FastAPI()

# Set max upload size (default: 10MB)
app.add_middleware(
    ...,
    max_upload_size=20_000_000  # 20MB
)`}
              </DocsCodeBlock>

              <DocsCodeBlock language="bash">
{`# Or set via environment variable
MAX_UPLOAD_SIZE=20971520  # 20MB in bytes`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Badge variant="warning">WARNING</Badge>
                Duplicate device error
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                <strong>Cause:</strong> Device with same Vendor ID and Device ID already exists.
              </DocsParagraph>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong>
              </DocsParagraph>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground">
                <li>Delete the existing device first (if you want to replace it)</li>
                <li>Use the API to update the existing device instead</li>
                <li>Check if you're uploading the same file twice</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Performance Issues */}
      <DocsSection title="Performance Issues" icon={<Zap />}>
        <DocsParagraph>
          Common performance problems and optimization tips.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Slow search results</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Database lacks indexes on search columns</li>
                <li>Too many results returned (use pagination)</li>
                <li>SQLite performance limits (switch to PostgreSQL)</li>
                <li>Full-text search on large text fields</li>
              </ul>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong> Add database indexes, implement pagination, use PostgreSQL.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">High memory usage</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Loading entire large files into memory</li>
                <li>No connection pooling for database</li>
                <li>Caching too much data</li>
                <li>Memory leaks in long-running processes</li>
              </ul>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong> Stream large files, configure connection pools, restart periodically.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Frontend loads slowly</CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="list-disc ml-6 space-y-2 text-sm text-muted-foreground mb-3">
                <li>Large bundle size (code splitting needed)</li>
                <li>No caching headers configured</li>
                <li>Images not optimized</li>
                <li>Too many API calls on page load</li>
              </ul>

              <DocsParagraph className="mb-3">
                <strong>Solutions:</strong> Use production build, enable gzip compression, lazy load components.
              </DocsParagraph>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Still Need Help */}
      <DocsSection title="Still Having Issues?">
        <DocsParagraph>
          If your issue isn't listed here, try these resources:
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <DocsLink href="/docs/troubleshooting/debugging" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Debugging Guide</h5>
            <p className="text-sm text-muted-foreground">Learn how to debug and diagnose issues</p>
          </DocsLink>

          <DocsLink href="/docs/troubleshooting/faq" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">FAQ</h5>
            <p className="text-sm text-muted-foreground">Frequently asked questions</p>
          </DocsLink>

          <DocsLink href="https://github.com/ME-Catalyst/greenstack/issues" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">GitHub Issues</h5>
            <p className="text-sm text-muted-foreground">Report a bug or request help</p>
          </DocsLink>

          <DocsLink href="https://github.com/ME-Catalyst/greenstack/discussions" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">GitHub Discussions</h5>
            <p className="text-sm text-muted-foreground">Ask the community for help</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
