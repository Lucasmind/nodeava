"""Chat completions route — both non-streaming and streaming.

This is the workhorse endpoint. In Plan #1 it forwards every request
through the configured Provider. Plans #3-#4 will add an agentic loop
that wraps the provider when tools are enabled.
"""
import time
import uuid

from fastapi import APIRouter, Request
from fastapi.responses import JSONResponse, StreamingResponse

from orchestrator.events import ErrorEvent, FinalDoneEvent, TokenEvent
from orchestrator.sse import encode_openai_chunk, encode_openai_done, encode_sse

router = APIRouter()


@router.post("/v1/chat/completions")
@router.post("/chat/completions")
async def chat_completions(request: Request):
    body = await request.json()
    messages = body.get("messages") or []
    stream = bool(body.get("stream", False))

    provider = request.app.state.provider

    if not stream:
        return await _non_streaming(provider, messages)
    return await _streaming(provider, messages)


async def _non_streaming(provider, messages) -> JSONResponse:
    parts: list[str] = []
    error: str | None = None
    async for event in provider.chat(messages, stream=False):
        if isinstance(event, TokenEvent):
            parts.append(event.delta)
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
        # Initial role chunk (OpenAI convention — many clients expect this).
        yield encode_openai_chunk(delta_content=None, role="assistant")

        async for event in provider.chat(messages, stream=True):
            if isinstance(event, TokenEvent):
                yield encode_openai_chunk(delta_content=event.delta)
            elif isinstance(event, ErrorEvent):
                # Emit on the named SSE event channel so the frontend can
                # display the error without confusing the OpenAI SDK parser.
                yield encode_sse(event)
            elif isinstance(event, FinalDoneEvent):
                break

        yield encode_openai_chunk(delta_content=None, finish_reason="stop")
        yield encode_openai_done()

    return StreamingResponse(gen(), media_type="text/event-stream")
