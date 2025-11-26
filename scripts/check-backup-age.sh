#!/bin/bash
###############################################################################
# GreenStack Backup Age Monitor
###############################################################################
# Purpose: Monitor backup age and alert if backups are too old
# Created: 2025-11-25
# Usage: ./scripts/check-backup-age.sh [max_age_hours]
###############################################################################

set -e

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
MAX_AGE_HOURS="${1:-48}"  # Default: 48 hours
ALERT_EMAIL="${ALERT_EMAIL_OPS:-ops@example.com}"
SLACK_WEBHOOK="${SLACK_WEBHOOK_URL:-}"

# Colors
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

# Find latest backup
LATEST_BACKUP=$(find "${BACKUP_DIR}" -name "greenstack_backup_*.tar.gz" -type f -printf '%T@ %p\n' 2>/dev/null | sort -rn | head -1 | cut -d' ' -f2)

if [ -z "${LATEST_BACKUP}" ]; then
    echo -e "${RED}CRITICAL: No backups found in ${BACKUP_DIR}${NC}"

    # Send alert
    if [ -n "${SLACK_WEBHOOK}" ]; then
        curl -X POST "${SLACK_WEBHOOK}" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"🔴 CRITICAL: GreenStack - No backups found!\"}" \
            2>/dev/null || true
    fi

    exit 2
fi

# Get backup age in hours
BACKUP_TIMESTAMP=$(stat -c %Y "${LATEST_BACKUP}" 2>/dev/null || stat -f %m "${LATEST_BACKUP}")
CURRENT_TIMESTAMP=$(date +%s)
BACKUP_AGE_SECONDS=$((CURRENT_TIMESTAMP - BACKUP_TIMESTAMP))
BACKUP_AGE_HOURS=$((BACKUP_AGE_SECONDS / 3600))

# Get backup size
BACKUP_SIZE=$(du -h "${LATEST_BACKUP}" | cut -f1)

# Check age
if [ ${BACKUP_AGE_HOURS} -gt ${MAX_AGE_HOURS} ]; then
    echo -e "${RED}CRITICAL: Latest backup is ${BACKUP_AGE_HOURS} hours old (threshold: ${MAX_AGE_HOURS} hours)${NC}"
    echo -e "Backup: ${LATEST_BACKUP}"
    echo -e "Size: ${BACKUP_SIZE}"
    echo -e "Age: ${BACKUP_AGE_HOURS} hours"

    # Send alert
    if [ -n "${SLACK_WEBHOOK}" ]; then
        curl -X POST "${SLACK_WEBHOOK}" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"🔴 CRITICAL: GreenStack backup is ${BACKUP_AGE_HOURS}h old (max: ${MAX_AGE_HOURS}h)\\nBackup: ${LATEST_BACKUP}\\nSize: ${BACKUP_SIZE}\"}" \
            2>/dev/null || true
    fi

    exit 1
elif [ ${BACKUP_AGE_HOURS} -gt $((MAX_AGE_HOURS / 2)) ]; then
    echo -e "${YELLOW}WARNING: Latest backup is ${BACKUP_AGE_HOURS} hours old${NC}"
    echo -e "Backup: ${LATEST_BACKUP}"
    echo -e "Size: ${BACKUP_SIZE}"
    exit 0
else
    echo -e "${GREEN}OK: Latest backup is ${BACKUP_AGE_HOURS} hours old${NC}"
    echo -e "Backup: ${LATEST_BACKUP}"
    echo -e "Size: ${BACKUP_SIZE}"
    exit 0
fi
