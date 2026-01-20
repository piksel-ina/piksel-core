# Piksel-core

Enable users to run the piksel services on their local machines, providing a self-contained environment for managing and analysing satellite data using Open Data Cube (ODC) for Indonesia region

## Services

Piksel-core consists of multiple services that work together to provide a complete satellite data management and analysis platform:

| Service                  | Description                                                                                | Documentation                                                      |
| ------------------------ | ------------------------------------------------------------------------------------------ | ------------------------------------------------------------------ |
| **PostgreSQL**           | Database backend with PostGIS extension for storing ODC metadata and spatial indices       | [PostgreSQL Docs](https://www.postgresql.org/docs/)                |
| **ODC (Open Data Cube)** | Core indexing and data management service for satellite imagery                            | [ODC Docs](https://datacube-core.readthedocs.io/)                  |
| **Jupyter Notebook**     | Interactive Python environment for data analysis, visualisation, and algorithm development | [Jupyter Docs](https://jupyter-notebook.readthedocs.io/)           |
| **Datacube Explorer**    | Web-based interface for browsing, searching, and visualizing indexed satellite datasets    | [Explorer Docs](https://github.com/opendatacube/datacube-explorer) |

## Prerequisites

- **Docker:** For installation documentation, please refer to [Docker's official documentation](https://docs.docker.com/get-docker/).
- **Make:** Required for using the Makefile automation

## Quick Start

Follow these steps to get your ODC environment up and running:

1.  **Clone the Repository:**

    ```bash
    git clone https://github.com/piksel-ina/piksel-core.git
    cd piksel-core/
    ```

2.  **Setup Environment:**

    ```bash
    make setup
    ```

    This creates a .env file from .env.example and generates the ODC configuration (datacube.conf).

    > The generated .env and datacube.conf are starter template. Use them as-is or customise them for your environment before continuing..

3.  **Build the Docker Images:**

    ```bash
    make build
    ```

    This command builds the Docker images for your ODC environment. 

4.  **Start the Services:**

    ```bash
    # Start Core services only (PostgreSQL + ODC)
    make up

    # Start Core + Jupyter Notebook (if needed)
    make up-jupyter 
    ```

5.  **Initialise the Database:**

    ```bash
    make init-db
    ```

    This initialises the ODC database schema.

6.  **Add Product Definitions:**

    ```bash
    make all-products
    ```

    This adds all product definitions from the `products/` directory to the ODC.

7.  **Index Data (Example):**

    ```bash
    make index-sentinel2
    ```

    This indexes Sentinel-2 L2A data with default parameters. You can customise the parameters by passing variables:

    ```bash
    make index-sentinel2 Bbox='115,-10,117,-8' Date='2021-01-01/2021-01-31'
    ```

8. **More Commands:**

    For a full list of available `make` commands and their descriptions, run:

    ```bash
    make help
    ```

9. **Stop the Environment:**

    Stopping and removing containers:

    ```bash
    make down
    ```

    


## For Developers


1. **View Service Status and logs:**

    ```bash
    make ps
    make logs
    ```

2. **Access Shells**:

    ```bash
    make bash-odc
    make psql
    make bash-jupyter
    ```

3. **Manage Products**

    ```bash
    make list-products                    # List all products
    make all-products                     # Add all products from products/
    make add-product F=product.yaml       # Add specific product
    make rm-product P=product_name        # Remove specific product
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
            Jupyter/Explorer (Analysis & Visualisation)
```

## Docker Build Workflows (GitHub Actions)

This repo contains GitHub Actions workflows to build and push Docker images to **AWS ECR**.

1. **Tag build**

    Runs automatically when push a Git tag:
    - `odc-*`
    - `ows-*`
    - `jupyter-*`
    - `dev-jupyter-*`

2. **Manual build**
    
    - Run from GitHub UI (Actions → Manual Docker Build) and select a component.
    
    - It tags the image using a date-based version vYYYYMMDD (example: odc-v20260120).