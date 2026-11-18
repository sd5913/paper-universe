import streamlit as st
import streamlit.components.v1 as components


def render():
    """Display the Living World module."""
    st.header("🌱 Living World: The Origami Meadow")
    st.write(
        "点击折纸小屋唤醒小精灵，移动鼠标并点击/按住左键在花园中浇水，见证草木生长、多造型折纸花绽放与蝶鸟归来。"
    )

    p5_html = """
    <!DOCTYPE html>
    <html lang="zh">
    <head>
      <meta charset="UTF-8" />
      <script src="https://cdnjs.cloudflare.com/ajax/libs/p5.js/1.9.0/p5.min.js"></script>
      <style>
        html, body {
          margin: 0;
          padding: 0;
          overflow: hidden;
          background: #f6f1e7;
          font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
        }
        canvas {
          display: block;
          border-radius: 14px;
          box-shadow: 0 8px 24px rgba(60, 50, 40, 0.12);
        }
      </style>
    </head>
    <body>
    <script>
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

      function setup() {
        createCanvas(860, 540);
        angleMode(RADIANS);

        // 初始化远山剪纸层
        bgHills = [
          { yBase: 360, amp: 45, freq: 0.004, color: '#e4dfd3', offset: 0 },
          { yBase: 395, amp: 30, freq: 0.007, color: '#d7d8c9', offset: 120 }
        ];

        // 初始化左侧折纸小屋
        house = new OrigamiHouse(135, GROUND_Y);

        // 初始化小精灵（初始藏在屋里）
        sprite = new OrigamiSprite(house.x, house.y - 45);

        // 初始化折纸大树（在花园右侧）
        tree = new OrigamiTree(675, GROUND_Y);

        // 初始化地面折纸小草
        for (let x = 230; x < 830; x += 14) {
          grassBlades.push(new OrigamiGrass(x + random(-4, 4), GROUND_Y + random(-2, 6)));
        }

        // 初始化不同种类的折纸花苞（分布在不同位置）
        const flowerTypes = ['pinwheel', 'lotus', 'tulip'];
        const flowerSpots = [265, 315, 365, 420, 475, 525, 580, 755, 805];
        flowerSpots.forEach((fx, idx) => {
          let fType = flowerTypes[idx % flowerTypes.length];
          flowers.push(new OrigamiFlower(fx, GROUND_Y + random(2, 10), fType));
        });
      }

      function draw() {
        // 温暖的手工和纸底色
        background('#f7f2e7');
        drawPaperTexture();
        drawSunCorner();
        drawHills();

        // 地面剪纸层
        setPaperShadow(10, 0, -3, 'rgba(50, 60, 40, 0.12)');
        noStroke();
        fill('#e5dec9');
        rect(0, GROUND_Y, width, height - GROUND_Y);
        clearShadow();

        // 更新并绘制折纸大树
        tree.update();
        tree.display();

        // 绘制折纸小屋
        house.update();
        house.display();

        // 更新并绘制小草
        for (let g of grassBlades) {
          g.update();
          g.display();
        }

        // 更新并绘制多种折纸花
        let bloomedCount = 0;
        for (let f of flowers) {
          f.update();
          f.display();
          if (f.bloom > 0.75) bloomedCount++;
        }

        // 当足够多花朵开放且大树长成时，召唤折纸蝴蝶与小鸟
        if (bloomedCount >= 4 && butterflies.length < 6 && frameCount % 45 === 0) {
          let sourceFlower = random(flowers.filter(f => f.bloom > 0.75));
          if (sourceFlower) {
            butterflies.push(new OrigamiButterfly(sourceFlower.x, sourceFlower.y - sourceFlower.stemHeight));
          }
        }
        if (tree.growth > 0.85 && birds.length < 2 && frameCount % 90 === 0) {
          let perch = tree.getPerchPoint(birds.length);
          birds.push(new OrigamiBird(-30, random(110, 200), perch.x, perch.y));
        }

        // 绘制地面水波纹
        for (let i = ripples.length - 1; i >= 0; i--) {
          ripples[i].update();
          ripples[i].display();
          if (ripples[i].alpha <= 0) ripples.splice(i, 1);
        }

        // 绘制折纸水滴
        for (let i = waterDrops.length - 1; i >= 0; i--) {
          waterDrops[i].update();
          waterDrops[i].display();
          if (waterDrops[i].y >= GROUND_Y) {
            triggerWaterImpact(waterDrops[i].x, GROUND_Y);
            waterDrops.splice(i, 1);
          }
        }

        // 绘制蝴蝶与小鸟
        for (let b of butterflies) {
          b.update();
          b.display();
        }
        for (let bird of birds) {
          bird.update();
          bird.display();
        }

        // 持续按住鼠标浇水
        if (sceneState === "GARDEN_ACTIVE" && mouseIsPressed && frameCount % 7 === 0) {
          sprite.pourWater();
        }

        // 更新并绘制小精灵
        sprite.update();
        sprite.display();

        // 顶部柔和交互提示条
        drawHUD(bloomedCount);
      }

      function mousePressed() {
        if (sceneState === "HOUSE_CLOSED") {
          sceneState = "SPRITE_EMERGING";
        } else if (sceneState === "GARDEN_ACTIVE") {
          sprite.pourWater();
        }
      }

      function triggerWaterImpact(wx, wy) {
        ripples.push(new PaperRipple(wx, wy));

        // 唤醒附近小草
        for (let g of grassBlades) {
          if (abs(g.x - wx) < 85) {
            g.targetGrowth = min(1, g.targetGrowth + 0.55);
          }
        }
        // 唤醒附近花朵
        for (let f of flowers) {
          if (abs(f.x - wx) < 95) {
            f.targetBloom = min(1, f.targetBloom + 0.45);
          }
        }
        // 浇到大树附近时唤醒大树
        if (abs(tree.x - wx) < 160) {
          tree.targetGrowth = min(1, tree.targetGrowth + 0.35);
        }
      }

      // ================== 辅助：折纸质感与阴影 ==================
      function setPaperShadow(blur = 8, ox = 3, oy = 5, col = 'rgba(45, 40, 35, 0.2)') {
        drawingContext.shadowBlur = blur;
        drawingContext.shadowColor = col;
        drawingContext.shadowOffsetX = ox;
        drawingContext.shadowOffsetY = oy;
      }

      function clearShadow() {
        drawingContext.shadowBlur = 0;
        drawingContext.shadowOffsetX = 0;
        drawingContext.shadowOffsetY = 0;
      }

      function drawPaperTexture() {
        stroke(180, 170, 155, 25);
        strokeWeight(1);
        for (let i = 0; i < width; i += 28) {
          line(i, 0, i - 18, height);
        }
        noStroke();
      }

      function drawSunCorner() {
        push();
        translate(780, 75);
        setPaperShadow(12, 2, 4, 'rgba(220, 160, 50, 0.25)');
        fill('#fbd36b');
        beginShape();
        for (let i = 0; i < 12; i++) {
          let r = i % 2 === 0 ? 42 : 28;
          let a = (TWO_PI / 12) * i + frameCount * 0.004;
          vertex(cos(a) * r, sin(a) * r);
        }
        endShape(CLOSE);
        fill('#ffe599');
        triangle(0, 0, -20, -18, 12, -25);
        clearShadow();
        pop();
      }

      function drawHills() {
        for (let h of bgHills) {
          setPaperShadow(10, 0, -2, 'rgba(60, 60, 60, 0.08)');
          fill(h.color);
          beginShape();
          vertex(0, height);
          for (let x = 0; x <= width; x += 60) {
            let y = h.yBase - abs(sin(x * h.freq + h.offset)) * h.amp;
            vertex(x, y);
          }
          vertex(width, height);
          endShape(CLOSE);
        }
        clearShadow();
      }

      function drawHUD(bloomedCount) {
        push();
        fill(65, 58, 50, 210);
        noStroke();
        textSize(14);
        textAlign(LEFT, CENTER);
        let msg = "";
        if (sceneState === "HOUSE_CLOSED") {
          msg = "✨ 点击画面任意处，打开折纸小屋让小精灵飞出来";
        } else if (sceneState === "SPRITE_EMERGING") {
          msg = "🧚 小精灵正在飞出小屋...";
        } else {
          msg = `💧 移动鼠标引导小精灵，点击或长按左键浇水唤醒花园（已绽放花朵: ${bloomedCount}/${flowers.length}）`;
        }
        text(msg, 24, 28);
        pop();
      }

      // ================== 类 1：立体折纸小屋 ==================
      class OrigamiHouse {
        constructor(x, y) {
          this.x = x;
          this.y = y;
        }
        update() {
          if (sceneState !== "HOUSE_CLOSED") {
            doorProgress = lerp(doorProgress, 1, 0.06);
            if (sceneState === "SPRITE_EMERGING" && doorProgress > 0.88) {
              sprite.emergeTo(340, 220);
            }
          }
        }
        display() {
          push();
          translate(this.x, this.y);
          setPaperShadow(12, 4, 6);

          // 屋身左折面 & 右折面
          fill('#fffaf0');
          quad(-55, 0, 0, 0, 0, -75, -55, -75);
          fill('#efe6d5');
          quad(0, 0, 55, 0, 55, -75, 0, -75);

          // 门框内部暖光
          fill('#ffdf85');
          rect(-18, -52, 36, 52);

          // 双开折纸门扇（随 doorProgress 向外翻折）
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

          // 三角折纸屋顶（双面明暗分色）
          fill('#e06d53');
          triangle(-72, -75, 0, -135, 0, -75);
          fill('#c8563d');
          triangle(0, -135, 72, -75, 0, -75);

          clearShadow();
          pop();
        }
      }

      // ================== 类 2：折纸小精灵 ==================
      class OrigamiSprite {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.targetX = x;
          this.targetY = y;
          this.visible = false;
          this.scaleVal = 0.1;
          this.trail = [];
        }
        emergeTo(tx, ty) {
          this.visible = true;
          this.targetX = tx;
          this.targetY = ty;
          if (dist(this.x, this.y, tx, ty) < 18) {
            sceneState = "GARDEN_ACTIVE";
          }
        }
        pourWater() {
          for (let i = 0; i < 2; i++) {
            waterDrops.push(new PaperWaterDrop(this.x + random(-14, 14), this.y + 18));
          }
        }
        update() {
          if (!this.visible) return;
          this.scaleVal = lerp(this.scaleVal, 1, 0.08);

          if (sceneState === "GARDEN_ACTIVE") {
            this.targetX = constrain(mouseX, 60, width - 60);
            this.targetY = constrain(mouseY, 60, GROUND_Y - 55);
          }

          let hoverY = sin(frameCount * 0.08) * 6;
          this.x = lerp(this.x, this.targetX, 0.09);
          this.y = lerp(this.y, this.targetY + hoverY, 0.09);

          this.trail.push({ x: this.x, y: this.y, alpha: 180 });
          if (this.trail.length > 14) this.trail.shift();
        }
        display() {
          if (!this.visible) return;

          // 飞行微光纸屑尾迹
          noStroke();
          for (let t of this.trail) {
            t.alpha -= 12;
            fill(255, 225, 130, max(0, t.alpha));
            push();
            translate(t.x, t.y);
            rotate(t.alpha * 0.05);
            triangle(-4, 0, 4, -3, 2, 4);
            pop();
          }

          push();
          translate(this.x, this.y);
          scale(this.scaleVal);
          setPaperShadow(14, 0, 6, 'rgba(255, 195, 70, 0.45)');

          let wingFlap = sin(frameCount * 0.25) * 0.35;

          // 折纸精灵双翼
          fill('#fff9db');
          push();
          rotate(-0.3 + wingFlap);
          triangle(0, -4, -34, -22, -22, 8);
          pop();
          push();
          rotate(0.3 - wingFlap);
          triangle(0, -4, 34, -22, 22, 8);
          pop();

          // 折纸精灵菱形身体（双面折痕）
          fill('#ffdf78');
          triangle(0, -22, -13, 2, 0, 18);
          fill('#f4be46');
          triangle(0, -22, 13, 2, 0, 18);

          // 头顶折纸皇冠/触角
          fill('#ffffff');
          triangle(0, -22, -6, -32, 0, -26);
          triangle(0, -22, 6, -32, 0, -26);

          clearShadow();
          pop();
        }
      }

      // ================== 类 3：折纸水滴与水波纹 ==================
      class PaperWaterDrop {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.vy = random(3.5, 5.5);
          this.rot = random(-0.2, 0.2);
        }
        update() {
          this.y += this.vy;
          this.vy += 0.18;
        }
        display() {
          push();
          translate(this.x, this.y);
          rotate(this.rot);
          noStroke();
          fill('#7ec8e3');
          triangle(0, -10, -6, 2, 0, 8);
          fill('#5aa9c9');
          triangle(0, -10, 6, 2, 0, 8);
          pop();
        }
      }

      class PaperRipple {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.r = 6;
          this.alpha = 200;
        }
        update() {
          this.r += 2.2;
          this.alpha -= 7;
        }
        display() {
          push();
          noFill();
          stroke(110, 185, 215, this.alpha);
          strokeWeight(2);
          ellipse(this.x, this.y, this.r * 2, this.r * 0.45);
          pop();
        }
      }

      // ================== 类 4：折纸小草 ==================
      class OrigamiGrass {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.growth = 0.08;
          this.targetGrowth = 0.08;
          this.maxH = random(24, 42);
          this.lean = random(-0.22, 0.22);
        }
        update() {
          this.growth = lerp(this.growth, this.targetGrowth, 0.07);
        }
        display() {
          let h = this.maxH * this.growth;
          let sway = sin(frameCount * 0.04 + this.x * 0.1) * 3 * this.growth;
          push();
          translate(this.x, this.y);
          noStroke();
          // 左半草叶（亮绿）
          fill(this.growth > 0.3 ? '#8ec472' : '#d2ccb8');
          triangle(-5, 0, 0, 0, this.lean * 20 + sway, -h);
          // 右半草叶（暗绿折痕）
          fill(this.growth > 0.3 ? '#72a858' : '#c0b9a4');
          triangle(0, 0, 5, 0, this.lean * 20 + sway, -h);
          pop();
        }
      }

      // ================== 类 5：多造型折纸花朵 ==================
      class OrigamiFlower {
        constructor(x, y, type) {
          this.x = x;
          this.y = y;
          this.type = type; // 'pinwheel' | 'lotus' | 'tulip'
          this.bloom = 0.05;
          this.targetBloom = 0.05;
          this.stemHeight = random(58, 92);

          const palettes = {
            pinwheel: ['#f28482', '#e06361', '#ffe5d9'],
            lotus:    ['#f6bd60', '#e59f3c', '#fff3b0'],
            tulip:    ['#b5838d', '#96616b', '#ffcdb2']
          };
          this.colors = palettes[type];
        }
        update() {
          this.bloom = lerp(this.bloom, this.targetBloom, 0.06);
        }
        display() {
          let curH = this.stemHeight * map(this.bloom, 0.05, 1, 0.25, 1);
          let sway = sin(frameCount * 0.035 + this.x) * 4 * this.bloom;

          push();
          translate(this.x, this.y);

          // 折纸花茎
          stroke(this.bloom > 0.25 ? '#6a994e' : '#bfb8a5');
          strokeWeight(3);
          line(0, 0, sway, -curH);
          noStroke();

          // 对生小折纸叶
          if (this.bloom > 0.3) {
            let leafScale = map(this.bloom, 0.3, 1, 0, 1);
            fill('#80b960');
            push();
            translate(sway * 0.5, -curH * 0.45);
            scale(leafScale);
            triangle(0, 0, -18, -8, -10, 4);
            triangle(0, 0, 18, -10, 10, 2);
            pop();
          }

          // 移动到花头位置绘制不同折纸造型
          translate(sway, -curH);
          setPaperShadow(8, 2, 4, 'rgba(50, 40, 35, 0.18)');

          if (this.bloom <= 0.22) {
            // 未开放时的白色折纸花苞
            fill('#ede6d6');
            triangle(-6, 0, 0, -14, 0, 0);
            fill('#dcd3c0');
            triangle(6, 0, 0, -14, 0, 0);
          } else {
            let s = map(this.bloom, 0.22, 1, 0.2, 1.05);
            scale(s);
            if (this.type === 'pinwheel') {
              this.drawPinwheel();
            } else if (this.type === 'lotus') {
              this.drawLotus();
            } else {
              this.drawTulip();
            }
          }

          clearShadow();
          pop();
        }

        // 造型 1：四瓣风车折纸花
        drawPinwheel() {
          rotate(sin(frameCount * 0.02 + this.x) * 0.12);
          for (let i = 0; i < 4; i++) {
            push();
            rotate(HALF_PI * i);
            fill(this.colors[0]);
            triangle(0, 0, 0, -24, 16, -14);
            fill(this.colors[1]);
            triangle(0, 0, 16, -14, 12, 0);
            pop();
          }
          fill(this.colors[2]);
          quad(-5, 0, 0, -5, 5, 0, 0, 5);
        }

        // 造型 2：六边形层叠折纸莲花
        drawLotus() {
          for (let i = 0; i < 6; i++) {
            push();
            rotate((TWO_PI / 6) * i);
            fill(this.colors[0]);
            triangle(0, 0, -8, -16, 0, -26);
            fill(this.colors[1]);
            triangle(0, 0, 8, -16, 0, -26);
            pop();
          }
          for (let i = 0; i < 6; i++) {
            push();
            rotate((TWO_PI / 6) * i + PI / 6);
            fill(this.colors[2]);
            triangle(0, 0, -5, -10, 0, -16);
            pop();
          }
        }

        // 造型 3：几何锯齿折纸郁金香
        drawTulip() {
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
        }
      }

      // ================== 类 6：层叠折纸大树 ==================
      class OrigamiTree {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.growth = 0.12;
          this.targetGrowth = 0.12;
        }
        update() {
          this.growth = lerp(this.growth, this.targetGrowth, 0.05);
        }
        getPerchPoint(index) {
          return index === 0
            ? { x: this.x - 42, y: this.y - 168 }
            : { x: this.x + 38, y: this.y - 205 };
        }
        display() {
          push();
          translate(this.x, this.y);
          setPaperShadow(12, 4, 6);

          // 折纸树干（双面立体）
          let trunkH = lerp(55, 155, this.growth);
          fill('#9c7a5b');
          quad(-14, 0, 0, 0, 0, -trunkH, -8, -trunkH);
          fill('#7f6044');
          quad(0, 0, 14, 0, 8, -trunkH, 0, -trunkH);

          // 三层叠折三角树冠（随 growth 逐层弹出）
          const tiers = [
            { yOff: -trunkH + 15, w: 85, h: 85, c1: '#74b466', c2: '#5a964e', thresh: 0.2 },
            { yOff: -trunkH - 35, w: 68, h: 75, c1: '#88c776', c2: '#6ba85b', thresh: 0.45 },
            { yOff: -trunkH - 80, w: 48, h: 62, c1: '#a3d98e', c2: '#82ba6e', thresh: 0.7 }
          ];

          for (let t of tiers) {
            let s = constrain(map(this.growth, t.thresh - 0.2, t.thresh + 0.15, 0.15, 1), 0.15, 1);
            push();
            translate(0, t.yOff);
            scale(s);
            fill(this.growth > 0.25 ? t.c1 : '#dcd5c4');
            triangle(-t.w, 0, 0, -t.h, 0, 0);
            fill(this.growth > 0.25 ? t.c2 : '#cbc3b0');
            triangle(0, -t.h, t.w, 0, 0, 0);
            pop();
          }

          clearShadow();
          pop();
        }
      }

      // ================== 类 7：折纸蝴蝶 ==================
      class OrigamiButterfly {
        constructor(x, y) {
          this.x = x;
          this.y = y;
          this.seed = random(1000);
          const cols = ['#ff9f1c', '#ffbf69', '#a0c4ff', '#ffadad', '#bdb2ff'];
          this.color = random(cols);
        }
        update() {
          this.seed += 0.025;
          this.x += map(noise(this.seed), 0, 1, -2.2, 2.4);
          this.y += map(noise(this.seed + 50), 0, 1, -2.0, 1.6);
          this.x = constrain(this.x, 80, width - 60);
          this.y = constrain(this.y, 80, GROUND_Y - 35);
        }
        display() {
          let flap = cos(frameCount * 0.28 + this.seed * 10);
          push();
          translate(this.x, this.y);
          rotate(sin(this.seed * 3) * 0.25);
          setPaperShadow(6, 2, 3);
          noStroke();

          // 左翼
          push();
          scale(flap, 1);
          fill(this.color);
          triangle(0, 0, -16, -12, -12, 4);
          triangle(0, 2, -12, 4, -8, 12);
          pop();

          // 右翼
          push();
          scale(-flap, 1);
          fill(this.color);
          triangle(0, 0, -16, -12, -12, 4);
          triangle(0, 2, -12, 4, -8, 12);
          pop();

          clearShadow();
          pop();
        }
      }

      // ================== 类 8：折纸小鸟 ==================
      class OrigamiBird {
        constructor(x, y, tx, ty) {
          this.x = x;
          this.y = y;
          this.tx = tx;
          this.ty = ty;
          this.perched = false;
        }
        update() {
          if (!this.perched) {
            this.x = lerp(this.x, this.tx, 0.035);
            this.y = lerp(this.y, this.ty + sin(frameCount * 0.1) * 5, 0.035);
            if (dist(this.x, this.y, this.tx, this.ty) < 6) {
              this.perched = true;
              this.x = this.tx;
              this.y = this.ty;
            }
          }
        }
        display() {
          push();
          translate(this.x, this.y);
          setPaperShadow(8, 2, 4);
          noStroke();

          // 折纸鸟身体与尾翼
          fill('#e63946');
          triangle(-14, 0, 8, -8, 4, 6);
          // 尾羽
          fill('#c1121f');
          triangle(-14, 0, -24, -8, -20, 2);
          // 头部与鸟喙
          fill('#f1faee');
          triangle(4, -5, 14, -12, 14, -2);
          fill('#ffb703');
          triangle(14, -9, 21, -7, 14, -5);

          // 飞行时扇动折纸翅膀
          if (!this.perched) {
            let wingY = sin(frameCount * 0.35) * 14;
            fill('#ffffff');
            triangle(-4, -3, 4, -3, -6, -16 + wingY);
          }

          clearShadow();
          pop();
        }
      }
    </script>
    </body>
    </html>
    """

    components.html(p5_html, height=560)