"""LocalLlamaProvider — forwards chat requests to a local llama-server.

The llama-server speaks OpenAI-compatible HTTP. This provider POSTs the
messages and translates either the JSON response (non-streaming) or the
SSE stream (streaming) into typed Events.

Error handling: HTTP errors and connection errors do NOT raise out of
the generator. Instead, the generator yields an ErrorEvent followed by
FinalDoneEvent. This contract simplifies the route layer — it always
gets a clean event stream regardless of backend health.
"""
import json
import logging
from collections.abc import AsyncIterator
from typing import Any

import httpx

from orchestrator.events import Event, ErrorEvent, FinalDoneEvent, TokenEvent
from orchestrator.providers.base import Provider

log = logging.getLogger("orchestrator.providers.local")


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
            async for event in self._chat_streaming(messages):
                yield event
        else:
            async for event in self._chat_non_streaming(messages):
                yield event

    async def _chat_non_streaming(
        self, messages: list[dict[str, Any]]
    ) -> AsyncIterator[Event]:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                resp = await client.post(
                    f"{self._base_url}/v1/chat/completions",
                    json={"messages": messages, "stream": False},
                )
                if resp.status_code >= 400:
                    log.warning("backend HTTP %d: %s", resp.status_code, resp.text[:200])
                    yield ErrorEvent(
                        message=f"backend returned HTTP {resp.status_code}"
                    )
                    yield FinalDoneEvent()
                    return
                data = resp.json()
        except httpx.HTTPError as e:
            log.warning("backend connection error: %s", e)
            yield ErrorEvent(message=f"backend connection error: {e}")
            yield FinalDoneEvent()
            return

        choices = data.get("choices") or []
        if not choices:
            yield FinalDoneEvent()
            return

        content = choices[0].get("message", {}).get("content") or ""
        yield TokenEvent(delta=content)
        yield FinalDoneEvent()

    async def _chat_streaming(
        self, messages: list[dict[str, Any]]
    ) -> AsyncIterator[Event]:
        try:
            async with httpx.AsyncClient(timeout=self._timeout) as client:
                async with client.stream(
                    "POST",
                    f"{self._base_url}/v1/chat/completions",
                    json={"messages": messages, "stream": True},
                ) as resp:
                    if resp.status_code >= 400:
                        body = (await resp.aread()).decode(errors="replace")[:200]
                        log.warning("backend HTTP %d: %s", resp.status_code, body)
                        yield ErrorEvent(
                            message=f"backend returned HTTP {resp.status_code}"
                        )
                        yield FinalDoneEvent()
                        return
                    async for line in resp.aiter_lines():
                        if not line or not line.startswith("data: "):
                            continue
                        payload = line.removeprefix("data: ").strip()
                        if payload == "[DONE]":
                            break
                        try:
                            chunk = json.loads(payload)
                        except json.JSONDecodeError:
                            continue
                        choices = chunk.get("choices") or []
                        if not choices:
                            continue
                        delta = choices[0].get("delta") or {}
                        content = delta.get("content")
                        if content:
                            yield TokenEvent(delta=content)
        except httpx.HTTPError as e:
            log.warning("backend connection error: %s", e)
            yield ErrorEvent(message=f"backend connection error: {e}")
            yield FinalDoneEvent()
            return

        yield FinalDoneEvent()
