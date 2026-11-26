# Design & Development Process — Living World: The Origami Meadow

**Project:** Paper Universe (Interactive Multi-World Web Experience)  
**Module:** Living World: The Origami Meadow (`modules/living.py`)  
**Tech Stack:** Python, Streamlit, HTML5/CSS3, JavaScript (ES6+), p5.js, Web Audio API  
**Target Display:** 1920 × 1080 (16:9 Full-Bleed Exhibition Viewport, Retina `pixelDensity(2)`)  

---

## 1. Project Concept & Aesthetic Philosophy

### 1.1 Vision & Narrative Framing
**Living World: The Origami Meadow** is the foundational ecological chapter of **Paper Universe**, an interactive multi-module web experience inspired by physical pop-up books and handcrafted paper-cut dioramas. Rather than presenting users with complex menus or text-heavy tutorials, the experience opens directly into a tranquil origami meadow at dawn. Through gentle, tactile curiosity—waking a sleeping Flower Fairy, scooping pond water to nurture sprouts, shifting time from Day to Dusk, and gathering glowing fireflies—users gradually awaken a living miniature ecosystem before turning the physical page corner into *Weather World*.

### 1.2 Core Design Principles
1. **Tactile Paper Materiality:** Every visual element is composed as a layered paper cutout with calibrated drop shadows, organic silhouettes, and warm, restorative color palettes that evoke physical craft rather than cold digital UI.
2. **Artwork-First Immersion (Zero-Clutter Canvas):** All external browser chrome, Streamlit headers, sidebars, and redundant title banners are stripped away so the 16:9 canvas fills 100% of the viewport like an interactive gallery installation.
3. **Human-Curated Hybrid Pipeline:** Instead of relying on heavy 3D meshes or unpredictable end-to-end generative rendering, custom illustrated sprites are combined with deterministic **p5.js** procedural motion—ensuring high fault tolerance, instant responsiveness, and consistent artistic authorship.

---

## 2. Collaborative Architecture & System Integration

**Paper Universe** is structured as a modular multi-world application where individual worlds operate independently inside a unified entry shell (`app.py`):

- **`app.py` (Application Shell & Viewport Controller):** Configures wide layout mode, suppresses default Streamlit headers/sidebars via injected CSS, enforces full-bleed `100vw × 100vh` iframe sizing, and routes directly into the active world module (`living.render()`).
- **`modules/living.py` (Living World Engine):** Encapsulates asset serialization (`load_asset_data_uri`), state management, interactive physics, particle emitters, procedural audio synthesis, and the full-screen p5.js canvas.
- **Sibling Modules (`weather.py`, `secret.py`, `experience.py`):** Connected conceptually via the pop-up book page-flip transition at the bottom-right corner of the meadow.
- **`assets/` (Shared Visual Library):** Centralized repository of high-resolution transparent PNG sprites (`fairy.PNG`, `dialog.PNG`, `lantern.PNG`, `bucket.PNG`, `firefly.PNG`, `frog.PNG`, `flower1.PNG`–`flower3.PNG`, `mushroom1.PNG`, `lotus.png`, `moon.png`, `star.png`, `owl.png`, etc.).

---

## 3. Visual Asset Pipeline & Procedural Synthesis

### 3.1 Custom Paper-Cut Sprite Library
All key focal characters and botanical elements were illustrated as layered paper-cut sprites with clean alpha channels:
- **Characters & Creatures:** Sleeping/awakened Flower Fairy (`fairy.PNG`), interactive pond Frog (`frog.PNG`), nocturnal Owl (`owl.png`), and glowing Fireflies (`firefly.PNG`).
- **Interactive Props & UI Scrolls:** Illustrated 4-step guide scroll (`dialog.PNG`), brass/paper Firefly Lantern (`lantern.PNG`), and wooden Watering Can (`bucket.PNG`).
- **Flora & Celestial Elements:** Multi-stage blooming flowers (`flower1.PNG`–`flower3.PNG`), forest mushrooms (`mushroom1.PNG`), pond lotus (`lotus.png`), crescent moon (`moon.png`), and twinkling dusk stars (`star.png`).

### 3.2 Base64 Data URI Serialization (`load_asset_data_uri`)
Because Streamlit renders custom HTML/JS components inside sandboxed iframes, relative file paths (`assets/...`) frequently break across local and cloud deployments. To solve this, `modules/living.py` implements a recursive path resolver (`load_asset_data_uri`) that locates each image file (handling case-insensitive extensions like `.PNG` and `.png`) and encodes it into an inline `data:image/png;base64,...` URI at runtime—guaranteeing 100% asset reliability with zero external network latency.

### 3.3 Real-Time Procedural Animation (p5.js)
To breathe life into static paper layers, p5.js continuously computes lightweight procedural behaviors at 60 FPS:
- **Environmental Motion:** Wind-driven grass blade oscillation (`grassBlades`), expanding water ripples (`ripples`), drifting leaves (`fallingLeaves`), and gentle fairy levitation.
- **Dynamic Day/Dusk Atmosphere:** Smooth color interpolation between sunlit meadow greens and deep twilight blues, paired with radial lantern light falloff and firefly flight trajectories.
- **Tactile Feedback & Sound:** Synchronized particle bursts (`harvestParticles`, `skyEnergyOrbs`) and Web Audio API harmonic chimes triggered on every watering, blooming, catching, and crafting action.

---

## 4. Core Gameplay Loop & Interaction Mechanics

The user journey follows a natural, four-stage discovery loop guided by the **Origami Meadow Guide** (`dialog.PNG`):

1. **Stage 1 — Awakening the Meadow:**
   - The user clicks the **Origami Meadow Guide** pagination (`1/4` to `4/4`) or taps the mushroom door to wake the sleeping Flower Fairy.
2. **Stage 2 — Watering & Botanical Growth:**
   - The user picks up the **Watering Can** (`bucket.PNG`), dips it into the pond to replenish water, and holds the mouse button over soil sprouts—triggering water droplets (`waterDrops`) and blooming multi-stage paper flowers (`flower1`–`flower3`) that increase overall `gardenVitality`.
3. **Stage 3 — Day/Dusk Cycle & Firefly Gathering:**
   - Toggling the **Day/Dusk** lighting switch transitions the meadow into twilight, activating nocturnal creatures and spawning glowing fireflies. Users catch **5 fireflies** to illuminate the fairy's lantern (`lantern.PNG`) and harvest sky energy orbs.
4. **Stage 4 — Workbench Crafting & Page-Corner Transition:**
   - Gathered resources (flowers, mushrooms, water, firefly light) are combined at the meadow **Workbench** to craft ecological wonders, unlocking the interactive **page-corner curl** to transition seamlessly into *Weather World*.

---

## 5. Iterative Development Timeline & Refinements

Based on our Git commit history (`main` branch) and continuous visual testing, the module evolved through five major milestones:

### Phase 1: Core Canvas & Asset Integration
- Established the base p5.js meadow scene (`860 × 560`), integrated custom transparent PNG sprites, and implemented `load_asset_data_uri()` for reliable asset embedding.
- Built core state machines for the Flower Fairy, watering can physics, sprout growth stages, and pond ripple interactions.

### Phase 2: Dusk Lighting, Lantern & Firefly Mechanics
- Added custom dusk visual assets (`moon.png`, `star.png`, `owl.png`, `lantern.PNG`) and smooth Day/Dusk sky transitions.
- Implemented firefly catching logic, lantern illumination thresholds, and harvest particle feedback.

### Phase 3: Spatial Calibration & UI Micro-Polish
- **Anchor & Scale Tuning:** Adjusted sprite coordinates, bounding hitboxes, and animation speeds so interactive elements sit naturally on the paper terrain without visual overlap.
- **Dynamic Toast Pill Sizing:** Refactored notification banners (`craftToastText`, `comboBannerText`) to auto-fit text width dynamically rather than stretching across the artwork.
- **State Cleanup:** Hid redundant hand-held lantern sprites when switching world/lighting states to prevent visual artifacts.

### Phase 4: Content Streamlining & Guide Readability
- Refined the 4-page **Origami Meadow Guide** typography, line breaks, and pagination controls (`Next >`) so onboarding instructions remain concise and legible inside the illustrated scroll.
- Removed extraneous external page headers (`st.header`) and instructional paragraphs above the canvas so users enter the visual world immediately without scrolling.

### Phase 5: 1920 × 1080 (16:9) Full-Bleed Exhibition Adaptation
- **Viewport Override (`app.py`):** Applied `st.set_page_config(layout="wide", initial_sidebar_state="collapsed")` and custom CSS (`padding: 0`, `margin: 0`, `100vw × 100vh` iframe sizing) to eliminate white borders and Streamlit UI chrome.
- **High-DPI Canvas Scaling (`modules/living.py`):** Updated the p5.js canvas to fill a strict **16:9 (`100vw` × `56.25vw` / `1920 × 1080`)** aspect ratio with `pixelDensity(2)`, ensuring razor-sharp paper edges on Retina and large exhibition displays.

---

## 6. Technical Challenges & Engineering Solutions

| Challenge | Root Cause | Engineering Solution |
| :--- | :--- | :--- |
| **Broken image paths inside Streamlit components** | Streamlit serves `components.v1.html` inside an isolated iframe origin that cannot directly resolve local `./assets/` URLs. | Built `load_asset_data_uri()` in Python to read binary image bytes and inject inline Base64 Data URIs directly into the JS template string. |
| **White margins and vertical scrolling around canvas** | Streamlit's default `.block-container` enforces `max-width` padding and top header spacing, while fixed `860 × 560` canvas dimensions left empty whitespace. | Injected `!important` full-viewport CSS rules in `app.py`, removed `st.header`/`st.write` blocks in `living.py`, and set the HTML/body/iframe containers to `100vw × 100vh` (`overflow: hidden`). |
| **Blurry paper edges on macOS Retina displays** | Default HTML5 `<canvas>` renders at `1x` CSS pixel density, softening fine paper textures and drop shadows when scaled to 1920 × 1080. | Added `pixelDensity(2)` inside p5.js `setup()` and matched coordinate scaling so every sprite renders at native Retina sharpness. |
| **JavaScript string escaping inside Python f-strings** | Multi-line guide strings (`\n`) inside Python triple-quoted `f"""..."""` templates caused syntax errors when parsed by the browser JS engine. | Sanitized newline escape sequences (`\\n`) within `INTER_PAGES` guide definitions and verified clean console execution. |
| **Multi-contributor Git merge conflicts on `main`** | Simultaneous edits across `app.py` and `modules/living.py` during team integration caused branch divergence and cached Uvicorn server states. | Reconciled merge commits cleanly, verified direct single-module routing (`living.render()`), and performed hard server restarts (`pkill -f streamlit && streamlit run app.py`) to load updated builds. |

---

## 7. Testing & Quality Assurance Checklist

Before finalizing the 16:9 exhibition build, the module was verified against the following criteria:
- [x] **Full-Bleed Framing:** Zero white borders, scrollbars, or Streamlit toolbars visible at `1920 × 1080` and macOS Chrome Full-Screen (`Command + Shift + F`).
- [x] **Asset Integrity:** All 18+ PNG sprites load instantaneously without console `404` or `Data URI` decoding errors.
- [x] **Complete Interaction Loop:** Guide pagination (`1/4`–`4/4`), fairy awakening, pond water refilling, sprout blooming, Day/Dusk toggle, 5-firefly lantern charging, workbench crafting, and page-corner flip all trigger reliably.
- [x] **Audio & Performance:** Smooth 60 FPS frame rate with `pixelDensity(2)` enabled and responsive Web Audio feedback on user clicks.

---

## 8. Reflection & Future Roadmap

Developing **Living World: The Origami Meadow** demonstrated how combining handmade visual craft with lightweight creative coding (`p5.js`) can turn a standard web viewport into an intimate, tactile storytelling space. Removing traditional web UI chrome and committing to a pure 16:9 full-bleed canvas dramatically elevated the emotional warmth and spatial immersion of the artwork.

### Planned Next Steps
1. **Cross-World State Persistence:** Pass collected firefly energy, bloomed flora counts, and crafted meadow items via session state into *Weather World* and *Secret World* when the user flips the page corner.
2. **Adaptive Aspect-Ratio Letterboxing:** Add subtle paper-textured pillarbox/letterbox framing for ultra-wide (`21:9`) or `16:10` laptop displays so the `16:9` composition never crops interactive edges.
3. **Multi-Touch Exhibition Support:** Extend mouse hover and drag listeners with native touch events (`touchStarted`, `touchMoved`, `touchEnded`) for gallery touchscreens and iPads.