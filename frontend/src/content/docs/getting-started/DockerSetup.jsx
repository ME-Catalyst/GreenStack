import React from 'react';
import { Package, Play, Settings, Server, Database, CheckCircle, AlertCircle } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsList, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsTabs from '../../../components/docs/DocsTabs';
import DocsSteps from '../../../components/docs/DocsSteps';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'getting-started/docker',
  title: 'Docker Setup',
  description: 'Deploy Greenstack using Docker and Docker Compose for development and production',
  category: 'getting-started',
  order: 4,
  keywords: ['docker', 'container', 'docker-compose', 'deployment', 'containerization'],
  lastUpdated: '2025-01-17',
};

export default function DockerSetup({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Docker Setup"
        description="Deploy Greenstack with Docker for consistent, portable, and production-ready deployments"
        icon={<Package className="w-12 h-12 text-brand-green" />}
      />

      {/* Why Docker */}
      <DocsSection title="Why Use Docker?" icon={<Server />}>
        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-brand-green" />
                Consistency
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph>
                Same environment across development, testing, and production. No more "works on my machine" issues.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-brand-green" />
                Isolation
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph>
                All dependencies packaged together. No conflicts with system packages or other applications.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-brand-green" />
                Easy Deployment
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph>
                Single command to start all services. Perfect for production deployments and scaling.
              </DocsParagraph>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="flex items-center gap-2">
                <CheckCircle className="w-5 h-5 text-brand-green" />
                Reproducibility
              </CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph>
                Every deployment is identical. Easy rollbacks and version management.
              </DocsParagraph>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Prerequisites */}
      <DocsSection title="Prerequisites" icon={<Package />}>
        <DocsParagraph>
          You'll need Docker and Docker Compose installed on your system:
        </DocsParagraph>

        <div className="my-6">
          <Card>
            <CardHeader>
              <CardTitle>Docker Desktop (Recommended)</CardTitle>
              <CardDescription>Includes both Docker Engine and Docker Compose</CardDescription>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-foreground">
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span><strong>Windows/Mac:</strong> <DocsLink href="https://www.docker.com/products/docker-desktop/" external>Docker Desktop</DocsLink></span>
                </li>
                <li className="flex items-center gap-2">
                  <CheckCircle className="w-4 h-4 text-brand-green flex-shrink-0" />
                  <span><strong>Linux:</strong> <DocsLink href="https://docs.docker.com/engine/install/" external>Docker Engine</DocsLink> + <DocsLink href="https://docs.docker.com/compose/install/" external>Docker Compose</DocsLink></span>
                </li>
              </ul>

              <DocsParagraph className="mt-4">
                Verify installation:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`docker --version
docker-compose --version`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Quick Start */}
      <DocsSection title="Quick Start" icon={<Play />}>
        <DocsParagraph>
          Get Greenstack running with Docker in just a few commands:
        </DocsParagraph>

        <DocsTabs
          tabs={[
            {
              id: 'docker-hub',
              label: 'Docker Hub (Production)',
              icon: <Package className="w-4 h-4" />,
              content: (
                <div>
                  <DocsParagraph>
                    Pull the official Greenstack image from Docker Hub and run it:
                  </DocsParagraph>
                  <DocsCodeBlock language="bash">
{`# Pull the latest image
docker pull ghcr.io/me-catalyst/greenstack:latest

# Run the container
docker run -d \\
  --name greenstack \\
  -p 8000:8000 \\
  -v greenstack-data:/data \\
  ghcr.io/me-catalyst/greenstack:latest

# Access the application
open http://localhost:8000`}
                  </DocsCodeBlock>
                  <DocsCallout type="success" title="Production Ready">
                    <DocsParagraph>
                      This image is optimized for production with pre-built frontend assets.
                    </DocsParagraph>
                  </DocsCallout>
                </div>
              )
            },
            {
              id: 'docker-compose',
              label: 'Docker Compose (Full Stack)',
              icon: <Server className="w-4 h-4" />,
              content: (
                <div>
                  <DocsParagraph>
                    Use Docker Compose to run the full stack with all services:
                  </DocsParagraph>
                  <DocsCodeBlock language="bash">
{`# Clone the repository
git clone https://github.com/ME-Catalyst/greenstack.git
cd greenstack

# Start all services
docker-compose up -d

# View logs
docker-compose logs -f

# Stop all services
docker-compose down`}
                  </DocsCodeBlock>
                  <DocsParagraph className="mt-4">
                    This starts:
                  </DocsParagraph>
                  <ul className="list-disc list-inside space-y-1 text-foreground ml-4">
                    <li>Greenstack API (port 8000)</li>
                    <li>Frontend dev server (port 5173)</li>
                    <li>PostgreSQL database (optional)</li>
                  </ul>
                </div>
              )
            }
          ]}
        />
      </DocsSection>

      {/* Docker Compose Configuration */}
      <DocsSection title="Docker Compose Configuration" icon={<Settings />}>
        <DocsParagraph>
          Example <code>docker-compose.yml</code> for Greenstack:
        </DocsParagraph>

        <DocsCodeBlock language="yaml">
{`version: '3.8'

services:
  # Greenstack API
  api:
    image: ghcr.io/me-catalyst/greenstack:latest
    container_name: greenstack-api
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite:///data/greenstack.db
      - CORS_ORIGINS=http://localhost:5173,http://localhost:8000
      - LOG_LEVEL=INFO
    volumes:
      - greenstack-data:/data
    restart: unless-stopped
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
      interval: 30s
      timeout: 10s
      retries: 3

  # Frontend (development)
  frontend:
    image: node:18-alpine
    container_name: greenstack-frontend
    working_dir: /app
    ports:
      - "5173:5173"
    environment:
      - VITE_API_URL=http://localhost:8000
    volumes:
      - ./frontend:/app
      - /app/node_modules
    command: sh -c "npm install && npm run dev"
    depends_on:
      - api

  # PostgreSQL (optional - for production)
  # db:
  #   image: postgres:15-alpine
  #   container_name: greenstack-db
  #   environment:
  #     - POSTGRES_DB=greenstack
  #     - POSTGRES_USER=greenstack
  #     - POSTGRES_PASSWORD=changeme
  #   volumes:
  #     - postgres-data:/var/lib/postgresql/data
  #   ports:
  #     - "5432:5432"

volumes:
  greenstack-data:
  # postgres-data:`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Environment Variables */}
      <DocsSection title="Environment Variables" icon={<Database />}>
        <DocsParagraph>
          Configure Greenstack using environment variables in your <code>docker-compose.yml</code>
          or with <code>docker run -e</code>:
        </DocsParagraph>

        <Card className="my-6">
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div>
                <div className="flex items-center gap-2 mb-2">
                  <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">DATABASE_URL</code>
                  <Badge variant="outline">Optional</Badge>
                </div>
                <p className="text-sm text-muted-foreground ml-6">
                  Database connection string. Default: <code>sqlite:///data/greenstack.db</code>
                </p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                  <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">CORS_ORIGINS</code>
                  <Badge variant="outline">Optional</Badge>
                </div>
                <p className="text-sm text-muted-foreground ml-6">
                  Comma-separated list of allowed CORS origins
                </p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                  <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">LOG_LEVEL</code>
                  <Badge variant="outline">Optional</Badge>
                </div>
                <p className="text-sm text-muted-foreground ml-6">
                  Logging level: DEBUG, INFO, WARNING, ERROR. Default: INFO
                </p>
              </div>

              <div>
                <div className="flex items-center gap-2 mb-2">
                  <code className="px-2 py-1 bg-surface-active rounded text-sm font-mono">API_PORT</code>
                  <Badge variant="outline">Optional</Badge>
                </div>
                <p className="text-sm text-muted-foreground ml-6">
                  Port for API server. Default: 8000
                </p>
              </div>
            </div>
          </CardContent>
        </Card>

        <DocsParagraph>
          For complete configuration options, see <DocsLink href="/docs/user-guide/configuration" external={false} onNavigate={onNavigate}>
          Configuration Guide</DocsLink>.
        </DocsParagraph>
      </DocsSection>

      {/* Data Persistence */}
      <DocsSection title="Data Persistence" icon={<Database />}>
        <DocsParagraph>
          Use Docker volumes to persist your data:
        </DocsParagraph>

        <DocsCodeBlock language="bash">
{`# Create a named volume
docker volume create greenstack-data

# Run with volume mounted
docker run -d \\
  --name greenstack \\
  -p 8000:8000 \\
  -v greenstack-data:/data \\
  ghcr.io/me-catalyst/greenstack:latest

# Backup data
docker run --rm \\
  -v greenstack-data:/data \\
  -v $(pwd):/backup \\
  alpine tar czf /backup/greenstack-backup.tar.gz /data

# Restore data
docker run --rm \\
  -v greenstack-data:/data \\
  -v $(pwd):/backup \\
  alpine tar xzf /backup/greenstack-backup.tar.gz -C /`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Production Deployment */}
      <DocsSection title="Production Deployment">
        <DocsParagraph>
          For production deployments, consider these additional configurations:
        </DocsParagraph>

        <DocsSteps
          steps={[
            {
              title: 'Use PostgreSQL',
              content: (
                <div>
                  <DocsParagraph>
                    Switch from SQLite to PostgreSQL for better concurrent access:
                  </DocsParagraph>
                  <DocsCodeBlock language="bash">
{`docker run -d \\
  --name greenstack \\
  -p 8000:8000 \\
  -e DATABASE_URL=postgresql://user:pass@db:5432/greenstack \\
  ghcr.io/me-catalyst/greenstack:latest`}
                  </DocsCodeBlock>
                </div>
              )
            },
            {
              title: 'Configure Reverse Proxy',
              content: (
                <div>
                  <DocsParagraph>
                    Use Nginx or Traefik for SSL termination and load balancing:
                  </DocsParagraph>
                  <DocsCodeBlock language="yaml">
{`# Example Nginx config
server {
    listen 443 ssl http2;
    server_name greenstack.example.com;

    ssl_certificate /path/to/cert.pem;
    ssl_certificate_key /path/to/key.pem;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}`}
                  </DocsCodeBlock>
                </div>
              )
            },
            {
              title: 'Set Resource Limits',
              content: (
                <div>
                  <DocsParagraph>
                    Limit memory and CPU usage:
                  </DocsParagraph>
                  <DocsCodeBlock language="yaml">
{`services:
  api:
    deploy:
      resources:
        limits:
          cpus: '2'
          memory: 2G
        reservations:
          cpus: '1'
          memory: 1G`}
                  </DocsCodeBlock>
                </div>
              )
            },
            {
              title: 'Enable Monitoring',
              content: (
                <div>
                  <DocsParagraph>
                    Add health checks and monitoring:
                  </DocsParagraph>
                  <DocsCodeBlock language="yaml">
{`healthcheck:
  test: ["CMD", "curl", "-f", "http://localhost:8000/api/health"]
  interval: 30s
  timeout: 10s
  retries: 3
  start_period: 40s`}
                  </DocsCodeBlock>
                </div>
              )
            }
          ]}
        />

        <DocsParagraph className="mt-6">
          For more production deployment details, see <DocsLink href="/docs/deployment/production" external={false} onNavigate={onNavigate}>
          Production Deployment Guide</DocsLink>.
        </DocsParagraph>
      </DocsSection>

      {/* Troubleshooting */}
      <DocsSection title="Troubleshooting" icon={<AlertCircle />}>
        <DocsCallout type="warning" title="Common Issues">
          <div className="space-y-4">
            <div>
              <h4 className="font-semibold text-foreground mb-2">Container won't start</h4>
              <DocsParagraph>Check logs for errors:</DocsParagraph>
              <DocsCodeBlock language="bash">
{`docker logs greenstack
docker-compose logs api`}
              </DocsCodeBlock>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Port already in use</h4>
              <DocsParagraph>Change the port mapping:</DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Use port 9000 instead
docker run -p 9000:8000 ghcr.io/me-catalyst/greenstack:latest`}
              </DocsCodeBlock>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Permission denied on volume</h4>
              <DocsParagraph>Ensure proper permissions:</DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Linux: Fix volume permissions
sudo chown -R 1000:1000 ./data`}
              </DocsCodeBlock>
            </div>

            <div>
              <h4 className="font-semibold text-foreground mb-2">Database locked errors</h4>
              <DocsParagraph>
                If using SQLite with multiple containers, switch to PostgreSQL or ensure only one container accesses the database.
              </DocsParagraph>
            </div>
          </div>
        </DocsCallout>
      </DocsSection>

      {/* Next Steps */}
      <DocsSection title="Next Steps">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/user-guide/configuration" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Configuration Guide</h5>
            <p className="text-sm text-muted-foreground">Detailed configuration options</p>
          </DocsLink>

          <DocsLink href="/docs/deployment/production" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Production Deployment</h5>
            <p className="text-sm text-muted-foreground">Deploy to production environments</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/web-interface" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Web Interface Guide</h5>
            <p className="text-sm text-muted-foreground">Learn the dashboard features</p>
          </DocsLink>

          <DocsLink href="/docs/api/overview" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">API Documentation</h5>
            <p className="text-sm text-muted-foreground">Explore the REST API</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
