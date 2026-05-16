"""LocalLlamaProvider — forwards chat requests to a local llama-server.

The llama-server speaks OpenAI-compatible HTTP. This provider POSTs the
messages and translates either the JSON response (non-streaming) or the
SSE stream (streaming, added in Task 7) into typed Events.
"""
from collections.abc import AsyncIterator
from typing import Any

import httpx

from orchestrator.events import Event, FinalDoneEvent, TokenEvent
from orchestrator.providers.base import Provider


class LocalLlamaProvider(Provider):
    def __init__(self, *, base_url: str, timeout: float = 300.0) -> None:
        self._base_url = base_url.rstrip("/")
        self._timeout = timeout

    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        stream: bool = False,
    ) -> AsyncIterator[Event]:
        if stream:
            raise NotImplementedError("streaming added in Task 7")

        async for event in self._chat_non_streaming(messages):
            yield event

    async def _chat_non_streaming(
        self, messages: list[dict[str, Any]]
    ) -> AsyncIterator[Event]:
        async with httpx.AsyncClient(timeout=self._timeout) as client:
            resp = await client.post(
                f"{self._base_url}/v1/chat/completions",
                json={"messages": messages, "stream": False},
            )
            resp.raise_for_status()
            data = resp.json()

        choices = data.get("choices") or []
        if not choices:
            yield FinalDoneEvent()
            return

        content = choices[0].get("message", {}).get("content") or ""
        yield TokenEvent(delta=content)
        yield FinalDoneEvent()
