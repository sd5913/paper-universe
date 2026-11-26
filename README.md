# 🌸 Paper Universe — Interactive Pop-Up World

**Paper Universe** is an interactive, multi-module digital pop-up book and paper-cut collage experience built with **Python**, **Streamlit**, **HTML5/CSS3**, **JavaScript (ES6+)**, and **p5.js**[cite: 1, 8]. Designed with a warm, tactile aesthetic and zero-clutter full-bleed framing, the project transforms a standard browser viewport into a handcrafted miniature ecosystem where gentle environmental interactions bring layered paper worlds to life.

> **Exhibition Display Mode:** Optimized for **1920 × 1080 (16:9)** full-bleed presentation at Retina sharpness (`pixelDensity(2)`).

---

## 🖼️ Visual Preview

<!-- Replace the path below with a screenshot of your 16:9 full-screen meadow in assets/ -->
<!-- ![Living World — The Origami Meadow](assets/preview_16x9.png) -->

- **Live Entry:** Opens directly into *Living World: The Origami Meadow* with zero external UI chrome or scrollbars.
- **Pop-Up Transitions:** Features tactile page-corner curl interactions that bridge between narrative worlds.

---

## 🌍 The Paper Universe Ecosystem

**Paper Universe** is architected as a modular multi-world web installation where each module explores a distinct sensory and environmental theme:

| Module | File | Description |
| :--- | :--- | :--- |
| **Living World** *(Flagship)* | `modules/living.py`[cite: 1] | **The Origami Meadow** — Nurture sprouts, wake the Flower Fairy, toggle Day/Dusk lighting, catch fireflies, and craft ecological wonders. |
| **Weather World** | `modules/weather.py`[cite: 1] | Atmospheric paper-cut climate simulation triggered via page-corner flip from Living World. |
| **Secret World** | `modules/secret.py`[cite: 1] | Hidden interactive paper diorama layer unlocked through exploration. |
| **World Experience** | `modules/experience.py`[cite: 1] | Unified multi-sensory narrative journey across the Paper Universe. |

---

## ✨ Key Features (*Living World: The Origami Meadow*)

- **🧚 Guided Discovery & Awakening:** Navigate the 4-page illustrated *Origami Meadow Guide* (`dialog.PNG`)[cite: 1] and tap the mushroom door to wake the sleeping Flower Fairy (`fairy.PNG`)[cite: 1].
- **💧 Botanical Nurturing:** Pick up the wooden watering can, scoop water from the pond, and hold over soil sprouts to bloom multi-stage paper flowers (`flower1.PNG`–`flower3.PNG`)[cite: 1].
- **🌗 Dynamic Day / Dusk Cycle:** Switch between sunlit meadow greens and twilight blues to awaken nocturnal creatures (`owl.png`)[cite: 1], reveal the moon and stars (`moon.png`, `star.png`)[cite: 1], and spawn glowing fireflies (`firefly.PNG`)[cite: 1].
- **🏮 Firefly Lantern & Workbench Crafting:** Catch 5 fireflies to illuminate the fairy's lantern (`lantern.PNG`)[cite: 1], harvest sky energy orbs, and craft ecological wonders at the workbench.
- **🎵 Procedural Web Audio & Particles:** Real-time Web Audio API harmonic chimes paired with particle bursts (`HarvestParticles`, `SkyEnergyOrbs`) provide immediate tactile feedback.
- **📦 Self-Contained Base64 Asset Pipeline:** Runtime image serialization (`load_asset_data_uri`) embeds all transparent PNG sprites directly as Data URIs[cite: 1], guaranteeing zero broken assets across local and cloud deployments.

---

## 🎮 Controls & Interaction Guide

| Action | Input | Effect in Meadow |
| :--- | :--- | :--- |
| **Read Meadow Guide** | Click `Next >` on scroll | Advances through the 4-step illustrated onboarding guide (`1/4`–`4/4`). |
| **Wake Flower Fairy** | Click mushroom door / fairy | Awakens the Flower Fairy and unlocks meadow interactions. |
| **Refill & Water Sprouts** | Click watering can → Pond → Hold on sprout | Scoops pond water and blooms multi-stage paper flowers. |
| **Toggle Day / Dusk** | Click Day/Dusk lighting switch | Transitions sky lighting, awakens the owl, and spawns fireflies. |
| **Catch Fireflies** | Click glowing fireflies at dusk | Collects up to 5 fireflies to charge the fairy's lantern. |
| **Craft & Turn Page** | Click Workbench / Bottom-right page corner | Crafts meadow wonders and curls the page corner toward *Weather World*. |

---

## 🗂️ Repository Structure

- `app.py`[cite: 1] — Main Streamlit application shell & 16:9 full-bleed viewport CSS controller
- `modules/living.py`[cite: 1] — Living World: The Origami Meadow (p5.js canvas, state machines & Base64 loader)
- `modules/weather.py`[cite: 1] — Weather World module
- `modules/secret.py`[cite: 1] — Secret World module
- `modules/experience.py`[cite: 1] — World Experience module
- `assets/`[cite: 1] — High-resolution transparent PNG paper-cut sprites (`fairy.PNG`, `lantern.PNG`, `frog.PNG`, `lotus.png`, `flower1.PNG`–`flower3.PNG`, etc.)[cite: 1]
- `living_world_standalone.html`[cite: 1] — Standalone single-file HTML build (runs offline without a Python server)
- `PROCESS.md`[cite: 6] — Comprehensive design & development process documentation
- `TECHNICAL_AGREEMENT.md`[cite: 1] — Team integration conventions & technical architecture agreement
- `pyproject.toml` & `uv.lock`[cite: 1] — Python project dependencies & locked environment configuration

---

## 🚀 Getting Started

### Option A: Run via Streamlit (Recommended Full Experience)

1. **Clone the repository:**
   `git clone https://github.com/634461276-boop/paper-universe.git`
   `cd paper-universe`

2. **Install dependencies (Python 3.10+, tested on 3.14)[cite: 1]:**
   `uv sync` *(or `pip install streamlit`)*

3. **Start the local server:**
   `streamlit run app.py`[cite: 1]

4. **Enter 16:9 Full-Bleed Exhibition Mode:**
   - Open `http://localhost:8501` in Google Chrome[cite: 1].
   - Enter browser Full-Screen mode and press **`Command + Shift + F`** (macOS) to hide the browser tab bar and address bar.

### Option B: Standalone Offline HTML Preview

- Double-click `living_world_standalone.html`[cite: 1] in Finder/Explorer to open *Living World* directly in any modern browser without running Python or Streamlit.

---

## 📖 Documentation

- **[`PROCESS.md`](./PROCESS.md):** Full documentation of visual concept, Base64 asset pipeline, 5-phase iterative development timeline, 16:9 full-bleed adaptation, and QA testing checklist.
- **[`TECHNICAL_AGREEMENT.md`](./TECHNICAL_AGREEMENT.md):** Multi-module routing conventions and repository collaboration guidelines.

---

## 🛠️ Tech Stack

- **Application Shell:** Python, Streamlit (`layout="wide"`, custom full-viewport CSS)
- **Creative Coding & Rendering:** HTML5, CSS3, JavaScript (ES6+), p5.js (`pixelDensity(2)`)
- **Audio & Particles:** Web Audio API, custom 2D particle emitters
- **Environment & Version Control:** `uv`[cite: 1], Git / GitHub (`main` branch)[cite: 4]

---

## 👥 Authors & Credits

- **Interactive Design, Visual Assets & Creative Coding:** Paper Universe Project Team
- **Core Module (*Living World: The Origami Meadow*):** Designed and engineered with a human-centered, tactile craft philosophy.