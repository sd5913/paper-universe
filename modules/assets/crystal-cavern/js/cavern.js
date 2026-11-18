/* ============================================
   cavern.js — 场景三：水晶洞窟 (The Crystal Cavern)
   成员 D：场景三与全局视听
   ============================================
   【故事背景】
   小精灵跟随纸蝴蝶进入地底洞窟，这里沉睡着
   维系整个折纸世界能量的"折纸之心"。洞窟漆黑
   一片，需要利用自然元素与矿石的结合，点亮
   整个地底世界。

   【合成链】
   1. 岩石 + 春雨 = 原石（多面体折纸矿石生长）
   2. 原石 + 太阳 = 发光水晶（粉白色光晕+几何光斑）
   3. 发光水晶 + 野花丛 = 折纸之心（生命之树展开）

   【交互动词】
   拖拽元素使其重叠 → 自动检测配方 → 合成新物质

   【视觉特色】
   - 暖棕剪纸洞窟（弧形分层纸边）
   - 元素与场景融合（岩石生根、云垂藤蔓、花长茎、日在窗框）
   - 粉白水晶发光与折纸之心
   ============================================ */

// ===== 缓动函数 =====
const EaseOutCubic = t => 1 - Math.pow(1 - t, 3);
const EaseInOutCubic = t => t < 0.5 ? 4*t*t*t : 1 - Math.pow(-2*t+2,3)/2;
const EaseOutBack = t => { const c1=1.70158, c3=c1+1; return 1+c3*Math.pow(t-1,3)+c1*Math.pow(t-1,2) };
const EaseOutElastic = t => { if(t===0||t===1)return t; const c4=(2*Math.PI)/3; return Math.pow(2,-10*t)*Math.sin((t*10-0.75)*c4)+1 };

// ===== 暖棕剪纸风绘制辅助函数 =====
const PAPER_SHADOW = 'rgba(30, 18, 12, 0.42)';

// 在当前 translate/scale 之后的局部坐标系中绘制多边形剪纸
function drawPaperShape(radius, npoints, fillR, fillG, fillB, strokeR, strokeG, strokeB) {
  drawingContext.shadowOffsetX = 0;
  drawingContext.shadowOffsetY = 5;
  drawingContext.shadowBlur = 12;
  drawingContext.shadowColor = PAPER_SHADOW;
  fill(fillR, fillG, fillB);
  stroke(strokeR, strokeG, strokeB);
  strokeWeight(2);
  beginShape();
  let angle = TWO_PI / npoints;
  for (let a = 0; a < TWO_PI; a += angle) {
    vertex(cos(a) * radius, sin(a) * radius);
  }
  endShape(CLOSE);
  drawingContext.shadowBlur = 0;
  drawingContext.shadowOffsetY = 0;
}

// 剪纸风分层椭圆
function drawPaperEllipse(w, h, baseR, baseG, baseB, topR, topG, topB) {
  drawingContext.shadowOffsetX = 0;
  drawingContext.shadowOffsetY = 5;
  drawingContext.shadowBlur = 10;
  drawingContext.shadowColor = PAPER_SHADOW;
  noStroke();
  fill(baseR, baseG, baseB);
  ellipse(0, 3, w, h);
  drawingContext.shadowBlur = 0;
  drawingContext.shadowOffsetY = 0;
  fill(topR, topG, topB);
  ellipse(0, 0, w * 0.8, h * 0.8);
}

// 剪纸风分层多边形（底层 + 顶层 + 高光三角）
function drawPaperLayered(radius, npoints, baseR, baseG, baseB, topR, topG, topB, hiR, hiG, hiB) {
  drawingContext.shadowOffsetX = 0;
  drawingContext.shadowOffsetY = 5;
  drawingContext.shadowBlur = 12;
  drawingContext.shadowColor = PAPER_SHADOW;
  fill(baseR, baseG, baseB);
  stroke(baseR * 0.55, baseG * 0.55, baseB * 0.55);
  strokeWeight(2);
  beginShape();
  let angle = TWO_PI / npoints;
  for (let a = 0; a < TWO_PI; a += angle) {
    vertex(cos(a) * radius, sin(a) * radius);
  }
  endShape(CLOSE);
  drawingContext.shadowBlur = 0;
  drawingContext.shadowOffsetY = 0;
  noStroke();
  fill(topR, topG, topB);
  beginShape();
  for (let a = 0; a < TWO_PI; a += angle) {
    vertex(cos(a) * radius * 0.78, sin(a) * radius * 0.78 - radius * 0.08);
  }
  endShape(CLOSE);
  if (hiR !== undefined) {
    fill(hiR, hiG, hiB, 180);
    beginShape();
    vertex(0, -radius * 0.7);
    vertex(radius * 0.3, -radius * 0.35);
    vertex(-radius * 0.15, -radius * 0.3);
    endShape(CLOSE);
  }
}

// 绘制藤蔓/根须曲线
function drawVine(x1, y1, x2, y2, thickness, colorR, colorG, colorB, alpha) {
  stroke(colorR, colorG, colorB, alpha);
  strokeWeight(thickness);
  noFill();
  beginShape();
  let steps = 12;
  for (let i = 0; i <= steps; i++) {
    let t = i / steps;
    let x = lerp(x1, x2, t) + sin(t * PI * 2 + i * 0.3) * (8 - t * 4);
    let y = lerp(y1, y2, t);
    curveVertex(x, y);
  }
  endShape();
  noStroke();
}

// ===== 元素类 =====
class GameElement {
  constructor(type, x, y) {
    this.type = type;
    this.x = x; this.y = y;
    this.homeX = x; this.homeY = y;
    this.vx = 0; this.vy = 0;
    this.size = type === 'heart' ? 50 : (type === 'sun' ? 38 : 34);
    this.dragging = false;
    this.dragOffX = 0; this.dragOffY = 0;
    this.bobPhase = random(TWO_PI);
    this.scale = 0.3;
    this.targetScale = 1;
    this.glow = 0;
    this.consumed = false;
    this.spawnTime = 0;
    this.info = ELEMENT_INFO[type] || { name: type, color: '#FFF' };
  }

  update(dt) {
    this.spawnTime += dt;
    this.scale += (this.targetScale - this.scale) * min(1, dt * 8);
    this.bobPhase += dt * 1.5;

    if (this.dragging) {
      this.x = mouseX - this.dragOffX;
      this.y = mouseY - this.dragOffY;
    } else if (!this.consumed) {
      // 回弹到原位
      let dx = this.homeX - this.x;
      let dy = this.homeY - this.y;
      this.vx += dx * dt * 15;
      this.vy += dy * dt * 15;
      this.vx *= 0.80;
      this.vy *= 0.80;
      this.x += this.vx * dt;
      this.y += this.vy * dt;
    }

    if (this.type === 'crystal') {
      this.glow = 0.7 + 0.3 * sin(this.bobPhase * 2);
    }
  }

  contains(x, y) {
    return dist(x, y, this.x, this.y) < this.size + 8;
  }

  overlaps(other) {
    return dist(this.x, this.y, other.x, other.y) < (this.size + other.size) * 0.7;
  }

  draw() {
    if (this.consumed) return;
    let bob = sin(this.bobPhase) * 2.5;
    let s = this.scale;
    if (s < 0.01) return;

    push();
    translate(this.x, this.y + bob);
    scale(s);

    // 绘制元素与场景的连接（藤蔓/根须/茎），让它看起来不是独立个体
    // 当使用外部背景图时，背景已包含这些连接，跳过绘制
    if (!TextureManager.bgImage) {
      this._drawAnchors();
    }

    switch (this.type) {
      case 'rock':      this._drawRock(); break;
      case 'rain':      this._drawRain(); break;
      case 'sun':       this._drawSun(); break;
      case 'flowers':   this._drawFlowers(); break;
      case 'raw_stone': this._drawRawStone(); break;
      case 'crystal':   this._drawCrystal(); break;
      case 'heart':     this._drawHeart(); break;
    }

    // 标签
    if (this.scale > 0.5) {
      fill(CONFIG.PALETTE.paper);
      textSize(11);
      textAlign(CENTER, CENTER);
      textStyle(BOLD);
      text(this.info.name, 0, this.size + 20);
      textStyle(NORMAL);
    }

    pop();
  }

  // --- 元素与场景的连接件 ---
  _drawAnchors() {
    if (this.type === 'rock') {
      // 从岩石底部向下生根
      for (let i = -2; i <= 2; i++) {
        drawVine(i * 8, this.size * 0.7, i * 12, this.size * 1.6,
                 2, 90, 70, 55, 120);
      }
    } else if (this.type === 'rain') {
      // 云朵向上连到洞顶
      for (let i = -1; i <= 1; i++) {
        drawVine(i * 12, -this.size * 0.8, i * 18, -this.size * 2.2,
                 2, 120, 110, 100, 100);
      }
    } else if (this.type === 'flowers') {
      // 花丛向下扎根
      for (let i = -2; i <= 2; i++) {
        drawVine(i * 10, this.size * 0.6, i * 14, this.size * 1.5,
                 1.8, 80, 100, 60, 120);
      }
    }
  }

  // --- 岩石：左下角棕色几何石块堆 ---
  _drawRock() {
    let s = this.size;
    push();
    // 三颗大小不一的石块
    let rocks = [
      { x: -s * 0.3, y: s * 0.35, r: s * 0.6, n: 5, rot: 0.2 },
      { x: s * 0.25, y: s * 0.45, r: s * 0.45, n: 6, rot: 0.8 },
      { x: s * 0.05, y: -s * 0.15, r: s * 0.55, n: 5, rot: -0.3 },
    ];
    for (let r of rocks) {
      push();
      translate(r.x, r.y);
      rotate(r.rot + this.bobPhase * 0.03);
      drawPaperLayered(r.r, r.n,
        120, 95, 72,    // base: 深棕
        166, 139, 106,  // top: 浅棕
        200, 180, 150   // highlight: 亮棕
      );
      // 折痕线
      stroke(80, 60, 45, 120);
      strokeWeight(0.8);
      line(0, -r.r * 0.6, 0, r.r * 0.5);
      line(-r.r * 0.4, 0, r.r * 0.4, 0);
      noStroke();
      pop();
    }
    pop();
  }

  // --- 春雨：灰色云朵 + 垂下的藤蔓雨滴 ---
  _drawRain() {
    let s = this.size;
    // 云朵（由几个椭圆组成）
    push();
    drawingContext.shadowOffsetX = 0;
    drawingContext.shadowOffsetY = 5;
    drawingContext.shadowBlur = 12;
    drawingContext.shadowColor = PAPER_SHADOW;
    fill(160, 152, 142);
    noStroke();
    ellipse(-s * 0.4, -s * 0.2, s * 0.9, s * 0.55);
    ellipse(s * 0.3, -s * 0.25, s * 0.8, s * 0.5);
    ellipse(0, 0, s * 1.1, s * 0.6);
    // 亮面
    fill(190, 182, 172);
    ellipse(-s * 0.35, -s * 0.25, s * 0.55, s * 0.3);
    ellipse(s * 0.25, -s * 0.3, s * 0.45, s * 0.25);
    drawingContext.shadowBlur = 0;
    drawingContext.shadowOffsetY = 0;
    pop();

    // 垂下的藤蔓根须 + 水滴
    let drops = 5;
    for (let i = 0; i < drops; i++) {
      let t = (i / (drops - 1)) - 0.5;
      let ox = t * s * 1.1;
      let len = s * 0.9 + sin(this.bobPhase * 2 + i) * 6;
      // 藤蔓线
      stroke(140, 125, 110, 160);
      strokeWeight(1.5);
      noFill();
      beginShape();
      for (let j = 0; j <= 8; j++) {
        let tt = j / 8;
        let vx = lerp(ox * 0.5, ox, tt) + sin(tt * PI * 2 + i) * 3;
        let vy = lerp(0, len, tt);
        curveVertex(vx, vy);
      }
      endShape();
      noStroke();
      // 水滴
      let pulse = 0.85 + 0.15 * sin(this.bobPhase * 3 + i * 1.2);
      push();
      translate(ox, len);
      drawPaperEllipse(s * 0.16 * pulse, s * 0.24 * pulse,
        130, 150, 168,   // base: 蓝灰
        168, 196, 216    // top: 浅蓝
      );
      // 高光
      noStroke();
      fill(255, 255, 255, 120);
      ellipse(-s * 0.04, -s * 0.06, s * 0.06, s * 0.1);
      pop();
    }
  }

  // --- 太阳：暖金色太阳 ---
  _drawSun() {
    let s = this.size;
    let rot = this.bobPhase * 0.15;

    // 光芒（从中心辐射的剪纸光芒）
    push();
    rotate(rot);
    drawingContext.shadowOffsetX = 0;
    drawingContext.shadowOffsetY = 3;
    drawingContext.shadowBlur = 8;
    drawingContext.shadowColor = PAPER_SHADOW;
    fill(255, 228, 161);
    stroke(200, 160, 80);
    strokeWeight(1.2);
    for (let i = 0; i < 12; i++) {
      let a = i * PI / 6;
      push();
      rotate(a);
      triangle(0, -s * 1.05, s * 0.1, -s * 0.55, -s * 0.1, -s * 0.55);
      pop();
    }
    drawingContext.shadowBlur = 0;
    drawingContext.shadowOffsetY = 0;
    pop();

    // 太阳本体
    drawPaperEllipse(s * 1.25, s * 1.25,
      255, 214, 130,   // base: 金黄
      255, 250, 220    // top: 暖白
    );
    // 中心高光
    noStroke();
    fill(255, 255, 240, 200);
    circle(0, -s * 0.08, s * 0.45);
    fill(255, 255, 255, 120);
    circle(-s * 0.1, -s * 0.15, s * 0.2);
  }

  // --- 野花丛：右下角茂密花丛 + 枝叶 ---
  _drawFlowers() {
    let s = this.size;
    // 底层叶子/草丛
    push();
    drawingContext.shadowOffsetX = 0;
    drawingContext.shadowOffsetY = 5;
    drawingContext.shadowBlur = 10;
    drawingContext.shadowColor = PAPER_SHADOW;
    fill(80, 110, 70);
    noStroke();
    for (let i = 0; i < 7; i++) {
      let a = i * TWO_PI / 7;
      let r = s * (0.5 + sin(i * 2.5) * 0.15);
      push();
      translate(cos(a) * r * 0.5, sin(a) * r * 0.25 + s * 0.1);
      rotate(a + 0.3);
      ellipse(0, 0, s * 0.5, s * 0.9);
      pop();
    }
    drawingContext.shadowBlur = 0;
    drawingContext.shadowOffsetY = 0;
    pop();

    // 上层亮叶
    fill(100, 135, 80);
    for (let i = 0; i < 5; i++) {
      let a = i * TWO_PI / 5 + 0.5;
      let r = s * 0.35;
      push();
      translate(cos(a) * r, sin(a) * r * 0.5);
      rotate(a);
      ellipse(0, 0, s * 0.4, s * 0.75);
      pop();
    }

    // 小花（多色，密集）
    let flowerColors = [
      [255, 200, 200], [255, 220, 170], [255, 190, 210],
      [255, 240, 230], [255, 180, 180], [255, 210, 150]
    ];
    for (let i = 0; i < 12; i++) {
      let a = i * TWO_PI / 12 + this.bobPhase * 0.1;
      let r = s * (0.25 + noise(i * 0.7) * 0.35);
      let fx = cos(a) * r;
      let fy = sin(a) * r * 0.5 - s * 0.05;
      let fs = s * 0.12 + noise(i * 1.3) * s * 0.06;
      let c = flowerColors[i % flowerColors.length];
      push();
      translate(fx, fy);
      rotate(a + this.bobPhase * 0.2);
      drawPaperLayered(fs, 5,
        Math.round(c[0] * 0.7), Math.round(c[1] * 0.7), Math.round(c[2] * 0.7),
        c[0], c[1], c[2],
        255, 255, 255
      );
      // 花蕊
      fill(255, 230, 140);
      circle(0, 0, fs * 0.25);
      pop();
    }
  }

  // --- 原石：暖灰棕多面体 ---
  _drawRawStone() {
    let s = this.size;
    let rot = this.bobPhase * 0.08;
    push();
    rotate(rot);
    drawPaperLayered(s, 6,
      110, 95, 82,      // base: 深暖灰
      170, 155, 135,    // top: 浅暖灰
      210, 195, 175     // highlight: 亮灰
    );
    // 折痕线
    stroke(80, 70, 60, 130);
    strokeWeight(0.8);
    line(0, -s * 0.7, 0, s * 0.7);
    line(-s * 0.6, 0, s * 0.6, 0);
    noStroke();
    pop();
  }

  // --- 发光水晶：粉白暖色水晶簇 ---
  _drawCrystal() {
    let s = this.size;
    let g = this.glow;
    let pulse = 0.7 + 0.3 * sin(this.bobPhase * 2);

    // 外层暖色光晕
    push();
    blendMode(ADD);
    noStroke();
    for (let i = 5; i > 0; i--) {
      fill(255, 200, 200, g * pulse * 22 / i);
      circle(0, 0, s + i * 14);
    }
    fill(255, 230, 210, g * pulse * 12);
    circle(0, 0, s * 2.3);
    blendMode(BLEND);
    pop();

    // 水晶簇（多个小水晶组合）
    let crystals = [
      { x: 0, y: 0, r: s * 0.75, n: 6, rot: 0 },
      { x: -s * 0.45, y: s * 0.25, r: s * 0.45, n: 5, rot: 0.4 },
      { x: s * 0.4, y: -s * 0.15, r: s * 0.5, n: 5, rot: -0.5 },
      { x: s * 0.1, y: -s * 0.45, r: s * 0.4, n: 6, rot: 0.2 },
    ];
    for (let c of crystals) {
      push();
      translate(c.x, c.y);
      rotate(c.rot + this.bobPhase * 0.1);
      drawPaperLayered(c.r, c.n,
        160, 100, 110,           // base: 深粉褐
        255, 205, 210,           // top: 粉白
        255, 245, 240            // highlight: 暖白
      );
      // 折痕线
      stroke(255, 255, 255, 80 + g * 80);
      strokeWeight(0.8);
      line(0, -c.r * 0.6, 0, c.r * 0.6);
      line(-c.r * 0.5, 0, c.r * 0.5, 0);
      noStroke();
      pop();
    }

    // 持续投射暖色光斑
    if (frameCount % 12 === 0 && !this.consumed) {
      TextureManager.spawnLightSpot(
        this.x + random(-20, 20),
        this.y + random(-20, 20),
        random(['#ffd1dc', '#f8c6c6', '#fff0e0']),
        random(12, 28)
      );
    }
  }

  // --- 折纸之心：中央粉白几何心形水晶 ---
  _drawHeart() {
    let s = this.size;
    let prog = STATE.heartActivationProgress;
    let pulse = 0.8 + 0.2 * sin(this.bobPhase * 0.5);

    // 核心暖色光晕
    push();
    blendMode(ADD);
    noStroke();
    for (let i = 8; i > 0; i--) {
      fill(255, 220, 210, prog * 15);
      circle(0, 0, s + i * 20);
    }
    fill(255, 200, 200, prog * 30 * pulse);
    circle(0, 0, s * 3);
    blendMode(BLEND);
    pop();

    if (prog < 0.3) {
      // 未激活：粉白几何心形
      this._drawHeartShape(s, pulse);
      // 中心亮点
      noStroke();
      fill(255, 255, 255, 180);
      circle(0, -s * 0.05, s * 0.25);
    } else {
      // 激活中/后：生命之树展开
      let unfold = EaseOutCubic(constrain((prog - 0.2) / 0.6, 0, 1));
      this._drawTree(s, unfold, pulse);
    }
  }

  _drawHeartShape(s, pulse) {
    // 用心形轮廓的多个切面组合
    let faces = [
      { x: 0, y: -s * 0.35, r: s * 0.55, n: 5, rot: 0 },
      { x: -s * 0.35, y: -s * 0.25, r: s * 0.42, n: 5, rot: -0.5 },
      { x: s * 0.35, y: -s * 0.25, r: s * 0.42, n: 5, rot: 0.5 },
      { x: 0, y: s * 0.25, r: s * 0.5, n: 6, rot: 0 },
    ];
    for (let f of faces) {
      push();
      translate(f.x, f.y);
      rotate(f.rot + this.bobPhase * 0.05);
      drawPaperLayered(f.r, f.n,
        180, 130, 145,    // base: 深粉
        255, 210, 220,    // top: 粉白
        255, 245, 240     // highlight: 暖白
      );
      pop();
    }
    // 中心强高光
    noStroke();
    fill(255, 255, 255, 150 * pulse);
    ellipse(0, -s * 0.15, s * 0.3, s * 0.5);
  }

  // --- 生命之树 ---
  _drawTree(s, unfold, pulse) {
    push();
    let trunkH = s * 1.5 * unfold;

    // 树干（剪纸风分层矩形）
    drawingContext.shadowOffsetX = 0;
    drawingContext.shadowOffsetY = 6;
    drawingContext.shadowBlur = 10;
    drawingContext.shadowColor = PAPER_SHADOW;
    fill(120, 85, 60);
    stroke(70, 50, 35);
    strokeWeight(1.5);
    rect(-s * 0.14, -s * 0.05, s * 0.28, trunkH + s * 0.05, 4);
    drawingContext.shadowBlur = 0;
    drawingContext.shadowOffsetY = 0;
    noStroke();
    fill(165, 120, 85);
    rect(-s * 0.10, 0, s * 0.12, trunkH, 3);
    stroke(90, 65, 45, 150);
    strokeWeight(0.8);
    line(0, 0, 0, trunkH);
    noStroke();

    // 树枝（层层展开）
    let layers = 4;
    for (let l = 0; l < layers; l++) {
      let lt = constrain((unfold - l * 0.15) / 0.25, 0, 1);
      if (lt <= 0) continue;
      let le = EaseOutBack(lt);
      let branchY = -trunkH * (0.3 + l * 0.18);
      let branchW = s * (0.8 + l * 0.4) * le;

      stroke(130, 95, 65, 200 * lt);
      strokeWeight(2 - l * 0.3);
      noFill();
      beginShape();
      for (let i = 0; i <= 8; i++) {
        let t = i / 8;
        let bx = lerp(-branchW * 0.3, branchW * (t - 0.5), t);
        let by = branchY + sin(t * PI) * s * 0.15 * le - l * s * 0.1;
        vertex(bx, by);
      }
      endShape();
      noStroke();

      // 叶片/花（暖粉、金、青）
      let leafCount = 5 + l;
      let leafColors = [
        [255, 200, 200], // 粉
        [255, 220, 170], // 金
        [255, 190, 210], // 浅粉
        [200, 230, 210], // 淡青
        [255, 240, 230], // 白
      ];
      for (let i = 0; i < leafCount; i++) {
        let a = (i / leafCount) * TWO_PI + l * 0.5 + this.bobPhase * 0.1;
        let r = branchW * 0.5 * (0.7 + sin(i * 1.7) * 0.2);
        let lx = cos(a) * r;
        let ly = branchY + sin(a) * r * 0.4 - l * s * 0.1;
        let ls = s * 0.22 * le * (0.8 + sin(i * 2.3) * 0.15);

        let cIdx = (i + l) % leafColors.length;
        let c = leafColors[cIdx];
        let br = Math.round(c[0] * 0.6);
        let bg = Math.round(c[1] * 0.6);
        let bb = Math.round(c[2] * 0.6);

        push();
        translate(lx, ly);
        rotate(a + this.bobPhase * 0.2);
        drawPaperLayered(ls, 5,
          br, bg, bb,
          c[0], c[1], c[2],
          255, 255, 255
        );
        pop();
      }
    }

    // 树顶光球
    if (unfold > 0.5) {
      let topGlow = EaseOutCubic((unfold - 0.5) * 2);
      push();
      blendMode(ADD);
      noStroke();
      for (let i = 5; i > 0; i--) {
        fill(255, 230, 200, topGlow * 40 / i);
        circle(0, -trunkH - s * 0.2, s * 0.3 + i * 8);
      }
      blendMode(BLEND);
      pop();
      fill(255, 245, 220, 220);
      circle(0, -trunkH - s * 0.2, s * 0.25 * pulse);
    }
    pop();
  }
}

// ===== 水晶洞窟场景 =====
class CrystalCavern {
  constructor() {
    this.elements = [];
    this.particles = [];
    this.draggedElement = null;
    this.synthCooldown = 0;
    this.heartElement = null;
    this.heartParticles = [];
    this.cameraShake = 0;
  }

  init() {
    this.elements = [];
    this.particles = [];
    this.heartElement = null;
    this.heartParticles = [];
    STATE.cavernLit = 0;
    STATE.heartActivated = false;
    STATE.heartActivationProgress = 0;
    STATE.cameraZoom = 1;
    STATE.cameraTargetZoom = 1;
    STATE.elementsPulse = 0;
    STATE.discoveredRecipes.clear();

    // 生成基础元素
    for (let def of BASE_ELEMENTS) {
      let el = new GameElement(def.type, def.x, def.y);
      el.targetScale = 1;
      this.elements.push(el);
    }

    // 生成洞窟中央的折纸之心（未激活状态）
    this.heartElement = new GameElement('heart', CONFIG.CANVAS_W / 2, 260);
    this.heartElement.size = 55;
    this.heartElement.targetScale = 0.85;
    this.elements.push(this.heartElement);

    EventBus.emit('cavern:ready', {});
  }

  update(dt) {
    this.synthCooldown = max(0, this.synthCooldown - dt);

    // 更新元素
    for (let el of this.elements) {
      el.update(dt);
    }

    // 移除已消耗的元素
    this.elements = this.elements.filter(e => !e.consumed);

    // 确保心元素在列表中
    if (this.heartElement && !this.heartElement.consumed) {
      if (!this.elements.includes(this.heartElement)) {
        this.elements.push(this.heartElement);
      }
    }

    // 洞窟亮度渐变
    let targetLit = STATE.discoveredRecipes.size / 3 * 0.8;
    if (STATE.heartActivated) targetLit = 1;
    STATE.cavernLit += (targetLit - STATE.cavernLit) * min(1, dt * 2);

    // 心觉醒进度
    if (STATE.heartActivated) {
      STATE.heartActivationProgress = min(1, STATE.heartActivationProgress + dt * 0.25);
      STATE.cameraTargetZoom = 0.7; // 镜头拉远
      STATE.elementsPulse = min(1, STATE.elementsPulse + dt * 0.5);
    }
    STATE.cameraZoom += (STATE.cameraTargetZoom - STATE.cameraZoom) * min(1, dt * 1.5);

    // 更新粒子
    for (let i = this.particles.length - 1; i >= 0; i--) {
      let p = this.particles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += 80 * dt;
      p.vx *= 0.98;
      p.life -= dt * 1.5;
      p.rotation += p.rotSpeed * dt;
      if (p.life <= 0) this.particles.splice(i, 1);
    }

    // 心觉醒粒子
    for (let i = this.heartParticles.length - 1; i >= 0; i--) {
      let p = this.heartParticles[i];
      p.x += p.vx * dt;
      p.y += p.vy * dt;
      p.vy += 30 * dt;
      p.vx *= 0.95;
      p.vy *= 0.95;
      p.life -= dt * 0.3;
      p.rotation += p.rotSpeed * dt;
      if (p.life <= 0) this.heartParticles.splice(i, 1);
    }

    // 相机抖动衰减
    this.cameraShake = max(0, this.cameraShake - dt * 4);

    // 全局元素律动
    if (STATE.elementsPulse > 0) {
      for (let el of this.elements) {
        el.targetScale = 1 + sin(frameCount * 0.05 + el.bobPhase) * 0.1 * STATE.elementsPulse;
      }
    }
  }

  draw() {
    push();

    // 相机变换
    let shakeX = (random() - 0.5) * this.cameraShake * 10;
    let shakeY = (random() - 0.5) * this.cameraShake * 10;
    translate(CONFIG.CANVAS_W / 2, CONFIG.CANVAS_H / 2);
    scale(STATE.cameraZoom);
    translate(-CONFIG.CANVAS_W / 2 + shakeX, -CONFIG.CANVAS_H / 2 + shakeY);

    // 洞窟背景
    TextureManager.drawCavernBackground(STATE.cavernLit);

    // 几何光斑
    TextureManager.drawLightSpots();

    // 元素（按 y 排序）
    let sorted = [...this.elements].sort((a, b) => a.y - b.y);
    for (let el of sorted) {
      try {
        el.draw();
      } catch(e) {
        push();
        translate(el.x, el.y);
        fill(255, 100, 100);
        noStroke();
        circle(0, 0, 20);
        fill(255);
        textSize(10);
        textAlign(CENTER, CENTER);
        text(el.type, 0, 0);
        pop();
      }
    }

    // 粒子
    noStroke();
    for (let p of this.particles) {
      let rgb = hexToRgb(p.color);
      fill(rgb.r, rgb.g, rgb.b, p.life * 200);
      push();
      translate(p.x, p.y);
      rotate(p.rotation);
      triangle(0, -p.size, p.size * 0.87, p.size * 0.5, -p.size * 0.87, p.size * 0.5);
      pop();
    }

    // 心觉醒粒子
    push();
    blendMode(ADD);
    noStroke();
    for (let p of this.heartParticles) {
      let rgb = hexToRgb(p.color);
      fill(rgb.r, rgb.g, rgb.b, p.life * 150);
      push();
      translate(p.x, p.y);
      rotate(p.rotation);
      let sz = p.size * p.life;
      beginShape();
      for (let i = 0; i < 6; i++) {
        let a = i * PI / 3;
        vertex(cos(a) * sz, sin(a) * sz);
      }
      endShape(CLOSE);
      pop();
    }
    blendMode(BLEND);
    pop();

    pop();
  }

  // ===== 交互 =====
  handlePress(x, y) {
    if (STATE.heartActivated) return false;

    // 从后往前检测（顶层优先）
    for (let i = this.elements.length - 1; i >= 0; i--) {
      let el = this.elements[i];
      if (el.consumed) continue;
      if (el.type === 'heart') continue; // 心不能直接拖
      if (el.contains(x, y)) {
        this.draggedElement = el;
        el.dragging = true;
        el.dragOffX = x - el.x;
        el.dragOffY = y - el.y;
        AudioManager.pick();
        return true;
      }
    }
    return false;
  }

  handleDrag(x, y) {
    // 拖动时由元素自身的 update 处理位置
  }

  handleRelease() {
    if (!this.draggedElement) return;
    let el = this.draggedElement;
    el.dragging = false;

    // 检测是否与其他元素重叠 → 尝试合成
    if (this.synthCooldown <= 0) {
      for (let other of this.elements) {
        if (other === el || other.consumed) continue;
        if (other.type === 'heart') continue;
        if (el.overlaps(other)) {
          this._trySynthesize(el, other);
          break;
        }
      }
    }

    this.draggedElement = null;
  }

  // ===== 合成 =====
  _trySynthesize(elA, elB) {
    let recipe = findRecipe(elA.type, elB.type);
    if (!recipe) {
      AudioManager.fail();
      notify('这两个元素无法合成…', '#888');
      this.synthCooldown = 0.5;
      return;
    }

    // 消耗两个元素
    elA.consumed = true;
    elB.consumed = true;

    // 合成位置（两元素中点）
    let mx = (elA.x + elB.x) / 2;
    let my = (elA.y + elB.y) / 2;

    // 生成合成粒子
    this._spawnSynthParticles(mx, my, recipe);

    // 如果产出是折纸之心 → 激活心
    if (recipe.output === 'heart') {
      this._activateHeart();
    } else {
      // 生成新元素
      let newEl = new GameElement(recipe.output, mx, my);
      newEl.targetScale = 0;
      setTimeout(() => { newEl.targetScale = 1; }, 100);
      this.elements.push(newEl);

      // 记录发现
      STATE.discoveredRecipes.add(recipe.output);
      AudioManager.synthSuccess();

      notify('✦ 合成：' + recipe.name + '！', ELEMENT_INFO[recipe.output].color);

      // 特殊效果
      if (recipe.output === 'raw_stone') {
        AudioManager.rainDrop();
      } else if (recipe.output === 'crystal') {
        AudioManager.crystalChime();
        this.cameraShake = 0.3;
      }
    }

    this.synthCooldown = 0.8;
  }

  _spawnSynthParticles(x, y, recipe) {
    let color = ELEMENT_INFO[recipe.output].color;
    for (let i = 0; i < 20; i++) {
      let a = random(TWO_PI);
      let sp = random(80, 200);
      this.particles.push({
        x: x, y: y,
        vx: cos(a) * sp, vy: sin(a) * sp - 50,
        size: random(3, 7),
        rotation: random(TWO_PI),
        rotSpeed: random(-5, 5),
        life: 1.0,
        color: color,
      });
    }
  }

  // ===== 折纸之心觉醒 =====
  _activateHeart() {
    STATE.heartActivated = true;
    STATE.discoveredRecipes.add('heart');
    AudioManager.heartAwaken();
    this.cameraShake = 1.5;

    notify('✦✦ 折纸之心已激活！世界正在恢复生机…', '#FFFFFF');

    // 大量觉醒粒子
    for (let i = 0; i < 80; i++) {
      let a = random(TWO_PI);
      let sp = random(50, 200);
      this.heartParticles.push({
        x: CONFIG.CANVAS_W / 2,
        y: 260,
        vx: cos(a) * sp,
        vy: sin(a) * sp - 30,
        size: random(4, 10),
        rotation: random(TWO_PI),
        rotSpeed: random(-3, 3),
        life: 1.0,
        color: random(['#ffd1dc', '#f8c6c6', '#ffe4a1', '#f2a6a6', '#FFFFFF']),
      });
    }

    // 持续投射光斑
    for (let i = 0; i < 20; i++) {
      TextureManager.spawnLightSpot(
        CONFIG.CANVAS_W / 2 + random(-100, 100),
        random(50, 400),
        random(['#ffd1dc', '#f8c6c6', '#FFFFFF']),
        random(20, 40)
      );
    }

    EventBus.emit('heart:activated', {});
  }

  // ===== 重置 =====
  reset() {
    this.init();
    notify('洞窟已重置', CONFIG.PALETTE.accent);
  }

  getProgress() {
    return {
      found: STATE.discoveredRecipes.size,
      total: RECIPES.length,
    };
  }
}
