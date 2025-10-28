#!/bin/bash
set -e

# Generate datacube.conf from template with environment variables
if [ -f /home/ows/.datacube.conf.template ]; then
    envsubst < /home/ows/.datacube.conf.template > /home/ows/.datacube.conf
    echo "Generated datacube.conf from environment variables"
fi

# Wait for database to be ready
echo "Waiting for database..."
until PGPASSWORD=$ODC_DEFAULT_DB_PASSWORD psql -h "$ODC_DEFAULT_DB_HOSTNAME" -U "$ODC_DEFAULT_DB_USERNAME" -d "$ODC_DEFAULT_DB_DATABASE" -c '\q' 2>/dev/null; do
  echo "Database is unavailable - sleeping"
  sleep 2
done
echo "Database is up!"

# Verify datacube connection
echo "Verifying datacube connection..."
datacube system check

exec "$@"
