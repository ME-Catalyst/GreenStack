#!/bin/bash
###########################################
# GreenStack Health Check Script
# Version: 1.0
# Purpose: Comprehensive system health verification
###########################################

set -euo pipefail

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Configuration
API_URL="${API_URL:-http://localhost:8000}"
GRAFANA_URL="${GRAFANA_URL:-http://localhost:3000}"
INFLUXDB_URL="${INFLUXDB_URL:-http://localhost:8086}"
PROMETHEUS_URL="${PROMETHEUS_URL:-http://localhost:9090}"
NODERED_URL="${NODERED_URL:-http://localhost:1880}"

# Counters
TOTAL_CHECKS=0
PASSED_CHECKS=0
FAILED_CHECKS=0
WARNING_CHECKS=0

# ============================================================================
# Functions
# ============================================================================

check_pass() {
    echo -e "${GREEN}✓${NC} $1"
    ((PASSED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_fail() {
    echo -e "${RED}✗${NC} $1"
    ((FAILED_CHECKS++))
    ((TOTAL_CHECKS++))
}

check_warn() {
    echo -e "${YELLOW}!${NC} $1"
    ((WARNING_CHECKS++))
    ((TOTAL_CHECKS++))
}

section_header() {
    echo ""
    echo -e "${BLUE}═══ $1 ═══${NC}"
}

# ============================================================================
# Health Checks
# ============================================================================

check_docker_services() {
    section_header "Docker Services"

    local services=(
        "greenstack-api"
        "greenstack-postgres"
        "greenstack-redis"
        "greenstack-mosquitto"
        "greenstack-influxdb"
        "greenstack-grafana"
        "greenstack-prometheus"
    )

    for service in "${services[@]}"; do
        if docker ps --format '{{.Names}}' | grep -q "^${service}$"; then
            local status=$(docker inspect --format='{{.State.Health.Status}}' "${service}" 2>/dev/null || echo "no-health-check")

            if [ "${status}" = "healthy" ]; then
                check_pass "${service} is running and healthy"
            elif [ "${status}" = "no-health-check" ]; then
                if docker ps --format '{{.Names}}:{{.Status}}' | grep "^${service}:" | grep -q "Up"; then
                    check_pass "${service} is running (no health check configured)"
                else
                    check_fail "${service} is not running properly"
                fi
            else
                check_warn "${service} is running but health status: ${status}"
            fi
        else
            check_fail "${service} is not running"
        fi
    done
}

check_api_health() {
    section_header "API Health"

    if command -v curl &> /dev/null; then
        local response=$(curl -s -w "%{http_code}" -o /tmp/api_health.json "${API_URL}/api/health" 2>/dev/null || echo "000")

        if [ "${response}" = "200" ]; then
            local status=$(cat /tmp/api_health.json | grep -o '"status":"[^"]*"' | cut -d'"' -f4)

            if [ "${status}" = "healthy" ]; then
                check_pass "API health endpoint returns healthy"

                # Check database connection
                local db_status=$(cat /tmp/api_health.json | grep -o '"database":"[^"]*"' | cut -d'"' -f4)
                if [ "${db_status}" = "connected" ]; then
                    check_pass "Database connection is healthy"
                else
                    check_fail "Database connection failed: ${db_status}"
                fi
            else
                check_fail "API health status: ${status}"
            fi
        else
            check_fail "API health endpoint returned status: ${response}"
        fi

        rm -f /tmp/api_health.json
    else
        check_warn "curl not installed, skipping API health check"
    fi
}

check_database() {
    section_header "Database"

    # Check PostgreSQL connection
    if docker exec greenstack-postgres pg_isready -U iodd_user &>/dev/null; then
        check_pass "PostgreSQL is accepting connections"

        # Check database exists
        local db_exists=$(docker exec greenstack-postgres psql -U iodd_user -lqt 2>/dev/null | cut -d \| -f 1 | grep -w greenstack | wc -l)

        if [ "${db_exists}" -gt 0 ]; then
            check_pass "Database 'greenstack' exists"

            # Check table count
            local table_count=$(docker exec greenstack-postgres psql -U iodd_user -d greenstack -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')

            if [ "${table_count}" -gt 0 ]; then
                check_pass "Database has ${table_count} tables"
            else
                check_warn "Database has no tables (may be new installation)"
            fi
        else
            check_fail "Database 'greenstack' does not exist"
        fi
    else
        check_fail "PostgreSQL is not accepting connections"
    fi
}

check_redis() {
    section_header "Redis Cache"

    if docker exec greenstack-redis redis-cli ping &>/dev/null; then
        check_pass "Redis is responding to PING"

        # Check Redis info
        local redis_version=$(docker exec greenstack-redis redis-cli INFO server 2>/dev/null | grep ^redis_version | cut -d: -f2 | tr -d '\r')
        if [ -n "${redis_version}" ]; then
            check_pass "Redis version: ${redis_version}"
        fi

        # Check memory usage
        local used_memory=$(docker exec greenstack-redis redis-cli INFO memory 2>/dev/null | grep ^used_memory_human | cut -d: -f2 | tr -d '\r')
        if [ -n "${used_memory}" ]; then
            echo -e "  ${BLUE}ℹ${NC} Redis memory usage: ${used_memory}"
        fi
    else
        check_fail "Redis is not responding"
    fi
}

check_mosquitto() {
    section_header "MQTT Broker"

    if docker ps --format '{{.Names}}' | grep -q "greenstack-mosquitto"; then
        check_pass "Mosquitto container is running"

        # Check if mosquitto is listening
        if docker exec greenstack-mosquitto netstat -tln 2>/dev/null | grep -q ":1883"; then
            check_pass "MQTT port 1883 is listening"
        else
            check_warn "MQTT port 1883 may not be listening"
        fi

        # Check TLS port
        if docker exec greenstack-mosquitto netstat -tln 2>/dev/null | grep -q ":8883"; then
            check_pass "MQTT TLS port 8883 is listening"
        else
            check_warn "MQTT TLS port 8883 is not configured"
        fi
    else
        check_fail "Mosquitto container is not running"
    fi
}

check_influxdb() {
    section_header "InfluxDB"

    if command -v curl &> /dev/null; then
        local response=$(curl -s -w "%{http_code}" -o /dev/null "${INFLUXDB_URL}/health" 2>/dev/null || echo "000")

        if [ "${response}" = "200" ]; then
            check_pass "InfluxDB health endpoint is accessible"
        else
            check_fail "InfluxDB health endpoint returned: ${response}"
        fi
    else
        if docker ps --format '{{.Names}}' | grep -q "greenstack-influxdb"; then
            check_pass "InfluxDB container is running"
        else
            check_fail "InfluxDB container is not running"
        fi
    fi
}

check_grafana() {
    section_header "Grafana"

    if command -v curl &> /dev/null; then
        local response=$(curl -s -w "%{http_code}" -o /dev/null "${GRAFANA_URL}/api/health" 2>/dev/null || echo "000")

        if [ "${response}" = "200" ]; then
            check_pass "Grafana health endpoint is accessible"
        else
            check_warn "Grafana health endpoint returned: ${response}"
        fi
    else
        if docker ps --format '{{.Names}}' | grep -q "greenstack-grafana"; then
            check_pass "Grafana container is running"
        else
            check_fail "Grafana container is not running"
        fi
    fi
}

check_prometheus() {
    section_header "Prometheus"

    if command -v curl &> /dev/null; then
        local response=$(curl -s -w "%{http_code}" -o /dev/null "${PROMETHEUS_URL}/-/healthy" 2>/dev/null || echo "000")

        if [ "${response}" = "200" ]; then
            check_pass "Prometheus is healthy"

            # Check targets
            local targets_up=$(curl -s "${PROMETHEUS_URL}/api/v1/targets" 2>/dev/null | grep -o '"health":"up"' | wc -l)
            local targets_total=$(curl -s "${PROMETHEUS_URL}/api/v1/targets" 2>/dev/null | grep -o '"health":' | wc -l)

            if [ "${targets_total}" -gt 0 ]; then
                echo -e "  ${BLUE}ℹ${NC} Prometheus targets: ${targets_up}/${targets_total} up"
            fi
        else
            check_fail "Prometheus health check returned: ${response}"
        fi
    else
        if docker ps --format '{{.Names}}' | grep -q "greenstack-prometheus"; then
            check_pass "Prometheus container is running"
        else
            check_warn "Prometheus container is not running"
        fi
    fi
}

check_disk_space() {
    section_header "Disk Space"

    local disk_usage=$(df -h . | tail -1 | awk '{print $5}' | sed 's/%//')

    if [ "${disk_usage}" -lt 80 ]; then
        check_pass "Disk usage is ${disk_usage}% (healthy)"
    elif [ "${disk_usage}" -lt 90 ]; then
        check_warn "Disk usage is ${disk_usage}% (consider cleanup)"
    else
        check_fail "Disk usage is ${disk_usage}% (critical!)"
    fi

    # Check Docker volumes
    local volume_count=$(docker volume ls -q | wc -l)
    echo -e "  ${BLUE}ℹ${NC} Docker volumes: ${volume_count}"
}

check_memory() {
    section_header "Memory Usage"

    if command -v free &> /dev/null; then
        local mem_usage=$(free | grep Mem | awk '{printf "%.0f", $3/$2 * 100}')

        if [ "${mem_usage}" -lt 80 ]; then
            check_pass "Memory usage is ${mem_usage}% (healthy)"
        elif [ "${mem_usage}" -lt 90 ]; then
            check_warn "Memory usage is ${mem_usage}% (monitor closely)"
        else
            check_fail "Memory usage is ${mem_usage}% (critical!)"
        fi
    else
        check_warn "free command not available, skipping memory check"
    fi
}

check_logs_for_errors() {
    section_header "Recent Error Logs"

    local error_count=$(docker logs --since 1h greenstack-api 2>&1 | grep -i "error\|exception\|critical" | wc -l)

    if [ "${error_count}" -eq 0 ]; then
        check_pass "No errors in API logs (last hour)"
    elif [ "${error_count}" -lt 10 ]; then
        check_warn "Found ${error_count} errors in API logs (last hour)"
    else
        check_fail "Found ${error_count} errors in API logs (last hour) - investigate!"
    fi
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   GreenStack Health Check              ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"

    check_docker_services
    check_api_health
    check_database
    check_redis
    check_mosquitto
    check_influxdb
    check_grafana
    check_prometheus
    check_disk_space
    check_memory
    check_logs_for_errors

    # Summary
    echo ""
    echo -e "${BLUE}═══ Summary ═══${NC}"
    echo -e "Total checks:   ${TOTAL_CHECKS}"
    echo -e "${GREEN}Passed:${NC}         ${PASSED_CHECKS}"
    echo -e "${YELLOW}Warnings:${NC}       ${WARNING_CHECKS}"
    echo -e "${RED}Failed:${NC}         ${FAILED_CHECKS}"
    echo ""

    # Overall status
    if [ "${FAILED_CHECKS}" -eq 0 ]; then
        if [ "${WARNING_CHECKS}" -eq 0 ]; then
            echo -e "${GREEN}✓ System Status: HEALTHY${NC}"
            exit 0
        else
            echo -e "${YELLOW}! System Status: HEALTHY (with warnings)${NC}"
            exit 0
        fi
    else
        echo -e "${RED}✗ System Status: UNHEALTHY${NC}"
        echo "Please review failed checks above"
        exit 1
    fi
}

main "$@"
