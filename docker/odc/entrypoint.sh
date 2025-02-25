#!/bin/bash
set -e

echo "Starting ODC environment..."

# Optional: Run database initialization if needed (or run it externally)
if [ "$INIT_DB" = "true" ]; then
    echo "Initializing database schema..."
    datacube -E new system init
fi

# Check if indexing should be run automatically
if [ "$RUN_INDEXING" = "true" ]; then
    echo "Starting indexing process..."
    exec stac-to-dc "$@"
else
    echo "No indexing command provided. Container is running in idle mode."
    exec tail -f /dev/null  # Keep container running, but idle.
fi
