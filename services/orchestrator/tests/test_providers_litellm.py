"""Tests for LiteLLMProvider."""
from types import SimpleNamespace

import pytest

from orchestrator.events import FinalDoneEvent, TokenEvent
from orchestrator.providers.litellm_provider import LiteLLMProvider


async def fake_acompletion_non_streaming(*, model, messages, stream, api_key, **kwargs):
    """Mimics litellm.acompletion(stream=False) — returns a coroutine that
    resolves to a non-streaming response object."""
    assert stream is False
    return SimpleNamespace(
        choices=[
            SimpleNamespace(
                message=SimpleNamespace(content="Hi there.", role="assistant"),
                finish_reason="stop",
            )
        ]
    )


async def test_non_streaming_emits_token_then_done(monkeypatch):
    """Non-streaming: LiteLLM returns one response, provider yields one
    TokenEvent with the full content + FinalDoneEvent."""
    import litellm

    monkeypatch.setattr(litellm, "acompletion", fake_acompletion_non_streaming)

    provider = LiteLLMProvider(
        provider_name="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key="sk-ant-test",
        timeout=30.0,
    )
    events = [
        e async for e in provider.chat(
            [{"role": "user", "content": "hello"}], stream=False
        )
    ]
    assert len(events) == 2
    assert isinstance(events[0], TokenEvent)
    assert events[0].delta == "Hi there."
    assert isinstance(events[1], FinalDoneEvent)
