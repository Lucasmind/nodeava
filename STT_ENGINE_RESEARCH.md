# Speech-to-Text (STT) / Automatic Speech Recognition (ASR) Engine Research

**Date:** 2025-02-10
**Goal:** Identify the best open-source STT engine for a digital avatar project that runs fully local, is GPU-agnostic (AMD/Nvidia/Intel), containerizable, real-time streaming capable, accurate, and low-latency.

---

## Table of Contents

1. [Executive Summary & Recommendations](#executive-summary--recommendations)
2. [Master Comparison Matrix](#master-comparison-matrix)
3. [Detailed Engine Profiles](#detailed-engine-profiles)
4. [GPU Agnosticism Analysis](#gpu-agnosticism-analysis)
5. [Streaming & Real-Time Analysis](#streaming--real-time-analysis)
6. [VAD & End-of-Utterance Detection](#vad--end-of-utterance-detection)
7. [ONNX Runtime Ecosystem](#onnx-runtime-ecosystem)
8. [Architecture Decision](#architecture-decision)

---

## Executive Summary & Recommendations

### Top Recommendation: whisper.cpp + Silero VAD (via streaming wrapper)

For a digital avatar project requiring GPU-agnostic, containerized, real-time streaming STT:

| Priority | Engine | Role |
|----------|--------|------|
| **PRIMARY** | **whisper.cpp** (Vulkan backend) | Core ASR engine - works on AMD/Nvidia/Intel via Vulkan |
| **SECONDARY** | **Moonshine** (ONNX) | Lightweight alternative for ultra-low-latency edge scenarios |
| **FALLBACK** | **Vosk** | CPU-only fallback, native streaming, lowest resource usage |
| **VAD Layer** | **Silero VAD** | Voice activity detection, end-of-utterance detection |
| **Wrapper** | **RealtimeSTT** or **WhisperLive** | Real-time streaming orchestration with VAD integration |

### Why whisper.cpp Wins

1. **GPU-agnostic via Vulkan**: Works on AMD, Nvidia, AND Intel GPUs through the Vulkan API backend. No CUDA lock-in.
2. **Proven streaming**: Built-in `whisper-stream` example for real-time microphone transcription.
3. **Docker-ready**: Official Docker images including `main-vulkan` variant.
4. **Word-level timestamps**: Supported via `--max-len 1` and DTW-based alignment.
5. **VAD integration**: Built-in VAD support plus easy Silero VAD integration.
6. **Active maintenance**: Extremely active development by ggml-org (same team as llama.cpp).
7. **Accuracy**: Uses OpenAI Whisper models (large-v3 achieves ~7.4% WER on benchmarks).
8. **Quantization**: GGML quantization (Q4, Q5, Q8) reduces memory while preserving accuracy.
9. **MIT License**: Fully permissive for commercial use.

### Runner-Up: Moonshine (for ultra-low-latency scenarios)

If sub-100ms latency is critical (e.g., for very responsive avatar lip-sync):
- Moonshine processes 10s of audio in ~70ms
- MIT license for English models
- Native ONNX support (cross-platform inference)
- Built-in Silero VAD integration
- 5x faster than Whisper Tiny with comparable accuracy
- Runs on Raspberry Pi-class hardware

### When to Consider Alternatives

| Scenario | Best Choice |
|----------|-------------|
| Maximum accuracy (English only) | Parakeet TDT 0.6B v3 (6.05% WER) - but NVIDIA GPU only |
| Maximum accuracy (multilingual) | Whisper Large V3 via whisper.cpp |
| Lowest resource/CPU only | Vosk (50MB models, streaming native) |
| Best word-level timestamps for lip-sync | WhisperX (uses wav2vec2 forced alignment) |
| Emotion detection + ASR | SenseVoice (built-in emotion recognition) |

---

## Master Comparison Matrix

### Core Requirements Compliance

| Engine | License | Fully Local | GPU-Agnostic | Containerizable | Real-Time Streaming | Good Accuracy | Low Latency |
|--------|---------|-------------|--------------|-----------------|--------------------|--------------:|-------------|
| **whisper.cpp** | MIT | YES | YES (Vulkan) | YES | YES | YES (~7-8% WER) | GOOD |
| **faster-whisper** | MIT | YES | PARTIAL (CUDA+ROCm) | YES | LIMITED | YES (~7-8% WER) | VERY GOOD |
| **Whisper (OpenAI)** | MIT | YES | PARTIAL (CUDA+ROCm) | YES | NO (batch only) | YES (~7-8% WER) | POOR |
| **WhisperX** | BSD-4 | YES | NO (CUDA only) | YES | NO (batch only) | YES (~7-8% WER) | POOR |
| **distil-whisper** | MIT | YES | PARTIAL | YES | LIMITED | YES (~8% WER) | GOOD |
| **Vosk** | Apache 2.0 | YES | YES (CPU-based) | YES | YES (native) | FAIR (10-15% WER) | VERY GOOD |
| **DeepSpeech** | MPL 2.0 | YES | YES (CPU) | YES | LIMITED | POOR (outdated) | FAIR |
| **Coqui STT** | MPL 2.0 | YES | YES (CPU) | YES | LIMITED | POOR (outdated) | FAIR |
| **NeMo/Parakeet** | CC-BY-4.0 | YES | NO (CUDA only) | YES | YES | EXCELLENT (6% WER) | EXCELLENT |
| **NeMo/Canary** | CC-BY-4.0* | YES | NO (CUDA only) | YES | YES | EXCELLENT (5.6% WER) | GOOD |
| **Wav2Vec 2.0** | Apache 2.0 | YES | PARTIAL | YES | LIMITED | GOOD (~5% WER clean) | FAIR |
| **Moonshine** | MIT** | YES | YES (ONNX/CPU) | YES | YES | GOOD (~12% WER) | EXCELLENT |
| **SenseVoice** | MIT | YES | PARTIAL (ONNX available) | YES | PSEUDO | GOOD | EXCELLENT |
| **WhisperLive** | MIT | YES | PARTIAL*** | YES | YES | YES (uses Whisper) | GOOD |
| **RealtimeSTT** | MIT | YES | PARTIAL (CUDA preferred) | PARTIAL | YES | YES (uses Whisper) | VERY GOOD |
| **speech_recognition** | BSD-3 | YES**** | Depends on backend | YES | NO | Depends on backend | Depends |

\* Canary-1B is CC-BY-NC-4.0; Canary-1B-Flash is CC-BY-4.0
\** MIT for English models; Moonshine Community License (non-commercial) for other languages
\*** WhisperLive supports OpenVINO (Intel GPU) and faster-whisper (CPU/CUDA)
\**** Offline via Vosk/Whisper/PocketSphinx backends only

### Technical Capabilities

| Engine | ONNX Support | CPU Only | AMD GPU | Intel GPU | Word Timestamps | VAD Built-in | End-of-Utterance | Docker Ready |
|--------|:------------:|:--------:|:-------:|:---------:|:---------------:|:------------:|:----------------:|:------------:|
| **whisper.cpp** | NO (GGML) | YES | YES (Vulkan) | YES (Vulkan) | YES (DTW/max-len) | YES | YES (VAD-based) | YES |
| **faster-whisper** | NO (CT2) | YES | PARTIAL (ROCm) | NO | YES | YES (Silero) | YES (Silero) | YES |
| **Whisper (OpenAI)** | NO (PyTorch) | YES | YES (ROCm) | NO | YES | NO | NO | YES |
| **WhisperX** | NO (PyTorch) | Slow | NO | NO | YES (best) | YES (Silero) | YES | YES |
| **distil-whisper** | YES | YES | Via ONNX | Via ONNX | YES | NO | NO | YES |
| **Vosk** | NO (Kaldi) | YES | N/A (CPU) | N/A (CPU) | YES | NO | YES (endpoint rules) | YES |
| **DeepSpeech** | NO (TFLite) | YES | N/A | N/A | NO | NO | NO | YES |
| **Coqui STT** | NO (TFLite) | YES | N/A | N/A | NO | NO | NO | YES |
| **NeMo/Parakeet** | YES (sherpa) | YES (slow) | NO | NO | YES | NO (external) | Via streaming | YES |
| **NeMo/Canary** | Partial | YES (slow) | NO | NO | YES (flash models) | NO (external) | Via streaming | YES |
| **Wav2Vec 2.0** | YES (export) | YES | Via ONNX | Via ONNX | PARTIAL | NO | NO | PARTIAL |
| **Moonshine** | YES (native) | YES | Via ONNX | Via ONNX | NO (native) | YES (Silero) | YES (Silero) | PARTIAL |
| **SenseVoice** | YES (native) | YES | Via ONNX | Via ONNX | PARTIAL* | YES (FunASR) | YES (FunASR) | PARTIAL |
| **WhisperLive** | Via backends | YES | NO | YES (OpenVINO) | Via backends | YES | YES | YES |
| **RealtimeSTT** | NO | YES | NO | NO | Via faster-whisper | YES (Silero+WebRTC) | YES | PARTIAL |

\* OmniSenseVoice variant adds word timestamps

---

## Detailed Engine Profiles

### 1. OpenAI Whisper (Original)

- **Repository**: https://github.com/openai/whisper
- **License**: MIT
- **Architecture**: Encoder-decoder Transformer
- **Models**: tiny (39M), base (74M), small (244M), medium (769M), large-v3 (1.55B), large-v3-turbo (809M)
- **GPU**: CUDA (Nvidia), ROCm (AMD with manual setup). No Intel GPU. CPU works but slow.
- **ONNX**: Not natively; can be exported
- **Streaming**: NO - batch/file processing only. Not designed for real-time.
- **Word Timestamps**: YES (via `--word_timestamps` flag)
- **VAD**: NO built-in
- **WER**: ~7.4% average on Open ASR Leaderboard (large-v3)
- **Latency**: HIGH - processes 30-second chunks, significant overhead
- **Docker**: Community images available
- **Maintenance**: Active (OpenAI)
- **Verdict**: Great model, poor for real-time. Use via optimized frontends instead.

### 2. whisper.cpp (GGML C++ Port)

- **Repository**: https://github.com/ggml-org/whisper.cpp
- **License**: MIT
- **Architecture**: Same Whisper models, ported to C/C++ with GGML tensor library
- **GPU Backends**:
  - **Vulkan**: AMD, Nvidia, Intel - any GPU with Vulkan driver support. 3-4x speedup over CPU on integrated graphics. 12x boost reported on Whisper.cpp 1.8.3.
  - **CUDA**: Nvidia GPUs (fastest path for Nvidia)
  - **Metal**: Apple Silicon
  - **OpenCL**: Legacy support
  - **SYCL**: Intel oneAPI
- **CPU**: YES - x86_64, ARM64, WASM
- **ONNX**: NO (uses GGML format with quantization: Q4_0, Q4_1, Q5_0, Q5_1, Q8_0, F16, F32)
- **Streaming**: YES - `whisper-stream` example for live microphone transcription
- **Word Timestamps**: YES
  - Via `--max-len 1` flag (splits output at word boundaries)
  - Via DTW (Dynamic Time Warping) on cross-attention weights (`--dtw` flag, v1.0.55+)
  - Token-level timestamps with configurable probability thresholds
- **VAD**: YES (built-in since recent versions)
  - Uses VAD model to detect speech segments before passing to Whisper
  - Configurable min speech duration, min silence duration, max speech duration
  - Silero VAD integration available via external tools
- **WER**: Same as Whisper models (~7-8% WER with large-v3)
- **Latency**: GOOD - C++ native performance, quantized models, GPU acceleration
  - tiny model: near real-time on CPU
  - base/small models: real-time with GPU
  - large-v3: real-time with discrete GPU
- **Docker**: YES
  - `ghcr.io/ggml-org/whisper.cpp:main` (CPU)
  - `ghcr.io/ggml-org/whisper.cpp:main-vulkan` (Vulkan GPU)
  - `ghcr.io/ggml-org/whisper.cpp:main-cuda` (CUDA)
  - Community ROCm images available
- **Maintenance**: VERY ACTIVE (ggml-org, same team as llama.cpp)
- **Verdict**: BEST CHOICE for GPU-agnostic, containerized, real-time STT.

### 3. faster-whisper (CTranslate2)

- **Repository**: https://github.com/SYSTRAN/faster-whisper
- **License**: MIT
- **Architecture**: Whisper models converted to CTranslate2 format
- **GPU**: CUDA (primary), ROCm (via community CTranslate2-rocm fork), CPU. No Intel GPU.
- **ONNX**: NO (CTranslate2 format). Community fork `faster-whisper-onnx` exists.
- **Streaming**: LIMITED - Not natively streaming. Can be wrapped with tools like whisper_streaming or WhisperLive for pseudo-streaming.
- **Word Timestamps**: YES (`word_timestamps=True` parameter)
- **VAD**: YES (built-in Silero VAD integration, filters silence >2s by default, configurable)
- **WER**: Same as Whisper (~7-8% WER) with 4x speed improvement
- **Latency**: VERY GOOD - 4x faster than OpenAI Whisper, 8-bit quantization on CPU and GPU
- **Docker**: YES - `linuxserver/faster-whisper` and community images
- **Maintenance**: Active (SYSTRAN)
- **Verdict**: Excellent for NVIDIA-focused deployments. ROCm support is experimental.

### 4. WhisperX

- **Repository**: https://github.com/m-bain/whisperX
- **License**: BSD-4-Clause
- **Architecture**: Whisper + wav2vec2 forced alignment + speaker diarization
- **GPU**: CUDA only (requires CUDA toolkit 12.x)
- **ONNX**: NO
- **Streaming**: NO - designed for batch processing of files
- **Word Timestamps**: BEST in class - uses wav2vec2 phoneme-level forced alignment for precise word boundaries. Critical for lip-sync applications.
- **VAD**: YES (Silero VAD for speech segmentation)
- **WER**: Same as Whisper + better timestamp accuracy
- **Latency**: POOR for real-time (batch processing, 60-70x realtime throughput)
- **Docker**: YES (community images)
- **Maintenance**: Active (community)
- **Verdict**: Best word-level timestamps for lip-sync, but not suitable for real-time streaming. Could be used as a post-processing step.

### 5. distil-whisper

- **Repository**: https://github.com/huggingface/distil-whisper
- **License**: MIT
- **Models**: distil-large-v3 (756M), distil-large-v3.5, distil-medium.en
- **Architecture**: Knowledge-distilled Whisper (fewer decoder layers)
- **GPU**: Same as Whisper (CUDA, ROCm)
- **ONNX**: YES - `distil-whisper/distil-large-v3.5-ONNX` available on HuggingFace
- **Streaming**: LIMITED - compatible with sequential long-form algorithm (sliding window)
- **Word Timestamps**: YES (inherits from Whisper)
- **VAD**: NO built-in
- **WER**: Within 1% of Whisper large-v3 (~8% WER)
- **Latency**: GOOD - 6x faster than large-v3, 50% smaller
- **Docker**: Via HuggingFace ecosystem
- **Maintenance**: Active (Hugging Face)
- **Verdict**: Good compromise of speed/accuracy. ONNX availability is a plus for cross-platform.

### 6. Vosk

- **Repository**: https://github.com/alphacep/vosk-api
- **License**: Apache 2.0
- **Architecture**: Kaldi-based (traditional ASR pipeline)
- **Models**: Small (50MB) to large server models. 20+ languages.
- **GPU**: CPU-primary. GPU-accelerated Kaldi server available (CUDA) but CPU models are the strength.
- **ONNX**: NO (Kaldi format)
- **Streaming**: YES - native streaming API. Zero-latency response. WebSocket, gRPC, MQTT, WebRTC servers.
- **Word Timestamps**: YES (JSON output with word-level start/end times and confidence)
- **VAD**: NO built-in (relies on endpoint detection)
- **End-of-Utterance**: YES
  - Configurable endpoint rules: `min-trailing-silence`, `max-speech-duration`
  - `SetEndpointerDelays()` for fine-grained control
  - Silence timeout detection (typically 0.5-1.0s)
- **WER**: FAIR - 10-15% WER depending on model. Prioritizes speed over accuracy.
- **Latency**: EXCELLENT - designed for real-time, runs on Raspberry Pi
- **Docker**: YES - `alphacep/kaldi-vosk-server`, `alphacep/kaldi-vosk-server-gpu`
- **Maintenance**: Active (Alpha Cephei)
- **Languages**: Python, Java, Node.JS, C#, C++, Rust, Go, and more
- **Verdict**: Best CPU-only fallback. Native streaming with endpoint detection. Lower accuracy than Whisper-family.

### 7. Mozilla DeepSpeech

- **Repository**: https://github.com/mozilla/DeepSpeech
- **License**: MPL 2.0
- **Status**: DISCONTINUED (2021). 16,100 GitHub stars. No active development.
- **Architecture**: RNN-based (LSTM)
- **GPU**: CPU and CUDA
- **ONNX**: NO (TensorFlow Lite)
- **Streaming**: LIMITED
- **Word Timestamps**: NO
- **VAD**: NO
- **WER**: Outdated - significantly behind modern models
- **Verdict**: DO NOT USE for new projects. Historical significance only.

### 8. Coqui STT

- **Repository**: https://github.com/coqui-ai/STT
- **License**: MPL 2.0
- **Status**: DISCONTINUED. Coqui company shut down December 2023, services offline January 2024.
- **Architecture**: DeepSpeech fork with improvements
- **GPU**: CPU and CUDA
- **Verdict**: DO NOT USE for new projects. Company and active development ceased.

### 9. NVIDIA NeMo / Parakeet

- **Repository**: https://github.com/NVIDIA-NeMo/NeMo
- **License**: CC-BY-4.0 (Parakeet models)
- **Models**:
  - Parakeet-TDT-0.6B-v3 (600M params, English only)
  - Parakeet-TDT-1.1B (1.1B params)
  - Parakeet-CTC, Parakeet-RNNT variants
- **Architecture**: FastConformer encoder + TDT/CTC/RNNT decoder
- **GPU**: CUDA ONLY. Designed for NVIDIA GPUs. No AMD/Intel GPU support.
- **ONNX**: YES - available via sherpa-onnx (including INT8 quantized). Community ONNX exports on HuggingFace.
- **Streaming**: YES - RNN-Transducer architecture enables streaming. Dedicated streaming inference script.
- **Word Timestamps**: YES - enabled by default for char, word, and segment levels
- **VAD**: NO built-in (external VAD required)
- **WER**: EXCELLENT
  - Parakeet-TDT-0.6B-v3: ~6.05% WER average (Open ASR Leaderboard)
  - First model to achieve <7.0% average WER
  - RTFx >2,000 (extremely fast)
- **Latency**: EXCELLENT (64% faster than Parakeet-RNNT, RTFx >2000)
- **Docker**: YES - NVIDIA provides NeMo Docker containers
- **Maintenance**: VERY ACTIVE (NVIDIA)
- **Verdict**: BEST ACCURACY for English STT, but CUDA-only. Use via ONNX export on sherpa-onnx for cross-platform CPU inference.

### 10. NVIDIA NeMo / Canary

- **Repository**: https://github.com/NVIDIA-NeMo/NeMo
- **License**:
  - Canary-1B: CC-BY-NC-4.0 (non-commercial)
  - Canary-1B-Flash: CC-BY-4.0 (commercial OK)
  - Canary-Qwen-2.5B: CC-BY-4.0
- **Architecture**: FastConformer Encoder + Transformer Decoder
- **GPU**: CUDA ONLY
- **ONNX**: Partial (via sherpa-onnx for some variants)
- **Streaming**: YES - chunked and streaming decoding with Wait-k and AlignAtt policies
- **Word Timestamps**: YES (experimental, Flash models support English/German/French/Spanish)
- **VAD**: NO built-in
- **WER**: BEST - Canary-Qwen-2.5B achieves 5.63% WER (#1 on Open ASR Leaderboard)
- **Multilingual**: 25 EU languages + translation
- **Docker**: YES (NeMo containers)
- **Maintenance**: VERY ACTIVE
- **Verdict**: Highest accuracy available, but CUDA-locked and large model.

### 11. Wav2Vec 2.0 (Meta)

- **Repository**: https://github.com/facebookresearch/fairseq
- **License**: Apache 2.0 (MIT for some model variants)
- **Architecture**: Self-supervised Transformer (contrastive learning)
- **GPU**: CUDA (PyTorch), CPU possible
- **ONNX**: YES (can export Wav2VecForCTC from HuggingFace to ONNX)
- **Streaming**: LIMITED - wav2vec-S (ACL 2024) adds streaming adaptation, but not production-ready
- **Word Timestamps**: PARTIAL - not native, requires post-processing. Used by WhisperX for forced alignment.
- **VAD**: NO
- **WER**: EXCELLENT on clean audio (1.8% clean / 3.3% other on LibriSpeech with all labeled data). ~37% on noisy benchmarks.
- **Latency**: FAIR - designed for batch processing
- **Docker**: Community images
- **Maintenance**: LOW (Meta shifted focus to newer models)
- **Verdict**: Best used as an alignment tool (via WhisperX) rather than primary ASR. Brittle on noisy audio.

### 12. Moonshine (Useful Sensors / Moonshine AI)

- **Repository**: https://github.com/moonshine-ai/moonshine
- **License**: MIT (English models + inference code), Moonshine Community License (non-commercial, other languages)
- **Architecture**: Encoder-decoder Transformer with RoPE (Rotary Position Embedding), variable-length encoder
- **Models**: Tiny (~27M), Base (~61M), plus specialized variants
- **GPU**: CPU-primary (designed for edge). ONNX Runtime for acceleration.
- **ONNX**: YES (native, primary deployment format). `onnx-community/moonshine-tiny-ar-ONNX` on HuggingFace.
- **Streaming**: YES - designed for live transcription. VAD-triggered segment processing.
- **Word Timestamps**: NO native word-level timestamps (segment-level only)
- **VAD**: YES - uses Silero VAD for speech detection in streaming mode
- **WER**: GOOD
  - Moonshine Tiny: ~12.81% (comparable to Whisper Tiny at 12.66%)
  - Moonshine Base: lower WER, outperforms Whisper Small in some benchmarks
  - Specialized models achieve 48% lower error than Whisper Tiny
- **Latency**: EXCELLENT
  - 5x faster than Whisper Tiny on 10s audio
  - 70ms to process 10 seconds of audio (for SenseVoice-class speed)
  - Variable-length encoder avoids zero-padding overhead
- **Docker**: PARTIAL (portable C++ core, ONNX Runtime based - easy to containerize)
- **Maintenance**: Active (Moonshine AI, formerly Useful Sensors)
- **Verdict**: Excellent for ultra-low-latency edge scenarios. ONNX-native means cross-platform GPU via DirectML/OpenVINO. Lower accuracy than Whisper large models.

### 13. SenseVoice (Alibaba FunAudioLLM)

- **Repository**: https://github.com/FunAudioLLM/SenseVoice
- **License**: MIT (code); model license via FunAudioLLM
- **Architecture**: Non-autoregressive end-to-end (Paraformer-based)
- **Models**: SenseVoice-Small (primary), trained on 400K+ hours
- **GPU**: CUDA (primary), CPU
- **ONNX**: YES - official ONNX export via FunASR (`funasr-onnx-0.4.0`). GGML port also available.
- **Streaming**: PSEUDO - Streaming-SenseVoice uses chunked inference with truncated attention. Not true streaming.
- **Word Timestamps**: PARTIAL - OmniSenseVoice variant provides word timestamps
- **VAD**: YES - FunASR includes VAD module
- **Unique Features**:
  - Speech Emotion Recognition (SER) - detects happy, sad, angry, neutral
  - Audio Event Detection (AED) - detects laughter, applause, music, etc.
  - Language Identification (LID) - 50+ languages
- **WER**: GOOD - surpasses Whisper on Chinese/Cantonese. Competitive on English.
- **Latency**: EXCELLENT - 70ms for 10 seconds of audio (15x faster than Whisper-Large)
- **Docker**: Via FunASR ecosystem
- **Maintenance**: Active (Alibaba DAMO Academy)
- **Deployment**: sherpa-onnx supports SenseVoice across 10 programming languages, iOS, Android, Raspberry Pi
- **Verdict**: Unique multi-modal capabilities (emotion + events). Great for avatar emotion detection. ONNX availability is strong.

### 14. WhisperLive (Collabora)

- **Repository**: https://github.com/collabora/WhisperLive
- **License**: MIT
- **Architecture**: Streaming wrapper around multiple Whisper backends
- **Backends**:
  - `faster_whisper` - CPU/CUDA
  - `tensorrt` - NVIDIA GPUs (highest throughput)
  - `openvino` - Intel CPUs and iGPU/dGPU
- **GPU**: CUDA (TensorRT), Intel (OpenVINO), CPU (faster_whisper). NO AMD GPU.
- **Streaming**: YES - real-time from microphone, files, RTSP, HLS streams
- **VAD**: YES (optional)
- **Word Timestamps**: Via backend capabilities
- **Docker**: YES - Docker images for each backend, GPU auto-detection
- **Maintenance**: Active (Collabora)
- **Verdict**: Good turnkey streaming solution. Intel GPU support via OpenVINO is notable. No AMD GPU path.

### 15. RealtimeSTT (KoljaB)

- **Repository**: https://github.com/KoljaB/RealtimeSTT
- **License**: MIT
- **Architecture**: High-level Python wrapper around faster-whisper with VAD
- **GPU**: CUDA preferred, CPU fallback
- **Streaming**: YES - designed specifically for real-time microphone transcription
- **VAD**: YES - EXCELLENT VAD integration
  - Silero VAD for end-of-speech detection
  - WebRTC VAD for voice activity detection
  - faster-whisper built-in VAD filter
  - All callbacks are async via helper threads
- **Wake Word**: YES (Openwakeword integration)
- **End-of-Utterance**: YES - robust silence/speech boundary detection
- **Word Timestamps**: Via faster-whisper backend
- **Docker**: PARTIAL (Python package, needs containerization)
- **Maintenance**: Active
- **Verdict**: Best high-level real-time STT library for Python. Excellent VAD/end-of-utterance. But CUDA-focused.

### 16. speech_recognition (Python Library)

- **Repository**: https://github.com/Uberi/speech_recognition
- **License**: BSD-3-Clause
- **Architecture**: Wrapper library supporting multiple backends
- **Offline Backends**: Vosk, Whisper, PocketSphinx (CMU Sphinx)
- **Online Backends**: Google, Azure, AWS, IBM Watson, etc.
- **Streaming**: NO (processes audio chunks, not true streaming)
- **Verdict**: Useful for prototyping. Not suitable for production real-time applications. Use specific engines directly.

---

## GPU Agnosticism Analysis

### GPU Backend Support Matrix

| Backend Technology | Nvidia | AMD | Intel | Notes |
|-------------------|:------:|:---:|:-----:|-------|
| **CUDA** | YES | NO | NO | Fastest for Nvidia. Most engines default to this. |
| **ROCm/HIP** | NO | YES | NO | AMD's CUDA equivalent. Requires separate builds. |
| **Vulkan** | YES | YES | YES | Cross-vendor. Used by whisper.cpp. 3-12x over CPU. |
| **OpenVINO** | NO | NO | YES | Intel-optimized. Used by WhisperLive. |
| **ONNX Runtime (CUDA EP)** | YES | NO | NO | ONNX with CUDA execution provider |
| **ONNX Runtime (DirectML EP)** | YES | YES | YES | Windows only. Cross-vendor via DirectX 12. |
| **ONNX Runtime (CPU)** | YES | YES | YES | Universal fallback. Decent performance. |
| **SYCL/oneAPI** | NO | NO | YES | Intel's compute framework. whisper.cpp supports it. |
| **Metal** | NO | NO | NO | Apple Silicon only. |

### Engines That Work on ALL THREE GPU Vendors

Only these engines can run accelerated on AMD, Nvidia, AND Intel GPUs:

1. **whisper.cpp** (via Vulkan backend) - RECOMMENDED
2. **Moonshine** (via ONNX Runtime + DirectML on Windows, or CPU cross-platform)
3. **distil-whisper** (via ONNX Runtime + DirectML on Windows)
4. **SenseVoice** (via ONNX Runtime / sherpa-onnx)
5. **Vosk** (CPU-only, but runs everywhere)
6. **Parakeet** (via sherpa-onnx ONNX export, CPU inference only for non-NVIDIA)

### Linux GPU-Agnostic Strategy

On Linux (Docker/Podman), the options narrow:
- **Vulkan** is the only truly cross-vendor GPU API on Linux
- **whisper.cpp with Vulkan** is the only production-ready option for all three GPU vendors on Linux
- ONNX Runtime on Linux supports CUDA EP (Nvidia) and ROCm EP (AMD) but NOT DirectML
- For Intel on Linux: OpenVINO or SYCL

**Recommended architecture for maximum portability:**
```
Docker Container
  |
  +-- whisper.cpp (primary engine)
  |     |
  |     +-- Vulkan backend (auto-detected: AMD/Nvidia/Intel)
  |     +-- CUDA backend (if Nvidia detected)
  |     +-- CPU fallback
  |
  +-- Silero VAD (ONNX, CPU - lightweight)
  |
  +-- Streaming orchestration layer
```

---

## Streaming & Real-Time Analysis

### True Streaming vs. Pseudo-Streaming

| Type | Description | Engines |
|------|-------------|---------|
| **True Streaming** | Processes audio continuously, outputs words as they arrive | Vosk, Parakeet (RNNT/TDT), sherpa-onnx streaming models |
| **Chunked Streaming** | Processes audio in small chunks (0.5-2s), outputs after each chunk | whisper.cpp stream, WhisperLive, Moonshine, RealtimeSTT |
| **Pseudo-Streaming** | Processes accumulated audio, outputs delta of new text | faster-whisper with wrappers, whisper_streaming |
| **Batch Only** | Processes complete files/segments | Whisper (OpenAI), WhisperX |

### Latency Comparison for Real-Time Conversation

| Engine | Typical Latency | Notes |
|--------|----------------|-------|
| **Vosk** | 100-200ms | Native streaming, lowest latency |
| **Moonshine Tiny** | ~70ms per 10s segment | Ultra-fast but segment-based |
| **SenseVoice-Small** | ~70ms per 10s segment | Very fast, segment-based |
| **whisper.cpp (tiny/base)** | 200-500ms | Chunked streaming mode |
| **whisper.cpp (small)** | 300-800ms | With Vulkan GPU acceleration |
| **faster-whisper** | 200-600ms | Depends on model size and GPU |
| **Parakeet TDT** | <100ms | True streaming but CUDA only |
| **RealtimeSTT** | 300-800ms | Includes VAD processing overhead |
| **WhisperLive** | 300-1000ms | Depends on backend |
| **Whisper (OpenAI)** | 3-10s | 30-second chunk processing |
| **WhisperX** | 5-15s | Batch + alignment pipeline |

### For Digital Avatar Conversation

Target latency: <500ms for natural conversation feel.

**Recommended streaming architecture:**
```
Microphone Input
     |
     v
  Silero VAD (detect speech start/stop)
     |
     +-- Speech detected --> Buffer audio
     |
     +-- Silence detected (end of utterance) --> Process buffered audio
          |
          v
       whisper.cpp (small/medium model with Vulkan GPU)
          |
          v
       Transcription text --> Send to LLM / Avatar controller
```

For word-by-word streaming (words appear while speaking):
```
Microphone Input
     |
     v
  Continuous chunked processing (whisper.cpp --stream mode)
     |
     +-- Every 200-500ms, process accumulated audio
     +-- Output delta (new words since last chunk)
     +-- On silence: finalize and emit complete utterance
```

---

## VAD & End-of-Utterance Detection

### Why VAD Matters for Digital Avatars

1. **Know when user starts speaking** - trigger listening animation
2. **Know when user stops speaking** - trigger processing/thinking animation, send to LLM
3. **Filter background noise** - avoid false transcription triggers
4. **Reduce compute** - only run ASR on speech segments

### VAD Solutions Comparison

| VAD Solution | License | Latency | Accuracy | Integration |
|-------------|---------|---------|----------|-------------|
| **Silero VAD** | MIT | <50ms | EXCELLENT | PyTorch/ONNX, widely supported |
| **WebRTC VAD** | BSD | <10ms | GOOD | C library, very lightweight |
| **whisper.cpp built-in** | MIT | Varies | GOOD | Integrated, configurable |
| **FunASR VAD** | MIT | <50ms | EXCELLENT | Part of SenseVoice ecosystem |
| **Kaldi/Vosk endpointer** | Apache 2.0 | <100ms | GOOD | Integrated in Vosk |

### Recommended VAD Stack

**Primary: Silero VAD (ONNX)**
- MIT license, pre-trained, enterprise-grade
- Works on CPU with ONNX Runtime (no GPU needed)
- 50ms latency
- Configurable thresholds for speech start/end
- Used by: RealtimeSTT, Moonshine, WhisperX, faster-whisper

**Configuration for conversation:**
```
min_speech_duration_ms: 250    # Ignore very short sounds
min_silence_duration_ms: 500   # Wait 500ms of silence before "end of utterance"
speech_pad_ms: 200             # Pad speech segments by 200ms
threshold: 0.5                 # Speech probability threshold
```

---

## ONNX Runtime Ecosystem

### Why ONNX Matters

ONNX Runtime is the most GPU-agnostic inference engine:
- **CUDA EP**: Nvidia GPUs
- **ROCm EP**: AMD GPUs (Linux)
- **DirectML EP**: AMD + Nvidia + Intel GPUs (Windows)
- **OpenVINO EP**: Intel CPUs/GPUs
- **CPU EP**: Universal fallback

### Engines with ONNX Models Available

| Engine | ONNX Model Available | Source |
|--------|---------------------|--------|
| **distil-whisper** | YES (official) | `distil-whisper/distil-large-v3.5-ONNX` on HuggingFace |
| **Moonshine** | YES (native/primary) | `onnx-community/moonshine-tiny-ar-ONNX` on HuggingFace |
| **SenseVoice** | YES (official) | Via FunASR ONNX export, sherpa-onnx |
| **Parakeet TDT** | YES (community) | Via sherpa-onnx, INT8 quantized available |
| **Canary** | Partial | Some variants via sherpa-onnx |
| **Wav2Vec 2.0** | YES (exportable) | Export from HuggingFace Transformers |
| **Whisper** | YES (exportable) | Via Optimum/ONNX export tools |

### sherpa-onnx: The Cross-Platform ONNX Hub

**Repository**: https://github.com/k2-fsa/sherpa-onnx

sherpa-onnx is a critical piece of the ecosystem:
- Runs ONNX models for STT, TTS, VAD, speaker diarization
- 12 programming languages: C++, C, Python, C#, Go, Swift, Kotlin, Java, JavaScript, Dart
- Platforms: Linux, macOS, Windows, Android, iOS, Raspberry Pi, RISC-V
- Models supported: Whisper, Paraformer, Zipformer, SenseVoice, NeMo Transducer
- Streaming and non-streaming modes
- **Limitation**: GPU acceleration currently CUDA-only. CPU for other platforms.

---

## Architecture Decision

### Recommended Architecture for Digital Avatar STT

```
+--------------------------------------------------+
|            Docker/Podman Container                |
|                                                   |
|  +---------------------------------------------+ |
|  |          Streaming Orchestrator              | |
|  |  (WebSocket server for audio input)          | |
|  +---------------------------------------------+ |
|           |                    |                   |
|  +----------------+  +---------------------+      |
|  | Silero VAD     |  | whisper.cpp         |      |
|  | (ONNX, CPU)    |  | (Vulkan/CUDA/CPU)   |      |
|  |                |  |                     |      |
|  | - Speech start |  | - ASR inference     |      |
|  | - Speech end   |  | - Word timestamps   |      |
|  | - Noise filter |  | - Model: small/med  |      |
|  +----------------+  +---------------------+      |
|           |                    |                   |
|  +---------------------------------------------+ |
|  |          Output API                          | |
|  |  - Streaming partial transcripts             | |
|  |  - Final utterance text                      | |
|  |  - Word timestamps (for lip-sync)            | |
|  |  - VAD events (speaking/silent)              | |
|  +---------------------------------------------+ |
+--------------------------------------------------+
```

### Model Selection Guide

| GPU Available | Recommended Model | Expected Performance |
|--------------|-------------------|---------------------|
| Nvidia (8GB+ VRAM) | whisper-large-v3-turbo (CUDA) | ~7.75% WER, real-time |
| Nvidia (4GB VRAM) | whisper-small (CUDA) | ~9% WER, real-time |
| AMD discrete | whisper-small (Vulkan) | ~9% WER, real-time |
| Intel discrete/iGPU | whisper-small (Vulkan) | ~9% WER, real-time |
| CPU only | whisper-base or Moonshine Tiny | ~12% WER, near real-time |
| Raspberry Pi / Edge | Moonshine Tiny (ONNX) or Vosk | ~12-15% WER |

### Future-Proof Considerations

1. **Parakeet ONNX models via sherpa-onnx**: As ONNX Runtime adds better cross-GPU support, Parakeet's 6% WER could become accessible on AMD/Intel.
2. **Moonshine evolution**: The Moonshine project is rapidly improving. Watch for larger models with word timestamps.
3. **SenseVoice for emotion**: If the avatar needs to detect user emotion, SenseVoice's built-in SER is unique and valuable.
4. **whisper.cpp Vulkan maturation**: Vulkan backend is relatively new (~2024). Performance will improve.

### Implementation Priority

1. **Phase 1**: whisper.cpp with Vulkan in Docker, Silero VAD, basic streaming
2. **Phase 2**: Add word-level timestamps (DTW mode) for lip-sync alignment
3. **Phase 3**: Evaluate Moonshine as low-latency alternative for quick responses
4. **Phase 4**: Consider SenseVoice integration for emotion-aware avatar responses

---

## Sources

### Primary Engine Repositories
- OpenAI Whisper: https://github.com/openai/whisper
- whisper.cpp: https://github.com/ggml-org/whisper.cpp
- faster-whisper: https://github.com/SYSTRAN/faster-whisper
- WhisperX: https://github.com/m-bain/whisperX
- distil-whisper: https://github.com/huggingface/distil-whisper
- Vosk: https://github.com/alphacep/vosk-api
- Mozilla DeepSpeech: https://github.com/mozilla/DeepSpeech
- NVIDIA NeMo: https://github.com/NVIDIA-NeMo/NeMo
- Wav2Vec 2.0 (fairseq): https://github.com/facebookresearch/fairseq
- Moonshine: https://github.com/moonshine-ai/moonshine
- SenseVoice: https://github.com/FunAudioLLM/SenseVoice
- WhisperLive: https://github.com/collabora/WhisperLive
- RealtimeSTT: https://github.com/KoljaB/RealtimeSTT
- speech_recognition: https://github.com/Uberi/speech_recognition
- sherpa-onnx: https://github.com/k2-fsa/sherpa-onnx
- Silero VAD: https://github.com/snakers4/silero-vad

### Benchmark & Comparison Sources
- Northflank STT Benchmarks 2026: https://northflank.com/blog/best-open-source-speech-to-text-stt-model-in-2026-benchmarks
- Modal Open Source STT 2025: https://modal.com/blog/open-source-stt
- AssemblyAI Top 8 Open Source STT 2025: https://www.assemblyai.com/blog/top-open-source-stt-options-for-voice-applications
- Ionio Edge STT Benchmark 2025: https://research.ionio.ai/posts/2025/edge-stt-model-benchmark
- HuggingFace Open ASR Leaderboard: https://huggingface.co/spaces/hf-audio/open_asr_leaderboard

### Technical References
- whisper.cpp Vulkan 12x boost: https://www.phoronix.com/news/Whisper-cpp-1.8.3-12x-Perf
- CTranslate2 on AMD GPUs (ROCm): https://rocm.blogs.amd.com/artificial-intelligence/ctranslate2/README.html
- ONNX Runtime DirectML: https://onnxruntime.ai/docs/execution-providers/DirectML-ExecutionProvider.html
- AMD DirectML Guide: https://gpuopen.com/learn/onnx-directlml-execution-provider-guide-part1/
- Moonshine paper: https://arxiv.org/abs/2410.15608
- NVIDIA Parakeet TDT blog: https://developer.nvidia.com/blog/turbocharge-asr-accuracy-and-speed-with-nvidia-nemo-parakeet-tdt/
- Parakeet TDT 0.6B v3 model: https://huggingface.co/nvidia/parakeet-tdt-0.6b-v3
- Canary 1B v2 model: https://huggingface.co/nvidia/canary-1b-v2
- distil-whisper ONNX: https://huggingface.co/distil-whisper/distil-large-v3.5-ONNX
