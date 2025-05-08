# Build stage
ARG GDAL_VERSION=ubuntu-small-3.10.3
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
    && apt-get clean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Create and activate virtual environment
RUN python3 -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

COPY docker/odc/requirements.txt /app/requirements.txt

# Install Python packages
RUN pip install --break-system-packages \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --no-cache-dir \
    -r requirements.txt

# Install ODC packages from GitHub
RUN pip install --break-system-packages \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --no-cache-dir \
    --no-deps \
    "git+https://github.com/opendatacube/datacube-core.git@develop-1.9" \
    "git+https://github.com/opendatacube/odc-tools.git@develop-1.9#subdirectory=apps/dc_tools" \
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
    && apt-get clean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Copy virtual environment from builder
COPY --from=builder /home/venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

# Copy configuration to root's home
COPY datacube.conf /root/.datacube.conf

# Create user first
RUN useradd -m -s /bin/bash appuser

# Then copy configuration to appuser's home and set permissions
COPY datacube.conf /home/appuser/.datacube.conf
RUN chown appuser:appuser /home/appuser/.datacube.conf

USER appuser
WORKDIR /home/appuser/app

CMD ["tail", "-f", "/dev/null"]
