"""Tests for HTTP routes."""
import respx
from httpx import Response


async def test_app_imports_and_serves_404_for_unknown_route(app_client):
    """Smoke test: the app boots and serves an unknown path with 404."""
    resp = await app_client.get("/does-not-exist")
    assert resp.status_code == 404


@respx.mock
async def test_health_ok_when_backend_healthy(app_client):
    respx.get("http://localhost:8081/health").mock(return_value=Response(200))
    resp = await app_client.get("/health")
    assert resp.status_code == 200
    assert resp.json() == {"status": "ok", "backend": "http://localhost:8081"}


@respx.mock
async def test_health_503_when_backend_unhealthy(app_client):
    respx.get("http://localhost:8081/health").mock(return_value=Response(500))
    resp = await app_client.get("/health")
    assert resp.status_code == 503
    body = resp.json()
    assert body["status"] == "unhealthy"
    assert "backend" in body
