.PHONY: install run test lint format docker-up docker-down docker-build pre-commit clean help

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install: ## Install all dependencies (app + dev)
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

run: ## Run dev server with hot reload
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: ## Run pytest with coverage
	pytest tests/ -v --tb=short

lint: ## Lint with ruff
	ruff check .

format: ## Format with black
	black .

docker-build: ## Build Docker image
	docker build -t devsecops-pipeline-demo .

docker-up: ## Start with Docker Compose
	docker compose up --build

docker-down: ## Stop Docker Compose
	docker compose down

pre-commit: ## Run pre-commit hooks on all files
	pre-commit run --all-files

clean: ## Remove __pycache__ and .pytest_cache
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	rm -rf .pytest_cache .ruff_cache