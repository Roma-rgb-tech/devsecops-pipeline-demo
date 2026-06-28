# Architecture & Pipeline

## System Overview

```
Developer
    │
    │  git push
    ▼
GitHub Repository
    │
    ├──────────────────────────────────────────┐
    │                                          │
    ▼                                          ▼
CI Workflow (ci.yml)                    CD Workflow (cd.yml)
    │                                   (triggers only if CI passes)
    ├── 1. Lint (ruff)                        │
    ├── 2. Test (pytest)                      ├── Deploy to Railway
    ├── 3. Security Scan (Trivy)              └── Telegram notify ✅/❌
    └── 4. Telegram notify ✅/❌
                │
    ┌───────────┴──────────────┐
    │ Trivy blocks deploy if   │
    │ CRITICAL or HIGH CVE     │
    │ found in Docker image    │
    └──────────────────────────┘
```

## Application Architecture

```
HTTP Request
    │
    ▼
FastAPI App (app/main.py)
    │
    ├── GET  /              → HTML landing page
    ├── GET  /health        → JSON status + timestamp
    ├── GET  /version       → app version + Python info
    ├── GET  /metrics       → item & message counts
    ├── GET  /ping          → simple pong liveness
    │
    ├── GET  /items         → list all items (in-memory)
    ├── POST /items         → create item
    ├── GET  /items/{id}    → get by ID (404 if missing)
    ├── DELETE /items/{id}  → delete by ID (404 if missing)
    │
    ├── GET  /messages      → list all messages (in-memory)
    └── POST /messages      → post message
```

## Docker Setup

```
Dockerfile
    └── python:3.12-slim base
        ├── Copy requirements.txt
        ├── pip install
        ├── Copy app/
        ├── HEALTHCHECK (curl /health every 30s)
        └── CMD uvicorn app.main:app

docker-compose.yml
    └── service: api
        ├── build: .
        ├── ports: 8000:8000
        └── env_file: .env

docker-compose.override.yml  (local dev only)
    └── volumes: ./app:/app/app  (hot reload)
```

## Security Scanning

Trivy runs on every CI execution:

```bash
trivy image --exit-code 1 --severity CRITICAL,HIGH <image>
```

- Exit code `1` = pipeline fails, deploy is blocked
- Exit code `0` = clean, pipeline continues to CD

## Deployment

Railway auto-detects the Dockerfile and builds the container. CD is triggered via the official Railway GitHub Action with `RAILWAY_TOKEN` secret.

Deployment flow:
1. CI passes all checks
2. CD workflow starts
3. `railway up` pushes new image
4. Railway performs rolling update (zero downtime)
5. Telegram notification sent with live URL