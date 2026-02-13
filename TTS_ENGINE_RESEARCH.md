# Open-Source Text-to-Speech (TTS) Engine Research Report

**Date:** 2026-02-10
**Objective:** Identify fully local, GPU-agnostic, containerizable, high-quality, open-source TTS engines suitable for real-time conversational use in a digital avatar project.

---

## Executive Summary

After extensive research across 17 open-source TTS engines, the following emerge as the strongest candidates for a GPU-agnostic, containerized, real-time digital avatar pipeline:

| Rank | Engine | Why |
|------|--------|-----|
| 1 | **Kokoro TTS** | Apache 2.0, native ONNX, 82M params, < 0.3s latency, viseme support via HeadTTS, runs on CPU |
| 2 | **Piper TTS** | MIT/GPL, native ONNX, ultra-fast on CPU, mature ecosystem, phoneme maps available |
| 3 | **MeloTTS** | MIT, real-time on CPU, Dockerfile included, ONNX PR in progress, multi-lingual |
| 4 | **F5-TTS** | CC-BY-NC-SA (weights), ONNX port exists, zero-shot voice cloning, ROCm support |
| 5 | **Orpheus TTS** | Apache 2.0, streaming ~100ms TTFB, emotion tags, voice cloning, but CUDA-focused |

**Best for GPU-agnostic deployment:** Kokoro (ONNX) > Piper (ONNX) > MeloTTS (CPU)
**Best quality:** Sesame CSM > Orpheus > F5-TTS > Dia > StyleTTS 2
**Best for lip sync / visemes:** Kokoro (via HeadTTS) > Piper (phoneme maps) > VITS/VITS2 (ONNX phoneme data)

---

## Detailed Engine Analysis

---

### 1. Piper TTS (by Rhasspy / OHF-Voice)

**Repository:** https://github.com/OHF-Voice/piper1-gpl (active fork), https://github.com/rhasspy/piper (archived Oct 2025)
**Architecture:** VITS-based, ONNX native

| Attribute | Detail |
|-----------|--------|
| **License** | Original: MIT. New fork (piper1-gpl): **GPL-3.0** as of v1.3.0 (March 2025) |
| **GPU/CUDA requirement** | **None required.** Runs entirely on CPU via ONNX Runtime. GPU (CUDA) optional but CPU is often faster. |
| **ONNX Runtime support** | **Native.** Models are distributed as .onnx files. This is the primary inference path. |
| **Quality** | Good for a lightweight model. Natural-sounding with multiple quality tiers (low/medium/high). Not as expressive as larger models. |
| **Latency/Speed** | **Excellent.** Sub-second on CPU. One of the fastest TTS engines. Runs on Raspberry Pi 4. |
| **Phoneme/Viseme** | Models ship with `phoneme_id_map` in JSON config. No native viseme output, but phoneme data is accessible for external mapping. |
| **Docker/Container** | Easily containerized. Minimal dependencies (just onnxruntime). Many community Docker images exist. |
| **Maintenance** | Original repo archived. Active development at OHF-Voice/piper1-gpl. Looking for maintainers. |
| **Voice cloning** | No zero-shot cloning. Requires fine-tuning to add new voices. ~100 pre-trained voices available. |
| **Streaming** | Supports streaming output. Works with Home Assistant and real-time pipelines. |
| **AMD/Intel GPU** | Works on any hardware via ONNX Runtime CPU. DirectML (Windows) possible but untested for TTS. |

**Verdict:** Best choice for ultra-low-latency, CPU-only deployment. Excellent for embedded/edge. Quality is good but not state-of-the-art for expressiveness. GPL-3.0 license on the active fork may be a concern for some use cases.

---

### 2. Kokoro TTS (by hexgrad)

**Repository:** https://github.com/thewh1teagle/kokoro-onnx, https://huggingface.co/hexgrad/Kokoro-82M
**Architecture:** StyleTTS-based, 82M parameters

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0** (model weights and code) |
| **GPU/CUDA requirement** | **None required.** Runs on CPU via ONNX. Also supports WebGPU/WASM in-browser. |
| **ONNX Runtime support** | **Native.** Official ONNX models at `onnx-community/Kokoro-82M-v1.0-ONNX`. Quantized version ~80MB. |
| **Quality** | **Excellent.** #1 on TTS Spaces Arena. 44% win rate on TTS Arena V2. Outperforms models 5-10x its size. |
| **Latency/Speed** | **Excellent.** < 0.3s consistently. 96x real-time on basic cloud GPU. Near real-time on M1 Mac CPU. |
| **Phoneme/Viseme** | **Yes via HeadTTS.** HeadTTS provides phoneme-level timestamps and Oculus visemes for lip-sync using Kokoro ONNX. Word-level timestamps via Kokoro-FastAPI. |
| **Docker/Container** | **Yes.** Kokoro-FastAPI provides Dockerized deployment with OpenAI-compatible API. Multiple Docker images on Docker Hub. |
| **Maintenance** | Active. Regular updates. Strong community. Multiple integration projects. |
| **Voice cloning** | **No zero-shot cloning.** 10+ pre-built voice packs. Cannot clone arbitrary voices. |
| **Streaming** | **Yes.** OpenAI-compatible streaming with 1-2s time-to-first-audio. |
| **AMD/Intel GPU** | **Fully supported via ONNX Runtime.** CPU, DirectML, OpenVINO all viable. WebGPU works in-browser (3x real-time). |

**Verdict:** Best overall candidate for this project. Apache 2.0 license, native ONNX, excellent quality-to-size ratio, viseme support through HeadTTS, and runs anywhere. Main limitation: no voice cloning.

---

### 3. Coqui TTS / XTTS v2 (by Coqui AI / IDIAP fork)

**Repository:** https://github.com/idiap/coqui-ai-TTS (maintained fork), https://github.com/coqui-ai/TTS (original, unmaintained)
**Architecture:** GPT-based autoregressive + VITS decoder

| Attribute | Detail |
|-----------|--------|
| **License** | Code: **MPL-2.0** (Coqui TTS framework). XTTS v2 model weights: **CPML (Coqui Public Model License)** - **non-commercial only**. Commercial license was $365/yr but Coqui shut down Jan 2024. |
| **GPU/CUDA requirement** | **CUDA strongly preferred.** PyTorch-based. CPU inference is very slow. No official ONNX export. |
| **ONNX Runtime support** | **No.** ONNX conversion attempts exist but are incomplete/problematic for XTTS v2. |
| **Quality** | **Very good.** Natural, expressive, multi-lingual (17 languages). |
| **Latency/Speed** | Moderate. ~200ms TTFB on suitable GPU hardware. Too slow on CPU for real-time. |
| **Phoneme/Viseme** | No native viseme/phoneme timing output. |
| **Docker/Container** | Containerizable but requires CUDA runtime in container. |
| **Maintenance** | IDIAP fork is maintained with bug fixes. No new model development. |
| **Voice cloning** | **Excellent.** 6-second reference audio for zero-shot cloning. |
| **Streaming** | Yes, supports streaming inference. |
| **AMD/Intel GPU** | **Poor.** No ONNX path. ROCm theoretically possible but untested/unsupported. |

**Verdict:** Great quality and voice cloning, but CPML license is restrictive, CUDA-dependent, and no ONNX path makes it poor for GPU-agnostic deployment. The company shutdown creates long-term risk.

---

### 4. VITS / VITS2

**Repository:** https://github.com/jaywalnut310/vits (VITS), https://github.com/p0p4k/vits2_pytorch (VITS2)
**Architecture:** End-to-end VAE + normalizing flows + adversarial training

| Attribute | Detail |
|-----------|--------|
| **License** | **MIT** |
| **GPU/CUDA requirement** | Can run on CPU. ONNX export supported. |
| **ONNX Runtime support** | **Yes.** VITS2 has ONNX export. sherpa-onnx ships many pre-trained VITS ONNX models. |
| **Quality** | Good. Natural for single-speaker. VITS2 improves quality and efficiency over VITS. |
| **Latency/Speed** | Fast. Lightweight non-autoregressive architecture. Real-time on CPU. |
| **Phoneme/Viseme** | Phoneme-based input with phoneme IDs accessible. Can be used to derive timing. |
| **Docker/Container** | Lightweight, easily containerized. |
| **Maintenance** | Original VITS repo is research code (not actively maintained). VITS2 has community forks. Piper uses VITS architecture internally. |
| **Voice cloning** | VITS2 supports multi-speaker but not zero-shot cloning without fine-tuning. |
| **Streaming** | Non-autoregressive, so full utterance at once (very fast). Chunk-based streaming possible. |
| **AMD/Intel GPU** | **Good via ONNX Runtime.** Same GPU-agnostic path as Piper. |

**Verdict:** The foundation that Piper builds on. Using VITS/VITS2 directly gives more control but less polish. Best accessed through Piper or sherpa-onnx wrappers.

---

### 5. Bark (by Suno)

**Repository:** https://github.com/suno-ai/bark
**Architecture:** Transformer-based neural codec language model (3 sub-models)

| Attribute | Detail |
|-----------|--------|
| **License** | **MIT** |
| **GPU/CUDA requirement** | **GPU strongly recommended.** CPU inference is 10-20x slower and impractical. 6-12GB VRAM for bark-small. |
| **ONNX Runtime support** | **No official ONNX export.** PyTorch/Transformers-based. |
| **Quality** | **Very good.** Can generate speech, music, sound effects. Expressive with laughter, pauses, etc. |
| **Latency/Speed** | **Slow.** Not suitable for real-time conversation. Several seconds per utterance on GPU. |
| **Phoneme/Viseme** | No phoneme/viseme timing output. |
| **Docker/Container** | Docker images available. Requires CUDA runtime. |
| **Maintenance** | Low. Suno shifted focus to music generation. Repository not actively updated. |
| **Voice cloning** | Can clone tone, pitch, emotion, prosody from speaker prompts. Not fine-grained zero-shot. |
| **Streaming** | Not designed for streaming. Generates full utterances. |
| **AMD/Intel GPU** | **Poor.** No ONNX path. CUDA-focused. |

**Verdict:** Interesting capabilities (music, sound effects) but too slow for real-time conversation, CUDA-dependent, and low maintenance. Not suitable for this project.

---

### 6. Tortoise TTS (by neonbjb)

**Repository:** https://github.com/neonbjb/tortoise-tts
**Architecture:** Autoregressive transformer + diffusion decoder

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0** |
| **GPU/CUDA requirement** | **GPU required.** Very slow on CPU (~2 minutes per sentence on older hardware). |
| **ONNX Runtime support** | **No official ONNX.** Community fast-inference forks exist but no ONNX conversion. |
| **Quality** | **Excellent.** One of the highest quality open-source TTS models. Very natural. |
| **Latency/Speed** | **Very slow.** Not suitable for real-time. Even with tortoise-tts-fast, still not conversational speed. |
| **Phoneme/Viseme** | No native phoneme/viseme output. |
| **Docker/Container** | Docker support available. Requires CUDA. |
| **Maintenance** | Low. Author moved on. Community forks (tortoise-tts-fast, tortoise-tts-fastest) exist. |
| **Voice cloning** | **Excellent.** High-quality voice cloning from short reference audio. |
| **Streaming** | Limited. Too slow for practical streaming. |
| **AMD/Intel GPU** | **Poor.** Linux+ROCm partially works. Windows AMD is problematic. |

**Verdict:** Extremely high quality but far too slow for real-time use. Best for offline/batch generation only.

---

### 7. StyleTTS 2

**Repository:** https://github.com/yl4579/StyleTTS2
**Architecture:** Style diffusion + adversarial training with large speech language models

| Attribute | Detail |
|-----------|--------|
| **License** | **MIT** (code). Model use requires disclosure that speech is synthesized (unless speaker grants permission). |
| **GPU/CUDA requirement** | **CUDA preferred.** PyTorch-based. ONNX conversion requested but not officially supported. |
| **ONNX Runtime support** | **Partial.** Community ONNX exports exist (hexgrad/styletts2 on HuggingFace). Not official. |
| **Quality** | **State-of-the-art.** Surpasses human recordings on LJSpeech. Matches human on VCTK. |
| **Latency/Speed** | Moderate. Faster than Tortoise but not as fast as Piper/Kokoro. |
| **Phoneme/Viseme** | No native viseme output. Phoneme-based input. |
| **Docker/Container** | Docker available on HuggingFace Spaces and Salad Technologies. |
| **Maintenance** | Moderate. Academic project. Community fork (Stylish-TTS) adds features. |
| **Voice cloning** | Yes, style-based voice cloning from reference audio. |
| **Streaming** | Experimental streaming API in community forks. |
| **AMD/Intel GPU** | **Limited.** No official ONNX. Community ONNX exports may work with DirectML/ROCm. |

**Verdict:** Top-tier quality but CUDA-centric. Partial ONNX support through community efforts. Good quality-to-speed ratio but not as deployment-ready as Kokoro or Piper.

---

### 8. OpenVoice V2 (by MyShell.ai)

**Repository:** https://github.com/myshell-ai/OpenVoice
**Architecture:** Two-stage: base TTS + tone color converter

| Attribute | Detail |
|-----------|--------|
| **License** | **MIT** (since April 2024, both V1 and V2) |
| **GPU/CUDA requirement** | Runs on CPU and GPU. Lightweight architecture. |
| **ONNX Runtime support** | **Community ONNX export** via nnWhisperer/OpenVoice_ONNX. Not official. |
| **Quality** | Good. Focused on voice cloning rather than base TTS quality. |
| **Latency/Speed** | Fast. Lightweight and optimized for real-time inference. |
| **Phoneme/Viseme** | No native phoneme/viseme output. |
| **Docker/Container** | Docker available via community (Decentralised-AI/OpenVoice-DockerFile). Gradio demo included. |
| **Maintenance** | Active. MyShell.ai continues development. |
| **Voice cloning** | **Excellent.** Core feature. Instant zero-shot cross-lingual voice cloning. Fine-grained style control. |
| **Streaming** | Limited streaming support. Primarily batch inference. |
| **AMD/Intel GPU** | **Moderate.** Community ONNX export enables GPU-agnostic deployment. CPU works fine. |

**Verdict:** Best for voice cloning specifically. Use it as a voice conversion layer on top of another TTS engine (e.g., Kokoro + OpenVoice for cloned voice output).

---

### 9. WhisperSpeech

**Repository:** https://github.com/WhisperSpeech/WhisperSpeech
**Architecture:** Multi-stage pipeline (semantic tokens via Whisper + acoustic tokens via EnCodec + Vocos vocoder)

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0 / MIT** (all code). Trained only on properly licensed data. |
| **GPU/CUDA requirement** | **GPU recommended.** PyTorch-based. 12x real-time on RTX 4090. CPU is slow. |
| **ONNX Runtime support** | **No ONNX export available.** |
| **Quality** | Good to very good. Built on proven Whisper architecture inverted for synthesis. |
| **Latency/Speed** | Moderate to fast with torch.compile optimizations. Not as fast as Kokoro/Piper on CPU. |
| **Phoneme/Viseme** | No native phoneme/viseme output. |
| **Docker/Container** | Can be containerized. Standard Python/PyTorch stack. |
| **Maintenance** | Active development by Collabora and LAION. |
| **Voice cloning** | Yes. Reference audio-based voice cloning. |
| **Streaming** | Possible with pipeline optimization. |
| **AMD/Intel GPU** | **Poor.** No ONNX path. CUDA-focused for GPU acceleration. |

**Verdict:** Interesting architecture and commercially safe licensing, but lacks ONNX support and is GPU-dependent for good performance. Not ideal for GPU-agnostic deployment.

---

### 10. Fish Speech / OpenAudio

**Repository:** https://github.com/fishaudio/fish-speech
**Architecture:** Neural codec language model. S1 (4B) and S1-mini (0.5B) variants.

| Attribute | Detail |
|-----------|--------|
| **License** | Code: **Apache 2.0**. Model weights: **CC-BY-NC-SA-4.0** (non-commercial). |
| **GPU/CUDA requirement** | **GPU recommended.** 4GB VRAM minimum. CUDA or ROCm. CPU mode available. |
| **ONNX Runtime support** | **No official ONNX.** Community ZLUDA fork for AMD on Windows. |
| **Quality** | **Very good.** 1:7 real-time factor on RTX 4090. Multilingual (8 languages). |
| **Latency/Speed** | Fast on GPU. Moderate on CPU. |
| **Phoneme/Viseme** | No native phoneme/viseme output. Does not use traditional phoneme alignment. |
| **Docker/Container** | **Yes.** Official Docker images on Docker Hub (fishaudio/fish-speech). |
| **Maintenance** | **Very active.** Continuous development by Fish Audio team. |
| **Voice cloning** | **Excellent.** 10-30 second reference for accurate cloning. Captures timbre, style, emotion. |
| **Streaming** | Supports streaming inference. |
| **AMD/Intel GPU** | **Partial.** ROCm support on Linux (torch+rocm). ZLUDA community fork for Windows AMD. CPU fallback. |

**Verdict:** Powerful model with good Docker support, but CC-BY-NC-SA model weights license is restrictive. Not truly GPU-agnostic (no ONNX). Good for non-commercial projects with NVIDIA GPUs.

---

### 11. Parler TTS (by Hugging Face)

**Repository:** https://github.com/huggingface/parler-tts
**Architecture:** Transformer-based with natural language voice descriptions for control

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0** |
| **GPU/CUDA requirement** | **GPU preferred.** PyTorch/Transformers-based. |
| **ONNX Runtime support** | **No official ONNX export.** |
| **Quality** | Good. Unique natural language voice control (describe voice characteristics in text). |
| **Latency/Speed** | Moderate. Supports torch.compile for optimization. |
| **Phoneme/Viseme** | No native phoneme/viseme output. |
| **Docker/Container** | Community Docker wrapper (parler-tts-server) with OpenAI-compatible API. |
| **Maintenance** | Active. Backed by Hugging Face team. |
| **Voice cloning** | Not traditional cloning. Uses text descriptions to control voice characteristics. |
| **Streaming** | Yes. Supports audio output streaming. |
| **AMD/Intel GPU** | **Limited.** No ONNX path. Standard PyTorch GPU backends. |

**Verdict:** Interesting approach with text-based voice control, but not optimized for GPU-agnostic deployment. Apache 2.0 is great. More of a research project than production-ready.

---

### 12. MeloTTS (by MyShell.ai)

**Repository:** https://github.com/myshell-ai/MeloTTS
**Architecture:** Non-autoregressive (based on VITS). Optimized for speed.

| Attribute | Detail |
|-----------|--------|
| **License** | **MIT** |
| **GPU/CUDA requirement** | **None required.** Optimized for real-time on CPU. GPU optional. |
| **ONNX Runtime support** | **In progress.** PR opened May 2025 to add ONNX inference acceleration. |
| **Quality** | Good. 44.1 kHz output. Multi-lingual (EN, ES, FR, ZH, JA, KO). |
| **Latency/Speed** | **Excellent.** Among the fastest. Consistent sub-second latency even for long texts. Real-time on CPU. |
| **Phoneme/Viseme** | No native viseme output. Phoneme-based internally. |
| **Docker/Container** | **Yes.** Official Dockerfile in repo. Community Docker images available. |
| **Maintenance** | Active. MyShell.ai continues development. |
| **Voice cloning** | **No.** Does not support zero-shot voice cloning. |
| **Streaming** | Non-autoregressive streaming optimized for low latency. |
| **AMD/Intel GPU** | **Good.** CPU performance is already excellent. ONNX support incoming will improve GPU-agnostic deployment. |

**Verdict:** Excellent speed and CPU performance. MIT license. Great for real-time conversational use. Main gaps: no voice cloning, no viseme output. ONNX support in development will make it even better.

---

### 13. F5-TTS

**Repository:** https://github.com/SWivid/F5-TTS
**Architecture:** Flow matching + Diffusion Transformer (DiT). Non-phoneme-based.

| Attribute | Detail |
|-----------|--------|
| **License** | Code: **CC-BY-NC-SA-4.0** (non-commercial). |
| **GPU/CUDA requirement** | **GPU recommended.** Supports CUDA and **ROCm** (torch+rocm6.2). |
| **ONNX Runtime support** | **Yes.** Community ONNX port at DakeQQ/F5-TTS-ONNX with onnxruntime-openvino support. |
| **Quality** | **Excellent.** State-of-the-art voice cloning quality. V1 released March 2025. |
| **Latency/Speed** | Moderate. Flow matching is faster than diffusion but not as fast as VITS-based models. |
| **Phoneme/Viseme** | No phoneme alignment needed (end-to-end). No viseme output. |
| **Docker/Container** | No official Docker. Standard conda/pip installation. |
| **Maintenance** | **Very active.** Regular releases. V1 base model March 2025. |
| **Voice cloning** | **Excellent.** Zero-shot voice cloning is the primary feature. |
| **Streaming** | Supports streaming inference. |
| **AMD/Intel GPU** | **Good.** ROCm support on Linux. ONNX port with OpenVINO EP supports Intel. |

**Verdict:** One of the best for voice cloning quality. ONNX port exists with OpenVINO support for Intel. ROCm support for AMD. But CC-BY-NC-SA license is restrictive for commercial use.

---

### 14. Dia (by Nari Labs)

**Repository:** https://github.com/nari-labs/dia (v1), https://github.com/nari-labs/dia2 (v2 streaming)
**Architecture:** 1.6B parameter transformer. Dia2 adds streaming architecture.

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0** |
| **GPU/CUDA requirement** | **GPU required.** ~10GB VRAM. CUDA 12.6. ~40 tokens/second on A4000. |
| **ONNX Runtime support** | **No ONNX export available.** |
| **Quality** | **Excellent.** Ultra-realistic dialogue. Multi-speaker. Non-verbal sounds (laughs, sighs). |
| **Latency/Speed** | Moderate. Real-time on single GPU. Dia2 streams from first tokens. |
| **Phoneme/Viseme** | No native phoneme/viseme output. |
| **Docker/Container** | Can be containerized. Standard PyTorch stack. |
| **Maintenance** | **Very active.** Dia2 released 2025 with streaming. |
| **Voice cloning** | Yes. Can condition on audio for voice/emotion matching. |
| **Streaming** | **Dia2: Yes.** Can start generating audio before full text input. Low-latency conversational. |
| **AMD/Intel GPU** | **Poor.** CUDA-focused. No ONNX path. |

**Verdict:** Excellent for conversational dialogue with multi-speaker and emotion. Dia2's streaming is perfect for real-time agents. But GPU-heavy and CUDA-only. Apache 2.0 is great.

---

### 15. Orpheus TTS (by Canopy Labs)

**Repository:** https://github.com/canopyai/Orpheus-TTS
**Architecture:** Llama-3 backbone (3B, 1B, 400M, 150M variants) + SNAC decoder

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0** |
| **GPU/CUDA requirement** | **GPU required.** 24GB for 3B model. Smaller variants (150M Nano) more accessible. |
| **ONNX Runtime support** | **Partial.** Model artifacts can be exported to ONNX with LoRA weights. Nano model planned for WebGPU. |
| **Quality** | **Excellent.** Human-like intonation, emotion, rhythm. Rivals closed-source systems. |
| **Latency/Speed** | **Good.** ~100-200ms streaming TTFB. Real-time on single GPU. |
| **Phoneme/Viseme** | No native phoneme/viseme output. Emotion controlled via tags (<laugh>, <sigh>, etc.). |
| **Docker/Container** | **Yes.** Docker image on Docker Hub (olilanz/ai-orpheus-tts). Orpheus-FastAPI provides containerized deployment. |
| **Maintenance** | **Very active.** Multiple model sizes released 2025. Multilingual research preview April 2025. |
| **Voice cloning** | **Yes.** Zero-shot voice cloning. |
| **Streaming** | **Yes.** Real-time streaming with ~100ms latency. vLLM/SGLang backends. |
| **AMD/Intel GPU** | **Limited.** Primarily CUDA/NVIDIA. Orpheus-FastAPI mentions ROCm support but CUDA is primary. 150M Nano model could work via ONNX/WebGPU. |

**Verdict:** Top-tier quality and expressiveness. Apache 2.0 license. Nano model (150M) could be GPU-agnostic via ONNX. Full 3B model is CUDA-dependent. Watch for Nano ONNX release.

---

### 16. Sesame CSM (Conversational Speech Model)

**Repository:** https://github.com/SesameAILabs/csm
**Architecture:** Llama backbone + Mimi audio decoder. 1B parameters.

| Attribute | Detail |
|-----------|--------|
| **License** | **Apache 2.0** |
| **GPU/CUDA requirement** | **Flexible.** 4.5GB VRAM on CUDA, 8.1GB on MLX (Mac), 8.5GB on CPU. |
| **ONNX Runtime support** | **No ONNX export available.** Supports CUDA, MLX, and CPU. |
| **Quality** | **State-of-the-art.** Considered the most realistic voice model. Trained on 1M hours. |
| **Latency/Speed** | Moderate. ~6s raw, ~1-2s with streaming/WebSocket optimization. |
| **Phoneme/Viseme** | No native phoneme/viseme output. |
| **Docker/Container** | Can be containerized. Multi-GPU support via environment variables. Community Docker implementations. |
| **Maintenance** | **Active.** Released March 2025. Active community. |
| **Voice cloning** | **Yes.** Voice cloning from audio samples. Can clone from YouTube videos. |
| **Streaming** | **Yes.** Community streaming implementation available. WebSocket-based. |
| **AMD/Intel GPU** | **Moderate.** CPU mode works. MLX for Mac. No ONNX, but CPU inference at 8.5GB is viable. |

**Verdict:** Highest quality conversational speech. Apache 2.0 is excellent. CPU mode makes it accessible without NVIDIA. Main concern is latency for real-time use and lack of ONNX. Excellent for avatar conversational use case.

---

### 17. Dia / Sesame CSM Already Covered Above

---

## GPU-Agnostic Deployment Strategy

### ONNX Runtime Execution Providers (Key for GPU-Agnostic)

| Provider | Hardware | Status |
|----------|----------|--------|
| **CPU** | Any | Always works. Default fallback. |
| **CUDA** | NVIDIA | Mature, best performance. |
| **ROCm/MIGraphX** | AMD | ROCm EP removed in ORT 1.23+. MIGraphX EP now recommended for AMD. |
| **DirectML** | AMD/NVIDIA/Intel (Windows) | Works across all Windows GPUs. 92% of TensorRT perf on Intel NPUs. |
| **OpenVINO** | Intel | Optimized for Intel CPUs, GPUs, and NPUs. |
| **Vulkan** | All GPUs | **Not yet implemented** as ONNX Runtime EP. Feature requested but not available. |
| **WebGPU** | All GPUs (browser) | Available for in-browser inference. Kokoro supports this. |

### Recommended Architecture for GPU-Agnostic Container

```
[Text Input] -> [Kokoro TTS (ONNX)] -> [Audio + Phoneme Timestamps]
                                               |
                                    [HeadTTS Viseme Mapper]
                                               |
                                    [Viseme Timing Data for Lip Sync]
```

**Container Strategy:**
- Base image: Python 3.10+ with onnxruntime (CPU version works everywhere)
- Optional: onnxruntime-gpu for NVIDIA, onnxruntime-directml for Windows mixed-GPU
- Model: Kokoro-82M ONNX (~300MB, quantized ~80MB)
- Visemes: HeadTTS for phoneme-to-viseme mapping with timestamps

---

## Comparison Matrix

| Engine | License | ONNX | CPU-OK | Quality | Latency | Viseme | Clone | Stream | Active |
|--------|---------|------|--------|---------|---------|--------|-------|--------|--------|
| **Kokoro** | Apache 2.0 | **Native** | **Yes** | Excellent | **< 0.3s** | **Yes*** | No | Yes | Yes |
| **Piper** | GPL-3.0 | **Native** | **Yes** | Good | **< 1s** | Partial | No | Yes | Moderate |
| **MeloTTS** | MIT | WIP | **Yes** | Good | **< 1s** | No | No | Yes | Yes |
| **VITS/VITS2** | MIT | **Yes** | **Yes** | Good | Fast | Partial | No | N/A | Low |
| **F5-TTS** | CC-BY-NC-SA | **Community** | Slow | Excellent | Moderate | No | **Yes** | Yes | Yes |
| **Orpheus** | Apache 2.0 | Partial | No | Excellent | ~100ms | No | **Yes** | **Yes** | **Yes** |
| **Sesame CSM** | Apache 2.0 | No | Slow | **Best** | ~1-2s | No | **Yes** | Yes | Yes |
| **Dia/Dia2** | Apache 2.0 | No | No | Excellent | Real-time | No | Yes | **Yes** | **Yes** |
| **StyleTTS 2** | MIT | Community | Slow | **Excellent** | Moderate | No | Yes | Exp. | Moderate |
| **OpenVoice** | MIT | Community | Yes | Good | Fast | No | **Best** | Limited | Yes |
| **Coqui XTTS** | CPML (NC) | No | Very Slow | Very Good | ~200ms | No | **Yes** | Yes | Low |
| **Bark** | MIT | No | Very Slow | Good | Slow | No | Partial | No | Low |
| **Tortoise** | Apache 2.0 | No | No | Excellent | **Very Slow** | No | **Yes** | No | Low |
| **WhisperSpeech** | Apache/MIT | No | Slow | Good | Moderate | No | Yes | Possible | Yes |
| **Fish Speech** | Apache/NC** | No | Slow | Very Good | Fast (GPU) | No | **Yes** | Yes | **Yes** |
| **Parler TTS** | Apache 2.0 | No | Slow | Good | Moderate | No | Text-ctrl | Yes | Yes |

*\* Kokoro visemes via HeadTTS integration*
*\*\* Fish Speech: code is Apache, model weights are CC-BY-NC-SA*

---

## Recommendations for Digital Avatar Project

### Tier 1: Deploy Now (GPU-Agnostic, Production-Ready)

1. **Kokoro TTS (ONNX)** - Primary recommendation
   - Apache 2.0, runs anywhere via ONNX
   - Viseme support via HeadTTS for lip sync
   - Kokoro-FastAPI for Dockerized deployment
   - Sub-300ms latency, streaming support
   - Limitation: No voice cloning (use fixed voice packs)

2. **Piper TTS (ONNX)** - Fallback / embedded option
   - Runs on Raspberry Pi, near-instant
   - GPL-3.0 may affect distribution
   - Lower quality than Kokoro but faster

### Tier 2: Deploy with Constraints

3. **MeloTTS** - MIT license, fast CPU, but no ONNX yet and no cloning
4. **OpenVoice V2** - Use as voice conversion layer on top of Kokoro/Piper for cloning
5. **F5-TTS (ONNX port)** - If voice cloning needed and non-commercial is acceptable

### Tier 3: Watch and Evaluate

6. **Orpheus TTS Nano (150M)** - When ONNX/WebGPU version ships, could be the best overall
7. **Sesame CSM** - Highest quality, but needs ONNX port for GPU-agnostic use
8. **Dia2** - Best streaming conversational model, but CUDA-only currently

### Recommended Pipeline for Avatar

```
Option A (No Voice Cloning):
  Kokoro TTS (ONNX, CPU) -> HeadTTS Viseme Mapper -> Avatar Lip Sync

Option B (With Voice Cloning):
  Kokoro TTS (ONNX) -> OpenVoice V2 (tone conversion) -> Viseme Extraction -> Avatar

Option C (Highest Quality, NVIDIA GPU):
  Orpheus TTS / Sesame CSM -> External Viseme Extraction (forced alignment) -> Avatar
```

---

## Sources

- [Piper TTS (archived)](https://github.com/rhasspy/piper)
- [Piper1-GPL (active fork)](https://github.com/OHF-Voice/piper1-gpl)
- [piper-onnx](https://github.com/thewh1teagle/piper-onnx)
- [Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)
- [kokoro-onnx](https://github.com/thewh1teagle/kokoro-onnx)
- [Kokoro-FastAPI](https://github.com/remsky/Kokoro-FastAPI)
- [HeadTTS (Kokoro visemes)](https://github.com/met4citizen/HeadTTS)
- [IDIAP Coqui TTS Fork](https://github.com/idiap/coqui-ai-TTS)
- [XTTS v2 License Discussion](https://github.com/coqui-ai/TTS/discussions/4304)
- [VITS](https://github.com/jaywalnut310/vits)
- [VITS2](https://github.com/p0p4k/vits2_pytorch)
- [Bark (Suno)](https://huggingface.co/suno/bark)
- [Tortoise TTS](https://github.com/neonbjb/tortoise-tts)
- [StyleTTS 2](https://github.com/yl4579/StyleTTS2)
- [OpenVoice](https://github.com/myshell-ai/OpenVoice)
- [OpenVoice ONNX](https://github.com/nnWhisperer/OpenVoice_ONNX)
- [WhisperSpeech](https://github.com/WhisperSpeech/WhisperSpeech)
- [Fish Speech](https://github.com/fishaudio/fish-speech)
- [Parler TTS](https://github.com/huggingface/parler-tts)
- [MeloTTS](https://github.com/myshell-ai/MeloTTS)
- [F5-TTS](https://github.com/SWivid/F5-TTS)
- [F5-TTS ONNX](https://github.com/DakeQQ/F5-TTS-ONNX)
- [Dia (Nari Labs)](https://github.com/nari-labs/dia)
- [Dia2 (Nari Labs)](https://github.com/nari-labs/dia2)
- [Orpheus TTS](https://github.com/canopyai/Orpheus-TTS)
- [Orpheus-FastAPI](https://github.com/Lex-au/Orpheus-FastAPI)
- [Sesame CSM](https://github.com/SesameAILabs/csm)
- [sherpa-onnx](https://github.com/k2-fsa/sherpa-onnx)
- [ONNX Runtime Execution Providers](https://onnxruntime.ai/docs/execution-providers/)
- [DirectML Guide (AMD GPUOpen)](https://gpuopen.com/learn/onnx-directlml-execution-provider-guide-part1/)
- [Inferless TTS Comparison 2025](https://www.inferless.com/learn/comparing-different-text-to-speech---tts--models-part-2)
- [BentoML TTS Overview 2026](https://bentoml.com/blog/exploring-the-world-of-open-source-text-to-speech-models)
- [Resemble AI TTS Guide 2025](https://www.resemble.ai/best-open-source-text-to-speech-models/)
