import pytest
from fastapi.testclient import TestClient

from app.main import app, items_db, messages_db, _item_counter


@pytest.fixture(autouse=True)
def clear_state():
    """Reset in-memory stores before every test."""
    items_db.clear()
    messages_db.clear()
    import app.main as m
    m._item_counter = 0
    yield


@pytest.fixture
def client():
    return TestClient(app)


# ── Landing & health ──────────────────────────────────────────────────────────

class TestLanding:
    def test_returns_html(self, client):
        r = client.get("/")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert "Hackathon" in r.text

    def test_health(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        body = r.json()
        assert body["status"] == "ok"
        assert "timestamp" in body
        assert "version" in body


# ── Items ─────────────────────────────────────────────────────────────────────

class TestItems:
    PAYLOAD = {"name": "Widget", "description": "A nice widget", "price": 9.99, "in_stock": True}

    def test_list_empty(self, client):
        r = client.get("/items")
        assert r.status_code == 200
        assert r.json() == {"items": [], "count": 0}

    def test_create(self, client):
        r = client.post("/items", json=self.PAYLOAD)
        assert r.status_code == 201
        body = r.json()
        assert body["id"] == 1
        assert body["name"] == "Widget"
        assert body["price"] == pytest.approx(9.99)
        assert "created_at" in body

    def test_create_minimal(self, client):
        r = client.post("/items", json={"name": "Bare", "price": 0.0})
        assert r.status_code == 201
        body = r.json()
        assert body["in_stock"] is True
        assert body["description"] is None

    def test_list_after_create(self, client):
        client.post("/items", json=self.PAYLOAD)
        client.post("/items", json={**self.PAYLOAD, "name": "Gadget"})
        r = client.get("/items")
        assert r.json()["count"] == 2

    def test_get_by_id(self, client):
        client.post("/items", json=self.PAYLOAD)
        r = client.get("/items/1")
        assert r.status_code == 200
        assert r.json()["name"] == "Widget"

    def test_get_not_found(self, client):
        r = client.get("/items/999")
        assert r.status_code == 404
        assert "not found" in r.json()["detail"].lower()

    def test_delete(self, client):
        client.post("/items", json=self.PAYLOAD)
        r = client.delete("/items/1")
        assert r.status_code == 200
        assert r.json() == {"deleted": 1}
        assert client.get("/items/1").status_code == 404

    def test_delete_not_found(self, client):
        r = client.delete("/items/42")
        assert r.status_code == 404

    def test_create_invalid_missing_price(self, client):
        r = client.post("/items", json={"name": "NoPriceItem"})
        assert r.status_code == 422


# ── Messages ──────────────────────────────────────────────────────────────────

class TestMessages:
    def test_list_empty(self, client):
        r = client.get("/messages")
        assert r.status_code == 200
        assert r.json() == {"messages": [], "count": 0}

    def test_post_message(self, client):
        r = client.post("/messages", json={"text": "Hello world", "author": "alice"})
        assert r.status_code == 201
        body = r.json()
        assert body["text"] == "Hello world"
        assert body["author"] == "alice"
        assert body["id"] == 1
        assert "created_at" in body

    def test_post_anonymous(self, client):
        r = client.post("/messages", json={"text": "Hi"})
        assert r.status_code == 201
        assert r.json()["author"] == "anonymous"

    def test_list_after_posts(self, client):
        client.post("/messages", json={"text": "First"})
        client.post("/messages", json={"text": "Second"})
        r = client.get("/messages")
        data = r.json()
        assert data["count"] == 2
        assert data["messages"][0]["text"] == "First"

    def test_post_invalid_missing_text(self, client):
        r = client.post("/messages", json={"author": "bob"})
        assert r.status_code == 422