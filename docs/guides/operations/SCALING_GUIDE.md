# GreenStack Scaling Guide

This guide outlines how to scale the GreenStack platform from a single host to a horizontally scaled deployment that serves hundreds of concurrent users.

## Current Capacity Baseline
- **Reference host:** 4 vCPU / 8 GB RAM
- **Validated throughput:** 50–75 concurrent users (API + frontend)
- **Primary bottlenecks:** synchronous parsing jobs, database I/O, and Redis cache misses

## Monitoring Thresholds (Scale Triggers)
- CPU utilization sustained above **70%** for 15 minutes
- Memory utilization above **85%**
- API latency **p95 > 1 second**
- Redis cache hit rate **< 80%**
- Postgres connections > 80% of pool capacity

Instrument these via Prometheus/Grafana dashboards defined in `deployment/monitoring/`.

## Phase 1 – Immediate Optimizations
1. Enable SQLAlchemy connection pooling (PgBouncer or SQLAlchemy pool).
2. Turn on Redis caching (`scripts/setup.bat` and `docker-compose.yml` already provision Redis).
3. Run periodic `VACUUM ANALYZE` on PostgreSQL.
4. Move background parsing jobs to a dedicated worker (Celery/RQ).

**Target improvement:** 30% latency reduction, 2× throughput.

## Phase 2 – Vertical Scaling
1. Upgrade host to 8 vCPU / 16 GB RAM.
2. Allocate dedicated volume for Postgres with provisioned IOPS.
3. Increase Gunicorn/Uvicorn workers (2 × CPU cores).
4. Pin Redis to RAM-backed instances.

**Target capacity:** 200 concurrent users, parsing queue under 10 seconds.

## Phase 3 – Horizontal Scaling
1. Deploy two+ API instances behind a load balancer (NGINX, Traefik, or AWS ALB).
2. Separate job queue workers (Celery + RabbitMQ/Redis).
3. Host static assets (Vite build) behind a CDN (CloudFront, Azure CDN).
4. Promote PostgreSQL replicas for read-heavy workloads.

**Target capacity:** 500+ concurrent users with <750 ms p95 latency.

## Operational Checklist
- [ ] Update `docs/guides/operations/DEPLOYMENT_RUNBOOK.md` with new host inventory.
- [ ] Ensure `docs/guides/operations/DISASTER_RECOVERY.md` includes replica failover steps.
- [ ] Load-test via `locust` or `k6` before and after each scaling phase.
- [ ] Document queue depth and Redis memory targets in Grafana.
- [ ] Revisit cost projections after each phase.

## References
- `docs/guides/operations/DEPLOYMENT_RUNBOOK.md`
- `docs/guides/operations/DISASTER_RECOVERY.md`
- `docs/guides/operations/MONITORING_SETUP_GUIDE.md`
