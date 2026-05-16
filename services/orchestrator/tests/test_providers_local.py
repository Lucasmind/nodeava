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
