# Integrated Open-Source Digital Avatar Projects Research

**Date:** 2026-02-10
**Goal:** Find existing open-source projects that ALREADY combine avatar + TTS + STT + LLM into integrated conversational avatar systems as potential starting points.

---

## TABLE OF CONTENTS

1. [Executive Summary & Top Picks](#executive-summary--top-picks)
2. [Open-LLM-VTuber](#1-open-llm-vtuber)
3. [Linly-Talker](#2-linly-talker)
4. [OpenAvatarChat](#3-openavatarchat)
5. [Amica](#4-amica)
6. [TalkingHead Ecosystem (met4citizen)](#5-talkinghead-ecosystem-met4citizen)
7. [Duix-Avatar (formerly HeyGem)](#6-duix-avatar-formerly-heygem)
8. [ProtoReplicant](#7-protoreplicant)
9. [Vroid AI Companion](#8-vroid-ai-companion)
10. [AI Iris Avatar](#9-ai-iris-avatar)
11. [TalkMateAI](#10-talkmateai)
12. [AIAvatarKit](#11-aiavatarkit)
13. [talking-avatar-with-ai](#12-talking-avatar-with-ai)
14. [LiveTalk-Unity](#13-livetalk-unity)
15. [NVIDIA ACE / Tokkio / Pipecat](#14-nvidia-ace--tokkio--pipecat)
16. [Pipecat Framework](#15-pipecat-framework)
17. [AllTalk TTS](#16-alltalk-tts)
18. [LLM-Based-3D-Avatar-Assistant](#17-llm-based-3d-avatar-assistant)
19. [Realtime Avatar AI Companion](#18-realtime-avatar-ai-companion)
20. [Comparative Matrix](#comparative-matrix)
21. [Recommended Starting Points](#recommended-starting-points)

---

## EXECUTIVE SUMMARY & TOP PICKS

### Tier 1: Most Complete & Best Maintained (Start Here)

**1. Open-LLM-VTuber -- BEST OVERALL INTEGRATED PROJECT**
- 5.9k stars, MIT license, very active (v1.2.1 Aug 2025)
- Full pipeline: STT + LLM + TTS + Live2D avatar
- Runs 100% offline on all platforms (Windows/Mac/Linux)
- Supports CPU, NVIDIA GPU, and partial Mac GPU
- Docker support, web + desktop clients
- Voice interruption, long-term memory, emotion mapping
- **Missing:** Uses Live2D (2D), not 3D VRM avatars
- **Closest to requirements:** 85%

**2. OpenAvatarChat (Alibaba) -- BEST FOR 3D AVATARS**
- 3.1k stars, Apache 2.0 license, backed by Alibaba
- Full pipeline: ASR + LLM + TTS + 3D avatar rendering
- Multiple avatar renderers: LiteAvatar, LAM (3D Gaussian), MuseTalk
- Docker support with CUDA
- Modular architecture with swappable components
- **Missing:** Requires NVIDIA GPU (20GB+ VRAM recommended)
- **Closest to requirements:** 75%

**3. Amica -- BEST FOR VRM + BROWSER**
- 1.2k stars, MIT license, active development
- Full pipeline: STT + LLM + TTS + VRM avatar
- VRM avatar support with emotion engine
- Supports Ollama, KoboldCpp, and many local LLMs
- Docker support, web + desktop (Tauri)
- Local models = full privacy
- **Missing:** Lip sync method not well documented
- **Closest to requirements:** 80%

**4. Linly-Talker -- BEST FOR REALISTIC TALKING HEADS**
- 3.1k stars, MIT license, very active (2026 updates)
- Full pipeline: ASR + LLM + TTS + talking head synthesis
- Multiple talking head models: SadTalker, Wav2Lip, MuseTalk
- Voice cloning via GPT-SoVITS, CosyVoice
- Docker support, Gradio WebUI
- Real-time streaming mode available
- **Missing:** Uses realistic talking heads (not cartoon VRM), requires NVIDIA GPU
- **Closest to requirements:** 70%

### Tier 2: Good Starting Points with Gaps

**5. TalkingHead + HeadTTS (met4citizen) -- BEST LIP SYNC**
- 1k+ stars combined, MIT license
- Excellent browser-based VRM lip sync + free TTS
- GPU-agnostic, runs in any modern browser
- **Missing:** No built-in STT or LLM integration (you add your own)

**6. Duix-Avatar -- BEST FOR VIDEO AVATAR CLONING**
- 12.3k stars, community license (free for < 100k users)
- Video avatar synthesis with voice cloning
- Full Docker deployment
- **Missing:** No built-in LLM, not real-time interactive

### Tier 3: Smaller/Experimental Projects

**7-18.** Various smaller projects with partial integration (detailed below)

---

## 1. OPEN-LLM-VTUBER

**Repository:** https://github.com/Open-LLM-VTuber/Open-LLM-VTuber
**Documentation:** https://open-llm-vtuber.github.io/en/
**Stars:** 5.9k | **Forks:** 768 | **License:** MIT
**Last Release:** v1.2.1 (August 2025)
**Language:** Python (96.6%), JavaScript (2.8%)

### Components Included

| Component | Options |
|-----------|---------|
| **STT/ASR** | sherpa-onnx, FunASR, Faster-Whisper, Whisper.cpp, Whisper, Groq Whisper, Azure ASR |
| **TTS** | sherpa-onnx, pyttsx3, MeloTTS, Coqui-TTS, GPTSoVITS, Bark, CosyVoice, Edge TTS, Fish Audio, Azure TTS |
| **LLM** | Ollama, OpenAI-compatible, Gemini, Claude, Mistral, DeepSeek, Zhipu AI, GGUF, LM Studio, vLLM |
| **Avatar** | Live2D models with emotion-mapped expressions |
| **Lip Sync** | Built-in audio-to-lip-sync for Live2D |

### Key Features
- Voice interruption without headphones
- Touch feedback for avatar interaction
- Live2D expressions with emotion mapping
- Desktop pet mode (transparent background)
- AI inner thoughts display
- Camera/screen recording visual perception
- Voice cloning capability
- Chat log persistence
- TTS language translation
- Proactive AI speaking
- Letta-based long-term memory (v1.2.0)
- MCP (Model Context Protocol) support
- Bilibili Danmaku client (streaming)

### GPU Requirements
- NVIDIA GPU supported (optimal)
- Non-NVIDIA GPU compatible
- CPU operation option (slower)
- Cloud API fallback for heavy tasks
- Partial macOS GPU acceleration

### Docker Support
- Yes, Docker containerization available

### Platform Support
- Windows, macOS, Linux
- Web browser client
- Desktop client (pet mode)

### Active Maintenance
- Very active: 31+ contributors, frequent releases
- Latest release Aug 2025
- Strong documentation site

### What's Missing for This Project
- Uses **Live2D (2D)** avatars, not 3D VRM
- No built-in 3D avatar support
- Would need custom frontend for 3D/VRM avatar
- Live2D is not truly open source (Cubism SDK has restrictions)

### Assessment
Open-LLM-VTuber has the most complete and well-maintained backend pipeline. Its modular architecture with many STT/TTS/LLM options is excellent. The main gap is the Live2D frontend -- replacing it with a Three.js/VRM frontend using TalkingHead would create an ideal solution.

---

## 2. LINLY-TALKER

**Repository:** https://github.com/Kedreamix/Linly-Talker
**Stars:** 3.1k | **Forks:** 500 | **License:** MIT
**Last Update:** February 2026 (stream architecture)
**Language:** Python

### Components Included

| Component | Options |
|-----------|---------|
| **STT/ASR** | Whisper, FunASR, OmniSenseVoice |
| **TTS** | Edge TTS, PaddleTTS (offline), CosyVoice, ChatTTS, FishTTS (planned) |
| **Voice Cloning** | GPT-SoVITS, XTTS, CosyVoice |
| **LLM** | Linly-AI, Qwen, Gemini-Pro, ChatGPT, ChatGLM, GPT4Free |
| **Talking Head** | SadTalker, Wav2Lip, Wav2Lipv2, MuseTalk, ER-NeRF, TFG |
| **Lip Sync** | Integrated via talking head models |

### Key Features
- Multiple talking head model choices
- Voice cloning from 1 minute of speech data
- Real-time streaming architecture (Linly-Talker-Stream)
- WebRTC for low-latency full-duplex conversation
- Gradio-based WebUI
- FastAPI integration
- MuseTalk achieves near real-time speed

### GPU Requirements
- NVIDIA GPU required (CUDA)
- PyTorch 2.0.1+ with CUDA 11.8/12.1/12.4
- Multiple GPU-intensive models running simultaneously
- Specific VRAM requirements not documented but significant

### Docker Support
- Yes, pre-built Docker images available
- `docker pull registry.cn-beijing.aliyuncs.com/codewithgpu2/kedreamix-linly-talker`

### Deployment Options
- Docker
- Local installation (Conda/pip)
- Google Colab
- AutoDL cloud
- Windows all-in-one package

### Active Maintenance
- Very active: updates through Feb 2026
- New stream architecture recently added
- Active GitHub issues

### What's Missing for This Project
- **Requires NVIDIA GPU** (not GPU-agnostic)
- Uses **realistic talking heads** (photo-driven), not cartoon/stylized 3D
- No VRM avatar support
- Heavy computational requirements
- Chinese-focused documentation (English available but secondary)

### Assessment
Linly-Talker is the most feature-complete system for realistic talking head avatars. Its multi-model approach (SadTalker, MuseTalk, Wav2Lip) gives flexibility. However, it's fundamentally designed for photorealistic avatars driven by face images, not 3D cartoon-style VRM models. The CUDA requirement is also a dealbreaker for GPU-agnostic deployment.

---

## 3. OPENAVATARCHAT

**Repository:** https://github.com/HumanAIGC-Engineering/OpenAvatarChat
**Website:** https://www.openavatarchat.ai/
**Stars:** 3.1k | **Forks:** 513 | **License:** Apache 2.0
**Last Release:** v0.5.1 (August 2025)
**Backed by:** Alibaba HumanAIGC team
**Language:** Python (98.1%)

### Components Included

| Component | Options |
|-----------|---------|
| **STT/ASR** | SenseVoice, Qwen-Omni, MiniCPM-o |
| **TTS** | CosyVoice (local or API), Edge TTS, Qwen-Omni |
| **LLM** | MiniCPM-o (local multimodal), OpenAI-compatible APIs, Qwen-Omni Realtime, Dify Chatflow |
| **Avatar Rendering** | LiteAvatar (server-side, lightweight), LAM (3D Gaussian, client-side), MuseTalk (lip sync) |
| **Lip Sync** | Via MuseTalk or LiteAvatar built-in |

### Key Features
- Modular architecture with independently configurable modules
- Six preset YAML configurations
- WebRTC real-time communication
- Multimodal interaction (text, audio, video)
- ~2.2 second average latency
- Separate WebUI frontend
- MiniCPM-o multimodal model can replace ASR+LLM+TTS chain

### GPU Requirements
- NVIDIA CUDA-capable GPU required
- 20GB+ VRAM for unquantized MiniCPM-o
- 10GB+ with int4 quantization
- CPU alternative: i9-13980HX achieves 30 FPS rendering (LiteAvatar only)

### Docker Support
- Yes, Docker Compose provided
- CUDA 12.8 Dockerfile
- Pre-built configurations

### Platform Support
- Linux, Windows
- Browser-based WebUI (separate repo)
- WebRTC-based communication

### Active Maintenance
- Very active: backed by Alibaba's HumanAIGC team
- Regular releases through 2025
- Growing community (3.1k stars)

### What's Missing for This Project
- **Requires NVIDIA GPU** for full functionality (CPU only for LiteAvatar)
- Avatar options are limited (LiteAvatar is basic, LAM is heavy)
- No VRM format support
- No cartoon/stylized avatar option
- Complex infrastructure setup
- Newer project with less community testing

### Assessment
OpenAvatarChat has the strongest architectural design -- true modular pipeline with swappable components. The Alibaba backing gives confidence in continued development. However, the NVIDIA GPU requirement and lack of VRM/cartoon avatar support are significant gaps. The modular design means components could be reused even if the avatar renderer is replaced.

---

## 4. AMICA

**Repository:** https://github.com/semperai/amica
**Website:** https://www.heyamica.com/
**Documentation:** https://docs.heyamica.com/
**Stars:** 1.2k | **Forks:** 221 | **License:** MIT
**Commits:** 965 total

### Components Included

| Component | Options |
|-----------|---------|
| **STT/ASR** | OpenAI Whisper |
| **TTS** | Eleven Labs, SpeechT5, OpenAI TTS, Coqui (local), RVC, AllTalkTTS |
| **LLM** | Llama.cpp, ChatGPT/OpenAI-compatible, Window.ai, Ollama, KoboldCpp, Oobabooga, OpenRouter |
| **Avatar** | VRM models (via @pixiv/three-vrm + Three.js) |
| **Vision** | Bakllava visual processing |
| **Lip Sync** | Built-in (method not well documented) |

### Key Features
- VRM avatar import (drag and drop)
- 14 different emotions and animations
- Autonomous behavior (gets bored, engages, sleeps)
- Voice activity detection with interruption
- Vision capabilities (can see via camera)
- Full local operation (Ollama + Coqui)
- Web + Desktop (Tauri framework)
- Custom personality configuration
- External API for agent integration

### GPU Requirements
- Not explicitly specified
- Local LLMs via Ollama need appropriate hardware
- VRM rendering via WebGL (GPU-agnostic)
- Coqui TTS can run on CPU

### Docker Support
- Yes, Dockerfile and docker-compose.yml included

### Platform Support
- Web (mobile, tablet, desktop browsers)
- Desktop via Tauri (Windows, macOS, Linux)

### Active Maintenance
- Active development (965 commits)
- Multiple TTS/LLM integrations added over time

### What's Missing for This Project
- **Lip sync quality** not well documented (unclear method)
- STT options limited to Whisper only
- Some TTS options require cloud APIs (Eleven Labs, OpenAI)
- No built-in voice cloning
- Less documentation than Open-LLM-VTuber

### Assessment
Amica is the closest existing project to the requirements: VRM avatars + local LLM + TTS + STT in a browser/desktop app. The VRM support with Three.js is exactly the right technology choice. The main concerns are: (1) lip sync quality is unclear, (2) STT options are limited, (3) less actively maintained than Open-LLM-VTuber. Could be an excellent starting point if lip sync is improved using TalkingHead/HeadTTS.

---

## 5. TALKINGHEAD ECOSYSTEM (MET4CITIZEN)

**Repositories:**
- TalkingHead: https://github.com/met4citizen/TalkingHead (1k+ stars)
- HeadTTS: https://github.com/met4citizen/HeadTTS (106 stars)
**License:** MIT (both)

### Components Included

| Component | Built-in? | Options |
|-----------|-----------|---------|
| **STT/ASR** | No | Bring your own (examples show OpenAI, Google, Azure) |
| **TTS** | Yes (HeadTTS) | HeadTTS/Kokoro (free, in-browser), Google Cloud, ElevenLabs, Azure |
| **LLM** | No | Bring your own (examples show GPT, Gemini) |
| **Avatar** | Yes | GLB with ARKit + Oculus blendshapes |
| **Lip Sync** | Yes | Phoneme-based (from TTS) or audio-driven (HeadAudio) |

### Key Features
- Best-in-class browser-based lip sync for VRM-style avatars
- HeadTTS produces both audio AND visemes in one pass
- WebGPU TTS: 3x real-time speed
- Full body animation with physics
- Emoji to facial expression mapping
- Multiple language support for lip sync
- Published in academic research

### GPU Requirements
- WebGL required (universally available)
- WebGPU optional (3x faster TTS)
- No CUDA dependency
- Fully GPU-agnostic

### What's Missing
- **No STT** -- must integrate separately
- **No LLM** -- must integrate separately
- **No conversation management** -- pure rendering/TTS component
- Requires building the orchestration layer

### Assessment
TalkingHead + HeadTTS is NOT an integrated project, but it provides the best avatar rendering + lip sync + TTS foundation. Combining it with Open-LLM-VTuber's backend (STT + LLM) or building a simple orchestrator would create the ideal solution. The MIT license and GPU-agnostic design match requirements perfectly.

---

## 6. DUIX-AVATAR (FORMERLY HEYGEM)

**Repository:** https://github.com/duixcom/Duix-Avatar
**Stars:** 12.3k | **Forks:** 2k
**License:** Community license (free commercial use for < 100k users or < $10M revenue)
**Created:** December 2024

### Components Included

| Component | Built-in? |
|-----------|-----------|
| **STT/ASR** | Yes (FunASR via Docker service) |
| **TTS** | Yes (Fish-Speech via Docker service) |
| **LLM** | No |
| **Avatar** | Video avatar synthesis (realistic) |
| **Lip Sync** | Yes (video-based lip sync engine) |
| **Voice Cloning** | Yes (from ~10 second reference video) |

### System Requirements
- CPU: Intel i5-13400F or better
- RAM: 32GB
- GPU: RTX 4070 or better (NVIDIA only, 8GB+ VRAM)
- Storage: 130GB+
- NVIDIA drivers required

### Docker Support
- Three Docker services via docker-compose
- ~70GB total image download
- Lite version available (single service)

### Deployment
- Windows 10+ or Ubuntu 22.04
- Docker-based deployment
- Electron desktop client
- REST API endpoints
- All computing is local

### What's Missing
- **No LLM integration** (video synthesis only)
- **Not real-time interactive** (generates video from audio)
- **NVIDIA GPU required** (RTX 4070+)
- **Realistic only** (no cartoon/stylized option)
- No VRM support
- Restrictive license for large enterprises

### Assessment
Duix-Avatar is very popular (12.3k stars) but fundamentally different from what's needed. It's a video avatar synthesis tool (like a self-hosted HeyGen), not an interactive conversational agent. It generates video files from audio input. Not suitable as a starting point for a real-time conversational avatar.

---

## 7. PROTOREPLICANT

**Repository:** https://github.com/OpenReplicant/ProtoReplicant
**License:** Open source (not specified)
**Status:** Prototype/Proof-of-Concept

### Components Included

| Component | Implementation |
|-----------|---------------|
| **VAD** | Voice Activity Detection (browser) |
| **STT** | Transcription in browser |
| **LLM** | Kobold Horde (pygmalion-6b default) |
| **TTS** | Coqui TTS |
| **Avatar** | VRM files (drag-and-drop) |
| **Lip Sync** | Audio-driven mouth/face movement |

### Pipeline
User speech -> Microphone -> VAD -> STT -> LLM (Kobold Horde) -> TTS (Coqui) -> Audio + lip sync -> VRM avatar

### Key Features
- Browser-based execution
- VRM drag-and-drop avatar loading
- Microservices for heavy processing
- Some models run in-browser

### What's Missing
- **Prototype quality** -- not production ready
- Limited documentation
- Small community
- No Docker support documented
- Kobold Horde dependency (external service)

### Assessment
ProtoReplicant demonstrates the correct architecture (VAD -> STT -> LLM -> TTS -> VRM in browser) but is a proof of concept, not a usable product. Valuable as a reference implementation showing how the pieces fit together.

---

## 8. VROID AI COMPANION

**Repository:** https://github.com/anjaydo/vroid-ai-companion
**Live Demo:** https://vroid-ai-companion.vercel.app/
**Status:** Active project

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | Not built-in |
| **TTS** | Google Gemini TTS |
| **LLM** | Google Gemini (via FastAPI backend) |
| **Avatar** | VRM via @pixiv/three-vrm |
| **Lip Sync** | Web Audio API FFT -> VRM expressions (Aa, Ee, Oh) |
| **Animations** | Mixamo FBX retargeted to VRM |

### Tech Stack
- Frontend: Next.js, React 19, @react-three/fiber, @pixiv/three-vrm, Zustand
- Backend: FastAPI, Google GenAI (Gemini)
- Data: Supabase (conversation history)

### Lip Sync Method
Web Audio API AnalyserNode (FFT 1024) computes energy in frequency bands, maps to VRM expressions Aa, Ee, Oh each frame.

### What's Missing
- **No STT** (text input only)
- Relies on Google Gemini API (not local)
- Basic FFT lip sync (only 3 mouth shapes)
- Small project, limited community

### Assessment
Good reference for Next.js + Three.js + VRM + Gemini integration pattern. The lip sync is basic (3 shapes via FFT) but the VRM rendering pipeline is solid. Could be improved significantly with TalkingHead or Lipsync-Engine.

---

## 9. AI IRIS AVATAR

**Repository:** https://github.com/Scthe/ai-iris-avatar
**License:** Not specified

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | Not built-in (implied audio input) |
| **TTS** | Configurable (streaming + DeepSpeed) |
| **LLM** | Configurable |
| **Avatar** | Custom 3D model in Unity |
| **Lip Sync** | Oculus OVR LipSync library |
| **Animations** | Unity state machine with random clip selection |

### Key Features
- Fast response time (< 4 second latency with streaming TTS + DeepSpeed)
- Unity client for 3D rendering
- Oculus lip sync for mouth shapes
- Skeleton animation (idle + speaking states)
- Remote event triggering (browser to Unity)

### What's Missing
- **Requires Unity** (not browser-based)
- No Docker support
- OVR LipSync is proprietary
- Small project
- Platform-specific

### Assessment
Demonstrates how to achieve low-latency conversational avatar in Unity with Oculus lip sync. The < 4 second response time is notable. However, Unity dependency makes it unsuitable for browser/container deployment.

---

## 10. TALKMATEAI

**Repository:** https://github.com/kiranbaby14/TalkMateAI

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | Voice input (method not specified) |
| **TTS** | Kokoro TTS (native word-level timing) |
| **LLM** | Multimodal AI |
| **Vision** | SmolVLM2-256M-Video-Instruct |
| **Avatar** | TalkingHead (met4citizen) |
| **Lip Sync** | Kokoro native timing + TalkingHead |

### Key Features
- Uses TalkingHead + Kokoro TTS for lip sync (best approach)
- Vision understanding via SmolVLM2
- Camera integration with voice commands
- WebSocket communication
- Real-time analytics
- Streaming response with chunked audio generation

### What's Missing
- Smaller project, less community
- Documentation may be limited
- Unclear local LLM support (may require cloud APIs)

### Assessment
TalkMateAI demonstrates the TalkingHead + Kokoro TTS integration working end-to-end. This is essentially the recommended architecture from the lip sync research. Good reference for how to combine these components, but may not be production-ready.

---

## 11. AIAVATARKIT

**Repository:** https://github.com/uezo/aiavatarkit
**PyPI:** `aiavatar`
**License:** Not specified
**Language:** Python 3.11+

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | Google Speech / Azure Speech Services |
| **TTS** | VOICEVOX |
| **LLM** | OpenAI API (ChatGPT) |
| **Avatar** | Platform-agnostic (VRChat, cluster, devices) |
| **Lip Sync** | Via platform (VRChat native, etc.) |

### Key Features
- Runs on any platform with audio I/O (PC, Raspberry Pi, robots)
- WebSocket server for multi-client conversations
- Wake word activation
- Extensible architecture

### Related Projects
- **ChatdollKit** (Unity-based, same author)
- **litests** (lightweight Speech-to-Speech framework)
- **WaifuOS** (full virtual companion suite)

### What's Missing
- Requires API keys (OpenAI, Google/Azure)
- VOICEVOX dependency (Japanese-focused TTS)
- No built-in avatar rendering
- Limited English-language documentation

### Assessment
AIAvatarKit is a good Python framework for building the orchestration layer. Its platform-agnostic design is interesting for IoT/robot use cases. However, it relies on external APIs and doesn't include avatar rendering, making it more of a middleware than a complete solution.

---

## 12. TALKING-AVATAR-WITH-AI

**Repository:** https://github.com/asanchezyali/talking-avatar-with-ai

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | OpenAI Whisper API |
| **TTS** | Eleven Labs API |
| **LLM** | OpenAI GPT |
| **Avatar** | React Three Fiber 3D model |
| **Lip Sync** | Rhubarb Lip Sync |

### Pipeline
Audio -> Whisper (STT) -> GPT (LLM) -> Eleven Labs (TTS) -> Rhubarb (lip sync) -> 3D avatar

### What's Missing
- **All cloud APIs** (no local operation)
- Rhubarb adds latency (batch processing)
- No Docker support
- Tutorial/demo project, not production-ready
- No VRM support (custom 3D model)

### Assessment
Good educational reference showing the full pipeline with widely-known tools. The Rhubarb lip sync approach adds noticeable latency since it processes complete audio files. All components require cloud API keys. Not suitable as a production starting point but useful for understanding the architecture.

---

## 13. LIVETALK-UNITY

**Repository:** https://github.com/arghyasur1991/LiveTalk-Unity

### Components Included

| Component | Implementation |
|-----------|---------------|
| **TTS** | SparkTTS (built-in) |
| **Avatar** | LivePortrait + MuseTalk |
| **Lip Sync** | MuseTalk (real-time) |
| **Facial Animation** | LivePortrait (expression transfer) |
| **STT** | Not included |
| **LLM** | Not included |

### Key Features
- ONNX + CoreML model optimization
- Dual pipeline: LivePortrait (animation) + MuseTalk (lip sync)
- 7 built-in expressions
- Character creation tools
- Cross-platform: macOS (CPU/CoreML)

### What's Missing
- **No STT or LLM** (rendering/synthesis only)
- Unity dependency
- Realistic talking heads (not cartoon/VRM)
- macOS focused (CoreML optimization)

### Assessment
LiveTalk-Unity excels at the avatar rendering layer (combining LivePortrait + MuseTalk in Unity), but lacks STT and LLM integration. More of a rendering component than an integrated system. The ONNX model approach is interesting for potential CPU deployment.

---

## 14. NVIDIA ACE / TOKKIO / PIPECAT

**Repositories:**
- ACE: https://github.com/NVIDIA/ACE
- ACE Controller: https://github.com/NVIDIA/ace-controller
- Digital Human Blueprint: https://github.com/NVIDIA-AI-Blueprints/digital-human

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT/ASR** | NVIDIA Riva |
| **TTS** | NVIDIA Riva |
| **LLM** | NVIDIA NIM (NeMo) + RAG |
| **Avatar** | Omniverse rendering + Audio2Face |
| **Lip Sync** | Audio2Face 3D |
| **Orchestrator** | Pipecat (open source) |
| **Transport** | WebSocket + WebRTC |

### Key Features
- Enterprise-grade digital human solution
- Multi-microservice architecture
- RAG integration for knowledge-grounded responses
- Pipecat open-source orchestrator
- Docker/Kubernetes deployment
- NIM inference microservices

### ACE Controller (Open Source)
- Based on Pipecat framework
- Audio2Face3DService, AnimationGraphService
- FacialGestureProviderProcessor, PostureProviderProcessor
- ACETransport for microservice integration

### GPU Requirements
- **NVIDIA GPU required** (T4, A10, L40S, A100 recommended)
- Enterprise-scale infrastructure
- Multiple GPU microservices

### License
- Pipecat: BSD-2-Clause (fully open source)
- ACE components: NVIDIA ACE License (restrictive)
- NIM: NVIDIA commercial license

### What's Missing for This Project
- **Heavy NVIDIA dependency** (GPU, CUDA, proprietary NIMs)
- Enterprise infrastructure requirements
- Not designed for single-machine deployment
- Expensive GPU requirements
- Mixed licensing

### Assessment
NVIDIA ACE/Tokkio represents the enterprise ceiling for digital human technology. The Pipecat orchestrator is valuable open source, but the full stack requires significant NVIDIA infrastructure. The ACE Controller code is useful as a reference for how to orchestrate the pipeline. For this project, only Pipecat itself is practically useful.

---

## 15. PIPECAT FRAMEWORK

**Repository:** https://github.com/pipecat-ai/pipecat
**Website:** https://www.pipecat.ai/
**License:** BSD-2-Clause
**Created by:** Daily.co

### What It Is
Open-source Python framework for building real-time voice and multimodal conversational agents. NOT an avatar project itself, but the orchestration layer that connects STT, LLM, TTS, and avatar components.

### Key Features
- 40+ AI service plugins
- Pipeline architecture for processing frames
- SDKs: Python, JavaScript, React, iOS, Android, C++
- WebSocket and WebRTC transport
- RTVIProcessor for real-time audio analysis (avatar animation)
- Sub-second voice-to-voice latency demonstrated

### Supported Services
STT, TTS, LLM from all major providers, plus custom service integration

### Avatar Support
- RTVIProcessor generates data for avatar animation
- Demonstrated with custom animated mascots
- Parallel pipeline for concurrent avatar streams
- NVIDIA ACE integration for Audio2Face

### Assessment
Pipecat is the best orchestration framework for this project. It handles the STT -> LLM -> TTS pipeline with real-time streaming and can feed data to an avatar renderer. Using Pipecat as the backend + TalkingHead as the frontend is a strong architecture choice.

---

## 16. ALLTALK TTS

**Repository:** https://github.com/erew123/alltalk_tts
**License:** AGPL-3.0 (important!)

### What It Is
Multi-engine TTS server, not a complete avatar project. Supports Coqui XTTS, VITS, Piper, Parler, F5, and custom engines.

### Key Features
- Multiple TTS engine support with easy switching
- Voice cloning pipeline (RVC)
- Narrator functionality
- Low VRAM mode + DeepSpeed support
- JSON API for 3rd party integration
- SillyTavern integration

### Avatar Integration
- Not built-in, but JSON API enables integration
- SillyTavern (which has avatar support) uses AllTalk
- Could serve as TTS component in custom pipeline

### License Warning
- **AGPL-3.0** -- viral copyleft license
- Any software that uses AllTalk must also be AGPL
- This may be a dealbreaker for many projects

### Assessment
AllTalk is an excellent TTS server but NOT an avatar project. Its AGPL license is restrictive. For this project, HeadTTS (MIT) or Piper (MIT) are better TTS choices unless voice cloning is critical.

---

## 17. LLM-BASED-3D-AVATAR-ASSISTANT

**Repository:** https://github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | OpenAI Whisper (language detection) |
| **TTS** | Parler TTS (fine-tuned) |
| **LLM** | Gemini |
| **Avatar** | Unity 3D character |
| **Lip Sync** | Custom facial expression model |
| **Animations** | Custom animation model |

### Pipeline
Microphone -> Whisper (language detect + STT) -> Gemini (LLM) -> Parler TTS -> Unity (3D avatar + lip sync + animations)

### Key Features
- GATEBOX-inspired virtual assistant
- Singing and dancing capabilities
- Dynamic animation generation
- WebSocket communication

### What's Missing
- Unity dependency
- Gemini API dependency
- Smaller project
- Not containerizable without Unity

### Assessment
Interesting project with unique features (singing, dancing) but Unity dependency and API requirements limit its applicability.

---

## 18. REALTIME AVATAR AI COMPANION

**Repository:** https://github.com/igna-s/Realtime_Avatar_AI_Companion

### Components Included

| Component | Implementation |
|-----------|---------------|
| **STT** | Not specified |
| **TTS** | OpenVoice (voice cloning) |
| **LLM** | Google Gemini |
| **Avatar** | VRM anime-style (Three.js) |
| **Lip Sync** | Audio-driven via Three.js |

### Key Features
- VRM avatar with idle/talking animations
- Automatic blinking
- Voice cloning via OpenVoice
- Runs in Google Colab (no local GPU needed)
- 100% free
- Inspired by xAI's Ani

### What's Missing
- Google Colab dependency
- Gemini API dependency
- Basic lip sync
- Small project

### Assessment
Notable for running without a GPU (via Colab) and voice cloning. The VRM + Three.js approach is correct but the implementation is basic.

---

## COMPARATIVE MATRIX

| Project | Stars | License | STT | TTS | LLM | Avatar Type | Lip Sync | GPU Agnostic | Docker | Local | Active |
|---------|-------|---------|-----|-----|-----|-------------|----------|-------------|--------|-------|--------|
| **Open-LLM-VTuber** | 5.9k | MIT | Many | Many | Many | Live2D | Built-in | Yes | Yes | Yes | Very |
| **Linly-Talker** | 3.1k | MIT | 3+ | 5+ | 6+ | Realistic TH | SadTalker/MuseTalk | No (CUDA) | Yes | Yes | Very |
| **OpenAvatarChat** | 3.1k | Apache 2.0 | 3+ | 3+ | 4+ | 3D (multiple) | MuseTalk/LiteAvatar | No (CUDA) | Yes | Yes | Very |
| **Amica** | 1.2k | MIT | 1 | 6+ | 7+ | VRM (3D) | Built-in | Yes | Yes | Yes | Active |
| **TalkingHead+HeadTTS** | 1.1k | MIT | No | HeadTTS | No | GLB/VRM | Best | Yes | Possible | Yes | Active |
| **Duix-Avatar** | 12.3k | Community | Yes | Yes | No | Video | Built-in | No (CUDA) | Yes | Yes | Active |
| **ProtoReplicant** | Small | OS | Yes | Yes | Yes | VRM | Audio | Yes | No | Partial | Low |
| **Vroid AI Companion** | Small | OS | No | Gemini | Gemini | VRM | FFT (3 shapes) | Yes | No | No | Low |
| **TalkMateAI** | Small | OS | Yes | Kokoro | Yes | TalkingHead | Kokoro native | Yes | No | Partial | New |
| **Pipecat** | Large | BSD-2 | Plugin | Plugin | Plugin | Plugin | Via plugins | Yes | Yes | Yes | Very |
| **LiveTalk-Unity** | Small | OS | No | SparkTTS | No | Realistic TH | MuseTalk | Partial | No | Yes | Active |

### Legend
- TH = Talking Head
- OS = Open Source (specific license not documented)
- Many = 5+ options available

---

## RECOMMENDED STARTING POINTS

### Strategy 1: Build on Open-LLM-VTuber (Backend) + Replace Frontend

**Approach:** Use Open-LLM-VTuber's excellent backend (STT/LLM/TTS with many options) and replace the Live2D frontend with a Three.js/VRM frontend using TalkingHead.

**Pros:**
- Most mature and well-maintained backend (5.9k stars)
- All STT/TTS/LLM options already integrated
- Voice interruption, long-term memory already implemented
- GPU-agnostic backend options (sherpa-onnx for STT, MeloTTS for TTS)
- MIT licensed

**Cons:**
- Requires custom frontend development
- Need to bridge Python backend to JavaScript frontend
- Live2D emotion system needs reimplementation for VRM

**Effort:** Medium-High

### Strategy 2: Extend Amica with Better Lip Sync

**Approach:** Fork Amica (already has VRM + LLM + TTS + STT) and improve the lip sync by integrating TalkingHead/HeadTTS or Lipsync-Engine.

**Pros:**
- Already has VRM avatars in browser
- Already integrates Ollama, Coqui, and many backends
- Docker support exists
- MIT licensed
- Emotion engine already built

**Cons:**
- Less actively maintained than Open-LLM-VTuber
- Fewer STT options
- Lip sync improvement requires significant work
- Less modular architecture

**Effort:** Medium

### Strategy 3: Compose from Best Components (Pipecat + TalkingHead)

**Approach:** Use Pipecat as the orchestration framework, HeadTTS for TTS+visemes, and TalkingHead for avatar rendering. Add STT and LLM via Pipecat plugins.

**Pros:**
- Each component is best-in-class
- Clean architecture from the start
- GPU-agnostic throughout
- All MIT/BSD licensed
- Strong community for each component
- Pipecat handles real-time streaming natively

**Cons:**
- Requires integration work
- No single project to fork
- Need to build the full stack
- More moving parts to maintain

**Effort:** High (but cleanest result)

### Strategy 4: Fork TalkMateAI

**Approach:** TalkMateAI already uses TalkingHead + Kokoro (HeadTTS) which is the recommended lip sync approach. Extend it with better STT and LLM options.

**Pros:**
- Already demonstrates the best lip sync approach
- VRM avatars with proper viseme support
- Vision capabilities included

**Cons:**
- Small/new project
- May need significant stabilization
- Less community support

**Effort:** Medium

### RECOMMENDED: Strategy 1 or Strategy 3

**For fastest results:** Strategy 1 (Open-LLM-VTuber backend + TalkingHead frontend)
- Leverages the most mature, well-tested backend
- Only the frontend needs custom work
- Everything runs locally

**For cleanest architecture:** Strategy 3 (Pipecat + TalkingHead + HeadTTS)
- Purpose-built from best components
- Most maintainable long-term
- Professional-grade orchestration via Pipecat

Both approaches meet all core requirements:
- GPU-agnostic (no CUDA dependency)
- VRM avatar support
- Real-time lip sync
- Fully open source (MIT/BSD)
- Local operation
- Containerizable

---

## SOURCES

### Primary GitHub Repositories
- Open-LLM-VTuber: https://github.com/Open-LLM-VTuber/Open-LLM-VTuber
- Linly-Talker: https://github.com/Kedreamix/Linly-Talker
- OpenAvatarChat: https://github.com/HumanAIGC-Engineering/OpenAvatarChat
- Amica: https://github.com/semperai/amica
- TalkingHead: https://github.com/met4citizen/TalkingHead
- HeadTTS: https://github.com/met4citizen/HeadTTS
- Duix-Avatar: https://github.com/duixcom/Duix-Avatar
- ProtoReplicant: https://github.com/OpenReplicant/ProtoReplicant
- Pipecat: https://github.com/pipecat-ai/pipecat
- NVIDIA ACE: https://github.com/NVIDIA/ACE
- NVIDIA Audio2Face-3D: https://github.com/NVIDIA/Audio2Face-3D
- AllTalk TTS: https://github.com/erew123/alltalk_tts
- TalkMateAI: https://github.com/kiranbaby14/TalkMateAI
- Vroid AI Companion: https://github.com/anjaydo/vroid-ai-companion
- AI Iris Avatar: https://github.com/Scthe/ai-iris-avatar
- LiveTalk-Unity: https://github.com/arghyasur1991/LiveTalk-Unity
- LLM-Based-3D-Avatar-Assistant: https://github.com/NeuralHarbour/LLM-Based-3D-Avatar-Assistant
- Realtime Avatar AI Companion: https://github.com/igna-s/Realtime_Avatar_AI_Companion
- Lipsync-Engine: https://github.com/Amoner/lipsync-engine
- wLipSync: https://github.com/mrxz/wLipSync
- Rhubarb Lip Sync: https://github.com/DanielSWolf/rhubarb-lip-sync
- Rhubarb WASM: https://github.com/danieloquelis/rhubarb-lip-sync-wasm
- AIAvatarKit: https://github.com/uezo/aiavatarkit

### HuggingFace
- NVIDIA Audio2Face-3D v3.0: https://huggingface.co/nvidia/Audio2Face-3D-v3.0

### Documentation & Websites
- Open-LLM-VTuber docs: https://open-llm-vtuber.github.io/en/
- Amica docs: https://docs.heyamica.com/
- OpenAvatarChat: https://www.openavatarchat.ai/
- Pipecat: https://www.pipecat.ai/
- NVIDIA ACE: https://developer.nvidia.com/ace-for-games
- Oculus Viseme Reference: https://developers.meta.com/horizon/documentation/unreal/audio-ovrlipsync-viseme-reference/
- ARKit Blendshapes: https://arkit-face-blendshapes.com/
