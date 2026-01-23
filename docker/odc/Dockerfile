# Build stage
ARG GDAL_VERSION=ubuntu-small-3.12.0
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS builder
WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive

COPY --from=ghcr.io/astral-sh/uv:latest /uv /usr/local/bin/uv

RUN apt-get update && apt-get install -y \
      build-essential \
      git \
      python3-venv \
      python3-dev \
      libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

ENV VIRTUAL_ENV=/opt/venv
RUN uv venv "$VIRTUAL_ENV"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"


COPY docker/odc/pyproject.toml /app/pyproject.toml

RUN uv lock
RUN uv sync --active --frozen --no-cache

# Runtime stage
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION}
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y \
      postgresql-client \
      gettext-base \
      git \
      libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"

COPY datacube.conf.template /root/.datacube.conf.template

RUN useradd -m -s /bin/bash odc

COPY datacube.conf.template /home/odc/.datacube.conf.template
RUN chown odc:odc /home/odc/.datacube.conf.template

COPY docker/odc/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

USER odc
WORKDIR /home/odc/app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
