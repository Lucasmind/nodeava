"""Tests for the Provider abstract base class."""
import pytest

from orchestrator.events import TokenEvent, FinalDoneEvent
from orchestrator.providers.base import Provider


class StubProvider(Provider):
    """Yields a fixed event sequence — used to test the ABC contract."""

    async def chat(self, messages, *, stream=False):
        yield TokenEvent(delta="hello")
        yield TokenEvent(delta=" world")
        yield FinalDoneEvent()


async def test_provider_is_async_iterable():
    """A Provider's `chat` method returns an async iterator of Events."""
    provider = StubProvider()
    events = [e async for e in provider.chat([{"role": "user", "content": "hi"}])]
    assert [e.type for e in events] == ["token", "token", "final_done"]


async def test_provider_subclass_must_implement_chat():
    """Instantiating a Provider that didn't override chat raises TypeError."""

    class BadProvider(Provider):
        pass

    with pytest.raises(TypeError):
        BadProvider()  # type: ignore[abstract]
