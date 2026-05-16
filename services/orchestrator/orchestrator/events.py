"""Typed event models emitted by Providers and consumed by the SSE encoder.

Plans extend this union as new event types arrive:
  Plan #1: TokenEvent, FinalDoneEvent, ErrorEvent
  Plan #2: ThinkingTokenEvent (this file)
  Plan #4 will add: ToolCallStartEvent, ToolCallEndEvent, StageTimingEvent
"""
from typing import Literal, Union

from pydantic import BaseModel


class TokenEvent(BaseModel):
    type: Literal["token"] = "token"
    delta: str


class ThinkingTokenEvent(BaseModel):
    """Reasoning content emitted by providers that expose it (e.g. Anthropic
    extended thinking). The frontend's brain-pane subscribes to these on
    a named SSE channel — they are NOT mixed into the user-visible content
    stream.
    """
    type: Literal["thinking_token"] = "thinking_token"
    delta: str


class FinalDoneEvent(BaseModel):
    type: Literal["final_done"] = "final_done"


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str


Event = Union[TokenEvent, ThinkingTokenEvent, FinalDoneEvent, ErrorEvent]
