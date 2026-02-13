# Avatar Models

NodeAva ships with a default avatar: `default-avatar.glb`.

## Included Avatar

| File | Source | License |
|------|--------|---------|
| `default-avatar.glb` | [Ready Player Me](https://readyplayer.me) | CC BY-NC-SA 4.0 |

**Important:** This avatar is licensed separately from the project code (Apache-2.0). It is included for personal and educational use. If you use NodeAva commercially, replace it with your own avatar. See `THIRD-PARTY-LICENSES.md` for details.

## Adding Your Own Avatar

### Option 1: VRoid Studio (free, recommended)
1. Download VRoid Studio from https://vroid.com/en/studio
2. Create a character
3. Export as VRM (TalkingHead supports VRM natively — no conversion needed)
4. Save in this directory and update `config.js`

### Option 2: Pre-made models
Search for "VRM avatar free" or "GLB avatar ARKit blend shapes" for compatible models.
Make sure the license allows your intended use.

## Requirements

GLB/VRM models must include:
- **ARKit blend shapes** (52 facial expressions)
- **Oculus Viseme blend shapes** (15 visemes for lip sync)
- Rigged skeleton with standard humanoid bone names

## Switching Avatars

Edit `avatarUrl` in `src/app/config.js`:

```javascript
avatarUrl: '/avatars/your-avatar.glb',
avatarBody: 'F',  // 'F' for female, 'M' for male
```
