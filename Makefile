# Piksel Platform Makefile
# A set of commands to manage ODC development and deployment

# Settings
COMPOSE_FILE := docker/docker-compose.yml
COMPOSE_FILE_TEST := docker/docker-compose-test.yml
PROJECT_NAME := piksel
ENVIRONMENT ?= default
EPSG ?= 4326

# Common Docker Compose command with environment variables
DOCKER_COMPOSE = docker compose --env-file .env -f $(COMPOSE_FILE) -p $(PROJECT_NAME)

# Colors for pretty output
BLUE=\033[34;1m
GREEN=\033[32m
RED=\033[31m
YELLOW=\033[33m
NC=\033[0m # No Color

# Default target
.PHONY: help
help:
	@echo ""
	@echo "${BLUE}Piksel Platform Management Commands ${NC}"
	@echo "${GREEN}Basic Commands:${NC}"
	@echo "  make init          - Initialize environment files and configuration"
	@echo "  make ows-init      - Initialize OWS (after database is set up)"
	@echo "  make build-all		- Build all Docker images"
	@echo "  make build-odc     - Build ODC Docker images"
	@echo "  make build-jupyter - Build Jupyter Docker images"
	@echo "  make up            - Start ODC only"
	@echo "  make up-all        - Start ODC, Jupyter and Explorer services"
	@echo "  make up-jupyter    - Start ODC with Jupyter services"
	@echo "  make up-explorer   - Start ODC with Datacube Explorer services"
	@echo "  make up-ows     	- Start ODC with Open Web Services (OWS)"
	@echo "  make stop          - Stop all project containers (without removing them)"
	@echo "  make down          - Stop and remove all project containers (but preserve volumes)"
	@echo "  make rmvol         - Stop and remove project containers and volumes"
	@echo "  make restart       - Restart all services"
	@echo "  make ps            - Show service status"
	@echo "  make logs          - View logs from all services"
	@echo "  make clean         - Prune unused Docker resources"
	@echo ""
	@echo "${GREEN}Configuration Commands:${NC}"
	@echo "  make setup-config  - Generate datacube.conf from template"
	@echo "  make check-env     - Display environment variables"
	@echo "  make check-config  - Check datacube configuration"
	@echo ""
	@echo "${GREEN}Database Commands:${NC}"
	@echo "  make init-db          - Initialize the ODC database"
	@echo "  make reset-db         - Reset the ODC database (destroys all data)"
	@echo "  make spindex-create   - Add spatial index"
	@echo "  make spindex-update   - Populates or refreshes the spatial index"
	@echo "  make backup-db        - Backup the database"
	@echo "  make psql             - Open an interactive PostgreSQL shell"
	@echo "  make update-metadata  - Add or update metadata definition"
	@echo ""
	@echo "${GREEN}Product Commands:${NC}"
	@echo "  make list-products                   - List all registered products"
	@echo "  make all-products                    - Add all product definitions"
	@echo "  make add-product P=<product.yaml>    - Add a specific product definition"
	@echo "  make rm-product P=<product.yaml>     - Remove a specific product definition"
	@echo ""
	@echo "${GREEN}Indexing Commands:${NC}"
	@echo "  make index-sentinel2      - Index Sentinel-2 L2A data with the following defaults:"
	@echo "                               Bbox  (default: $(Bbox))"
	@echo "                               Date  (default: $(Date))"
	@echo ""
	@echo "  To override these defaults, pass new values as variables."
	@echo "  For example: ${GREEN}make index-sentinel2 Bbox='115,-10,117,-8' Date='2021-01-01/2021-01-31'${NC}"
	@echo ""
	@echo "  make index-ls9-st         - Index Landsat-9 Surface Temperature data"
	@echo "  make index-ls8-st         - Index Landsat-8 Surface Temperature data"
	@echo "  make index-ls7-st         - Index Landsat-7 Surface Temperature data"
	@echo "  make index-ls5-st         - Index Landsat-5 Surface Temperature data"
	@echo "  make index-ls9-sr         - Index Landsat-9 Surface Reflectance data"
	@echo "  make index-ls8-sr         - Index Landsat-8 Surface Reflectance data"
	@echo "  make index-ls7-sr         - Index Landsat-7 Surface Reflectance data"
	@echo "  make index-ls5-sr         - Index Landsat-5 Surface Reflectance data"
	@echo "  make index-s1-rtc         - Index Sentinel-1 RTC data"
	@echo ""
	@echo "${GREEN}Testing Commands:${NC}"
	@echo "  make test                   - Run all tests with minimal output"
	@echo "  make test-verbose           - Run all tests with detailed output"
	@echo "  make test-unit              - Run only unit tests"
	@echo "  make test-integration       - Run only integration tests"
	@echo "  make test-up                - Start test environment"
	@echo "  make test-down              - Stop and remove test environment"
	@echo "  make test-logs              - View test environment logs"
	@echo "  make test-deps              - Install test dependencies"
	@echo ""
	@echo "${GREEN}Dependency Management Commands:${NC}"
	@echo "  make compile-deps          - Compile all dependencies (ODC, Jupyter, Test)"
	@echo "  make compile-odc-deps      - Compile only ODC dependencies"
	@echo "  make compile-jupyter-deps  - Compile only Jupyter dependencies"
	@echo "  make compile-test-deps     - Compile only test dependencies"
	@echo "  make update-deps           - Update all dependencies to latest versions"
	@echo ""
	@echo "${GREEN}Utility Commands:${NC}"
	@echo "  make bash-odc               - Open a shell in the ODC container"
	@echo "  make bash-jupyter           - Open a shell in the Jupyter container"
	@echo "  make jupyter-token          - Get the Jupyter token"
	@echo ""


# Docker commands
.PHONY: build-odc build-jupyter build-ows build-all up up-jupyter up-explorer stop down rmvol restart ps logs clean setup-config init check-env check-config ows-init up-ows
build-odc:
	@echo "$(BLUE)Building odc docker image...$(NC)"
	$(DOCKER_COMPOSE) build odc

build-jupyter:
	@echo "$(BLUE)Building jupyter docker image...$(NC)"
	$(DOCKER_COMPOSE) build jupyter

build-jupyter-dev:
	@echo "$(BLUE)Building jupyter-dev docker image...$(NC)"
	$(DOCKER_COMPOSE) build jupyter-dev

build-ows:
	@echo "$(BLUE)Building ows docker image...$(NC)"
	$(DOCKER_COMPOSE) build ows

build-all: build-odc build-jupyter build-ows
	@echo "$(GREEN)All Docker images built successfully!$(NC)"

setup-config:
	@echo "$(BLUE)Generating datacube.conf from template...$(NC)"
	@chmod +x scripts/generate_config.sh
	@export $$(grep -v '^#' .env | xargs) && ./scripts/generate_config.sh
	@echo "$(GREEN)Configuration generated successfully!$(NC)"

init:
	@if [ ! -f .env ]; then \
		cp .env.example .env; \
		echo "$(GREEN)Created .env file from template. Please edit with your local settings.$(NC)"; \
	else \
		echo "$(YELLOW).env file already exists. Skipping.$(NC)"; \
	fi
	@$(MAKE) setup-config

ows-init: setup-config
	@echo "$(BLUE)Initializing OWS...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	echo "${BLUE}Check Datacube Connection:${NC}" && \
	COMPOSE_PROFILES=ows $(DOCKER_COMPOSE) run --rm ows datacube system check && \
	COMPOSE_PROFILES=ows $(DOCKER_COMPOSE) run --rm ows datacube-ows-update --schema --write-role $$ODC_DEFAULT_DB_USERNAME && \
	COMPOSE_PROFILES=ows $(DOCKER_COMPOSE) run --rm ows datacube-ows-update s2_l2a && \
	echo "$(GREEN)OWS Initialized$(NC)"

check-env:
	@echo "$(BLUE)Environment variables:$(NC)"
	@grep -v '^#' .env | sort
	@echo "$(BLUE)Docker environment check:$(NC)"
	@$(DOCKER_COMPOSE) config | grep -E 'POSTGRES_|JUPYTER_PORT'

check-config:
	@echo "$(BLUE)Checking datacube configuration:$(NC)"
	@if [ -f datacube.conf ]; then \
		cat datacube.conf; \
	else \
		echo "$(RED)datacube.conf not found!$(NC)"; \
	fi
	@echo "\n$(BLUE)Environment variables in .env:$(NC)"
	@grep -v '^#' .env | sort

up: setup-config
	@echo "$(BLUE)Starting Piksel Base services...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	$(DOCKER_COMPOSE) up -d && \
	echo "$(BLUE)ODC and PostgreSQL Services Started$(NC)" && \
	echo "To Start With Jupyter Notebook: $(BLUE)make up-jupyter$(NC)" && \
	echo "To Start With Datacube Explorer: $(BLUE)make up-explorer$(NC)"

up-jupyter: setup-config
	@echo "$(BLUE)Starting Piksel Base services...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	COMPOSE_PROFILES=jupyter $(DOCKER_COMPOSE) up -d && \
	echo "$(GREEN)Services started. Jupyter is available at http://localhost:$$JUPYTER_PORT$(NC)"

up-jupyter-dev: setup-config
	@echo "$(BLUE)Starting With Jupyter Development Container...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	COMPOSE_PROFILES=jupyter-dev $(DOCKER_COMPOSE) up -d && \
	echo "$(GREEN)Services started. Jupyter is available at http://localhost:$$JUPYTER_PORT$(NC)"

up-explorer: setup-config
	@echo "$(BLUE)Starting Piksel Base services...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	COMPOSE_PROFILES=explorer $(DOCKER_COMPOSE) up -d && \
	echo "$(GREEN)Services started. Datacube Explorer is available at http://localhost:$$EXPLORER_PORT$(NC)"

up-ows: setup-config
	@echo "$(BLUE)Starting Piksel OWS service...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	COMPOSE_PROFILES=ows $(DOCKER_COMPOSE) up -d && \
	echo "$(GREEN)OWS started. Available at http://localhost:$${OWS_PORT:-8000}$(NC)"

up-all: setup-config
	@echo "$(BLUE)Starting Piksel Base services...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	COMPOSE_PROFILES=jupyter,explorer,ows $(DOCKER_COMPOSE) up -d && \
	echo "$(GREEN)Services started. Jupyter is available at http://localhost:$$JUPYTER_PORT$(NC)" && \
	echo "$(GREEN)Services started. Datacube Explorer is available at http://localhost:$$EXPLORER_PORT$(NC)"

stop:
	@echo "$(BLUE)Stopping Piksel services...$(NC)"
	$(DOCKER_COMPOSE) stop

down:
	@echo "$(BLUE)Stopping and removing Piksel containers (preserving volumes)...$(NC)"
	COMPOSE_PROFILES=jupyter,jupyter-dev,explorer,ows $(DOCKER_COMPOSE) down

rmvol:
	@echo "$(BLUE)Stopping and removing Piksel containers and volumes...$(NC)"
	COMPOSE_PROFILES=jupyter,jupyter-dev,explorer,ows $(DOCKER_COMPOSE) down -v

restart:
	@echo "$(BLUE)Restarting Piksel services...$(NC)"
	$(DOCKER_COMPOSE) restart

ps:
	@echo "$(BLUE)Piksel service status:$(NC)"
	$(DOCKER_COMPOSE) ps

logs:
	@echo "$(BLUE)Viewing Piksel logs (press Ctrl+C to exit)...$(NC)"
	$(DOCKER_COMPOSE) logs -f

clean:
	@echo $(YELLOW)"WARNING: This will prune ALL unused Docker resources."$(NC)
	@echo "Do you want to proceed? (y/n)"; \
	read ans; \
	if [ "$$ans" = "y" ]; then \
		docker system prune -a -f; \
	else \
		echo "Aborted clean."; \
	fi

# DataCube System and Spatial Index Commands
.PHONY: init-db reset-db spindex-create spindex-update backup-db psql, update-metadata
init-db:
	@echo "$(BLUE)Initializing ODC database for environment '$(ENVIRONMENT)'...$(NC)"
	@echo "$(BLUE)1. Checking PostgreSQL connection...$(NC)"
	@$(DOCKER_COMPOSE) exec postgres psql -U piksel_user -d piksel_db -c "SELECT version();" || { echo "$(RED)Failed to connect to PostgreSQL$(NC)"; exit 1; }
	@echo "$(BLUE)2. Creating PostGIS extension...$(NC)"
	@$(DOCKER_COMPOSE) exec postgres psql -U piksel_user -d piksel_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
	@echo "$(BLUE)3. Initializing ODC system...$(NC)"
	@$(DOCKER_COMPOSE) exec odc bash -c "datacube -v system init"
	@echo "$(BLUE)4. Verifying ODC system...$(NC)"
	@$(DOCKER_COMPOSE) exec odc bash -c "datacube -v system check"
	@echo "$(BLUE)5. Listing available products (if any)...$(NC)"
	@$(DOCKER_COMPOSE) exec odc bash -c "datacube product list" || echo "$(YELLOW)No products available yet. This is normal for a fresh installation.$(NC)"
	@echo "$(GREEN)ODC database initialization successful!$(NC)"


reset-db:
	@echo "$(RED)WARNING: This will destroy all data in the ODC database for environment '$(ENVIRONMENT)'!$(NC)"
	@read -p "Are you sure you want to proceed? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "$(BLUE)Dropping public schema in PostgreSQL...$(NC)"; \
		$(DOCKER_COMPOSE) exec postgres psql -U piksel_user piksel_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"; \
		echo "$(BLUE)Reinitializing ODC database for environment '$(ENVIRONMENT)'...$(NC)"; \
		$(DOCKER_COMPOSE) exec odc datacube -E $(ENVIRONMENT) system init && \
		$(DOCKER_COMPOSE) exec odc datacube -E $(ENVIRONMENT) spindex create 9468 && \
		$(DOCKER_COMPOSE) exec odc datacube -E $(ENVIRONMENT) spindex update 9468; \
	else \
		echo "$(BLUE)Database reset cancelled$(NC)"; \
	fi

spindex-create:
	@echo "$(BLUE)Adding spatial index for EPSG:$(EPSG)...$(NC)"
	$(DOCKER_COMPOSE) exec odc datacube spindex create $(EPSG)

spindex-update:
	@echo "$(BLUE)Updating spatial index for EPSG:$(EPSG)...$(NC)"
	$(DOCKER_COMPOSE) exec odc datacube spindex update $(EPSG)

backup-db:
	@echo "$(BLUE)Backing up ODC database...$(NC)"
	@mkdir -p ./backups
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	$(DOCKER_COMPOSE) exec -T postgres pg_dump -U piksel_user piksel_db | gzip > ./backups/piksel_db_$$timestamp.sql.gz; \
	@echo "$(GREEN)Database backup created in ./backups$(NC)"

psql:
	@echo "$(BLUE)Connecting to PostgreSQL database...$(NC)"
	$(DOCKER_COMPOSE) exec postgres psql -U piksel_user -d piksel_db

update-metadata:
	@echo "$(BLUE)Adding or updating metadata definition...$(NC)"
	@$(DOCKER_COMPOSE) exec odc bash -c "datacube metadata update --allow-unsafe /home/venv/metadata/custom_metadata.odc-type.yaml"
	@echo "$(GREEN)Metadata add/update complete!$(NC)"

cubedash-init: 
	@echo "$(BLUE)Initializing Datacube Explorer...$(NC)"
	$(DOCKER_COMPOSE) exec datacube-explorer cubedash-gen --init --all

# Product commands
.PHONY: list-products all-products add-product rm-product check

check:
	@echo "$(BLUE)Checking system...$(NC)"
	$(DOCKER_COMPOSE) exec odc datacube system check

list-products:
	@echo "${BLUE}Listing ODC products:${NC}"
	$(DOCKER_COMPOSE) exec odc datacube product list

all-products:
	@echo "${BLUE}Adding all product definitions...${NC}"
	@for product in products/*.yaml; do \
		echo "${YELLOW}Adding product: $$product${NC}"; \
		$(DOCKER_COMPOSE) exec -T odc bash -c "datacube product add /home/venv/products/$$(basename $$product)" || echo "${RED}Failed to add product: $$product${NC}"; \
	done

add-product:
	@if [ -z "$(P)" ]; then \
		echo "${RED}Error: Missing product file. Usage: make add-product P=<product.yaml>${NC}"; \
		exit 1; \
	fi
	@echo "${BLUE}Adding product definition: $(P)${NC}"
	$(DOCKER_COMPOSE) exec -T odc bash -c "datacube product add /home/venv/products/$(P)"
	

rm-product:
	@if [ -z "$(P)" ]; then \
		echo "$(RED)Error: Missing product name. Usage: make rm-product P=<product_name>$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Removing product '$(P)' using SQL script...$(NC)"
	@cat scripts/delete_odc_product.sql | $(DOCKER_COMPOSE) exec -T postgres \
		psql -U piksel_user -d piksel_db -v product_name="$(P)"


# Indexing commands
# STAC Catalog URLs
LANDSATLOOK ?= https://landsatlook.usgs.gov/stac-server/

# Default parameters for indexing
Bbox ?= 105,-8,106,-5
Date ?= 2022-01-01/2022-07-31
CollectionS2 ?= sentinel-2-l2a


# Default parameters for LSX indexing (adjust these as appropriate)
DateLsOld ?= 2000-01-01/2000-07-31
CollectionLsSR ?= landsat-c2l2-sr
CollectionLsST ?= landsat-c2l2-st

LIMIT ?= 9999

.PHONY: index-sentinel2 index-s1-rtc index-ls9-st index-ls8-st index-ls7-st index-ls5-st \
	index-ls9-sr index-ls8-sr index-ls7-sr index-ls5-sr index-all

# Index all products
index-all: index-sentinel2 index-landsat index-s1-rtc
	@echo "$(GREEN)All products indexed successfully!$(NC)"

index-landsat-sr: index-ls9-sr index-ls8-sr index-ls7-sr index-ls5-sr

index-landsat-st: index-ls9-st index-ls8-st index-ls7-st index-ls5-st

index-landsat: index-landsat-sr index-landsat-st

# Sentinel-2 L2A
index-sentinel2:
	@echo "$(BLUE)Indexing Sentinel-2 L2A data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='https://earth-search.aws.element84.com/v1/' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionS2)' \
	            --datetime='$(Date)' \
	            --rename-product='s2_l2a'

# Sentinel 2 C0
index-s2-c0:
	@echo "$(BLUE)Indexing Sentinel-2 L2A Collection 0 data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='https://earth-search.aws.element84.com/v1/' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionS2)' \
	            --datetime='$(Date)' \
	            --rename-product='sentinel_2_l2a_c0'

# Landsat Surface Temperature
index-ls9-st:
	@echo "$(BLUE)Indexing LS9 C2L2 ST data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsST)' \
	            --datetime='$(Date)' \
	            --rename-product='ls9_c2l2_st' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_9\"]}}" \


index-ls8-st:
	@echo "$(BLUE)Indexing LS8 C2L2 ST data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsST)' \
	            --datetime='$(Date)' \
	            --rename-product='ls8_c2l2_st' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_8\"]}}" \

index-ls7-st:
	@echo "$(BLUE)Indexing LS7 C2L2 ST data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsST)' \
	            --datetime='$(DateLsOld)' \
	            --rename-product='ls7_c2l2_st' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_7\"]}}" \

index-ls5-st:
	@echo "$(BLUE)Indexing LS5 C2L2 ST data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsST)' \
	            --datetime='$(DateLsOld)' \
	            --rename-product='ls5_c2l2_st' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_5\"]}}" \

# Landsat Surface Reflectance
index-ls9-sr:
	@echo "$(BLUE)Indexing LS9 C2L2 SR data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsSR)' \
	            --datetime='$(Date)' \
	            --rename-product='ls9_c2l2_sr' \
	            --url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_9\"]}}" \


index-ls8-sr:
	@echo "$(BLUE)Indexing LS8 C2L2 SR data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsSR)' \
	            --datetime='$(Date)' \
	            --rename-product='ls8_c2l2_sr' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_8\"]}}" \

index-ls7-sr:
	@echo "$(BLUE)Indexing LS7 C2L2 SR data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsSR)' \
	            --datetime='$(DateLsOld)' \
	            --rename-product='ls7_c2l2_sr' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_7\"]}}" \

index-ls5-sr:
	@echo "$(BLUE)Indexing LS5 C2L2 SR data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='${LANDSATLOOK}' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionLsSR)' \
	            --datetime='$(DateLsOld)' \
	            --rename-product='ls5_c2l2_sr' \
				--url-string-replace='https://landsatlook.usgs.gov/data,s3://usgs-landsat' \
	            --limit=$(LIMIT) \
	            --options="query={\"platform\":{\"in\":[\"LANDSAT_5\"]}}" \

index-s1-rtc:
	@echo "$(BLUE)Indexing Sentinel-1 RTC data...$(NC)"
	$(DOCKER_COMPOSE) exec odc \
	  stac-to-dc --catalog-href='https://planetarycomputer.microsoft.com/api/stac/v1/' \
	            --bbox='$(Bbox)' \
	            --collections='sentinel-1-rtc' \
	            --datetime='$(Date)' \
	            --rename-product='s1_rtc'
	            --limit=$(LIMIT) 

# Utility commands
.PHONY: bash-odc bash-jupyter jupyter-token
bash-odc:
	@echo "${BLUE}Opening shell in ODC container...${NC}"
	$(DOCKER_COMPOSE) exec odc bash

bash-jupyter:
	@echo "${BLUE}Opening shell in Jupyter container...${NC}"
	$(DOCKER_COMPOSE) exec jupyter bash

jupyter-token:
	@echo "${BLUE}Getting Jupyter token...${NC}"
	@token=$$($(DOCKER_COMPOSE) exec -T jupyter jupyter server list | grep -oP "token=\K[^[:space:]]*" || echo "No token found"); \
	if [ "$$token" != "No token found" ]; then \
		echo "${GREEN}Jupyter URL: http://localhost:8888/?token=$$token${NC}"; \
	else \
		echo "${YELLOW}No token found. Authentication may be disabled.${NC}"; \
		echo "${GREEN}Jupyter URL: http://localhost:8888/${NC}"; \
	fi

# Dependencies management commands
.PHONY: compile-deps compile-odc-deps compile-jupyter-deps  update-deps

# Compile all dependencies
compile-deps: compile-odc-deps compile-jupyter-deps 
	@echo "$(GREEN)All dependencies compiled successfully!$(NC)"

# Compile ODC dependencies
compile-odc-deps:
	@echo "$(BLUE)Compiling ODC dependencies using uv...$(NC)"
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv pip compile docker/odc/requirements.in -o docker/odc/requirements.txt
	@echo "$(GREEN)ODC dependencies compiled!$(NC)"

# Compile Jupyter dependencies
compile-jupyter-deps:
	@echo "$(BLUE)Compiling Jupyter dependencies using uv...$(NC)"
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	@uv pip compile docker/jupyter/requirements.in -o docker/jupyter/requirements.txt
	@echo "$(GREEN)Jupyter dependencies compiled!$(NC)"

# Update all dependencies to latest versions
update-deps:
	@echo "$(BLUE)Updating all dependencies to their latest versions using uv...$(NC)"
	@command -v uv >/dev/null 2>&1 || curl -LsSf https://astral.sh/uv/install.sh | sh
	@echo "$(YELLOW)Updating ODC dependencies...$(NC)"
	@uv pip compile docker/odc/requirements.in -o docker/odc/requirements.txt --upgrade
	@echo "$(YELLOW)Updating Jupyter dependencies...$(NC)"
	@uv pip compile docker/jupyter/requirements.in -o docker/jupyter/requirements.txt --upgrade
	@echo "$(GREEN)All dependencies updated successfully!$(NC)"

# Test Settings
TEST_PROJECT_NAME := piksel-test
TEST_VENV_DIR := .venv
PYTEST_ARGS ?= -v

# Test commands
.PHONY: test-up test-down test-logs test-ps test test-venv test-deps test-verbose test-clean

# Start test environment with test project name (creates isolated network)
test-up: setup-config
	@echo "$(BLUE)Starting Piksel test services...$(NC)"
	@export $$(grep -v '^#' .env | xargs) && \
	docker compose --env-file .env -f $(COMPOSE_FILE_TEST) -p $(TEST_PROJECT_NAME) up -d && \
	echo "$(GREEN)Test services started with project name: $(TEST_PROJECT_NAME)$(NC)"

# Stop and remove test services
test-down:
	@echo "$(BLUE)Stopping and removing Piksel test containers...$(NC)"
	docker compose --env-file .env -f $(COMPOSE_FILE_TEST) -p $(TEST_PROJECT_NAME) down -v 
	@echo "$(GREEN)Test environment removed$(NC)"

# View logs from test services
test-logs:
	@echo "$(BLUE)Viewing Piksel test logs (press Ctrl+C to exit)...$(NC)"
	docker compose --env-file .env -f $(COMPOSE_FILE_TEST) -p $(TEST_PROJECT_NAME) logs -f

# Create a Python virtual environment for testing
test-venv:
	@echo "$(BLUE)Creating Python virtual environment for testing...$(NC)"
	python3 -m venv $(TEST_VENV_DIR)
	@echo "$(GREEN)Virtual environment created at $(TEST_VENV_DIR)$(NC)"
	@echo "$(YELLOW)Activate with: source $(TEST_VENV_DIR)/bin/activate$(NC)"

# Install test dependencies in virtual environment
test-deps: test-venv
	@echo "$(BLUE)Installing test dependencies...$(NC)"
	$(TEST_VENV_DIR)/bin/pip install --upgrade pip
	$(TEST_VENV_DIR)/bin/pip install pytest pytest-cov python-dotenv pyyaml
	@echo "$(GREEN)Test dependencies installed$(NC)"

# Run tests (requires virtual environment)
test: test-up
	@echo "$(BLUE)Running tests...$(NC)"
	@if [ ! -d "$(TEST_VENV_DIR)" ]; then \
		echo "$(RED)Virtual environment not found. Run 'make test-deps' first.$(NC)"; \
		exit 1; \
	fi
	@echo "$(YELLOW)Running pytest...$(NC)"
	@( $(TEST_VENV_DIR)/bin/pytest $(PYTEST_ARGS) tests/ ; test_exit=$$? ; \
	  echo "$(BLUE)Cleaning up test environment...$(NC)" ; \
	  $(MAKE) test-down > /dev/null 2>&1 ; \
	  exit $$test_exit )

test-unit: 
	@echo "$(BLUE)Running unit tests...$(NC)"
	@if [ ! -d "$(TEST_VENV_DIR)" ]; then \
		echo "$(RED)Virtual environment not found. Run 'make test-deps' first.$(NC)"; \
		exit 1; \
	fi
	$(TEST_VENV_DIR)/bin/pytest $(PYTEST_ARGS) tests/unit

test-integration: test-up
	@echo "$(BLUE)Running integration tests...$(NC)"
	@if [ ! -d "$(TEST_VENV_DIR)" ]; then \
		echo "$(RED)Virtual environment not found. Run 'make test-deps' first.$(NC)"; \
		exit 1; \
	fi
	@( $(TEST_VENV_DIR)/bin/pytest $(PYTEST_ARGS) tests/integration ; test_exit=$$? ; \
	  echo "$(BLUE)Cleaning up test environment...$(NC)" ; \
	  $(MAKE) test-down > /dev/null 2>&1 ; \
	  exit $$test_exit )

test-verbose: PYTEST_ARGS=-xvs
test-verbose: test
	@echo "$(GREEN)Test complete$(NC)"
	# Add this with your other test commands

test-clean: test-down
	@echo "$(BLUE)Cleaning up all test artifacts...$(NC)"
	@echo "$(YELLOW)Cleaning up Docker test networks...$(NC)"
	@docker network prune -f --filter "name=$(TEST_PROJECT_NAME)" 2>/dev/null || true
	@echo "$(YELLOW)Removing Docker test images...$(NC)"
	@docker images --format "{{.Repository}}:{{.Tag}}" | grep "$(TEST_PROJECT_NAME)" | xargs -r docker rmi -f 2>/dev/null || true
	@echo "$(YELLOW)Removing dangling Docker images from tests...$(NC)"
	@docker image prune -f 2>/dev/null || true
	@echo "$(YELLOW)Removing pytest cache...$(NC)"
	@rm -rf .pytest_cache
	@find . -name "__pycache__" -type d -exec rm -rf {} +  2>/dev/null || true
	@echo "$(YELLOW)Removing coverage reports...$(NC)"
	@rm -f .coverage
	@rm -rf htmlcov
	@echo "$(YELLOW)Cleaning up test virtual environment...$(NC)"
	@rm -rf $(TEST_VENV_DIR)
	@echo "$(GREEN)Test environment completely cleaned!$(NC)"
