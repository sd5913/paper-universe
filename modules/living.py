import base64
from pathlib import Path
import streamlit as st
import streamlit.components.v1 as components


def load_asset_data_uri(filenames: list[str]) -> str:
    """自动查找 assets 文件夹里的指定图片并转为 Base64 格式"""
    root_dir = Path(__file__).resolve().parent.parent
    for name in filenames:
        candidates = [
            root_dir / "assets" / name,
            Path("assets") / name,
            root_dir / name,
        ]
        for p in candidates:
            if p.exists():
                ext = p.suffix.lower().lstrip(".")
                mime = "jpeg" if ext in ("jpg", "jpeg") else "png"
                b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
                return f"data:image/{mime};base64,{b64}"
    return ""


def render():
    """Display the Living World module."""
    st.header("🌱 Living World: The Origami Meadow")
    st.write(
        "点击木门唤醒花仙子；点击大树树冠摇落折纸树叶，点击荷叶小青蛙连跳四下，点击门前鹅卵石奏响音阶；拾起水壶在荷花池舀水并浇灌花朵与蘑菇，盛开后点击它们即可采摘（伴随花瓣与孢子飞散）！"
    )

    bg_data_uri = load_asset_data_uri(["bg.jpg", "bg.JPG", "bg.png", "bg.PNG"])
    fairy_data_uri = load_asset_data_uri(["fairy.PNG", "fairy.png"])
    bucket_data_uri = load_asset_data_uri(["bucket.PNG", "bucket.png"])

    f1_uri = load_asset_data_uri(["flower1.png", "flower1.PNG"])
    f2_uri = load_asset_data_uri(["flower2.png", "flower2.PNG"])
    f3_uri = load_asset_data_uri(["flower3.png", "flower3.PNG"])
    m1_uri = load_asset_data_uri(["mushroom1.png", "mushroom1.PNG"])
    m2_uri = load_asset_data_uri(["mushroom2.png", "mushroom2.PNG"])

    b1_uri = load_asset_data_uri(["bird1.png", "bird1.PNG", "bird.png", "bird.PNG"])
    b2_uri = load_asset_data_uri(["bird2.png", "bird2.PNG"])
    frog_uri = load_asset_data_uri(["frog.png", "frog.PNG"])

    p5_html = f"""
    <!DOCTYPE html>
    <html lang="zh">
    <head>
      <meta charset="UTF-8" />
      <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
      <style>
        html, body {{
          margin: 0;
          padding: 0;
          overflow: hidden;
          background: #f6f1e7;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }}
        canvas {{
          display: block;
          border-radius: 14px;
          box-shadow: 0 8px 24px rgba(60, 50, 40, 0.14);
        }}
      </style>
    </head>
    <body>
    <script>
      const BG_IMG_DATA = "{bg_data_uri}";
      const FAIRY_IMG_DATA = "{fairy_data_uri}";
      const BUCKET_IMG_DATA = "{bucket_data_uri}";
      const FLOWER_URIS = ["{f1_uri}", "{f2_uri}", "{f3_uri}"];
      const MUSHROOM_URIS = ["{m1_uri}", "{m2_uri}"];
      const BIRD_URIS = ["{b1_uri}", "{b2_uri}"];
      const FROG_IMG_DATA = "{frog_uri}";

      let bgImg = null;
      let fairyImg = null;
      let bucketImg = null;
      let frogImg = null;
      let flowerImgs = [];
      let mushroomImgs = [];
      let birdImgs = [];

      let sceneState = "HOUSE_CLOSED";
      let doorGlow = 0;
      let sprite;
      let frog;
      let grassBlades = [];
      let plants = [];
      let waterDrops = [];
      let ripples = [];
      let butterflies = [];
      let birds = [];
      let stepStones = [];

      // 自然生态交互系统状态
      let fallingLeaves = [];
      let waterLilies = [];
      let musicNotes = [];

      // 采摘花朵与蘑菇精细化系统
      let harvestedItems = [];      // 抛物线飞向花仙子的采摘战利品
      let harvestParticles = [];    // 采摘瞬间的折纸花瓣 & 金色孢子粒子
      let orbitWreathItems = [];    // 近期采摘后短暂环绕花仙子的迷你花环挂饰
      let fairyBurstRing = 0;       // 每采满 5 份收获时的星尘光环
      let harvestedFlowerCount = 0;
      let harvestedMushroomCount = 0;

      let gardenVitality = 0;
      let hasWateredFlowers = false;
      let hasPickedBucketOnce = false;

      // ================== Web Audio API 零素材合成音效引擎 ==================
      let audioCtx = null;
      let soundEnabled = true;

      function ensureAudio() {{
        if (!soundEnabled) return null;
        if (!audioCtx) {{
          const AudioContext = window.AudioContext || window.webkitAudioContext;
          if (AudioContext) audioCtx = new AudioContext();
        }}
        if (audioCtx && audioCtx.state === "suspended") {{
          audioCtx.resume();
        }}
        return audioCtx;
      }}

      function playChimeNote(freq, duration = 0.55, volume = 0.11, delay = 0) {{
        let ctx = ensureAudio();
        if (!ctx) return;
        let now = ctx.currentTime + delay;

        let osc = ctx.createOscillator();
        let gain = ctx.createGain();
        osc.type = "sine";
        osc.frequency.setValueAtTime(freq, now);

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.exponentialRampToValueAtTime(volume, now + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + duration);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + duration + 0.02);
      }}

      function playHarvestSound(isMushroom = false) {{
        let ctx = ensureAudio();
        if (!ctx) return;
        let freqs = isMushroom ? [523.25, 783.99] : [659.25, 987.77];
        freqs.forEach((f, idx) => {{
          playChimeNote(f, 0.38, 0.09, idx * 0.07);
        }});
      }}

      function playMilestoneFanfare() {{
        const notes = [587.33, 739.99, 880.00, 1174.66];
        notes.forEach((f, i) => playChimeNote(f, 0.55, 0.09, i * 0.08));
      }}

      function playBirdChirpSound(variant = 0) {{
        let ctx = ensureAudio();
        if (!ctx) return;
        let notes = variant === 0 ? [1046.5, 1318.5, 1567.98] : [1174.66, 1396.91, 1760.0];
        notes.forEach((f, idx) => {{
          let now = ctx.currentTime + idx * 0.09;
          let osc = ctx.createOscillator();
          let gain = ctx.createGain();
          osc.type = "sine";
          osc.frequency.setValueAtTime(f * 0.92, now);
          osc.frequency.exponentialRampToValueAtTime(f * 1.08, now + 0.07);

          gain.gain.setValueAtTime(0.0001, now);
          gain.gain.exponentialRampToValueAtTime(0.075, now + 0.015);
          gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.11);

          osc.connect(gain);
          gain.connect(ctx.destination);
          osc.start(now);
          osc.stop(now + 0.12);
        }});
      }}

      function playLeafRustleSound() {{
        let ctx = ensureAudio();
        if (!ctx) return;
        let now = ctx.currentTime;
        let osc = ctx.createOscillator();
        let gain = ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(420, now);
        osc.frequency.exponentialRampToValueAtTime(290, now + 0.18);

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.exponentialRampToValueAtTime(0.055, now + 0.02);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.20);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.22);
      }}

      function playWaterDropSound(isScoop = false) {{
        let ctx = ensureAudio();
        if (!ctx) return;
        let now = ctx.currentTime;

        let osc = ctx.createOscillator();
        let gain = ctx.createGain();
        osc.type = "sine";
        if (isScoop) {{
          osc.frequency.setValueAtTime(340, now);
          osc.frequency.exponentialRampToValueAtTime(680, now + 0.18);
        }} else {{
          let base = random(520, 760);
          osc.frequency.setValueAtTime(base, now);
          osc.frequency.exponentialRampToValueAtTime(base * 1.35, now + 0.09);
        }}

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.exponentialRampToValueAtTime(isScoop ? 0.11 : 0.045, now + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + (isScoop ? 0.22 : 0.11));

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.25);
      }}

      function playFrogHopSound() {{
        let ctx = ensureAudio();
        if (!ctx) return;
        let now = ctx.currentTime;

        let osc = ctx.createOscillator();
        let gain = ctx.createGain();
        osc.type = "triangle";
        osc.frequency.setValueAtTime(210, now);
        osc.frequency.exponentialRampToValueAtTime(330, now + 0.09);

        gain.gain.setValueAtTime(0.0001, now);
        gain.gain.exponentialRampToValueAtTime(0.09, now + 0.015);
        gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.12);

        osc.connect(gain);
        gain.connect(ctx.destination);
        osc.start(now);
        osc.stop(now + 0.14);
      }}

      let groundBucket = {{
        x: 365,
        y: 445,
        targetY: 445,
        scale: 1
      }};

      const DOOR_X = 562;
      const DOOR_Y = 326;

      const POND_X = 195;
      const POND_Y = 382;

      const TREE_CROWNS = [
        {{ x: 108, y: 145, rx: 76, ry: 82 }},
        {{ x: 375, y: 158, rx: 68, ry: 74 }},
        {{ x: 752, y: 142, rx: 74, ry: 80 }}
      ];

      function getClickedTreeCrown(px, py) {{
        for (let t of TREE_CROWNS) {{
          let dx = (px - t.x) / t.rx;
          let dy = (py - t.y) / t.ry;
          if (dx * dx + dy * dy <= 1.0) return t;
        }}
        return null;
      }}

      function isPointInPond(px, py) {{
        let dx = (px - POND_X) / 132;
        let dy = (py - POND_Y) / 68;
        return (dx * dx + dy * dy) <= 1.05;
      }}

      function isPointOnMuteButton(px, py) {{
        return px >= width - 104 && px <= width - 16 && py >= 16 && py <= 46;
      }}

      function preload() {{
        if (BG_IMG_DATA) bgImg = loadImage(BG_IMG_DATA);
        if (FAIRY_IMG_DATA) fairyImg = loadImage(FAIRY_IMG_DATA);
        if (BUCKET_IMG_DATA) bucketImg = loadImage(BUCKET_IMG_DATA);
        if (FROG_IMG_DATA) frogImg = loadImage(FROG_IMG_DATA);

        for (let uri of FLOWER_URIS) {{
          if (uri && uri.length > 0) flowerImgs.push(loadImage(uri));
        }}
        for (let uri of MUSHROOM_URIS) {{
          if (uri && uri.length > 0) mushroomImgs.push(loadImage(uri));
        }}
        for (let uri of BIRD_URIS) {{
          if (uri && uri.length > 0) birdImgs.push(loadImage(uri));
        }}
      }}

      function setup() {{
        createCanvas(860, 560);
        angleMode(RADIANS);

        sprite = new OrigamiSprite(DOOR_X, DOOR_Y);
        frog = new OrigamiFrog();

        waterLilies = [
          {{ x: 136, y: 398, bloom: 0, targetBloom: 0, color: '#f7cad0' }},
          {{ x: 204, y: 374, bloom: 0, targetBloom: 0, color: '#fff0f3' }},
          {{ x: 256, y: 406, bloom: 0, targetBloom: 0, color: '#ffccd5' }}
        ];

        const stoneNotes = [
          {{ x: 545, y: 392, freq: 523.25 }},
          {{ x: 514, y: 405, freq: 587.33 }},
          {{ x: 552, y: 418, freq: 659.25 }},
          {{ x: 506, y: 428, freq: 698.46 }},
          {{ x: 536, y: 438, freq: 783.99 }},
          {{ x: 472, y: 444, freq: 880.00 }},
          {{ x: 512, y: 458, freq: 987.77 }},
          {{ x: 454, y: 465, freq: 1046.50 }}
        ];
        for (let s of stoneNotes) {{
          stepStones.push({{ x: s.x, y: s.y, freq: s.freq, glow: 0 }});
        }}

        const grassZones = [
          {{ x1: 55,  x2: 225, y1: 470, y2: 538 }},
          {{ x1: 340, x2: 412, y1: 465, y2: 538 }},
          {{ x1: 340, x2: 400, y1: 338, y2: 362 }},
          {{ x1: 615, x2: 825, y1: 385, y2: 535 }}
        ];
        for (let z of grassZones) {{
          for (let x = z.x1; x <= z.x2; x += 22) {{
            grassBlades.push(new OrigamiGrass(x + random(-4, 4), random(z.y1, z.y2)));
          }}
        }}

        const plantConfigs = [
          // --- 区域一：左下角水池周围 & 左边大树旁 ---
          {{ x: 52,  y: 475, kind: 'flower',   variant: 0 }},
          {{ x: 78,  y: 515, kind: 'flower',   variant: 1 }},
          {{ x: 105, y: 495, kind: 'flower',   variant: 2 }},
          {{ x: 135, y: 535, kind: 'flower',   variant: 0 }},
          {{ x: 168, y: 512, kind: 'mushroom', variant: 0 }},
          {{ x: 198, y: 536, kind: 'flower',   variant: 1 }},
          {{ x: 232, y: 518, kind: 'flower',   variant: 2 }},
          {{ x: 265, y: 534, kind: 'flower',   variant: 0 }},

          // --- 区域二：水池右侧到石头小路左边（x <= 412） ---
          {{ x: 325, y: 485, kind: 'flower',   variant: 1 }},
          {{ x: 348, y: 522, kind: 'flower',   variant: 2 }},
          {{ x: 368, y: 472, kind: 'flower',   variant: 0 }},
          {{ x: 385, y: 505, kind: 'flower',   variant: 1 }},
          {{ x: 406, y: 534, kind: 'flower',   variant: 2 }},
          {{ x: 408, y: 465, kind: 'flower',   variant: 0 }},

          // --- 区域三：中间大树树干两侧 ---
          {{ x: 332, y: 358, kind: 'flower',   variant: 2 }},
          {{ x: 354, y: 348, kind: 'flower',   variant: 1 }},
          {{ x: 398, y: 356, kind: 'mushroom', variant: 1 }},
          {{ x: 418, y: 348, kind: 'flower',   variant: 0 }},

          // --- 区域四：石头小路右侧 & 右边大树旁（x >= 615） ---
          {{ x: 615, y: 478, kind: 'flower',   variant: 0 }},
          {{ x: 632, y: 522, kind: 'flower',   variant: 1 }},
          {{ x: 665, y: 492, kind: 'flower',   variant: 2 }},
          {{ x: 675, y: 532, kind: 'mushroom', variant: 0 }},
          {{ x: 705, y: 512, kind: 'flower',   variant: 0 }},
          {{ x: 735, y: 478, kind: 'flower',   variant: 1 }},
          {{ x: 765, y: 445, kind: 'flower',   variant: 2 }},
          {{ x: 795, y: 415, kind: 'flower',   variant: 0 }},
          {{ x: 822, y: 375, kind: 'flower',   variant: 1 }},

          // --- 新增：右下角最下方空白草地 ---
          {{ x: 738, y: 525, kind: 'flower',   variant: 2 }},
          {{ x: 772, y: 505, kind: 'flower',   variant: 0 }},
          {{ x: 798, y: 536, kind: 'flower',   variant: 1 }},
          {{ x: 824, y: 488, kind: 'flower',   variant: 2 }}
        ];
        for (let cfg of plantConfigs) {{
          plants.push(new CustomPlant(cfg.x, cfg.y, cfg.kind, cfg.variant));
        }}
      }}

      function draw() {{
        if (bgImg) {{
          imageMode(CORNER);
          image(bgImg, 0, 0, width, height);
        }} else {{
          background('#f7f2e7');
        }}

        drawDoorPortal();
        drawPondHint();
        drawStepStonesGlow();
        drawWaterLilies();

        for (let g of grassBlades) {{
          g.update();
          g.display();
        }}

        let bloomedCount = 0;
        let totalBloom = 0;
        for (let p of plants) {{
          p.update();
          p.display();
          totalBloom += p.bloom;
          if (p.bloom > 0.55) bloomedCount++;
        }}
        gardenVitality = totalBloom / plants.length;

        if (hasWateredFlowers && bloomedCount >= 1) {{
          let targetButterflyCount = min(7, 2 + floor(bloomedCount / 3));
          if (butterflies.length < targetButterflyCount && frameCount % 55 === 0) {{
            let wateredFlowers = plants.filter(p => p.kind === 'flower' && p.bloom > 0.45);
            let source = wateredFlowers.length > 0 ? random(wateredFlowers) : random(plants);
            butterflies.push(new OrigamiButterfly(source.x + random(-24, 24), source.y - source.stemHeight - 16));
          }}
        }}

        if (gardenVitality > 0.45 && birds.length < 2 && frameCount % 90 === 0) {{
          const treePerches = [
            {{ x: 112, y: 205 }},
            {{ x: 748, y: 195 }}
          ];
          let idx = birds.length;
          let perch = treePerches[idx];
          birds.push(new OrigamiBird(idx === 0 ? -35 : width + 35, random(90, 160), perch.x, perch.y, idx));
        }}

        for (let i = ripples.length - 1; i >= 0; i--) {{
          ripples[i].update();
          ripples[i].display();
          if (ripples[i].alpha <= 0) ripples.splice(i, 1);
        }}

        frog.update();
        frog.display();

        for (let i = waterDrops.length - 1; i >= 0; i--) {{
          waterDrops[i].update();
          waterDrops[i].display();
          if (waterDrops[i].y >= waterDrops[i].targetGroundY) {{
            triggerWaterImpact(waterDrops[i].x, waterDrops[i].y);
            waterDrops.splice(i, 1);
          }}
        }}

        drawGroundBucket();
        updateAndDrawHarvestParticles();
        updateAndDrawHarvestedItems();

        for (let b of butterflies) {{
          b.update();
          b.display();
        }}

        for (let bird of birds) {{
          bird.update();
          bird.display();
        }}

        updateAndDrawFallingLeaves();
        updateAndDrawMusicNotes();

        if (sceneState === "GARDEN_ACTIVE" && sprite.hasBucket && sprite.bucketHasWater && mouseIsPressed && frameCount % 7 === 0) {{
          if (!isPointInPond(mouseX, mouseY) &&
              !frog.isPointOnFrog(mouseX, mouseY) &&
              !getClickedBird(mouseX, mouseY) &&
              !getClickedTreeCrown(mouseX, mouseY) &&
              !getClickedRipePlant(mouseX, mouseY) &&
              !isPointOnMuteButton(mouseX, mouseY)) {{
            sprite.pourWater();
          }}
        }}

        sprite.update();
        sprite.display();

        drawTopHUD();
        updateCursorStyle();
      }}

      // ================== 采摘盛开的花朵与蘑菇（含花瓣/孢子粒子、泥土波纹与花环反馈） ==================
      function getClickedRipePlant(px, py) {{
        let closest = null;
        let minDist = 24;
        for (let p of plants) {{
          if (p.bloom > 0.72) {{
            let centerY = p.kind === 'flower' ? (p.y - p.stemHeight) : (p.y - 16);
            let d = dist(px, py, p.x, centerY);
            if (d < minDist) {{
              minDist = d;
              closest = p;
            }}
          }}
        }}
        return closest;
      }}

      function spawnHarvestBurst(x, y, kind, variant) {{
        if (kind === 'flower') {{
          // 摘花瞬间爆散 5 片对应花色的折纸小花瓣
          const flowerPalettes = [
            ['#ffafcc', '#ffc8dd'], // 粉花
            ['#ffd166', '#ffe699'], // 黄花
            ['#90dbf4', '#bde0fe']  // 蓝花
          ];
          let cols = flowerPalettes[variant % flowerPalettes.length];
          for (let i = 0; i < 5; i++) {{
            let ang = (TWO_PI / 5) * i + random(-0.3, 0.3);
            let spd = random(1.2, 2.4);
            harvestParticles.push({{
              type: 'petal',
              x: x,
              y: y,
              vx: cos(ang) * spd,
              vy: sin(ang) * spd - 1.2,
              gravity: 0.045,
              rot: random(TWO_PI),
              rotSpeed: random(-0.08, 0.08),
              color: random(cols),
              alpha: 255
            }});
          }}
        }} else {{
          // 采蘑菇瞬间菌褶喷出 7 颗金色孢子星尘
          for (let i = 0; i < 7; i++) {{
            let ang = random(-PI, 0);
            let spd = random(0.8, 2.1);
            harvestParticles.push({{
              type: 'spore',
              x: x + random(-8, 8),
              y: y + 4,
              vx: cos(ang) * spd,
              vy: sin(ang) * spd - 0.5,
              gravity: -0.015, // 孢子轻盈向上漂浮
              size: random(4, 6.5),
              color: random(['#ffd166', '#fff3b0', '#f4a261']),
              alpha: 255
            }});
          }}
        }}
      }}

      function updateAndDrawHarvestParticles() {{
        for (let i = harvestParticles.length - 1; i >= 0; i--) {{
          let pt = harvestParticles[i];
          pt.x += pt.vx;
          pt.y += pt.vy;
          pt.vy += pt.gravity;
          pt.vx *= 0.97;
          pt.alpha -= 4.2;

          if (pt.alpha <= 0) {{
            harvestParticles.splice(i, 1);
            continue;
          }}

          push();
          translate(pt.x, pt.y);
          noStroke();
          let c = color(pt.color);
          c.setAlpha(pt.alpha);
          fill(c);

          if (pt.type === 'petal') {{
            pt.rot += pt.rotSpeed;
            rotate(pt.rot);
            // 折纸水滴形花瓣
            triangle(0, -6, -4, 1, 0, 5);
            c.setAlpha(pt.alpha * 0.82);
            fill(c);
            triangle(0, -6, 4, 1, 0, 5);
          }} else {{
            // 发光孢子微粒
            circle(0, 0, pt.size);
            fill(255, 255, 255, pt.alpha * 0.75);
            circle(0, 0, pt.size * 0.45);
          }}
          pop();
        }}
      }}

      function harvestPlant(p) {{
        let startY = p.kind === 'flower' ? (p.y - p.stemHeight) : (p.y - 16);
        let imgList = p.kind === 'flower' ? flowerImgs : mushroomImgs;
        let img = imgList.length > 0 ? imgList[p.variant % imgList.length] : null;

        // 1. 触发花瓣或孢子粒子爆散 + 脚下草叶微尘波纹
        spawnHarvestBurst(p.x, startY, p.kind, p.variant);
        ripples.push(new PaperRipple(p.x, p.y));

        // 2. 抛物线弧线飞向花仙子
        harvestedItems.push({{
          startX: p.x,
          startY: startY,
          x: p.x,
          y: startY,
          t: 0,
          duration: 28,
          kind: p.kind,
          variant: p.variant,
          img: img,
          rot: 0
        }});

        if (p.kind === 'flower') {{
          harvestedFlowerCount++;
          playHarvestSound(false);
        }} else {{
          harvestedMushroomCount++;
          playHarvestSound(true);
        }}

        // 3. 每采满 5 份收获触发一次星尘花环庆贺
        let totalHarvested = harvestedFlowerCount + harvestedMushroomCount;
        if (totalHarvested > 0 && totalHarvested % 5 === 0) {{
          fairyBurstRing = 1.0;
          playMilestoneFanfare();
        }}

        // 4. 采摘后花朵/蘑菇回到嫩芽/菌丝环状态，并记录刚被采摘的留痕时间
        p.bloom = 0.08;
        p.targetBloom = 0.08;
        p.harvestedFade = 1.0;
      }}

      function updateAndDrawHarvestedItems() {{
        for (let i = harvestedItems.length - 1; i >= 0; i--) {{
          let item = harvestedItems[i];
          item.t++;
          let prog = constrain(item.t / item.duration, 0, 1);
          // 抛物线飞向花仙子身边
          let arcLift = sin(prog * PI) * 48;
          item.x = lerp(item.startX, sprite.x, prog);
          item.y = lerp(item.startY, sprite.y - 6, prog) - arcLift;
          item.rot += 0.14;

          if (prog >= 1) {{
            // 融入花仙子身边的迷你环绕花环（最多保留最近 4 个挂饰）
            orbitWreathItems.push({{
              kind: item.kind,
              variant: item.variant,
              img: item.img,
              life: 320
            }});
            if (orbitWreathItems.length > 4) orbitWreathItems.shift();
            harvestedItems.splice(i, 1);
            continue;
          }}

          let s = map(prog, 0, 1, 1.1, 0.48);
          push();
          translate(item.x, item.y);
          rotate(item.rot);
          scale(s);
          if (item.img) {{
            imageMode(CENTER);
            let targetH = 38;
            let targetW = targetH * (item.img.width / item.img.height);
            image(item.img, 0, 0, targetW, targetH);
          }} else {{
            noStroke();
            fill(item.kind === 'flower' ? '#f28482' : '#e06d53');
            circle(0, 0, 22);
          }}
          pop();
        }}
      }}

      // ================== 荷花池粉白折纸睡莲 ==================
      function bloomNextWaterLily() {{
        for (let lily of waterLilies) {{
          if (lily.targetBloom < 1) {{
            lily.targetBloom = 1;
            break;
          }}
        }}
      }}

      function drawWaterLilies() {{
        for (let lily of waterLilies) {{
          lily.bloom = lerp(lily.bloom, lily.targetBloom, 0.06);
          if (lily.bloom <= 0.02) continue;

          push();
          translate(lily.x, lily.y);
          scale(lily.bloom);
          rotate(sin(frameCount * 0.03 + lily.x) * 0.06);
          setPaperShadow(5, 1, 2, 'rgba(40, 70, 90, 0.18)');
          noStroke();

          for (let i = 0; i < 6; i++) {{
            push();
            rotate((TWO_PI / 6) * i);
            fill(lily.color);
            triangle(0, 0, -5, -13, 5, -13);
            pop();
          }}
          for (let i = 0; i < 6; i++) {{
            push();
            rotate((TWO_PI / 6) * i + PI / 6);
            fill('#ffffff');
            triangle(0, 0, -3.5, -9, 3.5, -9);
            pop();
          }}
          fill('#ffd166');
          circle(0, 0, 5.5);

          clearShadow();
          pop();
        }}
      }}

      // ================== 摇晃大树飘落折纸树叶 ==================
      function spawnTreeLeaves(cx, cy) {{
        playLeafRustleSound();
        const leafCols = ['#8ac926', '#b5e48c', '#ffd166', '#99d98c'];
        for (let i = 0; i < 3; i++) {{
          fallingLeaves.push({{
            x: cx + random(-36, 36),
            y: cy + random(-15, 25),
            vy: random(0.65, 1.15),
            swaySeed: random(TWO_PI),
            rot: random(TWO_PI),
            rotSpeed: random(-0.04, 0.04),
            color: random(leafCols),
            alpha: 245
          }});
        }}
      }}

      function updateAndDrawFallingLeaves() {{
        for (let i = fallingLeaves.length - 1; i >= 0; i--) {{
          let lf = fallingLeaves[i];
          lf.y += lf.vy;
          lf.x += sin(frameCount * 0.045 + lf.swaySeed) * 0.85;
          lf.rot += lf.rotSpeed;

          if (lf.y > 460) {{
            lf.alpha -= 4;
          }}
          if (lf.alpha <= 0) {{
            fallingLeaves.splice(i, 1);
            continue;
          }}

          push();
          translate(lf.x, lf.y);
          rotate(lf.rot);
          setPaperShadow(4, 1, 2, 'rgba(40, 50, 30, 0.16)');
          noStroke();
          let c = color(lf.color);
          c.setAlpha(lf.alpha);
          fill(c);
          triangle(0, -9, -5, 0, 0, 9);
          c.setAlpha(lf.alpha * 0.82);
          fill(c);
          triangle(0, -9, 5, 0, 0, 9);
          clearShadow();
          pop();
        }}
      }}

      // ================== 小鸟对唱与飘出剪纸音符 ==================
      function getClickedBird(px, py) {{
        for (let b of birds) {{
          if (dist(px, py, b.x, b.y - 14) < 26) return b;
        }}
        return null;
      }}

      function spawnBirdMusicNotes(bx, by) {{
        const noteCols = ['#ff9f1c', '#ff758f', '#72efdd'];
        for (let i = 0; i < 3; i++) {{
          musicNotes.push({{
            x: bx + random(-14, 14),
            y: by - 26 - i * 8,
            vx: random(-0.3, 0.3),
            vy: random(-0.75, -0.55),
            alpha: 245,
            color: noteCols[i % noteCols.length],
            phase: random(TWO_PI)
          }});
        }}
      }}

      function updateAndDrawMusicNotes() {{
        for (let i = musicNotes.length - 1; i >= 0; i--) {{
          let n = musicNotes[i];
          n.x += n.vx + sin(frameCount * 0.08 + n.phase) * 0.25;
          n.y += n.vy;
          n.alpha -= 2.8;
          if (n.alpha <= 0) {{
            musicNotes.splice(i, 1);
            continue;
          }}

          push();
          translate(n.x, n.y);
          noStroke();
          let c = color(n.color);
          c.setAlpha(n.alpha);
          fill(c);
          ellipse(-2, 3, 6.5, 5);
          rect(0.5, -7, 2, 10);
          triangle(2.5, -7, 8, -4, 2.5, -2);
          pop();
        }}
      }}

      function drawStepStonesGlow() {{
        for (let s of stepStones) {{
          if (s.glow > 0.01) {{
            s.glow = lerp(s.glow, 0, 0.08);
            push();
            noStroke();
            fill(255, 248, 210, s.glow * 180);
            ellipse(s.x, s.y, 26 + (1 - s.glow) * 14, 14 + (1 - s.glow) * 8);
            pop();
          }}
        }}
      }}

      function drawTopHUD() {{
        let hy = 16;
        let hh = 30;

        // 1. 左上角花篮采摘计数徽章
        if (harvestedFlowerCount > 0 || harvestedMushroomCount > 0) {{
          push();
          let bw = 122;
          setPaperShadow(6, 1, 2, 'rgba(60, 50, 40, 0.14)');
          noStroke();
          fill(250, 245, 235, 225);
          rect(18, hy, bw, hh, 15);
          clearShadow();

          fill('#6b6356');
          textAlign(CENTER, CENTER);
          textSize(11.5);
          text(`🌸 ${{harvestedFlowerCount}}   🍄 ${{harvestedMushroomCount}}`, 18 + bw / 2, hy + hh / 2 + 0.5);
          pop();
        }}

        // 2. 右上角静音开关
        push();
        let bx = width - 104;
        let by = 16;
        let bw = 88;
        let bh = 30;
        setPaperShadow(6, 1, 2, 'rgba(60, 50, 40, 0.14)');
        noStroke();
        fill(250, 245, 235, 225);
        rect(bx, by, bw, bh, 15);
        clearShadow();

        fill('#6b6356');
        textAlign(CENTER, CENTER);
        textSize(12);
        text(soundEnabled ? "🔊 音效已开" : "🔇 已静音", bx + bw / 2, by + bh / 2 + 1);
        pop();
      }}

      function drawPondHint() {{
        if (sceneState === "GARDEN_ACTIVE" && sprite.hasBucket && !sprite.bucketHasWater) {{
          push();
          translate(POND_X, POND_Y);
          let pulse = sin(frameCount * 0.08) * 0.5 + 0.5;
          noFill();
          stroke(255, 255, 255, 110 + pulse * 100);
          strokeWeight(2.2);
          ellipse(0, 0, 120 + pulse * 24, 52 + pulse * 10);
          pop();
        }}
      }}

      function getHoveredStone(px, py) {{
        for (let s of stepStones) {{
          if (dist(px, py, s.x, s.y) < 15) return s;
        }}
        return null;
      }}

      function updateCursorStyle() {{
        if (isPointOnMuteButton(mouseX, mouseY)) {{
          cursor(HAND);
          return;
        }}
        if (sceneState !== "GARDEN_ACTIVE") {{
          cursor(HAND);
          return;
        }}
        if (frog.isPointOnFrog(mouseX, mouseY) ||
            getClickedBird(mouseX, mouseY) ||
            getClickedTreeCrown(mouseX, mouseY) ||
            getClickedRipePlant(mouseX, mouseY)) {{
          cursor(HAND);
        }} else if (sprite.hasBucket && sprite.isPointOnBucket(mouseX, mouseY)) {{
          cursor(HAND);
        }} else if (sprite.hasBucket && isPointInPond(mouseX, mouseY)) {{
          cursor(HAND);
        }} else if (groundBucket && dist(mouseX, mouseY, groundBucket.x, groundBucket.y) < 32) {{
          cursor(HAND);
        }} else if (getHoveredStone(mouseX, mouseY)) {{
          cursor(HAND);
        }} else {{
          cursor(ARROW);
        }}
      }}

      function mousePressed() {{
        if (isPointOnMuteButton(mouseX, mouseY)) {{
          soundEnabled = !soundEnabled;
          if (soundEnabled) playChimeNote(659.25, 0.3, 0.08);
          return;
        }}

        if (sceneState === "HOUSE_CLOSED") {{
          sceneState = "SPRITE_EMERGING";
          playChimeNote(523.25, 0.6, 0.09, 0.0);
          playChimeNote(659.25, 0.6, 0.09, 0.12);
          playChimeNote(783.99, 0.8, 0.10, 0.24);
        }} else if (sceneState === "GARDEN_ACTIVE") {{
          if (frog.isPointOnFrog(mouseX, mouseY)) {{
            frog.jumpToNextPad();
            return;
          }}

          let hitBird = getClickedBird(mouseX, mouseY);
          if (hitBird) {{
            hitBird.singAndHop();
            return;
          }}

          let hitTree = getClickedTreeCrown(mouseX, mouseY);
          if (hitTree) {{
            spawnTreeLeaves(mouseX, mouseY);
            return;
          }}

          let hitRipe = getClickedRipePlant(mouseX, mouseY);
          if (hitRipe) {{
            harvestPlant(hitRipe);
            return;
          }}

          let hitStone = getHoveredStone(mouseX, mouseY);
          if (hitStone) {{
            hitStone.glow = 1.0;
            playChimeNote(hitStone.freq, 0.55, 0.10);
            return;
          }}

          if (sprite.hasBucket) {{
            if (isPointInPond(mouseX, mouseY)) {{
              sprite.scoopWater(mouseX, mouseY);
              bloomNextWaterLily();
            }} else if (sprite.isPointOnBucket(mouseX, mouseY)) {{
              sprite.putBucketOnGround();
            }} else if (sprite.bucketHasWater) {{
              sprite.pourWater();
            }}
          }} else {{
            if (isPointInPond(mouseX, mouseY)) {{
              ripples.push(new PaperRipple(mouseX, mouseY));
              playWaterDropSound(true);
              bloomNextWaterLily();
            }} else if (groundBucket && dist(mouseX, mouseY, groundBucket.x, groundBucket.y) < 32) {{
              sprite.pickUpBucket();
            }}
          }}
        }}
      }}

      function drawGroundBucket() {{
        if (!groundBucket) return;

        groundBucket.y = lerp(groundBucket.y, groundBucket.targetY, 0.16);
        groundBucket.scale = lerp(groundBucket.scale, 1, 0.14);

        push();
        translate(groundBucket.x, groundBucket.y);
        scale(groundBucket.scale);

        noStroke();
        fill(45, 55, 35, 48);
        ellipse(0, 16, 34, 9);

        if (sceneState === "GARDEN_ACTIVE" && !sprite.hasBucket && !hasPickedBucketOnce) {{
          let pulse = sin(frameCount * 0.09) * 0.5 + 0.5;
          fill(255, 244, 185, 55 + pulse * 65);
          circle(0, 0, 44 + pulse * 8);
        }}

        setPaperShadow(8, 2, 4, 'rgba(55, 65, 50, 0.24)');
        if (bucketImg) {{
          imageMode(CENTER);
          let bH = 38;
          let bW = bH * (bucketImg.width / bucketImg.height);
          image(bucketImg, 0, 0, bW, bH);
        }} else {{
          fill('#a8c6df');
          stroke('#6b655c');
          strokeWeight(1.2);
          quad(-9, -9, 9, -9, 6, 9, -6, 9);
        }}
        clearShadow();
        pop();
      }}

      function triggerWaterImpact(wx, wy) {{
        ripples.push(new PaperRipple(wx, wy));
        playWaterDropSound(false);

        for (let g of grassBlades) {{
          if (dist(g.x, g.y, wx, wy) < 105) {{
            g.targetGrowth = min(1, g.targetGrowth + 0.55);
          }}
        }}
        let newlyBloomed = false;
        for (let p of plants) {{
          if (dist(p.x, p.y, wx, wy) < 115) {{
            let prevBloom = p.targetBloom;
            p.targetBloom = min(1, p.targetBloom + 0.48);
            if (prevBloom <= 0.65 && p.targetBloom > 0.65) {{
              newlyBloomed = true;
            }}
            if (p.kind === 'flower') {{
              hasWateredFlowers = true;
            }}
          }}
        }}
        if (newlyBloomed) {{
          const pentatonic = [523.25, 587.33, 659.25, 783.99, 880.00, 1046.50];
          playChimeNote(random(pentatonic), 0.7, 0.09);
        }}
      }}

      function drawDoorPortal() {{
        push();
        translate(DOOR_X, DOOR_Y);
        if (sceneState === "HOUSE_CLOSED") {{
          let pulse = sin(frameCount * 0.08) * 0.5 + 0.5;
          noStroke();
          fill(255, 238, 170, 70 + pulse * 85);
          circle(0, 0, 48 + pulse * 10);

          fill(255, 250, 220, 180 + pulse * 75);
          circle(0, sin(frameCount * 0.06) * 4, 7);
        }} else {{
          doorGlow = lerp(doorGlow, 1, 0.05);
          noStroke();
          fill(255, 240, 185, (1 - doorGlow) * 140);
          circle(0, 0, 52 + doorGlow * 40);
        }}
        pop();
      }}

      function setPaperShadow(blur = 8, ox = 3, oy = 5, col = 'rgba(45, 40, 35, 0.22)') {{
        drawingContext.shadowBlur = blur;
        drawingContext.shadowColor = col;
        drawingContext.shadowOffsetX = ox;
        drawingContext.shadowOffsetY = oy;
      }}

      function clearShadow() {{
        drawingContext.shadowBlur = 0;
        drawingContext.shadowOffsetX = 0;
        drawingContext.shadowOffsetY = 0;
      }}

      class OrigamiFrog {{
        constructor() {{
          this.lilyPads = [
            {{ x: 114, y: 386 }},
            {{ x: 182, y: 368 }},
            {{ x: 162, y: 414 }},
            {{ x: 238, y: 418 }},
            {{ x: 288, y: 396 }}
          ];
          this.padIndex = 0;
          this.x = this.lilyPads[0].x;
          this.y = this.lilyPads[0].y;
          this.startX = this.x;
          this.startY = this.y;
          this.targetX = this.x;
          this.targetY = this.y;

          this.isJumping = false;
          this.jumpT = 0;
          this.jumpDuration = 22;
          this.remainingJumps = 0;
          this.pauseTimer = 0;
          this.facing = 1;
          this.squash = 1;
        }}
        isPointOnFrog(px, py) {{
          return dist(px, py, this.x, this.y - 10) < 22;
        }}
        startSingleHop() {{
          this.startX = this.x;
          this.startY = this.y;

          this.padIndex = (this.padIndex + 1) % this.lilyPads.length;
          let nextPad = this.lilyPads[this.padIndex];
          this.targetX = nextPad.x;
          this.targetY = nextPad.y;
          this.facing = this.targetX >= this.startX ? 1 : -1;

          this.isJumping = true;
          this.jumpT = 0;
          ripples.push(new PaperRipple(this.startX, this.startY + 4));
          playFrogHopSound();
        }}
        jumpToNextPad() {{
          if (this.isJumping || this.remainingJumps > 0) return;
          this.remainingJumps = 3;
          this.startSingleHop();
        }}
        update() {{
          if (this.isJumping) {{
            this.jumpT++;
            let progress = constrain(this.jumpT / this.jumpDuration, 0, 1);
            this.x = lerp(this.startX, this.targetX, progress);
            let arcHeight = sin(progress * PI) * 34;
            this.y = lerp(this.startY, this.targetY, progress) - arcHeight;

            if (progress < 0.2) {{
              this.squash = lerp(1, 1.22, progress / 0.2);
            }} else if (progress > 0.85) {{
              this.squash = lerp(1, 0.82, (progress - 0.85) / 0.15);
            }} else {{
              this.squash = lerp(this.squash, 1.05, 0.2);
            }}

            if (progress >= 1) {{
              this.isJumping = false;
              this.x = this.targetX;
              this.y = this.targetY;
              this.squash = 0.85;
              ripples.push(new PaperRipple(this.x, this.y + 4));

              if (this.remainingJumps > 0) {{
                this.pauseTimer = 8;
              }}
            }}
          }} else if (this.pauseTimer > 0) {{
            this.pauseTimer--;
            this.squash = lerp(this.squash, 0.8, 0.3);
            if (this.pauseTimer === 0 && this.remainingJumps > 0) {{
              this.remainingJumps--;
              this.startSingleHop();
            }}
          }} else {{
            this.squash = lerp(this.squash, 1 + sin(frameCount * 0.08) * 0.03, 0.2);
          }}
        }}
        display() {{
          push();
          translate(this.x, this.y);

          let shadowScale = this.isJumping ? map(sin((this.jumpT / this.jumpDuration) * PI), 0, 1, 1, 0.45) : 1;
          noStroke();
          fill(40, 75, 45, 55 * shadowScale);
          ellipse(0, 5, 22 * shadowScale, 7 * shadowScale);

          scale(this.facing * (2 - this.squash), this.squash);
          setPaperShadow(6, 1, 3, 'rgba(35, 65, 40, 0.24)');

          if (frogImg) {{
            imageMode(CENTER);
            let targetH = 32;
            let targetW = targetH * (frogImg.width / frogImg.height);
            image(frogImg, 0, -targetH * 0.35, targetW, targetH);
          }} else {{
            noStroke();
            fill('#5e9c46');
            triangle(-11, 2, -3, -6, -2, 3);
            triangle(11, 2, 3, -6, 2, 3);

            fill('#7bc45c');
            ellipse(0, -5, 22, 16);
            fill('#e9f5d8');
            arc(0, -3, 14, 10, 0, PI);

            fill('#7bc45c');
            circle(-5, -13, 8);
            circle(5, -13, 8);
            fill('#ffffff');
            circle(-5, -13, 5.5);
            circle(5, -13, 5.5);
            fill('#2f362c');
            circle(-4.2, -13, 2.6);
            circle(5.8, -13, 2.6);

            fill('#f4a29e');
            ellipse(-7, -8, 4, 2.2);
            ellipse(7, -8, 4, 2.2);
          }}

          clearShadow();
          pop();
        }}
      }}

      class OrigamiSprite {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.targetX = x;
          this.targetY = y;
          this.visible = false;
          this.scaleVal = 0.1;
          this.trail = [];
          this.vx = 0;

          this.hasBucket = false;
          this.bucketHasWater = false;
          this.bucketScale = 0;
          this.bucketTilt = 0;
          this.pourTimer = 0;
          this.scoopTimer = 0;
        }}
        getBucketWorldPos() {{
          return {{ x: this.x - 24, y: this.y + 20 }};
        }}
        isPointOnBucket(px, py) {{
          if (!this.hasBucket) return false;
          let pos = this.getBucketWorldPos();
          return dist(px, py, pos.x, pos.y) < 18;
        }}
        scoopWater(px, py) {{
          if (!this.hasBucket) return;
          this.bucketHasWater = true;
          this.scoopTimer = 18;
          ripples.push(new PaperRipple(px, py));
          ripples.push(new PaperRipple(px + random(-14, 14), py + random(-8, 8)));
          playWaterDropSound(true);
        }}
        putBucketOnGround() {{
          let pos = this.getBucketWorldPos();
          let landX = constrain(pos.x, 85, width - 85);
          if (landX < 310) {{
            landX = max(landX, 320);
          }}
          if (landX > 435 && landX < 595) {{
            landX = landX < 515 ? 420 : 610;
          }}
          let landY = constrain(pos.y + 130, 445, 515);

          groundBucket = {{
            x: landX,
            y: pos.y,
            targetY: landY,
            scale: 0.9
          }};

          this.hasBucket = false;
          this.bucketScale = 0;
          this.pourTimer = 0;
          this.scoopTimer = 0;
          playChimeNote(392.00, 0.25, 0.07);
        }}
        pickUpBucket() {{
          if (!groundBucket) return;
          hasPickedBucketOnce = true;
          this.targetX = groundBucket.x + 22;
          this.targetY = groundBucket.y - 24;
          this.hasBucket = true;
          this.bucketScale = 0.2;
          groundBucket = null;
          playChimeNote(587.33, 0.28, 0.07);
        }}
        emergeTo(tx, ty) {{
          this.visible = true;
          this.targetX = tx;
          this.targetY = ty;
          if (dist(this.x, this.y, tx, ty) < 20) {{
            sceneState = "GARDEN_ACTIVE";
          }}
        }}
        pourWater() {{
          if (!this.hasBucket || !this.bucketHasWater) return;
          this.pourTimer = 14;
          let spoutX = this.x - 36;
          let spoutY = this.y + 20;
          let dropLandY = constrain(this.y + random(135, 195), 345, 540);
          for (let i = 0; i < 2; i++) {{
            waterDrops.push(new PaperWaterDrop(spoutX + random(-8, 6), spoutY + random(-4, 4), dropLandY));
          }}
        }}
        update() {{
          if (sceneState === "SPRITE_EMERGING") {{
            this.emergeTo(430, 295);
          }}
          if (!this.visible) return;
          this.scaleVal = lerp(this.scaleVal, 1, 0.08);

          if (sceneState === "GARDEN_ACTIVE") {{
            this.targetX = constrain(mouseX, 60, width - 60);
            this.targetY = constrain(mouseY, 80, 395);
          }}

          let hoverY = sin(frameCount * 0.07) * 5;
          let prevX = this.x;
          this.x = lerp(this.x, this.targetX, 0.09);
          this.y = lerp(this.y, this.targetY + hoverY, 0.09);
          this.vx = this.x - prevX;

          if (this.hasBucket) {{
            this.bucketScale = lerp(this.bucketScale, 1, 0.14);
          }}
          if (this.scoopTimer > 0) {{
            this.scoopTimer--;
            this.bucketTilt = lerp(this.bucketTilt, -0.55, 0.25);
          }} else if (this.pourTimer > 0) {{
            this.pourTimer--;
            this.bucketTilt = lerp(this.bucketTilt, -PI / 4, 0.25);
          }} else {{
            this.bucketTilt = lerp(this.bucketTilt, sin(frameCount * 0.1) * 0.07, 0.15);
          }}

          this.trail.push({{ x: this.x, y: this.y + 12, alpha: 175 }});
          if (this.trail.length > 14) this.trail.shift();
        }}
        display() {{
          if (!this.visible) return;

          noStroke();
          for (let t of this.trail) {{
            t.alpha -= 11;
            fill(255, 250, 225, max(0, t.alpha));
            circle(t.x, t.y, map(t.alpha, 0, 175, 2, 7));
          }}

          // 每采满 5 份收获时的星尘庆贺光环
          if (fairyBurstRing > 0.01) {{
            fairyBurstRing = lerp(fairyBurstRing, 0, 0.04);
            noFill();
            stroke(255, 232, 145, fairyBurstRing * 220);
            strokeWeight(2.5);
            circle(this.x, this.y, (1 - fairyBurstRing) * 140 + 30);
            noStroke();
          }}

          // 近期采摘的花朵/蘑菇化作迷你花环在花仙子身旁轻盈环绕一会儿
          for (let i = orbitWreathItems.length - 1; i >= 0; i--) {{
            let w = orbitWreathItems[i];
            w.life--;
            if (w.life <= 0) {{
              orbitWreathItems.splice(i, 1);
              continue;
            }}
            let alpha = w.life < 40 ? map(w.life, 0, 40, 0, 235) : 235;
            let ang = frameCount * 0.04 + (TWO_PI / max(1, orbitWreathItems.length)) * i;
            let ox = this.x + cos(ang) * 46;
            let oy = this.y + sin(ang * 1.2) * 20;

            push();
            translate(ox, oy);
            scale(0.42);
            tint(255, alpha);
            if (w.img) {{
              imageMode(CENTER);
              let targetH = 38;
              let targetW = targetH * (w.img.width / w.img.height);
              image(w.img, 0, 0, targetW, targetH);
            }} else {{
              fill(w.kind === 'flower' ? '#ffafcc' : '#e06d53', alpha);
              circle(0, 0, 18);
            }}
            noTint();
            pop();
          }}

          push();
          translate(this.x, this.y);
          rotate(constrain(this.vx * 0.03, -0.22, 0.22));
          let breathX = 1 + sin(frameCount * 0.22) * 0.035;
          scale(this.scaleVal * breathX, this.scaleVal);
          setPaperShadow(12, 3, 6, 'rgba(55, 65, 50, 0.26)');

          if (fairyImg) {{
            imageMode(CENTER);
            let drawH = 106;
            let drawW = drawH * (fairyImg.width / fairyImg.height);
            image(fairyImg, 0, 0, drawW, drawH);
          }} else {{
            fill('#fff9db');
            circle(0, 0, 40);
          }}

          if (this.hasBucket && this.bucketScale > 0.05) {{
            push();
            translate(-22, 16);
            scale(this.bucketScale);
            rotate(this.bucketTilt);

            if (bucketImg) {{
              imageMode(CENTER);
              let bH = 35;
              let bW = bH * (bucketImg.width / bucketImg.height);
              image(bucketImg, -2, 6, bW, bH);
            }} else {{
              fill('#a8c6df');
              stroke('#6b655c');
              strokeWeight(1.2);
              quad(-9, 0, 9, 0, 6, 18, -6, 18);
            }}
            pop();
          }}

          clearShadow();
          pop();
        }}
      }}

      class PaperWaterDrop {{
        constructor(x, y, targetGroundY) {{
          this.x = x;
          this.y = y;
          this.targetGroundY = targetGroundY;
          this.vy = random(3.5, 5.5);
          this.vx = random(-1.8, -0.6);
          this.rot = random(-0.2, 0.2);
        }}
        update() {{
          this.x += this.vx;
          this.y += this.vy;
          this.vy += 0.18;
        }}
        display() {{
          push();
          translate(this.x, this.y);
          rotate(this.rot);
          noStroke();
          fill('#7ec8e3');
          triangle(0, -10, -6, 2, 0, 8);
          fill('#5aa9c9');
          triangle(0, -10, 6, 2, 0, 8);
          pop();
        }}
      }}

      class PaperRipple {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.r = 6;
          this.alpha = 210;
        }}
        update() {{
          this.r += 2.2;
          this.alpha -= 7;
        }}
        display() {{
          push();
          noFill();
          stroke(100, 180, 215, this.alpha);
          strokeWeight(2.2);
          ellipse(this.x, this.y, this.r * 2, this.r * 0.45);
          pop();
        }}
      }}

      class OrigamiGrass {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.growth = 0.08;
          this.targetGrowth = 0.08;
          this.maxH = random(20, 32);
          this.lean = random(-0.22, 0.22);
        }}
        update() {{
          this.growth = lerp(this.growth, this.targetGrowth, 0.07);
        }}
        display() {{
          let h = this.maxH * this.growth;
          let sway = sin(frameCount * 0.04 + this.x * 0.1) * 3 * this.growth;
          push();
          translate(this.x, this.y);
          setPaperShadow(4, 1, 2, 'rgba(40, 50, 30, 0.16)');
          noStroke();
          fill(this.growth > 0.3 ? '#6ab04c' : '#d5d2be');
          triangle(-5, 0, 0, 0, this.lean * 20 + sway, -h);
          fill(this.growth > 0.3 ? '#529438' : '#c2bfa9');
          triangle(0, 0, 5, 0, this.lean * 20 + sway, -h);
          clearShadow();
          pop();
        }}
      }}

      class CustomPlant {{
        constructor(x, y, kind, variant) {{
          this.x = x;
          this.y = y;
          this.kind = kind;
          this.variant = variant;
          this.bloom = 0.05;
          this.targetBloom = 0.05;
          this.stemHeight = kind === 'flower' ? random(14, 38) : 0;
          this.harvestedFade = 0; // 刚被采摘后的菌丝/嫩叶留痕渐隐
        }}
        update() {{
          this.bloom = lerp(this.bloom, this.targetBloom, 0.065);
          if (this.harvestedFade > 0) {{
            this.harvestedFade = max(0, this.harvestedFade - 0.008);
          }}
        }}
        display() {{
          push();
          translate(this.x, this.y);
          setPaperShadow(8, 2, 4, 'rgba(40, 50, 30, 0.22)');

          if (this.kind === 'mushroom') {{
            if (this.bloom <= 0.2) {{
              noStroke();
              fill('#efe8d8');
              ellipse(0, 0, 12, 6);
              // 刚采走蘑菇后留下浅米色小菌丝环
              if (this.harvestedFade > 0.02) {{
                noFill();
                stroke(245, 240, 225, this.harvestedFade * 190);
                strokeWeight(1.5);
                ellipse(0, 0, 22, 9);
                noStroke();
              }}
            }} else {{
              let s = map(this.bloom, 0.2, 1, 0.15, 1.0);
              let sway = sin(frameCount * 0.03 + this.x) * 0.04 * this.bloom;
              rotate(sway);
              scale(s);

              let img = mushroomImgs.length > 0 ? mushroomImgs[this.variant % mushroomImgs.length] : null;
              if (img) {{
                imageMode(CENTER);
                let targetH = 42;
                let targetW = targetH * (img.width / img.height);
                image(img, 0, -targetH * 0.45, targetW, targetH);
              }} else {{
                noStroke();
                fill('#f7f1e3');
                rect(-6, -20, 12, 20, 4);
                fill('#e06d53');
                arc(0, -18, 32, 26, PI, TWO_PI);
              }}
            }}
          }} else {{
            let curH = this.stemHeight * map(this.bloom, 0.05, 1, 0.22, 1);
            let sway = sin(frameCount * 0.035 + this.x) * 3.5 * this.bloom;

            stroke(this.bloom > 0.22 ? '#588b3e' : '#bfb8a5');
            strokeWeight(2.8);
            line(0, 0, sway, -curH);
            noStroke();

            if (this.bloom > 0.3) {{
              let leafScale = map(this.bloom, 0.3, 1, 0, 1);
              fill('#72ac53');
              push();
              translate(sway * 0.5, -curH * 0.45);
              scale(leafScale);
              triangle(0, 0, -11, -5, -6, 3);
              triangle(0, 0, 11, -6, 6, 2);
              pop();
            }}

            translate(sway, -curH);

            if (this.bloom <= 0.2) {{
              fill('#f3ede0');
              triangle(-6, 0, 0, -13, 0, 0);
              fill('#e2dac9');
              triangle(6, 0, 0, -13, 0, 0);
            }} else {{
              let s = map(this.bloom, 0.2, 1, 0.15, 1.0);
              rotate(sin(frameCount * 0.025 + this.x) * 0.08);
              scale(s);

              let img = flowerImgs.length > 0 ? flowerImgs[this.variant % flowerImgs.length] : null;
              if (img) {{
                imageMode(CENTER);
                let targetH = 44;
                let targetW = targetH * (img.width / img.height);
                image(img, 0, -targetH * 0.15, targetW, targetH);
              }} else {{
                for (let i = 0; i < 4; i++) {{
                  push();
                  rotate(HALF_PI * i);
                  fill('#f28482');
                  triangle(0, 0, 0, -22, 15, -13);
                  fill('#e06361');
                  triangle(0, 0, 15, -13, 11, 0);
                  pop();
                }}
              }}
            }}
          }}

          clearShadow();
          pop();
        }}
      }}

      // ================== 折纸蝴蝶（始终围绕花朵轻盈飞舞） ==================
      class OrigamiButterfly {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.seed = random(1000);
          const cols = ['#ff9f1c', '#ffbf69', '#a0c4ff', '#ffadad', '#bdb2ff', '#ffd166'];
          this.color = random(cols);
          this.targetPlant = null;
          this.switchTimer = int(random(180, 340));
          this.orbitAngle = random(TWO_PI);
          this.orbitDir = random([-1, 1]);
          this.appearScale = 0.05;
        }}
        pickNewFlower() {{
          let bloomedFlowers = plants.filter(p => p.kind === 'flower' && p.bloom > 0.45);
          let allFlowers = plants.filter(p => p.kind === 'flower');
          let pool = bloomedFlowers.length > 0 ? bloomedFlowers : allFlowers;
          if (pool.length > 0) {{
            this.targetPlant = random(pool);
            this.orbitDir = random([-1, 1]);
          }}
        }}
        update() {{
          this.appearScale = lerp(this.appearScale, 1, 0.04);
          this.seed += 0.012;
          this.switchTimer--;
          if (!this.targetPlant || this.targetPlant.bloom <= 0.35 || this.switchTimer <= 0) {{
            this.pickNewFlower();
            this.switchTimer = int(random(220, 380));
          }}

          if (this.targetPlant) {{
            this.orbitAngle += 0.014 * this.orbitDir;
            let destX = this.targetPlant.x + cos(this.orbitAngle) * 26;
            let destY = (this.targetPlant.y - this.targetPlant.stemHeight - 15) + sin(this.orbitAngle * 1.4) * 9;
            this.x = lerp(this.x, destX, 0.015);
            this.y = lerp(this.y, destY, 0.015);
          }} else {{
            this.x += map(noise(this.seed), 0, 1, -0.8, 0.8);
            this.y += map(noise(this.seed + 50), 0, 1, -0.7, 0.7);
          }}

          this.x = constrain(this.x, 45, width - 45);
          this.y = constrain(this.y, 325, 525);
        }}
        display() {{
          let flap = cos(frameCount * 0.16 + this.seed * 10);
          push();
          translate(this.x, this.y);
          rotate(sin(this.seed * 2) * 0.22);
          scale(this.appearScale);
          setPaperShadow(6, 2, 3);
          noStroke();

          push();
          scale(flap, 1);
          fill(this.color);
          triangle(0, 0, -14, -10, -10, 4);
          triangle(0, 2, -10, 4, -7, 10);
          pop();

          push();
          scale(-flap, 1);
          fill(this.color);
          triangle(0, 0, -14, -10, -10, 4);
          triangle(0, 2, -10, 4, -7, 10);
          pop();

          clearShadow();
          pop();
        }}
      }}

      class OrigamiBird {{
        constructor(x, y, tx, ty, variant = 0) {{
          this.x = x;
          this.y = y;
          this.tx = tx;
          this.ty = ty;
          this.variant = variant;
          this.perched = false;
          this.facing = tx >= x ? 1 : -1;
          this.hopTimer = 0;
          this.proximityCooldown = 0;
        }}
        singAndHop() {{
          if (this.hopTimer > 0) return;
          this.hopTimer = 24;
          playBirdChirpSound(this.variant);
          spawnBirdMusicNotes(this.x, this.y);
        }}
        update() {{
          if (!this.perched) {{
            this.x = lerp(this.x, this.tx, 0.032);
            this.y = lerp(this.y, this.ty + sin(frameCount * 0.1) * 5, 0.032);
            if (dist(this.x, this.y, this.tx, this.ty) < 6) {{
              this.perched = true;
              this.x = this.tx;
              this.y = this.ty;
            }}
          }} else {{
            if (this.proximityCooldown > 0) this.proximityCooldown--;
            if (sprite.visible && this.proximityCooldown === 0 && dist(sprite.x, sprite.y, this.x, this.y) < 52) {{
              this.singAndHop();
              this.proximityCooldown = 140;
            }}
          }}

          if (this.hopTimer > 0) {{
            this.hopTimer--;
          }}
        }}
        display() {{
          let hopOffsetY = 0;
          let hopTilt = 0;
          if (this.hopTimer > 0) {{
            let p = 1 - this.hopTimer / 24;
            hopOffsetY = -abs(sin(p * TWO_PI)) * 12;
            hopTilt = sin(p * TWO_PI) * 0.24;
          }}

          push();
          translate(this.x, this.y + hopOffsetY);
          setPaperShadow(8, 2, 4, 'rgba(45, 40, 35, 0.24)');

          let img = birdImgs.length > 0 ? birdImgs[this.variant % birdImgs.length] : null;
          if (img) {{
            let idleTilt = this.perched ? sin(frameCount * 0.04 + this.variant) * 0.05 : sin(frameCount * 0.25) * 0.08;
            let flapScaleY = this.perched ? 1 : (1 + sin(frameCount * 0.32) * 0.06);

            scale(this.facing, flapScaleY);
            rotate(idleTilt + hopTilt);

            imageMode(CENTER);
            let targetH = 44;
            let targetW = targetH * (img.width / img.height);
            image(img, 0, -targetH * 0.35, targetW, targetH);
          }} else {{
            noStroke();
            fill('#e63946');
            triangle(-14, 0, 8, -8, 4, 6);
            fill('#c1121f');
            triangle(-14, 0, -24, -8, -20, 2);
            fill('#f1faee');
            triangle(4, -5, 14, -12, 14, -2);
            fill('#ffb703');
            triangle(14, -9, 21, -7, 14, -5);

            if (!this.perched) {{
              let wingY = sin(frameCount * 0.35) * 14;
              fill('#ffffff');
              triangle(-4, -3, 4, -3, -6, -16 + wingY);
            }}
          }}

          clearShadow();
          pop();
        }}
      }}
    </script>
    </body>
    </html>
    """

    components.html(p5_html, height=580)