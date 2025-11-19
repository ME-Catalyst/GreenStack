# GreenStack Disaster Recovery Plan

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Owner:** Infrastructure Team
**Review Cycle:** Quarterly

---

## Table of Contents

1. [Executive Summary](#executive-summary)
2. [Recovery Objectives](#recovery-objectives)
3. [Disaster Scenarios](#disaster-scenarios)
4. [Contact Information](#contact-information)
5. [Pre-Disaster Preparation](#pre-disaster-preparation)
6. [Recovery Procedures](#recovery-procedures)
7. [Testing & Validation](#testing--validation)
8. [Post-Recovery Activities](#post-recovery-activities)
9. [Appendices](#appendices)

---

## Executive Summary

This Disaster Recovery (DR) plan provides comprehensive procedures for recovering the GreenStack IO-DD Management Platform following various disaster scenarios. The plan ensures business continuity, data integrity, and minimal service disruption.

### Scope

This DR plan covers:
- All production infrastructure components (API, database, cache, message broker, monitoring)
- Critical data assets (PostgreSQL database, uploaded IODD files, generated outputs)
- Configuration and application code
- Docker volumes and persistent storage

### Out of Scope

- Individual developer workstations
- Third-party SaaS services (Sentry, cloud storage providers)
- Network infrastructure (DNS, load balancers) - see separate Network DR plan

---

## Recovery Objectives

### Recovery Time Objective (RTO)

**Target RTO: 4 hours** (from disaster declaration to service restoration)

| Component | RTO Target | Notes |
|-----------|------------|-------|
| Database (PostgreSQL) | 1 hour | Critical path - highest priority |
| API Server | 30 minutes | Quick to deploy, depends on database |
| MQTT Broker | 30 minutes | IoT communication priority |
| Redis Cache | 15 minutes | Can operate with cold cache |
| InfluxDB | 2 hours | Time-series data, lower priority |
| Grafana | 1 hour | Monitoring and dashboards |
| Node-RED | 2 hours | Automation workflows |
| Prometheus | 1 hour | Metrics collection |

### Recovery Point Objective (RPO)

**Target RPO: 24 hours** (maximum acceptable data loss)

| Data Type | RPO Target | Backup Frequency |
|-----------|------------|------------------|
| PostgreSQL Database | 24 hours | Daily (3:00 AM UTC) |
| IODD Storage Files | 24 hours | Daily (3:00 AM UTC) |
| Generated Outputs | 24 hours | Daily (3:00 AM UTC) |
| Configuration | 1 week | Weekly (Sunday 3:00 AM) |
| Docker Volumes | 24 hours | Daily (3:00 AM UTC) |
| Grafana Dashboards | 1 week | Weekly (with volumes) |
| Node-RED Flows | 1 week | Weekly (with volumes) |

**For Zero RPO Requirements:**
- Implement PostgreSQL streaming replication
- Use continuous backup solutions (WAL archiving)
- See Appendix C: High Availability Configuration

---

## Disaster Scenarios

### Scenario 1: Database Corruption

**Likelihood:** Medium
**Impact:** Critical
**Detection:** Application errors, data inconsistencies, failed queries

**Immediate Actions:**
1. Stop API server to prevent further corruption
2. Create emergency snapshot of current state
3. Assess corruption extent using PostgreSQL tools
4. Activate recovery procedure (see [Database Recovery](#database-recovery))

**Recovery Time:** 1-2 hours

---

### Scenario 2: Complete Server Failure

**Likelihood:** Low
**Impact:** Critical
**Detection:** Total service outage, server unreachable

**Immediate Actions:**
1. Declare disaster and activate DR team
2. Provision replacement server
3. Restore from backup to new server
4. Update DNS/load balancer to point to new server
5. Activate recovery procedure (see [Full System Recovery](#full-system-recovery))

**Recovery Time:** 3-4 hours

---

### Scenario 3: Data Center Outage

**Likelihood:** Very Low
**Impact:** Critical
**Detection:** Regional service outage, cloud provider alerts

**Immediate Actions:**
1. Declare disaster
2. Activate failover to secondary region (if configured)
3. Or provision infrastructure in alternate region
4. Restore from S3 backups to new infrastructure
5. Update DNS to point to new region

**Recovery Time:** 4-6 hours (without failover), 30 minutes (with automated failover)

---

### Scenario 4: Ransomware/Security Breach

**Likelihood:** Medium
**Impact:** Critical
**Detection:** Encryption notices, suspicious activity, security alerts

**Immediate Actions:**
1. **DO NOT pay ransom**
2. Isolate affected systems immediately
3. Activate incident response team
4. Engage security forensics
5. Restore from known-good backup (at least 7 days old)
6. Change all credentials before reconnecting to network

**Recovery Time:** 6-8 hours (includes security validation)

---

### Scenario 5: Accidental Data Deletion

**Likelihood:** Medium
**Impact:** Medium
**Detection:** User reports, missing data, audit logs

**Immediate Actions:**
1. Identify scope of deletion
2. Check if soft-delete/recycle bin available
3. If permanent deletion, restore from backup
4. Validate restored data integrity

**Recovery Time:** 30 minutes - 2 hours (depending on scope)

---

### Scenario 6: Configuration Error

**Likelihood:** High
**Impact:** Medium
**Detection:** Service degradation, application errors, failed health checks

**Immediate Actions:**
1. Identify configuration change that caused issue
2. Roll back to previous configuration
3. If rollback fails, restore configuration from backup
4. Review change management process

**Recovery Time:** 15-30 minutes

---

### Scenario 7: Storage Volume Failure

**Likelihood:** Medium
**Impact:** High
**Detection:** I/O errors, disk full alerts, mount failures

**Immediate Actions:**
1. Stop services using affected volume
2. Provision replacement volume
3. Restore Docker volume from backup
4. Restart services

**Recovery Time:** 1-3 hours

---

## Contact Information

### Primary DR Team

| Role | Name | Primary Contact | Secondary Contact | Escalation |
|------|------|----------------|-------------------|------------|
| DR Coordinator | [NAME] | [PHONE] | [EMAIL] | N/A |
| Infrastructure Lead | [NAME] | [PHONE] | [EMAIL] | DR Coordinator |
| Database Administrator | [NAME] | [PHONE] | [EMAIL] | Infrastructure Lead |
| Security Lead | [NAME] | [PHONE] | [EMAIL] | DR Coordinator |
| Application Lead | [NAME] | [PHONE] | [EMAIL] | Infrastructure Lead |

### Escalation Path

```
Level 1: On-call Engineer (respond within 15 minutes)
    ↓ (30 minutes, no resolution)
Level 2: Infrastructure Lead (respond within 30 minutes)
    ↓ (1 hour, no resolution)
Level 3: DR Coordinator (respond within 1 hour)
    ↓ (2 hours, no resolution)
Level 4: CTO / Executive Team
```

### External Contacts

| Vendor | Service | Support Contact | Account/Contract # |
|--------|---------|----------------|-------------------|
| Cloud Provider | Infrastructure | [SUPPORT URL] | [ACCOUNT ID] |
| Database Support | PostgreSQL Enterprise | [CONTACT] | [CONTRACT #] |
| Security Firm | Incident Response | [24/7 HOTLINE] | [CONTRACT #] |
| Backup Service | S3/Cloud Storage | [SUPPORT] | [ACCOUNT ID] |

---

## Pre-Disaster Preparation

### Backup Verification Checklist (Daily)

Run automated verification:

```bash
# 1. Verify latest backup exists
ls -lh backups/ | tail -5

# 2. Verify backup integrity
cd backups/
latest_backup=$(ls -t greenstack_backup_*.tar.gz | head -1)
tar -tzf "$latest_backup" > /dev/null && echo "✓ Backup archive is valid"

# 3. Verify backup size (should be > 10MB for production)
size=$(du -m "$latest_backup" | cut -f1)
if [ $size -gt 10 ]; then
    echo "✓ Backup size is reasonable: ${size}MB"
else
    echo "⚠ Backup size seems small: ${size}MB - investigate!"
fi

# 4. Verify S3 upload (if configured)
if [ -n "$BACKUP_S3_BUCKET" ]; then
    aws s3 ls "s3://$BACKUP_S3_BUCKET/greenstack/" --recursive | tail -5
fi

# 5. Run health check
./scripts/healthcheck.sh
```

**Expected Results:**
- Backup file created within last 24 hours
- Archive is valid (no corruption)
- Size is consistent with historical backups (±20%)
- S3 backup present (if configured)
- All health checks pass

**Alert Conditions:**
- No backup created in 24 hours → Page on-call engineer
- Backup size anomaly → Investigate immediately
- S3 upload failed → Retry and escalate if continues
- Health check failures → Investigate per standard procedures

---

### Infrastructure as Code (IaC) Preparation

Ensure all infrastructure is defined in code:

```bash
# 1. Verify docker-compose files are version controlled
git status docker-compose*.yml

# 2. Verify configuration files are backed up
ls -la config/

# 3. Verify scripts are executable and version controlled
ls -la scripts/

# 4. Document any manual infrastructure setup
# Update: Appendix B - Manual Infrastructure Checklist
```

---

### Credential Management

**Before Disaster:**
1. Store credentials in secure password manager (e.g., 1Password, LastPass Enterprise)
2. Ensure DR team has access to:
   - Database credentials
   - Cloud provider access keys
   - Docker registry credentials
   - SSL/TLS certificates
   - API keys for third-party services
3. Test credential access quarterly
4. Maintain offline encrypted backup of critical credentials

**Credential Inventory:**
```
- PostgreSQL: POSTGRES_PASSWORD
- Redis: REDIS_PASSWORD
- MQTT: MQTT_PASSWORD
- InfluxDB: INFLUXDB_TOKEN, INFLUXDB_ADMIN_PASSWORD
- Grafana: GRAFANA_ADMIN_PASSWORD
- Node-RED: NODERED_CREDENTIAL_SECRET
- Application: SECRET_KEY, JWT_SECRET_KEY
- Cloud: AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY
- Monitoring: SENTRY_DSN
```

---

### Documentation Requirements

Ensure these documents are accessible offline and in multiple locations:

- [ ] This Disaster Recovery Plan (PDF + printed copy)
- [ ] Deployment Runbook (`docs/guides/operations/DEPLOYMENT_RUNBOOK.md`)
- [ ] Architecture diagrams
- [ ] Network topology
- [ ] Backup procedures (`scripts/backup.sh`)
- [ ] Restore procedures (`scripts/restore.sh`)
- [ ] Health check procedures (`scripts/healthcheck.sh`)
- [ ] Contact lists (updated quarterly)

**Storage Locations:**
1. Git repository (primary)
2. Secure wiki/knowledge base
3. Encrypted USB drive (offline backup)
4. Printed binder in secure location
5. Cloud storage (separate from production infrastructure)

---

## Recovery Procedures

### Database Recovery

**When to Use:**
- Database corruption detected
- Accidental data deletion
- Failed migration/upgrade
- Need to restore to specific point in time

**Prerequisites:**
- PostgreSQL container is running
- Backup file is available and validated
- Database credentials are available

**Procedure:**

#### Step 1: Assess Current State (5 minutes)

```bash
# Check database connectivity
docker exec greenstack-postgres pg_isready -U iodd_user

# Check database size and table count
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
SELECT
    pg_size_pretty(pg_database_size('greenstack')) as db_size,
    (SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public') as table_count;
"

# Check for active connections
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "
SELECT datname, count(*)
FROM pg_stat_activity
WHERE datname = 'greenstack'
GROUP BY datname;
"
```

**Decision Point:**
- If database is accessible and data looks reasonable → Consider point-in-time recovery
- If database is corrupted or inaccessible → Proceed with full restore
- If only specific tables affected → Consider selective table restore

#### Step 2: Stop Application Services (2 minutes)

```bash
# Stop API to prevent new connections
docker-compose stop api

# Verify no active connections
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "
SELECT pg_terminate_backend(pid)
FROM pg_stat_activity
WHERE datname = 'greenstack' AND pid != pg_backend_pid();
"
```

#### Step 3: Create Emergency Snapshot (5 minutes)

**IMPORTANT:** Always create a snapshot before restore in case you need to recover recent data

```bash
# Create emergency backup
timestamp=$(date +%Y%m%d_%H%M%S)
emergency_dir="./backups/emergency_${timestamp}"
mkdir -p "$emergency_dir"

# Quick dump of current state
docker exec greenstack-postgres pg_dump \
    -U iodd_user \
    -d greenstack \
    --format=custom \
    --compress=9 \
    > "$emergency_dir/emergency_snapshot.dump"

echo "Emergency snapshot saved to: $emergency_dir"
```

#### Step 4: Select Backup to Restore (2 minutes)

```bash
# List available backups
ls -lth backups/greenstack_backup_*.tar.gz | head -10

# Extract backup information
backup_file="backups/greenstack_backup_20251118_030000.tar.gz"

# Verify backup integrity
tar -tzf "$backup_file" | grep -E "(postgres.dump|MANIFEST.txt)"

# Review manifest
tar -xzOf "$backup_file" */MANIFEST.txt | head -20
```

#### Step 5: Restore Database (10-20 minutes)

```bash
# Use automated restore script (recommended)
./scripts/restore.sh "$backup_file" --database-only --no-confirmation

# Or manual restore:
# 1. Extract backup
temp_dir="./restore_temp"
mkdir -p "$temp_dir"
tar -xzf "$backup_file" -C "$temp_dir"
extracted_dir=$(find "$temp_dir" -maxdepth 1 -type d -name "greenstack_backup_*" | head -1)

# 2. Drop and recreate database
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "DROP DATABASE IF EXISTS greenstack;"
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "CREATE DATABASE greenstack;"

# 3. Restore from dump
docker exec -i greenstack-postgres pg_restore \
    -U iodd_user \
    -d greenstack \
    --no-owner \
    --no-acl \
    --verbose \
    < "$extracted_dir/postgres.dump"

# 4. Cleanup
rm -rf "$temp_dir"
```

#### Step 6: Verify Restore (10 minutes)

```bash
# Check table count
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
SELECT COUNT(*) as table_count
FROM information_schema.tables
WHERE table_schema='public';
"

# Check critical tables have data
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
SELECT
    'devices' as table_name, COUNT(*) as row_count FROM devices
UNION ALL
SELECT 'iodd_files', COUNT(*) FROM iodd_files
UNION ALL
SELECT 'users', COUNT(*) FROM users;
"

# Verify database integrity
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
SELECT datname, pg_database_size(datname)
FROM pg_database
WHERE datname = 'greenstack';
"

# Check for any corruption
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
VACUUM ANALYZE;
"
```

**Verification Checklist:**
- [ ] Table count matches expected value
- [ ] Critical tables have data
- [ ] Database size is reasonable
- [ ] No corruption errors
- [ ] Foreign key constraints are valid

#### Step 7: Restart Services (5 minutes)

```bash
# Start API server
docker-compose up -d api

# Wait for startup
sleep 10

# Check health
curl -s http://localhost:8000/api/health | jq .

# Run comprehensive health check
./scripts/healthcheck.sh
```

#### Step 8: Smoke Testing (10 minutes)

```bash
# Test 1: User authentication
curl -X POST http://localhost:8000/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"your_password"}' | jq .

# Test 2: Device listing
curl -H "Authorization: Bearer $TOKEN" \
    http://localhost:8000/api/devices | jq .

# Test 3: IODD file retrieval
curl -H "Authorization: Bearer $TOKEN" \
    http://localhost:8000/api/iodd | jq .

# Test 4: Search functionality
curl -H "Authorization: Bearer $TOKEN" \
    "http://localhost:8000/api/devices/search?q=sensor" | jq .
```

**Expected Results:**
- Authentication successful
- Device list returns data
- IODD files accessible
- Search returns results

#### Step 9: Document Recovery (5 minutes)

Create incident report:

```bash
cat > "incident_reports/db_recovery_${timestamp}.md" <<EOF
# Database Recovery - $(date)

## Incident Details
- **Time Detected:** [TIME]
- **Time Declared:** [TIME]
- **Time Resolved:** [TIME]
- **Total Downtime:** [DURATION]

## Root Cause
[Description of what caused the need for recovery]

## Recovery Actions Taken
1. Stopped API services at [TIME]
2. Created emergency snapshot
3. Restored from backup: $backup_file
4. Verified restore at [TIME]
5. Restarted services at [TIME]

## Data Loss Assessment
- **RPO:** [e.g., "24 hours - last backup from 3:00 AM UTC"]
- **Records Lost:** [NUMBER or "None - within RPO"]
- **Business Impact:** [DESCRIPTION]

## Verification Results
- Table count: [NUMBER]
- Device records: [NUMBER]
- IODD files: [NUMBER]
- Users: [NUMBER]

## Lessons Learned
[What could be improved?]

## Follow-up Actions
- [ ] Review backup frequency
- [ ] Implement additional monitoring
- [ ] Update runbooks
- [ ] Train team on recovery procedures
EOF
```

**Total Recovery Time:** ~50 minutes (within 1-hour RTO)

---

### Full System Recovery

**When to Use:**
- Complete server failure
- Hardware failure
- Data center outage
- Migration to new infrastructure

**Prerequisites:**
- New server/infrastructure provisioned
- Backup files accessible (local or S3)
- DNS/networking configuration ready
- Credentials available

**Procedure:**

#### Step 1: Provision New Infrastructure (30-60 minutes)

**Cloud Provider (AWS EC2 Example):**

```bash
# Launch EC2 instance
aws ec2 run-instances \
    --image-id ami-xxxxxxxxx \
    --instance-type t3.xlarge \
    --key-name greenstack-production \
    --security-group-ids sg-xxxxxxxxx \
    --subnet-id subnet-xxxxxxxxx \
    --block-device-mappings '[
        {
            "DeviceName": "/dev/sda1",
            "Ebs": {
                "VolumeSize": 100,
                "VolumeType": "gp3",
                "Encrypted": true
            }
        }
    ]' \
    --tag-specifications 'ResourceType=instance,Tags=[{Key=Name,Value=greenstack-production}]'

# Get instance IP
instance_id="i-xxxxxxxxx"
public_ip=$(aws ec2 describe-instances \
    --instance-ids $instance_id \
    --query 'Reservations[0].Instances[0].PublicIpAddress' \
    --output text)

echo "New server IP: $public_ip"
```

**Bare Metal / VM:**
- Provision Ubuntu 22.04 LTS server
- Minimum: 4 CPU, 16GB RAM, 100GB SSD
- Configure networking and firewall

#### Step 2: Install Dependencies (15 minutes)

SSH into new server:

```bash
ssh ubuntu@$public_ip

# Update system
sudo apt update && sudo apt upgrade -y

# Install Docker
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER

# Install Docker Compose
sudo curl -L "https://github.com/docker/compose/releases/download/v2.24.0/docker-compose-$(uname -s)-$(uname -m)" \
    -o /usr/local/bin/docker-compose
sudo chmod +x /usr/local/bin/docker-compose

# Verify installations
docker --version
docker-compose --version

# Install additional tools
sudo apt install -y git curl wget jq postgresql-client redis-tools

# Log out and back in for group changes
exit
ssh ubuntu@$public_ip
```

#### Step 3: Clone Repository (5 minutes)

```bash
# Clone application repository
cd /opt
sudo git clone https://github.com/your-org/greenstack.git
sudo chown -R $USER:$USER greenstack
cd greenstack

# Checkout production branch/tag
git checkout production
# or
git checkout tags/v2.0.1
```

#### Step 4: Retrieve Backup (10-30 minutes)

**Option A: From S3**

```bash
# Configure AWS CLI
aws configure

# Download latest backup
mkdir -p backups
aws s3 cp s3://your-backup-bucket/greenstack/ backups/ --recursive

# Verify download
ls -lh backups/ | tail -5

# Get latest backup
latest_backup=$(ls -t backups/greenstack_backup_*.tar.gz | head -1)
echo "Latest backup: $latest_backup"
```

**Option B: From Offsite Storage**

```bash
# Transfer from backup server via SCP
scp backup-server:/backups/greenstack_backup_*.tar.gz ./backups/

# Or from USB/external drive
sudo mount /dev/sdb1 /mnt/backup
cp /mnt/backup/greenstack_backup_*.tar.gz ./backups/
sudo umount /mnt/backup
```

**Option C: From Network Storage**

```bash
# Mount NFS share
sudo mkdir -p /mnt/nfs
sudo mount backup-server:/exports/backups /mnt/nfs
cp /mnt/nfs/greenstack_backup_*.tar.gz ./backups/
sudo umount /mnt/nfs
```

#### Step 5: Configure Environment (15 minutes)

```bash
# Restore .env from password manager or secure storage
# NEVER restore .env from backup (contains redacted secrets)

# Copy template
cp .env.example .env

# Edit with actual credentials
nano .env

# Set critical variables:
# - ENVIRONMENT=production
# - DEBUG=False
# - SECRET_KEY=[from password manager]
# - JWT_SECRET_KEY=[from password manager]
# - POSTGRES_PASSWORD=[from password manager]
# - REDIS_PASSWORD=[from password manager]
# - MQTT_PASSWORD=[from password manager]
# - INFLUXDB_TOKEN=[from password manager]
# - GRAFANA_ADMIN_PASSWORD=[from password manager]

# Or use credential management tool
# ./scripts/load-credentials.sh --from-vault

# Secure permissions
chmod 600 .env

# Verify critical variables are set
grep -E "^(ENVIRONMENT|DEBUG|SECRET_KEY|DATABASE_URL)" .env
```

#### Step 6: Restore from Backup (30-45 minutes)

```bash
# Full system restore
./scripts/restore.sh "$latest_backup" --no-confirmation

# This will:
# 1. Extract backup archive
# 2. Restore PostgreSQL database
# 3. Restore IODD storage files
# 4. Restore generated outputs
# 5. Restore configuration
# 6. Restore Docker volumes
# 7. Verify checksums
# 8. Restart all services

# Monitor progress
tail -f /var/log/greenstack/restore.log
```

#### Step 7: Start Services (10 minutes)

```bash
# Start database and cache first
docker-compose -f docker-compose.iot.yml up -d postgres redis

# Wait for database to be ready
timeout 60 bash -c 'until docker exec greenstack-postgres pg_isready -U iodd_user; do sleep 2; done'

# Start message broker and time-series DB
docker-compose -f docker-compose.iot.yml up -d mosquitto influxdb

# Start application
docker-compose up -d api

# Start monitoring and visualization
docker-compose -f docker-compose.iot.yml up -d grafana prometheus nodered

# Verify all containers are running
docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
```

#### Step 8: Verify Recovery (20 minutes)

```bash
# Run comprehensive health check
./scripts/healthcheck.sh

# Check API health endpoint
curl -s http://localhost:8000/api/health | jq .

# Expected output:
# {
#   "status": "healthy",
#   "version": "2.0.1",
#   "database": "connected",
#   "redis": "connected",
#   "uptime": 120
# }

# Verify database
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
SELECT
    'devices' as table_name, COUNT(*) as row_count FROM devices
UNION ALL
SELECT 'iodd_files', COUNT(*) FROM iodd_files
UNION ALL
SELECT 'users', COUNT(*) FROM users
UNION ALL
SELECT 'parser_results', COUNT(*) FROM parser_results;
"

# Verify file storage
ls -lh iodd_storage/ | head -10
du -sh iodd_storage/

# Verify Docker volumes
docker volume ls | grep greenstack

# Test MQTT connectivity
mosquitto_pub -h localhost -p 1883 -u greenstack -P "$MQTT_PASSWORD" -t test -m "DR test"

# Test Redis
docker exec greenstack-redis redis-cli -a "$REDIS_PASSWORD" ping

# Test InfluxDB
curl -s http://localhost:8086/health
```

#### Step 9: Configure SSL/TLS Certificates (30 minutes)

**Option A: Let's Encrypt (Recommended for Production)**

```bash
# Install certbot
sudo apt install -y certbot

# Obtain certificates
sudo certbot certonly --standalone \
    -d greenstack.yourdomain.com \
    --email admin@yourdomain.com \
    --agree-tos \
    --non-interactive

# Configure nginx/reverse proxy with certificates
# See: Appendix C - SSL/TLS Configuration Checklist
```

**Option B: Use Existing Certificates**

```bash
# Copy certificates from secure storage
cp /secure/storage/greenstack.crt /opt/greenstack/certs/
cp /secure/storage/greenstack.key /opt/greenstack/certs/

# Set permissions
chmod 644 /opt/greenstack/certs/greenstack.crt
chmod 600 /opt/greenstack/certs/greenstack.key
```

#### Step 10: Update DNS (10 minutes)

**Update DNS Records:**

```bash
# Get new server IP
new_ip=$(curl -s http://ifconfig.me)
echo "New server IP: $new_ip"

# Update DNS via API (example with Cloudflare)
curl -X PUT "https://api.cloudflare.com/client/v4/zones/${ZONE_ID}/dns_records/${RECORD_ID}" \
    -H "Authorization: Bearer ${CF_API_TOKEN}" \
    -H "Content-Type: application/json" \
    --data "{\"type\":\"A\",\"name\":\"greenstack\",\"content\":\"${new_ip}\",\"ttl\":300}"

# Or update manually in DNS provider dashboard
```

**Verify DNS Propagation:**

```bash
# Check DNS resolution
dig greenstack.yourdomain.com +short

# Wait for TTL to expire (typically 5-15 minutes)
# Monitor with:
watch -n 10 "dig greenstack.yourdomain.com +short"
```

#### Step 11: End-to-End Testing (30 minutes)

```bash
# Test from external network (not from server itself)
export API_URL="https://greenstack.yourdomain.com"

# Test 1: API Health
curl -s $API_URL/api/health | jq .

# Test 2: User Login
TOKEN=$(curl -X POST $API_URL/api/auth/login \
    -H "Content-Type: application/json" \
    -d '{"username":"admin","password":"your_admin_password"}' | jq -r .access_token)

# Test 3: Device Listing
curl -H "Authorization: Bearer $TOKEN" $API_URL/api/devices | jq .

# Test 4: IODD Upload
curl -X POST $API_URL/api/iodd/upload \
    -H "Authorization: Bearer $TOKEN" \
    -F "file=@test_files/sample.iodd" | jq .

# Test 5: Parser Functionality
curl -H "Authorization: Bearer $TOKEN" \
    "$API_URL/api/parser/test?device_id=1234" | jq .

# Test 6: Search
curl -H "Authorization: Bearer $TOKEN" \
    "$API_URL/api/devices/search?q=temperature+sensor" | jq .

# Test 7: Grafana Dashboards
curl -s $API_URL:3000/api/health

# Test 8: MQTT Connectivity (from client)
mosquitto_pub -h greenstack.yourdomain.com -p 1883 \
    -u greenstack -P "$MQTT_PASSWORD" \
    -t test/recovery -m "Recovery test message"

# Monitor MQTT
mosquitto_sub -h greenstack.yourdomain.com -p 1883 \
    -u greenstack -P "$MQTT_PASSWORD" \
    -t test/#
```

#### Step 12: Monitor for Issues (2-24 hours)

```bash
# Set up monitoring dashboard
# Watch for:
# - Error rates
# - Response times
# - Resource usage
# - Application logs

# Tail application logs
docker logs -f greenstack-api

# Monitor error logs
docker logs --since 10m greenstack-api 2>&1 | grep -i "error\|exception"

# Check system resources
htop

# Monitor disk usage
df -h
docker system df

# Set up alerts
# - Configure Sentry error tracking
# - Configure Prometheus alerts
# - Configure health check monitoring
```

**Total Recovery Time:** 3-4 hours (within RTO)

---

### File Recovery (IODD Storage)

**When to Use:**
- Accidental file deletion
- File corruption
- Storage volume failure
- Need to restore specific files

**Procedure:**

```bash
# 1. Identify missing files
ls -la iodd_storage/

# 2. Extract only file backup from latest backup
backup_file="backups/greenstack_backup_20251118_030000.tar.gz"
temp_dir="./restore_temp"
mkdir -p "$temp_dir"
tar -xzf "$backup_file" -C "$temp_dir"

# 3. List files in backup
extracted_dir=$(find "$temp_dir" -maxdepth 1 -type d -name "greenstack_backup_*" | head -1)
tar -tzf "$extracted_dir/iodd_storage.tar.gz" | head -20

# 4. Restore specific file
tar -xzf "$extracted_dir/iodd_storage.tar.gz" -C . "iodd_storage/specific_file.iodd"

# 5. Or restore all files
tar -xzf "$extracted_dir/iodd_storage.tar.gz" -C .

# 6. Verify permissions
chown -R 1000:1000 iodd_storage/
chmod 755 iodd_storage/
find iodd_storage/ -type f -exec chmod 644 {} \;

# 7. Cleanup
rm -rf "$temp_dir"
```

**Selective File Restore:**

```bash
# Restore only files matching pattern
tar -xzf "$extracted_dir/iodd_storage.tar.gz" \
    -C . \
    --wildcards "iodd_storage/*sensor*.iodd"

# Restore to different location for comparison
tar -xzf "$extracted_dir/iodd_storage.tar.gz" \
    -C /tmp/restored_files/
```

---

### Configuration Recovery

**When to Use:**
- Configuration file corruption
- Bad configuration deployment
- Need to rollback configuration changes

**Procedure:**

```bash
# 1. Extract configuration from backup
backup_file="backups/greenstack_backup_20251118_030000.tar.gz"
temp_dir="./restore_temp"
tar -xzf "$backup_file" -C "$temp_dir"
extracted_dir=$(find "$temp_dir" -maxdepth 1 -type d -name "greenstack_backup_*" | head -1)

# 2. Review current configuration
ls -la config/
git diff config/

# 3. Backup current configuration before restore
timestamp=$(date +%Y%m%d_%H%M%S)
tar -czf "config_backup_${timestamp}.tar.gz" config/

# 4. Restore configuration
tar -xzf "$extracted_dir/config.tar.gz" -C .

# 5. Compare configurations
diff -r "config/" "/tmp/old_config/"

# 6. Restart affected services
docker-compose restart api grafana prometheus

# 7. Verify services
./scripts/healthcheck.sh
```

---

### Docker Volume Recovery

**When to Use:**
- Volume corruption
- Accidental volume deletion
- Need to restore Grafana dashboards, Node-RED flows, etc.

**Procedure:**

```bash
# List available volumes in backup
backup_file="backups/greenstack_backup_20251118_030000.tar.gz"
tar -tzf "$backup_file" | grep -E "\.tar\.gz$"

# Restore specific volume (e.g., Grafana)
./scripts/restore.sh "$backup_file" --skip-database --skip-files

# Or manual volume restore:
# 1. Stop service using the volume
docker-compose -f docker-compose.iot.yml stop grafana

# 2. Extract backup
temp_dir="./restore_temp"
tar -xzf "$backup_file" -C "$temp_dir"
extracted_dir=$(find "$temp_dir" -maxdepth 1 -type d -name "greenstack_backup_*" | head -1)

# 3. Remove old volume
docker volume rm greenstack_grafana-data

# 4. Create new volume
docker volume create greenstack_grafana-data

# 5. Restore data to volume
docker run --rm \
    -v greenstack_grafana-data:/data \
    -v "$(pwd)/${extracted_dir}:/backup:ro" \
    alpine \
    sh -c "cd /data && tar -xzf /backup/grafana-data.tar.gz"

# 6. Restart service
docker-compose -f docker-compose.iot.yml up -d grafana

# 7. Verify restoration
docker logs greenstack-grafana
curl -s http://localhost:3000/api/health
```

---

### Point-in-Time Recovery (PITR)

**When to Use:**
- Need to restore to specific point in time
- Data corruption occurred at known time
- Requires PostgreSQL WAL archiving

**Prerequisites:**
- WAL archiving configured (see Appendix C)
- Base backup available
- WAL archives available

**Procedure:**

```bash
# 1. Stop PostgreSQL
docker-compose -f docker-compose.iot.yml stop postgres

# 2. Backup current data directory
docker run --rm \
    -v greenstack_postgres-data:/data \
    -v "$(pwd)/emergency_backup:/backup" \
    alpine \
    tar -czf /backup/postgres_emergency_$(date +%Y%m%d_%H%M%S).tar.gz -C /data .

# 3. Remove current data
docker volume rm greenstack_postgres-data
docker volume create greenstack_postgres-data

# 4. Restore base backup
docker run --rm \
    -v greenstack_postgres-data:/data \
    -v "$(pwd)/backups:/backup:ro" \
    alpine \
    sh -c "cd /data && tar -xzf /backup/postgres_base_backup.tar.gz"

# 5. Create recovery configuration
cat > recovery.conf <<EOF
restore_command = 'cp /wal_archive/%f %p'
recovery_target_time = '2025-11-18 14:30:00'
recovery_target_action = 'promote'
EOF

# 6. Copy recovery.conf to data directory
docker run --rm \
    -v greenstack_postgres-data:/data \
    -v "$(pwd)/recovery.conf:/recovery.conf:ro" \
    alpine \
    cp /recovery.conf /data/recovery.conf

# 7. Start PostgreSQL (will replay WAL to target time)
docker-compose -f docker-compose.iot.yml up -d postgres

# 8. Monitor recovery
docker logs -f greenstack-postgres | grep recovery

# 9. Verify recovery target
docker exec greenstack-postgres psql -U iodd_user -d greenstack -c "
SELECT pg_last_xact_replay_timestamp();
"

# 10. Resume normal operations
docker-compose up -d
```

**Note:** PITR requires continuous WAL archiving to be configured in advance. See Appendix C for setup instructions.

---

## Testing & Validation

### Quarterly DR Test (Every 3 Months)

**Objective:** Validate recovery procedures and train team

**Schedule:**
- Q1: January 15
- Q2: April 15
- Q3: July 15
- Q4: October 15

**Test Procedure:**

#### Phase 1: Preparation (1 week before)

```bash
# 1. Notify stakeholders
# 2. Schedule test window (non-business hours recommended)
# 3. Verify latest backups are available
# 4. Review DR plan for updates
# 5. Assign roles to team members
```

#### Phase 2: Test Execution (4-6 hours)

```bash
# Scenario: Simulate complete data center failure

# 1. Document current production state
./scripts/healthcheck.sh > "dr_test_$(date +%Y%m%d)_before.txt"

# 2. Take final backup before test
./scripts/backup.sh

# 3. Provision test recovery environment
# (separate from production)

# 4. Execute full system recovery to test environment
./scripts/restore.sh "backups/greenstack_backup_*.tar.gz"

# 5. Verify recovery
./scripts/healthcheck.sh > "dr_test_$(date +%Y%m%d)_after.txt"

# 6. Compare before/after states
diff dr_test_*_before.txt dr_test_*_after.txt

# 7. Run smoke tests
# 8. Measure recovery time vs RTO
# 9. Document any issues encountered
# 10. Decommission test environment
```

#### Phase 3: Post-Test Review (1 week after)

```bash
# 1. Create test report
cat > "dr_test_reports/dr_test_$(date +%Y%m%d).md" <<EOF
# DR Test Report - $(date)

## Test Details
- **Date:** $(date)
- **Type:** Full System Recovery Test
- **Environment:** Test/Staging
- **Team:** [List participants]

## Objectives
- Validate recovery procedures
- Measure recovery time
- Train team on DR processes

## Results
- **Actual RTO:** [TIME]
- **Target RTO:** 4 hours
- **RPO Achieved:** [TIME]
- **Success Criteria Met:** [YES/NO]

## Issues Encountered
1. [Issue description]
   - Impact: [HIGH/MEDIUM/LOW]
   - Resolution: [How it was resolved]

## Improvements Identified
1. [Improvement]
2. [Improvement]

## Action Items
- [ ] Update DR plan with lessons learned
- [ ] Fix identified issues
- [ ] Update training materials
- [ ] Schedule next test

## Recommendations
[Recommendations for improving DR processes]

## Sign-off
- DR Coordinator: [NAME] [DATE]
- Infrastructure Lead: [NAME] [DATE]
EOF
```

#### Phase 4: Update Procedures (Within 2 weeks)

- Update DR plan based on lessons learned
- Fix any issues discovered during test
- Update contact lists
- Retrain team on updated procedures

---

### Backup Validation Test (Monthly)

**Objective:** Verify backups are restorable

**Procedure:**

```bash
#!/bin/bash
# Monthly Backup Validation Test

set -e

echo "=== Monthly Backup Validation Test ==="
date

# 1. Select latest backup
latest_backup=$(ls -t backups/greenstack_backup_*.tar.gz | head -1)
echo "Testing backup: $latest_backup"

# 2. Verify archive integrity
echo "Verifying archive integrity..."
tar -tzf "$latest_backup" > /dev/null && echo "✓ Archive is valid"

# 3. Extract to temp location
echo "Extracting backup..."
temp_dir="/tmp/backup_test_$(date +%Y%m%d_%H%M%S)"
mkdir -p "$temp_dir"
tar -xzf "$latest_backup" -C "$temp_dir"

# 4. Verify contents
extracted_dir=$(find "$temp_dir" -maxdepth 1 -type d -name "greenstack_backup_*" | head -1)

echo "Verifying backup contents..."
required_files=(
    "postgres.dump"
    "postgres.sql"
    "MANIFEST.txt"
    "checksums.sha256"
    "iodd_storage.tar.gz"
    "config.tar.gz"
)

for file in "${required_files[@]}"; do
    if [ -f "$extracted_dir/$file" ]; then
        echo "✓ $file present"
    else
        echo "✗ $file MISSING"
        exit 1
    fi
done

# 5. Verify checksums
echo "Verifying checksums..."
(cd "$extracted_dir" && sha256sum -c checksums.sha256 2>/dev/null)

if [ $? -eq 0 ]; then
    echo "✓ Checksums valid"
else
    echo "✗ Checksum verification FAILED"
    exit 1
fi

# 6. Test database restore to temp database
echo "Testing database restore..."
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "DROP DATABASE IF EXISTS test_restore;"
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "CREATE DATABASE test_restore;"

docker exec -i greenstack-postgres pg_restore \
    -U iodd_user \
    -d test_restore \
    --no-owner \
    --no-acl \
    < "$extracted_dir/postgres.dump"

# 7. Verify restored data
table_count=$(docker exec greenstack-postgres psql -U iodd_user -d test_restore -t -c \
    "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';")

echo "Restored table count: $table_count"

if [ "$table_count" -gt 0 ]; then
    echo "✓ Database restore successful"
else
    echo "✗ Database restore FAILED"
    exit 1
fi

# 8. Cleanup
docker exec greenstack-postgres psql -U iodd_user -d postgres -c "DROP DATABASE test_restore;"
rm -rf "$temp_dir"

echo "=== Backup Validation Complete ==="
echo "Result: SUCCESS"
date
```

**Automated Execution:**

```bash
# Add to crontab for monthly execution (1st of each month at 2 AM)
0 2 1 * * /opt/greenstack/scripts/validate-backup.sh >> /var/log/greenstack/backup-validation.log 2>&1
```

---

### Restore Performance Baseline

Establish baseline recovery times for capacity planning:

| Component | Data Size | Restore Time | Notes |
|-----------|-----------|--------------|-------|
| PostgreSQL (10GB) | 10GB | 15 minutes | Custom format, parallel restore |
| PostgreSQL (50GB) | 50GB | 45 minutes | Estimate: 1GB/minute |
| PostgreSQL (100GB) | 100GB | 90 minutes | Estimate: 1GB/minute |
| IODD Storage (5GB) | 5GB | 5 minutes | Compressed tar extraction |
| IODD Storage (20GB) | 20GB | 15 minutes | Estimate: 1GB/minute |
| Docker Volumes | 10GB total | 20 minutes | All volumes combined |
| Full System (10GB) | 25GB total | 50 minutes | All components |
| Full System (50GB) | 100GB total | 2.5 hours | All components |

**Test annually and update this table**

---

## Post-Recovery Activities

### Incident Report

Within 24 hours of recovery, complete incident report:

```markdown
# Incident Report: [TITLE]

## Executive Summary
[1-2 paragraph summary of incident and resolution]

## Timeline
| Time (UTC) | Event |
|------------|-------|
| 14:00 | Issue detected |
| 14:05 | On-call engineer alerted |
| 14:10 | Incident declared |
| 14:15 | DR team assembled |
| 14:30 | Recovery initiated |
| 16:00 | Services restored |
| 16:30 | Verification complete |
| 17:00 | Incident closed |

**Total Downtime:** 3 hours

## Root Cause Analysis
### What Happened
[Detailed description of what went wrong]

### Why It Happened
[Root cause - technical, process, human error, etc.]

### Why It Wasn't Detected Earlier
[What monitoring/alerting we were missing]

## Impact Assessment
### Service Impact
- API: 100% down for 3 hours
- User-facing features: Complete outage
- Data loss: None (RPO: 24 hours, within acceptable range)

### Business Impact
- Users affected: [NUMBER]
- Transactions lost: [NUMBER]
- Revenue impact: $[AMOUNT]
- SLA breach: [YES/NO]

### Data Integrity
- Records lost: [NUMBER] (within RPO)
- Data corruption: None detected
- Verification: All smoke tests passed

## Recovery Actions
1. [Action taken]
2. [Action taken]
3. [Action taken]

## What Went Well
- Quick detection (5 minutes)
- Team response time (10 minutes)
- Backup restoration successful
- Within RTO target (4 hours)

## What Went Wrong
- [Issue]
- [Issue]

## Lessons Learned
1. [Lesson]
2. [Lesson]

## Action Items
- [ ] [Action] - Owner: [NAME] - Due: [DATE]
- [ ] [Action] - Owner: [NAME] - Due: [DATE]

## Preventive Measures
[How to prevent this from happening again]

## Sign-off
- Incident Commander: [NAME] [DATE]
- DR Coordinator: [NAME] [DATE]
- Infrastructure Lead: [NAME] [DATE]
```

---

### User Communication

**During Incident:**

```
Subject: [URGENT] Service Disruption - GreenStack Platform

Dear GreenStack Users,

We are currently experiencing a service disruption affecting the GreenStack platform.
Our team is actively working to restore service.

Current Status: INVESTIGATING
Estimated Resolution: [TIME]
Affected Services: API, Web Interface, MQTT Broker
Workarounds: None available at this time

We will provide updates every 30 minutes.

Latest Update: [TIME]
[Update details]

For urgent inquiries, contact: support@greenstack.com

Thank you for your patience.

GreenStack Operations Team
```

**After Recovery:**

```
Subject: [RESOLVED] Service Restored - GreenStack Platform

Dear GreenStack Users,

The GreenStack platform has been fully restored and all services are operational.

Incident Summary:
- Start Time: [TIME]
- End Time: [TIME]
- Duration: [DURATION]
- Root Cause: [BRIEF DESCRIPTION]
- Data Loss: None

What We've Done:
1. Restored all services from backup
2. Verified data integrity
3. Implemented monitoring improvements
4. Completed full system health check

Next Steps:
- We will publish a detailed post-mortem within 48 hours
- Additional monitoring has been implemented
- We are implementing preventive measures

We apologize for any inconvenience this may have caused. If you experience any
issues or have questions, please contact support@greenstack.com.

Thank you for your patience and understanding.

GreenStack Operations Team
```

---

### Post-Mortem Meeting (Within 1 Week)

**Agenda:**
1. Incident timeline review (15 minutes)
2. Root cause analysis (20 minutes)
3. Recovery process review (15 minutes)
4. Lessons learned (20 minutes)
5. Action items assignment (15 minutes)
6. Preventive measures (15 minutes)

**Attendees:**
- DR Coordinator
- Infrastructure Team
- Application Team
- Security Team
- Management (optional)

**Deliverables:**
- Updated incident report
- Action items with owners and due dates
- DR plan updates
- Training plan updates

---

### DR Plan Updates

Review and update DR plan after each incident:

```bash
# Update this document
git checkout -b dr-plan-update-$(date +%Y%m%d)
nano docs/guides/operations/DISASTER_RECOVERY.md

# Document changes
# - Update contact information
# - Add new scenarios
# - Update procedures based on lessons learned
# - Update RTO/RPO if needed
# - Add new tools/scripts

# Commit changes
git add docs/guides/operations/DISASTER_RECOVERY.md
git commit -m "Update DR plan based on [INCIDENT-ID] post-mortem"
git push origin dr-plan-update-$(date +%Y%m%d)

# Create pull request for review
```

---

## Appendices

### Appendix A: Backup Retention Policy

**Local Backups:**
- Daily backups: Retain 7 days
- Weekly backups: Retain 4 weeks
- Monthly backups: Retain 12 months

**S3/Cloud Backups:**
- Daily backups: Retain 30 days
- Weekly backups: Retain 12 weeks
- Monthly backups: Retain 24 months

**Lifecycle Policy Example (AWS S3):**

```json
{
  "Rules": [
    {
      "Id": "DailyBackupLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "greenstack/daily/"
      },
      "Transitions": [
        {
          "Days": 7,
          "StorageClass": "GLACIER"
        }
      ],
      "Expiration": {
        "Days": 30
      }
    },
    {
      "Id": "MonthlyBackupLifecycle",
      "Status": "Enabled",
      "Filter": {
        "Prefix": "greenstack/monthly/"
      },
      "Transitions": [
        {
          "Days": 90,
          "StorageClass": "DEEP_ARCHIVE"
        }
      ],
      "Expiration": {
        "Days": 730
      }
    }
  ]
}
```

---

### Appendix B: Emergency Contact Card

Print and carry this card for 24/7 access:

```
╔════════════════════════════════════════╗
║  GREENSTACK DISASTER RECOVERY          ║
║  EMERGENCY CONTACT CARD                ║
╠════════════════════════════════════════╣
║ DR Hotline: [PHONE]                    ║
║ DR Coordinator: [NAME] [PHONE]         ║
║ Infrastructure Lead: [NAME] [PHONE]    ║
║                                        ║
║ CRITICAL PROCEDURES:                   ║
║ 1. Assess situation                    ║
║ 2. Declare disaster if RTO at risk     ║
║ 3. Activate DR team                    ║
║ 4. Follow DR plan                      ║
║                                        ║
║ DR Plan Location:                      ║
║ - Git: docs/guides/operations/DISASTER_       ║
║        RECOVERY.md                     ║
║ - Wiki: [URL]                          ║
║ - USB: Encrypted backup drive          ║
║                                        ║
║ Backup Locations:                      ║
║ - S3: s3://[BUCKET]/greenstack/       ║
║ - Local: /opt/greenstack/backups/     ║
║                                        ║
║ Last Updated: 2025-11-18               ║
╚════════════════════════════════════════╝
```

---

### Appendix C: High Availability Configuration

For environments requiring zero downtime and zero data loss:

**PostgreSQL Streaming Replication:**

```yaml
# Primary Server (docker-compose.ha-primary.yml)
services:
  postgres-primary:
    image: postgres:15
    environment:
      - POSTGRES_USER=iodd_user
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - POSTGRES_DB=greenstack
    command: |
      postgres
      -c wal_level=replica
      -c max_wal_senders=3
      -c max_replication_slots=3
      -c hot_standby=on
    volumes:
      - postgres-primary-data:/var/lib/postgresql/data
      - ./config/postgres/pg_hba.conf:/etc/postgresql/pg_hba.conf

# Standby Server (docker-compose.ha-standby.yml)
services:
  postgres-standby:
    image: postgres:15
    environment:
      - POSTGRES_USER=iodd_user
      - POSTGRES_PASSWORD=${POSTGRES_PASSWORD}
      - PGDATA=/var/lib/postgresql/data/pgdata
    command: |
      bash -c "
      if [ ! -f /var/lib/postgresql/data/pgdata/recovery.signal ]; then
        pg_basebackup -h postgres-primary -U replicator -D /var/lib/postgresql/data/pgdata -Fp -Xs -R
      fi
      postgres
      "
    volumes:
      - postgres-standby-data:/var/lib/postgresql/data
```

**WAL Archiving for Point-in-Time Recovery:**

```bash
# postgresql.conf additions
archive_mode = on
archive_command = 'test ! -f /wal_archive/%f && cp %p /wal_archive/%f'
archive_timeout = 300  # Force WAL rotation every 5 minutes

# Create WAL archive directory
mkdir -p /wal_archive
chown postgres:postgres /wal_archive

# Backup WAL archives to S3
0 * * * * aws s3 sync /wal_archive s3://your-bucket/wal-archive/
```

**Load Balancer Configuration (HAProxy):**

```
frontend greenstack_api
    bind *:443 ssl crt /etc/ssl/certs/greenstack.pem
    default_backend greenstack_servers

backend greenstack_servers
    balance roundrobin
    option httpchk GET /api/health
    http-check expect status 200
    server api1 10.0.1.10:8000 check
    server api2 10.0.1.11:8000 check
    server api3 10.0.1.12:8000 check backup
```

**Redis Sentinel for High Availability:**

```yaml
services:
  redis-sentinel:
    image: redis:7
    command: redis-sentinel /etc/redis/sentinel.conf
    volumes:
      - ./config/redis/sentinel.conf:/etc/redis/sentinel.conf
```

---

### Appendix D: Backup Script Reference

**Location:** `scripts/backup.sh`

**Usage:**
```bash
# Standard daily backup
./scripts/backup.sh

# Custom backup directory
BACKUP_DIR=/mnt/backups ./scripts/backup.sh

# Custom retention
BACKUP_RETENTION_DAYS=14 ./scripts/backup.sh

# Backup to S3
BACKUP_S3_BUCKET=my-backup-bucket ./scripts/backup.sh
```

**Configuration via .env:**
```bash
BACKUP_DIR=./backups
BACKUP_RETENTION_DAYS=7
BACKUP_S3_BUCKET=your-bucket-name
AWS_DEFAULT_REGION=us-east-1
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

**Cron Schedule:**
```bash
# Daily backup at 3:00 AM
0 3 * * * cd /opt/greenstack && ./scripts/backup.sh >> /var/log/greenstack/backup.log 2>&1

# Weekly backup on Sunday at 3:00 AM (same as daily, retention handles it)
0 3 * * 0 cd /opt/greenstack && BACKUP_RETENTION_DAYS=28 ./scripts/backup.sh >> /var/log/greenstack/backup-weekly.log 2>&1
```

---

### Appendix E: Restore Script Reference

**Location:** `scripts/restore.sh`

**Usage:**
```bash
# Full restore with confirmation
./scripts/restore.sh backups/greenstack_backup_20251118_030000.tar.gz

# Full restore without confirmation (automated)
./scripts/restore.sh backups/greenstack_backup_20251118_030000.tar.gz --no-confirmation

# Database only
./scripts/restore.sh backups/greenstack_backup_20251118_030000.tar.gz --database-only

# Files only (no database)
./scripts/restore.sh backups/greenstack_backup_20251118_030000.tar.gz --files-only

# Configuration only
./scripts/restore.sh backups/greenstack_backup_20251118_030000.tar.gz --config-only

# Skip Docker volumes
./scripts/restore.sh backups/greenstack_backup_20251118_030000.tar.gz --skip-volumes
```

**Help:**
```bash
./scripts/restore.sh --help
```

---

### Appendix F: Health Check Script Reference

**Location:** `scripts/healthcheck.sh`

**Usage:**
```bash
# Run comprehensive health check
./scripts/healthcheck.sh

# Custom service URLs
API_URL=http://api.example.com:8000 ./scripts/healthcheck.sh

# Exit codes:
# 0 = All checks passed
# 0 = Some warnings but no failures
# 1 = One or more critical failures
```

**Health Check Categories:**
1. Docker Services (API, PostgreSQL, Redis, Mosquitto, InfluxDB, Grafana, Prometheus)
2. API Health endpoint
3. Database connectivity and table count
4. Redis connectivity and memory usage
5. MQTT broker ports (1883, 8883)
6. InfluxDB health endpoint
7. Grafana health endpoint
8. Prometheus health and targets
9. Disk space usage
10. Memory usage
11. Recent error logs (last hour)

**Integration with Monitoring:**
```bash
# Add to crontab for continuous monitoring (every 5 minutes)
*/5 * * * * /opt/greenstack/scripts/healthcheck.sh || echo "Health check failed" | mail -s "GreenStack Health Alert" ops@example.com
```

---

### Appendix G: Glossary

**RTO (Recovery Time Objective):** Maximum acceptable time to restore service after a disaster

**RPO (Recovery Point Objective):** Maximum acceptable data loss measured in time

**Disaster:** Any event that disrupts normal operations and triggers this DR plan

**Failover:** Switching to a redundant or standby system upon failure of the primary system

**Failback:** Returning operations to the primary system after it has been restored

**Hot Backup:** Backup performed while the system is running

**Cold Backup:** Backup performed while the system is offline

**Full Backup:** Complete backup of all data

**Incremental Backup:** Backup of only data changed since last backup

**Differential Backup:** Backup of data changed since last full backup

**PITR (Point-in-Time Recovery):** Ability to restore database to any specific point in time

**WAL (Write-Ahead Logging):** PostgreSQL transaction logging mechanism used for recovery

---

### Appendix H: Revision History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-11-18 | Infrastructure Team | Initial version created with comprehensive procedures, RTO/RPO definitions, disaster scenarios, contact information, and testing procedures |

**Review Schedule:**
- Quarterly review of contact information
- Quarterly review of procedures
- Annual full review and testing
- Update immediately after any disaster recovery incident

---

## Document Approval

| Role | Name | Signature | Date |
|------|------|-----------|------|
| DR Coordinator | [NAME] | _______________ | ________ |
| Infrastructure Lead | [NAME] | _______________ | ________ |
| Security Lead | [NAME] | _______________ | ________ |
| CTO | [NAME] | _______________ | ________ |

---

**END OF DISASTER RECOVERY PLAN**

*This document contains sensitive information about recovery procedures and contact details. Store securely and limit distribution to authorized personnel.*
