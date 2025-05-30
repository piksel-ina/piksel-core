# Use a GDAL image from OSGeo as the base
ARG GDAL_VERSION=ubuntu-small-3.11.0
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION}

# Set noninteractive mode for apt-get
ENV DEBIAN_FRONTEND=noninteractive

# Install system dependencies needed for Jupyter and analysis
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
      postgresql-server-dev-all \
      gettext-base \
    && apt-get autoclean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# (For development only: disable SSL verification for Git; remove in production)
ENV GIT_SSL_NO_VERIFY true

# Create a Python virtual environment and upgrade pip
RUN bash -c "python3 -m venv /home/venv && source /home/venv/bin/activate && pip install --upgrade pip"
ENV PATH="/home/venv/bin:$PATH"

# Configure pip to trust specific hosts
RUN pip config --global set global.trusted-host "pypi.org files.pythonhosted.org"

# Install base dependencies needed for ODC and Jupyter
RUN pip install --break-system-packages --no-cache-dir \
    jupyter \
    jupyterlab \
    odc-stac \
    odc-geo \
    "git+https://github.com/opendatacube/datacube-core.git@develop-1.9" \
    "git+https://github.com/opendatacube/eo-datasets.git@integrate-1.9" \
    boto3 \
    importlib_resources \
    psycopg2-binary \
    && pip install --break-system-packages --no-cache-dir \
    odc-ui \
    odc-stats \
    odc-io \
    odc-cloud \
    odc-dscache

# Copy and install additional Jupyter-specific dependencies
COPY docker/jupyter/requirements.jupyter.txt /tmp/requirements.jupyter.txt
RUN pip install --no-cache-dir -r /tmp/requirements.jupyter.txt

# Create a non-root user for Jupyter
RUN useradd -ms /bin/bash jupyter

# Ensure the notebooks directory exists and set as working directory
RUN mkdir -p /home/venv/notebooks
WORKDIR /home/venv/notebooks

# Copy datacube config template from root directory
COPY datacube.conf.template /home/venv/.datacube.conf.template

# Copy and setup entrypoint script
COPY docker/jupyter/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Change ownership of relevant directories
RUN chown -R jupyter:jupyter /home/venv

# Install tini via apt-get to ensure correct binary
RUN apt-get update && apt-get install -y tini

# Expose port 8888 for Jupyter Notebook
EXPOSE 8888

# Set Jupyter environment variables
ENV JUPYTER_PORT=8888
ENV JUPYTER_IP=0.0.0.0
ENV JUPYTER_ENABLE_LAB=yes

# Switch to non-root user
USER jupyter

# Use custom entrypoint with tini
ENTRYPOINT ["/usr/bin/tini", "--", "/entrypoint.sh"]

# Start Jupyter Lab with proper configuration
CMD ["jupyter", "lab", "--ip", "0.0.0.0", "--port", "8888", "--no-browser", "--allow-root", "--NotebookApp.token=''", "--NotebookApp.password=''"]