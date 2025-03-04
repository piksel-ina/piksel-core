FROM ghcr.io/osgeo/gdal:ubuntu-small-3.10.2

WORKDIR /app

ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Install runtime dependencies
RUN apt-get update && apt-get install -y \
      python3-full \
      python3-dev \
      python3-venv \
      git \
      build-essential \
      libpq-dev \
      postgresql-client \
    && apt-get clean \
    && rm -rf /var/lib/{apt,dpkg,cache,log}

# Create and activate virtual environment
RUN python3 -m venv /home/venv
ENV PATH="/home/venv/bin:$PATH"

# Copy and install test requirements first
COPY docker/test/requirements-test.txt /app/requirements-test.txt
RUN pip install --break-system-packages --no-cache-dir -r requirements-test.txt

# Copy datacube config
COPY datacube.conf /root/.datacube.conf

# Copy application code and tests
COPY . /app/

CMD ["pytest", "test/"]
