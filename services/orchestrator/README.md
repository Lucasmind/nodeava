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
| `LLAMA_URL` | `http://localhost:8081` | Backend llama-server URL (used when provider=local) |
| `REQUEST_TIMEOUT` | `300` | Seconds, applies to all backend calls |
| `BIND_HOST` | `127.0.0.1` | Listener host. Default = localhost only. |
| `BIND_PORT` | `8082` | Listener port. |
| `PROVIDER` | `local` | Default provider when request omits one |
| `PROVIDER_MODEL` | `""` | Default model id (only used when PROVIDER != "local") |

## Provider selection — local vs. cloud (Plan #2)

The orchestrator can route per request to either the local llama-server
(default) or any LiteLLM-supported cloud provider (Anthropic, OpenAI,
Groq, Together, Mistral, ...). The frontend sends the API key in a
header — it's never stored server-side.

### Request-level override

```bash
curl http://localhost:8082/v1/chat/completions \
  -H 'Content-Type: application/json' \
  -H 'X-Provider-Key: sk-ant-…' \
  -d '{
    "provider": "anthropic",
    "model": "claude-haiku-4-5-20251001",
    "messages": [{"role": "user", "content": "hi"}]
  }'
```

Body fields consumed by the orchestrator (stripped before upstream call):
- `provider` — `"local"`, `"anthropic"`, `"openai"`, `"groq"`, ... (anything LiteLLM supports)
- `model` — model id for the chosen provider; kept in the upstream call

Headers consumed by the orchestrator:
- `X-Provider-Key` — your API key for the chosen cloud provider

### Deploy-level default

For deployments that always want a cloud provider, set env vars:

| Var | Example | Purpose |
|---|---|---|
| `PROVIDER` | `anthropic` | Default provider when request omits one |
| `PROVIDER_MODEL` | `claude-haiku-4-5-20251001` | Default model for that provider |

Per-request overrides still win. API keys still come from `X-Provider-Key` —
the orchestrator never reads keys from env vars (defense in depth).

### Reasoning content streaming

Providers that expose reasoning (Anthropic extended thinking) emit
`ThinkingTokenEvent` on a NAMED SSE channel — `event: thinking_token`.
The default `data:` stream stays clean for OpenAI-SDK clients. Hook the
brain-pane visualizer with:

```js
const es = new EventSource('/v1/chat/completions?...');
es.addEventListener('thinking_token', (ev) => {
  const { delta } = JSON.parse(ev.data);
  brainPane.append(delta);
});
```

OpenAI o-series models hide reasoning entirely — no thinking events
will be emitted for those.

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

Most providers come for free via LiteLLM — just set `provider` in the
request body and supply `X-Provider-Key`. Custom providers (e.g. a
shimmed CLI, a fully-local subprocess, an in-process model) follow this
recipe:

1. Subclass `orchestrator.providers.base.Provider`.
2. Implement the `chat()` async generator — yield `TokenEvent`,
   `ThinkingTokenEvent` (if reasoning), `ErrorEvent`, `FinalDoneEvent`.
3. Update `orchestrator.providers.pick_provider` to recognise its
   `provider` name and construct your class.
4. Write tests that mock its backend.

## Why a custom service when LLMRunners has one?

NodeAva needs a NodeAva-flavored orchestrator: provider switching,
wiki tools, named SSE events for visualizers, localhost-only default.
The LLMRunners orchestrator is the inspiration but is shaped for a
different deployment (chimera, MoE thinking models, OpenWebUI). See
`docs/superpowers/specs/2026-05-16-nodeava-workshop-mvp-design.md`.
