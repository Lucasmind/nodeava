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


@respx.mock
async def test_chat_non_streaming_returns_openai_shape(app_client):
    """Non-streaming chat returns an OpenAI-shaped JSON response with the
    full text in choices[0].message.content."""
    respx.post("http://localhost:8081/v1/chat/completions").mock(
        return_value=Response(
            200,
            json={
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "Greetings."},
                        "finish_reason": "stop",
                    }
                ]
            },
        )
    )

    resp = await app_client.post(
        "/v1/chat/completions",
        json={"messages": [{"role": "user", "content": "hi"}]},
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["choices"][0]["message"]["content"] == "Greetings."
    assert body["choices"][0]["finish_reason"] == "stop"
    assert body["object"] == "chat.completion"


import json


@respx.mock
async def test_chat_streaming_emits_openai_chunks_then_done(app_client):
    """Streaming chat: each TokenEvent → an OpenAI-shaped `data: {...}` chunk;
    FinalDoneEvent → `data: [DONE]`."""
    sse_body = (
        b'data: {"choices":[{"delta":{"role":"assistant"},"index":0,"finish_reason":null}]}\n\n'
        b'data: {"choices":[{"delta":{"content":"Hi"},"index":0,"finish_reason":null}]}\n\n'
        b'data: {"choices":[{"delta":{"content":"!"},"index":0,"finish_reason":null}]}\n\n'
        b'data: {"choices":[{"delta":{},"index":0,"finish_reason":"stop"}]}\n\n'
        b'data: [DONE]\n\n'
    )
    respx.post("http://localhost:8081/v1/chat/completions").mock(
        return_value=Response(
            200,
            content=sse_body,
            headers={"content-type": "text/event-stream"},
        )
    )

    async with app_client.stream(
        "POST",
        "/v1/chat/completions",
        json={
            "messages": [{"role": "user", "content": "hi"}],
            "stream": True,
        },
    ) as resp:
        assert resp.status_code == 200
        assert "text/event-stream" in resp.headers["content-type"]
        body = (await resp.aread()).decode()

    # Parse the SSE body: collect content from data: chunks before [DONE].
    contents = []
    for line in body.split("\n"):
        if not line.startswith("data: "):
            continue
        payload = line.removeprefix("data: ").strip()
        if payload == "[DONE]":
            continue
        chunk = json.loads(payload)
        delta = chunk.get("choices", [{}])[0].get("delta", {})
        if "content" in delta:
            contents.append(delta["content"])

    assert contents == ["Hi", "!"]
    assert body.rstrip().endswith("data: [DONE]")


def test_run_uses_settings_bind_host_and_port(monkeypatch):
    """`run()` must pass settings.bind_host / settings.bind_port to uvicorn —
    so the localhost-only default isn't silently bypassed."""
    from orchestrator import main as orch_main

    captured = {}

    def fake_run(app_target, *, host, port, log_level):  # noqa: ARG001
        captured["host"] = host
        captured["port"] = port
        captured["app_target"] = app_target

    monkeypatch.setattr("uvicorn.run", fake_run)
    orch_main.app.state.settings.bind_host = "203.0.113.4"
    orch_main.app.state.settings.bind_port = 9999
    try:
        orch_main.run()
    finally:
        orch_main.app.state.settings.bind_host = "127.0.0.1"
        orch_main.app.state.settings.bind_port = 8082

    assert captured["host"] == "203.0.113.4"
    assert captured["port"] == 9999
    assert captured["app_target"] == "orchestrator.main:app"
