# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---


## [1.1.0] - 2025-06-25

### Added
- `/version` endpoint returning app version and Python runtime info
- `/metrics` endpoint returning counts of items and messages
- `/ping` liveness endpoint (separate from `/health`)
- `requirements-dev.txt` with dev/test dependencies isolated
- `docker-compose.override.yml` for local development overrides
- `Makefile` with shortcuts for common dev tasks (`run`, `test`, `lint`, `format`, `docker-up`)
- `.pre-commit-config.yaml` with ruff, black, and trailing-whitespace hooks
- `CONTRIBUTING.md` with development workflow guidelines
- `CHANGELOG.md` (this file)
- `docs/architecture.md` with system design and pipeline diagram
- `docs/api.md` with full API reference and curl examples
- GitHub Issue Templates for bug reports and feature requests
- `HEALTHCHECK` instruction in Dockerfile
- 9 additional pytest tests (negative cases: 404s, invalid payloads, empty fields)
- README badges for CI, CD, Python version, Docker, security, and license
- Roadmap section in README

### Changed
- README restructured with cleaner Quick Start and updated project structure tree

---

## [1.0.0] - 2025-06-24

### Added
- FastAPI REST API with Items and Messages CRUD endpoints
- Landing page at `/`
- Swagger UI at `/docs` and ReDoc at `/redoc`
- Health check endpoint at `/health`
- Docker + Docker Compose setup
- GitHub Actions CI pipeline (ruff lint → pytest → Trivy security scan → Telegram notify)
- GitHub Actions CD pipeline (auto-deploy to Railway on CI pass)
- Trivy container image scanning blocking CRITICAL/HIGH CVEs
- Telegram build notifications
- `.env.example` for environment configuration
- 16 pytest tests covering all endpoints
- `pytest.ini` configuration
