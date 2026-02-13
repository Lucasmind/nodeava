# NodeAva — Development Guide

Self-contained digital avatar that runs entirely on one machine. No cloud APIs.

## Architecture

4 Docker services behind nginx:

```
Browser (localhost:3000)
  └── nginx ──┬── /api/stt/ ──► whisper.cpp (port 8080)  [Vulkan]
              ├── /api/tts/ ──► Kokoro-FastAPI (port 8880) [CUDA/ROCm]
              └── /api/llm/ ──► llama.cpp (port 8081)     [CUDA/Vulkan]
```

- **Frontend**: Vite + Three.js + TalkingHead + VAD-web (browser-based orchestrator)
- **LLM**: Qwen3-4B via llama.cpp (thinking model with `<think>` tags)
- **TTS**: Kokoro-82M via Kokoro-FastAPI (returns PCM + word timestamps)
- **STT**: Whisper base.en via whisper.cpp (Vulkan)

## Key Files

| File | Purpose |
|------|---------|
| `frontend/src/pipeline/Orchestrator.js` | Main pipeline: LLM streaming → thinking filter → sentence split → TTS queue |
| `frontend/src/app/config.js` | All configuration: endpoints, system prompt, VAD thresholds |
| `frontend/src/llm/LLMClient.js` | OpenAI-compatible SSE streaming client |
| `frontend/src/tts/TTSManager.js` | Kokoro-FastAPI client, PCM decoding, timestamp mapping |
| `frontend/src/stt/STTManager.js` | VAD (Silero) + Whisper transcription |
| `frontend/src/avatar/AvatarManager.js` | TalkingHead wrapper, 3D model, lip sync |
| `docker-compose.yml` | Base service definitions |
| `docker-compose.gpu-nvidia.yml` | NVIDIA CUDA overrides |
| `docker-compose.gpu-amd.yml` | AMD Vulkan + ROCm overrides |

## Development

```bash
# Frontend dev server (hot reload)
cd frontend && npm install && npm run dev

# Services (need GPU profile)
docker compose -f docker-compose.yml -f docker-compose.gpu-nvidia.yml up stt tts llm
```

Vite dev proxies: STT → localhost:8080, TTS → localhost:8880, LLM → localhost:8081

## GPU Profiles

- **NVIDIA**: `docker-compose.gpu-nvidia.yml` — CUDA for LLM+TTS, Vulkan for STT
- **AMD**: `docker-compose.gpu-amd.yml` — Vulkan for LLM+STT, ROCm for TTS (built from `docker/kokoro-rocm/Dockerfile`)
- **Windows + AMD**: Not supported (Docker Desktop limitation)

## Qwen3 Thinking Mode

The LLM uses `--jinja --reasoning-format none` flags. Output format:

```
<think>
Internal reasoning...
</think>

[happy] The visible response to the user.
```

- Orchestrator buffers first 7 chars to detect `<think>` tag
- Thinking content is stripped before display and history storage
- Temperature set server-side (`--temp 0.6`) — DO NOT use temp 0 with thinking models
- Emotion tags (`[happy]`, `[neutral]`, etc.) parsed after thinking filter

## Port Mappings

| Service | Internal | External |
|---------|----------|----------|
| Frontend/nginx | 80 | 3000 |
| STT (whisper.cpp) | 8080 | 8080 |
| LLM (llama.cpp) | 8080 | 8081 |
| TTS (Kokoro-FastAPI) | 8880 | 8880 |

## Vite/ONNX Compatibility (DO NOT CHANGE)

- `vad-web` is CJS: must NOT be excluded from optimizeDeps
- `talkinghead` uses dynamic workers: MUST be excluded from optimizeDeps
- ONNX WASM files served by custom Vite plugin (`serveOnnxFiles()`)
- VAD init is lazy (first mic click) — getUserMedia blocks page load otherwise
- After changing optimizeDeps: delete `node_modules/.vite` cache

## Testing

```bash
# Check LLM is loaded
curl http://localhost:8081/v1/models

# Test TTS
curl -X POST http://localhost:8880/dev/captioned_speech \
  -H 'Content-Type: application/json' \
  -d '{"model":"kokoro","input":"Hello","voice":"af_bella","response_format":"pcm","stream":false,"return_timestamps":true}'

# Test STT (with a WAV file)
curl -X POST http://localhost:8080/v1/audio/transcriptions \
  -F "file=@test.wav" -F "model=base.en"
```

## macOS (Apple Silicon) — Native Mode

macOS runs all services natively (no Docker) for Metal/MPS GPU acceleration.

### Scripts

| Script | Purpose |
|--------|---------|
| `scripts/setup-mac.sh` | Install Homebrew packages, clone Kokoro-FastAPI, download models |
| `scripts/start-mac.sh` | Launch all services + Vite dev server |
| `scripts/stop-mac.sh` | Kill all running services |

### How It Works

- **LLM**: `llama-server` via Homebrew — Metal GPU auto-enabled
- **TTS**: Kokoro-FastAPI cloned to `~/.nodeava/kokoro-fastapi/`, run via `uv` with `DEVICE_TYPE=mps` (PyTorch MPS)
- **STT**: `whisper-server` via Homebrew — Metal GPU auto-enabled
- **Frontend**: Vite dev server (no nginx) — same proxy config routes to native services
- **Same ports**: LLM 8081, TTS 8880, STT 8080, Frontend 3000 — identical to Docker setup
- **PID files**: Written to `.pids/` for process management
- **Logs**: Written to `logs/` (both dirs gitignored)

### Why Not Docker on Mac

Docker Desktop on macOS runs a Linux VM — no GPU passthrough to Metal/MPS. Docker services would run CPU-only, too slow for TTS inference.

## Known Constraints

- Default avatar (default-avatar.glb) is CC BY-NC-SA 4.0, licensed separately from project code (Apache-2.0).
- AMD TTS uses ROCm (first build ~20-30 min, ~22GB image)
- Windows + AMD GPU = not supported (Docker Desktop/WSL2 limitation)
- Minimum 8 GB VRAM recommended (~4.8 GB actual usage)
- macOS: requires Apple Silicon (M1+), 16 GB unified memory recommended
