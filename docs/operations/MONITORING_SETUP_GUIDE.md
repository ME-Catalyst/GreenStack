# Monitoring Stack Setup Guide

**Version:** 1.0
**Date:** 2025-11-18

## Overview

This guide walks you through setting up and verifying the complete monitoring and alerting stack for GreenStack, including:

- **Prometheus** - Metrics collection and alerting
- **Grafana** - Visualization and dashboards
- **Alertmanager** - Alert routing and notifications

---

## Prerequisites

- Docker and Docker Compose installed
- GreenStack application running
- Email account for SMTP alerts (optional)
- Slack workspace with webhook configured (optional)

---

## Quick Start

### 1. Start Monitoring Services

```bash
# Start the IoT monitoring stack
docker-compose -f docker-compose.iot.yml up -d prometheus alertmanager grafana

# Verify services are running
docker ps | grep -E "prometheus|alertmanager|grafana"
```

**Expected output:**
```
greenstack-prometheus      Up 30 seconds   0.0.0.0:9090->9090/tcp
greenstack-alertmanager    Up 30 seconds   0.0.0.0:9093->9093/tcp
greenstack-grafana         Up 30 seconds   0.0.0.0:3000->3000/tcp
```

### 2. Access Monitoring Interfaces

| Service | URL | Default Credentials |
|---------|-----|-------------------|
| Prometheus | http://localhost:9090 | None |
| Alertmanager | http://localhost:9093 | None |
| Grafana | http://localhost:3000 | admin / (from .env) |

### 3. Verify Prometheus Targets

1. Open http://localhost:9090/targets
2. Verify all targets are "UP":
   - `greenstack-api` - Should be UP
   - `prometheus` - Should be UP

**Troubleshooting:**
- If `greenstack-api` is DOWN, check that the API is running: `docker ps | grep greenstack-api`
- Verify API metrics endpoint is accessible: `curl http://localhost:8000/metrics`

### 4. Verify Alert Rules

1. Open http://localhost:9090/alerts
2. You should see all configured alert rules (40+ rules)
3. Status should be "Inactive" (green) for healthy system
4. Status shows "Pending" (yellow) if alert is about to fire
5. Status shows "Firing" (red) if alert condition is met

**Alert Groups:**
- `critical_alerts` - 7 rules (ServiceDown, HighErrorRate, etc.)
- `high_priority_alerts` - 8 rules (HighResponseTime, HighCPUUsage, etc.)
- `business_alerts` - 4 rules (NoIODDUploads, HighParseFailureRate, etc.)
- `performance_alerts` - 4 rules (SlowDatabaseQueries, etc.)
- `security_alerts` - 3 rules (HighAuthenticationFailure, etc.)
- `data_quality_alerts` - 3 rules (MissingMetrics, StaleTelemetryData, etc.)

### 5. Verify Grafana Datasource

1. Log in to Grafana at http://localhost:3000
2. Navigate to **Configuration** → **Data sources**
3. Verify "Prometheus" datasource is configured
4. Click "Test" button - should show "Data source is working"

**Troubleshooting:**
- If datasource not found, check that provisioning directory is mounted:
  ```bash
  docker exec greenstack-grafana ls /etc/grafana/provisioning/datasources/
  ```
- Should see: `prometheus.yml`

### 6. Test Alerting (Optional but Recommended)

#### Test A: Trigger a Test Alert Manually

Create a test alert rule that always fires:

```bash
# Add test alert to Prometheus
cat >> config/prometheus/alerts.yml <<EOF

  - name: test_alerts
    rules:
      - alert: TestAlert
        expr: vector(1)
        labels:
          severity: warning
          component: test
        annotations:
          summary: "This is a test alert"
          description: "Testing alert routing and notifications"
EOF

# Reload Prometheus configuration
curl -X POST http://localhost:9090/-/reload
```

**Verify:**
1. Open http://localhost:9090/alerts
2. Find "TestAlert" - should show as "Firing" (red)
3. Open http://localhost:9093/#/alerts
4. Verify alert appears in Alertmanager

**Cleanup:**
```bash
# Remove test alert from alerts.yml
# Restart Prometheus or reload config
docker-compose -f docker-compose.iot.yml restart prometheus
```

#### Test B: Stop a Service to Trigger ServiceDown Alert

```bash
# Stop API to trigger ServiceDown alert
docker-compose stop api

# Wait 1-2 minutes for alert to fire

# Check Prometheus alerts
curl -s http://localhost:9090/api/v1/alerts | jq '.data.alerts[] | select(.labels.alertname=="ServiceDown")'

# Check Alertmanager
curl -s http://localhost:9093/api/v2/alerts | jq '.[] | select(.labels.alertname=="ServiceDown")'

# Restart API
docker-compose up -d api
```

---

## Configuration

### Email Alerts

To enable email alerts, configure SMTP in `.env`:

```bash
# SMTP Configuration
SMTP_HOST=smtp.gmail.com:587
SMTP_USERNAME=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# Alert Recipients
ALERT_EMAIL_CRITICAL=oncall@example.com
ALERT_EMAIL_DEFAULT=ops@example.com
ALERT_EMAIL_DBA=dba@example.com
ALERT_EMAIL_SECURITY=security@example.com
```

**For Gmail:**
1. Enable 2-factor authentication
2. Generate App Password: https://support.google.com/accounts/answer/185833
3. Use App Password as `SMTP_PASSWORD`

**Restart Alertmanager after configuration:**
```bash
docker-compose -f docker-compose.iot.yml restart alertmanager
```

### Slack Alerts

To enable Slack alerts:

1. Create Slack Incoming Webhook:
   - Go to https://api.slack.com/messaging/webhooks
   - Click "Create your Slack app"
   - Enable Incoming Webhooks
   - Add webhook to workspace
   - Copy webhook URL

2. Configure in `.env`:
```bash
SLACK_WEBHOOK_URL=https://hooks.slack.com/services/YOUR/WEBHOOK/URL
SLACK_CHANNEL_CRITICAL=#greenstack-critical
SLACK_CHANNEL_WARNINGS=#greenstack-alerts
SLACK_CHANNEL_INFO=#greenstack-info
```

3. Restart Alertmanager:
```bash
docker-compose -f docker-compose.iot.yml restart alertmanager
```

### PagerDuty Integration (Optional)

To enable PagerDuty alerts:

1. Uncomment PagerDuty section in `config/alertmanager/config.yml`
2. Add PagerDuty service key to `.env`:
```bash
PAGERDUTY_SERVICE_KEY=your-integration-key
```
3. Restart Alertmanager

---

## Alert Rules Reference

### Critical Alerts (Page Immediately)

| Alert | Condition | Threshold | Duration |
|-------|-----------|-----------|----------|
| ServiceDown | Service not responding | up == 0 | 1 minute |
| HighErrorRate | 5xx errors | >5% of requests | 5 minutes |
| DatabaseDown | PostgreSQL down | up == 0 | 1 minute |
| APIServerDown | API unreachable | up == 0 | 1 minute |
| HighMemoryUsage | Container memory | >90% | 5 minutes |
| DiskSpaceCritical | Disk space | <10% free | 5 minutes |
| DatabaseConnectionPoolExhausted | DB connections | >90% used | 5 minutes |

### Warning Alerts (Investigate Promptly)

| Alert | Condition | Threshold | Duration |
|-------|-----------|-----------|----------|
| HighResponseTime | P95 latency | >2 seconds | 10 minutes |
| HighCPUUsage | Container CPU | >80% | 10 minutes |
| HighRequestRate | Request rate | >1000 req/s | 10 minutes |
| RedisDown | Redis cache down | up == 0 | 2 minutes |
| MQTTBrokerDown | Mosquitto down | up == 0 | 2 minutes |
| InfluxDBDown | InfluxDB down | up == 0 | 5 minutes |
| BackupAgeTooOld | Backup age | >48 hours | 1 hour |
| SSLCertificateExpiringSoon | Cert expiration | <30 days | 1 day |

### Business Metrics Alerts

| Alert | Condition | Threshold | Duration |
|-------|-----------|-----------|----------|
| NoIODDUploadsRecently | No uploads | 0 uploads | 24 hours |
| HighParseFailureRate | Parse failures | >20% | 30 minutes |
| SlowIODDParsing | P95 parse time | >5 seconds | 30 minutes |
| NoDeviceSearchesRecently | No searches | 0 searches | 6 hours |

---

## Troubleshooting

### Prometheus Not Scraping Targets

**Symptom:** Target shows as "DOWN" in http://localhost:9090/targets

**Solutions:**
1. Verify target service is running:
   ```bash
   docker ps | grep greenstack-api
   ```

2. Check network connectivity:
   ```bash
   docker exec greenstack-prometheus wget -O- http://greenstack:8000/metrics
   ```

3. Check Prometheus logs:
   ```bash
   docker logs greenstack-prometheus
   ```

### Alert Rules Not Loading

**Symptom:** No alerts visible in http://localhost:9090/alerts

**Solutions:**
1. Verify alerts.yml is mounted:
   ```bash
   docker exec greenstack-prometheus cat /etc/prometheus/alerts.yml
   ```

2. Check Prometheus config references alerts:
   ```bash
   docker exec greenstack-prometheus cat /etc/prometheus/prometheus.yml | grep rule_files
   ```

3. Check for syntax errors:
   ```bash
   docker exec greenstack-prometheus promtool check rules /etc/prometheus/alerts.yml
   ```

4. Reload configuration:
   ```bash
   curl -X POST http://localhost:9090/-/reload
   ```

### Alertmanager Not Receiving Alerts

**Symptom:** Alerts firing in Prometheus but not showing in Alertmanager

**Solutions:**
1. Verify Alertmanager is reachable from Prometheus:
   ```bash
   docker exec greenstack-prometheus wget -O- http://greenstack-alertmanager:9093/api/v2/status
   ```

2. Check Prometheus alerting configuration:
   ```bash
   docker exec greenstack-prometheus cat /etc/prometheus/prometheus.yml | grep -A5 alerting
   ```

3. Check Alertmanager logs:
   ```bash
   docker logs greenstack-alertmanager
   ```

### Email Alerts Not Sending

**Symptom:** Alerts showing in Alertmanager but emails not received

**Solutions:**
1. Verify SMTP configuration:
   ```bash
   docker exec greenstack-alertmanager cat /etc/alertmanager/config.yml | grep -A10 smtp
   ```

2. Check Alertmanager logs for SMTP errors:
   ```bash
   docker logs greenstack-alertmanager | grep -i smtp
   ```

3. Test SMTP connectivity:
   ```bash
   # From host machine
   telnet smtp.gmail.com 587
   ```

4. For Gmail:
   - Verify 2FA is enabled
   - Verify App Password is used (not regular password)
   - Check "Less secure app access" is NOT required (App Passwords bypass this)

### Slack Alerts Not Sending

**Symptom:** Alerts showing in Alertmanager but Slack messages not received

**Solutions:**
1. Verify webhook URL is correct:
   ```bash
   docker logs greenstack-alertmanager | grep -i slack
   ```

2. Test webhook manually:
   ```bash
   curl -X POST "${SLACK_WEBHOOK_URL}" \
     -H 'Content-Type: application/json' \
     -d '{"text":"Test alert from GreenStack"}'
   ```

3. Check Slack app permissions:
   - Webhook must be enabled
   - App must be added to target channels

### Grafana Cannot Connect to Prometheus

**Symptom:** "Data source is not working" in Grafana

**Solutions:**
1. Verify Prometheus is accessible from Grafana:
   ```bash
   docker exec greenstack-grafana wget -O- http://greenstack-prometheus:9090/api/v1/status/config
   ```

2. Check datasource configuration:
   ```bash
   docker exec greenstack-grafana cat /etc/grafana/provisioning/datasources/prometheus.yml
   ```

3. Restart Grafana:
   ```bash
   docker-compose -f docker-compose.iot.yml restart grafana
   ```

---

## Maintenance

### Updating Alert Rules

1. Edit `config/prometheus/alerts.yml`
2. Validate syntax:
   ```bash
   docker exec greenstack-prometheus promtool check rules /etc/prometheus/alerts.yml
   ```
3. Reload Prometheus:
   ```bash
   curl -X POST http://localhost:9090/-/reload
   ```

### Updating Alertmanager Configuration

1. Edit `config/alertmanager/config.yml`
2. Validate syntax:
   ```bash
   docker exec greenstack-alertmanager amtool check-config /etc/alertmanager/config.yml
   ```
3. Reload Alertmanager:
   ```bash
   curl -X POST http://localhost:9093/-/reload
   ```

### Viewing Alert History

```bash
# View all alerts (active and resolved)
curl -s http://localhost:9093/api/v2/alerts | jq .

# View only active alerts
curl -s http://localhost:9093/api/v2/alerts?filter=active=true | jq .

# View alerts for specific severity
curl -s 'http://localhost:9093/api/v2/alerts?filter={severity="critical"}' | jq .
```

### Silencing Alerts

Temporarily silence alerts during maintenance:

```bash
# Silence specific alert
curl -X POST http://localhost:9093/api/v2/silences \
  -H 'Content-Type: application/json' \
  -d '{
    "matchers": [
      {
        "name": "alertname",
        "value": "HighCPUUsage",
        "isRegex": false
      }
    ],
    "startsAt": "2025-11-18T00:00:00Z",
    "endsAt": "2025-11-18T02:00:00Z",
    "createdBy": "ops@example.com",
    "comment": "Planned maintenance window"
  }'
```

Or use the Alertmanager UI: http://localhost:9093

---

## Metrics Reference

### Application Metrics (from API)

```promql
# Request rate
rate(http_requests_total[5m])

# Error rate
rate(http_requests_total{status=~"5.."}[5m])

# Response time (P95)
histogram_quantile(0.95, rate(http_request_duration_seconds_bucket[5m]))

# IODD uploads
rate(iodd_uploads_total[1h])

# Parse duration
rate(iodd_parse_duration_seconds_sum[5m]) / rate(iodd_parse_duration_seconds_count[5m])

# Device searches
rate(device_searches_total[5m])
```

### Database Metrics

```promql
# Connection pool usage
db_connection_pool_checked_out / db_connection_pool_size

# Query duration
rate(database_query_duration_seconds_sum[5m]) / rate(database_query_duration_seconds_count[5m])
```

### System Metrics

```promql
# Container CPU usage
rate(container_cpu_usage_seconds_total[5m])

# Container memory usage
container_memory_usage_bytes / container_spec_memory_limit_bytes

# Disk space
(node_filesystem_avail_bytes / node_filesystem_size_bytes) * 100
```

---

## Best Practices

1. **Alert Fatigue Prevention:**
   - Use appropriate thresholds and durations
   - Implement alert inhibition rules
   - Route alerts to appropriate teams
   - Silence alerts during known maintenance

2. **Runbook Links:**
   - All critical alerts have runbook annotations
   - Keep runbooks up to date
   - Test runbooks regularly

3. **Regular Testing:**
   - Test alerts quarterly
   - Verify notification delivery
   - Update contact information
   - Review and adjust thresholds

4. **Documentation:**
   - Document all custom metrics
   - Maintain alert rule changelog
   - Document escalation procedures
   - Keep contact lists current

---

## Next Steps

1. **Create Grafana Dashboards** (Day 8)
   - Application overview dashboard
   - System health dashboard
   - Database performance dashboard
   - Business metrics dashboard

2. **Set Up Log Aggregation**
   - Consider adding Loki for log aggregation
   - Correlate logs with metrics
   - Create log-based alerts

3. **Add More Exporters**
   - Node Exporter for system metrics
   - PostgreSQL Exporter for database metrics
   - Redis Exporter for cache metrics
   - Mosquitto Exporter for MQTT metrics

4. **Implement Distributed Tracing**
   - Add OpenTelemetry instrumentation
   - Integrate with Jaeger or Tempo
   - Correlate traces with metrics and logs

---

## References

- [Prometheus Documentation](https://prometheus.io/docs/)
- [Alertmanager Documentation](https://prometheus.io/docs/alerting/latest/alertmanager/)
- [Grafana Documentation](https://grafana.com/docs/)
- [PromQL Basics](https://prometheus.io/docs/prometheus/latest/querying/basics/)
- [Alert Rule Best Practices](https://prometheus.io/docs/practices/alerting/)

---

**Document Version:** 1.0
**Last Updated:** 2025-11-18
**Maintained By:** Infrastructure Team
