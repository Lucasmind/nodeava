"""Tests for LocalLlamaProvider."""
import respx
from httpx import Response

from orchestrator.events import TokenEvent, FinalDoneEvent
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
