import React from 'react';
import { Container, Layers, Play, Settings, AlertTriangle, Zap } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsMermaid from '../../../components/docs/DocsMermaid';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'deployment/docker',
  title: 'Docker Deployment',
  description: 'Deploy Greenstack using Docker and Docker Compose for containerized, reproducible deployments',
  category: 'deployment',
  order: 1,
  keywords: ['docker', 'container', 'deployment', 'compose', 'containerization', 'production'],
  lastUpdated: '2025-01-17',
};

export default function DockerDeployment({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Docker Deployment"
        description="Containerized deployment with Docker for production environments"
        icon={<Container className="w-12 h-12 text-brand-green" />}
      />

      {/* Overview */}
      <DocsSection title="Docker Overview" icon={<Container />}>
        <DocsParagraph>
          Docker provides a containerized deployment solution for Greenstack, ensuring consistent
          environments across development, staging, and production. The Docker setup includes
          multi-stage builds, health checks, and optimized layer caching.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-3 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Layers className="w-4 h-4 text-brand-green" />
                Multi-Container
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Separate containers for frontend, backend, and database with Docker Compose orchestration
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Zap className="w-4 h-4 text-brand-green" />
                Production-Ready
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Optimized builds with health checks, restart policies, and volume persistence
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <Settings className="w-4 h-4 text-brand-green" />
                Easy Configuration
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Environment-based configuration with .env files and Docker Compose profiles
              </p>
            </CardContent>
          </Card>
        </div>

        <DocsMermaid chart={`
graph TB
    subgraph Host["🖥️ Docker Host"]
        subgraph Network["greenstack-network"]
            Frontend["🌐 Frontend Container<br/>nginx:alpine<br/>Port 80"]
            Backend["⚡ Backend Container<br/>python:3.10-slim<br/>Port 8000"]
            DB["💾 Database Container<br/>postgres:15-alpine<br/>Port 5432"]
        end
        Volumes["📦 Docker Volumes<br/>- db_data<br/>- uploads"]
    end

    User["👤 User"] -->|HTTP/HTTPS| Frontend
    Frontend -->|API Requests| Backend
    Backend -->|SQL Queries| DB
    DB -.->|Persist Data| Volumes
    Backend -.->|Store Files| Volumes

    style Host fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Network fill:#2a3050,stroke:#51cf66,stroke-width:2px,color:#fff
    style Frontend fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Backend fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style DB fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Volumes fill:#1a1f3a,stroke:#51cf66,stroke-width:2px,color:#fff
    style User fill:#2d5016,stroke:#3DB60F,stroke-width:3px,color:#fff
`} className="my-6" />
      </DocsSection>

      {/* Prerequisites */}
      <DocsSection title="Prerequisites">
        <DocsParagraph>
          Ensure you have Docker and Docker Compose installed before proceeding.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Required Software</CardTitle>
          </CardHeader>
          <CardContent>
            <ul className="space-y-2 text-sm text-muted-foreground">
              <li>• <strong>Docker Engine 20.10+</strong> - Container runtime</li>
              <li>• <strong>Docker Compose 2.0+</strong> - Multi-container orchestration</li>
              <li>• <strong>4GB+ RAM</strong> - Recommended for production</li>
              <li>• <strong>10GB+ Disk Space</strong> - For images and volumes</li>
            </ul>
          </CardContent>
        </Card>

        <DocsCodeBlock language="bash">
{`# Verify Docker installation
docker --version
# Docker version 24.0.0 or higher

# Verify Docker Compose installation
docker compose version
# Docker Compose version v2.20.0 or higher

# Check Docker is running
docker ps`}
        </DocsCodeBlock>
      </DocsSection>

      {/* Quick Start */}
      <DocsSection title="Quick Start" icon={<Play />}>
        <DocsParagraph>
          Get Greenstack running with Docker Compose in under 2 minutes.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">One-Command Deployment</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="bash">
{`# Clone the repository
git clone https://github.com/ME-Catalyst/greenstack.git
cd greenstack

# Copy environment template
cp .env.example .env

# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Access the application
# Frontend: http://localhost
# Backend API: http://localhost:8000
# API Docs: http://localhost:8000/docs`}
            </DocsCodeBlock>
          </CardContent>
        </Card>

        <DocsCallout type="success" title="First Time Setup">
          <DocsParagraph>
            The first run will build images and initialize the database. This takes 2-3 minutes.
            Subsequent starts are much faster (~10 seconds).
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Docker Compose Configuration */}
      <DocsSection title="Docker Compose Configuration" icon={<Settings />}>
        <DocsParagraph>
          The <code>docker-compose.yml</code> file defines all services and their configuration.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">docker-compose.yml</CardTitle>
            <CardDescription>Complete Docker Compose configuration</CardDescription>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="yaml">
{`version: '3.8'

services:
  # PostgreSQL Database
  db:
    image: postgres:15-alpine
    container_name: greenstack-db
    restart: unless-stopped
    environment:
      POSTGRES_DB: greenstack
      POSTGRES_USER: greenstack
      POSTGRES_PASSWORD: \${DB_PASSWORD:-changeme}
    volumes:
      - db_data:/var/lib/postgresql/data
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U greenstack"]
      interval: 10s
      timeout: 5s
      retries: 5
    networks:
      - greenstack-network

  # FastAPI Backend
  backend:
    build:
      context: .
      dockerfile: Dockerfile.backend
      target: production
    container_name: greenstack-backend
    restart: unless-stopped
    ports:
      - "8000:8000"
    environment:
      DATABASE_URL: postgresql://greenstack:\${DB_PASSWORD:-changeme}@db:5432/greenstack
      ENVIRONMENT: production
      LOG_LEVEL: \${LOG_LEVEL:-info}
    volumes:
      - uploads:/app/uploads
    depends_on:
      db:
        condition: service_healthy
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:8000/health"]
      interval: 30s
      timeout: 10s
      retries: 3
      start_period: 40s
    networks:
      - greenstack-network

  # React Frontend (Production Build)
  frontend:
    build:
      context: ./frontend
      dockerfile: Dockerfile
      target: production
    container_name: greenstack-frontend
    restart: unless-stopped
    ports:
      - "80:80"
    environment:
      VITE_API_URL: http://localhost:8000
    depends_on:
      - backend
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost"]
      interval: 30s
      timeout: 10s
      retries: 3
    networks:
      - greenstack-network

volumes:
  db_data:
    name: greenstack-db-data
  uploads:
    name: greenstack-uploads

networks:
  greenstack-network:
    name: greenstack-network
    driver: bridge`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Dockerfiles */}
      <DocsSection title="Dockerfile Configuration">
        <DocsParagraph>
          Multi-stage Dockerfiles optimize image size and build performance.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Backend Dockerfile</CardTitle>
              <CardDescription>Python FastAPI with multi-stage build</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="dockerfile">
{`# Dockerfile.backend
FROM python:3.10-slim as base

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \\
    gcc \\
    curl \\
    && rm -rf /var/lib/apt/lists/*

# Copy requirements
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

# Development stage
FROM base as development
ENV ENVIRONMENT=development
CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--reload"]

# Production stage
FROM base as production
ENV ENVIRONMENT=production
ENV PYTHONUNBUFFERED=1

# Create non-root user
RUN useradd -m -u 1000 greenstack && \\
    chown -R greenstack:greenstack /app
USER greenstack

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \\
  CMD curl -f http://localhost:8000/health || exit 1

EXPOSE 8000

CMD ["uvicorn", "src.api:app", "--host", "0.0.0.0", "--port", "8000", "--workers", "4"]`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Frontend Dockerfile</CardTitle>
              <CardDescription>React app with Nginx serving</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="dockerfile">
{`# frontend/Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Copy package files
COPY package*.json ./

# Install dependencies
RUN npm ci --only=production

# Copy source code
COPY . .

# Build production bundle
RUN npm run build

# Production stage with Nginx
FROM nginx:alpine as production

# Copy built files
COPY --from=build /app/dist /usr/share/nginx/html

# Copy custom Nginx config
COPY nginx.conf /etc/nginx/conf.d/default.conf

# Health check
HEALTHCHECK --interval=30s --timeout=10s \\
  CMD wget --quiet --tries=1 --spider http://localhost || exit 1

EXPOSE 80

CMD ["nginx", "-g", "daemon off;"]`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Environment Configuration */}
      <DocsSection title="Environment Variables">
        <DocsParagraph>
          Configure your deployment using environment variables in <code>.env</code> file.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">.env Configuration</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="bash">
{`# Database Configuration
DB_PASSWORD=your_secure_password_here
DATABASE_URL=postgresql://greenstack:your_secure_password_here@db:5432/greenstack

# Backend Configuration
ENVIRONMENT=production
LOG_LEVEL=info
SECRET_KEY=your_secret_key_here
ALLOWED_ORIGINS=http://localhost,https://yourdomain.com

# Frontend Configuration
VITE_API_URL=http://localhost:8000

# Optional: Email Configuration
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Optional: File Upload Limits
MAX_UPLOAD_SIZE=10485760  # 10MB in bytes`}
            </DocsCodeBlock>
          </CardContent>
        </Card>

        <DocsCallout type="warning" title="Security">
          <DocsParagraph>
            Never commit <code>.env</code> files to version control. Always use strong,
            randomly generated passwords for production deployments.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Common Commands */}
      <DocsSection title="Common Docker Commands" icon={<Play />}>
        <DocsParagraph>
          Essential Docker Compose commands for managing your deployment.
        </DocsParagraph>

        <div className="grid gap-4 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Service Management</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Start all services
docker compose up -d

# Stop all services
docker compose down

# Restart all services
docker compose restart

# Stop and remove containers, networks, volumes
docker compose down -v

# View running containers
docker compose ps

# View logs from all services
docker compose logs -f

# View logs from specific service
docker compose logs -f backend

# Scale a service (e.g., run 3 backend instances)
docker compose up -d --scale backend=3`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Container Management</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Execute command in running container
docker compose exec backend bash

# Access database shell
docker compose exec db psql -U greenstack -d greenstack

# View container resource usage
docker stats

# Inspect container details
docker compose exec backend env

# Copy files from container
docker cp greenstack-backend:/app/logs ./logs`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Image Management</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Rebuild images (after code changes)
docker compose build

# Rebuild without cache
docker compose build --no-cache

# Pull latest base images
docker compose pull

# Remove unused images
docker image prune

# Remove all stopped containers and unused images
docker system prune -a`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Volume Management</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# List volumes
docker volume ls

# Inspect volume
docker volume inspect greenstack-db-data

# Backup database volume
docker run --rm -v greenstack-db-data:/data -v $(pwd):/backup \\
  alpine tar czf /backup/db-backup.tar.gz -C /data .

# Restore database volume
docker run --rm -v greenstack-db-data:/data -v $(pwd):/backup \\
  alpine tar xzf /backup/db-backup.tar.gz -C /data`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Production Deployment */}
      <DocsSection title="Production Deployment">
        <DocsParagraph>
          Additional considerations for production environments.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <AlertTriangle className="w-4 h-4 text-brand-green" />
                Security Checklist
              </CardTitle>
            </CardHeader>
            <CardContent>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">1</Badge>
                  <span>Use strong, randomly generated passwords for all services</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">2</Badge>
                  <span>Enable HTTPS with SSL/TLS certificates (use Let's Encrypt)</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">3</Badge>
                  <span>Configure firewall rules to restrict access</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">4</Badge>
                  <span>Enable Docker content trust for image verification</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">5</Badge>
                  <span>Run containers as non-root users</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">6</Badge>
                  <span>Regularly update base images and dependencies</span>
                </li>
                <li className="flex items-start gap-2">
                  <Badge variant="outline" className="mt-0.5">7</Badge>
                  <span>Set up automated backups for database and uploads</span>
                </li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Reverse Proxy with Nginx</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="nginx">
{`# nginx.conf for production
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Security headers
    add_header X-Frame-Options "SAMEORIGIN" always;
    add_header X-Content-Type-Options "nosniff" always;
    add_header X-XSS-Protection "1; mode=block" always;

    # Frontend
    location / {
        proxy_pass http://localhost:80;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }

    # Backend API
    location /api {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;

        # WebSocket support (if needed)
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
    }
}`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Troubleshooting */}
      <DocsSection title="Troubleshooting">
        <DocsParagraph>
          Common issues and their solutions when deploying with Docker.
        </DocsParagraph>

        <div className="space-y-4 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Container won't start</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Check container logs for error messages:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# View logs for specific service
docker compose logs backend

# Check container status
docker compose ps

# Inspect container
docker inspect greenstack-backend`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Database connection errors</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Ensure database is healthy and credentials are correct:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Check database health
docker compose exec db pg_isready -U greenstack

# Verify environment variables
docker compose exec backend env | grep DATABASE_URL

# Test database connection
docker compose exec db psql -U greenstack -d greenstack -c "SELECT 1;"`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Port already in use</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Change ports in <code>docker-compose.yml</code>:
              </DocsParagraph>
              <DocsCodeBlock language="yaml">
{`services:
  frontend:
    ports:
      - "8080:80"  # Use port 8080 instead of 80
  backend:
    ports:
      - "8001:8000"  # Use port 8001 instead of 8000`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Out of disk space</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Clean up unused Docker resources:
              </DocsParagraph>
              <DocsCodeBlock language="bash">
{`# Remove unused images
docker image prune -a

# Remove stopped containers
docker container prune

# Remove unused volumes
docker volume prune

# Remove all unused resources
docker system prune -a --volumes`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/deployment/production" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Production Guide</h5>
            <p className="text-sm text-muted-foreground">Full production deployment guide</p>
          </DocsLink>

          <DocsLink href="/docs/deployment/monitoring" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Monitoring & Logging</h5>
            <p className="text-sm text-muted-foreground">Monitor your Docker deployment</p>
          </DocsLink>

          <DocsLink href="https://docs.docker.com/compose/" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Docker Compose Docs</h5>
            <p className="text-sm text-muted-foreground">Official Docker Compose documentation</p>
          </DocsLink>

          <DocsLink href="https://docs.docker.com/engine/reference/builder/" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Dockerfile Reference</h5>
            <p className="text-sm text-muted-foreground">Dockerfile best practices</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
