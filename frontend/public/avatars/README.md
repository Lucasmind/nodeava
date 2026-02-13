# Avatar Models

Place your avatar GLB file here as `default-avatar.glb`.

**No avatar is included in this repo** because most free avatars use licenses (like CC BY-NC-SA) that are incompatible with Apache-2.0. You need to provide your own.

## Requirements

The GLB model must include:
- **ARKit blend shapes** (52 facial expressions)
- **Oculus Viseme blend shapes** (15 visemes for lip sync)
- Rigged skeleton with standard humanoid bone names

## Getting a Compatible Avatar

### Option 1: Ready Player Me (easiest)
1. Visit https://readyplayer.me
2. Create an avatar (cartoon or realistic)
3. Export as GLB with morph targets: ARKit, Oculus Visemes
4. Save as `default-avatar.glb` in this directory

### Option 2: VRoid Studio (free, more customizable)
1. Download VRoid Studio from https://vroid.com/en/studio
2. Create a character
3. Export as VRM
4. Convert VRM to GLB (VRM is GLB-based, may work directly with TalkingHead)

### Option 3: Pre-made models
Search for "VRM avatar free" or "Ready Player Me GLB" for compatible models.
Make sure the license allows your intended use.

## File naming
- `default-avatar.glb` is loaded by default
- Add more GLB files and reference them in `src/app/config.js`
