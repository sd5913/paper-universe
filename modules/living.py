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
                b64 = base64.b64encode(p.read_bytes()).decode("utf-8")
                return f"data:image/png;base64,{b64}"
    return ""


def render():
    """Display the Living World module."""
    st.header("🌱 Living World: The Origami Meadow")
    st.write(
        "点击折纸小屋唤醒花仙子，出屋后她会提起水桶；移动鼠标并点击/按住左键倾倒浇水，见证草木生长、多造型折纸花绽放与蝶鸟归来。"
    )

    fairy_data_uri = load_asset_data_uri(["fairy.PNG", "fairy.png"])
    bucket_data_uri = load_asset_data_uri(["bucket.PNG", "bucket.png"])

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
          box-shadow: 0 8px 24px rgba(60, 50, 40, 0.12);
        }}
      </style>
    </head>
    <body>
    <script>
      const FAIRY_IMG_DATA = "{fairy_data_uri}";
      const BUCKET_IMG_DATA = "{bucket_data_uri}";
      let fairyImg = null;
      let bucketImg = null;

      let sceneState = "HOUSE_CLOSED"; // HOUSE_CLOSED -> SPRITE_EMERGING -> GARDEN_ACTIVE
      let doorProgress = 0;
      let sprite;
      let house;
      let tree;
      let grassBlades = [];
      let flowers = [];
      let waterDrops = [];
      let ripples = [];
      let butterflies = [];
      let birds = [];
      let bgHills = [];

      const GROUND_Y = 440;

      function preload() {{
        if (FAIRY_IMG_DATA && FAIRY_IMG_DATA.length > 0) {{
          fairyImg = loadImage(FAIRY_IMG_DATA);
        }}
        if (BUCKET_IMG_DATA && BUCKET_IMG_DATA.length > 0) {{
          bucketImg = loadImage(BUCKET_IMG_DATA);
        }}
      }}

      function setup() {{
        createCanvas(860, 540);
        angleMode(RADIANS);

        bgHills = [
          {{ yBase: 360, amp: 45, freq: 0.004, color: '#e4dfd3', offset: 0 }},
          {{ yBase: 395, amp: 30, freq: 0.007, color: '#d7d8c9', offset: 120 }}
        ];

        house = new OrigamiHouse(135, GROUND_Y);
        sprite = new OrigamiSprite(house.x, house.y - 45);
        tree = new OrigamiTree(675, GROUND_Y);

        for (let x = 230; x < 830; x += 14) {{
          grassBlades.push(new OrigamiGrass(x + random(-4, 4), GROUND_Y + random(-2, 6)));
        }}

        const flowerTypes = ['pinwheel', 'lotus', 'tulip'];
        const flowerSpots = [265, 315, 365, 420, 475, 525, 580, 755, 805];
        flowerSpots.forEach((fx, idx) => {{
          let fType = flowerTypes[idx % flowerTypes.length];
          flowers.push(new OrigamiFlower(fx, GROUND_Y + random(2, 10), fType));
        }});
      }}

      function draw() {{
        background('#f7f2e7');
        drawPaperTexture();
        drawSunCorner();
        drawHills();

        setPaperShadow(10, 0, -3, 'rgba(50, 60, 40, 0.12)');
        noStroke();
        fill('#e5dec9');
        rect(0, GROUND_Y, width, height - GROUND_Y);
        clearShadow();

        tree.update();
        tree.display();

        house.update();
        house.display();

        for (let g of grassBlades) {{
          g.update();
          g.display();
        }}

        let bloomedCount = 0;
        for (let f of flowers) {{
          f.update();
          f.display();
          if (f.bloom > 0.75) bloomedCount++;
        }}

        if (bloomedCount >= 4 && butterflies.length < 6 && frameCount % 45 === 0) {{
          let sourceFlower = random(flowers.filter(f => f.bloom > 0.75));
          if (sourceFlower) {{
            butterflies.push(new OrigamiButterfly(sourceFlower.x, sourceFlower.y - sourceFlower.stemHeight));
          }}
        }}
        if (tree.growth > 0.85 && birds.length < 2 && frameCount % 90 === 0) {{
          let perch = tree.getPerchPoint(birds.length);
          birds.push(new OrigamiBird(-30, random(110, 200), perch.x, perch.y));
        }}

        for (let i = ripples.length - 1; i >= 0; i--) {{
          ripples[i].update();
          ripples[i].display();
          if (ripples[i].alpha <= 0) ripples.splice(i, 1);
        }}

        for (let i = waterDrops.length - 1; i >= 0; i--) {{
          waterDrops[i].update();
          waterDrops[i].display();
          if (waterDrops[i].y >= GROUND_Y) {{
            triggerWaterImpact(waterDrops[i].x, GROUND_Y);
            waterDrops.splice(i, 1);
          }}
        }}

        for (let b of butterflies) {{
          b.update();
          b.display();
        }}
        for (let bird of birds) {{
          bird.update();
          bird.display();
        }}

        if (sceneState === "GARDEN_ACTIVE" && mouseIsPressed && frameCount % 7 === 0) {{
          sprite.pourWater();
        }}

        sprite.update();
        sprite.display();

        drawHUD(bloomedCount);
      }}

      function mousePressed() {{
        if (sceneState === "HOUSE_CLOSED") {{
          sceneState = "SPRITE_EMERGING";
        }} else if (sceneState === "GARDEN_ACTIVE") {{
          sprite.pourWater();
        }}
      }}

      function triggerWaterImpact(wx, wy) {{
        ripples.push(new PaperRipple(wx, wy));

        for (let g of grassBlades) {{
          if (abs(g.x - wx) < 85) {{
            g.targetGrowth = min(1, g.targetGrowth + 0.55);
          }}
        }}
        for (let f of flowers) {{
          if (abs(f.x - wx) < 95) {{
            f.targetBloom = min(1, f.targetBloom + 0.45);
          }}
        }}
        if (abs(tree.x - wx) < 160) {{
          tree.targetGrowth = min(1, tree.targetGrowth + 0.35);
        }}
      }}

      function setPaperShadow(blur = 8, ox = 3, oy = 5, col = 'rgba(45, 40, 35, 0.2)') {{
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

      function drawPaperTexture() {{
        stroke(180, 170, 155, 25);
        strokeWeight(1);
        for (let i = 0; i < width; i += 28) {{
          line(i, 0, i - 18, height);
        }}
        noStroke();
      }}

      function drawSunCorner() {{
        push();
        translate(780, 75);
        setPaperShadow(12, 2, 4, 'rgba(220, 160, 50, 0.25)');
        fill('#fbd36b');
        beginShape();
        for (let i = 0; i < 12; i++) {{
          let r = i % 2 === 0 ? 42 : 28;
          let a = (TWO_PI / 12) * i + frameCount * 0.004;
          vertex(cos(a) * r, sin(a) * r);
        }}
        endShape(CLOSE);
        fill('#ffe599');
        triangle(0, 0, -20, -18, 12, -25);
        clearShadow();
        pop();
      }}

      function drawHills() {{
        for (let h of bgHills) {{
          setPaperShadow(10, 0, -2, 'rgba(60, 60, 60, 0.08)');
          fill(h.color);
          beginShape();
          vertex(0, height);
          for (let x = 0; x <= width; x += 60) {{
            let y = h.yBase - abs(sin(x * h.freq + h.offset)) * h.amp;
            vertex(x, y);
          }}
          vertex(width, height);
          endShape(CLOSE);
        }}
        clearShadow();
      }}

      function drawHUD(bloomedCount) {{
        push();
        fill(65, 58, 50, 210);
        noStroke();
        textSize(14);
        textAlign(LEFT, CENTER);
        let msg = "";
        if (sceneState === "HOUSE_CLOSED") {{
          msg = "✨ 点击画面任意处，打开折纸小屋让小精灵飞出来";
        }} else if (sceneState === "SPRITE_EMERGING") {{
          msg = "🧚 小精灵正在飞出小屋并拿起水桶...";
        }} else {{
          msg = `🪣 移动鼠标引导持桶小精灵，点击或长按左键倾倒浇水（已绽放花朵: ${{bloomedCount}}/${{flowers.length}}）`;
        }}
        text(msg, 24, 28);
        pop();
      }}

      class OrigamiHouse {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
        }}
        update() {{
          if (sceneState !== "HOUSE_CLOSED") {{
            doorProgress = lerp(doorProgress, 1, 0.06);
            if (sceneState === "SPRITE_EMERGING" && doorProgress > 0.88) {{
              sprite.emergeTo(340, 220);
            }}
          }}
        }}
        display() {{
          push();
          translate(this.x, this.y);
          setPaperShadow(12, 4, 6);

          fill('#fffaf0');
          quad(-55, 0, 0, 0, 0, -75, -55, -75);
          fill('#efe6d5');
          quad(0, 0, 55, 0, 55, -75, 0, -75);

          fill('#ffdf85');
          rect(-18, -52, 36, 52);

          let foldScale = cos(doorProgress * PI * 0.65);
          fill('#d98a6c');
          push();
          translate(-18, 0);
          scale(foldScale, 1);
          rect(0, -52, 18, 52);
          pop();

          fill('#c67456');
          push();
          translate(18, 0);
          scale(foldScale, 1);
          rect(-18, -52, 18, 52);
          pop();

          fill('#e06d53');
          triangle(-72, -75, 0, -135, 0, -75);
          fill('#c8563d');
          triangle(0, -135, 72, -75, 0, -75);

          clearShadow();
          pop();
        }}
      }}

      // ================== 铃兰花仙子小精灵 + 手持水桶逻辑 ==================
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

          // 水桶专属动画状态
          this.hasBucket = false;
          this.bucketScale = 0;
          this.bucketTilt = 0;
          this.pourTimer = 0;
        }}
        emergeTo(tx, ty) {{
          this.visible = true;
          this.targetX = tx;
          this.targetY = ty;
          if (dist(this.x, this.y, tx, ty) < 18) {{
            sceneState = "GARDEN_ACTIVE";
            this.hasBucket = true; // 出屋到达花园后正式拿起水桶
          }}
        }}
        pourWater() {{
          if (!this.hasBucket) return;
          this.pourTimer = 14; // 触发水桶向前倾倒动画
          // 从水桶口位置洒出水滴（右手侧偏移）
          let spoutX = this.x + 30;
          let spoutY = this.y + 18;
          for (let i = 0; i < 2; i++) {{
            waterDrops.push(new PaperWaterDrop(spoutX + random(-6, 8), spoutY + random(-4, 4)));
          }}
        }}
        update() {{
          if (!this.visible) return;
          this.scaleVal = lerp(this.scaleVal, 1, 0.08);

          if (sceneState === "GARDEN_ACTIVE") {{
            this.targetX = constrain(mouseX, 60, width - 60);
            this.targetY = constrain(mouseY, 70, GROUND_Y - 70);
          }}

          let hoverY = sin(frameCount * 0.07) * 5;
          let prevX = this.x;
          this.x = lerp(this.x, this.targetX, 0.09);
          this.y = lerp(this.y, this.targetY + hoverY, 0.09);
          this.vx = this.x - prevX;

          // 更新水桶出现缩放与倾倒角度
          if (this.hasBucket) {{
            this.bucketScale = lerp(this.bucketScale, 1, 0.12);
          }}
          if (this.pourTimer > 0) {{
            this.pourTimer--;
            this.bucketTilt = lerp(this.bucketTilt, 0.82, 0.25); // 向前倾倒约 47 度
          }} else {{
            this.bucketTilt = lerp(this.bucketTilt, sin(frameCount * 0.1) * 0.08, 0.15); // 平时轻微晃动
          }}

          this.trail.push({{ x: this.x, y: this.y + 12, alpha: 170 }});
          if (this.trail.length > 14) this.trail.shift();
        }}
        display() {{
          if (!this.visible) return;

          noStroke();
          for (let t of this.trail) {{
            t.alpha -= 11;
            fill(215, 238, 205, max(0, t.alpha));
            circle(t.x, t.y, map(t.alpha, 0, 170, 2, 7));
          }}

          push();
          translate(this.x, this.y);
          rotate(constrain(this.vx * 0.03, -0.22, 0.22));
          let breathX = 1 + sin(frameCount * 0.22) * 0.035;
          scale(this.scaleVal * breathX, this.scaleVal);
          setPaperShadow(12, 3, 6, 'rgba(65, 75, 60, 0.22)');

          // 1. 绘制花仙子主体
          if (fairyImg) {{
            imageMode(CENTER);
            let drawH = 104;
            let drawW = drawH * (fairyImg.width / fairyImg.height);
            image(fairyImg, 0, 0, drawW, drawH);
          }} else {{
            fill('#fff9db');
            circle(0, 0, 40);
          }}

          // 2. 出屋后在花仙子右手边（x: +20, y: +16）绘制你设计的水桶
          if (this.hasBucket && this.bucketScale > 0.05) {{
            push();
            translate(20, 16); // 水桶提手挂载在花仙子右手位置（可微调此坐标对齐手部）
            scale(this.bucketScale);
            rotate(this.bucketTilt);

            if (bucketImg) {{
              imageMode(CENTER);
              let bH = 34; // 水桶高度（如果觉得水桶偏大或偏小，直接改这个数字即可）
              let bW = bH * (bucketImg.width / bucketImg.height);
              image(bucketImg, 2, 6, bW, bH);
            }} else {{
              // 若尚未放入 bucket.png 时的折纸水桶占位提示
              fill('#a8c6df');
              stroke('#6b655c');
              strokeWeight(1.2);
              quad(-9, 0, 9, 0, 6, 18, -6, 18);
              noFill();
              arc(0, 0, 16, 14, PI, TWO_PI);
            }}
            pop();
          }}

          clearShadow();
          pop();
        }}
      }}

      class PaperWaterDrop {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.vy = random(3.5, 5.5);
          this.vx = random(0.6, 1.8); // 随水桶倾倒方向略向右前方抛洒
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
          this.alpha = 200;
        }}
        update() {{
          this.r += 2.2;
          this.alpha -= 7;
        }}
        display() {{
          push();
          noFill();
          stroke(110, 185, 215, this.alpha);
          strokeWeight(2);
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
          this.maxH = random(24, 42);
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
          noStroke();
          fill(this.growth > 0.3 ? '#8ec472' : '#d2ccb8');
          triangle(-5, 0, 0, 0, this.lean * 20 + sway, -h);
          fill(this.growth > 0.3 ? '#72a858' : '#c0b9a4');
          triangle(0, 0, 5, 0, this.lean * 20 + sway, -h);
          pop();
        }}
      }}

      class OrigamiFlower {{
        constructor(x, y, type) {{
          this.x = x;
          this.y = y;
          this.type = type;
          this.bloom = 0.05;
          this.targetBloom = 0.05;
          this.stemHeight = random(58, 92);

          const palettes = {{
            pinwheel: ['#f28482', '#e06361', '#ffe5d9'],
            lotus:    ['#f6bd60', '#e59f3c', '#fff3b0'],
            tulip:    ['#b5838d', '#96616b', '#ffcdb2']
          }};
          this.colors = palettes[type];
        }}
        update() {{
          this.bloom = lerp(this.bloom, this.targetBloom, 0.06);
        }}
        display() {{
          let curH = this.stemHeight * map(this.bloom, 0.05, 1, 0.25, 1);
          let sway = sin(frameCount * 0.035 + this.x) * 4 * this.bloom;

          push();
          translate(this.x, this.y);

          stroke(this.bloom > 0.25 ? '#6a994e' : '#bfb8a5');
          strokeWeight(3);
          line(0, 0, sway, -curH);
          noStroke();

          if (this.bloom > 0.3) {{
            let leafScale = map(this.bloom, 0.3, 1, 0, 1);
            fill('#80b960');
            push();
            translate(sway * 0.5, -curH * 0.45);
            scale(leafScale);
            triangle(0, 0, -18, -8, -10, 4);
            triangle(0, 0, 18, -10, 10, 2);
            pop();
          }}

          translate(sway, -curH);
          setPaperShadow(8, 2, 4, 'rgba(50, 40, 35, 0.18)');

          if (this.bloom <= 0.22) {{
            fill('#ede6d6');
            triangle(-6, 0, 0, -14, 0, 0);
            fill('#dcd3c0');
            triangle(6, 0, 0, -14, 0, 0);
          }} else {{
            let s = map(this.bloom, 0.22, 1, 0.2, 1.05);
            scale(s);
            if (this.type === 'pinwheel') {{
              this.drawPinwheel();
            }} else if (this.type === 'lotus') {{
              this.drawLotus();
            }} else {{
              this.drawTulip();
            }}
          }}

          clearShadow();
          pop();
        }}

        drawPinwheel() {{
          rotate(sin(frameCount * 0.02 + this.x) * 0.12);
          for (let i = 0; i < 4; i++) {{
            push();
            rotate(HALF_PI * i);
            fill(this.colors[0]);
            triangle(0, 0, 0, -24, 16, -14);
            fill(this.colors[1]);
            triangle(0, 0, 16, -14, 12, 0);
            pop();
          }}
          fill(this.colors[2]);
          quad(-5, 0, 0, -5, 5, 0, 0, 5);
        }}

        drawLotus() {{
          for (let i = 0; i < 6; i++) {{
            push();
            rotate((TWO_PI / 6) * i);
            fill(this.colors[0]);
            triangle(0, 0, -8, -16, 0, -26);
            fill(this.colors[1]);
            triangle(0, 0, 8, -16, 0, -26);
            pop();
          }}
          for (let i = 0; i < 6; i++) {{
            push();
            rotate((TWO_PI / 6) * i + PI / 6);
            fill(this.colors[2]);
            triangle(0, 0, -5, -10, 0, -16);
            pop();
          }}
        }}

        drawTulip() {{
          fill(this.colors[1]);
          triangle(-14, -8, 0, -26, 0, 4);
          triangle(14, -8, 0, -26, 0, 4);
          fill(this.colors[0]);
          beginShape();
          vertex(0, 6);
          vertex(-15, -6);
          vertex(-13, -24);
          vertex(-5, -15);
          vertex(0, -26);
          vertex(5, -15);
          vertex(13, -24);
          vertex(15, -6);
          endShape(CLOSE);
        }}
      }}

      class OrigamiTree {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.growth = 0.12;
          this.targetGrowth = 0.12;
        }}
        update() {{
          this.growth = lerp(this.growth, this.targetGrowth, 0.05);
        }}
        getPerchPoint(index) {{
          return index === 0
            ? {{ x: this.x - 42, y: this.y - 168 }}
            : {{ x: this.x + 38, y: this.y - 205 }};
        }}
        display() {{
          push();
          translate(this.x, this.y);
          setPaperShadow(12, 4, 6);

          let trunkH = lerp(55, 155, this.growth);
          fill('#9c7a5b');
          quad(-14, 0, 0, 0, 0, -trunkH, -8, -trunkH);
          fill('#7f6044');
          quad(0, 0, 14, 0, 8, -trunkH, 0, -trunkH);

          const tiers = [
            {{ yOff: -trunkH + 15, w: 85, h: 85, c1: '#74b466', c2: '#5a964e', thresh: 0.2 }},
            {{ yOff: -trunkH - 35, w: 68, h: 75, c1: '#88c776', c2: '#6ba85b', thresh: 0.45 }},
            {{ yOff: -trunkH - 80, w: 48, h: 62, c1: '#a3d98e', c2: '#82ba6e', thresh: 0.7 }}
          ];

          for (let t of tiers) {{
            let s = constrain(map(this.growth, t.thresh - 0.2, t.thresh + 0.15, 0.15, 1), 0.15, 1);
            push();
            translate(0, t.yOff);
            scale(s);
            fill(this.growth > 0.25 ? t.c1 : '#dcd5c4');
            triangle(-t.w, 0, 0, -t.h, 0, 0);
            fill(this.growth > 0.25 ? t.c2 : '#cbc3b0');
            triangle(0, -t.h, t.w, 0, 0, 0);
            pop();
          }}

          clearShadow();
          pop();
        }}
      }}

      class OrigamiButterfly {{
        constructor(x, y) {{
          this.x = x;
          this.y = y;
          this.seed = random(1000);
          const cols = ['#ff9f1c', '#ffbf69', '#a0c4ff', '#ffadad', '#bdb2ff'];
          this.color = random(cols);
        }}
        update() {{
          this.seed += 0.025;
          this.x += map(noise(this.seed), 0, 1, -2.2, 2.4);
          this.y += map(noise(this.seed + 50), 0, 1, -2.0, 1.6);
          this.x = constrain(this.x, 80, width - 60);
          this.y = constrain(this.y, 80, GROUND_Y - 35);
        }}
        display() {{
          let flap = cos(frameCount * 0.28 + this.seed * 10);
          push();
          translate(this.x, this.y);
          rotate(sin(this.seed * 3) * 0.25);
          setPaperShadow(6, 2, 3);
          noStroke();

          push();
          scale(flap, 1);
          fill(this.color);
          triangle(0, 0, -16, -12, -12, 4);
          triangle(0, 2, -12, 4, -8, 12);
          pop();

          push();
          scale(-flap, 1);
          fill(this.color);
          triangle(0, 0, -16, -12, -12, 4);
          triangle(0, 2, -12, 4, -8, 12);
          pop();

          clearShadow();
          pop();
        }}
      }}

      class OrigamiBird {{
        constructor(x, y, tx, ty) {{
          this.x = x;
          this.y = y;
          this.tx = tx;
          this.ty = ty;
          this.perched = false;
        }}
        update() {{
          if (!this.perched) {{
            this.x = lerp(this.x, this.tx, 0.035);
            this.y = lerp(this.y, this.ty + sin(frameCount * 0.1) * 5, 0.035);
            if (dist(this.x, this.y, this.tx, this.ty) < 6) {{
              this.perched = true;
              this.x = this.tx;
              this.y = this.ty;
            }}
          }}
        }}
        display() {{
          push();
          translate(this.x, this.y);
          setPaperShadow(8, 2, 4);
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

          clearShadow();
          pop();
        }}
      }}
    </script>
    </body>
    </html>
    """

    components.html(p5_html, height=560)