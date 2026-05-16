"""Typed event models emitted by Providers and consumed by the SSE encoder.

This module defines the events used in Plan #1 (foundation). Plans #2-#4 will
extend with ThinkingTokenEvent, ToolCallStartEvent, ToolCallEndEvent,
StageTimingEvent, etc. The discriminator is `type` so JSON consumers can
route on a single field.
"""
from typing import Literal, Union

from pydantic import BaseModel


class TokenEvent(BaseModel):
    type: Literal["token"] = "token"
    delta: str


class FinalDoneEvent(BaseModel):
    type: Literal["final_done"] = "final_done"


class ErrorEvent(BaseModel):
    type: Literal["error"] = "error"
    message: str


Event = Union[TokenEvent, FinalDoneEvent, ErrorEvent]
