# Build stage
ARG GDAL_VERSION=ubuntu-small-3.11.0
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS builder
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Install build dependencies
RUN apt-get update && apt-get install -y \
      python3-full \
      python3-dev \
      python3-venv \
      git \
      curl \
      ca-certificates \
      build-essential \
      libpq-dev \
      postgresql-client \
      postgis \
      gettext-base \
    && apt-get clean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Create and activate virtual environment
RUN python3 -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

COPY docker/odc/requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install --no-cache-dir -r requirements.txt

# Install ODC packages from GitHub
RUN pip install --no-cache-dir --no-deps \
    "git+https://github.com/opendatacube/datacube-core.git@1.9.6" \
    "odc-apps-dc-tools==1.9.3" \
    "git+https://github.com/opendatacube/eo-datasets.git@integrate-1.9"

# Runtime stage
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION}
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install runtime dependencies only
RUN apt-get update && apt-get install -y \
      python3-minimal \
      postgresql-client \
      gettext-base \
    && apt-get clean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Copy virtual environment from builder
COPY --from=builder /home/venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

# Copy configuration to root's home
COPY datacube.conf.template /root/.datacube.conf.template

# Create user first
RUN useradd -m -s /bin/bash appuser

# Copy template to appuser's home and set permissions
COPY datacube.conf.template /home/appuser/.datacube.conf.template
RUN chown appuser:appuser /home/appuser/.datacube.conf.template

# Copy entrypoint
COPY docker/odc/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER appuser
WORKDIR /home/appuser/app

# Use entrypoint
ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
