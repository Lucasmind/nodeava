"""Tests for LocalLlamaProvider."""
from unittest.mock import AsyncMock, patch
from httpx import Response

from orchestrator.events import TokenEvent, FinalDoneEvent
from orchestrator.providers.local import LocalLlamaProvider


async def test_non_streaming_emits_single_token_and_done(llama_url):
    """Non-streaming: provider POSTs once, receives full JSON, yields one
    TokenEvent with the full content, then FinalDoneEvent."""
    import json
    import httpx

    mock_response = Response(
        200,
        content=json.dumps({
            "choices": [
                {
                    "index": 0,
                    "message": {"role": "assistant", "content": "Hello, world."},
                    "finish_reason": "stop",
                }
            ]
        }).encode(),
    )
    # Attach a request object so raise_for_status works
    mock_response._request = httpx.Request("POST", f"{llama_url}/v1/chat/completions")

    with patch("httpx.AsyncClient.post", new_callable=AsyncMock) as mock_post:
        mock_post.return_value = mock_response

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
