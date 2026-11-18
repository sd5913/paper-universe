# Crystal Cavern (Scene 3) — Progress Documentation

## Project Overview

**Project:** The Folded Lumen (折光之森) — Scene 3: Crystal Cavern (水晶洞窟)

This is the upgraded version of the team project. The original "Secret World" module
has been replaced by Scene 3: Crystal Cavern, following the team's revised three-scene
storyline.

## Responsible Member

- **Member:** 圈圈 (quanquan)
- **Role:** Scene 3 (Crystal Cavern) + Global Audiovisual

## Story Context

The player's paper spirit (Foldy/Ori) follows paper butterflies into an underground
cavern. The cavern is dark and needs to be lit up by combining natural elements
with minerals to activate the Origami Heart — the energy core of the entire
paper world.

## Synthesis Chain (Three Steps)

| Step | Recipe | Output | Description |
|------|--------|--------|-------------|
| 1 | Rock + Rain | Raw Stone (原石) | Rain erodes rock to form raw crystal ore |
| 2 | Raw Stone + Sun | Luminous Crystal (发光水晶) | Sunlight charges the ore into a glowing crystal |
| 3 | Luminous Crystal + Wildflowers | Origami Heart (折纸之心) | The heart activates, lighting up the entire cavern |

## Technical Stack

- **Rendering:** p5.js (local copy bundled)
- **Architecture:** Vanilla JavaScript, modular structure
- **Audio:** Web Audio API (synthesized sounds, no external audio files)
- **Visual Style:** Paper-cut / pop-up-book aesthetic with drop shadows and layered paper textures
- **Background:** User-provided photograph integrated as canvas background

## File Structure

```
modules/assets/crystal-cavern/
├── index.html              # Entry point with cache-busting and error overlay
├── css/
│   └── style.css           # Page styling around the p5 canvas
├── js/
│   ├── p5.min.js           # Local p5.js library (v1.x)
│   ├── config.js           # Palette, canvas config, recipes, base elements
│   ├── audio.js            # AudioManager — Web Audio synthesized sound effects
│   ├── texture.js          # TextureManager — background image, paper overlay, light spots
│   ├── cavern.js           # CrystalCavern — main game logic, drag synthesis, element rendering
│   └── sketch.js           # p5 lifecycle (preload, setup, draw, mouse/key handlers)
└── assets/
    └── background.jpg      # External background image
```

## Key Features Implemented

### Interactive Elements
- **Rock (岩石):** Paper-cut polygon with layered shading
- **Rain (春雨):** Animated rain cloud with falling drops
- **Sun (太阳):** Radiating paper-cut sun with rotating rays (frame removed per user request)
- **Wildflowers (野花丛):** Cluster of paper-cut flowers with petals

### Drag-and-Overlap Synthesis
- Click and drag any element onto another to attempt synthesis
- Visual feedback: scale pulse, color flash, particle burst on success
- Notification banner shows recipe name and description
- Discovered recipes are tracked and displayed

### Visual System
- Paper-cut helper functions (`drawPaperShape`, `drawPaperLayered`, `drawPaperEllipse`)
- Drop shadows via `drawingContext.shadowBlur`
- Layered paper textures for depth
- Vine/root connectors between ground-integrated elements
- External background image with paper texture overlay

### Audio
- Paper fold noise on drag
- Crystal chime on synthesis
- Rain drop sound on rain interaction
- Discovery fanfare on new recipe found
- Heart awakening chord progression on final synthesis

### Heart Activation (Climax)
- When the Origami Heart is synthesized, the cavern gradually lights up
- Camera zoom effect toward the heart
- Growing tree of light animation
- Particle confetti celebration

### Debug & Error Handling
- Global `window.onerror` overlay for visible JS errors
- `D` key toggles debug panel (FPS, element count, state)
- Per-element `try/catch` to prevent one element from breaking all rendering
- Safe RGB fill/stroke calls to avoid hex+alpha browser issues

## Streamlit Integration

The project is integrated into the Streamlit app via `modules/crystal_cavern.py`,
which reads all project files and inlines them (CSS, JS, and base64-encoded
background image) into a single HTML string rendered via `components.html()`.

## Development Timeline

1. Initial Crystal Cavern prototype built from scratch
2. Fixed "blue background only" bug — elements starting at scale 0, unsafe color calls
3. Switched from CDN to local p5.js for offline reliability
4. Integrated user-provided paper-cut drawing helper functions
5. Restyled to warm brown pop-up-book aesthetic matching reference image
6. Replaced generated background with user-provided photograph
7. Fixed drag ghosting with cache-busting (`?v=3`) and safety clear
8. Removed sun frame/box per user request
9. Integrated into Streamlit app structure

## Known Issues

- p5.min.js is ~1MB; consider CDN fallback for production
- Background image is ~700KB; may affect load time on slow connections
- The Streamlit iframe inlining approach increases page payload

## Next Steps

- Add Scene 1 (Weather Valley) and Scene 2 (Flower Meadow) integration
- Implement scene transition between the three scenes
- Add the paper spirit (Foldy/Ori) character animation
- Polish the final tree-of-light climax animation
