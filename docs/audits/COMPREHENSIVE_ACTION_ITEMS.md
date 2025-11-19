# GreenStack Comprehensive Action Items - Path to 100%

**Generated:** 2025-11-18
**Current Overall Score:** 52/100 (Grade: D - NOT PRODUCTION READY)
**Target Score:** 92-95/100 (Grade: A - Production Ready)
**Total Items:** 150 issues across 18 audit phases
**Total Effort:** ~1,000 hours (approximately 6 months with 2 engineers)

---

## Executive Summary

This document contains EVERY unresolved action item from the comprehensive 18-phase codebase audit. Items are organized in the **optimal order of completion** to achieve maximum impact in minimum time. Complex tasks have been broken down into detailed subtasks.

### Remediation Timeline

| Phase | Duration | Team | Outcome | Score |
|-------|----------|------|---------|-------|
| **Phase 1: Critical Blockers (P0)** | 3 weeks | 2 engineers | Pilot deployment ready | 78/100 |
| **Phase 2: High Priority (P1)** | 3 weeks | 2 engineers | Production ready | 92/100 |
| **Phase 3: Optimization (P2)** | 2 weeks | 2 engineers | Enterprise grade | 95/100 |

---

## WEEK 1: CRITICAL SECURITY & PRODUCTION BLOCKERS

**Goal:** Fix immediate security vulnerabilities and production deployment blockers
**Effort:** 54 hours (2 engineers × 27 hours each)
**Score Impact:** +15 points

### Day 1 (Monday) - Security Hardening

#### SEC-002: Generate Strong Passwords (2 hours)
**Priority:** P0 - CRITICAL
**Files:** `.env.example`, all docker-compose files
**Current State:** 8 services with weak defaults (postgres123, redis123, mqtt123, etc.)

**Subtasks:**
1. Create password generation script `scripts/generate-secrets.sh`:
   ```bash
   #!/bin/bash
   echo "SECRET_KEY=$(openssl rand -hex 32)"
   echo "JWT_SECRET_KEY=$(openssl rand -hex 32)"
   echo "POSTGRES_PASSWORD=$(openssl rand -base64 32)"
   echo "REDIS_PASSWORD=$(openssl rand -base64 32)"
   echo "MQTT_PASSWORD=$(openssl rand -base64 32)"
   echo "INFLUXDB_TOKEN=$(openssl rand -base64 32)"
   echo "GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 32)"
   echo "NODERED_CREDENTIAL_SECRET=$(openssl rand -hex 32)"
   ```
2. Update `.env.example` to remove ALL default passwords
3. Add validation to `src/greenstack.py` startup to fail if production mode with weak passwords
4. Create `.env.production.template` with empty password fields
5. Update documentation to require password generation before first deployment
6. **Test:** Verify application refuses to start in production mode without strong passwords

#### SEC-001: Remove Hardcoded InfluxDB Token (1 hour)
**Priority:** P0 - CRITICAL
**Files:** `config/grafana/provisioning/datasources/influxdb.yml`
**Current:** Token hardcoded as `my-super-secret-auth-token`

**Subtasks:**
1. Edit `config/grafana/provisioning/datasources/influxdb.yml` line 436
2. Replace `token: my-super-secret-auth-token` with `token: ${INFLUXDB_TOKEN}`
3. Update `docker-compose.iot.yml` Grafana service environment to include `INFLUXDB_TOKEN`
4. Remove token from git history: `git filter-branch --tree-filter 'sed -i "s/my-super-secret-auth-token/\${INFLUXDB_TOKEN}/g" config/grafana/provisioning/datasources/influxdb.yml' HEAD`
5. **Test:** Verify Grafana can connect to InfluxDB with environment variable

#### SEC-003: Remove PostgreSQL Port Exposure (30 minutes)
**Priority:** P0 - CRITICAL
**Files:** `docker-compose.yml` line 28
**Current:** Port 5432 exposed to host

**Subtasks:**
1. Edit `docker-compose.yml` PostgreSQL service
2. Remove entire `ports:` section (lines 28-29)
3. Verify application can still connect via Docker network
4. Update documentation to note database only accessible internally
5. **Test:** Confirm `telnet localhost 5432` fails but application works

#### SEC-004: Enable MQTT TLS Encryption (3 hours)
**Priority:** P0 - CRITICAL
**Files:** `config/mosquitto/mosquitto.conf`, MQTT client configurations
**Current:** Unencrypted MQTT on port 1883

**Subtasks:**
1. Generate self-signed certificates for development:
   ```bash
   openssl req -new -x509 -days 365 -extensions v3_ca -keyout ca.key -out ca.crt
   openssl genrsa -out server.key 2048
   openssl req -new -out server.csr -key server.key
   openssl x509 -req -in server.csr -CA ca.crt -CAkey ca.key -CAcreateserial -out server.crt -days 365
   ```
2. Move certificates to `config/mosquitto/certs/`
3. Uncomment TLS configuration in `mosquitto.conf` (lines 30-36)
4. Update listener to port 8883
5. Update `services/mqtt-bridge/bridge.py` to use TLS:
   ```python
   client.tls_set(ca_certs="ca.crt", certfile="server.crt", keyfile="server.key")
   client.connect(broker_host, 8883, 60)
   ```
6. Update `docker-compose.iot.yml` to map port 8883 instead of 1883
7. Document certificate renewal procedure
8. **Test:** Verify MQTT publish/subscribe works over TLS

#### SEC-005: Enable InfluxDB TLS (2 hours)
**Priority:** P0 - CRITICAL
**Files:** `docker-compose.iot.yml`, InfluxDB configuration

**Subtasks:**
1. Generate InfluxDB certificates (similar to MQTT)
2. Create `config/influxdb/influxdb.conf` with TLS settings
3. Update `docker-compose.iot.yml` InfluxDB service to mount certificates
4. Update environment variables: `INFLUXDB_HTTP_HTTPS_ENABLED=true`
5. Update `services/influx-ingestion/ingest.py` InfluxDB client to use HTTPS
6. Update Grafana datasource to use HTTPS URL
7. **Test:** Verify data ingestion works over HTTPS

### Day 2 (Tuesday) - Monitoring Foundation

#### MON-002: Set Up Sentry Error Tracking (3 hours)
**Priority:** P0 - CRITICAL
**Files:** `src/greenstack.py`, `frontend/src/main.jsx`, `requirements.txt`, `package.json`

**Subtasks:**
1. Create free Sentry account at sentry.io
2. Create two projects: "greenstack-backend" and "greenstack-frontend"
3. Add to `requirements.txt`:
   ```
   sentry-sdk[fastapi]==1.40.0
   ```
4. Add to `frontend/package.json`:
   ```json
   "@sentry/react": "^7.100.0"
   ```
5. Initialize Sentry in `src/greenstack.py`:
   ```python
   import sentry_sdk
   from sentry_sdk.integrations.fastapi import FastApiIntegration

   if os.getenv("SENTRY_DSN"):
       sentry_sdk.init(
           dsn=os.getenv("SENTRY_DSN"),
           integrations=[FastApiIntegration()],
           environment=os.getenv("ENVIRONMENT", "development"),
           traces_sample_rate=0.1,
           profiles_sample_rate=0.1,
       )
   ```
6. Initialize Sentry in `frontend/src/main.jsx`:
   ```javascript
   import * as Sentry from "@sentry/react";

   if (import.meta.env.VITE_SENTRY_DSN) {
     Sentry.init({
       dsn: import.meta.env.VITE_SENTRY_DSN,
       environment: import.meta.env.VITE_ENVIRONMENT,
       tracesSampleRate: 0.1,
     });
   }
   ```
7. Add error boundaries to React app
8. Test by throwing intentional error
9. **Test:** Verify errors appear in Sentry dashboard

#### MON-003: Add Prometheus Metrics (6 hours)
**Priority:** P0 - CRITICAL
**Files:** `src/greenstack.py`, `requirements.txt`, `docker-compose.yml`

**Subtasks:**
1. Add to `requirements.txt`:
   ```
   prometheus-client==0.19.0
   prometheus-fastapi-instrumentator==6.1.0
   ```
2. Add to `src/greenstack.py`:
   ```python
   from prometheus_fastapi_instrumentator import Instrumentator

   instrumentator = Instrumentator(
       should_group_status_codes=True,
       should_ignore_untemplated=True,
       should_respect_env_var=True,
       excluded_handlers=["/health", "/metrics"],
   )

   instrumentator.instrument(app).expose(app, endpoint="/metrics")
   ```
3. Add custom metrics for business operations:
   ```python
   from prometheus_client import Counter, Histogram

   iodd_uploads = Counter('iodd_uploads_total', 'Total IODD file uploads')
   iodd_parse_duration = Histogram('iodd_parse_duration_seconds', 'IODD parsing duration')
   device_searches = Counter('device_searches_total', 'Device catalog searches')
   ```
4. Instrument key endpoints with custom metrics
5. Create `config/prometheus/prometheus.yml`:
   ```yaml
   global:
     scrape_interval: 15s
   scrape_configs:
     - job_name: 'greenstack'
       static_configs:
         - targets: ['greenstack:8000']
   ```
6. Add Prometheus to `docker-compose.yml`:
   ```yaml
   prometheus:
     image: prom/prometheus:latest
     volumes:
       - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
       - prometheus-data:/prometheus
     ports:
       - "9090:9090"
   ```
7. **Test:** Access http://localhost:9090 and query `http_requests_total`

### Day 3 (Wednesday) - Version Control & Configuration

#### CICD-001: Fix Version Mismatch (1 hour)
**Priority:** P0 - CRITICAL
**Files:** `pyproject.toml`, `frontend/package.json`, `.github/workflows/ci.yml`

**Subtasks:**
1. Update `frontend/package.json` version from 2.0.0 to 2.0.1
2. Create `.github/workflows/version-check.yml`:
   ```yaml
   name: Version Consistency Check
   on: [push, pull_request]
   jobs:
     check-versions:
       runs-on: ubuntu-latest
       steps:
         - uses: actions/checkout@v4
         - name: Extract versions
           run: |
             BACKEND=$(grep '^version = ' pyproject.toml | sed 's/version = "\(.*\)"/\1/')
             FRONTEND=$(grep '"version":' frontend/package.json | sed 's/.*"version": "\(.*\)".*/\1/')
             echo "Backend: $BACKEND"
             echo "Frontend: $FRONTEND"
             if [ "$BACKEND" != "$FRONTEND" ]; then
               echo "ERROR: Version mismatch!"
               exit 1
             fi
   ```
3. Add version check to existing CI pipeline
4. Document versioning policy in README
5. **Test:** Create PR with mismatched versions, verify CI fails

#### DB-003: Add Database Connection Pooling Limits (2 hours)
**Priority:** P0 - CRITICAL
**Files:** `src/database.py`

**Subtasks:**
1. Edit `src/database.py` engine creation
2. Add pooling parameters:
   ```python
   engine = create_engine(
       DATABASE_URL,
       pool_size=20,              # Concurrent connections
       max_overflow=40,           # Additional connections under load
       pool_timeout=30,           # Wait time for connection
       pool_recycle=3600,         # Recycle connections every hour
       pool_pre_ping=True,        # Check connection health before use
   )
   ```
3. Add connection pool monitoring metrics
4. Document pool sizing in deployment guide
5. **Test:** Run load test with 100 concurrent requests, verify no connection exhaustion

### Day 4 (Thursday) - Critical Accessibility Fixes

#### A11Y-009: Fix Color Contrast Failure (1 hour)
**Priority:** P0 - CRITICAL
**Files:** `frontend/src/config/themes.js` line 109
**Current:** #6b7280 on dark background = 3.93:1 (fails 4.5:1 minimum)

**Subtasks:**
1. Edit `frontend/src/config/themes.js` line 109
2. Change `foregroundMuted: '#6b7280'` to `foregroundMuted: '#7d8694'`
3. Run contrast checker to verify 4.5:1 ratio achieved
4. Check all usages of muted color still look acceptable
5. **Test:** Run axe accessibility scanner, verify color contrast passes

#### A11Y-001: Add Missing Form Labels (2 hours)
**Priority:** P0 - CRITICAL
**Files:** `frontend/src/App.jsx` lines 471-477, 505-512

**Subtasks:**
1. Find all checkbox inputs without proper labels
2. Add `id` to each input and `htmlFor` to corresponding label:
   ```jsx
   <input id="select-all-devices" type="checkbox" ... />
   <label htmlFor="select-all-devices">Select All</label>
   ```
3. Find all text inputs with only placeholder (not accessible)
4. Add proper `<Label>` components with `htmlFor` attributes
5. For visually hidden labels, add `className="sr-only"`:
   ```jsx
   <Label htmlFor="eds-search" className="sr-only">Search EDS files</Label>
   ```
6. **Test:** Use screen reader (NVDA/JAWS), verify all inputs announced with purpose

#### A11Y-002: Fix Interactive Divs (4 hours)
**Priority:** P0 - CRITICAL
**Files:** `frontend/src/App.jsx` lines 316-331

**Subtasks:**
1. Find all clickable `<div>` elements (search for `onClick` on divs)
2. For each, evaluate if it should be `<button>` or `<a>`
3. Replace divs with semantic elements:
   ```jsx
   // Before
   <div className="cursor-pointer" onClick={() => handleClick()}>

   // After
   <button onClick={() => handleClick()}>
   ```
4. If must remain div, add keyboard support:
   ```jsx
   <div
     role="button"
     tabIndex={0}
     onClick={handleClick}
     onKeyDown={(e) => e.key === 'Enter' && handleClick()}
   />
   ```
5. Ensure all buttons have proper focus styles
6. **Test:** Navigate entire UI with keyboard only, verify all actions accessible

### Day 5 (Friday) - More Accessibility + Documentation Start

#### A11Y-003: Add ARIA Labels to Icon Buttons (3 hours)
**Priority:** P0 - CRITICAL
**Files:** `frontend/src/App.jsx`, `frontend/src/components/TicketModal.jsx`

**Subtasks:**
1. Find all icon-only buttons (buttons with SVG but no text)
2. Add `aria-label` to each:
   ```jsx
   <button aria-label="Collapse sidebar">
     <ChevronLeftIcon />
   </button>
   ```
3. Create mapping of all icons to descriptive labels
4. For icon + text buttons, add `aria-label` only if icon meaning differs from text
5. **Test:** Use screen reader, verify all buttons announce their purpose

#### A11Y-004: Implement Modal Focus Trap (6 hours)
**Priority:** P0 - CRITICAL
**Files:** `frontend/src/components/TicketModal.jsx`

**Subtasks:**
1. Install focus-trap-react: `npm install focus-trap-react@^10.2.0`
2. Create `useFocusTrap` custom hook:
   ```javascript
   import { useRef, useEffect } from 'react';
   import { createFocusTrap } from 'focus-trap';

   export function useFocusTrap(active) {
     const ref = useRef();
     const trapRef = useRef();

     useEffect(() => {
       if (!ref.current || !active) return;
       trapRef.current = createFocusTrap(ref.current, {
         escapeDeactivates: true,
         returnFocusOnDeactivate: true,
       });
       trapRef.current.activate();
       return () => trapRef.current?.deactivate();
     }, [active]);

     return ref;
   }
   ```
3. Apply to TicketModal:
   ```jsx
   function TicketModal({ isOpen, onClose }) {
     const modalRef = useFocusTrap(isOpen);

     return (
       <div ref={modalRef} role="dialog" aria-modal="true">
         ...
       </div>
     );
   }
   ```
4. Ensure first focusable element gets focus on open
5. Ensure Tab/Shift-Tab cycles within modal only
6. Ensure Escape key closes modal
7. **Test:** Open modal, verify Tab doesn't escape, Escape closes, focus returns

#### DOC-001: Create Deployment Runbook (8 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `docs/guides/operations/DEPLOYMENT_RUNBOOK.md`

**Subtasks:**
1. Create `docs/guides/operations/` directory
2. Create runbook with sections:
   - **Prerequisites** (server requirements, DNS, certificates)
   - **Pre-deployment checklist** (passwords generated, backups configured, monitoring ready)
   - **Step-by-step deployment** (15-20 numbered steps with verification)
   - **Post-deployment verification** (health checks, smoke tests)
   - **Rollback procedure** (how to revert to previous version)
   - **Common deployment issues** (troubleshooting)
3. Include actual commands for each step
4. Add verification commands after critical steps
5. Reference other documentation (troubleshooting guide, disaster recovery)
6. **Test:** Have someone unfamiliar with the system deploy using only the runbook

---

## WEEK 2: CRITICAL PRODUCTION INFRASTRUCTURE

**Goal:** Implement backup, monitoring, and testing infrastructure
**Effort:** 66 hours (2 engineers × 33 hours each)
**Score Impact:** +11 points

### Day 6 (Monday) - Backup & Disaster Recovery

#### PROD-002 / DB-001: Implement Automated Backups (6 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `scripts/backup.sh`, `scripts/restore.sh`, `.env`

**Subtasks:**
1. Create `scripts/backup.sh`:
   ```bash
   #!/bin/bash
   # See detailed script from PHASE_17 report, section 3.2
   TIMESTAMP=$(date +%Y%m%d_%H%M%S)
   BACKUP_NAME="greenstack_backup_${TIMESTAMP}"

   # Backup PostgreSQL
   docker exec greenstack-postgres-1 pg_dump -U $POSTGRES_USER -d $POSTGRES_DB --format=custom > postgres_${TIMESTAMP}.dump

   # Backup uploaded files
   tar -czf uploads_${TIMESTAMP}.tar.gz uploads/

   # Create manifest with checksums
   sha256sum *.dump *.tar.gz > manifest_${TIMESTAMP}.txt

   # Upload to S3
   aws s3 cp greenstack_backup_${TIMESTAMP}.tar.gz s3://${BACKUP_S3_BUCKET}/

   # Cleanup old local backups (keep 7 days)
   find backups/ -name "*.tar.gz" -mtime +7 -delete
   ```
2. Create `scripts/restore.sh` (see PHASE_17 section 3.2 for full script)
3. Add to crontab: `0 2 * * * /opt/greenstack/scripts/backup.sh`
4. Create `scripts/verify-backup.sh` to test backup integrity
5. Add backup age monitoring alert (alert if backup older than 48 hours)
6. Document backup retention policy (30 days S3, 7 days local)
7. **Test:** Run backup, delete database, restore successfully

#### DOC-003: Create Disaster Recovery Procedures (4 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `docs/guides/operations/DISASTER_RECOVERY.md`

**Subtasks:**
1. Create disaster recovery document with scenarios:
   - **Scenario 1:** Database corruption (RTO: 30 min, RPO: 24 hrs)
   - **Scenario 2:** Server failure (RTO: 2-4 hrs, RPO: 24 hrs)
   - **Scenario 3:** Data center outage (RTO: 3-4 hrs, RPO: 24 hrs)
   - **Scenario 4:** Ransomware attack (RTO: 4-8 hrs, RPO: 24 hrs)
2. For each scenario, document:
   - Detection (how you know it happened)
   - Initial response (first 5 minutes)
   - Recovery procedure (step-by-step)
   - Verification (how to confirm recovery)
   - Post-incident (lessons learned template)
3. Include emergency contact information
4. Document backup locations (S3 bucket, credentials location)
5. Include restoration commands for each scenario
6. **Test:** Run tabletop exercise simulating server failure

### Day 7 (Tuesday) - Monitoring Stack Deployment Part 1

#### PROD-004 / MON-001: Deploy Prometheus + Grafana (14 hours)
**Priority:** P0 - CRITICAL
**Files:** `docker-compose.yml`, `config/prometheus/`, `config/grafana/`

**Subtasks:**
1. Create `config/prometheus/prometheus.yml` (see MON-003 above + PHASE_17)
2. Create `config/prometheus/alerts.yml` with critical alert rules:
   ```yaml
   groups:
     - name: critical_alerts
       rules:
         - alert: ServiceDown
           expr: up == 0
           for: 1m
           labels:
             severity: critical
           annotations:
             summary: "Service {{ $labels.job }} is down"
   ```
3. Add Grafana to `docker-compose.yml`:
   ```yaml
   grafana:
     image: grafana/grafana:10.2.3
     environment:
       - GF_SECURITY_ADMIN_PASSWORD=${GRAFANA_ADMIN_PASSWORD}
       - GF_INSTALL_PLUGINS=grafana-clock-panel,grafana-piechart-panel
     volumes:
       - grafana-data:/var/lib/grafana
       - ./config/grafana/provisioning:/etc/grafana/provisioning
     ports:
       - "3001:3000"
   ```
4. Create Grafana datasource provisioning `config/grafana/provisioning/datasources/prometheus.yml`
5. Deploy Alertmanager for notifications
6. **Test:** Verify all services scraped by Prometheus, Grafana accessible

**Continue Day 7 (afternoon):**

7. Create `config/alertmanager/config.yml`:
   ```yaml
   route:
     receiver: 'email-critical'
     routes:
       - match:
           severity: critical
         receiver: 'email-critical'
       - match:
           severity: warning
         receiver: 'slack-warnings'

   receivers:
     - name: 'email-critical'
       email_configs:
         - to: 'ops@example.com'
           from: 'alerts@greenstack.com'
     - name: 'slack-warnings'
       slack_configs:
         - api_url: '${SLACK_WEBHOOK_URL}'
   ```
8. Configure SMTP for email alerts
9. Set up Slack webhook for notifications
10. **Test:** Trigger test alert, verify notifications received

### Day 8 (Wednesday) - Grafana Dashboards

#### PROD-007: Create Grafana Dashboards (6 hours)
**Priority:** P0 - CRITICAL
**Files:** `config/grafana/dashboards/*.json`

**Subtasks:**
1. Create **Application Overview Dashboard**:
   - Request rate (requests/second)
   - Response time (p50, p95, p99)
   - Error rate (errors/total requests)
   - Active users (last 24h)
   - IODD uploads (last 24h)
   - Top 10 slowest endpoints
2. Create **System Health Dashboard**:
   - CPU usage per container
   - Memory usage per container
   - Disk usage
   - Network I/O
   - Container restarts
3. Create **Database Performance Dashboard**:
   - Active connections
   - Query duration
   - Transactions per second
   - Cache hit rate
   - Table sizes
4. Create **Business Metrics Dashboard**:
   - Total devices in catalog
   - Total parameters
   - Active users
   - Search queries per hour
   - Most searched vendors
5. Configure auto-refresh (30 seconds)
6. Set up dashboard variables (time range, environment)
7. Export dashboard JSON to `config/grafana/dashboards/`
8. **Test:** Verify all panels display data correctly

### Day 9 (Thursday) - Testing Infrastructure Part 1

#### TEST-001 / IOT-001: Create IoT Integration Tests (12 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `tests/integration/test_mqtt_*.py`, `tests/integration/test_influx_*.py`, `tests/integration/test_shadow_*.py`

**Subtasks:**
1. Create `tests/integration/conftest.py` with IoT service fixtures:
   ```python
   import pytest
   import docker
   import paho.mqtt.client as mqtt
   from influxdb_client import InfluxDBClient

   @pytest.fixture(scope="session")
   def mqtt_broker():
       """Start Mosquitto for testing"""
       client = docker.from_env()
       container = client.containers.run(
           "eclipse-mosquitto:2.0",
           detach=True,
           ports={'1883/tcp': 1883}
       )
       yield "localhost:1883"
       container.stop()
       container.remove()
   ```
2. Create `tests/integration/test_mqtt_bridge.py` (20+ tests):
   - `test_mqtt_connection_establishment()`
   - `test_mqtt_publish_telemetry()`
   - `test_mqtt_subscribe_to_topics()`
   - `test_mqtt_qos_levels()`
   - `test_mqtt_retained_messages()`
   - `test_mqtt_will_messages()`
   - `test_mqtt_reconnection_after_broker_restart()`
   - `test_mqtt_invalid_json_payload()`
   - `test_mqtt_redis_persistence()`
   - `test_mqtt_api_device_registration()`
3. Create `tests/integration/test_influx_ingestion.py` (15+ tests):
   - `test_influxdb_connection()`
   - `test_influxdb_write_single_point()`
   - `test_influxdb_write_batch()`
   - `test_influxdb_query_telemetry()`
   - `test_influxdb_retention_policy()`
   - `test_influxdb_write_error_handling()`
   - `test_influxdb_connection_failure_recovery()`
   - `test_mqtt_to_influxdb_e2e_flow()`
4. Create `tests/integration/test_device_shadow.py` (15+ tests):
   - `test_shadow_creation()`
   - `test_shadow_update_reported_state()`
   - `test_shadow_update_desired_state()`
   - `test_shadow_ttl_expiration()`
   - `test_shadow_concurrent_updates()`
   - `test_shadow_redis_persistence()`
5. Run tests in CI pipeline
6. **Test:** All 50+ integration tests pass

### Day 10 (Friday) - Testing Infrastructure Part 2

#### TEST-003: Create Load Testing Suite (12 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `tests/load/locustfile.py`, `tests/load/README.md`

**Subtasks:**
1. Install Locust: `pip install locust`
2. Create `tests/load/locustfile.py` with user scenarios:
   ```python
   from locust import HttpUser, task, between

   class GreenStackUser(HttpUser):
       wait_time = between(1, 5)

       def on_start(self):
           # Login
           response = self.client.post("/api/auth/login", json={
               "username": "test_user",
               "password": "test_password"
           })
           self.token = response.json()["access_token"]

       @task(3)
       def view_devices(self):
           self.client.get("/api/devices", headers={"Authorization": f"Bearer {self.token}"})

       @task(2)
       def search_devices(self):
           self.client.get("/api/devices/search?q=valve", headers={"Authorization": f"Bearer {self.token}"})

       @task(1)
       def view_device_details(self):
           self.client.get("/api/devices/1", headers={"Authorization": f"Bearer {self.token}"})
   ```
3. Create separate user class for heavy operations:
   ```python
   class IODDUploadUser(HttpUser):
       wait_time = between(10, 30)

       @task
       def upload_iodd(self):
           with open("tests/fixtures/sample.iodd", "rb") as f:
               self.client.post("/api/iodd/upload", files={"file": f})
   ```
4. Create load test scenarios:
   - **Baseline:** 10 concurrent users, 5 min
   - **Normal:** 50 concurrent users, 10 min
   - **Peak:** 100 concurrent users, 10 min
   - **Stress:** 200 concurrent users, 15 min
   - **Spike:** 10→100 users sudden spike, 5 min
5. Create `tests/load/run_tests.sh` script to execute all scenarios
6. Document performance targets in `tests/load/README.md`:
   - API response < 300ms (p95)
   - Homepage load < 2s
   - Error rate < 1%
   - Concurrent users: 100+
7. Run baseline test and document results
8. **Test:** System handles 100 concurrent users with <300ms p95 latency

#### TEST-004: Create Smoke Test Suite (8 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `tests/smoke/test_deployment.py`

**Subtasks:**
1. Create `tests/smoke/test_deployment.py`:
   ```python
   import pytest
   import requests

   BASE_URL = os.getenv("SMOKE_TEST_URL", "http://localhost:8000")

   def test_health_check():
       r = requests.get(f"{BASE_URL}/health")
       assert r.status_code == 200
       assert r.json()["status"] == "healthy"

   def test_database_connectivity():
       r = requests.get(f"{BASE_URL}/api/devices")
       assert r.status_code == 200

   def test_redis_connectivity():
       r = requests.post(f"{BASE_URL}/api/auth/login", json={"username": "admin", "password": "admin"})
       assert r.status_code == 200

   def test_iodd_upload():
       with open("tests/fixtures/sample.iodd", "rb") as f:
           r = requests.post(f"{BASE_URL}/api/iodd/upload", files={"file": f})
       assert r.status_code in [200, 202]

   def test_frontend_loads():
       r = requests.get(f"{BASE_URL}/")
       assert r.status_code == 200
       assert "GreenStack" in r.text
   ```
2. Add smoke tests for all critical paths:
   - User authentication
   - Device search
   - Parameter retrieval
   - Documentation generation
   - API endpoint availability
3. Create CI job to run smoke tests after deployment
4. Add to deployment runbook as verification step
5. **Test:** Run smoke tests against production staging environment

---

## WEEK 3: REMAINING P0 CRITICAL ITEMS

**Goal:** Complete all P0 blockers to achieve pilot deployment readiness
**Effort:** 62 hours (2 engineers × 31 hours each)
**Score Impact:** +6 points (Total after Week 3: 78/100)

### Day 11-12 (Monday-Tuesday) - Code Refactoring Part 1

#### CQ-001: Refactor save_device() Function (24 hours)
**Priority:** P0 - CRITICAL
**Files:** `src/greenstack.py` lines 2135-2617 (483 lines, complexity 46)

**Detailed Subtasks:**

**Day 11 Morning: Architecture & Base Classes (6 hours)**
1. Create new directory structure:
   ```
   src/storage/
     __init__.py
     base.py           # Abstract base class
     device.py         # DeviceSaver
     parameter.py      # ParameterSaver
     process_data.py   # ProcessDataSaver
     variable.py       # VariableSaver
     event.py          # EventSaver
     diagnostic.py     # DiagnosticSaver
     menu.py           # MenuSaver
     identity.py       # IdentitySaver
     communication.py  # CommunicationSaver
     profile.py        # ProfileImageSaver
   ```
2. Create `src/storage/base.py` with abstract base class:
   ```python
   from abc import ABC, abstractmethod
   from typing import Any, Optional
   import psycopg2

   class BaseSaver(ABC):
       """Base class for all storage savers"""

       def __init__(self, cursor: psycopg2.extensions.cursor):
           self.cursor = cursor

       @abstractmethod
       def save(self, device_id: int, data: Any) -> Optional[int]:
           """Save data and return ID if applicable"""
           pass

       def _execute(self, query: str, params: tuple):
           """Execute query with error handling"""
           try:
               self.cursor.execute(query, params)
           except psycopg2.Error as e:
               logger.error(f"Database error in {self.__class__.__name__}: {e}")
               raise
   ```

**Day 11 Afternoon: Device & Parameter Savers (6 hours)**
3. Create `src/storage/device.py`:
   ```python
   from .base import BaseSaver
   from ..models import DeviceProfile

   class DeviceSaver(BaseSaver):
       """Handles core device information storage"""

       def save(self, profile: DeviceProfile) -> int:
           """Save device and return device_id"""
           query = """
               INSERT INTO devices (
                   device_id, vendor_name, vendor_id, vendor_url,
                   device_name, device_family, device_symbol,
                   product_text, product_url, release_date
               ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
               ON CONFLICT (device_id) DO UPDATE SET
                   vendor_name = EXCLUDED.vendor_name,
                   device_name = EXCLUDED.device_name
               RETURNING id
           """
           params = (
               profile.device_id,
               profile.vendor_name,
               profile.vendor_id,
               # ... all other fields
           )
           self._execute(query, params)
           return self.cursor.fetchone()[0]
   ```
4. Create `src/storage/parameter.py`:
   ```python
   class ParameterSaver(BaseSaver):
       """Handles parameter storage"""

       def save(self, device_id: int, parameters: list) -> None:
           """Save all parameters for a device"""
           # Delete existing
           self._execute("DELETE FROM parameters WHERE device_id = %s", (device_id,))

           # Bulk insert new
           query = """
               INSERT INTO parameters (
                   device_id, index, name, description,
                   access, data_type, bit_offset, bit_length,
                   min_value, max_value, default_value, unit_code
               ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
           """
           for param in parameters:
               self._execute(query, (device_id, param.index, ...))
   ```

**Day 12 Morning: ProcessData, Variable, Event Savers (6 hours)**
5. Create `src/storage/process_data.py`, `variable.py`, `event.py` following same pattern
6. Each saver should:
   - Have single responsibility
   - Handle its own DELETE + INSERT
   - Log operations
   - Have comprehensive error handling
   - Be under 100 lines

**Day 12 Afternoon: Orchestrator & Integration (6 hours)**
7. Create `src/storage/__init__.py` with orchestrator:
   ```python
   from .device import DeviceSaver
   from .parameter import ParameterSaver
   # ... import all savers

   class StorageManager:
       """Orchestrates all savers"""

       def __init__(self, cursor):
           self.device_saver = DeviceSaver(cursor)
           self.parameter_saver = ParameterSaver(cursor)
           self.process_data_saver = ProcessDataSaver(cursor)
           # ... initialize all savers

       def save_device(self, profile: DeviceProfile) -> int:
           """
           Save complete device profile.
           Replaces original 483-line function with 45-line orchestrator.
           """
           try:
               # Save core device (returns device_id)
               device_id = self.device_saver.save(profile)

               # Save all related data (order matters due to foreign keys)
               self.parameter_saver.save(device_id, profile.parameters)
               self.process_data_saver.save(device_id, profile.process_data)
               self.variable_saver.save(device_id, profile.variables)
               self.event_saver.save(device_id, profile.events)
               self.diagnostic_saver.save(device_id, profile.diagnostics)
               self.menu_saver.save(device_id, profile.menus)
               self.identity_saver.save(device_id, profile.identity)
               self.communication_saver.save(device_id, profile.communication)
               self.profile_saver.save(device_id, profile.profile_image)

               logger.info(f"Successfully saved device {profile.device_name} (ID: {device_id})")
               return device_id

           except Exception as e:
               logger.error(f"Failed to save device {profile.device_name}: {e}")
               raise
   ```
8. Replace usage in `src/greenstack.py`:
   ```python
   # Old (line 2135):
   def save_device(self, profile: DeviceProfile) -> int:
       # ... 483 lines ...

   # New (line 2135):
   def save_device(self, profile: DeviceProfile) -> int:
       """Save device using modular storage system"""
       from src.storage import StorageManager
       storage = StorageManager(cursor)
       return storage.save_device(profile)
   ```
9. Write unit tests for each saver (10 tests per saver = 90 tests)
10. Update documentation
11. **Test:** Full integration test - upload IODD, verify all tables populated correctly

### Day 13 (Wednesday) - SSL/TLS Configuration

#### PROD-001: Obtain SSL/TLS Certificates and Configure Nginx (4 hours)
**Priority:** P0 - SHOWSTOPPER
**Files:** NEW - `/etc/nginx/sites-available/greenstack`, SSL certificates

**Subtasks:**
1. Install Nginx: `sudo apt install nginx certbot python3-certbot-nginx`
2. Configure DNS A record pointing to server IP
3. Obtain Let's Encrypt certificates:
   ```bash
   sudo certbot certonly --nginx -d greenstack.yourdomain.com
   ```
4. Create Nginx configuration `/etc/nginx/sites-available/greenstack`:
   ```nginx
   # HTTP -> HTTPS redirect
   server {
       listen 80;
       server_name greenstack.yourdomain.com;
       return 301 https://$server_name$request_uri;
   }

   # HTTPS server
   server {
       listen 443 ssl http2;
       server_name greenstack.yourdomain.com;

       ssl_certificate /etc/letsencrypt/live/greenstack.yourdomain.com/fullchain.pem;
       ssl_certificate_key /etc/letsencrypt/live/greenstack.yourdomain.com/privkey.pem;

       # Modern SSL configuration
       ssl_protocols TLSv1.2 TLSv1.3;
       ssl_ciphers HIGH:!aNULL:!MD5;
       ssl_prefer_server_ciphers on;

       # Security headers
       add_header Strict-Transport-Security "max-age=31536000; includeSubDomains" always;
       add_header X-Frame-Options "SAMEORIGIN" always;
       add_header X-Content-Type-Options "nosniff" always;

       # API backend
       location /api {
           proxy_pass http://localhost:8000;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
           proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
           proxy_set_header X-Forwarded-Proto $scheme;
       }

       # Frontend
       location / {
           proxy_pass http://localhost:3000;
           proxy_set_header Host $host;
       }
   }
   ```
5. Enable site: `sudo ln -s /etc/nginx/sites-available/greenstack /etc/nginx/sites-enabled/`
6. Test config: `sudo nginx -t`
7. Reload Nginx: `sudo systemctl reload nginx`
8. Set up auto-renewal: `sudo certbot renew --dry-run`
9. Add renewal to crontab: `0 3 * * * certbot renew --quiet`
10. **Test:** Access https://greenstack.yourdomain.com, verify HTTPS, check SSL Labs rating (should be A+)

### Day 14 (Thursday) - Documentation Completion

#### DOC-002: Create Comprehensive Troubleshooting Guide (8 hours)
**Priority:** P0 - CRITICAL
**Files:** NEW - `docs/guides/TROUBLESHOOTING.md`

**Subtasks:**
1. Create troubleshooting guide with sections:
   - **Application Won't Start** (5 scenarios + solutions)
   - **Slow Performance** (database, CPU, memory issues)
   - **Database Migration Failed** (version conflicts, rollback)
   - **File Upload Fails** (size limits, permissions)
   - **Redis Connection Issues** (password, network)
   - **IODD Parsing Errors** (XML validation, schema version)
   - **Out of Disk Space** (cleanup procedures)
   - **SSL Certificate Expired** (renewal)
   - **Health Check Failing** (service troubleshooting)
   - **IoT Services Not Receiving Data** (MQTT, InfluxDB troubleshooting)
2. For each issue, include:
   - Symptoms (how you know it's this issue)
   - Diagnosis commands (how to confirm)
   - Root causes (what could cause this)
   - Solution steps (numbered, with commands)
   - Prevention (how to avoid in future)
3. Add "Getting Help" section with:
   - Information to collect (logs, config, version)
   - How to create minimal reproduction
   - Support channels
4. Include actual command examples for common operations
5. **Test:** Walk through each scenario, verify commands work

#### PROD-008: Document Disaster Recovery Plan (8 hours)
**Priority:** P0
**Files:** Enhanced `docs/guides/operations/DISASTER_RECOVERY.md`

**Subtasks:**
1. Enhance disaster recovery document with:
   - **Emergency Contacts** (primary, secondary, escalation)
   - **RTO/RPO Definitions** (Recovery Time/Point Objectives)
   - **Backup Locations** (S3 bucket, local, credentials)
   - **Scenario 1: Database Corruption**
     - Detection: Database errors in logs, health check fails
     - Response: Stop writes, assess corruption extent
     - Recovery: Restore from latest backup (documented commands)
     - Verification: Run smoke tests
     - Expected RTO: 30 minutes
   - **Scenario 2: Complete Server Failure**
     - Detection: Monitoring alerts, ping fails
     - Response: Provision new server
     - Recovery: Deploy from backup (15 steps)
     - Verification: Full smoke test suite
     - Expected RTO: 2-4 hours
   - **Scenario 3: Ransomware Attack**
     - Detection: File encryption, ransom note
     - Response: Isolate systems immediately
     - Recovery: Restore from clean backup
     - Verification: Security scan
     - Expected RTO: 4-8 hours
   - **Scenario 4: AWS Region Outage**
     - Detection: AWS status page, service unreachable
     - Response: Activate DR region
     - Recovery: Restore from S3 cross-region backup
     - Expected RTO: 3-4 hours
2. Include actual recovery commands for each scenario
3. Add post-incident report template
4. Document last test date and next scheduled test
5. **Test:** Run tabletop disaster recovery drill

### Day 15 (Friday) - Remaining Accessibility

#### A11Y-005-008: Remaining Critical Accessibility (6 hours)
**Priority:** P0 - CRITICAL
**Files:** Multiple frontend files

**A11Y-005: Search Input Missing Label (2 hours)**
1. Find search input in `frontend/src/App.jsx` line 505-512
2. Add proper label (can be visually hidden):
   ```jsx
   <div className="search-container">
     <Label htmlFor="eds-search" className="sr-only">
       Search EDS files
     </Label>
     <input
       id="eds-search"
       type="text"
       placeholder="Search..."
     />
   </div>
   ```
3. Verify screen reader announces "Search EDS files" when focusing input

**A11Y-006: Sidebar Missing Landmark Role (1 hour)**
1. Change sidebar `<div>` to `<nav>`:
   ```jsx
   <nav aria-label="Main navigation" className="sidebar">
     {/* navigation items */}
   </nav>
   ```
2. Verify screen reader announces "Main navigation landmark"

**A11Y-007: Missing Page Titles & Heading Hierarchy (2 hours)**
1. Add proper semantic headings to all pages:
   ```jsx
   // Device List Page
   <main>
     <h1>Device Catalog</h1>
     <section>
       <h2>Filters</h2>
       ...
     </section>
     <section>
       <h2>Results</h2>
       {devices.map(device => (
         <article>
           <h3>{device.name}</h3>
           ...
         </article>
       ))}
     </section>
   </main>
   ```
2. Ensure all pages have exactly one `<h1>`
3. Ensure heading hierarchy doesn't skip levels (h1 → h2 → h3, not h1 → h3)
4. Replace styled div "headings" with actual semantic headings

**A11Y-008: Form Errors Not Announced (1 hour)**
1. Add to all form validation error messages:
   ```jsx
   {error && (
     <div role="alert" aria-live="assertive" className="error-message">
       {error}
     </div>
   )}
   ```
2. Ensure errors appear immediately when validation fails
3. **Test:** Submit invalid form, verify screen reader announces error

---

## WEEK 4: HIGH PRIORITY REFACTORING & TESTING

**Goal:** Major code refactoring and comprehensive testing
**Effort:** 84 hours (2 engineers × 42 hours each)
**Score Impact:** +8 points

### Day 16-17 (Monday-Tuesday) - greenstack.py Refactoring

#### CQ-002: Split greenstack.py into Modules (40 hours over 2 weeks)

**Week 4, Days 16-17 (16 hours):**

**Subtasks for Days 16-17:**
1. **Create Directory Structure:**
   ```
   src/
     models/         # Data models (12 classes)
       __init__.py
       device.py
       parameter.py
       process_data.py
       variable.py
       event.py
       menu.py
     parsing/        # IODD parsing (8 classes)
       __init__.py
       iodd_parser.py
       xml_validator.py
       schema_handler.py
       namespace_resolver.py
     storage/        # Database operations (9 classes - done in CQ-001)
     generation/     # Document generation (4 classes)
       __init__.py
       pdf_generator.py
       markdown_generator.py
       html_generator.py
       node_red_generator.py
     api/            # API routes (split into modules)
       __init__.py
       iodd_routes.py
       device_routes.py
       auth_routes.py
   ```
2. **Day 16 Morning: Extract Models (4 hours)**
   - Move all dataclass definitions to `src/models/`
   - Create `DeviceProfile` in `models/device.py`
   - Create `Parameter` in `models/parameter.py`
   - Create `ProcessData` in `models/process_data.py`
   - Update imports in `greenstack.py`
   - Run tests to verify no breakage
3. **Day 16 Afternoon: Extract Parsers Part 1 (4 hours)**
   - Move `IODDParser` class to `parsing/iodd_parser.py`
   - Move XML validation logic to `parsing/xml_validator.py`
   - Extract namespace handling to `parsing/namespace_resolver.py`
   - Update imports
   - Run parser tests
4. **Day 17 Morning: Extract Generators (4 hours)**
   - Move PDF generation to `generation/pdf_generator.py`
   - Move Markdown generation to `generation/markdown_generator.py`
   - Move HTML generation to `generation/html_generator.py`
   - Move Node-RED generation to `generation/node_red_generator.py`
   - Update imports
5. **Day 17 Afternoon: Extract API Routes (4 hours)**
   - Split routes into separate files by resource
   - Create `api/iodd_routes.py` with IODD upload/parse endpoints
   - Create `api/device_routes.py` with device CRUD endpoints
   - Create `api/auth_routes.py` with authentication endpoints
   - Update main `greenstack.py` to import and register routes
   - Test all endpoints still work

**Remaining 24 hours for CQ-002 will be in Week 5**

### Day 18 (Wednesday) - End-to-End Testing

#### TEST-002: Create End-to-End Test Suite (16 hours)
**Priority:** P1
**Files:** NEW - `e2e/tests/*.spec.js`

**Subtasks:**
1. Install Playwright: `npm install -D @playwright/test`
2. Create `playwright.config.js`:
   ```javascript
   export default {
     testDir: './e2e/tests',
     use: {
       baseURL: 'http://localhost:3000',
       screenshot: 'only-on-failure',
       video: 'retain-on-failure',
     },
   };
   ```
3. Create test scenarios:

**Critical User Flows (20 E2E tests):**
   - `test_01_user_registration.spec.js`:
     - Register new account
     - Verify email sent (if applicable)
     - Activate account
     - Login with new credentials

   - `test_02_device_upload.spec.js`:
     - Login as admin
     - Navigate to upload page
     - Select IODD file
     - Upload and wait for parsing
     - Verify success message
     - Verify device appears in catalog

   - `test_03_device_search.spec.js`:
     - Navigate to device catalog
     - Enter search term "valve"
     - Verify results filtered
     - Click on device
     - Verify details page loads

   - `test_04_parameter_editing.spec.js`:
     - Open device details
     - Navigate to parameters tab
     - Edit parameter description
     - Save changes
     - Verify changes persisted

   - `test_05_documentation_generation.spec.js`:
     - Select device
     - Click "Generate PDF"
     - Wait for generation
     - Verify download starts
     - Verify PDF contains device info

   - `test_06_iot_dashboard.spec.js`:
     - Navigate to IoT dashboard
     - Verify Grafana iframe loads
     - Verify telemetry data visible

   - `test_07_user_permissions.spec.js`:
     - Login as regular user (not admin)
     - Verify cannot access admin functions
     - Verify cannot upload IODD
     - Verify can view devices (read-only)

4. Create page object models for maintainability:
   ```javascript
   // e2e/pages/LoginPage.js
   export class LoginPage {
     constructor(page) {
       this.page = page;
       this.usernameInput = page.locator('#username');
       this.passwordInput = page.locator('#password');
       this.loginButton = page.locator('button[type="submit"]');
     }

     async login(username, password) {
       await this.usernameInput.fill(username);
       await this.passwordInput.fill(password);
       await this.loginButton.click();
     }
   }
   ```
5. Add to CI pipeline:
   ```yaml
   - name: E2E Tests
     run: |
       docker-compose up -d
       npm run test:e2e
   ```
6. **Test:** All 20 E2E tests pass

### Day 19-20 (Thursday-Friday) - Node-RED Adapter Generation

#### IOT-002: Implement Node-RED Flow Generation (40 hours over 2 weeks)

**Week 4, Days 19-20 (16 hours):**

**Subtasks for Days 19-20:**
1. **Day 19 Morning: Flow Format Research (4 hours)**
   - Study Node-RED flow JSON format
   - Analyze example flows in `config/nodered/flows.json`
   - Document required structure for:
     - MQTT input nodes
     - Function nodes (data processing)
     - Switch nodes (routing)
     - MQTT output nodes
     - Debug nodes
   - Create flow template structure

2. **Day 19 Afternoon: Flow Generator Core (4 hours)**
   - Create `src/generation/nodered/flow_generator.py`:
     ```python
     from typing import List, Dict
     from ..models import DeviceProfile, Parameter

     class FlowGenerator:
         """Generate Node-RED flows from IODD device profile"""

         def __init__(self, profile: DeviceProfile):
             self.profile = profile
             self.node_counter = 0

         def generate_flow(self) -> Dict:
             """Generate complete flow JSON"""
             nodes = []
             nodes.extend(self._create_input_nodes())
             nodes.extend(self._create_processing_nodes())
             nodes.extend(self._create_output_nodes())

             return {
                 "id": self._generate_id(),
                 "type": "tab",
                 "label": f"{self.profile.device_name} Flow",
                 "nodes": nodes
             }

         def _create_input_nodes(self) -> List[Dict]:
             """Create MQTT input nodes for telemetry"""
             return [{
                 "id": self._generate_id(),
                 "type": "mqtt in",
                 "name": f"{self.profile.device_name} Telemetry",
                 "topic": f"devices/{self.profile.device_id}/telemetry",
                 "qos": "2",
                 "broker": "${MQTT_BROKER_ID}",
             }]
     ```

3. **Day 20 Morning: Parameter Processing Logic (4 hours)**
   - Implement `_create_processing_nodes()`:
     ```python
     def _create_processing_nodes(self) -> List[Dict]:
         """Create function nodes for each parameter"""
         nodes = []

         for param in self.profile.parameters:
             # Create function node to extract and validate parameter
             func_code = self._generate_parameter_function(param)
             nodes.append({
                 "id": self._generate_id(),
                 "type": "function",
                 "name": f"Process {param.name}",
                 "func": func_code,
             })

             # Create switch node for threshold checking
             if param.min_value or param.max_value:
                 nodes.append(self._create_threshold_node(param))

         return nodes

     def _generate_parameter_function(self, param: Parameter) -> str:
         """Generate JavaScript function code for parameter extraction"""
         return f'''
         // Extract {param.name} from payload
         var value = msg.payload.{param.name};

         // Validate data type
         if (typeof value !== '{param.data_type.lower()}') {{
             node.error("Invalid data type for {param.name}");
             return null;
         }}

         // Apply scaling if needed
         var scaled = value * {param.scaling_factor or 1};

         msg.payload = {{
             parameter: "{param.name}",
             value: scaled,
             unit: "{param.unit_code}",
             timestamp: new Date().toISOString()
         }};

         return msg;
         '''
     ```

4. **Day 20 Afternoon: Alert & Output Nodes (4 hours)**
   - Implement threshold checking:
     ```python
     def _create_threshold_node(self, param: Parameter) -> Dict:
         """Create switch node for threshold alerts"""
         rules = []

         if param.min_value:
             rules.append({
                 "t": "lt",
                 "v": str(param.min_value),
                 "vt": "num"
             })

         if param.max_value:
             rules.append({
                 "t": "gt",
                 "v": str(param.max_value),
                 "vt": "num"
             })

         return {
             "id": self._generate_id(),
             "type": "switch",
             "name": f"{param.name} Thresholds",
             "property": "payload.value",
             "rules": rules
         }
     ```
   - Implement output nodes (InfluxDB, alerts)
   - Wire all nodes together with connections
   - **Test:** Generate flow for sample IODD, verify valid JSON

**Remaining 24 hours for IOT-002 will be in Week 5**

---

## WEEK 5: COMPLETE P1 REFACTORING

**Goal:** Complete major refactoring tasks and high-priority features
**Effort:** 80 hours (2 engineers × 40 hours each)
**Score Impact:** +6 points

### Day 21-22 (Monday-Tuesday) - Complete greenstack.py Split

**CQ-002 Continued (24 hours):**

**Subtasks:**
1. **Day 21: Create Comprehensive Tests (8 hours)**
   - Test each module in isolation:
     - `tests/unit/test_models.py` (20+ tests)
     - `tests/unit/test_parsing.py` (30+ tests)
     - `tests/unit/test_generation.py` (25+ tests)
   - Test integration between modules
   - Achieve 90%+ coverage on new modules
   - Fix any issues found

2. **Day 21-22: Update All Imports (8 hours)**
   - Find all occurrences of imports from `greenstack.py`
   - Update to new module paths
   - Use IDE refactoring tool to avoid manual errors:
     ```python
     # Old
     from greenstack import DeviceProfile, IODDParser

     # New
     from src.models.device import DeviceProfile
     from src.parsing.iodd_parser import IODDParser
     ```
   - Run full test suite after each batch of changes
   - Fix any broken imports or circular dependencies

3. **Day 22: Final Cleanup (8 hours)**
   - Verify `greenstack.py` is now just main application setup:
     - FastAPI app creation
     - Middleware configuration
     - Route registration
     - Database initialization
     - Should be ~300-400 lines (down from 3,219)
   - Update documentation to reflect new structure
   - Create architecture diagram showing module relationships
   - Update CONTRIBUTING.md with new code organization
   - Run full test suite one final time
   - **Test:** All 300+ tests pass, application works identically

### Day 23-24 (Wednesday-Thursday) - Complete Node-RED Generation

**IOT-002 Continued (24 hours):**

**Subtasks:**
1. **Day 23 Morning: Package Generation (4 hours)**
   - Implement `_generate_package_json()`:
     ```python
     def _generate_package_json(self) -> Dict:
         """Generate Node-RED node package.json"""
         safe_name = re.sub(r'[^a-z0-9-]', '-', self.profile.device_name.lower())

         return {
             "name": f"node-red-contrib-{safe_name}",
             "version": "1.0.0",
             "description": f"Node-RED nodes for {self.profile.device_name}",
             "keywords": ["node-red", "io-link", self.profile.vendor_name],
             "node-red": {
                 "nodes": {
                     f"{safe_name}": f"nodes/{safe_name}.js"
                 }
             },
             "dependencies": {
                 "mqtt": "^4.3.0",
                 "influx": "^5.9.0"
             }
         }
     ```

2. **Day 23 Afternoon: Node Configuration UI (4 hours)**
   - Generate HTML configuration for each node type
   - Create configuration form for MQTT broker connection
   - Create configuration form for parameter selection
   - Add help documentation to UI:
     ```python
     def _generate_node_html(self) -> str:
         """Generate Node-RED node configuration HTML"""
         return f'''
         <script type="text/x-red" data-template-name="{self.node_name}">
             <div class="form-row">
                 <label for="node-input-parameter">Parameter</label>
                 <select id="node-input-parameter">
                     {self._generate_parameter_options()}
                 </select>
             </div>
             <div class="form-row">
                 <label for="node-input-broker">MQTT Broker</label>
                 <input type="text" id="node-input-broker">
             </div>
         </script>

         <script type="text/x-red" data-help-name="{self.node_name}">
             <p>Processes telemetry for {self.profile.device_name}</p>
             <h3>Parameters:</h3>
             <ul>
                 {self._generate_parameter_help()}
             </ul>
         </script>
         '''
     ```

3. **Day 24 Morning: Flow Export & Deployment (4 hours)**
   - Create API endpoint to export flows:
     ```python
     @app.post("/api/devices/{device_id}/generate-nodered")
     async def generate_nodered_flow(device_id: int):
         device = get_device_profile(device_id)
         generator = FlowGenerator(device)

         flow = generator.generate_flow()
         package = generator.generate_package()

         # Create ZIP archive
         zip_buffer = create_zip({
             "flows.json": json.dumps(flow, indent=2),
             "package.json": json.dumps(package, indent=2),
             f"nodes/{device.device_name}.js": generator.generate_node_code(),
             f"nodes/{device.device_name}.html": generator.generate_node_html(),
         })

         return StreamingResponse(
             zip_buffer,
             media_type="application/zip",
             headers={"Content-Disposition": f"attachment; filename={device.device_name}-nodered.zip"}
         )
     ```
   - Test flow export via API
   - Create frontend button to trigger generation

4. **Day 24 Afternoon: Integration & Testing (4 hours)**
   - Test generated flows in actual Node-RED instance
   - Import generated package
   - Deploy flows
   - Verify MQTT messages processed correctly
   - Verify parameter extraction works
   - Verify threshold alerts trigger
   - Document usage instructions
   - **Test:** Complete E2E flow from IODD → Node-RED generation → deployment → data processing

### Day 25 (Friday) - Performance Optimization

#### PERF-001: Implement Background Job Queue (16 hours over 2 days)

**Day 25 (8 hours):**

**Subtasks:**
1. **Morning: Celery Setup (4 hours)**
   - Add to `requirements.txt`:
     ```
     celery[redis]==5.3.4
     redis==5.0.1
     ```
   - Create `src/tasks/__init__.py`:
     ```python
     from celery import Celery

     celery_app = Celery(
         'greenstack',
         broker=os.getenv('CELERY_BROKER_URL', 'redis://localhost:6379/1'),
         backend=os.getenv('CELERY_RESULT_BACKEND', 'redis://localhost:6379/1')
     )

     celery_app.conf.update(
         task_serializer='json',
         accept_content=['json'],
         result_serializer='json',
         timezone='UTC',
         enable_utc=True,
         task_track_started=True,
         task_time_limit=3600,  # 1 hour max
     )
     ```
   - Add Celery worker to `docker-compose.yml`:
     ```yaml
     celery-worker:
       build: .
       command: celery -A src.tasks worker --loglevel=info
       depends_on:
         - redis
       environment:
         - CELERY_BROKER_URL=redis://redis:6379/1
     ```

2. **Afternoon: Convert IODD Parsing to Background Task (4 hours)**
   - Create `src/tasks/iodd_tasks.py`:
     ```python
     from .celery import celery_app
     from ..parsing.iodd_parser import IODDParser
     from ..storage import StorageManager

     @celery_app.task(bind=True, name='parse_iodd_file')
     def parse_iodd_file(self, file_path: str, filename: str) -> dict:
         """Background task to parse IODD file"""
         try:
             self.update_state(state='PROGRESS', meta={'status': 'Parsing XML...'})

             parser = IODDParser()
             profile = parser.parse_file(file_path)

             self.update_state(state='PROGRESS', meta={'status': 'Saving to database...'})

             storage = StorageManager()
             device_id = storage.save_device(profile)

             return {
                 'status': 'success',
                 'device_id': device_id,
                 'device_name': profile.device_name
             }
         except Exception as e:
             return {'status': 'error', 'message': str(e)}
     ```
   - Update upload endpoint:
     ```python
     @app.post("/api/iodd/upload")
     async def upload_iodd(file: UploadFile):
         # Save file temporarily
         temp_path = f"/tmp/{file.filename}"
         with open(temp_path, "wb") as f:
             f.write(await file.read())

         # Queue parsing task
         task = parse_iodd_file.delay(temp_path, file.filename)

         return {
             "task_id": task.id,
             "status": "processing",
             "message": "IODD file is being parsed in the background"
         }

     @app.get("/api/iodd/status/{task_id}")
     def get_task_status(task_id: str):
         task = parse_iodd_file.AsyncResult(task_id)
         return {
             "task_id": task_id,
             "state": task.state,
             "result": task.result if task.ready() else None,
             "meta": task.info
         }
     ```
   - Update frontend to poll for task completion
   - **Test:** Upload large IODD, verify non-blocking, verify completion notification

**Remaining 8 hours for PERF-001 in Week 6**

---

## WEEK 6: COMPLETE HIGH PRIORITY ITEMS

**Goal:** Finish all P1 items, bringing score to 92/100
**Effort:** 72 hours (2 engineers × 36 hours each)
**Score Impact:** +8 points (Total after Week 6: 92/100 - PRODUCTION READY)

### Day 26 (Monday) - Complete Background Jobs

**PERF-001 Continued (8 hours):**

**Subtasks:**
1. **Morning: Add More Background Tasks (4 hours)**
   - Create task for PDF generation:
     ```python
     @celery_app.task(name='generate_pdf_documentation')
     def generate_pdf_documentation(device_id: int) -> dict:
         device = get_device_profile(device_id)
         generator = PDFGenerator(device)
         pdf_path = generator.generate()
         return {'status': 'success', 'pdf_path': pdf_path}
     ```
   - Create task for Node-RED generation
   - Create task for documentation export
   - Update all relevant endpoints to use tasks

2. **Afternoon: Monitoring & Retries (4 hours)**
   - Add Celery monitoring with Flower:
     ```yaml
     flower:
       image: mher/flower:2.0
       command: celery --broker=redis://redis:6379/1 flower
       ports:
         - "5555:5555"
     ```
   - Configure automatic retries:
     ```python
     @celery_app.task(bind=True, max_retries=3)
     def parse_iodd_file(self, ...):
         try:
             # ... parsing logic ...
         except Exception as exc:
             raise self.retry(exc=exc, countdown=60)  # Retry after 1 min
     ```
   - Add task timeout handling
   - Add dead letter queue for failed tasks
   - **Test:** Verify tasks retry on failure, eventually move to DLQ

### Day 27 (Tuesday) - Caching Layer

#### PERF-002: Implement Redis Caching (8 hours)
**Priority:** P1
**Files:** `src/cache.py`, all API routes

**Subtasks:**
1. **Morning: Cache Infrastructure (4 hours)**
   - Create `src/cache.py`:
     ```python
     import redis
     import json
     from functools import wraps

     redis_client = redis.Redis(
         host=os.getenv('REDIS_HOST', 'localhost'),
         port=6379,
         db=0,  # DB 0 for cache (DB 1 for Celery)
         decode_responses=True
     )

     def cached(ttl: int = 300):
         """Decorator to cache function results"""
         def decorator(func):
             @wraps(func)
             def wrapper(*args, **kwargs):
                 # Generate cache key from function name + args
                 cache_key = f"{func.__name__}:{hash(str(args) + str(kwargs))}"

                 # Try to get from cache
                 cached_result = redis_client.get(cache_key)
                 if cached_result:
                     return json.loads(cached_result)

                 # Execute function
                 result = func(*args, **kwargs)

                 # Store in cache
                 redis_client.setex(cache_key, ttl, json.dumps(result))

                 return result
             return wrapper
         return decorator
     ```

2. **Afternoon: Apply Caching to Hot Paths (4 hours)**
   - Cache device list (5 min TTL):
     ```python
     @cached(ttl=300)
     def get_all_devices():
         return db.query(Device).all()
     ```
   - Cache device details (15 min TTL):
     ```python
     @cached(ttl=900)
     def get_device_by_id(device_id: int):
         return db.query(Device).filter(Device.id == device_id).first()
     ```
   - Cache parameters (15 min TTL)
   - Cache search results (5 min TTL)
   - Add cache invalidation on updates:
     ```python
     @app.put("/api/devices/{device_id}")
     def update_device(device_id: int, data: dict):
         # Update database
         result = db.update(...)

         # Invalidate cache
         redis_client.delete(f"get_device_by_id:{device_id}")
         redis_client.delete("get_all_devices:*")

         return result
     ```
   - **Test:** Verify cache hits via Redis MONITOR, verify 10-50x speedup on cached endpoints

### Day 28 (Wednesday) - Database & Security Hardening

#### DB-002: Set Up Database Replication (12 hours)
**Priority:** P1
**Files:** `docker-compose.yml`, PostgreSQL configuration

**Subtasks:**
1. **Morning: Configure Primary Database (4 hours)**
   - Update `docker-compose.yml` for primary database:
     ```yaml
     postgres-primary:
       image: postgres:16-alpine
       environment:
         - POSTGRES_USER=${POSTGRES_USER}
         - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
         - POSTGRES_DB=${POSTGRES_DB}
       volumes:
         - postgres-primary-data:/var/lib/postgresql/data
         - ./config/postgres/postgresql.conf:/etc/postgresql/postgresql.conf
       command: postgres -c 'config_file=/etc/postgresql/postgresql.conf'
     ```
   - Create `config/postgres/postgresql.conf`:
     ```
     wal_level = replica
     max_wal_senders = 3
     wal_keep_size = 64
     ```
   - Create replication user:
     ```sql
     CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replication_password';
     ```

2. **Afternoon: Configure Replica Database (4 hours)**
   - Add replica to docker-compose:
     ```yaml
     postgres-replica:
       image: postgres:16-alpine
       environment:
         - POSTGRES_USER=${POSTGRES_USER}
         - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
       volumes:
         - postgres-replica-data:/var/lib/postgresql/data
       command: >
         bash -c "
         rm -rf /var/lib/postgresql/data/*
         pg_basebackup -h postgres-primary -D /var/lib/postgresql/data -U replicator -v -P -W
         touch /var/lib/postgresql/data/standby.signal
         postgres
         "
     ```
   - Configure streaming replication
   - Verify replication lag monitoring

3. **Evening: Application Read/Write Split (4 hours)**
   - Update `src/database.py` to use read replicas:
     ```python
     from sqlalchemy import create_engine
     from sqlalchemy.orm import sessionmaker

     # Primary for writes
     primary_engine = create_engine(DATABASE_URL)
     PrimarySession = sessionmaker(bind=primary_engine)

     # Replica for reads
     replica_url = os.getenv('DATABASE_REPLICA_URL', DATABASE_URL)
     replica_engine = create_engine(replica_url)
     ReplicaSession = sessionmaker(bind=replica_engine)

     def get_read_session():
         """Use replica for read-only queries"""
         return ReplicaSession()

     def get_write_session():
         """Use primary for writes"""
         return PrimarySession()
     ```
   - Update all GET endpoints to use replica
   - Keep POST/PUT/DELETE on primary
   - **Test:** Verify writes go to primary, reads from replica

#### SEC-006: Implement Rate Limiting (4 hours)
**Priority:** P1
**Files:** `src/api.py`, `requirements.txt`

**Subtasks:**
1. Add slowapi: `pip install slowapi==0.1.9`
2. Configure rate limiter:
   ```python
   from slowapi import Limiter, _rate_limit_exceeded_handler
   from slowapi.util import get_remote_address
   from slowapi.errors import RateLimitExceeded

   limiter = Limiter(key_func=get_remote_address)
   app.state.limiter = limiter
   app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
   ```
3. Apply to endpoints:
   ```python
   @app.post("/api/iodd/upload")
   @limiter.limit("5/minute")  # Max 5 uploads per minute
   async def upload_iodd(request: Request, file: UploadFile):
       pass

   @app.get("/api/devices")
   @limiter.limit("100/minute")  # Max 100 reads per minute
   async def get_devices(request: Request):
       pass
   ```
4. Add bypass for authenticated admin users
5. **Test:** Exceed rate limit, verify 429 Too Many Requests response

### Day 29 (Thursday) - TypeScript Migration Start

#### TYPE-001: Add Return Type Hints to API Routes (8 hours)
**Priority:** P1
**Files:** `src/routes/*.py`

**Subtasks:**
1. **Morning: Create Response Models (4 hours)**
   - Create Pydantic response models:
     ```python
     from pydantic import BaseModel
     from typing import List, Optional

     class DeviceResponse(BaseModel):
         id: int
         device_id: int
         vendor_name: str
         device_name: str
         release_date: Optional[str]

         class Config:
             from_attributes = True

     class DeviceListResponse(BaseModel):
         devices: List[DeviceResponse]
         total: int
         page: int
         per_page: int
     ```
   - Create response models for all major DTOs
   - Create error response models

2. **Afternoon: Add Type Hints to Routes (4 hours)**
   - Add return types to all endpoints:
     ```python
     @app.get("/api/devices", response_model=DeviceListResponse)
     async def get_devices(
         page: int = 1,
         per_page: int = 50
     ) -> DeviceListResponse:
         devices = db.query(Device).offset((page-1)*per_page).limit(per_page).all()
         total = db.query(Device).count()

         return DeviceListResponse(
             devices=devices,
             total=total,
             page=page,
             per_page=per_page
         )
     ```
   - Update all 60+ endpoints
   - Verify OpenAPI schema improved
   - **Test:** Access /docs, verify all responses documented

#### TYPE-002: Begin TypeScript Migration (20 hours over multiple weeks)

**Day 29 Continued (8 hours):**

**Subtasks:**
1. **Afternoon: TypeScript Configuration (2 hours)**
   - Update `tsconfig.json`:
     ```json
     {
       "compilerOptions": {
         "target": "ES2020",
         "useDefineForClassFields": true,
         "lib": ["ES2020", "DOM", "DOM.Iterable"],
         "module": "ESNext",
         "skipLibCheck": true,
         "strict": true,
         "noUnusedLocals": true,
         "noUnusedParameters": true,
         "noFallthroughCasesInSwitch": true
       }
     }
     ```
   - Configure Vite for TypeScript
   - Add TypeScript ESLint rules

2. **Evening: Create Type Definitions (6 hours)**
   - Create `src/types/api.ts`:
     ```typescript
     export interface Device {
       id: number;
       device_id: number;
       vendor_name: string;
       device_name: string;
       release_date?: string;
     }

     export interface Parameter {
       id: number;
       index: number;
       name: string;
       description?: string;
       data_type: string;
       access: string;
     }

     export interface DeviceListResponse {
       devices: Device[];
       total: number;
       page: number;
       per_page: number;
     }
     ```
   - Create type definitions for all API responses
   - Create type definitions for component props
   - Generate types from OpenAPI schema if possible

**Remaining 12 hours for TYPE-002 in Week 7**

### Day 30 (Friday) - Accessibility Completion

#### A11Y-010 to A11Y-025: Remaining High-Priority Accessibility (16 hours over 2 days)

**Day 30 (8 hours):**

**Subtasks:**
1. **A11Y-010: NavItem aria-current (1 hour)**
   ```jsx
   <a
     href={item.path}
     aria-current={currentPath === item.path ? 'page' : undefined}
   >
     {item.label}
   </a>
   ```

2. **A11Y-011: Select Dropdowns Accessible Names (2 hours)**
   - Add labels to all select elements:
   ```jsx
   <div className="form-group">
     <Label htmlFor="ticket-priority">Priority</Label>
     <select id="ticket-priority" name="priority">
       <option value="low">Low</option>
       <option value="medium">Medium</option>
       <option value="high">High</option>
     </select>
   </div>
   ```

3. **A11Y-012: Skip Navigation Link (2 hours)**
   - Add skip link at top of App.jsx:
   ```jsx
   <a href="#main-content" className="skip-link">
     Skip to main content
   </a>

   {/* ... navigation ... */}

   <main id="main-content">
     {/* page content */}
   </main>
   ```
   - Style skip link to be visible only on focus:
   ```css
   .skip-link {
     position: absolute;
     top: -40px;
     left: 0;
     background: #000;
     color: #fff;
     padding: 8px;
     z-index: 100;
   }
   .skip-link:focus {
     top: 0;
   }
   ```

4. **A11Y-013: Loading States Announced (2 hours)**
   ```jsx
   {loading && (
     <div role="status" aria-live="polite" aria-busy={loading}>
       <span className="sr-only">Loading devices...</span>
       <Spinner />
     </div>
   )}
   ```

5. **A11Y-014: Table Headers (1 hour)**
   - Add proper `<thead>` and `<th>` with scope:
   ```jsx
   <table>
     <thead>
       <tr>
         <th scope="col">Device Name</th>
         <th scope="col">Vendor</th>
         <th scope="col">Parameters</th>
       </tr>
     </thead>
     <tbody>
       {devices.map(device => (
         <tr key={device.id}>
           <td>{device.name}</td>
           <td>{device.vendor}</td>
           <td>{device.paramCount}</td>
         </tr>
       ))}
     </tbody>
   </table>
   ```

**Remaining 8 hours + 8 more A11Y items in Week 7**

---

## WEEK 7-8: COMPLETE P2 OPTIMIZATION & REMAINING ITEMS

**Goal:** Achieve 95/100 score (enterprise-grade)
**Effort:** 80 hours total (2 engineers × 2 weeks)
**Score Impact:** +3 points

### Remaining Tasks for Week 7-8:

#### CQ-003: Split App.jsx into 70+ Components (48 hours)
**Priority:** P0 (highest impact on maintainability)
**Files:** `frontend/src/App.jsx` → `frontend/src/components/`, `pages/`, `features/`

**Detailed breakdown:**
1. **Extract Page Components (16 hours)**
   - Create `pages/DeviceListPage.jsx`
   - Create `pages/DeviceDetailsPage.jsx` (currently 4,054 lines!)
   - Create `pages/UploadPage.jsx`
   - Create `pages/SettingsPage.jsx`
   - Create `pages/DashboardPage.jsx`

2. **Extract Feature Components (16 hours)**
   - Create `features/device-details/ParametersTab.jsx`
   - Create `features/device-details/ProcessDataTab.jsx`
   - Create `features/device-details/DiagnosticsTab.jsx`
   - Create `features/device-details/DocumentationTab.jsx`
   - Create `features/device-list/DeviceCard.jsx`
   - Create `features/device-list/FilterPanel.jsx`

3. **Extract UI Components (16 hours)**
   - Create `components/common/Modal.jsx`
   - Create `components/common/Button.jsx`
   - Create `components/common/Input.jsx`
   - Create `components/common/Select.jsx`
   - Create `components/layout/Sidebar.jsx`
   - Create `components/layout/Header.jsx`

#### TYPE-002 Continued: TypeScript Migration (12 hours)
- Convert 20 most critical components to .tsx
- Add prop types
- Fix all type errors

#### Remaining Accessibility Fixes (8 hours)
- Complete A11Y-015 through A11Y-025

#### CI/CD Improvements (12 hours)
- CICD-003: Publish IoT services to GHCR (6h)
- CICD-004: Expand Python linting coverage (1h)
- CICD-005: Add container security scanning (2h)
- CICD-002: Implement automated releases (3h)

#### Production Hardening (12 hours)
- PROD-009: Add Docker resource limits (2h)
- PROD-010: Configure log rotation (1h)
- PROD-012: Add request timeouts (2h)
- IOT-003: Implement circuit breakers (12h)

#### Additional Monitoring (12 hours)
- MON-004: Add distributed tracing (6h)
- MON-005: Set up centralized logging (6h)

#### Performance (12 hours)
- PERF-003: Fix N+1 queries (2h)
- PERF-004: Set up CDN (4h)
- PERF-005: Implement code splitting (6h)

---

## SUMMARY: PATH TO 100%

### Realistic Timeline to Production Ready (92/100):

| Week | Focus | Score Progress | Status |
|------|-------|----------------|--------|
| **Week 1** | Critical Security & Blockers | 52 → 67 (+15) | P0 Started |
| **Week 2** | Production Infrastructure | 67 → 78 (+11) | Pilot Ready |
| **Week 3** | Remaining P0 Items | 78 → 84 (+6) | P0 Complete |
| **Week 4** | Refactoring & Testing | 84 → 88 (+4) | Major Improvements |
| **Week 5** | Complete P1 Refactoring | 88 → 92 (+4) | **PRODUCTION READY** |
| **Week 6** | High Priority Features | 92 → 94 (+2) | Enhanced |
| **Week 7-8** | Optimization & Polish | 94 → 95 (+1) | Enterprise Grade |

### After 8 Weeks (P0 + P1 Complete):

**Overall Score:** 92-95/100 (Grade: A)

**Category Scores:**
- Code Quality: 90/100 ✅
- Security: 95/100 ✅
- Testing: 90/100 ✅
- Performance: 90/100 ✅
- Monitoring: 95/100 ✅
- Deployment: 90/100 ✅
- Accessibility: 95/100 ✅
- IoT Integration: 90/100 ✅

### Total Effort Breakdown:

- **P0 Critical:** 280 hours (Weeks 1-3)
- **P1 High Priority:** 320 hours (Weeks 4-6)
- **P2 Optimization:** 200 hours (Weeks 7-8)
- **TOTAL:** 800 hours

**With 2 Engineers:** 8 weeks to 95/100
**With 3 Engineers:** 5-6 weeks to 95/100

---

## Quick Reference: Priority Hierarchy

### Must Fix (P0) - 15 Items - 280 hours
Production blockers that prevent deployment

### Should Fix (P1) - 28 Items - 320 hours
High impact on quality, security, and performance

### Nice to Have (P2) - 45 Items - 400 hours
Optimization and polish for enterprise grade

### Total: 88 Items - 1,000 hours

---

**This comprehensive action plan provides a clear path from the current 52/100 score to a production-ready 92/100 score in 6 weeks, or an enterprise-grade 95/100 in 8 weeks.**
