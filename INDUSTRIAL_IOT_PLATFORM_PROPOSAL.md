# Industrial IoT Platform - Comprehensive Proposal
## IODD Manager Evolution: Scalable, Containerized Industrial Automation Platform

**Version:** 1.0
**Date:** January 2025
**Status:** Proposal

---

## Executive Summary

This proposal outlines the transformation of IODD Manager into a comprehensive, enterprise-grade Industrial IoT platform by integrating:

- **Eclipse Mosquitto** - MQTT broker for real-time device communication
- **InfluxDB** - Time-series database for sensor data and metrics
- **Node-RED** - Visual workflow automation and integration engine
- **Grafana** - Real-time monitoring and visualization dashboards
- **Redis** - High-performance caching and message queuing
- **Traefik** - Modern reverse proxy and load balancer
- **MinIO** - S3-compatible object storage for files and backups

The platform will be fully containerized using Docker Compose and Kubernetes, enabling:
- One-command deployment on any PC or server
- Horizontal scalability from 1 to 10,000+ devices
- Cloud-native architecture (AWS, Azure, GCP, on-premise)
- High availability and fault tolerance
- Enterprise security and authentication

---

## Table of Contents

1. [Current State Analysis](#1-current-state-analysis)
2. [Proposed Architecture](#2-proposed-architecture)
3. [Component Integration Details](#3-component-integration-details)
4. [Containerization Strategy](#4-containerization-strategy)
5. [Scalability Design](#5-scalability-design)
6. [Data Flow Architecture](#6-data-flow-architecture)
7. [Security Architecture](#7-security-architecture)
8. [Deployment Scenarios](#8-deployment-scenarios)
9. [Implementation Roadmap](#9-implementation-roadmap)
10. [Technical Specifications](#10-technical-specifications)
11. [Cost Analysis](#11-cost-analysis)
12. [Success Metrics](#12-success-metrics)

---

## 1. Current State Analysis

### Current IODD Manager Capabilities

**Strengths:**
- ✅ IODD/EDS file parsing and management
- ✅ 11,000+ parameter management
- ✅ REST API with FastAPI
- ✅ Modern React frontend
- ✅ SQLite database with Alembic migrations
- ✅ Device comparison and search
- ✅ Ticket/issue tracking system
- ✅ Configuration export (JSON/CSV)
- ✅ Admin console and diagnostics

**Gaps for Industrial IoT:**
- ❌ No real-time device communication (MQTT/OPC UA)
- ❌ No time-series data storage for sensor readings
- ❌ No visual workflow automation
- ❌ No real-time dashboards/monitoring
- ❌ Limited scalability (single container)
- ❌ No device provisioning or management
- ❌ No edge computing capabilities
- ❌ No cloud integration patterns

---

## 2. Proposed Architecture

### High-Level System Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                         LOAD BALANCER (Traefik)                         │
│                     SSL/TLS Termination, Routing                        │
└─────────────────────────────────────────────────────────────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
       ┌────────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
       │   Web UI Layer  │ │  API Gateway   │ │  MQTT Broker   │
       │  (React/Vite)   │ │  (FastAPI)     │ │  (Mosquitto)   │
       │   Port: 443     │ │  Port: 8000    │ │  Port: 1883    │
       └─────────────────┘ └────────────────┘ └────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
       ┌────────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
       │   Node-RED      │ │  MQTT Bridge   │ │  Device Shadow │
       │  Workflows      │ │   Service      │ │    Service     │
       │  Port: 1880     │ │  (Python)      │ │   (Python)     │
       └─────────────────┘ └────────────────┘ └────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
       ┌────────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
       │   PostgreSQL    │ │   InfluxDB     │ │     Redis      │
       │ (Config/Meta)   │ │ (Time-Series)  │ │    (Cache)     │
       └─────────────────┘ └────────────────┘ └────────────────┘
                                    │
                ┌───────────────────┼───────────────────┐
                │                   │                   │
       ┌────────▼────────┐ ┌───────▼────────┐ ┌───────▼────────┐
       │    Grafana      │ │     MinIO      │ │   Prometheus   │
       │  Dashboards     │ │  S3 Storage    │ │   Metrics      │
       │  Port: 3000     │ │  Port: 9000    │ │  Port: 9090    │
       └─────────────────┘ └────────────────┘ └────────────────┘
```

### Technology Stack Evolution

| Layer | Current | Proposed | Rationale |
|-------|---------|----------|-----------|
| **Frontend** | React, Vite, Tailwind | ✅ Same + Grafana embeds | Keep existing, add visualization |
| **API** | FastAPI, Python | ✅ Same + gRPC endpoints | Add high-performance RPC |
| **Database (Config)** | SQLite | PostgreSQL (production) / SQLite (dev) | Scalability, concurrent writes |
| **Database (Time-Series)** | None | InfluxDB 2.x | Optimized for sensor data |
| **Caching** | None | Redis | Performance, session management |
| **Message Broker** | None | Eclipse Mosquitto | MQTT for IoT devices |
| **Workflows** | None | Node-RED | Visual automation |
| **Monitoring** | Basic logs | Grafana + Prometheus | Real-time dashboards |
| **Storage** | Local filesystem | MinIO (S3-compatible) | Scalable object storage |
| **Reverse Proxy** | Uvicorn direct | Traefik | Load balancing, SSL |
| **Orchestration** | Docker | Docker Compose + K8s | Scalability |

---

## 3. Component Integration Details

### 3.1 Eclipse Mosquitto (MQTT Broker)

**Purpose:** Real-time bidirectional communication with industrial devices

**Configuration:**
```yaml
# mosquitto.conf
listener 1883
listener 8883  # TLS/SSL
protocol mqtt

# Authentication
allow_anonymous false
password_file /mosquitto/config/passwd

# ACL for topic-based permissions
acl_file /mosquitto/config/acl

# Persistence
persistence true
persistence_location /mosquitto/data/

# Logging
log_dest file /mosquitto/log/mosquitto.log
log_type all

# Bridge to cloud MQTT brokers (optional)
connection bridge-to-cloud
address mqtt.cloud-provider.com:8883
topic devices/+/telemetry out 1
```

**Integration Points:**
- **Device Registration:** Devices publish to `devices/{device_id}/register` with IODD reference
- **Telemetry:** Real-time sensor data on `devices/{device_id}/telemetry`
- **Commands:** Send configuration commands via `devices/{device_id}/commands`
- **Shadow State:** Maintain device twin in Redis via MQTT bridge service
- **Node-RED Integration:** Subscribe to MQTT topics for workflow triggers

**Scalability:**
- Clustered Mosquitto (3-5 brokers) with shared subscriptions
- MQTT bridge to cloud brokers (AWS IoT Core, Azure IoT Hub)
- Support for 100,000+ concurrent connections per cluster

### 3.2 InfluxDB (Time-Series Database)

**Purpose:** Store and query high-frequency sensor data and metrics

**Schema Design:**
```javascript
// Measurement: device_telemetry
{
  measurement: "device_telemetry",
  tags: {
    device_id: "IFM-O2D222",
    vendor: "ifm electronic",
    parameter_name: "Distance",
    site: "factory-floor-1"
  },
  fields: {
    value: 1234.56,
    unit: "mm",
    quality: "good",
    status_code: 0
  },
  timestamp: 1735689600000000000  // nanosecond precision
}

// Measurement: system_metrics
{
  measurement: "system_metrics",
  tags: {
    service: "api",
    host: "iodd-manager-api-1"
  },
  fields: {
    cpu_usage: 45.2,
    memory_mb: 512,
    request_count: 1543
  },
  timestamp: 1735689600000000000
}
```

**Retention Policies:**
```sql
-- Raw data: 30 days
CREATE RETENTION POLICY "raw_data" ON "iodd_iot"
  DURATION 30d REPLICATION 1 DEFAULT;

-- Downsampled 1-minute averages: 1 year
CREATE RETENTION POLICY "downsampled_1m" ON "iodd_iot"
  DURATION 365d REPLICATION 1;

-- Downsampled 1-hour averages: 5 years
CREATE RETENTION POLICY "downsampled_1h" ON "iodd_iot"
  DURATION 1825d REPLICATION 1;
```

**Continuous Queries (Downsampling):**
```sql
CREATE CONTINUOUS QUERY "downsample_1m" ON "iodd_iot"
BEGIN
  SELECT mean(value) AS value_mean,
         min(value) AS value_min,
         max(value) AS value_max
  INTO "downsampled_1m"."device_telemetry"
  FROM "raw_data"."device_telemetry"
  GROUP BY time(1m), device_id, parameter_name
END;
```

**Integration Points:**
- **MQTT Bridge Service:** Subscribe to telemetry topics, write to InfluxDB
- **API Endpoints:**
  - `GET /api/telemetry/{device_id}/history?start=&end=&downsample=`
  - `GET /api/telemetry/{device_id}/realtime` (WebSocket)
- **Grafana Datasource:** Native InfluxQL/Flux queries
- **Alerts:** Kapacitor or custom alerting service for threshold violations

**Scalability:**
- InfluxDB Enterprise clustering (separate data nodes and meta nodes)
- Sharding by device_id or site
- Read replicas for query performance
- Handle 1M+ points/second write throughput

### 3.3 Node-RED (Workflow Automation)

**Purpose:** Visual programming for device orchestration, data transformation, and integration

**Use Cases:**

1. **Device Onboarding Workflow:**
   ```
   [MQTT: devices/+/register]
     → [Parse IODD Reference]
     → [Validate Device]
     → [Create Database Record]
     → [Send Welcome Config]
     → [Notify Admin]
   ```

2. **Alerting Pipeline:**
   ```
   [InfluxDB Query: High Temperature]
     → [Check Threshold]
     → [Enrich with Device Info]
     → [Create Ticket]
     → [Send Email/Slack/Teams]
   ```

3. **Data Transformation:**
   ```
   [MQTT: Raw Sensor Data]
     → [Unit Conversion]
     → [Apply Calibration]
     → [Write to InfluxDB]
     → [Publish to Analytics Topic]
   ```

4. **Integration Hub:**
   ```
   [HTTP Request: ERP System]
     → [Map Production Order]
     → [Send Device Commands]
     → [Log to Database]
   ```

**Custom Nodes to Develop:**
- `iodd-device-lookup`: Query IODD Manager API for device specs
- `iodd-parameter-mapper`: Map raw values using IODD metadata
- `iodd-command-builder`: Generate device commands from IODD structure
- `influx-batch-writer`: Optimized bulk writes to InfluxDB

**Integration Points:**
- **HTTP API:** Call IODD Manager REST endpoints
- **MQTT Broker:** Native MQTT nodes
- **InfluxDB:** Native InfluxDB nodes
- **Database:** PostgreSQL nodes for configuration
- **Webhooks:** Expose flows as HTTP endpoints

**Security:**
- Admin UI behind authentication (OAuth2/LDAP)
- Encrypted credentials storage
- Flow encryption at rest

### 3.4 Grafana (Visualization & Dashboards)

**Purpose:** Real-time monitoring, historical analysis, and alerting

**Dashboard Examples:**

1. **Factory Floor Overview:**
   - Live device status map (online/offline/error)
   - Real-time telemetry gauges for key parameters
   - Alert summary panel
   - Device count by vendor/type

2. **Device Detail Dashboard:**
   - Time-series graphs for all parameters
   - Current vs. historical performance
   - Diagnostic information from IODD
   - Recent events and alarms

3. **System Health Dashboard:**
   - MQTT broker metrics (connections, messages/sec)
   - InfluxDB performance (write/query latency)
   - API response times
   - Container resource usage

4. **Production Analytics:**
   - OEE (Overall Equipment Effectiveness)
   - Uptime/downtime trends
   - Parameter correlation analysis
   - Energy consumption monitoring

**Datasources:**
- InfluxDB (primary telemetry data)
- PostgreSQL (configuration and metadata)
- Prometheus (system metrics)
- IODD Manager API (device information)

**Alerting:**
- Alert rules based on InfluxDB queries
- Notification channels: Email, Slack, MS Teams, PagerDuty
- Alert dependencies and grouping
- Silence rules for maintenance windows

### 3.5 Redis (Caching & Messaging)

**Purpose:** High-performance caching, session management, pub/sub messaging

**Use Cases:**

1. **API Response Caching:**
   ```python
   # Cache device list for 5 minutes
   @cache(redis_client, ttl=300)
   async def get_devices():
       return await db.query_devices()
   ```

2. **Device Shadow (Digital Twin):**
   ```json
   // Redis Key: device:shadow:{device_id}
   {
     "device_id": "IFM-O2D222",
     "connection_state": "connected",
     "last_seen": 1735689600,
     "parameters": {
       "Distance": {
         "value": 1234.56,
         "timestamp": 1735689595,
         "quality": "good"
       }
     },
     "desired_config": {
       "sampling_rate": 1000
     }
   }
   ```

3. **Rate Limiting:**
   ```python
   # Limit API calls to 1000/hour per user
   rate_limiter = RedisRateLimiter(redis_client, max_calls=1000, window=3600)
   ```

4. **Message Queue:**
   ```python
   # Background job processing
   redis_queue.enqueue('process_iodd_upload', file_path='/uploads/device.xml')
   ```

5. **Session Management:**
   - Store user sessions with expiration
   - OAuth2 token storage
   - Active WebSocket connections registry

**Scalability:**
- Redis Cluster (6+ nodes) for horizontal scaling
- Redis Sentinel for high availability
- Separate instances for cache vs. messaging

### 3.6 MinIO (Object Storage)

**Purpose:** S3-compatible storage for files, backups, and blob data

**Buckets:**

1. **`iodd-files`**: IODD/EDS uploaded files
2. **`device-configs`**: Device configuration snapshots
3. **`backups`**: Database backups (automated daily)
4. **`logs`**: Archived application logs
5. **`reports`**: Generated reports and exports
6. **`firmware`**: Device firmware files for OTA updates

**Features:**
- Versioning enabled for critical buckets
- Lifecycle policies (auto-delete old backups after 90 days)
- Access policies (public/private per bucket)
- Encryption at rest (SSE-S3)
- CDN integration (CloudFront, CloudFlare)

**Integration:**
- Python boto3 client for API access
- Direct upload from frontend (presigned URLs)
- Backup automation with retention policies

### 3.7 Traefik (Reverse Proxy & Load Balancer)

**Purpose:** Modern edge router with automatic SSL, load balancing, and service discovery

**Configuration:**
```yaml
# traefik.yml
entryPoints:
  web:
    address: ":80"
    http:
      redirections:
        entryPoint:
          to: websecure
          scheme: https
  websecure:
    address: ":443"
  mqtt:
    address: ":1883"
  mqtt-secure:
    address: ":8883"

certificatesResolvers:
  letsencrypt:
    acme:
      email: admin@example.com
      storage: /letsencrypt/acme.json
      httpChallenge:
        entryPoint: web

providers:
  docker:
    exposedByDefault: false
  file:
    directory: /etc/traefik/dynamic
```

**Routes:**
- `/` → React Frontend (SPA)
- `/api/*` → FastAPI Backend
- `/grafana/*` → Grafana Dashboards
- `/nodered/*` → Node-RED UI
- `/minio/*` → MinIO Console
- `mqtt://` → Mosquitto Broker

**Features:**
- Automatic SSL with Let's Encrypt
- HTTP/2 and WebSocket support
- Rate limiting and DDoS protection
- Circuit breakers and retry logic
- Distributed tracing (Jaeger integration)
- Metrics export to Prometheus

---

## 4. Containerization Strategy

### 4.1 Docker Compose (Development & Single Server)

**File Structure:**
```
iodd-manager/
├── docker-compose.yml              # Main orchestration
├── docker-compose.prod.yml         # Production overrides
├── docker-compose.dev.yml          # Development overrides
├── .env.example                    # Environment template
├── services/
│   ├── api/
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   ├── frontend/
│   │   ├── Dockerfile
│   │   └── nginx.conf
│   ├── mqtt-bridge/
│   │   ├── Dockerfile
│   │   └── bridge.py
│   └── device-shadow/
│       ├── Dockerfile
│       └── shadow_service.py
├── config/
│   ├── mosquitto/
│   │   ├── mosquitto.conf
│   │   ├── passwd
│   │   └── acl
│   ├── traefik/
│   │   ├── traefik.yml
│   │   └── dynamic/
│   ├── grafana/
│   │   ├── dashboards/
│   │   └── datasources/
│   └── nodered/
│       └── flows.json
└── volumes/
    ├── postgres-data/
    ├── influxdb-data/
    ├── redis-data/
    ├── minio-data/
    └── mosquitto-data/
```

**docker-compose.yml:**
```yaml
version: '3.8'

services:
  # Reverse Proxy & Load Balancer
  traefik:
    image: traefik:v2.11
    container_name: iodd-traefik
    command:
      - "--api.dashboard=true"
      - "--providers.docker=true"
      - "--entrypoints.web.address=:80"
      - "--entrypoints.websecure.address=:443"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge=true"
      - "--certificatesresolvers.letsencrypt.acme.httpchallenge.entrypoint=web"
      - "--certificatesresolvers.letsencrypt.acme.email=${ACME_EMAIL}"
      - "--certificatesresolvers.letsencrypt.acme.storage=/letsencrypt/acme.json"
    ports:
      - "80:80"
      - "443:443"
      - "8080:8080"  # Traefik dashboard
    volumes:
      - /var/run/docker.sock:/var/run/docker.sock:ro
      - ./volumes/letsencrypt:/letsencrypt
      - ./config/traefik:/etc/traefik
    networks:
      - iodd-network
    restart: unless-stopped

  # PostgreSQL Database
  postgres:
    image: postgres:16-alpine
    container_name: iodd-postgres
    environment:
      POSTGRES_DB: ${POSTGRES_DB:-iodd_manager}
      POSTGRES_USER: ${POSTGRES_USER:-iodd_user}
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
      PGDATA: /var/lib/postgresql/data/pgdata
    volumes:
      - ./volumes/postgres-data:/var/lib/postgresql/data
    networks:
      - iodd-network
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U ${POSTGRES_USER}"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # InfluxDB Time-Series Database
  influxdb:
    image: influxdb:2.7-alpine
    container_name: iodd-influxdb
    environment:
      DOCKER_INFLUXDB_INIT_MODE: setup
      DOCKER_INFLUXDB_INIT_USERNAME: ${INFLUX_USERNAME:-admin}
      DOCKER_INFLUXDB_INIT_PASSWORD: ${INFLUX_PASSWORD}
      DOCKER_INFLUXDB_INIT_ORG: ${INFLUX_ORG:-iodd-platform}
      DOCKER_INFLUXDB_INIT_BUCKET: ${INFLUX_BUCKET:-iodd_iot}
      DOCKER_INFLUXDB_INIT_ADMIN_TOKEN: ${INFLUX_TOKEN}
    volumes:
      - ./volumes/influxdb-data:/var/lib/influxdb2
    ports:
      - "8086:8086"
    networks:
      - iodd-network
    healthcheck:
      test: ["CMD", "influx", "ping"]
      interval: 30s
      timeout: 10s
      retries: 5
    restart: unless-stopped

  # Redis Cache & Message Queue
  redis:
    image: redis:7-alpine
    container_name: iodd-redis
    command: redis-server --appendonly yes --requirepass ${REDIS_PASSWORD}
    volumes:
      - ./volumes/redis-data:/data
    networks:
      - iodd-network
    healthcheck:
      test: ["CMD", "redis-cli", "--raw", "incr", "ping"]
      interval: 10s
      timeout: 5s
      retries: 5
    restart: unless-stopped

  # Eclipse Mosquitto MQTT Broker
  mosquitto:
    image: eclipse-mosquitto:2.0
    container_name: iodd-mosquitto
    volumes:
      - ./config/mosquitto/mosquitto.conf:/mosquitto/config/mosquitto.conf
      - ./config/mosquitto/passwd:/mosquitto/config/passwd
      - ./config/mosquitto/acl:/mosquitto/config/acl
      - ./volumes/mosquitto-data:/mosquitto/data
      - ./volumes/mosquitto-log:/mosquitto/log
    ports:
      - "1883:1883"  # MQTT
      - "8883:8883"  # MQTT over TLS
      - "9001:9001"  # WebSocket
    networks:
      - iodd-network
    restart: unless-stopped

  # MinIO Object Storage
  minio:
    image: minio/minio:latest
    container_name: iodd-minio
    command: server /data --console-address ":9001"
    environment:
      MINIO_ROOT_USER: ${MINIO_ROOT_USER:-minioadmin}
      MINIO_ROOT_PASSWORD: ${MINIO_ROOT_PASSWORD}
    volumes:
      - ./volumes/minio-data:/data
    ports:
      - "9000:9000"
      - "9001:9001"
    networks:
      - iodd-network
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:9000/minio/health/live"]
      interval: 30s
      timeout: 10s
      retries: 3
    restart: unless-stopped

  # Grafana Dashboards
  grafana:
    image: grafana/grafana:latest
    container_name: iodd-grafana
    environment:
      GF_SECURITY_ADMIN_USER: ${GRAFANA_ADMIN_USER:-admin}
      GF_SECURITY_ADMIN_PASSWORD: ${GRAFANA_ADMIN_PASSWORD}
      GF_INSTALL_PLUGINS: grafana-clock-panel,grafana-simple-json-datasource
      GF_SERVER_ROOT_URL: ${GRAFANA_ROOT_URL:-http://localhost:3000}
    volumes:
      - ./volumes/grafana-data:/var/lib/grafana
      - ./config/grafana/dashboards:/etc/grafana/provisioning/dashboards
      - ./config/grafana/datasources:/etc/grafana/provisioning/datasources
    ports:
      - "3000:3000"
    networks:
      - iodd-network
    depends_on:
      - influxdb
      - postgres
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.grafana.rule=Host(`grafana.${DOMAIN}`)"
      - "traefik.http.routers.grafana.entrypoints=websecure"
      - "traefik.http.routers.grafana.tls.certresolver=letsencrypt"

  # Node-RED Workflow Automation
  nodered:
    image: nodered/node-red:latest
    container_name: iodd-nodered
    environment:
      TZ: ${TIMEZONE:-America/New_York}
      NODE_RED_ENABLE_PROJECTS: "true"
    volumes:
      - ./volumes/nodered-data:/data
      - ./config/nodered:/data/settings
    ports:
      - "1880:1880"
    networks:
      - iodd-network
    depends_on:
      - mosquitto
      - influxdb
      - redis
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.nodered.rule=Host(`nodered.${DOMAIN}`)"
      - "traefik.http.routers.nodered.entrypoints=websecure"
      - "traefik.http.routers.nodered.tls.certresolver=letsencrypt"

  # FastAPI Backend
  api:
    build:
      context: ./services/api
      dockerfile: Dockerfile
    container_name: iodd-api
    environment:
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
      INFLUXDB_URL: http://influxdb:8086
      INFLUXDB_TOKEN: ${INFLUX_TOKEN}
      INFLUXDB_ORG: ${INFLUX_ORG}
      INFLUXDB_BUCKET: ${INFLUX_BUCKET}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0
      MQTT_BROKER: mosquitto:1883
      MQTT_USERNAME: ${MQTT_USERNAME}
      MQTT_PASSWORD: ${MQTT_PASSWORD}
      S3_ENDPOINT: http://minio:9000
      S3_ACCESS_KEY: ${MINIO_ROOT_USER}
      S3_SECRET_KEY: ${MINIO_ROOT_PASSWORD}
    volumes:
      - ./volumes/iodd-uploads:/uploads
      - ./volumes/iodd-backups:/backups
    networks:
      - iodd-network
    depends_on:
      - postgres
      - influxdb
      - redis
      - mosquitto
      - minio
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.api.rule=Host(`api.${DOMAIN}`) || PathPrefix(`/api`)"
      - "traefik.http.routers.api.entrypoints=websecure"
      - "traefik.http.routers.api.tls.certresolver=letsencrypt"
      - "traefik.http.services.api.loadbalancer.server.port=8000"

  # React Frontend
  frontend:
    build:
      context: ./services/frontend
      dockerfile: Dockerfile
    container_name: iodd-frontend
    networks:
      - iodd-network
    depends_on:
      - api
    restart: unless-stopped
    labels:
      - "traefik.enable=true"
      - "traefik.http.routers.frontend.rule=Host(`${DOMAIN}`)"
      - "traefik.http.routers.frontend.entrypoints=websecure"
      - "traefik.http.routers.frontend.tls.certresolver=letsencrypt"
      - "traefik.http.services.frontend.loadbalancer.server.port=80"

  # MQTT Bridge Service
  mqtt-bridge:
    build:
      context: ./services/mqtt-bridge
      dockerfile: Dockerfile
    container_name: iodd-mqtt-bridge
    environment:
      MQTT_BROKER: mosquitto:1883
      MQTT_USERNAME: ${MQTT_USERNAME}
      MQTT_PASSWORD: ${MQTT_PASSWORD}
      INFLUXDB_URL: http://influxdb:8086
      INFLUXDB_TOKEN: ${INFLUX_TOKEN}
      INFLUXDB_ORG: ${INFLUX_ORG}
      INFLUXDB_BUCKET: ${INFLUX_BUCKET}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0
    networks:
      - iodd-network
    depends_on:
      - mosquitto
      - influxdb
      - redis
    restart: unless-stopped

  # Device Shadow Service
  device-shadow:
    build:
      context: ./services/device-shadow
      dockerfile: Dockerfile
    container_name: iodd-device-shadow
    environment:
      MQTT_BROKER: mosquitto:1883
      MQTT_USERNAME: ${MQTT_USERNAME}
      MQTT_PASSWORD: ${MQTT_PASSWORD}
      REDIS_URL: redis://:${REDIS_PASSWORD}@redis:6379/0
      DATABASE_URL: postgresql://${POSTGRES_USER}:${POSTGRES_PASSWORD}@postgres:5432/${POSTGRES_DB}
    networks:
      - iodd-network
    depends_on:
      - mosquitto
      - redis
      - postgres
    restart: unless-stopped

  # Prometheus Monitoring
  prometheus:
    image: prom/prometheus:latest
    container_name: iodd-prometheus
    volumes:
      - ./config/prometheus/prometheus.yml:/etc/prometheus/prometheus.yml
      - ./volumes/prometheus-data:/prometheus
    command:
      - '--config.file=/etc/prometheus/prometheus.yml'
      - '--storage.tsdb.path=/prometheus'
    ports:
      - "9090:9090"
    networks:
      - iodd-network
    restart: unless-stopped

networks:
  iodd-network:
    driver: bridge

volumes:
  postgres-data:
  influxdb-data:
  redis-data:
  mosquitto-data:
  mosquitto-log:
  minio-data:
  grafana-data:
  nodered-data:
  prometheus-data:
```

### 4.2 Kubernetes (Production & Cloud)

**Namespace Structure:**
```yaml
# namespaces.yaml
apiVersion: v1
kind: Namespace
metadata:
  name: iodd-platform
---
apiVersion: v1
kind: Namespace
metadata:
  name: iodd-monitoring
```

**Deployment Strategy:**
- **Helm Charts** for easy deployment and upgrades
- **StatefulSets** for databases (PostgreSQL, InfluxDB, Redis)
- **Deployments** for stateless services (API, Frontend, MQTT Bridge)
- **DaemonSets** for node-level monitoring agents
- **ConfigMaps** for configuration
- **Secrets** for sensitive data
- **PersistentVolumeClaims** for data persistence
- **Horizontal Pod Autoscalers** for auto-scaling
- **NetworkPolicies** for service isolation

**Example Service Deployment:**
```yaml
# api-deployment.yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: iodd-api
  namespace: iodd-platform
spec:
  replicas: 3
  selector:
    matchLabels:
      app: iodd-api
  template:
    metadata:
      labels:
        app: iodd-api
        version: v2.1.0
    spec:
      containers:
      - name: api
        image: ghcr.io/me-catalyst/iodd-manager-api:v2.1.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABASE_URL
          valueFrom:
            secretKeyRef:
              name: database-credentials
              key: url
        resources:
          requests:
            memory: "512Mi"
            cpu: "500m"
          limits:
            memory: "2Gi"
            cpu: "2000m"
        livenessProbe:
          httpGet:
            path: /health
            port: 8000
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /ready
            port: 8000
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: iodd-api
  namespace: iodd-platform
spec:
  selector:
    app: iodd-api
  ports:
  - protocol: TCP
    port: 8000
    targetPort: 8000
  type: ClusterIP
---
apiVersion: autoscaling/v2
kind: HorizontalPodAutoscaler
metadata:
  name: iodd-api-hpa
  namespace: iodd-platform
spec:
  scaleTargetRef:
    apiVersion: apps/v1
    kind: Deployment
    name: iodd-api
  minReplicas: 3
  maxReplicas: 20
  metrics:
  - type: Resource
    resource:
      name: cpu
      target:
        type: Utilization
        averageUtilization: 70
  - type: Resource
    resource:
      name: memory
      target:
        type: Utilization
        averageUtilization: 80
```

---

## 5. Scalability Design

### 5.1 Scalability Tiers

| Tier | Devices | Users | Infrastructure | Estimated Cost/Month |
|------|---------|-------|----------------|---------------------|
| **Development** | 1-10 | 1-5 | Docker Compose on local PC | $0 |
| **Small Factory** | 10-100 | 5-20 | Single server (16GB RAM, 4 CPU) | $50-100 |
| **Medium Factory** | 100-1,000 | 20-100 | 2-3 servers or small K8s cluster | $200-500 |
| **Large Enterprise** | 1,000-10,000 | 100-500 | K8s cluster (5-10 nodes) | $1,000-3,000 |
| **Global Enterprise** | 10,000+ | 500+ | Multi-region K8s, managed services | $5,000+ |

### 5.2 Horizontal Scaling Components

**Stateless Services (Easy to Scale):**
- ✅ FastAPI Backend (scale to N replicas)
- ✅ Frontend Static Server (CDN distribution)
- ✅ MQTT Bridge Service (parallel processing)
- ✅ Device Shadow Service (sharded by device ID)
- ✅ Node-RED (separate flow instances)

**Stateful Services (Requires Planning):**
- 🔄 PostgreSQL (read replicas, sharding, Patroni clustering)
- 🔄 InfluxDB (Enterprise clustering, sharding by time/device)
- 🔄 Redis (Redis Cluster, Sentinel)
- 🔄 Mosquitto (MQTT bridge pattern, shared subscriptions)
- 🔄 MinIO (distributed mode, 4+ nodes)

### 5.3 Database Sharding Strategy

**PostgreSQL Sharding (10,000+ devices):**
```sql
-- Shard by device vendor_id hash
CREATE TABLE devices_shard_0 (
  LIKE devices INCLUDING ALL
) PARTITION OF devices FOR VALUES WITH (MODULUS 4, REMAINDER 0);

CREATE TABLE devices_shard_1 (
  LIKE devices INCLUDING ALL
) PARTITION OF devices FOR VALUES WITH (MODULUS 4, REMAINDER 1);

-- Citus extension for distributed tables
SELECT create_distributed_table('devices', 'vendor_id');
```

**InfluxDB Sharding:**
- Shard by time (automatic)
- Shard by `site` tag for multi-site deployments
- Separate InfluxDB instances per geographic region

### 5.4 Load Balancing

**API Load Balancing:**
- Round-robin by default
- Sticky sessions for WebSocket connections
- Health check-based routing
- Geographic routing for multi-region

**MQTT Load Balancing:**
- Shared subscriptions: `$share/group/devices/#`
- MQTT bridge to multiple brokers
- Topic-based routing (shard by device_id prefix)

### 5.5 Caching Strategy

**Multi-Level Caching:**
```
Browser Cache (1 hour)
  ↓
CDN Cache (CloudFlare - 24 hours)
  ↓
Nginx Cache (5 minutes)
  ↓
Redis Cache (configurable TTL)
  ↓
Database (source of truth)
```

**Cache Invalidation:**
- Event-driven invalidation via Redis pub/sub
- TTL-based expiration
- Manual purge via admin API

---

## 6. Data Flow Architecture

### 6.1 Device Telemetry Flow

```
┌─────────────┐
│   Device    │ (IO-Link Master, EtherNet/IP Adapter)
│   Hardware  │
└──────┬──────┘
       │ 1. Publish telemetry
       │    Topic: devices/{device_id}/telemetry
       │    Payload: {"param": "Distance", "value": 1234.56, "ts": 1735689600}
       ▼
┌─────────────────────┐
│  MQTT Broker        │
│  (Mosquitto)        │
└──────┬──────────────┘
       │ 2. Subscribe to topics
       ▼
┌─────────────────────┐
│  MQTT Bridge        │
│  Service            │
└──────┬──────────────┘
       │ 3. Enrich with IODD metadata
       │    (lookup parameter details, units, ranges)
       ▼
┌─────────────────────┐
│  InfluxDB           │
│  (Time-Series DB)   │
└──────┬──────────────┘
       │ 4. Query for visualization
       ▼
┌─────────────────────┐
│  Grafana            │
│  Dashboard          │
└─────────────────────┘
```

### 6.2 Device Command Flow

```
┌─────────────┐
│  Web UI     │
│  (React)    │
└──────┬──────┘
       │ 1. User initiates command
       │    POST /api/devices/{id}/command
       │    {"parameter": "SamplingRate", "value": 1000}
       ▼
┌─────────────────────┐
│  FastAPI Backend    │
└──────┬──────────────┘
       │ 2. Validate command using IODD
       │    (check access rights, data type, range)
       ▼
┌─────────────────────┐
│  MQTT Broker        │
└──────┬──────────────┘
       │ 3. Publish command
       │    Topic: devices/{device_id}/commands
       │    Payload: {"param": "SamplingRate", "value": 1000, "id": "cmd-123"}
       ▼
┌─────────────┐
│   Device    │
│   Hardware  │
└──────┬──────┘
       │ 4. Execute & acknowledge
       │    Topic: devices/{device_id}/ack
       │    Payload: {"cmd_id": "cmd-123", "status": "success"}
       ▼
┌─────────────────────┐
│  Device Shadow      │
│  Service (Redis)    │
└─────────────────────┘
```

### 6.3 Workflow Automation Flow

```
┌─────────────────────┐
│  InfluxDB           │
│  Alert Query        │
│  (Temperature > 80) │
└──────┬──────────────┘
       │ 1. Threshold exceeded
       ▼
┌─────────────────────┐
│  Node-RED           │
│  Flow Trigger       │
└──────┬──────────────┘
       │ 2. Enrich with device info
       │    HTTP GET /api/devices/{id}
       ▼
┌─────────────────────┐
│  IODD Manager API   │
└──────┬──────────────┘
       │ 3. Return device details
       ▼
┌─────────────────────┐
│  Node-RED           │
│  Decision Logic     │
└──────┬──────────────┘
       │ 4. Create ticket
       │    POST /api/tickets
       │
       │ 5. Send notification
       ├─────────────► Email/Slack
       │
       │ 6. Log to database
       └─────────────► PostgreSQL
```

---

## 7. Security Architecture

### 7.1 Authentication & Authorization

**Multi-Tier Authentication:**

1. **User Authentication (Web UI, API):**
   - OAuth2 / OpenID Connect (Keycloak, Auth0, Okta)
   - LDAP/Active Directory integration
   - JWT token-based sessions
   - Role-Based Access Control (RBAC)

2. **Device Authentication (MQTT):**
   - X.509 certificates (mutual TLS)
   - Username/password (hashed in mosquitto passwd file)
   - Token-based authentication (JWT)
   - Device provisioning service

3. **Service-to-Service Authentication:**
   - API keys with rotation
   - mTLS between services
   - Service mesh (Istio) with automatic mTLS

**RBAC Roles:**
```yaml
roles:
  - name: admin
    permissions:
      - devices:*
      - users:*
      - system:*
      - mqtt:publish:*
      - mqtt:subscribe:*

  - name: operator
    permissions:
      - devices:read
      - devices:command
      - telemetry:read
      - mqtt:publish:devices/+/commands
      - mqtt:subscribe:devices/+/telemetry

  - name: viewer
    permissions:
      - devices:read
      - telemetry:read
      - mqtt:subscribe:devices/+/telemetry

  - name: device
    permissions:
      - mqtt:publish:devices/${client_id}/telemetry
      - mqtt:subscribe:devices/${client_id}/commands
```

### 7.2 Network Security

**Network Segmentation:**
```
┌─────────────────────────────────────────────────────────┐
│  Public Internet                                        │
└─────────────────────────────────────────────────────────┘
                          │
                ┌─────────▼─────────┐
                │   DMZ Network     │  (Traefik, WAF)
                └─────────┬─────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼────────┐    ┌───────▼────────┐   ┌───────▼────────┐
│ Frontend   │    │  API Gateway   │   │  MQTT Broker   │
│ (DMZ)      │    │  (DMZ)         │   │  (DMZ)         │
└────────────┘    └────────────────┘   └────────────────┘
                          │
                ┌─────────▼─────────┐
                │  Internal Network │  (VPC/VLAN)
                └─────────┬─────────┘
                          │
    ┌─────────────────────┼─────────────────────┐
    │                     │                     │
┌───▼────────┐    ┌───────▼────────┐   ┌───────▼────────┐
│ Services   │    │   Databases    │   │   Storage      │
│ (Private)  │    │   (Private)    │   │   (Private)    │
└────────────┘    └────────────────┘   └────────────────┘
```

**Firewall Rules:**
- Only Traefik exposed to public (ports 80, 443, 8883)
- Database ports only accessible from internal network
- MQTT broker has separate public/private listeners

### 7.3 Data Encryption

**Encryption at Rest:**
- PostgreSQL: Transparent Data Encryption (TDE)
- InfluxDB: File system encryption (LUKS, BitLocker)
- MinIO: Server-Side Encryption (SSE-S3)
- Secrets: Encrypted with Kubernetes secrets or HashiCorp Vault

**Encryption in Transit:**
- All HTTP traffic over TLS 1.3
- MQTT over TLS (port 8883)
- mTLS between internal services
- WebSocket Secure (WSS)

### 7.4 Secrets Management

**Development:** `.env` files (git-ignored)

**Production:**
- Kubernetes Secrets (base64 encoded)
- HashiCorp Vault (recommended)
- AWS Secrets Manager / Azure Key Vault
- Sealed Secrets (encrypted in Git)

**Secret Rotation:**
- Automated rotation every 90 days
- Zero-downtime rotation with dual-key periods
- Audit logging of all secret access

### 7.5 Compliance & Auditing

**Audit Logging:**
- All API calls logged with user, timestamp, action
- Database changes tracked with audit tables
- MQTT messages logged (configurable retention)
- Login attempts and failures tracked

**Compliance:**
- GDPR compliance (user data deletion, export)
- SOC 2 Type II (access controls, encryption)
- ISO 27001 (security management)
- IEC 62443 (industrial security)

---

## 8. Deployment Scenarios

### 8.1 Local Development

**Command:**
```bash
git clone https://github.com/ME-Catalyst/iodd-manager.git
cd iodd-manager
cp .env.example .env
# Edit .env with your settings
docker-compose up -d
```

**Access:**
- Frontend: http://localhost:5173
- API: http://localhost:8000
- Grafana: http://localhost:3000
- Node-RED: http://localhost:1880
- MinIO Console: http://localhost:9001

**Resources:** 8GB RAM, 4 CPU cores

### 8.2 Single Server (Small Factory)

**Hardware:** Dell PowerEdge R340, 32GB RAM, 8 cores, 1TB SSD

**Installation:**
```bash
# Install Docker
curl -fsSL https://get.docker.com | sh

# Clone repository
git clone https://github.com/ME-Catalyst/iodd-manager.git
cd iodd-manager

# Configure for production
cp .env.example .env
nano .env  # Set production passwords, domain

# Deploy with production config
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up -d

# Setup SSL
./scripts/setup-ssl.sh your-domain.com
```

**Backup Strategy:**
```bash
# Automated daily backups
0 2 * * * /opt/iodd-manager/scripts/backup.sh
```

### 8.3 Kubernetes (Cloud or On-Premise)

**Prerequisites:**
- Kubernetes cluster (1.24+)
- kubectl configured
- Helm 3.x

**Installation:**
```bash
# Add Helm repository
helm repo add iodd-platform https://charts.iodd-manager.io
helm repo update

# Install with custom values
helm install iodd-platform iodd-platform/iodd-manager \
  --namespace iodd-platform \
  --create-namespace \
  --values production-values.yaml

# Verify deployment
kubectl get pods -n iodd-platform
```

**production-values.yaml:**
```yaml
global:
  domain: iodd.example.com
  storageClass: fast-ssd

api:
  replicaCount: 3
  resources:
    requests:
      memory: 512Mi
      cpu: 500m
    limits:
      memory: 2Gi
      cpu: 2000m
  autoscaling:
    enabled: true
    minReplicas: 3
    maxReplicas: 20
    targetCPUUtilizationPercentage: 70

postgres:
  enabled: true
  primary:
    persistence:
      size: 100Gi
  readReplicas:
    replicaCount: 2

influxdb:
  enabled: true
  persistence:
    size: 500Gi
  resources:
    requests:
      memory: 4Gi
      cpu: 2000m

redis:
  enabled: true
  cluster:
    enabled: true
    nodes: 6

mosquitto:
  enabled: true
  replicaCount: 3
  persistence:
    size: 50Gi

minio:
  enabled: true
  mode: distributed
  replicas: 4
  persistence:
    size: 1Ti

grafana:
  enabled: true
  persistence:
    size: 10Gi

nodered:
  enabled: true
  persistence:
    size: 10Gi
```

### 8.4 Multi-Region Deployment

**Architecture:**
```
           ┌──────────────────────────────────┐
           │   Global Load Balancer           │
           │   (CloudFlare, Route53)          │
           └────────────┬─────────────────────┘
                        │
        ┌───────────────┼───────────────┐
        │               │               │
   ┌────▼──────┐  ┌────▼──────┐  ┌────▼──────┐
   │  Region   │  │  Region   │  │  Region   │
   │  US-East  │  │  EU-West  │  │  AP-South │
   └───────────┘  └───────────┘  └───────────┘
        │               │               │
        └───────────────┼───────────────┘
                        │
                 ┌──────▼──────┐
                 │  Global     │
                 │  PostgreSQL │
                 │  (CockroachDB)
                 └─────────────┘
```

**Data Residency:**
- Telemetry data stays in region (InfluxDB per region)
- Configuration data globally replicated (CockroachDB)
- Cross-region MQTT bridges for device mobility

---

## 9. Implementation Roadmap

### Phase 1: Foundation (Months 1-2)

**Goals:** Containerize existing application, add PostgreSQL support

**Tasks:**
- [ ] Create Dockerfiles for all services
- [ ] Write docker-compose.yml with basic stack
- [ ] Migrate from SQLite to PostgreSQL (optional for production)
- [ ] Add health checks and monitoring endpoints
- [ ] Create one-click deployment script
- [ ] Write basic deployment documentation

**Deliverables:**
- Docker Compose setup working locally
- Documentation for Docker deployment
- Automated build/test pipeline

### Phase 2: MQTT & Real-Time (Months 3-4)

**Goals:** Add MQTT broker and device communication

**Tasks:**
- [ ] Deploy Eclipse Mosquitto in Docker Compose
- [ ] Implement MQTT authentication and ACLs
- [ ] Create MQTT Bridge Service (Python)
  - Subscribe to device telemetry topics
  - Parse and validate messages
  - Write to InfluxDB
- [ ] Add MQTT client library to React frontend
  - Real-time telemetry display
  - Live device status updates
- [ ] Implement device shadow service (Redis)
- [ ] Create device simulator for testing
- [ ] Add MQTT API endpoints
  - GET /api/mqtt/status
  - POST /api/devices/{id}/publish

**Deliverables:**
- Working MQTT infrastructure
- Real-time telemetry ingestion
- Device shadow service
- Testing utilities

### Phase 3: Time-Series & Analytics (Months 5-6)

**Goals:** Add InfluxDB and Grafana for analytics

**Tasks:**
- [ ] Deploy InfluxDB 2.x in Docker Compose
- [ ] Design InfluxDB schema for telemetry
- [ ] Implement InfluxDB write pipeline
  - Batch writes for performance
  - Error handling and retries
- [ ] Create retention policies and downsampling
- [ ] Deploy Grafana with datasources
- [ ] Build 5-10 starter dashboards
  - Factory floor overview
  - Device detail view
  - System health
- [ ] Add API endpoints for historical data
  - GET /api/telemetry/{device_id}/history
  - GET /api/telemetry/aggregate
- [ ] Implement InfluxDB alerting rules

**Deliverables:**
- Time-series database operational
- Historical data query API
- Production-ready dashboards
- Alerting system

### Phase 4: Workflow Automation (Months 7-8)

**Goals:** Add Node-RED and custom nodes

**Tasks:**
- [ ] Deploy Node-RED in Docker Compose
- [ ] Create custom Node-RED nodes
  - `iodd-device-lookup`
  - `iodd-parameter-mapper`
  - `iodd-command-builder`
- [ ] Build 10 example flows
  - Device onboarding
  - Alert processing
  - Data transformation
  - Ticket creation
- [ ] Implement flow import/export API
- [ ] Add Node-RED UI to main frontend
  - Embedded iframe with SSO
- [ ] Create flow templates library
- [ ] Write workflow documentation

**Deliverables:**
- Node-RED integration
- Custom IODD nodes
- Example workflows
- User documentation

### Phase 5: Object Storage & Backups (Month 9)

**Goals:** Add MinIO and automated backups

**Tasks:**
- [ ] Deploy MinIO in Docker Compose
- [ ] Create S3 buckets for different data types
- [ ] Migrate file uploads to MinIO
  - IODD/EDS files
  - Ticket attachments
  - Firmware files
- [ ] Implement backup automation
  - Daily PostgreSQL backups to MinIO
  - Weekly full system backups
  - 90-day retention policy
- [ ] Add backup/restore API endpoints
- [ ] Create backup monitoring dashboard

**Deliverables:**
- S3-compatible object storage
- Automated backup system
- Restore procedures documented

### Phase 6: Scalability & Production (Months 10-11)

**Goals:** Kubernetes deployment, auto-scaling

**Tasks:**
- [ ] Create Kubernetes manifests
  - Deployments, Services, ConfigMaps
  - StatefulSets for databases
  - PersistentVolumeClaims
- [ ] Create Helm chart
  - Parameterized values
  - Sub-charts for dependencies
- [ ] Implement horizontal pod autoscaling
- [ ] Set up Prometheus monitoring
- [ ] Configure Traefik ingress
- [ ] Implement database sharding
- [ ] Load testing and optimization
- [ ] Write Kubernetes deployment guide

**Deliverables:**
- Production-ready Kubernetes deployment
- Helm chart published
- Performance benchmarks
- Deployment automation

### Phase 7: Security & Compliance (Month 12)

**Goals:** Harden security, add compliance features

**Tasks:**
- [ ] Implement OAuth2/OIDC authentication
- [ ] Add RBAC to all services
- [ ] Enable encryption at rest
- [ ] Configure mTLS between services
- [ ] Implement audit logging
- [ ] Add GDPR compliance features
  - User data export
  - Right to be forgotten
- [ ] Security scanning and hardening
- [ ] Penetration testing
- [ ] Write security documentation

**Deliverables:**
- Enterprise-grade security
- Compliance certifications
- Security audit report

### Phase 8: Advanced Features (Ongoing)

**Goals:** Edge computing, ML/AI, advanced analytics

**Ideas:**
- [ ] Edge agent for local processing
- [ ] Machine learning for predictive maintenance
- [ ] Anomaly detection
- [ ] Digital twin simulation
- [ ] AR/VR device visualization
- [ ] Voice control integration
- [ ] Mobile apps (iOS/Android)
- [ ] OPC UA server integration
- [ ] Modbus/Profinet support

---

## 10. Technical Specifications

### 10.1 API Additions

**New Endpoints:**

```python
# MQTT Management
GET    /api/mqtt/status
POST   /api/mqtt/publish
GET    /api/mqtt/topics
POST   /api/devices/{id}/command

# Time-Series Data
GET    /api/telemetry/{device_id}/current
GET    /api/telemetry/{device_id}/history
GET    /api/telemetry/aggregate
POST   /api/telemetry/query  # InfluxQL/Flux query

# Device Shadow
GET    /api/devices/{id}/shadow
PATCH  /api/devices/{id}/shadow/desired
GET    /api/devices/{id}/shadow/reported

# Workflows
GET    /api/workflows
POST   /api/workflows
GET    /api/workflows/{id}
PUT    /api/workflows/{id}
DELETE /api/workflows/{id}
POST   /api/workflows/{id}/deploy

# Storage
GET    /api/storage/buckets
POST   /api/storage/upload
GET    /api/storage/download/{key}

# Backup/Restore
POST   /api/admin/backup
GET    /api/admin/backups
POST   /api/admin/restore/{backup_id}
```

### 10.2 MQTT Topic Schema

```
devices/
  {device_id}/
    register          # Device registration (QoS 1)
    telemetry         # Real-time sensor data (QoS 0)
    telemetry/batch   # Batched telemetry (QoS 1)
    status            # Online/offline status (QoS 1, retain)
    commands          # Commands to device (QoS 1)
    commands/ack      # Command acknowledgments (QoS 1)
    config/desired    # Desired configuration (QoS 1, retain)
    config/reported   # Reported configuration (QoS 1, retain)
    logs              # Device logs (QoS 0)
    alarms            # Device alarms (QoS 1)

system/
  alerts/             # System-wide alerts
  metrics/            # Platform metrics
```

### 10.3 Database Schema Updates

**New PostgreSQL Tables:**

```sql
-- Device Shadow / Digital Twin
CREATE TABLE device_shadows (
  device_id VARCHAR(255) PRIMARY KEY REFERENCES devices(id),
  connection_state VARCHAR(50), -- connected, disconnected
  last_seen TIMESTAMP,
  desired_config JSONB,
  reported_config JSONB,
  metadata JSONB,
  version INTEGER DEFAULT 1,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- MQTT Topics Registry
CREATE TABLE mqtt_topics (
  id SERIAL PRIMARY KEY,
  topic VARCHAR(500) UNIQUE NOT NULL,
  description TEXT,
  qos INTEGER,
  retain BOOLEAN,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Workflows
CREATE TABLE workflows (
  id SERIAL PRIMARY KEY,
  name VARCHAR(255) NOT NULL,
  description TEXT,
  flow_json JSONB NOT NULL,
  enabled BOOLEAN DEFAULT TRUE,
  created_by VARCHAR(255),
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Alerts / Notifications
CREATE TABLE alerts (
  id SERIAL PRIMARY KEY,
  device_id VARCHAR(255) REFERENCES devices(id),
  severity VARCHAR(50), -- info, warning, error, critical
  title VARCHAR(255),
  message TEXT,
  source VARCHAR(100), -- mqtt, influxdb, system
  acknowledged BOOLEAN DEFAULT FALSE,
  acknowledged_by VARCHAR(255),
  acknowledged_at TIMESTAMP,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
```

### 10.4 Performance Targets

| Metric | Target | Measurement |
|--------|--------|-------------|
| **API Response Time** | < 100ms (p95) | Prometheus histogram |
| **MQTT Message Latency** | < 50ms (p99) | End-to-end telemetry |
| **InfluxDB Write Throughput** | 100,000+ points/sec | Load testing |
| **Database Queries** | < 50ms (p95) | APM tools |
| **WebSocket Latency** | < 20ms (real-time data) | Client-side measurement |
| **System Uptime** | 99.9% (8.76 hours downtime/year) | Monitoring dashboards |
| **Device Onboarding** | < 5 seconds | End-to-end automation |
| **Dashboard Load Time** | < 2 seconds | Lighthouse scores |

---

## 11. Cost Analysis

### 11.1 Development Costs

**Personnel (12-month project):**
- 1 Senior Full-Stack Engineer: $150k/year
- 1 DevOps Engineer: $130k/year
- 1 UI/UX Designer (part-time): $40k
- **Total:** $320k

**Infrastructure (Development):**
- GitHub private repos: $0 (public repo)
- CI/CD (GitHub Actions): $0 (free tier)
- Cloud testing environment: $200/month × 12 = $2,400
- **Total:** $2,400

### 11.2 Operational Costs (Per Year)

**Small Deployment (100 devices):**
- Single server (32GB RAM, 8 core): $100/month
- Domain + SSL: $50/year
- Backup storage: $20/month
- **Total:** ~$1,500/year

**Medium Deployment (1,000 devices):**
- 3-node Kubernetes cluster: $500/month
- Managed PostgreSQL: $200/month
- S3 storage: $100/month
- Monitoring: $100/month
- **Total:** ~$12,000/year

**Large Deployment (10,000 devices):**
- Kubernetes cluster (10 nodes): $2,000/month
- Managed databases: $1,000/month
- Object storage: $500/month
- CDN + monitoring: $500/month
- Support contracts: $1,000/month
- **Total:** ~$60,000/year

### 11.3 ROI Analysis

**Value Delivered:**
- Reduced device commissioning time: 80% faster (10 min → 2 min)
- Predictive maintenance: 30% reduction in downtime
- Centralized monitoring: 50% faster troubleshooting
- Automation: 70% reduction in manual tasks

**Break-Even:**
- For 1,000 devices saving 8 minutes each = 133 hours/year
- At $100/hour engineering time = $13,300 value
- Platform cost $12,000/year → ROI: 110%

---

## 12. Success Metrics

### 12.1 Technical Metrics

- ✅ 99.9% uptime
- ✅ Support 10,000 concurrent devices
- ✅ < 100ms API response time
- ✅ 100,000 MQTT messages/second
- ✅ 1 million data points/second to InfluxDB
- ✅ < 2 second dashboard load time
- ✅ Zero data loss during failover

### 12.2 Business Metrics

- ✅ 50+ production deployments in year 1
- ✅ 10,000+ devices managed
- ✅ 100+ active users
- ✅ 90% user satisfaction score
- ✅ < 5 minute device onboarding time
- ✅ 80% reduction in manual configuration
- ✅ 30% reduction in unexpected downtime

### 12.3 Community Metrics

- ✅ 1,000+ GitHub stars
- ✅ 50+ contributors
- ✅ 100+ community-built Node-RED flows
- ✅ Active forum/Discord community
- ✅ Monthly webinars/demos
- ✅ Conference presentations

---

## Conclusion

This proposal outlines a comprehensive transformation of IODD Manager into an enterprise-grade Industrial IoT platform. The modular, containerized architecture enables:

- **Rapid Deployment:** One-command setup on any PC
- **Massive Scalability:** From 10 to 10,000+ devices
- **Flexibility:** Docker Compose for small deployments, Kubernetes for enterprise
- **Real-Time Capabilities:** MQTT for instant device communication
- **Analytics:** Time-series data with powerful querying and visualization
- **Automation:** Visual workflows for complex integrations
- **Production-Ready:** Security, monitoring, and compliance built-in

The 12-month implementation roadmap provides a clear path forward with incremental value delivery. Each phase builds on the previous, allowing early adoption and feedback.

**Total Investment:** ~$320k development + $10-60k/year operational costs
**Expected ROI:** 110%+ for typical 1,000-device deployment

**Next Steps:**
1. Review and approve this proposal
2. Allocate budget and resources
3. Begin Phase 1 (Foundation) development
4. Set up project management and tracking
5. Engage with early adopter partners

---

**Document Version:** 1.0
**Last Updated:** January 2025
**Maintained By:** IODD Manager Development Team
