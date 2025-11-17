import React from 'react';
import { Activity, FileText, AlertCircle, BarChart3, Eye, Zap } from 'lucide-react';
import DocsPage from '../../../components/docs/DocsPage';
import DocsHero from '../../../components/docs/DocsHero';
import DocsSection from '../../../components/docs/DocsSection';
import DocsCallout from '../../../components/docs/DocsCallout';
import { DocsParagraph, DocsLink } from '../../../components/docs/DocsText';
import DocsCodeBlock from '../../../components/docs/DocsCodeBlock';
import DocsMermaid from '../../../components/docs/DocsMermaid';
import { Card, CardContent, CardHeader, CardTitle, CardDescription, Badge } from '../../../components/ui';

export const metadata = {
  id: 'deployment/monitoring',
  title: 'Monitoring & Logging',
  description: 'Monitor performance, track errors, and debug Greenstack in production environments',
  category: 'deployment',
  order: 2,
  keywords: ['monitoring', 'logging', 'debugging', 'metrics', 'observability', 'performance'],
  lastUpdated: '2025-01-17',
};

export default function MonitoringLogging({ onNavigate }) {
  return (
    <DocsPage>
      <DocsHero
        title="Monitoring & Logging"
        description="Comprehensive observability for production deployments"
        icon={<Activity className="w-12 h-12 text-brand-green" />}
      />

      {/* Overview */}
      <DocsSection title="Observability Overview" icon={<Eye />}>
        <DocsParagraph>
          Greenstack provides comprehensive logging, metrics, and monitoring capabilities for
          production deployments. The observability stack includes structured logging, health checks,
          performance metrics, and error tracking.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-3 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <FileText className="w-4 h-4 text-brand-green" />
                Structured Logging
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                JSON-formatted logs with request IDs, timestamps, and contextual information
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-brand-green" />
                Performance Metrics
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Real-time metrics for API response times, database queries, and resource usage
              </p>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base flex items-center gap-2">
                <AlertCircle className="w-4 h-4 text-brand-green" />
                Error Tracking
              </CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-sm text-muted-foreground">
                Automatic error capture with stack traces, context, and user impact analysis
              </p>
            </CardContent>
          </Card>
        </div>

        <DocsMermaid chart={`
graph TB
    subgraph App["📦 Greenstack Application"]
        Frontend["🌐 Frontend"]
        Backend["⚡ Backend API"]
        DB["💾 Database"]
    end

    subgraph Observability["👁️ Observability Stack"]
        Logs["📝 Log Aggregation<br/>Structured JSON logs"]
        Metrics["📊 Metrics Collection<br/>Prometheus/StatsD"]
        Traces["🔍 Distributed Tracing<br/>Request tracking"]
        Health["💚 Health Checks<br/>Endpoint monitoring"]
    end

    subgraph Visualization["📈 Visualization & Alerts"]
        Dashboard["📊 Grafana Dashboard<br/>Real-time metrics"]
        Alerts["🔔 Alerting<br/>Email/Slack notifications"]
        LogViewer["🔎 Log Viewer<br/>Search & analyze"]
    end

    Frontend --> Logs
    Backend --> Logs
    Backend --> Metrics
    Backend --> Traces
    Backend --> Health
    DB --> Metrics

    Logs --> LogViewer
    Metrics --> Dashboard
    Traces --> LogViewer
    Health --> Dashboard
    Metrics --> Alerts

    style App fill:#1a1f3a,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Observability fill:#2d5016,stroke:#3DB60F,stroke-width:2px,color:#fff
    style Visualization fill:#2a3050,stroke:#51cf66,stroke-width:2px,color:#fff
    style Logs fill:#1a1f3a,stroke:#51cf66,stroke-width:1px,color:#fff
    style Metrics fill:#1a1f3a,stroke:#51cf66,stroke-width:1px,color:#fff
    style Traces fill:#1a1f3a,stroke:#51cf66,stroke-width:1px,color:#fff
    style Health fill:#1a1f3a,stroke:#51cf66,stroke-width:1px,color:#fff
`} className="my-6" />
      </DocsSection>

      {/* Logging */}
      <DocsSection title="Application Logging" icon={<FileText />}>
        <DocsParagraph>
          Greenstack uses structured logging with Python's logging module and Winston for Node.js.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Backend Logging (Python)</CardTitle>
              <CardDescription>Structured JSON logging with FastAPI</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="python">
{`import logging
import json
from datetime import datetime

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(message)s',
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler('logs/greenstack.log')
    ]
)

logger = logging.getLogger(__name__)

class StructuredLogger:
    """Structured JSON logger for production."""

    def log(self, level, message, **kwargs):
        log_entry = {
            "timestamp": datetime.utcnow().isoformat(),
            "level": level,
            "message": message,
            "service": "greenstack-backend",
            **kwargs
        }
        logger.log(getattr(logging, level.upper()), json.dumps(log_entry))

# Usage in API endpoints
structured_logger = StructuredLogger()

@app.post("/api/iodds/upload")
async def upload_iodd(file: UploadFile, request: Request):
    request_id = str(uuid.uuid4())

    structured_logger.log(
        "info",
        "IODD upload started",
        request_id=request_id,
        filename=file.filename,
        content_type=file.content_type,
        client_ip=request.client.host
    )

    try:
        result = await process_upload(file)
        structured_logger.log(
            "info",
            "IODD upload completed",
            request_id=request_id,
            device_id=result["id"],
            duration_ms=result["duration"]
        )
        return result
    except Exception as e:
        structured_logger.log(
            "error",
            "IODD upload failed",
            request_id=request_id,
            error=str(e),
            stack_trace=traceback.format_exc()
        )
        raise`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Log Levels</CardTitle>
            </CardHeader>
            <CardContent>
              <div className="space-y-2 text-sm">
                <div className="flex items-center gap-3">
                  <Badge variant="outline" className="bg-red-500/10 text-red-400 border-red-500/30">ERROR</Badge>
                  <span className="text-muted-foreground">Critical failures requiring immediate attention</span>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="outline" className="bg-yellow-500/10 text-yellow-400 border-yellow-500/30">WARNING</Badge>
                  <span className="text-muted-foreground">Potential issues that may need investigation</span>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="outline" className="bg-blue-500/10 text-blue-400 border-blue-500/30">INFO</Badge>
                  <span className="text-muted-foreground">General application events and state changes</span>
                </div>
                <div className="flex items-center gap-3">
                  <Badge variant="outline" className="bg-gray-500/10 text-gray-400 border-gray-500/30">DEBUG</Badge>
                  <span className="text-muted-foreground">Detailed debugging information (development only)</span>
                </div>
              </div>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Viewing Logs</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Docker Compose logs
docker compose logs -f backend
docker compose logs -f frontend
docker compose logs --tail=100 backend

# Application logs (if mounted volume)
tail -f logs/greenstack.log

# Filter logs by level
docker compose logs backend | grep ERROR

# Search logs for specific request ID
docker compose logs backend | grep "request_id: abc-123"

# JSON log parsing with jq
docker compose logs --no-log-prefix backend | jq 'select(.level == "error")'`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Health Checks */}
      <DocsSection title="Health Checks" icon={<Activity />}>
        <DocsParagraph>
          Health check endpoints monitor application and dependency status.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Health Check Endpoints</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="python">
{`from fastapi import APIRouter, HTTPException
from sqlalchemy import text

router = APIRouter()

@router.get("/health")
async def health_check():
    """Basic health check - is the API responding?"""
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "version": "1.0.0"
    }

@router.get("/health/detailed")
async def detailed_health_check(db: Session = Depends(get_db)):
    """Detailed health check with dependency status."""
    health_status = {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat(),
        "checks": {}
    }

    # Database check
    try:
        db.execute(text("SELECT 1"))
        health_status["checks"]["database"] = {
            "status": "healthy",
            "response_time_ms": 5
        }
    except Exception as e:
        health_status["status"] = "unhealthy"
        health_status["checks"]["database"] = {
            "status": "unhealthy",
            "error": str(e)
        }

    # Disk space check
    disk_usage = psutil.disk_usage('/')
    disk_free_gb = disk_usage.free / (1024**3)
    health_status["checks"]["disk_space"] = {
        "status": "healthy" if disk_free_gb > 1 else "warning",
        "free_gb": round(disk_free_gb, 2),
        "percent_used": disk_usage.percent
    }

    # Memory check
    memory = psutil.virtual_memory()
    health_status["checks"]["memory"] = {
        "status": "healthy" if memory.percent < 90 else "warning",
        "percent_used": memory.percent,
        "available_gb": round(memory.available / (1024**3), 2)
    }

    if health_status["status"] == "unhealthy":
        raise HTTPException(status_code=503, detail=health_status)

    return health_status`}
            </DocsCodeBlock>
          </CardContent>
        </Card>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Monitoring Health Endpoints</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="bash">
{`# Test health endpoint
curl http://localhost:8000/health

# Detailed health check
curl http://localhost:8000/health/detailed

# Use in monitoring scripts
#!/bin/bash
HEALTH_URL="http://localhost:8000/health"
STATUS=$(curl -s -o /dev/null -w "%{http_code}" $HEALTH_URL)

if [ $STATUS -ne 200 ]; then
  echo "Health check failed! Status: $STATUS"
  # Send alert (email, Slack, PagerDuty, etc.)
fi`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Performance Metrics */}
      <DocsSection title="Performance Metrics" icon={<BarChart3 />}>
        <DocsParagraph>
          Track API performance, database queries, and resource utilization.
        </DocsParagraph>

        <div className="space-y-6 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Request Metrics Middleware</CardTitle>
              <CardDescription>Track API endpoint performance</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="python">
{`from fastapi import Request
import time
from prometheus_client import Counter, Histogram

# Prometheus metrics
request_count = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status']
)

request_duration = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration',
    ['method', 'endpoint']
)

@app.middleware("http")
async def metrics_middleware(request: Request, call_next):
    """Track request metrics."""
    start_time = time.time()

    # Process request
    response = await call_next(request)

    # Calculate duration
    duration = time.time() - start_time

    # Record metrics
    request_count.labels(
        method=request.method,
        endpoint=request.url.path,
        status=response.status_code
    ).inc()

    request_duration.labels(
        method=request.method,
        endpoint=request.url.path
    ).observe(duration)

    # Add custom headers
    response.headers["X-Process-Time"] = str(duration)

    return response`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Database Query Metrics</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="python">
{`from sqlalchemy import event
from sqlalchemy.engine import Engine

# Track slow queries
@event.listens_for(Engine, "before_cursor_execute")
def before_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    conn.info.setdefault('query_start_time', []).append(time.time())

@event.listens_for(Engine, "after_cursor_execute")
def after_cursor_execute(conn, cursor, statement, parameters, context, executemany):
    total_time = time.time() - conn.info['query_start_time'].pop(-1)

    # Log slow queries (> 100ms)
    if total_time > 0.1:
        logger.warning(
            "Slow query detected",
            duration_ms=total_time * 1000,
            query=statement[:200]
        )`}
              </DocsCodeBlock>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">System Metrics</CardTitle>
            </CardHeader>
            <CardContent>
              <DocsCodeBlock language="bash">
{`# Docker container stats
docker stats greenstack-backend greenstack-frontend greenstack-db

# System resource usage
docker compose exec backend python -c "
import psutil
print(f'CPU: {psutil.cpu_percent()}%')
print(f'Memory: {psutil.virtual_memory().percent}%')
print(f'Disk: {psutil.disk_usage(\"/\").percent}%')
"

# Database metrics
docker compose exec db psql -U greenstack -d greenstack -c "
SELECT
    schemaname,
    tablename,
    pg_size_pretty(pg_total_relation_size(schemaname||'.'||tablename)) AS size
FROM pg_tables
WHERE schemaname = 'public'
ORDER BY pg_total_relation_size(schemaname||'.'||tablename) DESC;
"`}
              </DocsCodeBlock>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Error Tracking */}
      <DocsSection title="Error Tracking" icon={<AlertCircle />}>
        <DocsParagraph>
          Capture and track errors with contextual information for debugging.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Error Handler Middleware</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="python">
{`from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
import traceback

@app.exception_handler(Exception)
async def global_exception_handler(request: Request, exc: Exception):
    """Global error handler with detailed logging."""

    # Generate error ID for tracking
    error_id = str(uuid.uuid4())

    # Log detailed error information
    logger.error(
        "Unhandled exception",
        error_id=error_id,
        error_type=type(exc).__name__,
        error_message=str(exc),
        stack_trace=traceback.format_exc(),
        request_path=str(request.url),
        request_method=request.method,
        client_ip=request.client.host,
        user_agent=request.headers.get("user-agent")
    )

    # Return user-friendly error response
    return JSONResponse(
        status_code=500,
        content={
            "error": "Internal server error",
            "error_id": error_id,
            "message": "An unexpected error occurred. Please contact support with this error ID."
        }
    )

@app.exception_handler(HTTPException)
async def http_exception_handler(request: Request, exc: HTTPException):
    """Handle HTTP exceptions."""
    logger.warning(
        "HTTP exception",
        status_code=exc.status_code,
        detail=exc.detail,
        request_path=str(request.url)
    )
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )`}
            </DocsCodeBlock>
          </CardContent>
        </Card>

        <DocsCallout type="info" title="Error Tracking Services">
          <DocsParagraph>
            For production deployments, consider integrating error tracking services like
            Sentry, Rollbar, or Bugsnag for advanced error monitoring with automatic grouping,
            release tracking, and user impact analysis.
          </DocsParagraph>
        </DocsCallout>
      </DocsSection>

      {/* Monitoring Tools */}
      <DocsSection title="Monitoring Tools" icon={<Zap />}>
        <DocsParagraph>
          Popular tools for monitoring Greenstack in production.
        </DocsParagraph>

        <div className="grid gap-4 md:grid-cols-2 my-6">
          <Card>
            <CardHeader>
              <CardTitle className="text-base">Prometheus + Grafana</CardTitle>
              <CardDescription>Metrics collection and visualization</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Industry-standard monitoring stack with custom dashboards.
              </DocsParagraph>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Real-time metrics collection</li>
                <li>• Custom alerting rules</li>
                <li>• Beautiful dashboards</li>
                <li>• Long-term metric storage</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">ELK Stack</CardTitle>
              <CardDescription>Elasticsearch, Logstash, Kibana</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Centralized log management and analysis.
              </DocsParagraph>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• Centralized log aggregation</li>
                <li>• Full-text search capabilities</li>
                <li>• Log visualization</li>
                <li>• Anomaly detection</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Datadog</CardTitle>
              <CardDescription>All-in-one monitoring platform</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                Comprehensive monitoring as a service.
              </DocsParagraph>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• APM (Application Performance Monitoring)</li>
                <li>• Infrastructure monitoring</li>
                <li>• Log management</li>
                <li>• Distributed tracing</li>
              </ul>
            </CardContent>
          </Card>

          <Card>
            <CardHeader>
              <CardTitle className="text-base">Uptime Monitoring</CardTitle>
              <CardDescription>UptimeRobot, Pingdom, StatusCake</CardDescription>
            </CardHeader>
            <CardContent>
              <DocsParagraph className="mb-3">
                External uptime monitoring and alerting.
              </DocsParagraph>
              <ul className="space-y-2 text-sm text-muted-foreground">
                <li>• HTTP/HTTPS endpoint monitoring</li>
                <li>• SSL certificate monitoring</li>
                <li>• Multi-location checks</li>
                <li>• Instant downtime alerts</li>
              </ul>
            </CardContent>
          </Card>
        </div>
      </DocsSection>

      {/* Alerting */}
      <DocsSection title="Alerting Strategy">
        <DocsParagraph>
          Configure alerts for critical issues requiring immediate attention.
        </DocsParagraph>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Recommended Alerts</CardTitle>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              <div>
                <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                  <Badge variant="outline" className="bg-red-500/10 text-red-400 border-red-500/30">CRITICAL</Badge>
                  Immediate Response Required
                </h4>
                <ul className="space-y-1 text-sm text-muted-foreground ml-4">
                  <li>• Application down (health check failing)</li>
                  <li>• Database connection lost</li>
                  <li>• Disk space &lt; 10% free</li>
                  <li>• Memory usage &gt; 95%</li>
                  <li>• Error rate &gt; 5% of requests</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                  <Badge variant="outline" className="bg-yellow-500/10 text-yellow-400 border-yellow-500/30">WARNING</Badge>
                  Monitor and Investigate
                </h4>
                <ul className="space-y-1 text-sm text-muted-foreground ml-4">
                  <li>• Response time &gt; 1 second (95th percentile)</li>
                  <li>• Disk space &lt; 20% free</li>
                  <li>• Memory usage &gt; 80%</li>
                  <li>• High number of slow database queries</li>
                  <li>• SSL certificate expiring in &lt; 30 days</li>
                </ul>
              </div>

              <div>
                <h4 className="font-semibold text-foreground mb-2 flex items-center gap-2">
                  <Badge variant="outline" className="bg-blue-500/10 text-blue-400 border-blue-500/30">INFO</Badge>
                  Informational Notices
                </h4>
                <ul className="space-y-1 text-sm text-muted-foreground ml-4">
                  <li>• New deployment completed</li>
                  <li>• Scheduled maintenance starting/completed</li>
                  <li>• Backup completed successfully</li>
                  <li>• Configuration changes applied</li>
                </ul>
              </div>
            </div>
          </CardContent>
        </Card>

        <Card className="my-6">
          <CardHeader>
            <CardTitle className="text-base">Alert Configuration Example</CardTitle>
          </CardHeader>
          <CardContent>
            <DocsCodeBlock language="yaml">
{`# Example Prometheus alert rules
groups:
  - name: greenstack_alerts
    rules:
      - alert: HighErrorRate
        expr: rate(http_requests_total{status=~"5.."}[5m]) > 0.05
        for: 5m
        labels:
          severity: critical
        annotations:
          summary: "High error rate detected"
          description: "Error rate is {{ $value | humanizePercentage }} over the last 5 minutes"

      - alert: SlowResponseTime
        expr: histogram_quantile(0.95, http_request_duration_seconds) > 1
        for: 10m
        labels:
          severity: warning
        annotations:
          summary: "Slow API response time"
          description: "95th percentile response time is {{ $value }}s"

      - alert: DatabaseDown
        expr: up{job="greenstack-db"} == 0
        for: 1m
        labels:
          severity: critical
        annotations:
          summary: "Database is down"
          description: "Database has been down for more than 1 minute"`}
            </DocsCodeBlock>
          </CardContent>
        </Card>
      </DocsSection>

      {/* Related Resources */}
      <DocsSection title="Related Resources">
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 my-6">
          <DocsLink href="/docs/deployment/docker" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Docker Deployment</h5>
            <p className="text-sm text-muted-foreground">Deploy with Docker containers</p>
          </DocsLink>

          <DocsLink href="/docs/user-guide/troubleshooting" external={false} onNavigate={onNavigate} className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Troubleshooting</h5>
            <p className="text-sm text-muted-foreground">Common issues and solutions</p>
          </DocsLink>

          <DocsLink href="https://prometheus.io/docs/introduction/overview/" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Prometheus Documentation</h5>
            <p className="text-sm text-muted-foreground">Learn about Prometheus monitoring</p>
          </DocsLink>

          <DocsLink href="https://grafana.com/docs/" external className="block border border-border rounded-lg p-4 hover:border-brand-green transition-colors">
            <h5 className="font-semibold text-foreground mb-1">Grafana Documentation</h5>
            <p className="text-sm text-muted-foreground">Create monitoring dashboards</p>
          </DocsLink>
        </div>
      </DocsSection>
    </DocsPage>
  );
}
