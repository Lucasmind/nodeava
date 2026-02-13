# Avatar Models

Place your avatar GLB file here as `default-avatar.glb`.

**No avatar is included in this repo** because most free avatars use licenses (like CC BY-NC-SA) that are incompatible with Apache-2.0. You need to provide your own.

## Requirements

The GLB model must include:
- **ARKit blend shapes** (52 facial expressions)
- **Oculus Viseme blend shapes** (15 visemes for lip sync)
- Rigged skeleton with standard humanoid bone names

## Getting a Compatible Avatar

### Option 1: VRoid Studio (free, recommended)
1. Download VRoid Studio from https://vroid.com/en/studio
2. Create a character
3. Export as VRM (TalkingHead supports VRM natively — no conversion needed)
4. Rename the file to `default-avatar.glb` and place it in this directory

### Option 2: Pre-made models
Search for "VRM avatar free" or "GLB avatar ARKit blend shapes" for compatible models.
Make sure the license allows your intended use.

## File naming
- `default-avatar.glb` is loaded by default
- Add more GLB files and reference them in `src/app/config.js`
