import os
import time 

from fastapi import FastAPI, HTTPException, Request 
from prometheus_fastapi_instrumentator import Instrumentator
from app.logger import logger
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from datetime import datetime, UTC
from typing import Optional
from fastapi import FastAPI
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import uvicorn

app = FastAPI()

FastAPIInstrumentor.instrument_app(app)

@app.get("/")
async def root():
    return {"message": "Hello World"}

app = FastAPI(
    title="🚀 Hackathon API",
    description="A production-ready FastAPI service deployed on Railway",
    version="1.0.0",
    docs_url="/docs",
    redoc_url=None,
)

Instrumentator().instrument(app).expose(app)

@app.middleware("http")
async def log_requests(request: Request, call_next):
    t0 = time.time()
    response = await call_next(request)
    logger.info("http_request", extra={
        "method":      request.method,
        "path":        request.url.path,
        "status_code": response.status_code,
        "duration_ms": round((time.time() - t0) * 1000, 2),
        "client_ip":   request.client.host,
    })
    return response
  
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/redoc", include_in_schema=False)
async def redoc_html():
    html = """<!DOCTYPE html>
<html>
<head>
    <title>ReDoc</title>
    <meta charset="utf-8"/>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <link href="https://fonts.googleapis.com/css?family=Montserrat:300,400,700|Roboto:300,400,700" rel="stylesheet">
    <style>body { margin: 0; padding: 0; }</style>
</head>
<body>
    <redoc spec-url='/openapi.json'></redoc>
    <script src="https://cdn.jsdelivr.net/npm/redoc/bundles/redoc.standalone.js"></script>
</body>
</html>"""
    return HTMLResponse(
        content=html,
        headers={
            "Content-Security-Policy": (
                "default-src 'self'; "
                "script-src 'self' 'unsafe-eval' https://cdn.jsdelivr.net; "
                "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
                "font-src 'self' https://fonts.gstatic.com; "
                "img-src 'self' data: blob: https:; "
                "worker-src blob:; "
                "connect-src 'self';"
            )
        }
    )

# ─── Models ───────────────────────────────────────────────────────────────────

class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    in_stock: bool = True

class Message(BaseModel):
    text: str
    author: Optional[str] = "anonymous"

# ─── In-memory store (replace with DB in production) ──────────────────────────

items_db: dict[int, dict] = {}
messages_db: list[dict] = []
_item_counter = 0

# ─── Landing page HTML ────────────────────────────────────────────────────────

LANDING_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0"/>
  <title>🚀 Hackathon API</title>
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link href="https://fonts.googleapis.com/css2?family=Space+Mono:wght@400;700&family=Syne:wght@400;700;800&display=swap" rel="stylesheet">
  <style>
    *, *::before, *::after { box-sizing: border-box; margin: 0; padding: 0; }

    :root {
      --bg: #0a0a0f;
      --surface: #13131a;
      --border: #1e1e2e;
      --accent: #7c3aed;
      --accent2: #06b6d4;
      --text: #e2e8f0;
      --muted: #64748b;
      --green: #10b981;
    }

    body {
      background: var(--bg);
      color: var(--text);
      font-family: 'Syne', sans-serif;
      min-height: 100vh;
      overflow-x: hidden;
    }

    /* Animated grid background */
    body::before {
      content: '';
      position: fixed;
      inset: 0;
      background-image:
        linear-gradient(rgba(124,58,237,0.04) 1px, transparent 1px),
        linear-gradient(90deg, rgba(124,58,237,0.04) 1px, transparent 1px);
      background-size: 40px 40px;
      pointer-events: none;
      z-index: 0;
    }

    .glow {
      position: fixed;
      width: 600px; height: 600px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(124,58,237,0.15) 0%, transparent 70%);
      top: -200px; left: -200px;
      pointer-events: none;
      animation: drift 8s ease-in-out infinite alternate;
    }
    .glow2 {
      position: fixed;
      width: 400px; height: 400px;
      border-radius: 50%;
      background: radial-gradient(circle, rgba(6,182,212,0.1) 0%, transparent 70%);
      bottom: -100px; right: -100px;
      pointer-events: none;
      animation: drift 10s ease-in-out infinite alternate-reverse;
    }
    @keyframes drift {
      from { transform: translate(0, 0); }
      to   { transform: translate(60px, 40px); }
    }

    .container {
      position: relative;
      z-index: 1;
      max-width: 900px;
      margin: 0 auto;
      padding: 60px 24px;
    }

    /* Header */
    .badge {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      background: rgba(16,185,129,0.1);
      border: 1px solid rgba(16,185,129,0.3);
      color: var(--green);
      font-family: 'Space Mono', monospace;
      font-size: 12px;
      padding: 6px 14px;
      border-radius: 100px;
      margin-bottom: 32px;
      animation: fadein 0.6s ease both;
    }
    .badge::before {
      content: '';
      width: 8px; height: 8px;
      border-radius: 50%;
      background: var(--green);
      animation: pulse 2s infinite;
    }
    @keyframes pulse {
      0%, 100% { opacity: 1; }
      50% { opacity: 0.3; }
    }

    h1 {
      font-size: clamp(42px, 8vw, 80px);
      font-weight: 800;
      line-height: 1.0;
      letter-spacing: -2px;
      margin-bottom: 20px;
      animation: fadein 0.6s 0.1s ease both;
    }
    h1 span {
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .subtitle {
      color: var(--muted);
      font-size: 18px;
      font-weight: 400;
      max-width: 520px;
      line-height: 1.6;
      margin-bottom: 48px;
      animation: fadein 0.6s 0.2s ease both;
    }

    /* Buttons */
    .actions {
      display: flex;
      gap: 12px;
      flex-wrap: wrap;
      margin-bottom: 64px;
      animation: fadein 0.6s 0.3s ease both;
    }
    .btn {
      display: inline-flex;
      align-items: center;
      gap: 8px;
      padding: 12px 24px;
      border-radius: 8px;
      font-family: 'Space Mono', monospace;
      font-size: 13px;
      font-weight: 700;
      text-decoration: none;
      cursor: pointer;
      border: none;
      transition: all 0.2s;
    }
    .btn-primary {
      background: var(--accent);
      color: white;
    }
    .btn-primary:hover { background: #6d28d9; transform: translateY(-2px); box-shadow: 0 8px 24px rgba(124,58,237,0.4); }
    .btn-outline {
      background: transparent;
      color: var(--text);
      border: 1px solid var(--border);
    }
    .btn-outline:hover { border-color: var(--accent); color: var(--accent); transform: translateY(-2px); }

    /* Endpoint cards */
    .section-label {
      font-family: 'Space Mono', monospace;
      font-size: 11px;
      letter-spacing: 3px;
      text-transform: uppercase;
      color: var(--muted);
      margin-bottom: 20px;
      animation: fadein 0.6s 0.4s ease both;
    }
    .endpoints {
      display: grid;
      gap: 12px;
      animation: fadein 0.6s 0.5s ease both;
    }
    .endpoint {
      display: flex;
      align-items: center;
      gap: 16px;
      background: var(--surface);
      border: 1px solid var(--border);
      border-radius: 10px;
      padding: 16px 20px;
      transition: border-color 0.2s, transform 0.2s;
      text-decoration: none;
      color: inherit;
    }
    .endpoint:hover { border-color: var(--accent); transform: translateX(4px); }
    .method {
      font-family: 'Space Mono', monospace;
      font-size: 11px;
      font-weight: 700;
      padding: 4px 10px;
      border-radius: 5px;
      min-width: 52px;
      text-align: center;
    }
    .get  { background: rgba(16,185,129,0.15);  color: #10b981; }
    .post { background: rgba(124,58,237,0.15); color: #a78bfa; }
    .del  { background: rgba(239,68,68,0.15);  color: #f87171; }
    .path {
      font-family: 'Space Mono', monospace;
      font-size: 13px;
      color: var(--text);
    }
    .desc {
      margin-left: auto;
      font-size: 13px;
      color: var(--muted);
    }

    /* Stats row */
    .stats {
      display: flex;
      gap: 32px;
      flex-wrap: wrap;
      margin-top: 64px;
      padding-top: 32px;
      border-top: 1px solid var(--border);
      animation: fadein 0.6s 0.6s ease both;
    }
    .stat-value {
      font-size: 28px;
      font-weight: 800;
      background: linear-gradient(135deg, var(--accent), var(--accent2));
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }
    .stat-label {
      font-size: 12px;
      color: var(--muted);
      font-family: 'Space Mono', monospace;
    }

    @keyframes fadein {
      from { opacity: 0; transform: translateY(16px); }
      to   { opacity: 1; transform: translateY(0); }
    }
  </style>
</head>
<body>
  <div class="glow"></div>
  <div class="glow2"></div>

  <div class="container">
    <div class="badge">API LIVE · Railway Production</div>

    <h1>Hackathon<br><span>API</span></h1>
    <p class="subtitle">
      A production-ready FastAPI service. Containerized with Docker,
      secured by Trivy, and auto-deployed via GitHub Actions CI/CD.
    </p>

    <div class="actions">
      <a class="btn btn-primary" href="/docs">📄 Swagger UI</a>
      <a class="btn btn-outline" href="/redoc">📘 ReDoc</a>
      <a class="btn btn-outline" href="/health">💚 Health Check</a>
    </div>

    <p class="section-label">Available endpoints</p>
    <div class="endpoints">
      <a class="endpoint" href="/health">
        <span class="method get">GET</span>
        <span class="path">/health</span>
        <span class="desc">Service health status</span>
      </a>
      <a class="endpoint" href="/items">
        <span class="method get">GET</span>
        <span class="path">/items</span>
        <span class="desc">List all items</span>
      </a>
      <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/items</span>
        <span class="desc">Create a new item</span>
      </div>
      <a class="endpoint" href="/messages">
        <span class="method get">GET</span>
        <span class="path">/messages</span>
        <span class="desc">List all messages</span>
      </a>
      <div class="endpoint">
        <span class="method post">POST</span>
        <span class="path">/messages</span>
        <span class="desc">Post a message</span>
      </div>
    </div>

    <div class="stats">
      <div>
        <div class="stat-value">FastAPI</div>
        <div class="stat-label">FRAMEWORK</div>
      </div>
      <div>
        <div class="stat-value">Railway</div>
        <div class="stat-label">PLATFORM</div>
      </div>
      <div>
        <div class="stat-value">Docker</div>
        <div class="stat-label">CONTAINER</div>
      </div>
      <div>
        <div class="stat-value">CI/CD</div>
        <div class="stat-label">GITHUB ACTIONS</div>
      </div>
    </div>
  </div>
</body>
</html>
"""

# ─── Routes ───────────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse, include_in_schema=False)
async def landing():
    """Beautiful landing page."""
    return HTMLResponse(content=LANDING_HTML)


@app.get("/health", tags=["System"])
async def health():
    """Health check endpoint for Railway / uptime monitors."""
    return {
        "status": "ok",
        "timestamp": datetime.now(UTC).isoformat() + "Z",
        "version": "1.0.0",
    }


# ── Items CRUD ─────────────────────────────────────────────────────────────────

@app.get("/items", tags=["Items"])
async def list_items():
    """Return all items."""
    return {"items": list(items_db.values()), "count": len(items_db)}


@app.get("/items/{item_id}", tags=["Items"])
async def get_item(item_id: int):
    """Get a single item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    return items_db[item_id]


@app.post("/items", status_code=201, tags=["Items"])
async def create_item(item: Item):
    """Create a new item."""
    global _item_counter
    _item_counter += 1
    record = {"id": _item_counter, **item.model_dump(), "created_at": datetime.now(UTC).isoformat()}
    items_db[_item_counter] = record
    return record


@app.delete("/items/{item_id}", tags=["Items"])
async def delete_item(item_id: int):
    """Delete an item by ID."""
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail=f"Item {item_id} not found")
    del items_db[item_id]
    return {"deleted": item_id}


# ── Messages ───────────────────────────────────────────────────────────────────

@app.get("/messages", tags=["Messages"])
async def list_messages():
    """Return all messages."""
    return {"messages": messages_db, "count": len(messages_db)}


@app.post("/messages", status_code=201, tags=["Messages"])
async def post_message(msg: Message):
    """Post a new message."""
    record = {
        "id": len(messages_db) + 1,
        **msg.model_dump(),
        "created_at": datetime.now(UTC).isoformat(),
    }
    messages_db.append(record)
    return record


# ─── Entry point ──────────────────────────────────────────────────────────────

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=False)
