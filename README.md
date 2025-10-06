# Piksel-core

Enable users to run the piksel services on their local machines, providing a self-contained environment for managing and analyzing satellite data using Open Data Cube (ODC) for Indonesia region

## Services

Piksel-core consists of multiple services that work together to provide a complete satellite data management and analysis platform:

| Service                  | Description                                                                                | Documentation                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **PostgreSQL**           | Database backend with PostGIS extension for storing ODC metadata and spatial indices       | [PostgreSQL Docs](https://www.postgresql.org/docs/)                |
| **ODC (Open Data Cube)** | Core indexing and data management service for satellite imagery                            | [ODC Docs](https://datacube-core.readthedocs.io/)                  |
| **Jupyter Notebook**     | Interactive Python environment for data analysis, visualization, and algorithm development | [Jupyter Docs](https://jupyter-notebook.readthedocs.io/)           |
| **Datacube Explorer**    | Web-based interface for browsing, searching, and visualizing indexed satellite datasets    | [Explorer Docs](https://github.com/opendatacube/datacube-explorer) |

## Prerequisites

- **Docker:** For installation documentation, please refer to [Docker's official documentation](https://docs.docker.com/get-docker/).
- **Make:** Required for using the Makefile automation (Linux/macOS recommended). For Windows users, you may need to run the Docker Compose commands directly or use WSL2 instead.

## Quick Start

Follow these steps to get your ODC environment up and running:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/piksel-ina/mini-piksel.git
    cd mini-piksel/
    ```

2.  **Initialize Environment:**

    ```bash
    make init
    ```

    This creates a .env file from .env.example and generates the ODC configuration (datacube.conf).

    > Important: Review and edit the .env file with appropriate settings for your environment.

3.  **Configuration:**

    - **Product Definitions:** Place your ODC product definition YAML files in the `products/` directory.
    - **Jupyter Notebooks:** Place your Jupyter notebooks in the `notebooks/` directory.

4.  **Build the Docker Images:**

    ```bash
    make build
    ```

    This command builds the Docker images for your ODC environment. This step is necessary before starting the containers.

5.  **Start the Services:**

    ```bash
    # Start Core services only (PostgreSQL + ODC)
    make up

    # Start Core + Jupyter Notebook
    make up-jupyter

    # Start Core + Datacube Explorer
    make up-explorer

    # Start All services (Core + Jupyter + Explorer)
    make up-all
    ```

6.  **Initialize the Database (First Time Only):**

    ```bash
    make init-db
    ```

    This initializes the ODC database schema.

7.  **Add Product Definitions:**

    ```bash
    make all-products
    ```

    This adds all product definitions from the `products/` directory to the ODC.

8.  **Index Data (Example):**

    ```bash
    make index-sentinel2a
    ```

    This indexes Sentinel-2 L2A data with default parameters. You can customize the parameters by passing variables:

    ```bash
    make index-sentinel2a Bbox='115,-10,117,-8' Date='2021-01-01/2021-01-31'
    ```

## For Developers

### Basic Management

- **Check Environment and ODC Configuration:**

  ```bash
  make check-env
  make check-config
  ```

- **View Service Status and logs:**

  ```bash
  make ps
  make logs
  ```

- **Stop the Environment:**

  ```bash
  make down
  ```

### Testing

1. **Install Test Dependencies**

```bash
make test-deps
```

2. **Run Tests**

- Run all tests: `make test`
- Run unit tests only: `make test-unit`
- Run integration tests only: `make test-integration`
- Run tests with verbose output: `make test-verbose`

For detailed information about our testing framework and practices, see the [Testing Documentation](tests/README.md).

### Access Shells:

```bash
make bash-odc
make bash-jupyter
make psql
```

### Database Management

```bash
make init-db        # Initialize ODC database
make reset-db       # Reset database (WARNING: destroys all data)
make backup-db      # Backup database to ./backups/
make spindex-create # Create spatial index
make spindex-update # Update spatial index
```

### Product Management

```bash
make list-products                    # List all products
make all-products                     # Add all products from products/
make add-product P=product.yaml       # Add specific product
make rm-product P=product_name        # Remove specific product
```

### Data Indexing

```bash
# Sentinel-2
make index-sentinel2 Bbox='115,-10,117,-8' Date='2021-01-01/2021-12-31'

# Landsat (Surface Reflectance)
make index-ls9-sr
make index-ls8-sr
make index-ls7-sr
make index-ls5-sr

# Landsat (Surface Temperature)
make index-ls9-st
make index-ls8-st
make index-ls7-st
make index-ls5-st

# Sentinel-1 RTC
make index-s1-rtc

# Index all Landsat products
make index-landsat
```

**More Commands:**

For a full list of available `make` commands and their descriptions, run:

```bash
make help
```

## Service Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                      Piksel-Core Platform                       │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────────┐   │
│  │  PostgreSQL  │◄─┤     ODC      │◄─┤   Jupyter Notebook   │   │
│  └──────────────┘  └──────────────┘  └──────────────────────┘   │
│         ▲                  ▲                                    │
│         │                  │                                    │
│         │          ┌───────┴──────────────┐                     │
│         └──────────┤  Datacube Explorer   │                     │
│                    └──────────────────────┘                     │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘

                    Data Flow:
    STAC Catalogs → ODC (Indexing) → PostgreSQL
                         ↓
            Jupyter/Explorer (Analysis & Visualization)
```

## CI/CD Workflow & Branch Naming for Docker Image Builds

The CI/CD pipeline automatically builds and pushes Docker images to the AWS ECR private repository based on branch and tag naming conventions:

- **Main Development:**  
  Commits to the `main` branch trigger a build and push Docker images tagged as `main` and `latest`.

- **Feature & Hotfix Branches:**  
  Branches named `feature/{feature-name}` or `hotfix/{hotfix-name}` trigger builds with images tagged accordingly (e.g., `feature-login`, `hotfix-urgent`).

All images are pushed to the AWS ECR private repository with tags that align with automated lifecycle policies, ensuring production, staging, and development images are managed and retained according to best practices.
