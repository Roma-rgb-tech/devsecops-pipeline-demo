# 🚀 DevSecOps-pipeline-demo
<img width="1700" height="955" alt="image" src="https://github.com/user-attachments/assets/d2ca6470-e439-4fc1-b53f-b6cb424afe57" />


A FastAPI-based REST API built during a hackathon. Fully containerized with Docker, automatically tested and deployed to Railway via GitHub Actions CI/CD pipeline with security scanning powered by Trivy.

🌍 **Live:** [devsecops-pipeline-demo-production.up.railway.app](https://devsecops-pipeline-demo-production.up.railway.app/)

## ✨ Features

- REST API built with FastAPI
- Beautiful landing page at `/`
- Automatic API docs at `/docs` (Swagger UI) and `/redoc`
- Dockerized — runs the same everywhere
- CI/CD pipeline: lint → test → security scan → deploy
- Telegram notifications on every build

## 📋 Requirements

- [Docker](https://docs.docker.com/get-docker/) + Docker Compose
- Python 3.12+ (for local development without Docker)

## ⚡ Quick Start

```bash
# 1. Clone the repo
git clone <repo-url> && cd crispy-giggle

# 2. Create environment file
cp .env.example .env

# 3. Run with Docker (recommended)
docker compose up --build

# Or run locally without Docker
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Local app: **http://localhost:8000**  
Production: **devsecops-pipeline-demo-production.up.railway.app**  
API documentation: **https://devsecops-pipeline-demo-production.up.railway.app/docs**

## ☸️ Kubernetes (local)

Manifests available in `k8s/` folder for local deployment via minikube.

```bash
eval $(minikube docker-env)
docker build -t ghcr.io/roma-rgb-tech/devsecops-pipeline-demo:latest .
kubectl apply -f k8s/
minikube service fastapi-service
```

## 🗂️ Project Structure

```
crispy-giggle/
├── app/
│   ├── __init__.py
│   └── main.py           # FastAPI entry point + landing page
├── tests/
│   └── test_main.py      # Pytest test suite (16 tests)
├── .github/
│   └── workflows/
│       ├── ci.yml        # Lint + Test + Trivy security scan
│       └── cd.yml        # Auto-deploy to Railway
├── Dockerfile
├── docker-compose.yml
├── requirements.txt
├── pytest.ini
├── .env.example
└── .gitignore
```

## 🔄 CI/CD Pipeline

Every push to `main` triggers the full pipeline:

```
push to main
    │
    ├── CI
    │   ├── Lint          (ruff)
    │   ├── Tests         (pytest)
    │   ├── Security scan (Trivy — CRITICAL/HIGH)
    │   └── Notify        (Telegram)
    │
    └── CD  (only if CI passes)
        ├── Deploy to Railway
        └── Notify (Telegram)
```

## 🔐 GitHub Secrets

Configure these in **Settings → Secrets → Actions** before running the pipeline:

| Secret | Description |
|--------|-------------|
| `RAILWAY_TOKEN` | Railway API token (Account Settings → Tokens) |
| `RAILWAY_SERVICE_NAME` | Service name in your Railway project |
| `RAILWAY_PUBLIC_URL` | Public URL after deployment |
| `TELEGRAM_TO` | Telegram chat ID for notifications |
| `TELEGRAM_TOKEN` | Telegram bot token |

## 🌍 Environment Variables

Copy `.env.example` to `.env` and fill in the values:

```env
APP_ENV=development
APP_PORT=8000
```

> ⚠️ Never commit `.env` to Git — it is listed in `.gitignore`.

## 🧪 Running Tests

```bash
pytest tests/ -v
```

16 tests covering all endpoints: landing page, health check, full Items CRUD, and Messages.

## 🐳 Docker

```bash
# Build image
docker build -t crispy-giggle .

# Run container
docker run -p 8000:8000 crispy-giggle

# Run with compose
docker compose up --build
```

## 🛡️ Security

This project uses [Trivy](https://trivy.dev) to scan for vulnerabilities on every CI run. Any `CRITICAL` or `HIGH` severity finding will fail the pipeline and block deployment.

## 📬 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/` | Landing page |
| GET | `/health` | Service status + timestamp |
| GET | `/docs` | Swagger UI |
| GET | `/redoc` | ReDoc documentation |
| GET | `/items` | List all items |
| POST | `/items` | Create a new item |
| GET | `/items/{id}` | Get item by ID |
| DELETE | `/items/{id}` | Delete item by ID |
| GET | `/messages` | List all messages |
| POST | `/messages` | Post a new message |

### Item schema

```json
{
  "name": "Widget",
  "description": "Optional description",
  "price": 9.99,
  "in_stock": true
}
```

### Message schema

```json
{
  "text": "Hello world",
  "author": "alice"
}
```

## 📊 Monitoring & Observability
<img width="1689" height="923" alt="image" src="https://github.com/user-attachments/assets/6c944b3d-be5d-4384-b7d6-0ab92f30c6f7" />


This project is fully instrumented with a Prometheus + Loki + Grafana Cloud stack.

- Traces → OpenTelemetry SDK → OTel Collector → Grafana Tempo
- Metrics → Prometheus + prometheus-fastapi-instrumentator  
- Logs → python-logging-loki → Grafana Loki

### Stack

| Tool | Role | Integration |
|------|------|-------------|
| **Prometheus** | Metrics collection | `prometheus-fastapi-instrumentator` exposes `/metrics` |
| **Loki** | Log aggregation | `python-logging-loki` pushes structured JSON logs |
| **Grafana Cloud** | Visualisation & alerting | Prometheus + Loki as datasources |

### Dashboard panels

Live dashboard: [grafana.net/d/fea3x93t76328c](https://minicosmos2942.grafana.net/d/fea3x93t76328c/fastapi-obsrvability)

- **Total requests** — 24h counter (49 total during initial load testing)
- **Requests by endpoint** — GET `/`, `/docs`, `/redoc`, `/health`, `/openapi.json`
- **Requests Average Duration** — per-endpoint heatmap (675–687 ms range)
- **Percent of 2xx Requests** — success rate over time
- **Percent of 5xx Requests** — error rate over time
- **P99 Request Duration** — tail latency tracking
- **Requests per second** — throughput graph

### Local setup

The app auto-exposes metrics on startup via `prometheus-fastapi-instrumentator`:

```python
# app/main.py
from prometheus_fastapi_instrumentator import Instrumentator
Instrumentator().instrument(app).expose(app)
```

Logs are pushed to Loki in structured JSON format via `python-logging-loki`.

To connect your own Grafana instance, add these datasources:
- **Prometheus** → scrape `http://localhost:8000/metrics`
- **Loki** → configure `python-logging-loki` with your Loki push URL

---
 
## 🛡️ DevSecOps & Security Observability
 
Security scan results from every CI run are automatically ingested into **Splunk Enterprise** for centralized vulnerability tracking and alerting.
<img width="1866" height="956" alt="image" src="https://github.com/user-attachments/assets/75fe7471-4e6d-4c96-abf3-d9e7562bd626" />

 
### How it works
 
| Stage | Tool | Action |
|-------|------|--------|
| Scanning | Trivy | FS & container scan (CRITICAL/HIGH) |
| Ingestion | Splunk HEC | Secure HTTP POST with structured JSON |
| Analysis | SPL | Real-time CVE parsing by severity and package |
| Alerting | Splunk Alerts | Automated notifications on security regressions |
 
### CI integration
 
```yaml
# .github/workflows/ci.yml
- name: Push Trivy results to Splunk
  run: |
    curl -k -X POST "${{ secrets.SPLUNK_HEC_URL }}/services/collector/event" \
      -H "Authorization: Splunk ${{ secrets.SPLUNK_HEC_TOKEN }}" \
      -H "Content-Type: application/json" \
      -d "{\"sourcetype\": \"_json\", \"event\": $(cat security_scan_report.json)}"
```
 
### SPL queries
 
```spl
index="security" sourcetype="_json"
| rename "Results{}.Packages{}.Vulnerabilities{}.*" as *
| table VulnerabilityID, PkgName, InstalledVersion, Severity
| where isnotnull(VulnerabilityID)
| sort - Severity
```
---

