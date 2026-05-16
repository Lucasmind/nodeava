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


async def fake_acompletion_streaming(*, model, messages, stream, api_key, **kwargs):
    """Mimics litellm.acompletion(stream=True) — returns an async iterator
    of chunk-like objects shaped after LiteLLM's actual streaming output."""
    assert stream is True

    async def gen():
        # LiteLLM normalises chunks to look like OpenAI:
        # chunk.choices[0].delta.content (str) carries visible text
        chunks = [
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content="Hi", role="assistant"), finish_reason=None)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=" there", role=None), finish_reason=None)]),
            SimpleNamespace(choices=[SimpleNamespace(delta=SimpleNamespace(content=None, role=None), finish_reason="stop")]),
        ]
        for c in chunks:
            yield c

    return gen()


async def test_streaming_emits_token_per_chunk(monkeypatch):
    """Streaming: yields one TokenEvent per non-empty content delta, then FinalDoneEvent."""
    import litellm

    monkeypatch.setattr(litellm, "acompletion", fake_acompletion_streaming)

    provider = LiteLLMProvider(
        provider_name="anthropic",
        model="claude-haiku-4-5-20251001",
        api_key="sk-ant-test",
        timeout=30.0,
    )
    events = [
        e async for e in provider.chat(
            [{"role": "user", "content": "hello"}], stream=True
        )
    ]
    deltas = [e.delta for e in events if isinstance(e, TokenEvent)]
    assert deltas == ["Hi", " there"]
    assert isinstance(events[-1], FinalDoneEvent)
