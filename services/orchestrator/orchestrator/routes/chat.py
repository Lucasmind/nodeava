"""Chat completions route — both non-streaming and streaming.

The route layer is thin: parses the OpenAI request body, picks a Provider
via `pick_provider(request, body)`, and translates the Provider's typed
Event stream into either an OpenAI-shaped JSON response (non-streaming)
or a dual-channel SSE stream (streaming).

Streaming routing rules:
  - TokenEvent  → emitted as an OpenAI streaming chunk on the default
    SSE stream (consumed by openai SDK / fetch clients).
  - ThinkingTokenEvent → emitted via `encode_sse` on the
    `event: thinking_token` named channel (consumed by the upcoming
    brain-pane visualizer).
  - ErrorEvent → emitted via `encode_sse` on `event: error`.
  - FinalDoneEvent → ends the streaming loop; closing chunks +
    `data: [DONE]` are emitted after.
"""
import time
import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from orchestrator.events import (
    ErrorEvent,
    FinalDoneEvent,
    ThinkingTokenEvent,
    TokenEvent,
)
from orchestrator.providers import pick_provider
from orchestrator.sse import encode_openai_chunk, encode_openai_done, encode_sse

router = APIRouter()


@router.post("/v1/chat/completions")
@router.post("/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages") or []
    stream = bool(body.get("stream", False))

    # pick_provider reads body["provider"] for routing — must call it first.
    provider = pick_provider(request, body)

    # Strip provider-routing fields AFTER routing so they are never echoed
    # into the upstream model API.
    # body["model"] is intentionally LEFT in place — it's an OpenAI-standard
    # field that providers may want to respect (e.g. LiteLLM uses it).
    body.pop("provider", None)

    if not stream:
        return await _non_streaming(provider, messages)
    return await _streaming(provider, messages)


async def _non_streaming(provider, messages) -> JSONResponse:
    parts: list[str] = []
    error: str | None = None
    async for event in provider.chat(messages, stream=False):
        if isinstance(event, TokenEvent):
            parts.append(event.delta)
        elif isinstance(event, ThinkingTokenEvent):
            # Thinking content is intentionally DROPPED from non-streaming
            # responses — there's no place to put it. Streaming clients
            # see it on the named SSE channel.
            continue
        elif isinstance(event, ErrorEvent):
            error = event.message
        elif isinstance(event, FinalDoneEvent):
            break

    content = "".join(parts)
    finish_reason = "error" if error else "stop"
    response = {
        "id": f"chatcmpl-{uuid.uuid4().hex[:24]}",
        "object": "chat.completion",
        "created": int(time.time()),
        "model": "nodeava-orch",
        "choices": [
            {
                "index": 0,
                "message": {"role": "assistant", "content": content},
                "finish_reason": finish_reason,
            }
        ],
    }
    if error:
        response["error"] = error
    return JSONResponse(response)


async def _streaming(provider, messages) -> StreamingResponse:
    async def gen():
        yield encode_openai_chunk(delta_content=None, role="assistant")

        async for event in provider.chat(messages, stream=True):
            if isinstance(event, TokenEvent):
                yield encode_openai_chunk(delta_content=event.delta)
            elif isinstance(event, ThinkingTokenEvent):
                # Named SSE channel — frontends listen via
                # EventSource.addEventListener("thinking_token", ...)
                yield encode_sse(event)
            elif isinstance(event, ErrorEvent):
                yield encode_sse(event)
            elif isinstance(event, FinalDoneEvent):
                break

        yield encode_openai_chunk(delta_content=None, finish_reason="stop")
        yield encode_openai_done()

    return StreamingResponse(gen(), media_type="text/event-stream")
