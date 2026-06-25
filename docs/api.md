# API Reference

Base URL (production): `https://devsecops-pipeline-demo-production.up.railway.app/`  
Base URL (local): `http://localhost:8000`

Interactive docs: `/docs` (Swagger UI) · `/redoc` (ReDoc)

---

## General

### GET `/`
Landing page (HTML).

```bash
curl  https://devsecops-pipeline-demo-production.up.railway.app/
```

---

### GET `/health`
Returns service status and current timestamp.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/health
```

Response:
```json
{
  "status": "ok",
  "timestamp": "2025-06-25T12:00:00.000Z"
}
```

---

### GET `/version`
Returns app version and Python runtime information.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/version
```

Response:
```json
{
  "version": "1.1.0",
  "python": "3.12.3"
}
```

---

### GET `/metrics`
Returns counts of stored items and messages.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/metrics
```

Response:
```json
{
  "items_count": 3,
  "messages_count": 5
}
```

---

### GET `/ping`
Simple liveness probe. Returns `pong`.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/ping
```

Response:
```json
{
  "ping": "pong"
}
```

---

## Items

### GET `/items`
List all items.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/items
```

Response:
```json
[
  {
    "id": 1,
    "name": "Widget",
    "description": "A useful widget",
    "price": 9.99,
    "in_stock": true
  }
]
```

---

### POST `/items`
Create a new item.

```bash
curl -X POST https://devsecops-pipeline-demo-production.up.railway.app/items/ \
  -H "Content-Type: application/json" \
  -d '{"name": "Widget", "description": "A useful widget", "price": 9.99, "in_stock": true}'
```

Request body:
```json
{
  "name": "Widget",           // required
  "description": "Optional",  // optional
  "price": 9.99,              // required, float
  "in_stock": true            // required, boolean
}
```

Response `201 Created`:
```json
{
  "id": 1,
  "name": "Widget",
  "description": "Optional",
  "price": 9.99,
  "in_stock": true
}
```

---

### GET `/items/{id}`
Get a single item by ID.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/items/1
```

Response `200 OK` or `404 Not Found`:
```json
{ "detail": "Item not found" }
```

---

### DELETE `/items/{id}`
Delete an item by ID.

```bash
curl -X DELETE https://devsecops-pipeline-demo-production.up.railway.app/items/1
```

Response `200 OK` or `404 Not Found`.

---

## Messages

### GET `/messages`
List all messages.

```bash
curl https://devsecops-pipeline-demo-production.up.railway.app/messages
```

Response:
```json
[
  {
    "id": 1,
    "text": "Hello world",
    "author": "alice"
  }
]
```

---

### POST `/messages`
Post a new message.

```bash
curl -X POST https://devsecops-pipeline-demo-production.up.railway.app/messages \
  -H "Content-Type: application/json" \
  -d '{"text": "Hello world", "author": "alice"}'
```

Request body:
```json
{
  "text": "Hello world",  // required
  "author": "alice"       // required
}
```

Response `201 Created`:
```json
{
  "id": 1,
  "text": "Hello world",
  "author": "alice"
}
```

---

## Error Responses

| Status | Meaning                        |
|--------|--------------------------------|
| 404    | Resource not found             |
| 422    | Validation error (bad payload) |
| 500    | Internal server error          |

Example validation error:
```json
{
  "detail": [
    {
      "loc": ["body", "price"],
      "msg": "field required",
      "type": "value_error.missing"
    }
  ]
}
```