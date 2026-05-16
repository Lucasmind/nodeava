"""Tests for the typed Event models."""
from orchestrator.events import Event, TokenEvent, FinalDoneEvent, ErrorEvent


def test_token_event_serialization():
    e = TokenEvent(delta="Hello")
    d = e.model_dump()
    assert d == {"type": "token", "delta": "Hello"}


def test_final_done_event_serialization():
    e = FinalDoneEvent()
    d = e.model_dump()
    assert d == {"type": "final_done"}


def test_error_event_serialization():
    e = ErrorEvent(message="backend unreachable")
    d = e.model_dump()
    assert d == {"type": "error", "message": "backend unreachable"}


def test_event_is_abstract_base_via_discriminator():
    """All concrete events should be assignable to the Event union type."""
    events: list[Event] = [
        TokenEvent(delta="x"),
        FinalDoneEvent(),
        ErrorEvent(message="boom"),
    ]
    types = [e.type for e in events]
    assert types == ["token", "final_done", "error"]
