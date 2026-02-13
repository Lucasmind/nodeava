# Digital Avatar Project - Implementation Plan

## Context

Build a fully local, containerized conversational digital avatar system. A user opens a web browser, sees a cartoon-style 3D avatar, and has a voice conversation with it. The avatar listens (STT), thinks (LLM on remote host Chimera at http://192.168.1.221:8080/v1), speaks back (TTS) with synchronized lip movement and emotions.

**Key constraints:** GPU-agnostic (AMD/Nvidia/Intel), no CUDA lock-in, all containers for lift-and-shift portability, fully local (no cloud), open source (MIT/Apache 2.0).

**LLM setup:** llama.cpp on Chimera (192.168.1.221:8080), OSS 120B model, OpenAI-compatible API.

---

## Architecture

```
Browser (user's machine)
├── TalkingHead (Three.js/WebGL) → 3D avatar with lip sync + emotions
├── HeadTTS (Kokoro ONNX, WebGPU/WASM) → TTS runs IN BROWSER, outputs audio+visemes
├── @ricky0123/vad-web (Silero VAD) → Voice activity detection IN BROWSER
└── Orchestrator.js → wires the pipeline together

Container: frontend (nginx) - serves static web app + proxies API requests
Container: stt-service (whisper.cpp Vulkan) - /v1/audio/transcriptions
Remote: Chimera (192.168.1.221:8080) - llama.cpp /v1/chat/completions
```

Only 2 containers to build. TTS runs in-browser. LLM already exists on Chimera.

## Phases

- [x] Phase 0: Research (complete)
- [ ] Phase 1: Project scaffold + static avatar rendering
- [ ] Phase 2: In-browser TTS + lip sync
- [ ] Phase 3: STT container + voice input
- [ ] Phase 4: LLM integration + full pipeline
- [ ] Phase 5: Polish + error handling
- [ ] Phase 6: Docker Compose full stack
