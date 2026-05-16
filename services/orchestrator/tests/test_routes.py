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


@respx.mock
async def test_models_proxies_backend_list(app_client):
    """GET /v1/models proxies the backend's /v1/models response."""
    respx.get("http://localhost:8081/v1/models").mock(
        return_value=Response(
            200,
            json={
                "object": "list",
                "data": [{"id": "qwen3-4b", "object": "model"}],
            },
        )
    )
    resp = await app_client.get("/v1/models")
    assert resp.status_code == 200
    assert resp.json()["data"][0]["id"] == "qwen3-4b"


@respx.mock
async def test_models_returns_empty_list_if_backend_down(app_client):
    """If the backend is unreachable we return an empty list, not 500."""
    import httpx

    respx.get("http://localhost:8081/v1/models").mock(
        side_effect=httpx.ConnectError("down")
    )
    resp = await app_client.get("/v1/models")
    assert resp.status_code == 200
    assert resp.json() == {"object": "list", "data": []}
