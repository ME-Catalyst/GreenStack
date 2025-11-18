#!/bin/bash
###########################################
# GreenStack Automated Backup Script
# Version: 1.0
# Purpose: Backup database, files, and configuration
###########################################

set -euo pipefail

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Configuration
BACKUP_DIR="${BACKUP_DIR:-./backups}"
RETENTION_DAYS="${BACKUP_RETENTION_DAYS:-7}"
TIMESTAMP=$(date +%Y%m%d_%H%M%S)
BACKUP_NAME="greenstack_backup_${TIMESTAMP}"
BACKUP_PATH="${BACKUP_DIR}/${BACKUP_NAME}"

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# PostgreSQL Configuration
POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-greenstack-postgres}"
POSTGRES_USER="${POSTGRES_USER:-iodd_user}"
POSTGRES_DB="${POSTGRES_DB:-greenstack}"

# Directories to backup
IODD_STORAGE_DIR="${IODD_STORAGE_DIR:-./iodd_storage}"
GENERATED_OUTPUT_DIR="${GENERATED_OUTPUT_DIR:-./generated}"
CONFIG_DIR="./config"

# S3 Configuration (optional)
S3_BUCKET="${BACKUP_S3_BUCKET:-}"
S3_REGION="${AWS_DEFAULT_REGION:-us-east-1}"

# ============================================================================
# Functions
# ============================================================================

log() {
    echo -e "${BLUE}[$(date '+%Y-%m-%d %H:%M:%S')]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[$(date '+%Y-%m-%d %H:%M:%S')] ✓${NC} $1"
}

log_error() {
    echo -e "${RED}[$(date '+%Y-%m-%d %H:%M:%S')] ✗${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[$(date '+%Y-%m-%d %H:%M:%S')] !${NC} $1"
}

check_dependencies() {
    local missing_deps=()

    if ! command -v docker &> /dev/null; then
        missing_deps+=("docker")
    fi

    if ! command -v tar &> /dev/null; then
        missing_deps+=("tar")
    fi

    if [ ${#missing_deps[@]} -gt 0 ]; then
        log_error "Missing required dependencies: ${missing_deps[*]}"
        exit 1
    fi
}

create_backup_directory() {
    log "Creating backup directory: ${BACKUP_PATH}"
    mkdir -p "${BACKUP_PATH}"
}

backup_database() {
    log "Backing up PostgreSQL database..."

    # Check if PostgreSQL container is running
    if ! docker ps --format '{{.Names}}' | grep -q "^${POSTGRES_CONTAINER}$"; then
        log_warning "PostgreSQL container '${POSTGRES_CONTAINER}' not running, skipping database backup"
        return 0
    fi

    # Create database dump
    docker exec "${POSTGRES_CONTAINER}" pg_dump \
        -U "${POSTGRES_USER}" \
        -d "${POSTGRES_DB}" \
        --format=custom \
        --compress=9 \
        > "${BACKUP_PATH}/postgres.dump" 2>/dev/null

    if [ $? -eq 0 ]; then
        log_success "Database backup completed: postgres.dump"

        # Create human-readable SQL backup as well
        docker exec "${POSTGRES_CONTAINER}" pg_dump \
            -U "${POSTGRES_USER}" \
            -d "${POSTGRES_DB}" \
            --format=plain \
            > "${BACKUP_PATH}/postgres.sql" 2>/dev/null

        log_success "SQL backup completed: postgres.sql"
    else
        log_error "Database backup failed"
        return 1
    fi
}

backup_files() {
    log "Backing up uploaded files and data..."

    # Backup IODD storage
    if [ -d "${IODD_STORAGE_DIR}" ]; then
        tar -czf "${BACKUP_PATH}/iodd_storage.tar.gz" \
            -C "$(dirname ${IODD_STORAGE_DIR})" \
            "$(basename ${IODD_STORAGE_DIR})" 2>/dev/null
        log_success "IODD storage backup completed: iodd_storage.tar.gz"
    else
        log_warning "IODD storage directory not found: ${IODD_STORAGE_DIR}"
    fi

    # Backup generated outputs
    if [ -d "${GENERATED_OUTPUT_DIR}" ]; then
        tar -czf "${BACKUP_PATH}/generated.tar.gz" \
            -C "$(dirname ${GENERATED_OUTPUT_DIR})" \
            "$(basename ${GENERATED_OUTPUT_DIR})" 2>/dev/null
        log_success "Generated files backup completed: generated.tar.gz"
    else
        log_warning "Generated output directory not found: ${GENERATED_OUTPUT_DIR}"
    fi
}

backup_configuration() {
    log "Backing up configuration files..."

    # Copy .env file (excluding secrets)
    if [ -f .env ]; then
        # Create sanitized version without actual secret values
        sed 's/=.*/=***REDACTED***/g' .env > "${BACKUP_PATH}/env.template"
        log_success "Environment template saved: env.template"
    fi

    # Backup configuration directory
    if [ -d "${CONFIG_DIR}" ]; then
        tar -czf "${BACKUP_PATH}/config.tar.gz" \
            --exclude="*.key" \
            --exclude="*.pem" \
            --exclude="passwd" \
            -C "$(dirname ${CONFIG_DIR})" \
            "$(basename ${CONFIG_DIR})" 2>/dev/null
        log_success "Configuration backup completed: config.tar.gz"
    fi

    # Backup docker-compose files
    tar -czf "${BACKUP_PATH}/docker-compose.tar.gz" \
        docker-compose*.yml 2>/dev/null
    log_success "Docker Compose files backed up: docker-compose.tar.gz"
}

backup_docker_volumes() {
    log "Backing up Docker volumes..."

    # List of volumes to backup
    local volumes=(
        "postgres-data"
        "redis-data"
        "mosquitto-data"
        "influxdb-data"
        "grafana-data"
        "nodered-data"
    )

    for volume in "${volumes[@]}"; do
        local full_volume_name="greenstack_${volume}"

        # Check if volume exists
        if docker volume ls --format '{{.Name}}' | grep -q "^${full_volume_name}$"; then
            log "Backing up volume: ${volume}"

            # Create a temporary container to access the volume
            docker run --rm \
                -v "${full_volume_name}:/data:ro" \
                -v "$(pwd)/${BACKUP_PATH}:/backup" \
                alpine \
                tar -czf "/backup/${volume}.tar.gz" -C /data . 2>/dev/null

            if [ $? -eq 0 ]; then
                log_success "Volume backup completed: ${volume}.tar.gz"
            else
                log_warning "Failed to backup volume: ${volume}"
            fi
        else
            log_warning "Volume not found: ${full_volume_name}"
        fi
    done
}

create_manifest() {
    log "Creating backup manifest..."

    # Create manifest file
    cat > "${BACKUP_PATH}/MANIFEST.txt" <<EOF
GreenStack Backup Manifest
==========================
Backup ID: ${BACKUP_NAME}
Created: $(date '+%Y-%m-%d %H:%M:%S %Z')
Hostname: $(hostname)
User: $(whoami)

Environment Information:
- APP_VERSION: ${APP_VERSION:-unknown}
- ENVIRONMENT: ${ENVIRONMENT:-unknown}
- DATABASE_URL: $(echo ${DATABASE_URL:-unknown} | sed 's/:.*@/:***@/')

Backup Contents:
EOF

    # List all files in backup with sizes
    ls -lh "${BACKUP_PATH}" | tail -n +2 >> "${BACKUP_PATH}/MANIFEST.txt"

    # Create checksums
    log "Generating checksums..."
    (cd "${BACKUP_PATH}" && sha256sum *.dump *.sql *.tar.gz 2>/dev/null > checksums.sha256 || true)

    log_success "Manifest created: MANIFEST.txt"
}

compress_backup() {
    log "Compressing backup archive..."

    # Create final compressed archive
    tar -czf "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
        -C "${BACKUP_DIR}" \
        "${BACKUP_NAME}" 2>/dev/null

    if [ $? -eq 0 ]; then
        # Remove temporary directory
        rm -rf "${BACKUP_PATH}"
        log_success "Backup archive created: ${BACKUP_NAME}.tar.gz"

        # Display backup size
        local backup_size=$(du -h "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" | cut -f1)
        log "Backup size: ${backup_size}"
    else
        log_error "Failed to compress backup"
        return 1
    fi
}

upload_to_s3() {
    if [ -z "${S3_BUCKET}" ]; then
        log_warning "S3 bucket not configured, skipping cloud upload"
        return 0
    fi

    log "Uploading backup to S3: s3://${S3_BUCKET}/"

    if ! command -v aws &> /dev/null; then
        log_error "AWS CLI not installed, cannot upload to S3"
        return 1
    fi

    aws s3 cp "${BACKUP_DIR}/${BACKUP_NAME}.tar.gz" \
        "s3://${S3_BUCKET}/greenstack/${BACKUP_NAME}.tar.gz" \
        --region "${S3_REGION}" \
        --storage-class STANDARD_IA

    if [ $? -eq 0 ]; then
        log_success "Backup uploaded to S3"
    else
        log_error "Failed to upload backup to S3"
        return 1
    fi
}

cleanup_old_backups() {
    log "Cleaning up old backups (retention: ${RETENTION_DAYS} days)..."

    # Find and delete backups older than retention period
    find "${BACKUP_DIR}" -name "greenstack_backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS} -delete

    local deleted_count=$(find "${BACKUP_DIR}" -name "greenstack_backup_*.tar.gz" -type f -mtime +${RETENTION_DAYS} | wc -l)

    if [ ${deleted_count} -gt 0 ]; then
        log_success "Deleted ${deleted_count} old backup(s)"
    else
        log "No old backups to delete"
    fi

    # List remaining backups
    local backup_count=$(find "${BACKUP_DIR}" -name "greenstack_backup_*.tar.gz" -type f | wc -l)
    log "Total backups: ${backup_count}"
}

send_notification() {
    local status=$1
    local message=$2

    # You can implement notification logic here
    # Examples: Slack webhook, email, PagerDuty, etc.

    if [ -n "${SLACK_WEBHOOK_URL:-}" ]; then
        curl -X POST "${SLACK_WEBHOOK_URL}" \
            -H 'Content-Type: application/json' \
            -d "{\"text\":\"GreenStack Backup ${status}: ${message}\"}" \
            2>/dev/null || true
    fi
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   GreenStack Automated Backup          ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""

    log "Starting backup process..."
    log "Backup ID: ${BACKUP_NAME}"

    # Pre-flight checks
    check_dependencies

    # Create backup directory
    create_backup_directory

    # Perform backups
    backup_database || log_warning "Database backup had issues"
    backup_files
    backup_configuration
    backup_docker_volumes

    # Finalize backup
    create_manifest
    compress_backup

    # Upload to cloud (if configured)
    upload_to_s3 || log_warning "Cloud upload had issues"

    # Cleanup old backups
    cleanup_old_backups

    # Summary
    echo ""
    log_success "Backup completed successfully!"
    log "Backup location: ${BACKUP_DIR}/${BACKUP_NAME}.tar.gz"

    # Send notification
    send_notification "SUCCESS" "Backup ${BACKUP_NAME} completed"

    echo ""
}

# Error handling
trap 'log_error "Backup failed with error on line $LINENO"; send_notification "FAILED" "Backup failed"; exit 1' ERR

# Run main function
main "$@"
