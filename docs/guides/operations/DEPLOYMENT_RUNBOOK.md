# GreenStack Deployment Runbook

**Version:** 2.0.1
**Last Updated:** 2025-11-18
**Maintained By:** DevOps Team

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Pre-Deployment Checklist](#pre-deployment-checklist)
3. [Step-by-Step Deployment](#step-by-step-deployment)
4. [Post-Deployment Verification](#post-deployment-verification)
5. [Rollback Procedure](#rollback-procedure)
6. [Common Deployment Issues](#common-deployment-issues)
7. [Environment-Specific Notes](#environment-specific-notes)

---

## Prerequisites

### Server Requirements

#### Minimum Hardware Specifications
- **CPU:** 4 cores (8+ recommended for production)
- **RAM:** 8 GB (16+ GB recommended for production)
- **Storage:** 50 GB SSD (100+ GB for production with data retention)
- **Network:** 100 Mbps connection (1 Gbps recommended)

#### Software Requirements
- **Operating System:** Ubuntu 20.04 LTS or newer / RHEL 8+ / Debian 11+
- **Docker:** Version 24.0+ ([Install Guide](https://docs.docker.com/engine/install/))
- **Docker Compose:** Version 2.20+ (included with Docker)
- **Git:** Version 2.30+
- **OpenSSL:** For certificate and secret generation

#### Network Requirements
- **DNS:** Fully qualified domain name (FQDN) configured
- **Ports Required:**
  - `80/443` - HTTP/HTTPS (Frontend & API)
  - `8000` - API Server (if not behind reverse proxy)
  - `3000` - Grafana Dashboard
  - `1880` - Node-RED (optional)
  - `1883/8883` - MQTT (standard/TLS)
  - `9090` - Prometheus (internal monitoring)
  - `8086` - InfluxDB (time-series data)

#### SSL/TLS Certificates
- Valid SSL certificates for HTTPS
- Or Let's Encrypt setup for automatic certificate management
- MQTT TLS certificates (can be self-signed for development)

---

## Pre-Deployment Checklist

### 1. Security Configuration ✓

- [ ] Generate all required secrets using `./scripts/generate-secrets.sh`
- [ ] Store secrets securely in `.env.production` file
- [ ] Set file permissions: `chmod 600 .env.production`
- [ ] Verify secrets are excluded from version control (`.gitignore`)
- [ ] Backup secrets in secure password manager (1Password, Vault, etc.)

**Generate Secrets:**
```bash
cd /opt/greenstack
./scripts/generate-secrets.sh > .env.production
chmod 600 .env.production
```

**Verify Secrets Generated:**
```bash
grep -E "^(SECRET_KEY|POSTGRES_PASSWORD|REDIS_PASSWORD|MQTT_PASSWORD|INFLUXDB_TOKEN)=" .env.production | wc -l
# Should output: 5 (or more depending on services)
```

### 2. Environment Configuration ✓

- [ ] Copy `.env.example` to `.env.production`
- [ ] Set `ENVIRONMENT=production`
- [ ] Set `DEBUG=false`
- [ ] Configure production database URL (PostgreSQL recommended)
- [ ] Set proper CORS origins (no wildcards!)
- [ ] Configure `API_HOST` and `API_PORT`
- [ ] Set data retention policies (`INFLUXDB_RETENTION`)

**Critical Environment Variables:**
```bash
ENVIRONMENT=production
DEBUG=false
DATABASE_URL=postgresql://user:password@postgres:5432/greenstack
CORS_ORIGINS=https://greenstack.example.com
LOG_TO_FILE=true
ENABLE_METRICS=true
```

### 3. Database Setup ✓

- [ ] PostgreSQL database created
- [ ] Database user with appropriate permissions
- [ ] Database connection tested from application server
- [ ] Backup strategy configured
- [ ] Connection pooling limits set (default: 20/40)

**Test Database Connection:**
```bash
docker exec -it greenstack-postgres psql -U iodd_user -d greenstack -c "SELECT version();"
```

### 4. DNS & Networking ✓

- [ ] Domain name resolves to server IP
- [ ] Firewall rules configured
- [ ] Reverse proxy configured (Nginx/Traefik)
- [ ] SSL certificates installed and validated
- [ ] Load balancer health checks configured (if applicable)

**Verify DNS:**
```bash
dig +short greenstack.example.com
# Should return your server's IP address
```

### 5. Backup Configuration ✓

- [ ] Backup storage configured (S3, Azure Blob, local NAS)
- [ ] Automated backup scripts tested
- [ ] Backup retention policy defined
- [ ] Restore procedure tested
- [ ] Monitoring for backup failures configured

### 6. Monitoring & Logging ✓

- [ ] Sentry DSN configured (`SENTRY_DSN`)
- [ ] Log aggregation configured (if using ELK, Datadog, etc.)
- [ ] Prometheus metrics enabled
- [ ] Grafana dashboards imported
- [ ] Alert rules configured
- [ ] On-call rotation defined

---

## Step-by-Step Deployment

### Phase 1: Initial Setup (30-45 minutes)

#### Step 1: Clone Repository
```bash
cd /opt
sudo git clone https://github.com/your-org/greenstack.git
cd greenstack
sudo chown -R $(whoami):$(whoami) .
```

**Verification:**
```bash
git log -1 --oneline
# Verify you're on the correct commit/tag
```

#### Step 2: Checkout Specific Version
```bash
# For tagged release
git checkout tags/v2.0.1

# Or specific commit
# git checkout <commit-hash>
```

**Verification:**
```bash
git describe --tags
# Should show: v2.0.1
```

#### Step 3: Configure Environment
```bash
# Copy production environment file
cp .env.production .env

# Generate secrets if not already done
./scripts/generate-secrets.sh >> .env
chmod 600 .env

# Verify critical variables are set
grep -E "^(ENVIRONMENT|DEBUG|SECRET_KEY|DATABASE_URL)" .env
```

**Verification:**
```bash
# Ensure no default/weak passwords
./scripts/generate-secrets.sh > /tmp/new-secrets.txt
diff <(grep SECRET_KEY .env) <(grep SECRET_KEY .env.example)
# Should show differences (not identical)
```

#### Step 4: Generate TLS Certificates (if not using Let's Encrypt)
```bash
# For MQTT
./scripts/generate-mqtt-certs.sh

# For InfluxDB (optional)
./scripts/generate-influxdb-certs.sh

# Verify certificates created
ls -lah config/mosquitto/certs/
ls -lah config/influxdb/certs/
```

**Verification:**
```bash
openssl x509 -in config/mosquitto/certs/server.crt -text -noout | grep "Not After"
# Verify expiration date is acceptable
```

### Phase 2: Database Initialization (10-20 minutes)

#### Step 5: Start Database Services
```bash
# Start only PostgreSQL and Redis first
docker-compose -f docker-compose.iot.yml up -d postgres redis

# Wait for services to be healthy
docker-compose -f docker-compose.iot.yml ps
```

**Verification:**
```bash
# Check PostgreSQL is ready
docker exec greenstack-postgres pg_isready -U iodd_user
# Output: /var/run/postgresql:5432 - accepting connections

# Check Redis is ready
docker exec greenstack-redis redis-cli ping
# Output: PONG
```

#### Step 6: Run Database Migrations
```bash
# Install Python dependencies
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Run migrations
alembic upgrade head
```

**Verification:**
```bash
# Check migration status
alembic current
# Should show latest migration

# Verify tables created
docker exec -it greenstack-postgres psql -U iodd_user -d greenstack -c "\dt"
```

### Phase 3: Application Deployment (20-30 minutes)

#### Step 7: Build Application Images
```bash
# Build backend
docker-compose build api

# Build frontend
docker-compose build frontend
```

**Verification:**
```bash
docker images | grep greenstack
# Should show freshly built images with recent timestamps
```

#### Step 8: Start Core Services
```bash
# Start API and Frontend
docker-compose up -d api frontend

# Monitor logs for errors
docker-compose logs -f api frontend
```

**Verification:**
```bash
# Check API health
curl http://localhost:8000/api/health
# Should return: {"status":"healthy","database":"connected",...}

# Check frontend accessible
curl -I http://localhost:3000
# Should return: HTTP/1.1 200 OK
```

#### Step 9: Start IoT Platform Services
```bash
# Start MQTT, InfluxDB, Grafana, Node-RED, Prometheus
docker-compose -f docker-compose.iot.yml up -d mosquitto influxdb grafana nodered prometheus

# Wait for all services to be healthy
sleep 30
docker-compose -f docker-compose.iot.yml ps
```

**Verification:**
```bash
# Check each service
curl http://localhost:8086/health  # InfluxDB
curl http://localhost:3000/api/health  # Grafana
curl http://localhost:1880  # Node-RED
curl http://localhost:9090/-/healthy  # Prometheus
```

#### Step 10: Configure Reverse Proxy
```bash
# Example Nginx configuration
sudo cp deployment/nginx/greenstack.conf /etc/nginx/sites-available/
sudo ln -s /etc/nginx/sites-available/greenstack.conf /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

**Verification:**
```bash
# Test HTTPS access
curl -I https://greenstack.example.com
# Should return: HTTP/2 200

# Verify SSL certificate
echo | openssl s_client -connect greenstack.example.com:443 2>/dev/null | openssl x509 -noout -dates
```

### Phase 4: Data & Configuration (10-15 minutes)

#### Step 11: Import Initial Data (if applicable)
```bash
# Import IODD library
docker exec -it greenstack-api python -m src.scripts.import_iodd_library

# Or restore from backup
docker exec -i greenstack-postgres psql -U iodd_user greenstack < backup/greenstack_backup.sql
```

**Verification:**
```bash
# Verify data imported
curl http://localhost:8000/api/iodd/devices | jq '. | length'
# Should show count of devices
```

#### Step 12: Configure Monitoring Dashboards
```bash
# Import Grafana dashboards
curl -X POST -H "Content-Type: application/json" \
  -d @config/grafana/dashboards/greenstack-overview.json \
  http://admin:${GRAFANA_ADMIN_PASSWORD}@localhost:3000/api/dashboards/db
```

**Verification:**
```bash
# Verify dashboard created
curl http://admin:${GRAFANA_ADMIN_PASSWORD}@localhost:3000/api/search | jq '.[] | select(.title=="GreenStack Overview")'
```

---

## Post-Deployment Verification

### Automated Health Checks

Run the automated health check script:
```bash
./scripts/healthcheck.sh
```

### Manual Verification Steps

#### 1. Application Health ✓
```bash
# API health endpoint
curl https://greenstack.example.com/api/health | jq .
# Expected: {"status":"healthy","database":"connected",...}

# Prometheus metrics
curl https://greenstack.example.com/metrics | grep http_requests_total

# Database pool status
curl https://greenstack.example.com/api/health/db-pool | jq .
```

#### 2. Service Connectivity ✓
```bash
# Test IODD file upload
curl -F "file=@test-data/iodd-files/sample.xml" \
  https://greenstack.example.com/api/iodd/upload

# Test MQTT connection
mosquitto_sub -h greenstack.example.com -p 8883 \
  --cafile config/mosquitto/certs/ca.crt \
  -u iodd -P ${MQTT_PASSWORD} -t test/topic
```

#### 3. Authentication & Authorization ✓
```bash
# Test API authentication (if enabled)
curl -X POST https://greenstack.example.com/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"username":"admin","password":"changeme"}'
```

#### 4. Performance Baseline ✓
```bash
# Run load test
ab -n 1000 -c 10 https://greenstack.example.com/api/iodd/devices

# Check response times in Prometheus
# Query: histogram_quantile(0.95, http_request_duration_seconds)
```

#### 5. Security Validation ✓
```bash
# Verify production security validation runs
docker logs greenstack-api 2>&1 | grep "PRODUCTION SECURITY VALIDATION"
# Should show: ✅ All security credentials validated

# Check for weak passwords
docker exec greenstack-api python -c "from src.config import validate_production_security; validate_production_security()"
```

#### 6. Monitoring & Alerts ✓
```bash
# Trigger test alert
curl -X POST https://greenstack.example.com/api/test/error

# Verify Sentry received error
# Check Sentry dashboard at sentry.io

# Check Prometheus targets
curl http://localhost:9090/api/v1/targets | jq '.data.activeTargets[] | {job:.labels.job, health:.health}'
```

### Smoke Test Checklist

- [ ] Homepage loads successfully
- [ ] User can log in (if auth enabled)
- [ ] Device catalog displays correctly
- [ ] IODD file upload works
- [ ] Parameter configuration functions
- [ ] Adapter code generation works
- [ ] Grafana dashboards display data
- [ ] MQTT pub/sub functional
- [ ] Logs are being written
- [ ] Metrics are being collected

---

## Rollback Procedure

### When to Rollback

Rollback immediately if:
- **Critical bugs** affecting core functionality
- **Data corruption** or loss detected
- **Security vulnerabilities** discovered
- **Performance degradation** > 50%
- **Service unavailability** > 5 minutes

### Quick Rollback (5-10 minutes)

#### Step 1: Stop Current Services
```bash
cd /opt/greenstack
docker-compose down
docker-compose -f docker-compose.iot.yml down
```

#### Step 2: Checkout Previous Version
```bash
# Find previous tag
git tag -l | sort -V | tail -2

# Checkout previous version
git checkout tags/v2.0.0  # Replace with your previous version
```

#### Step 3: Restore Environment Configuration
```bash
# Restore previous .env file from backup
cp .env.production.backup .env
```

#### Step 4: Rollback Database (if necessary)
```bash
# Check if database changes were made
alembic current

# Downgrade to previous migration
alembic downgrade -1

# Or restore from backup
docker exec -i greenstack-postgres psql -U iodd_user greenstack < backup/greenstack_backup_pre_deployment.sql
```

**Verification:**
```bash
alembic current
# Should show previous migration
```

#### Step 5: Restart Services
```bash
docker-compose up -d
docker-compose -f docker-compose.iot.yml up -d
```

#### Step 6: Verify Rollback Success
```bash
# Check API version
curl https://greenstack.example.com/api/health | jq '.app_version'
# Should show previous version

# Run smoke tests
./scripts/smoke-test.sh
```

### Full Rollback with Data Restore (30-60 minutes)

If database corruption or data loss occurred:

```bash
# 1. Stop all services
docker-compose down --volumes  # This will remove volumes!

# 2. Restore database from backup
./scripts/restore-backup.sh backup/greenstack_backup_YYYYMMDD_HHMMSS.tar.gz

# 3. Restore uploaded files
tar -xzf backup/uploads_YYYYMMDD_HHMMSS.tar.gz -C ./iodd_storage/

# 4. Restart services with previous version
git checkout tags/v2.0.0
docker-compose up -d
```

---

## Common Deployment Issues

### Issue 1: Database Connection Failed

**Symptoms:**
- API health check returns "unhealthy"
- Logs show: `sqlalchemy.exc.OperationalError: could not connect to server`

**Diagnosis:**
```bash
# Check PostgreSQL is running
docker ps | grep postgres

# Check connection from API container
docker exec greenstack-api nc -zv postgres 5432
```

**Solutions:**
```bash
# Verify DATABASE_URL is correct
grep DATABASE_URL .env

# Restart PostgreSQL
docker-compose -f docker-compose.iot.yml restart postgres

# Check PostgreSQL logs
docker logs greenstack-postgres
```

### Issue 2: Port Already in Use

**Symptoms:**
- Docker Compose fails to start
- Error: `Bind for 0.0.0.0:8000 failed: port is already allocated`

**Diagnosis:**
```bash
# Find process using port 8000
sudo lsof -i :8000
# Or
sudo netstat -tulpn | grep :8000
```

**Solutions:**
```bash
# Kill the process
sudo kill <PID>

# Or change port in .env
echo "API_PORT=8001" >> .env
```

### Issue 3: SSL Certificate Errors

**Symptoms:**
- Browser shows "Not Secure"
- Curl shows: `SSL certificate problem: self signed certificate`

**Diagnosis:**
```bash
# Check certificate validity
openssl s_client -connect greenstack.example.com:443 -servername greenstack.example.com
```

**Solutions:**
```bash
# Renew Let's Encrypt certificate
sudo certbot renew

# Or regenerate self-signed certificates
./scripts/generate-mqtt-certs.sh
```

### Issue 4: Out of Memory

**Symptoms:**
- Containers restarting frequently
- Logs show: `MemoryError` or `OOMKilled`

**Diagnosis:**
```bash
# Check memory usage
docker stats

# Check container memory limits
docker inspect greenstack-api | grep -A 10 "Memory"
```

**Solutions:**
```bash
# Increase Docker memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G

# Or increase host memory
# Add swap space if needed
sudo fallocate -l 4G /swapfile
sudo chmod 600 /swapfile
sudo mkswap /swapfile
sudo swapon /swapfile
```

### Issue 5: MQTT Connection Refused

**Symptoms:**
- Devices cannot connect to MQTT broker
- Error: `Connection refused` on port 1883 or 8883

**Diagnosis:**
```bash
# Test MQTT connection
mosquitto_sub -h localhost -p 1883 -t test/topic

# Check Mosquitto logs
docker logs greenstack-mosquitto
```

**Solutions:**
```bash
# Verify Mosquitto is running
docker ps | grep mosquitto

# Check password file exists
docker exec greenstack-mosquitto cat /mosquitto/config/passwd

# Regenerate password file
docker exec greenstack-mosquitto mosquitto_passwd -c -b /mosquitto/config/passwd iodd ${MQTT_PASSWORD}
docker restart greenstack-mosquitto
```

### Issue 6: Grafana Dashboard Not Loading

**Symptoms:**
- Grafana shows "No data"
- Dashboards don't display metrics

**Diagnosis:**
```bash
# Check Grafana can reach Prometheus
curl http://localhost:9090/api/v1/query?query=up

# Check InfluxDB datasource
curl http://admin:${GRAFANA_ADMIN_PASSWORD}@localhost:3000/api/datasources
```

**Solutions:**
```bash
# Restart Grafana
docker restart greenstack-grafana

# Re-provision datasources
docker exec greenstack-grafana grafana-cli admin reset-admin-password ${GRAFANA_ADMIN_PASSWORD}

# Verify InfluxDB token
echo $INFLUXDB_TOKEN
```

---

## Environment-Specific Notes

### Development Environment
- Use SQLite for database (faster setup)
- Self-signed certificates acceptable
- Debug mode enabled
- Auto-reload enabled
- Log to console

### Staging Environment
- Mirror production setup
- Use production-like data (sanitized)
- Test all deployment steps
- Enable debug logging temporarily
- Use separate Sentry project

### Production Environment
- PostgreSQL required
- Valid SSL certificates required
- Debug mode disabled
- Log to file with rotation
- Connection pooling enabled
- Automated backups configured
- Monitoring and alerting active

---

## Additional Resources

- **Troubleshooting Guide:** `docs/guides/TROUBLESHOOTING.md`
- **Disaster Recovery & Backups:** `docs/guides/operations/DISASTER_RECOVERY.md`
- **Monitoring Guide:** `docs/guides/operations/MONITORING_SETUP_GUIDE.md`
- **Security Hardening Checklist:** `docs/audits/PHASE_11_CONFIGURATION_REVIEW_REPORT.md`
- **API Documentation:** https://greenstack.example.com/docs

---

## Deployment Checklist Summary

```
Pre-Deployment:
☐ Generate secrets
☐ Configure environment variables
☐ Test database connection
☐ Verify DNS and SSL
☐ Configure backups

Deployment:
☐ Clone repository
☐ Checkout version
☐ Start database
☐ Run migrations
☐ Build images
☐ Start services
☐ Configure reverse proxy

Post-Deployment:
☐ Verify health checks
☐ Test core functionality
☐ Verify monitoring
☐ Run smoke tests
☐ Document deployment

Rollback Ready:
☐ Previous version tagged
☐ Database backup available
☐ Rollback procedure tested
☐ Team notified
```

---

**Document Version:** 1.0
**Last Reviewed:** 2025-11-18
**Next Review:** 2025-12-18
