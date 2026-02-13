# Open-Source Lip Sync Technology Research

**Date:** 2026-02-10
**Requirements:** Real-time audio-to-viseme conversion, GPU-agnostic (no CUDA dependency), VRM or similar avatar formats, open source

---

## TABLE OF CONTENTS

1. [Executive Summary & Recommendations](#executive-summary--recommendations)
2. [Rhubarb Lip Sync](#1-rhubarb-lip-sync)
3. [OVR LipSync (Oculus/Meta)](#2-ovr-lipsync-oculusmeta)
4. [NVIDIA Audio2Face 3D](#3-nvidia-audio2face-3d)
5. [Lipsync-Engine (Browser-native)](#4-lipsync-engine-browser-native)
6. [wLipSync (WASM)](#5-wlipsync-wasm)
7. [Wawa-Lipsync](#6-wawa-lipsync)
8. [HeadTTS (met4citizen)](#7-headtts-met4citizen)
9. [TalkingHead (met4citizen)](#8-talkinghead-met4citizen)
10. [Rhubarb Lip Sync WASM Port](#9-rhubarb-lip-sync-wasm-port)
11. [Viseme Mapping Approaches](#10-viseme-mapping-approaches)
12. [ARKit Blendshape Standard](#11-arkit-blendshape-standard)
13. [Oculus Viseme Standard](#12-oculus-viseme-standard)
14. [Comparative Matrix](#comparative-matrix)
15. [Recommended Architecture for This Project](#recommended-architecture)

---

## EXECUTIVE SUMMARY & RECOMMENDATIONS

### Top Recommendations for GPU-Agnostic, Real-Time Lip Sync

**1. TalkingHead + HeadTTS (met4citizen) -- BEST FIT FOR VRM AVATARS**
- Complete browser-based pipeline: TTS with phoneme timestamps + VRM lip-sync
- HeadTTS provides free Kokoro neural TTS with Oculus visemes, MIT licensed
- TalkingHead renders VRM avatars with real-time lip sync from viseme data
- Zero GPU dependency (runs on CPU, WebGPU optional acceleration)
- Supports ARKit + Oculus viseme blendshapes
- Actively maintained (2025), 1k+ stars

**2. Lipsync-Engine (Amoner) -- BEST FOR CUSTOM RENDERING PIPELINES**
- Zero-dependency, renderer-agnostic streaming lip sync engine
- Pure browser: AudioWorklet + Web Audio API FFT analysis
- Outputs both 15 Oculus visemes and 6 Preston Blair shapes
- ~15KB minified, MIT licensed
- Works with any audio source (streaming TTS, microphone, files)
- Ideal for plugging into Three.js/VRM rendering

**3. Rhubarb Lip Sync + WASM Port -- BEST FOR OFFLINE/BATCH PROCESSING**
- Mature, battle-tested tool (2.4k stars)
- WASM port enables browser use, MIT licensed
- Not real-time (processes complete audio files)
- Language-independent phonetic recognizer available
- Good fallback for pre-recorded content

**4. wLipSync -- BEST FOR MFCC-BASED REAL-TIME ANALYSIS**
- WASM port of Unity's uLipSync
- MFCC-based audio analysis (more accurate than FFT-only)
- Requires pre-calibrated profiles (created in Unity)
- Single-file WASM bundle, no dependencies

---

## 1. RHUBARB LIP SYNC

**Repository:** https://github.com/DanielSWolf/rhubarb-lip-sync
**Stars:** 2.4k | **License:** MIT (all dependencies MIT/BSD)
**Platforms:** Windows, macOS, Linux
**Last Activity:** Mature/stable (510 commits)

### What It Does
Command-line tool that analyzes audio files and produces timed mouth-shape data. Originally designed for 2D animation (Hanna-Barbera style).

### Mouth Shapes
- 6 basic shapes (A-F): Preston Blair standard from classic animation
- 3 extended shapes (G, H, X): Additional refinement
- Shape X = closed mouth (silence)

### Speech Recognition
- **PocketSphinx** (default): English only, best accuracy
- **Phonetic recognizer**: Language-independent, recognizes individual sounds/syllables
- Optional dialog text input improves accuracy

### Output Formats
- TSV, XML, JSON
- DAT (for Moho/OpenToonz)
- Integrations: Adobe After Effects, Spine, Moho, OpenToonz, Vegas Pro

### GPU Requirements
- **None** -- pure CPU processing
- Not designed for real-time use; processes complete audio files

### Real-Time Capability
- **No** -- batch/offline processing only
- Processes audio files and outputs timed mouth shapes
- A WASM port exists (see section 9) but is also async/non-streaming

### Quality
- Very good for cartoon-style animation
- Widely used in game development and animation
- The 6+3 mouth shape system is proven for stylized characters

### Integration Approach
1. Generate audio via TTS
2. Run Rhubarb on the audio file
3. Parse JSON output for mouth shapes + timing
4. Map Rhubarb shapes (A-H, X) to VRM viseme blendshapes
5. Drive avatar animation from the timing data

### Mapping Rhubarb to Oculus Visemes
| Rhubarb | Description | Closest Oculus Viseme |
|---------|-------------|----------------------|
| A | Closed mouth (M, B, P) | PP |
| B | Slightly open (most consonants) | DD |
| C | Open mouth (AH, AW) | aa |
| D | Wide mouth (EE, I) | E / ih |
| E | Rounded mouth (OH, OO) | oh / ou |
| F | Upper teeth on lower lip (F, V) | FF |
| G | Tongue on teeth (L) | nn |
| H | Tongue behind teeth (SH, CH) | CH / SS |
| X | Silence | sil |

---

## 2. OVR LIPSYNC (OCULUS/META)

**Documentation:** https://developers.meta.com/horizon/documentation/
**License:** Oculus SDK License (proprietary, free for commercial use)
**Platforms:** Unity, Unreal Engine, Native C++

### What It Does
Real-time audio analysis producing 15 viseme weights. The industry standard for VR lip sync. Analyzes audio input from microphone or audio files.

### 15 Visemes
sil, PP, FF, TH, DD, kk, CH, SS, nn, RR, aa, E, ih, oh, ou

### GPU Requirements
- **CPU-based** audio analysis (no GPU needed for viseme generation)
- Runs on all platforms supporting the game engines

### Real-Time Capability
- **Yes** -- designed specifically for real-time VR applications
- Can process microphone input or audio streams
- Visemes interpolated over time for natural mouth motion

### Quality
- Industry standard for VR applications
- 15 visemes provide comprehensive mouth coverage
- Language-agnostic (works with any language)
- Smooth interpolation between viseme states

### Limitations
- **NOT open source** -- proprietary Oculus SDK license
- Binary-only distribution (DLL/native libraries)
- Any modifications to the SDK must be shared back with Meta
- Tied to Unity/Unreal/native C++ platforms
- Cannot run in browser or Docker without game engine

### Integration Approach
- Unity: OVRLipSync Unity package
- Unreal: OVRLipSync UE plugin
- Native: C/C++ API via OVRLipSync.dll
- NOT suitable for browser-based or containerized deployment

### Open-Source Fork: Lipstick
**Repository:** https://github.com/radiatoryang/lipstick
- Open-source fork for Unity under Oculus Audio license
- Not supported or endorsed by Oculus
- Adds ease-of-use improvements

---

## 3. NVIDIA AUDIO2FACE 3D

**Repository:** https://github.com/NVIDIA/Audio2Face-3D
**HuggingFace:** https://huggingface.co/nvidia/Audio2Face-3D-v3.0
**Stars:** 188 | **Open-Sourced:** September 2025

### License (Complex)
| Component | License |
|-----------|---------|
| Audio2Face-3D SDK | MIT |
| Training Framework | Apache 2.0 |
| Maya Plugin (MACE) | MIT |
| Unreal Engine 5 Plugin | MIT |
| Pre-trained Models | NVIDIA Open Model License |
| Audio2Emotion Models | Custom (Audio2Face-only usage) |
| NIM Container | NVIDIA Software License |

### Models Available
- **v3.0** (Diffusion-based, Transformer + HuBERT, 180M params)
- **v2.3 Mark**, **v2.3.1 Claire**, **v2.3.1 James** (Regression-based)
- **Audio2Emotion** v2.2 and v3.0

### GPU Requirements
- **NVIDIA GPU strongly recommended** -- designed for CUDA/TensorRT
- Tested on: T4, A10, A40, L4, L40S, A100, RTX 3080/3090/4080/4090/5090
- ONNX format models CAN run on CPU via ONNX Runtime but this is not recommended
- **NOT GPU-agnostic** -- optimized for NVIDIA hardware

### Real-Time Capability
- **Yes** -- optimized for low-latency interactive applications
- NIM supports multiple simultaneous audio streams
- Inference via TensorRT for maximum GPU performance

### Output Format
- Blendshape weights (2D float arrays)
- Direct mesh deformations
- Joint transformations
- FBX export via Maya plugin
- **Note:** Does NOT directly output ARKit blendshapes -- uses its own blendshape topology

### Quality
- State-of-the-art quality for realistic facial animation
- Diffusion model (v3.0) produces highest quality
- Includes emotion inference for expressive animation
- Best suited for realistic/photorealistic avatars

### Integration Platforms
- C++ SDK
- Autodesk Maya (MACE v2.0)
- Unreal Engine 5 (5.4, 5.5, 5.6)
- Docker (NIM, Training Framework)
- Python bindings

### Assessment for This Project
- **Pros:** Highest quality, MIT-licensed SDK, active NVIDIA support
- **Cons:** Requires NVIDIA GPU, complex deployment, designed for realistic (not cartoon) style, heavy infrastructure
- **Verdict:** Overkill for cartoon-style VRM avatars; best for photorealistic digital humans

---

## 4. LIPSYNC-ENGINE (BROWSER-NATIVE)

**Repository:** https://github.com/Amoner/lipsync-engine
**Stars:** 20 | **License:** MIT
**Package:** `@beer-digital/lipsync-engine` (npm)

### What It Does
Zero-dependency, renderer-agnostic streaming lip sync engine for browser-based animation. Real-time viseme detection via AudioWorklet + Web Audio API.

### Technical Architecture
1. **AudioWorklet** -- low-latency ring buffer for gapless streaming audio
2. **Web Audio API AnalyserNode** -- FFT analysis producing frequency band energies
3. **FrequencyAnalyzer** -- detects viseme patterns with smoothing and classification

### Input Modes
- Direct PCM feed (ideal for streaming TTS APIs like OpenAI Realtime)
- MediaStream attachment (microphone/WebRTC)
- HTML audio elements

### Viseme Output
**Extended Set (15 shapes, MPEG-4 compatible):**
- Outputs: `{open: 0-1, width: 0-1, round: 0-1}` + confidence + transition metadata
- Includes: sil, aa, E, I, O, U, PP, FF, TH, DD, kk, CH, SS, nn, RR

**Simplified Set (6 shapes, animation-friendly):**
- Maps to Preston Blair positions (A-F) for sprite-sheet/cel animation

### GPU Requirements
- **None** -- pure CPU, Web Audio API
- ~15KB minified bundle
- Runs at ~60fps (requestAnimationFrame)

### Real-Time Capability
- **Yes** -- designed for streaming real-time audio
- Works with OpenAI Realtime API WebSocket streams
- Includes `base64ToInt16()` utility for decoding base64 audio deltas
- Configurable analysis intervals

### Built-in Renderers
- **SVGMouthRenderer** -- procedural animated mouth geometry
- **CanvasRenderer** -- sprite-sheet based frame selection
- **CSSClassRenderer** -- data attributes for CSS/framework animations
- **Custom** -- listen to `'viseme'` events for Three.js/Pixi/Lottie integration

### Quality
- FFT-based analysis (less accurate than MFCC or phoneme-based)
- Good for cartoon/stylized animation
- Smooth transitions between viseme states
- Confidence scores enable quality-based filtering

### Integration with VRM/Three.js
```javascript
engine.on('viseme', (frame) => {
  // frame.shape = 'aa', 'E', etc.
  // frame.intensity = 0-1
  // Map to VRM blendshape weights
  vrm.expressionManager.setValue('viseme_' + frame.shape, frame.intensity);
});
```

---

## 5. WLIPSYNC (WASM)

**Repository:** https://github.com/mrxz/wLipSync
**License:** MIT
**Based on:** uLipSync (Unity MFCC-based lip sync)

### What It Does
MFCC-based lip sync library using WASM and WebAudio. Port of the popular Unity uLipSync plugin to web.

### Technical Approach
- Uses Mel-Frequency Cepstrum Coefficients (MFCC) for audio analysis
- MFCC represents characteristics of the human vocal tract
- More accurate than simple FFT analysis for phoneme detection
- Requires pre-calibrated profiles mapping MFCC features to visemes

### GPU Requirements
- **None** -- WASM + WebAudio, pure CPU
- Single-file bundle (WASM binary + audio worklet inlined)

### Real-Time Capability
- **Yes** -- processes audio in real-time via AudioWorklet

### Profile System
- Requires calibration profiles to map MFCC features to specific visemes
- Profiles must be created in Unity using uLipSync editor tools
- JSON or compact binary profile format
- This is a significant limitation: you need Unity to create profiles

### Quality
- Higher accuracy than FFT-only approaches
- MFCC analysis is closer to how speech recognition works
- Well-proven in Unity VR/game development (uLipSync)

### Limitations
- **Requires Unity** to create calibration profiles (major barrier)
- Newer project, smaller community
- Less documentation than alternatives

---

## 6. WAWA-LIPSYNC

**Repository:** https://github.com/wass08/wawa-lipsync
**License:** MIT (inferred from creator's other projects)
**Creator:** Wawa Sensei (popular Three.js educator)

### What It Does
Browser-native, real-time lip sync library designed specifically for React Three Fiber and Three.js applications. Built for AI chatbot use cases.

### Technical Approach
- Listens to any audio source and outputs lipsync data instantly
- No server-side processing required
- Designed for integration with 3D avatars in web applications

### GPU Requirements
- **None** -- browser-based audio analysis
- Uses Web Audio API

### Real-Time Capability
- **Yes** -- designed for real-time streaming use

### Integration
- Native React Three Fiber integration
- Works with Ready Player Me avatars
- Three.js compatible
- Designed for AI chatbot templates

### Quality
- Focused on web/game use cases
- Good for cartoon/stylized characters
- Active community around Wawa Sensei's tutorials

---

## 7. HEADTTS (MET4CITIZEN)

**Repository:** https://github.com/met4citizen/HeadTTS
**Stars:** 106 | **License:** MIT
**NPM:** `@met4citizen/headtts`
**Last Update:** January 2025

### What It Does
Free neural text-to-speech solution that provides phoneme-level timestamps AND Oculus visemes alongside audio output. Uses the Kokoro-82M neural model.

### Key Innovation
This is not just a TTS engine -- it produces synchronized viseme data with every utterance, making it a complete TTS+lip-sync solution in one package.

### Output Per Utterance
- Audio (WAV/PCM)
- Word-level timestamps
- Phoneme-level timestamps
- Oculus viseme classifications (15 visemes)

### Deployment Options
| Mode | Runtime | Speed |
|------|---------|-------|
| Browser (WebGPU) | Chrome/Edge desktop | 3x real-time |
| Browser (WASM) | Any modern browser | ~10x slower than WebGPU |
| Node.js Server | WebSocket or REST | CPU-based |

### Model Precision Options
fp32, fp16, q8, q4, q4f16 -- enabling trade-offs between quality and speed

### GPU Requirements
- **None required** -- runs on CPU (WASM or Node.js)
- **WebGPU optional** -- 3x faster than real-time when available
- No CUDA dependency

### Language Support
- English only (based on CMU Pronunciation Dictionary, 134k+ words)
- Built-in phoneme-to-viseme mapping for American English

### Quality
- Neural TTS (Kokoro/StyleTTS 2) -- high quality voices
- Phoneme-level timing precision
- Multiple voice options

### Integration with TalkingHead
HeadTTS is specifically designed as the TTS component for the TalkingHead avatar system. The viseme output format directly matches what TalkingHead expects.

### Assessment for This Project
- **Pros:** Free, MIT licensed, no server needed, produces both audio AND visemes, WebGPU acceleration, perfect VRM integration via TalkingHead
- **Cons:** English only, requires WebGPU for best speed, newer project
- **Verdict:** Excellent choice for English-language avatar projects

---

## 8. TALKINGHEAD (MET4CITIZEN)

**Repository:** https://github.com/met4citizen/TalkingHead
**Stars:** 1k+ | **License:** MIT
**NPM:** `@met4citizen/talkinghead`
**Last Update:** December 2024

### What It Does
Browser-based JavaScript class that renders a full-body 3D avatar with real-time lip sync, facial expressions, body animations, and physics simulation.

### Avatar Support
- **Format:** GLB (with Mixamo-compatible rig)
- **Required blendshapes:** ARKit (52 shapes) AND Oculus visemes (15 shapes)
- VRM avatars can be converted to GLB with proper blendshapes
- Ready Player Me avatars supported
- Custom avatar creation guide included

### Viseme System
15 Oculus viseme codes: aa, E, I, O, U, PP, SS, TH, CH, FF, kk, nn, RR, DD, sil

### Language Support (Built-in Lip Sync)
English, German, French, Finnish, Lithuanian

### TTS Integration Options
| TTS Provider | Method | Viseme Source |
|-------------|--------|---------------|
| HeadTTS (Kokoro) | In-browser/local | Native viseme output |
| Google Cloud TTS | Cloud API | Built-in phoneme-to-viseme |
| ElevenLabs | WebSocket API | Word timestamps |
| Microsoft Azure | Cloud API | Native viseme IDs (100+ languages) |
| HeadAudio | Audio analysis | Audio-driven viseme detection |
| Custom TTS | Any with timestamps | Phoneme or word-level mapping |

### HeadAudio Module
Separate module providing audio-driven, real-time viseme detection WITHOUT text/transcription. Operates as a Web Audio worklet node -- useful for any audio source.

### Features Beyond Lip Sync
- Emoji-to-facial-expression conversion
- Idle animations and gestures
- Physics simulation (dynamic bones: hair, clothing)
- Configurable frame rate (default 30 FPS)
- Device pixel ratio adjustment

### GPU Requirements
- **WebGL** (required) -- works on all modern browsers
- **WebGPU** recommended for HeadTTS acceleration
- No CUDA dependency
- GPU-agnostic (Intel, AMD, NVIDIA, Apple Silicon)

### Real-Time Capability
- **Yes** -- designed for real-time conversational use
- Phoneme-based lip sync with smooth transitions
- 30 FPS default, configurable

### Deployment
- CDN (jsdelivr)
- NPM package
- Single HTML file minimal setup
- Can run in Docker via headless browser

### Quality
- Professional quality for stylized/cartoon avatars
- Smooth viseme transitions
- Full body animation
- Emotion expression support
- Published in academic venues (CHI 2025)

### Academic Use Cases
- Human-AI group conversation research (DialogLab)
- Video conferencing with real-time transcription
- Fully in-browser AI agents (EdgeSpeaker)
- Interactive applications

### Assessment for This Project
- **Pros:** Complete avatar rendering + lip sync solution, MIT licensed, GPU-agnostic, VRM-compatible workflow, multiple TTS options, actively maintained, academic credibility
- **Cons:** Requires specific blendshape setup on avatars, English-best for built-in lip sync
- **Verdict:** Top recommendation for browser-based VRM avatar with lip sync

---

## 9. RHUBARB LIP SYNC WASM PORT

**Repository:** https://github.com/danieloquelis/rhubarb-lip-sync-wasm
**Stars:** 21 | **License:** MIT
**NPM:** `rhubarb-lip-sync-wasm`
**Last Update:** March 2025 (v0.1.8, beta)

### What It Does
WebAssembly port of the original Rhubarb Lip Sync C++ codebase. Enables Rhubarb's lip sync analysis to run in JavaScript/TypeScript environments.

### Technical Details
- Compiled from C++ to WASM
- PocketSphinx speech recognition included
- TypeScript support
- Async/Promise-based API

### Usage
```javascript
import { Rhubarb } from 'rhubarb-lip-sync-wasm';
const result = await Rhubarb.getLipSync(audioBuffer16kHz, dialogText);
// Returns: [{start, end, shape: 'A'|'B'|...|'X'}]
```

### GPU Requirements
- **None** -- pure WASM, CPU only

### Real-Time Capability
- **No** -- processes complete audio buffers (async)
- Suitable for pre-processing TTS output before playback
- Not designed for streaming audio

### Quality
- Same quality as native Rhubarb (PocketSphinx + phonetic analysis)
- 9 mouth shapes (A-H, X)
- Dialog text guidance improves accuracy

### Assessment
- Good for scenarios where TTS output is generated first, then lip sync computed before playback
- Adds latency (TTS generation + lip sync processing + then playback)
- Better suited for turn-based conversations than real-time streaming

---

## 10. VISEME MAPPING APPROACHES

### Overview of Phoneme-to-Viseme Mapping

Visemes are visual representations of phonemes -- there is no one-to-one correspondence, as several phonemes often map to a single viseme (e.g., /s/ and /z/ look identical on the face).

### Common Approaches

#### 1. Rule-Based Mapping (Simplest)
- Static lookup table: phoneme -> viseme
- Fast, deterministic, no ML needed
- Used by TalkingHead, HeadTTS, most game engines
- Quality depends on table accuracy and transition smoothing

#### 2. MFCC Audio Analysis (uLipSync / wLipSync)
- Analyzes frequency characteristics of audio
- Mel-Frequency Cepstral Coefficients represent vocal tract shape
- Real-time, no text needed
- Requires calibration profiles
- Higher accuracy than simple FFT

#### 3. FFT/Frequency Band Analysis (Lipsync-Engine)
- Divides audio spectrum into frequency bands
- Maps energy distribution to viseme parameters
- Fast, lightweight, zero-dependency
- Less accurate than MFCC but good enough for cartoon style
- Works with any audio source

#### 4. Deep Learning / Neural (Audio2Face, recent research)
- Neural networks trained on audio-visual speech data
- Highest quality, handles emotion and prosody
- Typically requires GPU
- Disentangled phoneme-prosody approaches allow per-frame control

#### 5. Phoneme-First Pipeline (HeadTTS approach)
- TTS engine generates phonemes + timing as byproduct
- Map phonemes to visemes using lookup table
- Most accurate timing since phonemes are ground truth from TTS
- Only works when you control the TTS pipeline

### Recommended Approach for This Project

**Phoneme-First Pipeline** (HeadTTS + TalkingHead):
1. Text -> HeadTTS -> Audio + Phoneme timestamps + Oculus visemes
2. Visemes + timestamps -> TalkingHead -> VRM avatar animation
3. Audio -> Browser audio playback (synchronized)

This gives the best accuracy because visemes come directly from the TTS phoneme output, not from audio analysis.

**Fallback for external audio** (Lipsync-Engine):
- When audio comes from external source (no phoneme data)
- Use FFT-based real-time analysis
- Lower accuracy but works with any audio

---

## 11. ARKIT BLENDSHAPE STANDARD

### Overview
Apple's ARKit defines 52 facial blendshape coefficients for face tracking, widely adopted as a standard for facial animation beyond Apple devices.

### The 52 Blendshapes
Organized by facial region:

**Eyes (14):** eyeBlinkLeft, eyeBlinkRight, eyeLookDownLeft, eyeLookDownRight, eyeLookInLeft, eyeLookInRight, eyeLookOutLeft, eyeLookOutRight, eyeLookUpLeft, eyeLookUpRight, eyeSquintLeft, eyeSquintRight, eyeWideLeft, eyeWideRight

**Brows (4):** browDownLeft, browDownRight, browInnerUp, browOuterUpLeft, browOuterUpRight

**Jaw (3):** jawForward, jawLeft, jawOpen, jawRight

**Mouth (23):** mouthClose, mouthDimpleLeft, mouthDimpleRight, mouthFrownLeft, mouthFrownRight, mouthFunnel, mouthLeft, mouthLowerDownLeft, mouthLowerDownRight, mouthPressLeft, mouthPressRight, mouthPucker, mouthRight, mouthRollLower, mouthRollUpper, mouthShrugLower, mouthShrugUpper, mouthSmileLeft, mouthSmileRight, mouthStretchLeft, mouthStretchRight, mouthUpperUpLeft, mouthUpperUpRight

**Cheeks (4):** cheekPuff, cheekSquintLeft, cheekSquintRight

**Nose (2):** noseSneerLeft, noseSneerRight

**Tongue (1):** tongueOut

### Value Range
Each blendshape: 0.0 (neutral) to 1.0 (maximum expression)

### Relevance to Lip Sync
- Mouth shapes for lip sync are composed from COMBINATIONS of these blendshapes
- More expressive than discrete visemes (continuous blend)
- Industry standard used by Ready Player Me, VRoid, Apple devices
- VRM format supports ARKit blendshapes natively

### Relationship to FACS
- Based on Facial Action Coding System (FACS) action units
- More intuitive naming than raw FACS AU numbers
- Widely understood by 3D artists

---

## 12. OCULUS VISEME STANDARD

### The 15 Visemes

| ID | Name | Example Phonemes | Example Words |
|----|------|-----------------|---------------|
| 0 | sil | (silence) | -- |
| 1 | PP | p, b, m | put, bat, mat |
| 2 | FF | f, v | fat, vat |
| 3 | TH | th | think, that |
| 4 | DD | t, d | tip, dip |
| 5 | kk | k, g | call, gap |
| 6 | CH | tS, dZ, S | chair, join, she |
| 7 | SS | s, z | sir, zeal |
| 8 | nn | n, l | not, lot |
| 9 | RR | r | red |
| 10 | aa | A: | car |
| 11 | E | e | bed |
| 12 | ih | I | tip |
| 13 | oh | O | top |
| 14 | ou | U | book |

### How It Works
- Audio analysis produces weights for each viseme (0.0 to 1.0)
- Multiple visemes can be active simultaneously (blended)
- Interpolation between frames creates smooth mouth motion
- Language-agnostic (designed to work with any language)

### Adoption
- VRChat (standard for VRC avatars)
- Ready Player Me
- TalkingHead (met4citizen)
- HeadTTS (met4citizen)
- Many VRM avatar creation tools
- De facto standard for web-based avatar lip sync

### Comparison with ARKit
| Feature | Oculus Visemes | ARKit Blendshapes |
|---------|---------------|-------------------|
| Count | 15 | 52 (full face) |
| Focus | Mouth/lip sync | Full face |
| Complexity | Simple | Complex |
| Use case | Real-time lip sync | Full facial animation |
| VRM support | Yes | Yes |
| Composable | Standalone | Can be combined |

---

## COMPARATIVE MATRIX

| Solution | License | GPU Required | Real-Time | Quality | Browser | VRM/3D | Streaming Audio | Complexity |
|----------|---------|-------------|-----------|---------|---------|--------|----------------|------------|
| **TalkingHead** | MIT | No (WebGL) | Yes | High | Yes | Yes (GLB+blendshapes) | Yes (via HeadTTS/HeadAudio) | Medium |
| **HeadTTS** | MIT | No (WebGPU optional) | Yes | High | Yes | Outputs visemes for TalkingHead | Yes (streaming TTS) | Low |
| **Lipsync-Engine** | MIT | No | Yes | Medium | Yes | Renderer-agnostic | Yes | Low |
| **wLipSync** | MIT | No | Yes | High (MFCC) | Yes (WASM) | Renderer-agnostic | Yes | Medium (needs Unity profiles) |
| **Wawa-Lipsync** | MIT | No | Yes | Medium | Yes | React Three Fiber | Yes | Low |
| **Rhubarb** | MIT | No | No (batch) | High | Via WASM port | Outputs timing data | No | Low |
| **Rhubarb WASM** | MIT | No | No (async) | High | Yes | Outputs timing data | No | Low |
| **OVR LipSync** | Proprietary | No | Yes | Very High | No | Unity/Unreal only | Yes | Medium |
| **Audio2Face** | Mixed (MIT SDK) | NVIDIA GPU | Yes | Highest | No | UE5/Maya/C++ | Yes | High |

### Ranking for This Project's Requirements

**GPU-agnostic + Real-time + VRM + Open Source:**

1. **TalkingHead + HeadTTS** -- Score: 10/10
   - Checks every box. Complete pipeline.

2. **Lipsync-Engine** -- Score: 8/10
   - Missing avatar rendering (bring your own), but perfect lip sync component

3. **wLipSync** -- Score: 7/10
   - Excellent accuracy, but Unity dependency for profiles is a barrier

4. **Wawa-Lipsync** -- Score: 7/10
   - Good for React Three Fiber projects, less documented

5. **Rhubarb WASM** -- Score: 5/10
   - Not real-time, but good quality for batch processing

6. **Audio2Face** -- Score: 3/10
   - Requires NVIDIA GPU, overly complex for cartoon style

7. **OVR LipSync** -- Score: 2/10
   - Not open source, tied to game engines

---

## RECOMMENDED ARCHITECTURE

### Primary Pipeline (Real-Time Conversational)

```
User Speech -> STT Engine -> Text
                                |
                                v
                Text -> LLM -> Response Text
                                |
                                v
                Response Text -> HeadTTS (Kokoro)
                                |
                                +-> Audio (WAV/PCM)
                                +-> Phoneme Timestamps
                                +-> Oculus Visemes (15)
                                |
                                v
                Audio + Visemes -> TalkingHead
                                |
                                v
                VRM Avatar with Lip Sync (WebGL/Browser)
```

### Fallback Pipeline (External Audio Sources)

```
External Audio -> Lipsync-Engine (AudioWorklet + FFT)
                    |
                    +-> Viseme Events (15 Oculus or 6 Preston Blair)
                    |
                    v
                Viseme Events -> Three.js VRM Renderer
                    |
                    v
                VRM Avatar with Lip Sync
```

### Key Technical Decisions

1. **Viseme Standard:** Oculus 15 visemes (widest adoption, VRM native support)
2. **TTS Engine:** HeadTTS/Kokoro (free, MIT, produces visemes natively)
3. **Avatar Renderer:** TalkingHead or custom Three.js + @pixiv/three-vrm
4. **Lip Sync Method:** Phoneme-first when possible, FFT fallback for external audio
5. **Avatar Format:** GLB with ARKit + Oculus blendshapes (VRM-compatible workflow)
