# Default target
.PHONY: help
help:
	@echo "Usage:"
	@echo "  make dev     - Run in development mode (with auto-reload)"
	@echo "  make prod    - Run in production mode (clean build, no reload)"
	@echo "  make clean   - Stop all containers and remove volumes"
	@echo "  make rebuild - Rebuild images and restart in dev mode"

# Development (with override)
.PHONY: dev
dev:
	docker-compose up --build

# Production (base compose only)
.PHONY: prod
prod:
	docker-compose -f docker-compose.yml up --build -d

# Stop + remove everything including volumes
.PHONY: clean
clean:
	docker-compose down -v

#Stop without removing volumes
.PHONY stop
stop:
	docker-compose down

# Rebuild all images from scratch and restart in dev
.PHONY: rebuild
rebuild:
	docker-compose build --no-cache
	docker-compose up
