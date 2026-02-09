# Build stage
ARG GDAL_VERSION=ubuntu-small-3.10.3
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS builder
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Install UV from Astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install essential build dependencies
RUN apt-get update && apt-get install -y \
      git \
      gcc \
      g++ \
      libpq-dev \
      libgeos-dev \
      libhdf5-dev \
      libnetcdf-dev \
      python3-dev \
      build-essential \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment with UV
ENV VIRTUAL_ENV=/home/venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements.txt
COPY docker/ows/requirements.txt /app/requirements.txt

# Install Python packages with UV
RUN uv pip install --no-cache -r requirements.txt

# Runtime stage
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS runtime
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
      postgresql-client \
      gettext-base \
      curl \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /home/venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

# GDAL optimizations for OWS
ENV GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR" \
    CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif,.tiff" \
    GDAL_HTTP_MAX_RETRY="10" \
    GDAL_HTTP_RETRY_DELAY="1"

# Copy datacube configuration template to root's home
COPY datacube.conf.template /root/.datacube.conf.template

# Create user 'ows'
RUN useradd -m -s /bin/bash ows

# Copy template to ows's home and set permissions
COPY datacube.conf.template /home/ows/.datacube.conf.template
RUN chown ows:ows /home/ows/.datacube.conf.template

# Create config directory with proper permissions
RUN mkdir -p /env/config && chown -R ows:ows /env/config

ENV PYTHONPATH=/env/config
ENV DATACUBE_OWS_CFG=ows_config.ows_cfg.ows_cfg

# Copy entrypoint
COPY docker/ows/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER ows
WORKDIR /home/ows

EXPOSE 8000

ENTRYPOINT ["/entrypoint.sh"]
CMD ["gunicorn", "-b", "0.0.0.0:8000", "--workers=3", "-k", "gevent", "--timeout", "121", "--log-level", "info", "--worker-tmp-dir", "/dev/shm", "datacube_ows.wsgi"]
