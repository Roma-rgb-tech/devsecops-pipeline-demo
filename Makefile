.PHONY: install run test lint format docker-up docker-down docker-build pre-commit clean help

help: 
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'

install:
	pip install -r requirements.txt -r requirements-dev.txt
	pre-commit install

run: 
	uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

test: 
	pytest tests/ -v --tb=short

lint:
	ruff check .

format: 
	black .

docker-build: 
	docker build -t devsecops-pipeline-demo .

docker-up: 
	docker compose up --build

docker-down: 
	docker compose down

pre-commit: 
	pre-commit run --all-files

clean: 
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null; \
	rm -rf .pytest_cache .ruff_cache