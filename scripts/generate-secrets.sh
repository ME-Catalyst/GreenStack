#!/bin/bash

###############################################################################
# GreenStack Production Secrets Generator
###############################################################################
# Purpose: Generate strong, cryptographically secure secrets for production
# Created: 2025-11-25
# Usage: ./scripts/generate-secrets.sh > .env.production
###############################################################################

set -e

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo "# ============================================================================="
echo "# GreenStack Production Secrets"
echo "# Generated: $(date '+%Y-%m-%d %H:%M:%S')"
echo "# ============================================================================="
echo "# SECURITY WARNING: Keep this file secure! Never commit to version control!"
echo "# ============================================================================="
echo ""

echo -e "${GREEN}Generating cryptographically secure secrets...${NC}" >&2

# Check if openssl is available
if ! command -v openssl &> /dev/null; then
    echo -e "${YELLOW}WARNING: openssl not found. Install openssl for best security.${NC}" >&2
    exit 1
fi

echo "# ============================================================================="
echo "# CORE SECURITY"
echo "# ============================================================================="
echo ""

echo "# Secret key for JWT tokens and session encryption"
echo "SECRET_KEY=$(openssl rand -hex 32)"
echo ""

echo "# JWT secret key (should be different from SECRET_KEY)"
echo "JWT_SECRET_KEY=$(openssl rand -hex 32)"
echo ""

echo "# ============================================================================="
echo "# DATABASE CREDENTIALS"
echo "# ============================================================================="
echo ""

echo "# PostgreSQL database password"
echo "# Username: iodd_user | Database: iodd_manager"
echo "POSTGRES_PASSWORD=$(openssl rand -base64 32 | tr -d '\n')"
echo ""

echo "# ============================================================================="
echo "# CACHE & MESSAGE QUEUE"
echo "# ============================================================================="
echo ""

echo "# Redis password for cache and message queue"
echo "REDIS_PASSWORD=$(openssl rand -base64 32 | tr -d '\n')"
echo ""

echo "# ============================================================================="
echo "# IOT PLATFORM SERVICES"
echo "# ============================================================================="
echo ""

echo "# MQTT broker authentication password"
echo "# Username: iodd"
echo "MQTT_PASSWORD=$(openssl rand -base64 32 | tr -d '\n')"
echo ""

echo "# InfluxDB authentication token"
echo "# Organization: iodd-manager | Bucket: device-telemetry"
echo "INFLUXDB_TOKEN=$(openssl rand -base64 32 | tr -d '\n')"
echo ""

echo "# InfluxDB admin password"
echo "# Username: admin"
echo "INFLUXDB_ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d '\n')"
echo ""

echo "# Grafana admin password"
echo "# Username: admin | Access: http://localhost:3000"
echo "GRAFANA_ADMIN_PASSWORD=$(openssl rand -base64 32 | tr -d '\n')"
echo ""

echo "# Node-RED credential encryption secret"
echo "# Access: http://localhost:1880"
echo "NODERED_CREDENTIAL_SECRET=$(openssl rand -hex 32)"
echo ""

echo "# ============================================================================="
echo "# PRODUCTION CHECKLIST"
echo "# ============================================================================="
echo "#"
echo "# Before deploying to production, ensure you also:"
echo "# 1. Set ENVIRONMENT=production"
echo "# 2. Set DEBUG=false"
echo "# 3. Update CORS_ORIGINS to your domain (no wildcards!)"
echo "# 4. Set SHOW_ERROR_DETAILS=false"
echo "# 5. Enable TLS/SSL for all services"
echo "# 6. Configure backups (see scripts/backup.sh)"
echo "# 7. Set up monitoring alerts"
echo "# 8. Review all alert email addresses"
echo "# 9. Test disaster recovery procedures"
echo "# 10. Enable authentication (ENABLE_AUTH=true)"
echo "#"
echo "# Store this file securely:"
echo "# - Use secrets manager (AWS Secrets Manager, HashiCorp Vault, etc.)"
echo "# - Or encrypted storage with limited access"
echo "# - Never commit to version control"
echo "# - Rotate secrets every 90 days"
echo "#"
echo "# ============================================================================="
echo ""

echo -e "${GREEN}✅ Secrets generated successfully!${NC}" >&2
echo -e "${YELLOW}⚠️  Save output to .env.production and keep it secure!${NC}" >&2
echo -e "${YELLOW}⚠️  Run: ./scripts/generate-secrets.sh > .env.production${NC}" >&2
