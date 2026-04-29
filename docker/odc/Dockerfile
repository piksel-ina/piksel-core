ARG GDAL_VERSION=ubuntu-small-3.12.0

# --- Builder stage ---
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS builder

ENV DEBIAN_FRONTEND=noninteractive \
    UV_COMPILE_BYTECODE=1 \
    UV_LINK_MODE=copy \
    UV_PYTHON_DOWNLOADS=0

COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends \
      build-essential \
      libpq-dev \
      libgeos-dev \
      python3-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

RUN --mount=type=cache,target=/root/.cache/uv \
    --mount=type=bind,source=docker/odc/uv.lock,target=uv.lock \
    --mount=type=bind,source=docker/odc/pyproject.toml,target=pyproject.toml \
    uv sync --locked --no-install-project --no-dev

# --- Runtime stage ---
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION} AS runtime

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

RUN apt-get update && apt-get install -y --no-install-recommends \
      postgresql-client \
      gettext-base \
      libpq5 \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY --from=builder /app/.venv /app/.venv
ENV PATH="/app/.venv/bin:$PATH"

ENV GDAL_DISABLE_READDIR_ON_OPEN="EMPTY_DIR" \
    CPL_VSIL_CURL_ALLOWED_EXTENSIONS=".tif,.tiff" \
    GDAL_HTTP_MAX_RETRY="10" \
    GDAL_HTTP_RETRY_DELAY="1"

COPY datacube.conf.template /home/odc/.datacube.conf.template

RUN useradd -m -s /bin/bash odc \
    && chown odc:odc /home/odc/.datacube.conf.template

COPY --chmod=0755 docker/odc/entrypoint.sh /entrypoint.sh

USER odc
WORKDIR /home/odc/app

ENTRYPOINT ["/entrypoint.sh"]
CMD ["tail", "-f", "/dev/null"]
