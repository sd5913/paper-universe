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
        "点击蘑菇屋的拱形木门唤醒花仙子，出屋后她会提起水壶；移动鼠标并点击/按住左键向左倾倒浇水，唤醒草地上的立体折纸花草与蝶鸟。"
    )

    bg_data_uri = load_asset_data_uri(["bg.jpg", "bg.JPG", "bg.png", "bg.PNG"])
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
          box-shadow: 0 8px 24px rgba(60, 50, 40, 0.14);
        }}
      </style>
    </head>
    <body>
    <script>
      const BG_IMG_DATA = "{bg_data_uri}";
      const FAIRY_IMG_DATA = "{fairy_data_uri}";
      const BUCKET_IMG_DATA = "{bucket_data_uri}";

      let bgImg = null;
      let fairyImg = null;
      let bucketImg = null;

      let sceneState = "HOUSE_CLOSED"; // HOUSE_CLOSED -> SPRITE_EMERGING -> GARDEN_ACTIVE
      let doorGlow = 0;
      let sprite;
      let grassBlades = [];
      let flowers = [];
      let waterDrops = [];
      let ripples = [];
      let butterflies = [];
      let birds = [];
      let gardenVitality = 0;

      // 对齐背景图中蘑菇小屋拱形门洞中心坐标（860x560画布下）
      const DOOR_X = 576;
      const DOOR_Y = 328;

      function preload() {{
        if (BG_IMG_DATA && BG_IMG_DATA.length > 0) {{
          bgImg = loadImage(BG_IMG_DATA);
        }}
        if (FAIRY_IMG_DATA && FAIRY_IMG_DATA.length > 0) {{
          fairyImg = loadImage(FAIRY_IMG_DATA);
        }}
        if (BUCKET_IMG_DATA && BUCKET_IMG_DATA.length > 0) {{
          bucketImg = loadImage(BUCKET_IMG_DATA);
        }}
      }}

      function setup() {{
        createCanvas(860, 560);
        angleMode(RADIANS);

        // 花仙子初始从拱形门洞内部飞出
        sprite = new OrigamiSprite(DOOR_X, DOOR_Y);

        // 在背景图草地空白区域布置可生长的立体折纸小草（避开荷花池与石子路）
        const grassZones = [
          {{ x1: 255, x2: 395, y1: 475, y2: 535 }},
          {{ x1: 405, x2: 560, y1: 480, y2: 535 }},
          {{ x1: 590, x2: 735, y1: 445, y2: 525 }},
          {{ x1: 710, x2: 815, y1: 390, y2: 455 }}
        ];
        for (let z of grassZones) {{
          for (let x = z.x1; x <= z.x2; x += 22) {{
            grassBlades.push(new OrigamiGrass(x + random(-5, 5), random(z.y1, z.y2)));
          }}
        }}

        // 在草地前景与右侧花园布置 3 种不同造型的立体折纸花朵
        const flowerConfigs = [
          {{ x: 295, y: 515, type: 'pinwheel' }},
          {{ x: 355, y: 502, type: 'lotus' }},
          {{ x: 425, y: 522, type: 'tulip' }},
          {{ x: 545, y: 505, type: 'pinwheel' }},
          {{ x: 615, y: 492, type: 'lotus' }},
          {{ x: 675, y: 512, type: 'tulip' }},
          {{ x: 745, y: 445, type: 'pinwheel' }},
          {{ x: 795, y: 425, type: 'lotus' }}
        ];
        for (let cfg of flowerConfigs) {{
          flowers.push(new OrigamiFlower(cfg.x, cfg.y, cfg.type));
        }}
      }}

      function draw() {{
        // 1. 绘制你的纸片拼贴背景图
        if (bgImg) {{
          imageMode(CORNER);
          image(bgImg, 0, 0, width, height);
        }} else {{
          background('#f7f2e7');
        }}

        // 2. 小屋拱形门洞唤醒微光提示（未开门前呼吸闪烁）
        drawDoorPortal();

        // 3. 更新并绘制可生长的立体折纸小草
        for (let g of grassBlades) {{
          g.update();
          g.display();
        }}

        // 4. 更新并绘制多种立体折纸花朵
        let bloomedCount = 0;
        let totalBloom = 0;
        for (let f of flowers) {{
          f.update();
          f.display();
          totalBloom += f.bloom;
          if (f.bloom > 0.72) bloomedCount++;
        }}
        gardenVitality = totalBloom / flowers.length;

        // 5. 花朵陆续开放后，召唤折纸蝴蝶在花丛与池塘上方飞舞
        if (bloomedCount >= 3 && butterflies.length < 6 && frameCount % 45 === 0) {{
          let sourceFlower = random(flowers.filter(f => f.bloom > 0.72));
          if (sourceFlower) {{
            butterflies.push(new OrigamiButterfly(sourceFlower.x, sourceFlower.y - sourceFlower.stemHeight));
          }}
        }}

        // 6. 花园活力达到一定程度后，折纸小鸟飞入并停落在左右两棵剪纸大树枝头
        if (gardenVitality > 0.55 && birds.length < 2 && frameCount % 90 === 0) {{
          const treePerches = [
            {{ x: 112, y: 205 }}, // 左侧绿色剪纸大树枝头
            {{ x: 748, y: 195 }}  // 右侧黄绿色剪纸大树枝头
          ];
          let perch = treePerches[birds.length];
          birds.push(new OrigamiBird(birds.length === 0 ? -30 : width + 30, random(90, 160), perch.x, perch.y));
        }}

        // 7. 绘制水波纹（落在草地或荷花池水面都会激起涟漪）
        for (let i = ripples.length - 1; i >= 0; i--) {{
          ripples[i].update();
          ripples[i].display();
          if (ripples[i].alpha <= 0) ripples.splice(i, 1);
        }}

        // 8. 绘制折纸水滴下落与碰撞
        for (let i = waterDrops.length - 1; i >= 0; i--) {{
          waterDrops[i].update();
          waterDrops[i].display();
          if (waterDrops[i].y >= waterDrops[i].targetGroundY) {{
            triggerWaterImpact(waterDrops[i].x, waterDrops[i].y);
            waterDrops.splice(i, 1);
          }}
        }}

        // 9. 绘制折纸蝴蝶与小鸟
        for (let b of butterflies) {{
          b.update();
          b.display();
        }}
        for (let bird of birds) {{
          bird.update();
          bird.display();
        }}

        // 10. 按住鼠标持续浇水
        if (sceneState === "GARDEN_ACTIVE" && mouseIsPressed && frameCount % 7 === 0) {{
          sprite.pourWater();
        }}

        // 11. 更新并绘制花仙子与左侧水壶
        sprite.update();
        sprite.display();

        // 12. 顶部半透明纸条提示栏
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

        // 唤醒附近小草
        for (let g of grassBlades) {{
          if (dist(g.x, g.y, wx, wy) < 105) {{
            g.targetGrowth = min(1, g.targetGrowth + 0.55);
          }}
        }}
        // 唤醒附近花朵
        for (let f of flowers) {{
          if (dist(f.x, f.y, wx, wy) < 115) {{
            f.targetBloom = min(1, f.targetBloom + 0.45);
          }}
        }}
      }}

      function drawDoorPortal() {{
        push();
        translate(DOOR_X, DOOR_Y);
        if (sceneState === "HOUSE_CLOSED") {{
          let pulse = sin(frameCount * 0.08) * 0.5 + 0.5;
          noStroke();
          fill(255, 238, 170, 70 + pulse * 85);
          ellipse(0, 0, 44 + pulse * 10, 62 + pulse * 10);

          // 门前浮动小光点提示
          fill(255, 250, 220, 180 + pulse * 75);
          circle(0, -10 + sin(frameCount * 0.06) * 4, 7);
        }} else {{
          doorGlow = lerp(doorGlow, 1, 0.05);
          noStroke();
          fill(255, 240, 185, (1 - doorGlow) * 140);
          ellipse(0, 0, 50 + doorGlow * 40, 68 + doorGlow * 40);
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

      function drawHUD(bloomedCount) {{
        push();
        // 柔和的米白半透明剪纸标签底框，确保在蓝色天空背景上文字清晰
        setPaperShadow(8, 0, 3, 'rgba(50, 60, 70, 0.14)');
        fill(252, 249, 242, 225);
        noStroke();
        rect(18, 14, 595, 34, 17);
        clearShadow();

        fill(65, 58, 50, 235);
        textSize(13.5);
        textAlign(LEFT, CENTER);
        let msg = "";
        if (sceneState === "HOUSE_CLOSED") {{
          msg = "✨ 点击画面（或蘑菇屋的拱形木门），唤醒花仙子飞出花园";
        }} else if (sceneState === "SPRITE_EMERGING") {{
          msg = "🧚 花仙子正在飞出蘑菇屋并提起水壶...";
        }} else {{
          msg = `🪣 移动鼠标引导花仙子，点击/按住左键向左倾倒浇水（已唤醒折纸花: ${{bloomedCount}}/${{flowers.length}}）`;
        }}
        text(msg, 34, 31);
        pop();
      }}

      // ================== 铃兰花仙子小精灵 + 左侧手持水壶（向左倾斜45度浇水） ==================
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
          this.bucketScale = 0;
          this.bucketTilt = 0;
          this.pourTimer = 0;
        }}
        emergeTo(tx, ty) {{
          this.visible = true;
          this.targetX = tx;
          this.targetY = ty;
          if (dist(this.x, this.y, tx, ty) < 20) {{
            sceneState = "GARDEN_ACTIVE";
            this.hasBucket = true;
          }}
        }}
        pourWater() {{
          if (!this.hasBucket) return;
          this.pourTimer = 14;
          // 从左侧水壶倾倒后的壶嘴位置洒出水滴，落点在花仙子下方草地/池塘高度
          let spoutX = this.x - 36;
          let spoutY = this.y + 20;
          let dropLandY = constrain(this.y + random(135, 195), 375, 540);
          for (let i = 0; i < 2; i++) {{
            waterDrops.push(new PaperWaterDrop(spoutX + random(-8, 6), spoutY + random(-4, 4), dropLandY));
          }}
        }}
        update() {{
          if (sceneState === "SPRITE_EMERGING") {{
            this.emergeTo(430, 270);
          }}
          if (!this.visible) return;
          this.scaleVal = lerp(this.scaleVal, 1, 0.08);

          if (sceneState === "GARDEN_ACTIVE") {{
            this.targetX = constrain(mouseX, 75, width - 75);
            this.targetY = constrain(mouseY, 80, 395);
          }}

          let hoverY = sin(frameCount * 0.07) * 5;
          let prevX = this.x;
          this.x = lerp(this.x, this.targetX, 0.09);
          this.y = lerp(this.y, this.targetY + hoverY, 0.09);
          this.vx = this.x - prevX;

          if (this.hasBucket) {{
            this.bucketScale = lerp(this.bucketScale, 1, 0.12);
          }}
          if (this.pourTimer > 0) {{
            this.pourTimer--;
            this.bucketTilt = lerp(this.bucketTilt, -PI / 4, 0.25); // 向左倾斜45度
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

          push();
          translate(this.x, this.y);
          rotate(constrain(this.vx * 0.03, -0.22, 0.22));
          let breathX = 1 + sin(frameCount * 0.22) * 0.035;
          scale(this.scaleVal * breathX, this.scaleVal);
          setPaperShadow(12, 3, 6, 'rgba(55, 65, 50, 0.26)');

          // 1. 绘制花仙子主体
          if (fairyImg) {{
            imageMode(CENTER);
            let drawH = 106;
            let drawW = drawH * (fairyImg.width / fairyImg.height);
            image(fairyImg, 0, 0, drawW, drawH);
          }} else {{
            fill('#fff9db');
            circle(0, 0, 40);
          }}

          // 2. 出屋后在花仙子左边绘制水壶，浇水时向左倾斜 45 度
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
          this.vx = random(-1.8, -0.6); // 随向左倾倒的水壶向左下方抛洒
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
          this.maxH = random(22, 36);
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

      class OrigamiFlower {{
        constructor(x, y, type) {{
          this.x = x;
          this.y = y;
          this.type = type;
          this.bloom = 0.05;
          this.targetBloom = 0.05;
          this.stemHeight = random(48, 72);

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
          setPaperShadow(6, 2, 3, 'rgba(40, 50, 30, 0.18)');

          stroke(this.bloom > 0.25 ? '#588b3e' : '#bfb8a5');
          strokeWeight(3);
          line(0, 0, sway, -curH);
          noStroke();

          if (this.bloom > 0.3) {{
            let leafScale = map(this.bloom, 0.3, 1, 0, 1);
            fill('#72ac53');
            push();
            translate(sway * 0.5, -curH * 0.45);
            scale(leafScale);
            triangle(0, 0, -16, -7, -9, 4);
            triangle(0, 0, 16, -9, 9, 2);
            pop();
          }}

          translate(sway, -curH);

          if (this.bloom <= 0.22) {{
            fill('#f3ede0');
            triangle(-6, 0, 0, -13, 0, 0);
            fill('#e2dac9');
            triangle(6, 0, 0, -13, 0, 0);
          }} else {{
            let s = map(this.bloom, 0.22, 1, 0.2, 1.0);
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
            triangle(0, 0, 0, -22, 15, -13);
            fill(this.colors[1]);
            triangle(0, 0, 15, -13, 11, 0);
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
            triangle(0, 0, -7, -15, 0, -24);
            fill(this.colors[1]);
            triangle(0, 0, 7, -15, 0, -24);
            pop();
          }}
          for (let i = 0; i < 6; i++) {{
            push();
            rotate((TWO_PI / 6) * i + PI / 6);
            fill(this.colors[2]);
            triangle(0, 0, -5, -9, 0, -15);
            pop();
          }}
        }}

        drawTulip() {{
          fill(this.colors[1]);
          triangle(-13, -7, 0, -24, 0, 4);
          triangle(13, -7, 0, -24, 0, 4);
          fill(this.colors[0]);
          beginShape();
          vertex(0, 5);
          vertex(-14, -5);
          vertex(-12, -22);
          vertex(-4, -14);
          vertex(0, -24);
          vertex(4, -14);
          vertex(12, -22);
          vertex(14, -5);
          endShape(CLOSE);
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
          this.y = constrain(this.y, 80, 440);
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

    components.html(p5_html, height=580)