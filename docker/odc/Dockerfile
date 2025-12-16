# Build stage
ARG GDAL_VERSION=ubuntu-small-3.12.0
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS builder
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

# Install UV from Astral
COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

# Install essential build dependencies
RUN apt-get update && apt-get install -y \
      git \
      libpq-dev \
      build-essential \
      python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Create virtual environment with UV
ENV VIRTUAL_ENV=/home/venv
RUN uv venv $VIRTUAL_ENV
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Copy requirements
COPY docker/odc/requirements.txt /app/requirements.txt

# Install Python packages with UV
RUN uv pip install --no-cache -r requirements.txt

# Runtime stage
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION}
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
      postgresql-client \
      gettext-base \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy virtual environment from builder
COPY --from=builder /home/venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

# Copy configuration to root's home
COPY datacube.conf.template /root/.datacube.conf.template

# Create user 'odc'
RUN useradd -m -s /bin/bash odc

# Copy template to odc's home and set permissions
COPY datacube.conf.template /home/odc/.datacube.conf.template
RUN chown odc:odc /home/odc/.datacube.conf.template

# Copy entrypoint
COPY docker/odc/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odc
WORKDIR /home/odc/app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
