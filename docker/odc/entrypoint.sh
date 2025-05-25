#!/bin/bash
set -e

# Generate config from template using environment variables
envsubst < /home/appuser/.datacube.conf.template > /home/appuser/.datacube.conf

exec "$@"