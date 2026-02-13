# Open-Source 3D Avatar & Character Rendering Solutions Research

**Date:** 2025-02-10
**Requirements:** GPU-agnostic (AMD/Nvidia/Intel), containerizable, cartoon/stylized look, lip-sync capable, open source

---

## TABLE OF CONTENTS

1. [Executive Summary & Recommendations](#executive-summary)
2. [Three.js / WebGL-Based Solutions](#threejs--webgl-based-solutions)
3. [VRM Format & Ecosystem](#vrm-format--ecosystem)
4. [Godot Engine](#godot-engine)
5. [Open 3D Engine (O3DE)](#open-3d-engine-o3de)
6. [Bevy (Rust Game Engine)](#bevy-rust-game-engine)
7. [Live2D Alternatives (2D Avatar Animation)](#live2d-alternatives)
8. [Talking Head / AI Lip-Sync Projects](#talking-head--ai-lip-sync-projects)
9. [VTuber Avatar Rendering Solutions](#vtuber-avatar-rendering-solutions)
10. [Kalidokit & MediaPipe Solutions](#kalidokit--mediapipe-solutions)
11. [OpenUSD (Pixar)](#openusd-pixar)
12. [NVIDIA Audio2Face (Open-Sourced)](#nvidia-audio2face)
13. [Comparative Matrix](#comparative-matrix)
14. [Recommended Architecture](#recommended-architecture)

---

## EXECUTIVE SUMMARY

### Top 3 Recommendations for This Project

**1. Three.js + @pixiv/three-vrm + TalkingHead (BEST FIT)**
- Browser-based WebGL rendering, fully GPU-agnostic
- VRM avatar format with built-in viseme/lip-sync
- Can run in Docker via headless Chromium + Xvfb or via headless-gl
- Cartoon/stylized VRM avatars freely available
- MIT licensed, large community, actively maintained

**2. Godot 4 Engine (with VRM support)**
- Vulkan + OpenGL ES 3.0 backends (GPU-agnostic)
- Can run headless in Docker containers
- VRM support via godot-vrm plugin
- Strong scripting with GDScript/C#
- MIT licensed

**3. Inochi2D (for 2D stylized avatars)**
- Open-source Live2D alternative, BSD 2-clause license
- OpenGL 3.1 rendering, GPU-agnostic
- Ideal for cartoon/stylized 2D characters
- Built-in face tracking and lip-sync via Session component

---

## THREE.JS / WEBGL-BASED SOLUTIONS

### @pixiv/three-vrm
- **URL:** https://github.com/pixiv/three-vrm
- **License:** MIT
- **Latest Version:** 3.4.4 (actively maintained, published ~2 months ago)
- **GPU Requirements:** WebGL 1.0/2.0 - works on ANY GPU with a browser or headless-gl
- **CUDA Dependency:** NONE
- **Container Strategy:**
  - Option A: Headless Chromium/Puppeteer in Docker with Xvfb (virtual framebuffer)
  - Option B: Node.js + headless-gl (stackgl/headless-gl) for server-side WebGL
  - Option C: Puppeteer with SwiftShader (software renderer, no GPU needed at all)
- **Lip Sync:** VRM format natively supports viseme blendshapes (A, I, U, E, O + extended set)
- **Community:** Large - pixiv is a major company, thousands of GitHub stars
- **Stylized/Cartoon:** VRM avatars from VRoid Studio are inherently anime/cartoon style

### met4citizen/TalkingHead
- **URL:** https://github.com/met4citizen/TalkingHead
- **License:** MIT
- **GPU Requirements:** WebGL (Three.js based) - GPU-agnostic
- **CUDA Dependency:** NONE
- **Container Strategy:** Same as three-vrm (browser/headless-gl based)
- **Lip Sync:** Built-in audio-driven real-time viseme detection. Supports 15 visemes: aa, E, I, O, U, PP, SS, TH, CH, FF, kk, nn, RR, DD, sil. No text transcription needed - works from audio alone.
- **Features:**
  - Supports Ready Player Me GLB avatars and VRM-compatible models
  - Mixamo animation support (FBX)
  - Built-in physics engine for dynamic bones
  - TTS integration (Google Cloud, Azure Speech SDK)
  - Emoji-to-expression conversion
  - Multi-avatar mode
  - NPM package available
- **Community:** Actively maintained, multiple forks
- **Stylized/Cartoon:** Supports any GLB model - cartoon characters work

### Babylon.js + VRM
- **URL:** https://github.com/virtual-cast/babylon-vrm-loader
- **License:** MIT
- **GPU Requirements:** WebGL/WebGPU - GPU-agnostic
- **CUDA Dependency:** NONE
- **Lip Sync:** Babylon.js 7.0 supports morph target lip sync animations blended with other animations
- **Container Strategy:** Can run in headless Puppeteer Docker container
- **Community:** Babylon.js is Microsoft-backed, large community. VRM loader is community-maintained.
- **Note:** Less VRM-specific tooling compared to Three.js ecosystem

### headless-gl (stackgl)
- **URL:** https://github.com/stackgl/headless-gl
- **Purpose:** Windowless WebGL implementation for Node.js
- **Built on:** ANGLE (passes full Khronos ARB conformance)
- **Docker Requirements:** libgl1, freeglut3-dev, xvfb
- **Performance Note:** Primarily CPU-based rendering (software rasterization). Good for lower-fidelity cartoon rendering, may struggle with complex scenes.
- **Advantage:** No GPU hardware required at all

### Ready Player Me Visage
- **URL:** https://github.com/readyplayerme/visage
- **License:** MIT
- **Purpose:** React component for displaying RPM avatars on the web
- **Note:** Avatars are GLB format served from RPM servers - can be self-hosted once downloaded
- **Lip Sync:** Compatible with standard viseme blendshapes

---

## VRM FORMAT & ECOSYSTEM

### VRM Format Overview
- **Specification:** https://github.com/vrm-c/vrm-specification
- **License:** Open standard (CC-BY-4.0 for spec)
- **Format:** Extension of glTF 2.0 (.glb binary)
- **Versions:** VRM 0.x (widely supported) and VRM 1.0 (newer, less supported)
- **Purpose:** Specifically designed for humanoid virtual avatars

### VRM Viseme/Expression System
- **VRM 0.x:** BlendShape system with preset clips: A, I, U, E, O (mapped to aa, ih, ou, E, oh)
- **VRM 1.0:** Renamed to "Expression" system, same concept
- **Extended visemes (VSeeFace standard):** SIL, CH, DD, FF, KK, NN, PP, RR, SS, TH
- **ARKit compatibility:** 52 ARKit blendshapes can be added to VRM models (via HANA Tool for VRoid)
- **Value range:** Each expression/viseme has value [0-1] for smooth interpolation

### VRM Avatar Creation Tools
- **VRoid Studio:** Free avatar creator by pixiv, outputs VRM format, inherently anime/cartoon style
- **VRM Viseme Tools:** https://github.com/ImLevath/vrm-viseme-tools - Unity editor tools for mapping Japanese viseme blendshapes to English VRM visemes
- **Open Source Avatar Registry:** https://github.com/ToxSam/open-source-avatars - curated free VRM avatars

### Key Advantage for This Project
VRM is the ideal avatar format because:
1. Open standard, not locked to any vendor
2. Built-in viseme/expression support for lip sync
3. Large ecosystem of free cartoon-style avatars (VRoid Hub)
4. Multiple rendering libraries (Three.js, Babylon.js, Godot, Unity)
5. Lightweight GLB format, easy to containerize

---

## GODOT ENGINE

### Godot 4.x Rendering Architecture
- **URL:** https://godotengine.org/
- **License:** MIT
- **Renderers:**
  - Forward+ (Vulkan/DX12) - most advanced, desktop only
  - Mobile (Vulkan/DX12) - optimized for mobile
  - Compatibility (OpenGL ES 3.0/WebGL 2.0) - broadest hardware support
- **GPU Requirements:** Vulkan OR OpenGL ES 3.0 - works on AMD, Nvidia, Intel
- **CUDA Dependency:** NONE

### Containerization
- **Docker support:** Multiple projects exist:
  - https://github.com/briancain/GodotServer-Docker - Godot 4.x server in Docker headless mode
  - https://github.com/robpc/docker-godot-headless - Docker builds with export templates
  - https://github.com/loherangrin/o3tanks - CLI tool to build/run in containers (O3DE focused but pattern applicable)
- **Headless mode:** `--headless` flag with Dummy display server and Dummy audio driver
- **Limitation:** Compute shaders do NOT work in headless mode. Standard rendering requires X11/Xvfb.

### VRM Support in Godot
- **godot-vrm plugin:** Supports VRM 0 and VRM 1 models
- **vpuppr (Virtual Puppet Project):** VTuber app made with Godot 4 - ARCHIVED May 2024
  - Supported VRM 0/1, Live2D (via gd_cubism), Inochi2D, MediaPipe face tracking
  - Shows feasibility but project is abandoned

### Lip Sync in Godot
- Morph target/blendshape animation supported
- No built-in viseme detection - would need external audio-to-viseme pipeline
- Could integrate with NVIDIA Audio2Face ONNX models or custom solution

### Assessment for This Project
- Strong choice if you want a full game engine with scripting
- GPU-agnostic via Compatibility renderer (OpenGL ES 3.0)
- Container support proven but requires Xvfb for rendering
- Would need custom lip-sync pipeline integration
- Active community (~90k GitHub stars)

---

## OPEN 3D ENGINE (O3DE)

### Overview
- **URL:** https://o3de.org/
- **License:** Apache 2.0
- **Maintained by:** Open 3D Foundation (Linux Foundation)
- **Renderer:** Atom - modular, multi-threaded, physically based renderer

### GPU & Graphics API Support
- **Supported APIs:** Vulkan, DirectX 12, Metal
- **NO OpenGL support** - only modern APIs
- **Linux:** Vulkan only (preview state as of O3DE 24.09)
- **Note:** Does NOT support older GPUs that lack Vulkan

### Containerization
- Docker images exist: https://hub.docker.com/r/husarion/o3de
- O3Tanks CLI tool for container management: https://github.com/loherangrin/o3tanks
- Null renderer mode: `--rhi=null` flag
- **Challenge:** Requires X11/Wayland even for headless operation

### Lip Sync Support
- No built-in lip sync system documented
- Would need custom implementation using morph targets
- Primarily designed for large-scale game/simulation, not avatar rendering

### Assessment for This Project
- **OVERKILL** for a digital avatar project
- Heavy engine (~50GB+ build), slow compile times
- Complex containerization
- Limited Linux/headless support
- Better suited for large game studios
- **NOT RECOMMENDED** for this use case

---

## BEVY (RUST GAME ENGINE)

### Overview
- **URL:** https://bevyengine.org/
- **License:** MIT OR Apache 2.0
- **Latest:** Bevy 0.16
- **Built on:** wgpu (supports Vulkan, DX12, Metal, OpenGL, WebGL2, WebGPU)

### GPU Support
- **Ideal:** Vulkan (Linux), DX12 (Windows), Metal (macOS)
- **Fallback:** OpenGL ES 3.0 (may have issues)
- **GPU-agnostic:** Yes, via wgpu abstraction layer
- **CUDA Dependency:** NONE

### Avatar & Animation Features
- Skeletal animation support
- Morph target animation (since Bevy 0.11)
- GPU-driven rendering for skinned meshes (Bevy 0.16)
- PBR, normal mapping, shadow mapping, etc.
- AnimationGraph for blending animations

### Lip Sync
- Morph target support enables viseme-based lip sync
- No dedicated lip sync plugin found as of 2024
- Would require custom implementation

### Containerization
- Headless mode possible via wgpu's software rendering
- Less Docker ecosystem compared to Godot/Three.js
- Rust compilation in containers is well-established

### Assessment for This Project
- Technically capable but immature ecosystem for avatars
- No VRM loader, no lip sync plugin
- Steep learning curve (Rust + ECS architecture)
- Best for teams already invested in Rust
- **NOT RECOMMENDED** unless Rust is a requirement

---

## LIVE2D ALTERNATIVES

### Inochi2D
- **URL:** https://inochi2d.com/
- **GitHub:** https://github.com/Inochi2D/inochi2d
- **License:** BSD 2-clause
- **Version:** 0.8.x (beta)
- **Language:** D programming language (with C FFI for other languages)
- **Rendering:** OpenGL 3.1 core context
- **GPU Requirements:** Any GPU with OpenGL 3.1 support - GPU-agnostic
- **CUDA Dependency:** NONE

### Inochi2D Features
- **Creator:** Rigging application for 2D characters
- **Session:** Live performance/puppeteering with face tracking
- **Lip Sync:** Via VMC (Virtual Motion Capture) protocol blendshapes
- **Supported Tracking:** Face tracking via webcam, mobile device sensors
- **Physics:** Built-in physics for hair, clothing, etc.
- **Art Style:** Any 2D art style - perfect for cartoon characters
- **Platform:** Windows, macOS, Linux

### Containerization Potential
- Flatpak packaging exists (can run in podman)
- OpenGL 3.1 rendering could work with Xvfb + Mesa in Docker
- No official Docker support
- C FFI (inochi2d-c) allows integration from other languages

### Assessment for This Project
- Excellent for 2D cartoon-style avatars
- GPU-agnostic, open source, actively developed
- Good lip sync via VMC protocol
- Immature compared to Live2D Cubism but improving
- Would need community work for headless Docker deployment
- **RECOMMENDED** if 2D style is acceptable

---

## TALKING HEAD / AI LIP-SYNC PROJECTS

### CRITICAL NOTE: CUDA Dependency Problem
Almost ALL deep-learning talking head models require NVIDIA CUDA. This is a fundamental conflict with the GPU-agnostic requirement. Workarounds exist (ONNX, OpenVINO) but with caveats.

### Wav2Lip
- **URL:** https://github.com/Rudrabha/Wav2Lip
- **License:** Custom (research license)
- **GPU:** CUDA required for training, ONNX/OpenVINO available for inference
- **ONNX version:** https://github.com/instant-high/wav2lip-onnx-256 (256x256 resolution)
- **OpenVINO:** Official support in OpenVINO 2024 docs - can run on CPU and Intel GPUs
- **Container:** Docker-friendly (Python + PyTorch)
- **Lip Sync:** Excellent - core function is lip sync
- **Style:** Works on video/images, not 3D avatars directly
- **Note:** CPU inference is viable but slow

### SadTalker
- **URL:** https://github.com/OpenTalker/SadTalker
- **License:** Custom (academic/non-commercial)
- **GPU:** CUDA 11.3 required (PyTorch)
- **AMD/Intel:** Theoretically via ROCm/OpenVINO but untested
- **Lip Sync:** Audio-driven single-image talking head generation
- **Style:** Generates realistic or stylized animations from single images
- **Container:** Docker-friendly
- **Community:** 11k+ GitHub stars

### ER-NeRF
- **URL:** https://github.com/Fictionarry/ER-NeRF
- **License:** Custom
- **GPU:** CUDA 11.3 required - strong NVIDIA dependency
- **Lip Sync:** Neural radiance field based talking portrait synthesis
- **Container:** Possible but complex
- **Assessment:** NOT GPU-agnostic. Skip for this project.

### GeneFace / GeneFace++
- **License:** Custom (research)
- **GPU:** CUDA required
- **Lip Sync:** 3D-aware talking heads with identity retention
- **Assessment:** CUDA-dependent. Not suitable for GPU-agnostic requirement.

### LivePortrait
- **URL:** https://github.com/KwaiVGI/LivePortrait
- **License:** Custom (research)
- **GPU Options:**
  - CUDA (native, best performance)
  - ONNX Runtime (community port - works on CPU, Apple Silicon)
  - FasterLivePortrait: https://github.com/warmshao/FasterLivePortrait (ONNX + TensorRT)
  - LiveTalk-Unity: ONNX + CoreML port
- **Lip Sync:** Portrait animation with stitching and retargeting
- **Container:** Docker-friendly via ONNX runtime
- **Assessment:** ONNX port makes it partially GPU-agnostic (CPU inference works but slow)

### MuseTalk (v1.5, March 2025)
- **URL:** https://github.com/TMElyralab/MuseTalk
- **License:** Custom
- **GPU:** CUDA 11.7 required, NVIDIA Tesla V100+ recommended
- **Lip Sync:** Real-time high quality lip sync (30fps+ on V100)
- **AMD/Intel:** No ROCm or OpenVINO support documented
- **Container:** Docker-friendly
- **Assessment:** CUDA-only. Excellent quality but NOT GPU-agnostic.

### Duix-Avatar
- **URL:** https://github.com/duixcom/Duix-Avatar
- **License:** Open source (check repo for specific license)
- **GPU:** NVIDIA GPU required
- **Features:**
  - Clone appearance/voice from ~10 second video
  - Fully offline operation
  - Docker-based deployment (3 microservices)
  - 8 language support
  - SQLite + file storage
- **Lip Sync:** Built-in natural lip-syncing
- **Container:** Docker-native architecture
- **Assessment:** Excellent Docker support but NVIDIA GPU required. NOT GPU-agnostic.

### Summary of Talking Head Models & GPU Agnosticism

| Model | CUDA Required | ONNX Available | OpenVINO | CPU Inference | GPU-Agnostic |
|-------|:---:|:---:|:---:|:---:|:---:|
| Wav2Lip | Training only | Yes (256x256) | Yes (2024) | Yes (slow) | Partial |
| SadTalker | Yes | No | No | No | No |
| ER-NeRF | Yes | No | No | No | No |
| LivePortrait | Default yes | Yes (community) | No | Yes (slow) | Partial |
| MuseTalk | Yes | No | No | No | No |
| Duix-Avatar | Yes | No | No | No | No |
| GeneFace++ | Yes | No | No | No | No |

---

## VTUBER AVATAR RENDERING SOLUTIONS

### VSeeFace
- **URL:** https://www.vseeface.icu/
- **License:** Free (closed source binary, but free to use)
- **GPU:** Unity-based, uses OpenGL/DirectX - GPU-agnostic
- **Platform:** Windows primarily (Wine on Linux)
- **VRM Support:** VRM 0.x only (not VRM 1.0)
- **Lip Sync:** Excellent
  - Standard: A, I, U, E, O visemes
  - Extended: SIL, CH, DD, FF, KK, NN, PP, RR, SS, TH
  - ARKit 52 blendshapes
  - Hybrid lip sync (camera + audio)
- **Container:** Difficult - Windows/Unity app, would need Wine in Docker
- **Assessment:** Great lip sync but NOT open source and NOT easily containerizable

### Automattic/VU-VRM
- **URL:** https://github.com/Automattic/VU-VRM
- **License:** Open source (GPL-2.0)
- **GPU:** WebGL (browser-based) - GPU-agnostic
- **Purpose:** Mic-driven VRM lip sync for OBS browser source
- **Lip Sync:** Volume-based mouth movement (VU meter style, not viseme-based)
- **Features:**
  - Load local .vrm files
  - Transparent background for compositing
  - No webcam needed
  - Works with VRoid Studio VRMs
- **Container:** Could run in headless browser Docker container
- **Limitation:** Simple volume-based lip sync, not phoneme/viseme-based
- **Assessment:** Too simple for quality lip sync but interesting as a lightweight option

### Kalidoface 3D
- **URL:** https://github.com/yeemachine/kalidoface-3d
- **License:** Open source
- **GPU:** WebGL (Three.js based) - GPU-agnostic
- **Lip Sync:** MediaPipe face tracking based
- **Features:**
  - VRM 3D avatar support
  - Full body tracking
  - Dynamic camera angles
  - Web-based
- **Container:** Could run in headless browser
- **Note:** Requires webcam input for tracking (not audio-driven)

### VMagicMirror
- **URL:** https://malaybaku.github.io/VMagicMirror/
- **License:** MIT
- **GPU:** Unity-based
- **Platform:** Windows only
- **Lip Sync:** Mic-based lip sync
- **Assessment:** Windows-only Unity app, NOT containerizable on Linux

---

## KALIDOKIT & MEDIAPIPE SOLUTIONS

### Kalidokit
- **URL:** https://github.com/yeemachine/kalidokit
- **License:** MIT
- **Purpose:** Blendshape & kinematics solver for MediaPipe/TensorFlow.js
- **GPU:** Runs in browser (WebGL) or Node.js - GPU-agnostic
- **CUDA Dependency:** NONE
- **Input:** MediaPipe face/pose/hand landmarks
- **Output:** Euler rotations + blendshape values for VRM/Live2D models
- **Lip Sync:** Calculates mouth blendshapes from face tracking data
- **Container:** Can run in headless browser or Node.js container
- **Community:** Well-known in VTuber community
- **Limitation:** Requires camera/video input - not audio-driven

### MediaPipe Face Mesh
- **License:** Apache 2.0 (Google)
- **GPU:** CPU, GPU (WebGL), or TPU - GPU-agnostic
- **Purpose:** 468 face landmarks + blendshape estimation
- **Output:** 52 ARKit-compatible blendshapes (includes mouth shapes for lip sync)
- **Container:** TensorFlow.js or Python versions both containerizable
- **Note:** Face tracking based, not audio-based lip sync

### Pipeline: Kalidokit + three-vrm
A proven combination for VTuber-style avatar animation:
1. MediaPipe detects face landmarks from camera
2. Kalidokit converts landmarks to VRM blendshapes
3. three-vrm applies blendshapes to VRM avatar
4. Three.js renders the scene
All WebGL-based, all GPU-agnostic, all containerizable.

---

## OPENUSD (PIXAR)

### Overview
- **URL:** https://openusd.org/
- **GitHub:** https://github.com/PixarAnimationStudios/OpenUSD
- **License:** Modified Apache 2.0
- **Latest:** OpenUSD 26.02 (February 2026), 25.11 (November 2025)
- **Governance:** Alliance for OpenUSD (Pixar, Apple, Adobe, Autodesk, NVIDIA)

### Hydra Rendering Framework
- **Storm renderer:** Supports OpenGL, Metal, Vulkan (experimental since OpenUSD 24.08)
- **Render delegates:** Pluggable architecture - can use different renderers
- **Available delegates:** Storm (built-in), hdOSPRay (Intel), hdEmbree, etc.

### GPU Support
- OpenGL + Vulkan = GPU-agnostic on Linux
- Intel's hdOSPRay delegate runs on CPU (ray tracing)
- **CUDA Dependency:** Only if using NVIDIA-specific render delegates

### Avatar & Animation
- Full skeletal animation support
- Used in Pixar's animation pipeline
- Character animation workflows documented
- SIGGRAPH 2024 presentation on "State and Future of USD Animation Characters"

### Containerization
- Complex build system but can be containerized
- Headless rendering possible via Storm renderer
- No official Docker images for avatar rendering

### Assessment for This Project
- **OVERKILL** - OpenUSD is a scene description format, not an avatar renderer
- Extremely complex to set up and maintain
- Designed for film/VFX pipelines with large teams
- Could be useful as a format if integrating with other tools
- **NOT RECOMMENDED** as primary renderer for this project

---

## NVIDIA AUDIO2FACE (OPEN-SOURCED)

### Overview
- **URL:** https://github.com/NVIDIA/Audio2Face-3D
- **Open-sourced:** September 2025
- **License:** Mixed
  - SDK (C++/CUDA): MIT license
  - Training framework (Python): Apache 2.0
  - Audio2Face-3D models: NVIDIA Open Model License (ONNX-TRT format)
  - Audio2Emotion models: Custom license (gated on HuggingFace)

### GPU Requirements
- **Optimized for:** NVIDIA GPUs via CUDA + TensorRT
- **CPU fallback:** Available in SDK for broader hardware support
- **ONNX format:** Models available in ONNX-TRT format

### Features
- AI-driven facial animation from audio input
- Outputs 52 ARKit blendshape weights
- Analyzes phonemes and intonation
- Accurate lip-sync + emotional expressions
- Real-time capable

### Assessment for This Project
- **Excellent lip sync quality** - industry standard
- CPU fallback makes it partially GPU-agnostic
- ONNX models could potentially run via ONNX Runtime on AMD/Intel
- Complex setup but well-documented
- **RECOMMENDED** as the audio-to-viseme component (not the renderer)
- Would pair well with Three.js + three-vrm for rendering

---

## COMPARATIVE MATRIX

| Solution | License | GPU-Agnostic | Containerizable | Cartoon Style | Lip Sync | Active | Complexity |
|----------|---------|:---:|:---:|:---:|:---:|:---:|:---:|
| Three.js + three-vrm | MIT | YES | YES | YES (VRM) | Via visemes | YES | Low |
| TalkingHead (met4citizen) | MIT | YES | YES | YES | Built-in (15 visemes) | YES | Low |
| Babylon.js + VRM | MIT | YES | YES | YES | Via morph targets | YES | Medium |
| Godot 4 + godot-vrm | MIT | YES | YES | YES | Custom needed | YES | Medium |
| Bevy | MIT/Apache | YES | Possible | Custom needed | Custom needed | YES | High |
| O3DE | Apache 2.0 | Partial (Vulkan only) | Difficult | Custom needed | Custom needed | Moderate | Very High |
| Inochi2D | BSD 2-clause | YES | Possible | YES (2D) | Via VMC | YES | Medium |
| Wav2Lip (ONNX) | Research | Partial | YES | N/A (video) | Core function | Moderate | Medium |
| LivePortrait (ONNX) | Research | Partial | YES | N/A (video) | Good | YES | Medium |
| NVIDIA Audio2Face | MIT/Mixed | Partial (CPU fallback) | YES | N/A (data only) | Excellent | YES | Medium |
| VSeeFace | Freeware | YES | NO | YES | Excellent | YES | N/A |
| Kalidokit | MIT | YES | YES | N/A (solver) | Camera-based | Moderate | Low |
| OpenUSD/Hydra | Apache 2.0 | YES | Difficult | Custom | No | YES | Very High |

---

## RECOMMENDED ARCHITECTURE

### Primary Recommendation: WebGL + VRM Pipeline

```
Architecture: Containerized WebGL Avatar Renderer

+--Docker Container------------------------------------------+
|                                                             |
|  +--Xvfb (Virtual Framebuffer)--+                          |
|  |                               |                          |
|  |  +--Headless Chromium------+  |                          |
|  |  |                         |  |    +--Audio Input--+     |
|  |  |  Three.js Scene         |  |    |  WAV/PCM     |     |
|  |  |  +--@pixiv/three-vrm--+ |  |    +------+--------+     |
|  |  |  | VRM Avatar Model   | |  |           |              |
|  |  |  | (cartoon style)    | |  |           v              |
|  |  |  +--------+-----------+ |  |    +------+--------+     |
|  |  |           |             |  |    | Audio2Viseme  |     |
|  |  |           v             |  |    | (ONNX/CPU)    |     |
|  |  |  +--------+-----------+ |  |    | Options:      |     |
|  |  |  | TalkingHead class  | |  |    | - Audio2Face  |     |
|  |  |  | (lip sync engine)  |<--------| - Wav2Lip     |     |
|  |  |  | Applies visemes    | |  |    | - Rhubarb     |     |
|  |  |  +--------+-----------+ |  |    +---------------+     |
|  |  |           |             |  |                           |
|  |  |           v             |  |                           |
|  |  |  WebGL Canvas Output    |  |                           |
|  |  |  (video frames)         |  |                           |
|  |  +-------------------------+  |                           |
|  +-------------------------------+                           |
|                                                             |
|  Output: Video stream / frame buffer / WebSocket            |
+-------------------------------------------------------------+
```

### Component Selection

1. **Renderer:** Three.js + @pixiv/three-vrm
   - Reason: GPU-agnostic WebGL, best VRM ecosystem, MIT licensed

2. **Avatar Format:** VRM (created in VRoid Studio)
   - Reason: Open standard, built-in viseme support, free cartoon avatars

3. **Lip Sync Engine:** TalkingHead class OR custom viseme mapper
   - Reason: Built-in audio-to-viseme, no external dependencies

4. **Audio-to-Viseme (Advanced):** NVIDIA Audio2Face ONNX with CPU fallback
   - Reason: Best quality, ONNX format enables GPU-agnostic inference

5. **Container:** Docker with Xvfb + headless Chromium
   - Reason: Proven approach, handles WebGL rendering in containers

6. **Alternative Container:** Node.js + headless-gl (for lighter weight)
   - Reason: No browser overhead, pure Node.js, but CPU-only rendering

### Alternative: Godot 4 Pipeline

If more control over 3D rendering is needed:
1. Godot 4 with Compatibility renderer (OpenGL ES 3.0)
2. godot-vrm plugin for VRM avatar loading
3. Custom GDScript for lip sync viseme application
4. Docker + Xvfb for headless container rendering
5. Export as server build with `--headless` flag

---

## SOURCES & REFERENCES

### Three.js / WebGL
- pixiv/three-vrm: https://github.com/pixiv/three-vrm
- TalkingHead: https://github.com/met4citizen/TalkingHead
- headless-gl: https://github.com/stackgl/headless-gl
- Headless Three.js gist: https://gist.github.com/crabmusket/b164c9b9d3c43db9bddbfb83afde0319
- Babylon.js VRM: https://github.com/virtual-cast/babylon-vrm-loader
- Ready Player Me Visage: https://github.com/readyplayerme/visage
- vroid-ai-companion: https://github.com/anjaydo/vroid-ai-companion
- Svelte VRM Live: https://github.com/thedexplorer/svelte-vrm-live

### VRM Ecosystem
- VRM Specification: https://github.com/vrm-c/vrm-specification
- VRM 1.0 Expressions: https://github.com/vrm-c/vrm-specification/blob/master/specification/VRMC_vrm-1.0/expressions.md
- VRM Viseme Tools: https://github.com/ImLevath/vrm-viseme-tools
- Open Source Avatars: https://github.com/ToxSam/open-source-avatars
- Gaussian-VRM: https://github.com/naruya/gaussian-vrm

### Godot
- Godot Renderers: https://docs.godotengine.org/en/stable/tutorials/rendering/renderers.html
- GodotServer-Docker: https://github.com/briancain/GodotServer-Docker
- docker-godot-headless: https://github.com/robpc/docker-godot-headless
- Godot dedicated server export: https://docs.godotengine.org/en/stable/tutorials/export/exporting_for_dedicated_servers.html

### O3DE
- O3DE Documentation: https://www.docs.o3de.org/docs/
- O3DE Docker: https://github.com/husarion/o3de-docker
- O3Tanks: https://github.com/loherangrin/o3tanks
- O3DE System Requirements: https://www.docs.o3de.org/docs/welcome-guide/requirements/

### Bevy
- Bevy Engine: https://bevyengine.org/
- Bevy 0.16: https://bevy.org/news/bevy-0-16/
- Bevy Rendering: https://taintedcoders.com/bevy/rendering

### Inochi2D
- Inochi2D: https://inochi2d.com/
- GitHub: https://github.com/Inochi2D/inochi2d
- Documentation: https://docs.inochi2d.com/

### Talking Head / AI Lip Sync
- SadTalker: https://github.com/OpenTalker/SadTalker
- MuseTalk: https://github.com/TMElyralab/MuseTalk
- LivePortrait: https://github.com/KwaiVGI/LivePortrait
- FasterLivePortrait: https://github.com/warmshao/FasterLivePortrait
- Wav2Lip ONNX 256: https://github.com/instant-high/wav2lip-onnx-256
- Wav2Lip OpenVINO: https://docs.openvino.ai/2024/notebooks/wav2lip-with-output.html
- Duix-Avatar: https://github.com/duixcom/Duix-Avatar
- ER-NeRF: https://github.com/Fictionarry/ER-NeRF

### VTuber / Avatar Tools
- VSeeFace: https://www.vseeface.icu/
- VU-VRM: https://github.com/Automattic/VU-VRM
- Kalidokit: https://github.com/yeemachine/kalidokit
- Kalidoface 3D: https://github.com/yeemachine/kalidoface-3d
- vpuppr (archived): https://github.com/virtual-puppet-project/vpuppr
- VMagicMirror: https://malaybaku.github.io/VMagicMirror/

### NVIDIA Audio2Face
- Blog post: https://developer.nvidia.com/blog/nvidia-open-sources-audio2face-animation-model
- SDK: https://github.com/NVIDIA/Audio2Face-3D-SDK
- Models: https://huggingface.co/nvidia/Audio2Face-3D-v3.0

### OpenUSD
- OpenUSD: https://openusd.org/
- GitHub: https://github.com/PixarAnimationStudios/OpenUSD
- Vulkan in Hydra: https://www.khronos.org/blog/vulkan-support-added-to-openusd-and-pixars-hydra-storm-renderer
- Alliance for OpenUSD: https://aousd.org/

### Headless Rendering / Docker
- Alpine Chrome: https://github.com/jlandure/alpine-chrome
- Puppeteer WebGL issues: https://github.com/puppeteer/puppeteer/issues/9555
- Chromium WebGL headless: https://bugs.chromium.org/p/chromium/issues/detail?id=617551
