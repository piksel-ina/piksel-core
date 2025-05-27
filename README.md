# mini-piksel

Enable users to run the mini-piksel product on their local machines, providing a self-contained environment for managing and analyzing satellite data using Open Data Cube (ODC) for Indonesia region

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

    This will start all Docker containers using the images built in the previous step.

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

**More Commands:**
For a full list of available `make` commands and their descriptions, run:

```bash
make help
```

### CI/CD Workflow & Branch Naming for Docker Image Builds

The CI/CD pipeline automatically builds and pushes Docker images to the AWS ECR private repository based on branch and tag naming conventions:

- **Main Development:**  
  Commits to the `main` branch trigger a build and push Docker images tagged as `main` and `latest`.

- **Feature & Hotfix Branches:**  
  Branches named `feature/{feature-name}` or `hotfix/{hotfix-name}` trigger builds with images tagged accordingly (e.g., `feature-login`, `hotfix-urgent`).

- **Production & Staging Releases:**  
  Git tags following the format `vX.Y.Z` (e.g., `v1.2.3`) or pre-release tags like `v1.2.3-beta1` trigger builds and push images tagged for production or staging.
  - Use `vX.Y.Z` for production releases.
  - Use `vX.Y.Z-betaN` or similar for staging/pre-release.

All images are pushed to the AWS ECR private repository with tags that align with automated lifecycle policies, ensuring production, staging, and development images are managed and retained according to best practices.
