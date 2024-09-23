# Makefile for managing the Docker Compose setup

.PHONY: up down build logs test install lint

# Start the services
up:
	docker-compose up -d

# Stop the services
down:
	docker-compose down

# Build the services
build:
	docker-compose build

# View logs
logs:
	docker-compose logs -f

# Run tests
test:
	cd app && PYTHONPATH=. poetry run pytest

# Install dependencies
install:
	cd app && poetry install

# Lint the code
lint:
	cd app && poetry run flake8 .