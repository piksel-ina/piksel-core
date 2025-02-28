# Use a GDAL image from OSGeo as the base
ARG GDAL_VERSION=ubuntu-small-3.10.2
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION}

# Set noninteractive mode for apt-get to avoid prompts during installation
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for building and running ODC
RUN apt-get update && apt-get install -y \
      python3-full \
      python3-dev \
      python3-venv \
      git \
      curl \
      ca-certificates \
      build-essential \
      postgresql-client \
      libpq-dev \
    && apt-get autoclean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Disable SSL verification for Git (not recommended for production)
ENV GIT_SSL_NO_VERIFY true

# Create a Python virtual environment and upgrade pip
RUN bash -c "python3 -m venv /home/venv && source /home/venv/bin/activate && pip install --upgrade pip"
ENV PATH="/home/venv/bin:$PATH"

# Configure pip to trust specific hosts
RUN pip config --global set global.trusted-host "pypi.org files.pythonhosted.org"

# Install Python packages (within the virtual environment)   
RUN pip install --break-system-packages \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --no-cache-dir \
    odc-stac \
    odc-geo \
    odc-cloud[ASYNC] \
    odc-dscache \
    boto3 \
    importlib_resources \
    psycopg2-binary \
    lark \
    sqlalchemy \
    alembic \
    geoalchemy2 \
    antimeridian \
    jsonschema \
    datadog \
    boltons \
    cattrs \
    ciso8601 \
    urlpath \
    click \
    fsspec \
    pystac-client>=0.2.0 \
    toolz \
    pyyaml \
    scipy \
    deprecat && \
    pip install --break-system-packages \
    --trusted-host pypi.org \
    --trusted-host files.pythonhosted.org \
    --no-cache-dir \
    --no-deps \
    "git+https://github.com/opendatacube/datacube-core.git@develop-1.9" \
    "git+https://github.com/opendatacube/odc-tools.git@develop-1.9#subdirectory=apps/dc_tools" \
    "git+https://github.com/opendatacube/eo-datasets.git@integrate-1.9"

# Copy the configuration file
COPY ../datacube.conf /root/.datacube.conf

# Copy the entrypoint script into the image
COPY docker/odc/entrypoint.sh /home/app/entrypoint.sh

# Set working directory
WORKDIR /home/app

# Set the entrypoint so that it runs before the CMD
ENTRYPOINT ["/home/app/entrypoint.sh"]

# Set the default command
CMD ["stac-to-dc"]
