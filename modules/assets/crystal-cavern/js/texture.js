/* ============================================
   texture.js — 全局视听：折纸质感与投影
   成员 D 负责模块
   ============================================
   - 暖棕剪纸洞窟背景（弧形分层纸边）
   - 岩壁嵌晶、藤蔓纹理
   - 水晶光斑投影（几何光斑投射到洞壁）
   - 折纸投影效果（柔和阴影）
   ============================================ */

const TextureManager = {
  paperBuffer: null,    // 离屏纸张纹理缓存
  sparkBuffer: null,    // 微光缓存
  lightSpots: [],       // 几何光斑列表
  bgImage: null,        // 外部背景图

  init() {
    this._createPaperTexture();
    this._createSparkField();
  },

  // 接收 sketch.js preload 加载好的背景图
  setBackgroundImage(img) {
    this.bgImage = img;
  },

  // --- 创建纸张噪点纹理（离屏缓存） ---
  _createPaperTexture() {
    this.paperBuffer = createGraphics(CONFIG.CANVAS_W, CONFIG.CANVAS_H);
    this.paperBuffer.noStroke();
    // 细密噪点 — 模拟卡纸纤维
    for (let i = 0; i < 3000; i++) {
      let x = random(CONFIG.CANVAS_W);
      let y = random(CONFIG.CANVAS_H);
      let n = noise(x * 0.01, y * 0.01);
      let alpha = n * 18;
      let bright = n > 0.5 ? 255 : 210;
      this.paperBuffer.fill(bright, bright - 10, bright - 20, alpha);
      this.paperBuffer.circle(x, y, random(0.5, 1.8));
    }
    // 较大的纸纹斑块
    for (let i = 0; i < 200; i++) {
      let x = random(CONFIG.CANVAS_W);
      let y = random(CONFIG.CANVAS_H);
      let n = noise(x * 0.005, y * 0.005);
      this.paperBuffer.fill(255, 245, 235, n * 10);
      this.paperBuffer.circle(x, y, random(3, 8));
    }
  },

  // --- 创建空中微光（暖色小亮点） ---
  _createSparkField() {
    this.sparkBuffer = createGraphics(CONFIG.CANVAS_W, CONFIG.CANVAS_H);
    this.sparkBuffer.noStroke();
    for (let i = 0; i < 80; i++) {
      let x = random(CONFIG.CANVAS_W);
      let y = random(CONFIG.CANVAS_H * 0.75);
      let size = random(0.5, 2);
      let alpha = random(30, 120);
      this.sparkBuffer.fill(255, 230, 200, alpha);
      this.sparkBuffer.circle(x, y, size);
    }
  },

  // --- 叠加纸张纹理 ---
  drawPaperOverlay() {
    if (this.paperBuffer) {
      push();
      tint(255, 255, 255, 35);
      image(this.paperBuffer, 0, 0);
      noTint();
      pop();
    }
  },

  // --- 绘制微光 ---
  drawSparkField(litAmount) {
    if (this.sparkBuffer) {
      push();
      let alpha = 120 + litAmount * 100;
      tint(255, 255, 255, alpha);
      image(this.sparkBuffer, 0, 0);
      noTint();
      pop();
    }
  },

  // --- 洞窟环境 ---
  drawCavernBackground(litAmount) {
    // 如果加载了外部背景图，直接绘制图片
    if (this.bgImage && this.bgImage.width > 0) {
      push();
      imageMode(CORNER);
      image(this.bgImage, 0, 0, CONFIG.CANVAS_W, CONFIG.CANVAS_H);
      pop();

      // 仍可叠加轻微纸张纹理，让交互元素与背景更融合
      this.drawPaperOverlay();
      return;
    }

    // 暖棕渐变背景（中心稍亮，四周暗）
    let topC = lerpHex(CONFIG.PALETTE.cavernDeep, '#3d2d24', litAmount * 0.4);
    let botC = lerpHex(CONFIG.PALETTE.cavernDark, '#5c4235', litAmount * 0.3);
    noStroke();
    for (let y = 0; y < CONFIG.CANVAS_H; y += 2) {
      let t = y / CONFIG.CANVAS_H;
      let c = lerpHex(topC, botC, t);
      fill(c);
      rect(0, y, CONFIG.CANVAS_W, 2);
    }

    // 微光
    this.drawSparkField(litAmount);

    // 洞窟墙壁轮廓（弧形分层剪纸）
    this._drawCavernWalls(litAmount);

    // 地面（与洞壁融为一体的剪纸地面）
    this._drawCavernFloor(litAmount);

    // 纸张纹理叠加
    this.drawPaperOverlay();
  },

  // --- 洞窟墙壁：弧形分层剪纸立体书效果 ---
  _drawCavernWalls(litAmount) {
    let wallDark = lerpHex(CONFIG.PALETTE.cavernDeep, '#2d211a', 0.5);
    let wallBase = lerpHex('#2d211a', CONFIG.PALETTE.cavernWallLit, litAmount * 0.5);
    let wallLit = lerpHex('#4a372b', '#7a5a4a', litAmount * 0.6);

    // 绘制多层弧形剪纸边缘（左右各3层）
    let layers = 4;
    for (let l = layers; l >= 0; l--) {
      let t = l / layers;
      let c = lerpHex(wallDark, wallBase, t);
      let inset = 10 + l * 35;
      let waveAmp = 12 + l * 4;

      // 左墙弧形层
      noStroke();
      fill(c);
      beginShape();
      vertex(0, 0);
      vertex(0, CONFIG.CAVERN_FLOOR + 20);
      for (let y = CONFIG.CAVERN_FLOOR + 20; y >= 0; y -= 15) {
        let w = inset + sin(y * 0.015 + l * 1.3) * waveAmp + noise(y * 0.008, l) * 25;
        vertex(w, y);
      }
      endShape(CLOSE);

      // 右墙弧形层
      fill(c);
      beginShape();
      vertex(CONFIG.CANVAS_W, 0);
      vertex(CONFIG.CANVAS_W, CONFIG.CAVERN_FLOOR + 20);
      for (let y = CONFIG.CAVERN_FLOOR + 20; y >= 0; y -= 15) {
        let w = CONFIG.CANVAS_W - (inset + sin(y * 0.015 + l * 1.3 + 2) * waveAmp + noise(y * 0.008, l + 10) * 25);
        vertex(w, y);
      }
      endShape(CLOSE);

      // 层间阴影线
      if (l > 0) {
        stroke(CONFIG.PALETTE.paperShadow);
        strokeWeight(1.5);
        let prevInset = 10 + (l - 1) * 35;
        for (let y = 20; y < CONFIG.CAVERN_FLOOR; y += 35) {
          let w = inset + sin(y * 0.015 + l * 1.3) * waveAmp + noise(y * 0.008, l) * 25;
          let pw = prevInset + sin(y * 0.015 + (l - 1) * 1.3) * (12 + (l - 1) * 4) + noise(y * 0.008, l - 1) * 25;
          line(pw, y, w, y);
          let rw = CONFIG.CANVAS_W - (inset + sin(y * 0.015 + l * 1.3 + 2) * waveAmp + noise(y * 0.008, l + 10) * 25);
          let rpw = CONFIG.CANVAS_W - (prevInset + sin(y * 0.015 + (l - 1) * 1.3 + 2) * (12 + (l - 1) * 4) + noise(y * 0.008, l + 9) * 25);
          line(rpw, y, rw, y);
        }
        noStroke();
      }
    }

    // 藤蔓/根须纹理（沿墙壁垂下）
    stroke(wallLit);
    strokeWeight(1.2);
    noFill();
    for (let i = 0; i < 6; i++) {
      let sx = 60 + i * 140 + noise(i) * 40;
      beginShape();
      for (let y = 30; y < CONFIG.CAVERN_FLOOR; y += 20) {
        let x = sx + sin(y * 0.02 + i * 2) * (15 + i * 3);
        curveVertex(x, y);
      }
      endShape();
    }
    noStroke();

    // 墙壁上的嵌晶（粉白发光，随点亮增强）
    if (litAmount > 0.05) {
      let crystalAlpha = constrain((litAmount - 0.05) * 350, 0, 255);
      for (let i = 0; i < 10; i++) {
        let side = i % 2 === 0 ? 1 : -1;
        let cx = side === 1
          ? 35 + noise(i * 4.1) * 90
          : CONFIG.CANVAS_W - (35 + noise(i * 4.1) * 90);
        let cy = 50 + (i * 47) % (CONFIG.CAVERN_FLOOR - 100);
        let cs = 6 + noise(i * 6.2) * 10;
        this._drawEmbeddedCrystal(cx, cy, cs, crystalAlpha);
      }
    }
  },

  // --- 嵌在墙壁上的小水晶 ---
  _drawEmbeddedCrystal(x, y, s, alpha) {
    push();
    translate(x, y);
    rotate(noise(x * 0.1, y * 0.1) * TWO_PI);
    // 投影
    drawingContext.shadowOffsetX = 0;
    drawingContext.shadowOffsetY = 3;
    drawingContext.shadowBlur = 8;
    drawingContext.shadowColor = 'rgba(0, 0, 0, 0.4)';
    // 底层
    fill(140, 100, 110, alpha);
    noStroke();
    beginShape();
    for (let j = 0; j < 6; j++) {
      let a = j * PI / 3;
      vertex(cos(a) * s, sin(a) * s);
    }
    endShape(CLOSE);
    drawingContext.shadowBlur = 0;
    drawingContext.shadowOffsetY = 0;
    // 顶层（偏小偏亮）
    fill(255, 220, 225, alpha);
    beginShape();
    for (let j = 0; j < 6; j++) {
      let a = j * PI / 3;
      vertex(cos(a) * s * 0.7, sin(a) * s * 0.7 - s * 0.08);
    }
    endShape(CLOSE);
    // 高光
    fill(255, 245, 240, alpha * 0.8);
    circle(-s * 0.15, -s * 0.2, s * 0.35);
    pop();
  },

  // --- 地面：与洞壁相连的分层剪纸地面 ---
  _drawCavernFloor(litAmount) {
    let floorDark = lerpHex('#1f1612', '#3d2d24', litAmount);
    let floorBase = lerpHex('#2d211a', '#5c4235', litAmount);
    let floorHi = lerpHex('#4a372b', '#7a5a4a', litAmount * 0.7);

    // 底层（大，带顶部投影）
    drawingContext.shadowOffsetX = 0;
    drawingContext.shadowOffsetY = -5;
    drawingContext.shadowBlur = 14;
    drawingContext.shadowColor = 'rgba(0, 0, 0, 0.5)';
    noStroke();
    fill(floorDark);
    beginShape();
    vertex(0, CONFIG.CAVERN_FLOOR);
    for (let x = 0; x <= CONFIG.CANVAS_W; x += 25) {
      let y = CONFIG.CAVERN_FLOOR + noise(x * 0.018) * 14 - 7;
      vertex(x, y);
    }
    vertex(CONFIG.CANVAS_W, CONFIG.CANVAS_H);
    vertex(0, CONFIG.CANVAS_H);
    endShape(CLOSE);
    drawingContext.shadowBlur = 0;
    drawingContext.shadowOffsetY = 0;

    // 顶层（偏亮，略向上缩）
    fill(floorBase);
    beginShape();
    vertex(0, CONFIG.CAVERN_FLOOR + 6);
    for (let x = 0; x <= CONFIG.CANVAS_W; x += 25) {
      let y = CONFIG.CAVERN_FLOOR + noise(x * 0.018) * 12 - 2;
      vertex(x, y);
    }
    vertex(CONFIG.CANVAS_W, CONFIG.CANVAS_H);
    vertex(0, CONFIG.CANVAS_H);
    endShape(CLOSE);

    // 顶部边缘高光
    fill(floorHi);
    rect(0, CONFIG.CAVERN_FLOOR + 3, CONFIG.CANVAS_W, 4);

    // 地面上的小石块/土丘（让元素更好融入）
    for (let i = 0; i < 5; i++) {
      let mx = 80 + i * 180 + noise(i * 3) * 40;
      let my = CONFIG.CAVERN_FLOOR + 15 + noise(i * 5) * 10;
      let ms = 10 + noise(i * 7) * 14;
      fill(lerpHex('#2d211a', '#4a372b', litAmount));
      ellipse(mx, my, ms * 1.6, ms);
      fill(lerpHex('#4a372b', '#7a5a4a', litAmount * 0.5));
      ellipse(mx - 2, my - 2, ms * 0.9, ms * 0.55);
    }
  },

  // --- 几何光斑投影（水晶发光时投射到墙壁） ---
  spawnLightSpot(x, y, color, size) {
    this.lightSpots.push({
      x: x, y: y,
      vx: random(-20, 20),
      vy: random(-15, 15),
      color: color,
      size: size || random(15, 35),
      rotation: random(TWO_PI),
      rotSpeed: random(-1, 1),
      life: 1.0,
      shape: floor(random(3)), // 0=三角 1=六边形 2=菱形
    });
  },

  updateLightSpots(dt) {
    for (let i = this.lightSpots.length - 1; i >= 0; i--) {
      let s = this.lightSpots[i];
      s.x += s.vx * dt;
      s.y += s.vy * dt;
      s.rotation += s.rotSpeed * dt;
      s.life -= dt * 0.3;
      if (s.life <= 0) this.lightSpots.splice(i, 1);
    }
  },

  drawLightSpots() {
    push();
    blendMode(ADD);
    noStroke();
    for (let s of this.lightSpots) {
      let rgb = hexToRgb(s.color);
      fill(rgb.r, rgb.g, rgb.b, s.life * 60);
      push();
      translate(s.x, s.y);
      rotate(s.rotation);
      let sz = s.size * s.life;
      if (s.shape === 0) {
        triangle(0, -sz, sz * 0.87, sz * 0.5, -sz * 0.87, sz * 0.5);
      } else if (s.shape === 1) {
        beginShape();
        for (let i = 0; i < 6; i++) {
          let a = i * PI / 3;
          vertex(cos(a) * sz, sin(a) * sz);
        }
        endShape(CLOSE);
      } else {
        quad(0, -sz, sz * 0.7, 0, 0, sz, -sz * 0.7, 0);
      }
      pop();
    }
    blendMode(BLEND);
    pop();
  },

  // --- 柔和投影 ---
  drawShadow(x, y, w, h, alpha) {
    noStroke();
    fill(0, 0, 0, alpha || 25);
    ellipse(x + 3, y + 4, w, h);
  },

  // --- 折纸折痕线（用于元素绘制） ---
  drawFoldLines(x, y, size, angle, alpha) {
    push();
    translate(x, y);
    rotate(angle);
    stroke(255, 255, 255, alpha || 40);
    strokeWeight(0.6);
    line(-size * 0.7, 0, size * 0.7, 0);
    line(0, -size * 0.7, 0, size * 0.7);
    line(-size * 0.5, -size * 0.5, size * 0.5, size * 0.5);
    line(-size * 0.5, size * 0.5, size * 0.5, -size * 0.5);
    noStroke();
    pop();
  },
};
