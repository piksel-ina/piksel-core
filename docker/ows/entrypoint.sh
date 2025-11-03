#!/bin/bash
set -e

# Generate datacube.conf from template with environment variables
if [ -f /home/ows/.datacube.conf.template ]; then
    envsubst < /home/ows/.datacube.conf.template > /home/ows/.datacube.conf
    echo "Generated datacube.conf from environment variables"
    chmod 600 /home/ows/.datacube.conf
else
    echo "Warning: .datacube.conf.template not found"
fi

# Wait for database to be ready
echo "Waiting for database connection..."
MAX_RETRIES=10
RETRY_COUNT=0

until PGPASSWORD=$ODC_DEFAULT_DB_PASSWORD psql \
    -h "$ODC_DEFAULT_DB_HOSTNAME" \
    -p "$ODC_DEFAULT_DB_PORT" \
    -U "$ODC_DEFAULT_DB_USERNAME" \
    -d "$ODC_DEFAULT_DB_DATABASE" \
    -c '\q' 2>/dev/null; do
  
  RETRY_COUNT=$((RETRY_COUNT+1))
  if [ $RETRY_COUNT -ge $MAX_RETRIES ]; then
    echo "Failed to connect to database after $MAX_RETRIES attempts"
    exit 1
  fi
  
  echo "Database is unavailable (attempt $RETRY_COUNT/$MAX_RETRIES) - sleeping"
  sleep 2
done

echo "Database connection successful!"

# Verify datacube connection
echo "Verifying datacube system..."
if datacube system check; then
    echo "Datacube system check passed!"
else
    echo "Warning: Datacube system check failed"
    exit 1
fi

# Print connection info (without password)
echo "Connected to: $ODC_DEFAULT_DB_HOSTNAME:$ODC_DEFAULT_DB_PORT/$ODC_DEFAULT_DB_DATABASE as $ODC_DEFAULT_DB_USERNAME"

exec "$@"
