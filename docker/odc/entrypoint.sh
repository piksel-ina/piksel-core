#!/bin/bash
set -e

# Better ogging functions
log() {
    echo "[$(date +'%Y-%m-%dT%H:%M:%S%z')]: $*" >&2
}

error_exit() {
    log "ERROR: $1"
    exit 1
}

# Function to wait for database to be ready
wait_for_db() {
    log "Waiting for database connection..."
    local max_attempts=30
    local attempt=0
    
    while [ $attempt -lt $max_attempts ]; do
        if PGPASSWORD=$ODC_DEFAULT_DB_PASSWORD psql -h $ODC_DEFAULT_DB_HOSTNAME -U $ODC_DEFAULT_DB_USERNAME -d $ODC_DEFAULT_DB_DATABASE -c '\q' 2>/dev/null; then
            log "PostgreSQL is up - continuing"
            return 0
        fi
        
        attempt=$((attempt+1))
        log "PostgreSQL is unavailable - sleeping (attempt $attempt/$max_attempts)"
        sleep 2
    done
    
    error_exit "Database connection failed after $max_attempts attempts"
}

# Handle healthcheck requests
if [ "$1" = "healthcheck" ]; then
    if datacube system check; then
        exit 0
    else
        exit 1
    fi
fi

log "Starting ODC environment..."

# Wait for database to be ready
wait_for_db

# Optional: Run database initialization if needed
if [ "$INIT_DB" = "true" ]; then
    log "Initializing database schema..."
    datacube -E default system init || error_exit "Database initialization failed"
    log "Database schema initialized successfully"
fi

# Check if indexing should be run automatically
if [ "$RUN_INDEXING" = "true" ]; then
    log "Starting indexing process..."
    exec stac-to-dc "$@" || error_exit "Indexing process failed"
else
    log "No indexing command provided. Container is running in idle mode."
    # Keep container running, but idle
    exec tail -f /dev/null
fi