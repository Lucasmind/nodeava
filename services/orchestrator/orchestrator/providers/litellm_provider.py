"""LiteLLMProvider — cloud (or any LiteLLM-supported) chat backend.

LiteLLM normalizes ~30 providers' APIs to an OpenAI-compatible shape. We
delegate transport + auth + tool-format translation to it, and only
worry about adapting its response shape into our typed Event stream.

In Plan #2 only non-tool chat is implemented. Tool support and reasoning
streaming arrive in Plans #3-#4.
"""
import logging
from collections.abc import AsyncIterator
from typing import Any

from orchestrator.events import Event, FinalDoneEvent, TokenEvent
from orchestrator.providers.base import Provider

log = logging.getLogger("orchestrator.providers.litellm")


class LiteLLMProvider(Provider):
    """Cloud chat provider routed through litellm.acompletion.

    Parameters
    ----------
    provider_name
        Identifier like "anthropic", "openai", "groq" — only used to construct
        the LiteLLM model string when callers omit a fully-qualified model.
    model
        Either a fully-qualified LiteLLM model string ("anthropic/claude-haiku-4-5-20251001")
        OR a bare model ID; provider_name is prepended when there's no slash.
    api_key
        The user's key. Passed per-request to litellm — never stored beyond
        this instance.
    timeout
        Seconds before LiteLLM gives up on the upstream call.
    """

    def __init__(
        self,
        *,
        provider_name: str,
        model: str,
        api_key: str,
        timeout: float = 300.0,
    ) -> None:
        self._provider_name = provider_name
        self._model = (
            model if "/" in model else f"{provider_name}/{model}"
        ) if model else provider_name
        self._api_key = api_key
        self._timeout = timeout

    async def chat(
        self,
        messages: list[dict[str, Any]],
        *,
        stream: bool = False,
    ) -> AsyncIterator[Event]:
        if stream:
            raise NotImplementedError("streaming added in Task 6")

        async for event in self._chat_non_streaming(messages):
            yield event

    async def _chat_non_streaming(
        self, messages: list[dict[str, Any]]
    ) -> AsyncIterator[Event]:
        import litellm

        resp = await litellm.acompletion(
            model=self._model,
            messages=messages,
            stream=False,
            api_key=self._api_key,
            timeout=self._timeout,
        )
        choices = resp.choices or []
        if not choices:
            yield FinalDoneEvent()
            return
        content = choices[0].message.content or ""
        if content:
            yield TokenEvent(delta=content)
        yield FinalDoneEvent()
