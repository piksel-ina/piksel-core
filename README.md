# mini-piksel

Enable users to run the mini-piksel product on their local machines, providing a self-contained environment for managing and analyzing satellite data using Open Data Cube (ODC) for Indonesia region

## Prerequisites

- **Docker:** Ensure Docker is installed on your system.
- **Docker Compose:** Ensure Docker Compose is installed on your system.

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

    > Important: Review and edit the .env file with appropriate settings for your environment, especially database credentials.

3.  **Configuration:**

    - **Product Definitions:** Place your ODC product definition YAML files in the `products/` directory.
    - **Jupyter Notebooks:** Place your Jupyter notebooks in the `notebooks/` directory.

4.  **Build the Docker Images:**

    ```bash
    make build
    ```

    This command builds the Docker images for your ODC environment. This step is necessary before starting the containers.

5.  **Start the Environment:**

    ```bash
    make up
    ```

    This will start all Docker containers using the images built in the previous step. Jupyter is accessible at `http://localhost:8888`.

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

9.  **Access Jupyter:**

    Open your web browser and navigate to http://localhost:8888. Use this command to retrieve the authentication token:

    ```bash
    make jupyter-token
    ```

## Working with the Environment

### Basic Management

- **Check Environment Configuration:**
  ```bash
  make check-env
  ```
- **Check ODC Configuration:**

  ```bash
  make check-config
  ```

- **View Service Status:**

  ```bash
  make ps
  ```

- **View Logs**
  ```bash
  make logs
  ```
- **Stop the Environment:**

  ```bash
  make down
  ```

### Access Shells:

```bash
make bash-odc
make bash-jupyter
make psql
```

## More Commands

For a full list of available `make` commands and their descriptions, run:

```bash
make help
```
