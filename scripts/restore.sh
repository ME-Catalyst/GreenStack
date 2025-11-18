#!/bin/bash
###########################################
# GreenStack Restore Script
# Version: 1.0
# Purpose: Restore database, files, and configuration from backup
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
RESTORE_DIR="${RESTORE_DIR:-./restore_temp}"

# Load environment variables
if [ -f .env ]; then
    source .env
fi

# PostgreSQL Configuration
POSTGRES_CONTAINER="${POSTGRES_CONTAINER:-greenstack-postgres}"
POSTGRES_USER="${POSTGRES_USER:-iodd_user}"
POSTGRES_DB="${POSTGRES_DB:-greenstack}"

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

show_usage() {
    cat <<EOF
Usage: $0 <backup_file.tar.gz> [options]

Restore GreenStack from a backup archive.

Arguments:
    backup_file.tar.gz    Path to backup archive to restore

Options:
    --database-only       Restore only the database
    --files-only          Restore only files (no database)
    --config-only         Restore only configuration
    --skip-volumes        Skip Docker volume restoration
    --no-confirmation     Skip confirmation prompts (dangerous!)
    --help                Show this help message

Examples:
    # Full restore
    $0 backups/greenstack_backup_20251118_120000.tar.gz

    # Restore only database
    $0 backups/greenstack_backup_20251118_120000.tar.gz --database-only

    # Restore without confirmation (automated)
    $0 backups/greenstack_backup_20251118_120000.tar.gz --no-confirmation

EOF
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

confirm_restore() {
    if [ "${NO_CONFIRMATION:-false}" = "true" ]; then
        return 0
    fi

    echo ""
    log_warning "⚠️  WARNING: This will overwrite existing data!"
    echo ""
    echo "You are about to restore from:"
    echo "  ${BACKUP_FILE}"
    echo ""
    echo "This will:"
    echo "  - Drop and recreate the database (if restoring database)"
    echo "  - Overwrite existing files (if restoring files)"
    echo "  - Replace configuration (if restoring config)"
    echo ""
    read -p "Are you sure you want to continue? (yes/no): " -r
    echo ""

    if [[ ! $REPLY =~ ^[Yy][Ee][Ss]$ ]]; then
        log "Restore cancelled by user"
        exit 0
    fi
}

extract_backup() {
    log "Extracting backup archive..."

    # Create restore directory
    mkdir -p "${RESTORE_DIR}"

    # Extract backup
    tar -xzf "${BACKUP_FILE}" -C "${RESTORE_DIR}"

    # Find extracted directory (should be greenstack_backup_TIMESTAMP)
    EXTRACTED_DIR=$(find "${RESTORE_DIR}" -maxdepth 1 -type d -name "greenstack_backup_*" | head -1)

    if [ -z "${EXTRACTED_DIR}" ]; then
        log_error "Failed to find extracted backup directory"
        return 1
    fi

    log_success "Backup extracted to: ${EXTRACTED_DIR}"

    # Verify manifest
    if [ -f "${EXTRACTED_DIR}/MANIFEST.txt" ]; then
        log "Backup manifest:"
        cat "${EXTRACTED_DIR}/MANIFEST.txt" | head -15
    fi

    # Verify checksums
    if [ -f "${EXTRACTED_DIR}/checksums.sha256" ]; then
        log "Verifying checksums..."
        (cd "${EXTRACTED_DIR}" && sha256sum -c checksums.sha256 2>/dev/null)
        if [ $? -eq 0 ]; then
            log_success "Checksum verification passed"
        else
            log_error "Checksum verification failed - backup may be corrupted"
            return 1
        fi
    fi
}

restore_database() {
    if [ "${DATABASE_ONLY:-true}" = "false" ]; then
        log "Skipping database restore (--files-only specified)"
        return 0
    fi

    log "Restoring PostgreSQL database..."

    # Check if database dump exists
    if [ ! -f "${EXTRACTED_DIR}/postgres.dump" ]; then
        log_warning "Database dump not found in backup, skipping"
        return 0
    fi

    # Check if PostgreSQL container is running
    if ! docker ps --format '{{.Names}}' | grep -q "^${POSTGRES_CONTAINER}$"; then
        log_error "PostgreSQL container '${POSTGRES_CONTAINER}' not running"
        log "Start PostgreSQL with: docker-compose -f docker-compose.iot.yml up -d postgres"
        return 1
    fi

    # Drop existing database (with confirmation)
    log_warning "Dropping existing database: ${POSTGRES_DB}"
    docker exec "${POSTGRES_CONTAINER}" psql -U "${POSTGRES_USER}" -d postgres \
        -c "DROP DATABASE IF EXISTS ${POSTGRES_DB};" 2>/dev/null

    # Create fresh database
    log "Creating fresh database: ${POSTGRES_DB}"
    docker exec "${POSTGRES_CONTAINER}" psql -U "${POSTGRES_USER}" -d postgres \
        -c "CREATE DATABASE ${POSTGRES_DB};" 2>/dev/null

    # Restore from dump
    log "Restoring database from dump..."
    docker exec -i "${POSTGRES_CONTAINER}" pg_restore \
        -U "${POSTGRES_USER}" \
        -d "${POSTGRES_DB}" \
        --no-owner \
        --no-acl \
        --verbose \
        < "${EXTRACTED_DIR}/postgres.dump" 2>/dev/null

    if [ $? -eq 0 ]; then
        log_success "Database restored successfully"

        # Verify restoration
        local table_count=$(docker exec "${POSTGRES_CONTAINER}" psql \
            -U "${POSTGRES_USER}" \
            -d "${POSTGRES_DB}" \
            -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')

        log "Restored ${table_count} tables"
    else
        log_error "Database restore failed"
        return 1
    fi
}

restore_files() {
    if [ "${FILES_ONLY:-true}" = "false" ]; then
        log "Skipping files restore (--database-only specified)"
        return 0
    fi

    log "Restoring files and data..."

    # Restore IODD storage
    if [ -f "${EXTRACTED_DIR}/iodd_storage.tar.gz" ]; then
        log "Restoring IODD storage..."
        mkdir -p "${IODD_STORAGE_DIR:-./iodd_storage}"
        tar -xzf "${EXTRACTED_DIR}/iodd_storage.tar.gz" -C .
        log_success "IODD storage restored"
    else
        log_warning "IODD storage backup not found"
    fi

    # Restore generated outputs
    if [ -f "${EXTRACTED_DIR}/generated.tar.gz" ]; then
        log "Restoring generated outputs..."
        mkdir -p "${GENERATED_OUTPUT_DIR:-./generated}"
        tar -xzf "${EXTRACTED_DIR}/generated.tar.gz" -C .
        log_success "Generated outputs restored"
    else
        log_warning "Generated outputs backup not found"
    fi
}

restore_configuration() {
    if [ "${CONFIG_ONLY:-false}" = "false" ] && [ "${FILES_ONLY:-false}" = "true" ]; then
        log "Skipping configuration restore"
        return 0
    fi

    log "Restoring configuration..."

    # Restore configuration directory
    if [ -f "${EXTRACTED_DIR}/config.tar.gz" ]; then
        log "Restoring config directory..."

        # Backup current config first
        if [ -d "./config" ]; then
            mv ./config "./config.backup.$(date +%Y%m%d_%H%M%S)"
            log "Current config backed up to config.backup.*"
        fi

        tar -xzf "${EXTRACTED_DIR}/config.tar.gz" -C .
        log_success "Configuration directory restored"
    else
        log_warning "Configuration backup not found"
    fi

    # Restore docker-compose files
    if [ -f "${EXTRACTED_DIR}/docker-compose.tar.gz" ]; then
        log "Restoring Docker Compose files..."

        # Backup current docker-compose files
        for f in docker-compose*.yml; do
            if [ -f "$f" ]; then
                cp "$f" "${f}.backup.$(date +%Y%m%d_%H%M%S)"
            fi
        done

        tar -xzf "${EXTRACTED_DIR}/docker-compose.tar.gz" -C .
        log_success "Docker Compose files restored"
    fi

    # Environment file note
    if [ -f "${EXTRACTED_DIR}/env.template" ]; then
        log_warning "Environment template found: env.template"
        log "Note: Secrets were redacted from backup. You must:"
        log "  1. Copy env.template to .env"
        log "  2. Fill in actual secret values"
        log "  3. Or restore .env from secure password manager"
    fi
}

restore_docker_volumes() {
    if [ "${SKIP_VOLUMES:-false}" = "true" ]; then
        log "Skipping Docker volumes restore (--skip-volumes specified)"
        return 0
    fi

    log "Restoring Docker volumes..."

    # List of volumes to restore
    local volumes=(
        "postgres-data"
        "redis-data"
        "mosquitto-data"
        "influxdb-data"
        "grafana-data"
        "nodered-data"
    )

    for volume in "${volumes[@]}"; do
        if [ -f "${EXTRACTED_DIR}/${volume}.tar.gz" ]; then
            log "Restoring volume: ${volume}"

            local full_volume_name="greenstack_${volume}"

            # Remove existing volume (with warning)
            if docker volume ls --format '{{.Name}}' | grep -q "^${full_volume_name}$"; then
                log_warning "Removing existing volume: ${full_volume_name}"
                docker volume rm "${full_volume_name}" 2>/dev/null || true
            fi

            # Create new volume
            docker volume create "${full_volume_name}"

            # Restore data to volume
            docker run --rm \
                -v "${full_volume_name}:/data" \
                -v "$(pwd)/${EXTRACTED_DIR}:/backup:ro" \
                alpine \
                sh -c "cd /data && tar -xzf /backup/${volume}.tar.gz" 2>/dev/null

            if [ $? -eq 0 ]; then
                log_success "Volume restored: ${volume}"
            else
                log_warning "Failed to restore volume: ${volume}"
            fi
        else
            log_warning "Volume backup not found: ${volume}"
        fi
    done
}

cleanup_restore_temp() {
    log "Cleaning up temporary files..."

    if [ -d "${RESTORE_DIR}" ]; then
        rm -rf "${RESTORE_DIR}"
        log_success "Temporary files cleaned up"
    fi
}

restart_services() {
    log "Restarting services..."

    # Stop services
    docker-compose down
    docker-compose -f docker-compose.iot.yml down

    # Wait a moment
    sleep 5

    # Start services
    docker-compose up -d
    docker-compose -f docker-compose.iot.yml up -d

    log_success "Services restarted"
}

verify_restore() {
    log "Verifying restore..."

    # Wait for services to be ready
    sleep 10

    # Check API health
    if command -v curl &> /dev/null; then
        local api_health=$(curl -s http://localhost:8000/api/health || echo "failed")

        if echo "${api_health}" | grep -q "healthy"; then
            log_success "API health check passed"
        else
            log_warning "API health check failed - services may still be starting"
        fi
    fi

    # Check database tables
    local table_count=$(docker exec "${POSTGRES_CONTAINER}" psql \
        -U "${POSTGRES_USER}" \
        -d "${POSTGRES_DB}" \
        -t -c "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='public';" 2>/dev/null | tr -d ' ')

    log "Database tables: ${table_count}"

    # Check device count (if devices table exists)
    local device_count=$(docker exec "${POSTGRES_CONTAINER}" psql \
        -U "${POSTGRES_USER}" \
        -d "${POSTGRES_DB}" \
        -t -c "SELECT COUNT(*) FROM devices;" 2>/dev/null | tr -d ' ' || echo "N/A")

    log "Devices in database: ${device_count}"
}

# ============================================================================
# Main Execution
# ============================================================================

main() {
    echo ""
    echo -e "${GREEN}╔════════════════════════════════════════╗${NC}"
    echo -e "${GREEN}║   GreenStack Restore                   ║${NC}"
    echo -e "${GREEN}╚════════════════════════════════════════╝${NC}"
    echo ""

    # Parse command line arguments
    BACKUP_FILE=""
    DATABASE_ONLY="false"
    FILES_ONLY="false"
    CONFIG_ONLY="false"
    SKIP_VOLUMES="false"
    NO_CONFIRMATION="false"

    while [[ $# -gt 0 ]]; do
        case $1 in
            --database-only)
                DATABASE_ONLY="true"
                FILES_ONLY="false"
                shift
                ;;
            --files-only)
                FILES_ONLY="true"
                DATABASE_ONLY="false"
                shift
                ;;
            --config-only)
                CONFIG_ONLY="true"
                DATABASE_ONLY="false"
                FILES_ONLY="false"
                shift
                ;;
            --skip-volumes)
                SKIP_VOLUMES="true"
                shift
                ;;
            --no-confirmation)
                NO_CONFIRMATION="true"
                shift
                ;;
            --help|-h)
                show_usage
                exit 0
                ;;
            *)
                if [ -z "${BACKUP_FILE}" ]; then
                    BACKUP_FILE="$1"
                else
                    log_error "Unknown option: $1"
                    show_usage
                    exit 1
                fi
                shift
                ;;
        esac
    done

    # Validate backup file
    if [ -z "${BACKUP_FILE}" ]; then
        log_error "No backup file specified"
        show_usage
        exit 1
    fi

    if [ ! -f "${BACKUP_FILE}" ]; then
        log_error "Backup file not found: ${BACKUP_FILE}"
        exit 1
    fi

    log "Starting restore process..."
    log "Backup file: ${BACKUP_FILE}"

    # Pre-flight checks
    check_dependencies

    # Confirm restore
    confirm_restore

    # Extract backup
    extract_backup

    # Perform restore
    if [ "${CONFIG_ONLY}" = "true" ]; then
        restore_configuration
    elif [ "${DATABASE_ONLY}" = "true" ]; then
        restore_database
    elif [ "${FILES_ONLY}" = "true" ]; then
        restore_files
        restore_configuration
    else
        # Full restore
        restore_database
        restore_files
        restore_configuration
        restore_docker_volumes
    fi

    # Cleanup
    cleanup_restore_temp

    # Restart services (for full restore)
    if [ "${DATABASE_ONLY}" = "false" ] && [ "${FILES_ONLY}" = "false" ] && [ "${CONFIG_ONLY}" = "false" ]; then
        restart_services
        verify_restore
    fi

    # Summary
    echo ""
    log_success "Restore completed successfully!"
    log "Next steps:"
    log "  1. Verify data integrity"
    log "  2. Check application logs"
    log "  3. Run smoke tests"
    log "  4. Restore .env file with actual secrets (if needed)"
    echo ""
}

# Error handling
trap 'log_error "Restore failed with error on line $LINENO"; exit 1' ERR

# Run main function
main "$@"
