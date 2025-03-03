# Piksel Platform Makefile
# A set of commands to manage ODC development and deployment

# Settings
COMPOSE_FILE := docker/docker-compose.yml
PROJECT_NAME := piksel
# Default Data Cube environment (can be "main" or "legacy")
ENVIRONMENT ?= default
EPSG ?= 9468

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
	@echo "${BLUE}Piksel Platform Management Commands${NC}"
	@echo "${GREEN}Basic Commands:${NC}"
	@echo "  make build         - Build all Docker containers"
	@echo "  make up            - Start all services"
	@echo "  make stop          - Stop all project containers (without removing them)"
	@echo "  make down          - Stop and remove all project containers (but preserve volumes)"
	@echo "  make rmvol         - Stop and remove project containers and volumes"
	@echo "  make restart       - Restart all services"
	@echo "  make ps            - Show service status"
	@echo "  make logs          - View logs from all services"
	@echo "  make clean         - Prune unused Docker resources"
	@echo ""
	@echo "${GREEN}Database Commands:${NC}"
	@echo "  make init-db          - Initialize the ODC database"
	@echo "  make reset-db         - Reset the ODC database (destroys all data)"
	@echo "  make spindex-create   - Add spatial index"
	@echo "  make spindex-update   - Populates or refreshes the spatial index"
	@echo "  make backup-db        - Backup the database"
	@echo "  make psql             - Open an interactive PostgreSQL shell"
	@echo ""
	@echo "${GREEN}Product Commands:${NC}"
	@echo "  make list-products                   - List all registered products"
	@echo "  make all-products                    - Add all product definitions"
	@echo "  make add-product P=<product.yaml>    - Add a specific product definition"
	@echo "  make rm-product P=<product.yaml>     - Remove a specific product definition"
	@echo ""
	@echo "${GREEN}Indexing Commands:${NC}"
	@echo "  make index-sentinel2a      - Index Sentinel-2 L2A data with the following defaults:"
	@echo "       BboxS2        (default: $(BboxS2))"
	@echo "       DateS2        (default: $(DateS2))"
	@echo "       CollectionS2  (default: $(CollectionS2))"
	@echo ""
	@echo "To override these defaults, pass new values as variables."
	@echo "For example: ${GREEN}make index-sentinel2a Bbox='115,-10,117,-8' Date='2021-01-01/2021-01-31'${NC}"
	@echo ""
	@echo "${GREEN}Utility Commands:${NC}"
	@echo "  make bash-odc      - Open a shell in the ODC container"
	@echo "  make bash-jupyter  - Open a shell in the Jupyter container"
	@echo "  make jupyter-token - Get the Jupyter token"
	@echo "  make compile-deps   - Compile dependencies from requirements.in to requirements.txt"
	@echo "  make update-deps    - Update all dependencies to their latest versions"
	@echo "  make verify-deps    - Verify dependencies are correctly installed"

# Docker commands
.PHONY: build up stop down rmvol restart ps logs clean
build:
	@echo "$(BLUE)Building Piksel containers...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) build

up:
	@echo "$(BLUE)Starting Piksel services...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) up -d
	@echo "$(GREEN)Services started. Jupyter is available at http://localhost:8888$(NC)"

stop:
	@echo "$(BLUE)Stopping Piksel services...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) stop

down:
	@echo "$(BLUE)Stopping and removing Piksel containers (preserving volumes)...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down

rmvol:
	@echo "$(BLUE)Stopping and removing Piksel containers and volumes...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) down -v

restart:
	@echo "$(BLUE)Restarting Piksel services...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) restart

ps:
	@echo "$(BLUE)Piksel service status:$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) ps

logs:
	@echo "$(BLUE)Viewing Piksel logs (press Ctrl+C to exit)...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) logs -f

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
.PHONY: init-db reset-db spindex-create spindex-update backup-db psql
init-db:
	@echo "$(BLUE)Initializing ODC database for environment '$(ENVIRONMENT)'...$(NC)"
	@docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec postgres psql -U piksel_user -d piksel_db -c "CREATE EXTENSION IF NOT EXISTS postgis;"
	@docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube -v system init
	@docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube -v system check

reset-db:
	@echo "$(RED)WARNING: This will destroy all data in the ODC database for environment '$(ENVIRONMENT)'!$(NC)"
	@read -p "Are you sure you want to proceed? [y/N] " confirm; \
	if [ "$$confirm" = "y" ] || [ "$$confirm" = "Y" ]; then \
		echo "$(BLUE)Dropping public schema in PostgreSQL...$(NC)"; \
		docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec postgres psql -U piksel_user piksel_db -c "DROP SCHEMA public CASCADE; CREATE SCHEMA public;"; \
		echo "$(BLUE)Reinitializing ODC database for environment '$(ENVIRONMENT)'...$(NC)"; \
		docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube -E $(ENVIRONMENT) system init && \
		docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube -E $(ENVIRONMENT) spindex create 9468 && \
		docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube -E $(ENVIRONMENT) spindex update 9468; \
	else \
		echo "$(BLUE)Database reset cancelled$(NC)"; \
	fi

spindex-create:
	@echo "$(BLUE)Adding spatial index for EPSG:$(EPSG)...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube spindex create $(EPSG)

spindex-update:
	@echo "$(BLUE)Updating spatial index for EPSG:$(EPSG)...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube spindex update $(EPSG)

backup-db:
	@echo "$(BLUE)Backing up ODC database...$(NC)"
	@mkdir -p ./backups
	@timestamp=$$(date +%Y%m%d_%H%M%S); \
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T postgres pg_dump -U piksel_user piksel_db | gzip > ./backups/piksel_db_$$timestamp.sql.gz; \
	echo "$(GREEN)Database backup created in ./backups$(NC)"

psql:
	@echo "$(BLUE)Connecting to PostgreSQL database...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec postgres psql -U piksel_user -d piksel_db

# Product commands
.PHONY: list-products all-products add-product rm-product
list-products:
	@echo "${BLUE}Listing ODC products:${NC}"
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc datacube product list

all-products:
	@echo "${BLUE}Adding all product definitions...${NC}"
	@for product in products/*.yaml; do \
		echo "${YELLOW}Adding product: $$product${NC}"; \
		docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T odc bash -c "datacube product add /home/venv/products/$$(basename $$product)" || echo "${RED}Failed to add product: $$product${NC}"; \
	done

add-product:
	@if [ -z "$(P)" ]; then \
		echo "${RED}Error: Missing product file. Usage: make add-product P=<product.yaml>${NC}"; \
		exit 1; \
	fi
	@echo "${BLUE}Adding product definition: $(P)${NC}"
	@docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T odc bash -c "datacube product add /home/venv/products/$(P)"
	

rm-product:
	@if [ -z "$(P)" ]; then \
		echo "$(RED)Error: Missing product name. Usage: make rm-product P=<product_name>$(NC)"; \
		exit 1; \
	fi
	@echo "$(BLUE)Removing product '$(P)' using SQL script...$(NC)"
	@cat scripts/delete_odc_product.sql | docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T postgres \
		psql -U piksel_user -d piksel_db -v product_name="$(P)"


# Indexing commands
# Default parameters for indexing
Bbox ?= 114,-9,116,-7
Date ?= 2020-01-01/2020-03-31
CollectionS2 ?= sentinel-2-l2a

# Default parameters for LSX indexing (adjust these as appropriate)
BboxLs ?= 112,-10,118,-6
DateLs ?= 2020-06-01/2020-06-30
CollectionLs ?= landsat-8

.PHONY: index-sentinel2a 

index-sentinel2a:
	@echo "$(BLUE)Indexing Sentinel-2 L2A data...$(NC)"
	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc \
	  stac-to-dc --catalog-href='https://earth-search.aws.element84.com/v1/' \
	            --bbox='$(Bbox)' \
	            --collections='$(CollectionS2)' \
	            --datetime='$(Date)' \
	            --rename-product='sentinel_2_l2a'

# index-lsx:
# 	@echo "$(BLUE)Indexing LSX data...$(NC)"
# 	docker compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc \
# 	  stac-to-dc --catalog-href='https://earth-search.aws.element84.com/v1/' \
# 	            --bbox='$(BboxLs)' \
# 	            --collections='$(CLs)' \
# 	            --datetime='$(DateLs)' \
# 	            --rename-product='lsx'


# Utility commands
.PHONY: bash-odc bash-jupyter jupyter-token
bash-odc:
	@echo "${BLUE}Opening shell in ODC container...${NC}"
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec odc bash

bash-jupyter:
	@echo "${BLUE}Opening shell in Jupyter container...${NC}"
	docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec jupyter bash

jupyter-token:
	@echo "${BLUE}Getting Jupyter token...${NC}"
	@token=$$(docker-compose -f $(COMPOSE_FILE) -p $(PROJECT_NAME) exec -T jupyter jupyter server list | grep -oP "token=\K[^[:space:]]*" || echo "No token found"); \
	if [ "$$token" != "No token found" ]; then \
		echo "${GREEN}Jupyter URL: http://localhost:8888/?token=$$token${NC}"; \
	else \
		echo "${YELLOW}No token found. Authentication may be disabled.${NC}"; \
		echo "${GREEN}Jupyter URL: http://localhost:8888/${NC}"; \
	fi

# Dependencies management commands
.PHONY: compile-deps update-deps verify-deps

compile-deps:
	@echo "$(BLUE)Compiling dependencies from requirements.in to requirements.txt...$(NC)"
	@docker run --rm -v $(shell pwd):/app -w /app python:3.12 \
		bash -c "apt-get update && apt-get install -y libpq-dev && \
		pip install pip-tools && \
		pip-compile docker/odc/requirements.in"
	@echo "$(GREEN)Dependencies compiled successfully!$(NC)"

update-deps:
	@echo "$(BLUE)Updating all dependencies to their latest versions...$(NC)"
	@docker run --rm -v $(shell pwd):/app -w /app python:3.12 \
		bash -c "apt-get update && apt-get install -y libpq-dev && \
		pip install pip-tools && \
		pip-compile --upgrade docker/odc/requirements.in"
	@echo "$(GREEN)Dependencies updated successfully!$(NC)"

verify-deps:
	@echo "$(BLUE)Verifying dependency installation (dry run)...$(NC)"
	@docker run --rm -v $(shell pwd):/app -w /app python:3.12 \
		bash -c 'apt-get update && apt-get install -y libpq-dev gdal-bin libgdal-dev && \
		echo "\n\033[32mPackages that would be installed:\033[0m" && \
		pip install --dry-run -r docker/odc/requirements.txt | grep -v "^Requirement already satisfied"'
	@echo "$(GREEN)Dependencies verified!$(NC)"