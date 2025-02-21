ARG GDAL_VERSION=ubuntu-small-3.10.2
FROM ghcr.io/osgeo/gdal:${GDAL_VERSION}

ENV DEBIAN_FRONTEND=noninteractive

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
    
    
# Create virtual environment and activate, and upgrade pip in a single RUN
RUN bash -c "python3 -m venv /home/venv && source /home/venv/bin/activate && pip install --upgrade pip"
    
ENV PATH="/home/venv/bin:$PATH"
    
# Install Python packages (within the virtual environment)    
RUN pip install --break-system-packages \
    odc-stac \
    odc-geo \
    "git+https://github.com/opendatacube/datacube-core.git@develop-1.9" \
    "git+https://github.com/opendatacube/odc-tools.git@develop-1.9#subdirectory=apps/dc_tools" \
    "git+https://github.com/opendatacube/eo-datasets.git@integrate-1.9" \
    "odc-cloud==0.2.3" \
    boto3 \
    jupyter \
    importlib_resources \
    psycopg2-binary

# Expose port 8888 for accessing Jupyter Notebook
EXPOSE 8888

RUN datacube --version
CMD ["jupyter", "notebook", "--ip", "0.0.0.0", "--port", "8888",  "--allow-root"]
