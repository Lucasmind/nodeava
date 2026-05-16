"""Tests for LocalLlamaProvider."""
import respx
from httpx import Response

from orchestrator.events import TokenEvent, FinalDoneEvent, ErrorEvent
from orchestrator.providers.local import LocalLlamaProvider


@respx.mock
async def test_non_streaming_emits_single_token_and_done(llama_url):
    """Non-streaming: provider POSTs once, receives full JSON, yields one
    TokenEvent with the full content, then FinalDoneEvent."""
    respx.post(f"{llama_url}/v1/chat/completions").mock(
        return_value=Response(
            200,
            json={
                "choices": [
                    {
                        "index": 0,
                        "message": {"role": "assistant", "content": "Hello, world."},
                        "finish_reason": "stop",
                    }
                ]
            },
        )
    )

    provider = LocalLlamaProvider(base_url=llama_url, timeout=30.0)
    events = [
        e
        async for e in provider.chat(
            [{"role": "user", "content": "hi"}], stream=False
        )
    ]

    assert len(events) == 2
    assert isinstance(events[0], TokenEvent)
    assert events[0].delta == "Hello, world."
    assert isinstance(events[1], FinalDoneEvent)


@respx.mock
async def test_streaming_emits_one_token_per_chunk(llama_url):
    """Streaming: provider opens an SSE stream and yields one TokenEvent per
    content chunk, terminating with FinalDoneEvent when the stream closes."""
    sse_body = (
        b'data: {"choices":[{"delta":{"role":"assistant"},"index":0,"finish_reason":null}]}\n\n'
        b'data: {"choices":[{"delta":{"content":"Hi"},"index":0,"finish_reason":null}]}\n\n'
        b'data: {"choices":[{"delta":{"content":" there"},"index":0,"finish_reason":null}]}\n\n'
        b'data: {"choices":[{"delta":{},"index":0,"finish_reason":"stop"}]}\n\n'
        b'data: [DONE]\n\n'
    )
    respx.post(f"{llama_url}/v1/chat/completions").mock(
        return_value=Response(
            200,
            content=sse_body,
            headers={"content-type": "text/event-stream"},
        )
    )

    provider = LocalLlamaProvider(base_url=llama_url, timeout=30.0)
    events = [
        e
        async for e in provider.chat(
            [{"role": "user", "content": "hello"}], stream=True
        )
    ]

    token_deltas = [e.delta for e in events if isinstance(e, TokenEvent)]
    assert token_deltas == ["Hi", " there"]
    assert isinstance(events[-1], FinalDoneEvent)


@respx.mock
async def test_backend_http_error_emits_error_event(llama_url):
    """If the llama-server returns a non-2xx, emit a single ErrorEvent
    followed by FinalDoneEvent — never raise out of the generator."""
    respx.post(f"{llama_url}/v1/chat/completions").mock(
        return_value=Response(503, text="model still loading")
    )

    provider = LocalLlamaProvider(base_url=llama_url, timeout=30.0)
    events = [
        e
        async for e in provider.chat(
            [{"role": "user", "content": "hi"}], stream=False
        )
    ]

    error_events = [e for e in events if isinstance(e, ErrorEvent)]
    done_events = [e for e in events if isinstance(e, FinalDoneEvent)]
    assert len(error_events) == 1
    assert "503" in error_events[0].message
    assert len(done_events) == 1


@respx.mock
async def test_backend_unreachable_emits_error_event(llama_url):
    """Connection errors also produce an ErrorEvent, not an exception."""
    import httpx

    respx.post(f"{llama_url}/v1/chat/completions").mock(
        side_effect=httpx.ConnectError("connection refused")
    )

    provider = LocalLlamaProvider(base_url=llama_url, timeout=30.0)
    events = [
        e
        async for e in provider.chat(
            [{"role": "user", "content": "hi"}], stream=False
        )
    ]

    error_events = [e for e in events if isinstance(e, ErrorEvent)]
    assert len(error_events) == 1
    assert "connection" in error_events[0].message.lower()
