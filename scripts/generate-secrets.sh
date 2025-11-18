#!/bin/bash
###########################################
# GreenStack Secret Generation Script
# Version: 1.0
# Purpose: Generate cryptographically secure passwords for all services
###########################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
echo -e "${GREEN}║  GreenStack Secret Generation Script  ║${NC}"
echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
echo ""

# Check if openssl is available
if ! command -v openssl &> /dev/null; then
    echo -e "${RED}ERROR: openssl is required but not installed${NC}"
    exit 1
fi

echo -e "${YELLOW}Generating secure passwords and tokens...${NC}"
echo ""

# Generate secrets
echo "# GreenStack Production Secrets"
echo "# Generated: $(date)"
echo "# IMPORTANT: Keep this file secure! Add to .gitignore"
echo ""
echo "# === Application Secrets ==="
echo "SECRET_KEY=$(openssl rand -hex 32)"
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)"
echo ""
echo "# === Admin Credentials ==="
echo "ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d '=/+')"
echo ""
echo "# === Database ==="
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d '=/+')"
echo ""
echo "# === Redis Cache ==="
echo "REDIS_PASSWORD=$(openssl rand -base64 32 | tr -d '=/+')"
echo ""
echo "# === MQTT Broker ==="
echo "MQTT_PASSWORD=$(openssl rand -base64 32 | tr -d '=/+')"
echo ""
echo "# === InfluxDB ==="
echo "INFLUXDB_TOKEN=$(openssl rand -base64 32 | tr -d '=/+')"
echo "INFLUXDB_ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d '=/+')"
echo ""
echo "# === Grafana ==="
echo "GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d '=/+')"
echo ""
echo "# === Node-RED ==="
echo "NODERED_CREDENTIAL_SECRET=$(openssl rand -hex 32)"
echo ""

echo ""
echo -e "${GREEN}✓ Secrets generated successfully!${NC}"
echo ""
echo -e "${YELLOW}NEXT STEPS:${NC}"
echo "1. Save the output above to .env.production"
echo "2. Set file permissions: chmod 600 .env.production"
echo "3. NEVER commit .env.production to git"
echo "4. Store backup copy in secure password manager"
echo ""
echo -e "${YELLOW}Usage:${NC}"
echo "  ./scripts/generate-secrets.sh > .env.production"
echo "  chmod 600 .env.production"
echo ""
