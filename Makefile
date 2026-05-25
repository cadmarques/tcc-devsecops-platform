APP_DIR = apps/python-fastapi
IMAGE_NAME = devsecops-tcc/fastapi-app
TAG ?= latest

.PHONY: build run stop test scan sbom

build:
	docker build -t $(IMAGE_NAME):$(TAG) $(APP_DIR)

run:
	docker compose -f $(APP_DIR)/docker-compose.yml up --build

stop:
	docker compose -f $(APP_DIR)/docker-compose.yml down

test:
	docker run --rm -v $(shell pwd)/$(APP_DIR):/app -w /app python:3.11-slim bash -c "pip install -r requirements.txt && pytest tests/ -v"

scan:
	trivy image --exit-code 1 --severity HIGH,CRITICAL $(IMAGE_NAME):$(TAG)

sbom:
	syft dir:$(APP_DIR) -o cyclonedx-json > sbom-fastapi.json

clean:
	docker system prune -f