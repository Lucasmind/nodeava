# nodeava-orch

An OpenAI-compatible chat-completions proxy in front of NodeAva's local
llama-server. This service is the seam where:

- The frontend talks to one URL regardless of backend (local or cloud).
- The agentic tool loop (Plan #4) lives.
- Tier A SSE events (`tool_call_start`, etc.) are emitted to drive the
  visualizer panels.

**Plan #1 scope:** scaffold + LocalLlamaProvider + chat/health/models
routes. Tools, LiteLLM, and agentic loop come in later plans.

## Endpoints

| Method | Path | Purpose |
|---|---|---|
| `POST` | `/v1/chat/completions` | OpenAI-compatible chat (stream + non-stream) |
| `POST` | `/chat/completions` | Alias |
| `GET`  | `/v1/models` | Proxy of backend model list |
| `GET`  | `/health` | Reports backend reachability |

## Configuration

Env vars (loaded via `pydantic-settings`):

| Var | Default | Purpose |
|---|---|---|
| `LLAMA_URL` | `http://localhost:8081` | Backend llama-server URL |
| `REQUEST_TIMEOUT` | `300` | Seconds, applies to all backend calls |
| `BIND_HOST` | `127.0.0.1` | Listener host. Default = localhost only. |
| `BIND_PORT` | `8082` | Listener port. |

## Run locally (dev)

```bash
cd services/orchestrator
python3.12 -m venv .venv
source .venv/bin/activate
pip install -r requirements-dev.txt
pip install -e .

# Point at a running llama-server (the workshop default port is 8081).
export LLAMA_URL=http://localhost:8081

# Production-style — honors BIND_HOST / BIND_PORT from env.
python -m orchestrator.main

# Or for hot-reload during development:
uvicorn orchestrator.main:app --reload --port 8082
```

## Run via Docker (with the rest of NodeAva)

```bash
# From the repo root:
docker compose up -d orchestrator
```

## Test

```bash
cd services/orchestrator
source .venv/bin/activate
pytest -v
```

## Architecture

```
HTTP (OpenAI) ──► routes/chat.py
                       │
                       ▼
                 Provider.chat() ──► local.py (Plan #1)
                       │              litellm.py (Plan #2)
                       │
                       ▼
                 Event async iter
                       │
                       ▼
              SSE encoder (sse.py)
                       │
                       ▼
                  Wire to client
```

A Provider is an abstract async generator that yields typed Events
(`orchestrator/events.py`). The chat route translates Events into
OpenAI-compatible SSE chunks (for the OpenAI client) and named SSE
events (for the frontend's Tier A panels) on a single stream.

## Adding a new provider

1. Subclass `orchestrator.providers.base.Provider`.
2. Implement the `chat()` async generator — yield `TokenEvent`,
   `ErrorEvent`, `FinalDoneEvent` (Plan #1 events). Later plans add
   more event types you'll yield from too.
3. Register it in `orchestrator/main.py::build_provider` keyed off a
   settings field.
4. Write tests that mock its backend with `respx`.

## Why a custom service when LLMRunners has one?

NodeAva needs a NodeAva-flavored orchestrator: provider switching,
wiki tools, named SSE events for visualizers, localhost-only default.
The LLMRunners orchestrator is the inspiration but is shaped for a
different deployment (chimera, MoE thinking models, OpenWebUI). See
`docs/superpowers/specs/2026-05-16-nodeava-workshop-mvp-design.md`.
