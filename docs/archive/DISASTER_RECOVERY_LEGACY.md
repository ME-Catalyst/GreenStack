# GreenStack Disaster Recovery Plan

## Executive Summary

This document outlines disaster recovery procedures for GreenStack to ensure business continuity in the event of system failures, data loss, or security incidents.

**Recovery Time Objective (RTO):** 4 hours
**Recovery Point Objective (RPO):** 24 hours
**Last Updated:** 2025-01-18
**Plan Owner:** DevOps Team

---

## Table of Contents

1. [Disaster Scenarios](#disaster-scenarios)
2. [Backup Strategy](#backup-strategy)
3. [Recovery Procedures](#recovery-procedures)
4. [Testing Schedule](#testing-schedule)
5. [Contact Information](#contact-information)
6. [Post-Incident Actions](#post-incident-actions)

---

## Disaster Scenarios

### Scenario 1: Database Corruption

**Impact:** High - Complete data loss
**Probability:** Low
**RTO:** 2 hours
**RPO:** 24 hours

**Triggers:**
- Database file corruption
- Disk failures
- Power outages during writes
- Software bugs

**Detection:**
- "Database disk image is malformed" errors
- Query failures
- Data inconsistencies
- Automatic health checks fail

**Recovery Procedure:** See [Database Corruption Recovery](#database-corruption-recovery)

---

### Scenario 2: Complete Server Failure

**Impact:** Critical - Total system unavailable
**Probability:** Medium
**RTO:** 4 hours
**RPO:** 24 hours

**Triggers:**
- Hardware failure
- Data center outage
- Network failures
- OS corruption

**Detection:**
- Monitoring alerts
- Unable to access server
- Service unavailable errors
- Health checks timeout

**Recovery Procedure:** See [Complete Server Failure Recovery](#complete-server-failure-recovery)

---

### Scenario 3: Accidental Data Deletion

**Impact:** Medium - Partial data loss
**Probability:** Medium
**RTO:** 1 hour
**RPO:** 24 hours

**Triggers:**
- User error (bulk delete)
- Script/automation error
- Malicious action

**Detection:**
- User reports missing data
- Unexpected database size reduction
- Audit logs show deletions

**Recovery Procedure:** See [Accidental Deletion Recovery](#accidental-deletion-recovery)

---

### Scenario 4: Security Breach / Ransomware

**Impact:** Critical - Data compromise/encryption
**Probability:** Low
**RTO:** 8 hours
**RPO:** 24 hours

**Triggers:**
- Unauthorized access
- Ransomware attack
- Data encryption by malware
- Account compromise

**Detection:**
- Unusual system behavior
- Files encrypted
- Ransom messages
- Security alerts
- Unauthorized access logs

**Recovery Procedure:** See [Security Breach Recovery](#security-breach-recovery)

---

## Backup Strategy

### Automated Daily Backups

**Schedule:** Daily at 2:00 AM UTC
**Retention:** 30 days rolling
**Location:** Off-site storage + cloud backup

**Backup Script:**

```bash
#!/bin/bash
# /opt/greenstack/backup-daily.sh

BACKUP_DIR="/opt/greenstack/backups"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
DB_PATH="/opt/greenstack/greenstack.db"
RETENTION_DAYS=30

# Create backup directory
mkdir -p "$BACKUP_DIR"

# Backup database
sqlite3 "$DB_PATH" ".backup '$BACKUP_DIR/greenstack_$TIMESTAMP.db'"

# Backup configuration files
tar -czf "$BACKUP_DIR/config_$TIMESTAMP.tar.gz" \
    /opt/greenstack/.env \
    /etc/nginx/sites-available/greenstack.conf \
    /opt/greenstack/frontend/dist

# Verify backup
if [ -f "$BACKUP_DIR/greenstack_$TIMESTAMP.db" ]; then
    sqlite3 "$BACKUP_DIR/greenstack_$TIMESTAMP.db" "PRAGMA integrity_check;"
    if [ $? -eq 0 ]; then
        echo "Backup successful: $TIMESTAMP"
    else
        echo "ERROR: Backup verification failed"
        exit 1
    fi
else
    echo "ERROR: Backup file not created"
    exit 1
fi

# Upload to cloud storage (AWS S3 example)
aws s3 cp "$BACKUP_DIR/greenstack_$TIMESTAMP.db" \
    s3://greenstack-backups/$(date +%Y/%m)/

# Remove old backups
find "$BACKUP_DIR" -name "greenstack_*.db" -mtime +$RETENTION_DAYS -delete
find "$BACKUP_DIR" -name "config_*.tar.gz" -mtime +$RETENTION_DAYS -delete

# Send notification
curl -X POST "https://hooks.slack.com/services/YOUR/WEBHOOK/URL" \
    -H 'Content-Type: application/json' \
    -d "{\"text\":\"GreenStack backup completed: $TIMESTAMP\"}"
```

**Setup:**

```bash
# Make executable
chmod +x /opt/greenstack/backup-daily.sh

# Add to crontab
sudo crontab -e
# Add line:
0 2 * * * /opt/greenstack/backup-daily.sh >> /var/log/greenstack-backup.log 2>&1
```

### Weekly Full System Backup

**Schedule:** Sundays at 1:00 AM UTC
**Retention:** 12 weeks (3 months)
**Location:** Off-site + cloud

```bash
#!/bin/bash
# /opt/greenstack/backup-weekly.sh

TIMESTAMP=$(date +%Y%m%d)
BACKUP_DIR="/opt/greenstack/backups/weekly"

mkdir -p "$BACKUP_DIR"

# Full system backup
tar -czf "$BACKUP_DIR/greenstack_full_$TIMESTAMP.tar.gz" \
    /opt/greenstack/ \
    /etc/nginx/sites-available/greenstack.conf \
    /var/www/greenstack/ \
    --exclude=/opt/greenstack/backups \
    --exclude=/opt/greenstack/node_modules \
    --exclude=/opt/greenstack/venv

# Upload to cloud
aws s3 cp "$BACKUP_DIR/greenstack_full_$TIMESTAMP.tar.gz" \
    s3://greenstack-backups/weekly/

# Keep only last 12 weeks
find "$BACKUP_DIR" -name "greenstack_full_*.tar.gz" -mtime +84 -delete
```

### Backup Verification

**Automated verification:** Daily after backup
**Manual testing:** Monthly (first Monday)

```bash
#!/bin/bash
# verify-backup.sh

LATEST_BACKUP=$(ls -t /opt/greenstack/backups/greenstack_*.db | head -1)

# Test database integrity
sqlite3 "$LATEST_BACKUP" "PRAGMA integrity_check;"

# Test read operations
sqlite3 "$LATEST_BACKUP" "SELECT COUNT(*) FROM devices;"
sqlite3 "$LATEST_BACKUP" "SELECT COUNT(*) FROM parameters;"
sqlite3 "$LATEST_BACKUP" "SELECT COUNT(*) FROM eds_files;"

# Test restore to temp location
mkdir -p /tmp/backup-test
cp "$LATEST_BACKUP" /tmp/backup-test/greenstack.db
sqlite3 /tmp/backup-test/greenstack.db "SELECT * FROM devices LIMIT 1;"

if [ $? -eq 0 ]; then
    echo "Backup verification PASSED"
    rm -rf /tmp/backup-test
    exit 0
else
    echo "Backup verification FAILED"
    # Send alert
    exit 1
fi
```

---

## Recovery Procedures

### Database Corruption Recovery

**Estimated Time:** 1-2 hours

**Prerequisites:**
- Access to backup files
- Root/sudo access
- Database stopped

**Steps:**

1. **Stop all services:**
   ```bash
   sudo systemctl stop greenstack-backend
   sudo systemctl stop nginx
   ```

2. **Verify database is corrupt:**
   ```bash
   sqlite3 greenstack.db "PRAGMA integrity_check;"
   # If output is not "ok", database is corrupt
   ```

3. **Backup corrupt database (forensics):**
   ```bash
   mv greenstack.db greenstack.db.corrupt.$(date +%Y%m%d_%H%M%S)
   ```

4. **Identify latest good backup:**
   ```bash
   ls -lth /opt/greenstack/backups/greenstack_*.db | head -5
   # Or check cloud storage
   aws s3 ls s3://greenstack-backups/$(date +%Y/%m)/ --recursive
   ```

5. **Download backup if needed:**
   ```bash
   aws s3 cp s3://greenstack-backups/YYYY/MM/greenstack_YYYYMMDD.db \
       /tmp/greenstack-restore.db
   ```

6. **Verify backup integrity:**
   ```bash
   sqlite3 /tmp/greenstack-restore.db "PRAGMA integrity_check;"
   sqlite3 /tmp/greenstack-restore.db "SELECT COUNT(*) FROM devices;"
   ```

7. **Restore database:**
   ```bash
   cp /tmp/greenstack-restore.db /opt/greenstack/greenstack.db
   chown greenstack:greenstack /opt/greenstack/greenstack.db
   chmod 644 /opt/greenstack/greenstack.db
   ```

8. **Start services:**
   ```bash
   sudo systemctl start greenstack-backend
   sudo systemctl start nginx
   ```

9. **Verify operation:**
   ```bash
   curl http://localhost:8000/health
   curl http://localhost:8000/api/stats
   ```

10. **Check web interface:**
    - Navigate to https://your-domain.com
    - Verify data displays correctly
    - Test key operations

11. **Document recovery:**
    - Note time of failure
    - Backup used for recovery
    - Data lost (time period)
    - Root cause analysis

**Expected Data Loss:** Up to 24 hours of data (since last backup)

**Rollback Procedure:**
- Keep corrupt database for 30 days
- If issues found, can attempt different backup

---

### Complete Server Failure Recovery

**Estimated Time:** 3-4 hours

**Prerequisites:**
- New server provisioned
- DNS access
- Backup access
- SSL certificates

**Steps:**

1. **Provision new server:**
   ```bash
   # Minimum specs:
   # - 4 CPU cores
   # - 8 GB RAM
   # - 100 GB SSD
   # - Ubuntu 22.04 LTS
   ```

2. **Install dependencies:**
   ```bash
   sudo apt-get update
   sudo apt-get install -y \
       python3 python3-pip python3-venv \
       nodejs npm \
       nginx \
       sqlite3 \
       certbot python3-certbot-nginx \
       git
   ```

3. **Clone repository:**
   ```bash
   cd /opt
   git clone https://github.com/your-org/greenstack.git
   cd greenstack
   ```

4. **Restore database:**
   ```bash
   # Download latest backup
   aws s3 cp s3://greenstack-backups/latest/greenstack.db \
       /opt/greenstack/greenstack.db

   # Verify
   sqlite3 /opt/greenstack/greenstack.db "PRAGMA integrity_check;"
   ```

5. **Restore configuration:**
   ```bash
   # Download config backup
   aws s3 cp s3://greenstack-backups/latest/config.tar.gz /tmp/

   # Extract
   cd /opt/greenstack
   tar -xzf /tmp/config.tar.gz

   # Set permissions
   chmod 600 .env
   ```

6. **Install Python dependencies:**
   ```bash
   cd /opt/greenstack
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

7. **Install Node dependencies and build frontend:**
   ```bash
   cd frontend
   npm install
   npm run build

   # Deploy to nginx directory
   sudo mkdir -p /var/www/greenstack/frontend
   sudo cp -r dist /var/www/greenstack/frontend/
   ```

8. **Configure Nginx:**
   ```bash
   sudo cp deployment/nginx/greenstack.conf \
       /etc/nginx/sites-available/

   # Update domain in config
   sudo sed -i 's/greenstack.example.com/your-domain.com/g' \
       /etc/nginx/sites-available/greenstack.conf

   sudo ln -s /etc/nginx/sites-available/greenstack.conf \
       /etc/nginx/sites-enabled/

   sudo nginx -t
   ```

9. **Setup SSL certificate:**
   ```bash
   sudo certbot --nginx -d your-domain.com
   ```

10. **Create systemd service:**
    ```bash
    sudo tee /etc/systemd/system/greenstack-backend.service << EOF
    [Unit]
    Description=GreenStack Backend API
    After=network.target

    [Service]
    Type=simple
    User=greenstack
    WorkingDirectory=/opt/greenstack
    Environment="PATH=/opt/greenstack/venv/bin"
    ExecStart=/opt/greenstack/venv/bin/uvicorn src.api:app --host 127.0.0.1 --port 8000
    Restart=always
    RestartSec=10

    [Install]
    WantedBy=multi-user.target
    EOF

    sudo systemctl daemon-reload
    sudo systemctl enable greenstack-backend
    sudo systemctl start greenstack-backend
    ```

11. **Start services:**
    ```bash
    sudo systemctl start greenstack-backend
    sudo systemctl start nginx
    ```

12. **Update DNS:**
    - Point domain to new server IP
    - Wait for propagation (up to 48 hours)
    - Use low TTL (300s) for faster updates

13. **Verify operation:**
    ```bash
    # Health check
    curl http://localhost:8000/health

    # API test
    curl http://localhost:8000/api/stats

    # Full test
    curl https://your-domain.com
    ```

14. **Restore monitoring:**
    - Update monitoring endpoints
    - Configure alerts
    - Verify backup jobs

15. **Document recovery:**
    - Failure time
    - Recovery time
    - Data loss
    - Lessons learned

**Expected Data Loss:** Up to 24 hours

---

### Accidental Deletion Recovery

**Estimated Time:** 30 minutes - 1 hour

**Prerequisites:**
- Access to backups
- SQL knowledge
- Database access

**Scenario A: Single Device Deleted**

```bash
# 1. Identify deleted device ID and deletion time
# Check audit logs if available

# 2. Find appropriate backup (before deletion)
BACKUP_DATE="20250117"  # Adjust as needed
BACKUP_FILE="/opt/greenstack/backups/greenstack_${BACKUP_DATE}.db"

# 3. Extract device data from backup
sqlite3 "$BACKUP_FILE" <<EOF
.mode insert
.output /tmp/device_recovery.sql
SELECT * FROM devices WHERE id = DEVICE_ID;
SELECT * FROM parameters WHERE device_id = DEVICE_ID;
SELECT * FROM events WHERE device_id = DEVICE_ID;
-- Include all related tables
.output stdout
.quit
EOF

# 4. Import to current database
sqlite3 /opt/greenstack/greenstack.db < /tmp/device_recovery.sql

# 5. Verify restoration
sqlite3 /opt/greenstack/greenstack.db \
    "SELECT * FROM devices WHERE id = DEVICE_ID;"
```

**Scenario B: Bulk Deletion**

```bash
# 1. Stop services to prevent further changes
sudo systemctl stop greenstack-backend

# 2. Backup current state
cp greenstack.db greenstack.db.before-restore

# 3. Identify tables affected
# Check audit logs or transaction history

# 4. Restore entire database from backup
cp /opt/greenstack/backups/greenstack_YYYYMMDD.db greenstack.db

# 5. Extract any new data added after backup
# (Manual process - requires identifying new records)

# 6. Start services
sudo systemctl start greenstack-backend

# 7. Verify
```

**Scenario C: "Delete All Data" Misuse**

```bash
# This is a complete restore scenario
# Use Database Corruption Recovery procedure
# Restore from most recent backup before deletion
```

---

### Security Breach Recovery

**Estimated Time:** 4-8 hours

**IMMEDIATE ACTIONS (First 30 minutes):**

1. **Isolate affected systems:**
   ```bash
   # Block all incoming traffic except SSH from admin IP
   sudo ufw default deny incoming
   sudo ufw allow from YOUR_ADMIN_IP to any port 22
   sudo ufw enable

   # Stop services
   sudo systemctl stop nginx
   sudo systemctl stop greenstack-backend
   ```

2. **Preserve evidence:**
   ```bash
   # Create forensics directory
   mkdir /tmp/forensics-$(date +%Y%m%d_%H%M%S)

   # Copy logs
   cp -r /var/log/nginx /tmp/forensics-*/
   cp /var/log/greenstack* /tmp/forensics-*/

   # Copy database
   cp greenstack.db /tmp/forensics-*/

   # System logs
   cp /var/log/auth.log /tmp/forensics-*/
   cp /var/log/syslog /tmp/forensics-*/

   # List active connections
   netstat -tulpn > /tmp/forensics-*/netstat.txt

   # List active processes
   ps aux > /tmp/forensics-*/processes.txt
   ```

3. **Assess damage:**
   ```bash
   # Check for unauthorized changes
   find /opt/greenstack -type f -mtime -1

   # Check for new users
   cat /etc/passwd | tail -n 10

   # Check for unauthorized SSH keys
   cat ~/.ssh/authorized_keys

   # Check crontabs
   crontab -l
   sudo crontab -l

   # Check for suspicious processes
   ps aux | grep -E "nc|ncat|backdoor"
   ```

4. **Notify stakeholders:**
   - Security team
   - Management
   - Affected users (if applicable)
   - Legal/compliance team

**RECOVERY ACTIONS (Next 4-8 hours):**

5. **Reset all credentials:**
   ```bash
   # System passwords
   sudo passwd root
   sudo passwd greenstack

   # Database passwords (if applicable)
   # API keys / tokens
   # SSL certificates (if compromised)
   ```

6. **Restore from clean backup:**
   ```bash
   # Use backup from before compromise
   # Verify backup is not compromised

   # Full system restore
   # See Complete Server Failure Recovery
   ```

7. **Patch vulnerabilities:**
   ```bash
   # Update all packages
   sudo apt-get update
   sudo apt-get upgrade -y

   # Update application
   cd /opt/greenstack
   git pull
   pip install -r requirements.txt --upgrade

   # Review and fix security issues
   ```

8. **Harden security:**
   ```bash
   # Enable fail2ban
   sudo apt-get install fail2ban

   # Configure stricter firewall rules
   sudo ufw default deny incoming
   sudo ufw allow 22/tcp
   sudo ufw allow 80/tcp
   sudo ufw allow 443/tcp
   sudo ufw enable

   # Disable root login
   sudo sed -i 's/PermitRootLogin yes/PermitRootLogin no/' \
       /etc/ssh/sshd_config
   sudo systemctl restart sshd

   # Enable SSH key-only authentication
   sudo sed -i 's/#PasswordAuthentication yes/PasswordAuthentication no/' \
       /etc/ssh/sshd_config
   ```

9. **Implement monitoring:**
   ```bash
   # Install intrusion detection
   sudo apt-get install aide
   sudo aideinit

   # Setup log monitoring
   sudo apt-get install logwatch
   ```

10. **Gradual service restoration:**
    ```bash
    # Start with limited access
    # Monitor closely
    # Gradually expand access
    ```

11. **Post-incident analysis:**
    - Root cause analysis
    - Timeline of events
    - Vulnerabilities exploited
    - Response effectiveness
    - Preventive measures

---

## Testing Schedule

### Monthly DR Tests (First Monday)

**Test:** Backup restoration
**Duration:** 1 hour
**Environment:** Staging server

**Procedure:**
1. Restore latest backup to staging
2. Verify data integrity
3. Test application functionality
4. Document results

### Quarterly DR Tests (First Monday of Q1, Q2, Q3, Q4)

**Test:** Complete server failure simulation
**Duration:** 4 hours
**Environment:** Dedicated DR environment

**Procedure:**
1. Provision new server
2. Execute complete recovery procedure
3. Verify full system operation
4. Time each step
5. Update procedures based on learnings

### Annual DR Tests (January)

**Test:** Full disaster recovery drill
**Duration:** Full day
**Participants:** All team members

**Procedure:**
1. Simulate complete data center failure
2. Execute all recovery procedures
3. Test all communication channels
4. Verify contact information
5. Update entire DR plan

### Test Documentation Template

```markdown
## DR Test Report

**Date:** YYYY-MM-DD
**Test Type:** [Backup Restoration | Complete Failure | Full Drill]
**Tester:** Name
**Environment:** [Staging | DR Environment]

### Results
- **Status:** [PASS | FAIL | PARTIAL]
- **Start Time:** HH:MM
- **End Time:** HH:MM
- **Total Duration:** HH hours MM minutes

### Steps Performed
1. Step 1 - Duration: XX min - Status: PASS
2. Step 2 - Duration: XX min - Status: PASS
...

### Issues Encountered
1. Issue description
   - Impact: [High | Medium | Low]
   - Resolution: Description

### Recommendations
1. Update procedure X
2. Add monitoring for Y
3. Improve documentation for Z

### Action Items
- [ ] Action 1 - Assigned to: Name - Due: Date
- [ ] Action 2 - Assigned to: Name - Due: Date
```

---

## Contact Information

### Emergency Response Team

**Primary On-Call:**
- Name: DevOps Lead
- Phone: +1-XXX-XXX-XXXX
- Email: devops@company.com
- Backup Phone: +1-XXX-XXX-XXXX

**Secondary On-Call:**
- Name: Senior SRE
- Phone: +1-XXX-XXX-XXXX
- Email: sre@company.com

**Management:**
- Name: CTO
- Phone: +1-XXX-XXX-XXXX
- Email: cto@company.com

### External Vendors

**Hosting Provider:**
- Company: AWS / DigitalOcean / etc.
- Support Phone: +1-XXX-XXX-XXXX
- Support Email: support@provider.com
- Account Number: XXXXXXXXXX

**Security Firm:**
- Company: Security Co
- Phone: +1-XXX-XXX-XXXX
- Email: incident@securityco.com

**Legal:**
- Firm: Law Firm
- Contact: Lawyer Name
- Phone: +1-XXX-XXX-XXXX

### Communication Channels

**Incident Slack Channel:** #incident-response
**Status Page:** https://status.greenstack.io
**Incident Management:** Jira / PagerDuty / etc.

---

## Post-Incident Actions

### Immediate (Within 24 hours)

1. **Document incident:**
   - Timeline
   - Actions taken
   - Data loss
   - Downtime duration

2. **Notify stakeholders:**
   - Internal teams
   - Affected users
   - Management

3. **Preserve evidence:**
   - Keep logs for 90 days
   - Document forensic findings

### Short-term (Within 1 week)

4. **Conduct root cause analysis:**
   - What happened?
   - Why did it happen?
   - What was the impact?

5. **Create incident report:**
   - Executive summary
   - Detailed timeline
   - Root causes
   - Response effectiveness
   - Recommendations

6. **Share learnings:**
   - Team debrief
   - Documentation updates
   - Training needs

### Long-term (Within 1 month)

7. **Implement preventive measures:**
   - Address root causes
   - Update procedures
   - Improve monitoring
   - Add safeguards

8. **Update DR plan:**
   - Incorporate lessons learned
   - Update procedures
   - Revise contact information
   - Adjust RTO/RPO if needed

9. **Schedule follow-up tests:**
   - Test new procedures
   - Validate improvements
   - Measure effectiveness

---

## Appendix

### Useful Commands Reference

```bash
# Database backup
sqlite3 greenstack.db ".backup backup.db"

# Database restore
cp backup.db greenstack.db

# Check database integrity
sqlite3 greenstack.db "PRAGMA integrity_check;"

# Export database to SQL
sqlite3 greenstack.db .dump > backup.sql

# Import from SQL
sqlite3 greenstack.db < backup.sql

# Check service status
systemctl status greenstack-backend
systemctl status nginx

# View logs
journalctl -u greenstack-backend -f
tail -f /var/log/nginx/greenstack-error.log

# Test API
curl http://localhost:8000/health
curl http://localhost:8000/api/stats

# Check disk space
df -h

# Check memory usage
free -h

# Check processes
ps aux | grep -E "uvicorn|nginx"

# Check network
netstat -tulpn
ss -tulpn
```

### Backup Storage Locations

**Primary:** Local server `/opt/greenstack/backups`
**Secondary:** AWS S3 `s3://greenstack-backups/`
**Tertiary:** External drive (kept off-site)

### Version History

| Version | Date | Author | Changes |
|---------|------|--------|---------|
| 1.0 | 2025-01-18 | DevOps | Initial version |

---

**This is a living document. Review and update quarterly or after each incident.**
