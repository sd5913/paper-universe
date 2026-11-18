/* ============================================
   sketch.js — 场景三主控制器
   p5 生命周期 + UI + 交互路由
   ============================================ */

let cavern;
let setupError = null;
let debugMode = false;
let bgImage = null;

function preload() {
  // 预加载背景图（用于替代程序生成的洞窟背景）
  try {
    bgImage = loadImage('assets/background.jpg?v=3',
      () => console.log('Background image loaded'),
      () => console.warn('Background image failed to load')
    );
  } catch(e) {
    console.warn('preload image error:', e);
  }
}

function setup() {
  try {
    let c = createCanvas(CONFIG.CANVAS_W, CONFIG.CANVAS_H);
    c.parent('app');
    textFont('Georgia');

    // 先初始化场景（核心逻辑，不能失败）
    cavern = new CrystalCavern();
    cavern.init();

    // 再初始化可选的视听模块（允许失败）
    try { AudioManager.init(); } catch(e) { console.log('Audio init skipped:', e.message); }
    try {
      TextureManager.init();
      if (bgImage && bgImage.width > 0) {
        TextureManager.setBackgroundImage(bgImage);
      }
    } catch(e) { console.log('Texture init skipped:', e.message); }

    // 首次提示
    setTimeout(function() {
      try {
        notify('✦ 水晶洞窟 — 拖拽元素进行合成', CONFIG.PALETTE.accent);
        setTimeout(function() {
          notify('提示：岩石 + 春雨 = 原石', CONFIG.PALETTE.accentWarm);
        }, 2000);
      } catch(e) {}
    }, 500);

  } catch(e) {
    setupError = e;
    console.error('Setup failed:', e);
    // 尝试创建画布（如果还没创建的话）
    try {
      if (!cavern) {
        let c = createCanvas(CONFIG.CANVAS_W, CONFIG.CANVAS_H);
        c.parent('app');
      }
    } catch(e2) {
      console.error('Even canvas creation failed:', e2);
    }
  }
}

function draw() {
  let dt = min(deltaTime / 1000, 0.05);

  // 如果 setup 失败，显示错误
  if (setupError) {
    background(26, 18, 14);
    fill(255, 100, 100);
    textSize(16);
    textAlign(LEFT, TOP);
    textStyle(BOLD);
    text('SETUP ERROR:', 20, 50);
    textStyle(NORMAL);
    fill(255);
    textSize(13);
    text(setupError.message, 20, 80, CONFIG.CANVAS_W - 40);
    if (setupError.stack) {
      fill(180);
      textSize(11);
      text(setupError.stack, 20, 120, CONFIG.CANVAS_W - 40);
    }
    return;
  }

  // 如果 cavern 没初始化成功
  if (!cavern) {
    background(26, 18, 14);
    fill(255);
    textSize(16);
    textAlign(CENTER, CENTER);
    text('Loading...', CONFIG.CANVAS_W / 2, CONFIG.CANVAS_H / 2);
    return;
  }

  // 更新
  try {
    cavern.update(dt);
  } catch(e) {
    console.error('Update error:', e);
  }

  try {
    TextureManager.updateLightSpots(dt);
  } catch(e) {}

  // 绘制
  try {
    background(CONFIG.PALETTE.cavernDeep); // 安全清屏，防止重影
    cavern.draw();
  } catch(e) {
    console.error('Draw error:', e);
    background(26, 18, 14);
    fill(255, 100, 100);
    textSize(14);
    textAlign(LEFT, TOP);
    text('DRAW ERROR: ' + e.message, 20, 50);
  }

  // UI 层
  try { _drawTopBar(); } catch(e) {}
  try { _drawNotifications(dt); } catch(e) {}
  if (STATE.showHelp) { try { _drawHelp(); } catch(e) {} }
  if (STATE.showRecipes) { try { _drawRecipeBook(); } catch(e) {} }

  // 调试信息（按 D 切换）
  if (debugMode) { try { _drawDebug(); } catch(e) {} }
}

// ===== 调试面板 =====
function _drawDebug() {
  noStroke();
  fill(0, 0, 0, 180);
  rect(0, CONFIG.CANVAS_H - 80, CONFIG.CANVAS_W, 80);

  fill(0, 255, 100);
  textSize(12);
  textAlign(LEFT, TOP);
  textStyle(BOLD);
  text('DEBUG (D to toggle)', 10, CONFIG.CANVAS_H - 75);
  textStyle(NORMAL);

  let info = [
    'elements: ' + cavern.elements.length,
    'cavernLit: ' + STATE.cavernLit.toFixed(2),
    'heartActivated: ' + STATE.heartActivated,
    'recipes found: ' + STATE.discoveredRecipes.size + '/' + RECIPES.length,
    'cameraZoom: ' + STATE.cameraZoom.toFixed(2),
    'paperBuffer: ' + !!TextureManager.paperBuffer,
    'sparkBuffer: ' + !!TextureManager.sparkBuffer,
    'audioEnabled: ' + AudioManager.enabled,
  ];

  fill(200, 255, 200);
  textSize(11);
  for (let i = 0; i < info.length; i++) {
    text(info[i], 10 + (i % 4) * 220, CONFIG.CANVAS_H - 55 + floor(i / 4) * 16);
  }

  // 元素详情
  for (let i = 0; i < cavern.elements.length && i < 8; i++) {
    let el = cavern.elements[i];
    text(el.type + ':s=' + el.scale.toFixed(2) + ' x=' + el.x.toFixed(0) + ' y=' + el.y.toFixed(0),
         10 + i * 200, CONFIG.CANVAS_H - 20);
  }
}

// ===== 顶栏 =====
function _drawTopBar() {
  noStroke();
  fill(0, 0, 0, 100);
  rect(0, 0, CONFIG.CANVAS_W, 36);

  fill(CONFIG.PALETTE.paper);
  textSize(14);
  textAlign(LEFT, CENTER);
  textStyle(BOLD);
  text('✦ 折光之森 — 水晶洞窟', 14, 18);
  textStyle(NORMAL);

  let prog = cavern.getProgress();
  textAlign(RIGHT, CENTER);
  textSize(11);
  text('配方 ' + prog.found + '/' + prog.total + '  |  H 帮助  B 配方  R 重置  D 调试', CONFIG.CANVAS_W - 14, 18);

  // 亮度指示器
  let litW = 80;
  let litX = CONFIG.CANVAS_W / 2 - litW / 2;
  fill(40, 40, 60, 150);
  rect(litX, 14, litW, 6, 3);
  let litColor = lerpHex(CONFIG.PALETTE.cavernDeep, CONFIG.PALETTE.crystalGlow, STATE.cavernLit);
  fill(litColor);
  rect(litX, 14, litW * STATE.cavernLit, 6, 3);
}

// ===== 通知 =====
function _drawNotifications(dt) {
  let ny = 52;
  for (let i = STATE.notifications.length - 1; i >= 0; i--) {
    let n = STATE.notifications[i];
    n.life -= dt;
    if (n.life <= 0) {
      STATE.notifications.splice(i, 1);
      continue;
    }
    let alpha = min(1, n.life / 0.5) * 255;
    noStroke();
    fill(0, 0, 0, alpha * 0.15);
    rect(CONFIG.CANVAS_W / 2 - 180, ny - 4, 360, 30, 6);
    fill(n.color);
    textSize(14);
    textAlign(CENTER, CENTER);
    textStyle(BOLD);
    text(n.text, CONFIG.CANVAS_W / 2, ny + 11);
    textStyle(NORMAL);
    ny += 36;
  }
}

// ===== 帮助面板 =====
function _drawHelp() {
  noStroke();
  fill(0, 0, 0, 160);
  rect(0, 0, CONFIG.CANVAS_W, CONFIG.CANVAS_H);

  let pw = 440, ph = 420;
  let px = (CONFIG.CANVAS_W - pw) / 2, py = (CONFIG.CANVAS_H - ph) / 2;

  fill(CONFIG.PALETTE.paper);
  rect(px, py, pw, ph, 14);
  noFill();
  stroke(CONFIG.PALETTE.accent);
  strokeWeight(2);
  rect(px, py, pw, ph, 14);
  noStroke();

  fill(CONFIG.PALETTE.ink);
  textSize(20);
  textAlign(CENTER, TOP);
  textStyle(BOLD);
  text('✦ 水晶洞窟 — 操作指南', px + pw / 2, py + 18);
  textStyle(NORMAL);

  let lines = [
    ['拖拽元素', '按住元素拖动到另一个元素上'],
    ['岩石 + 春雨', '→ 原石（多面体矿石生长）'],
    ['原石 + 太阳', '→ 发光水晶（粉白色光晕）'],
    ['发光水晶 + 野花丛', '→ 折纸之心（生命之树）'],
    ['', ''],
    ['洞窟亮度', '每完成一个合成，洞窟逐渐变亮'],
    ['水晶光斑', '水晶会向墙壁投射几何光斑'],
    ['折纸之心', '完成全部3个配方后激活终极动画'],
    ['', ''],
    ['H 键', '打开/关闭此帮助'],
    ['B 键', '打开/关闭配方图鉴'],
    ['R 键', '重置洞窟'],
    ['D 键', '调试信息'],
  ];

  textSize(12);
  textAlign(LEFT, TOP);
  for (let i = 0; i < lines.length; i++) {
    let ly = py + 54 + i * 28;
    if (lines[i][0] === '') continue;
    fill(CONFIG.PALETTE.accent);
    textStyle(BOLD);
    text(lines[i][0], px + 30, ly);
    fill(CONFIG.PALETTE.inkSoft);
    textStyle(NORMAL);
    text(lines[i][1], px + 200, ly);
  }

  fill(CONFIG.PALETTE.inkSoft);
  textSize(11);
  textAlign(CENTER, BOTTOM);
  text('按 H 关闭', px + pw / 2, py + ph - 10);
}

// ===== 配方图鉴 =====
function _drawRecipeBook() {
  noStroke();
  fill(0, 0, 0, 160);
  rect(0, 0, CONFIG.CANVAS_W, CONFIG.CANVAS_H);

  let pw = 480, ph = 400;
  let px = (CONFIG.CANVAS_W - pw) / 2, py = (CONFIG.CANVAS_H - ph) / 2;

  fill(CONFIG.PALETTE.paper);
  rect(px, py, pw, ph, 14);
  noFill();
  stroke(CONFIG.PALETTE.accentWarm);
  strokeWeight(2);
  rect(px, py, pw, ph, 14);
  noStroke();

  fill(CONFIG.PALETTE.ink);
  textSize(20);
  textAlign(CENTER, TOP);
  textStyle(BOLD);
  text('✦ 配方图鉴', px + pw / 2, py + 18);
  textStyle(NORMAL);

  for (let i = 0; i < RECIPES.length; i++) {
    let r = RECIPES[i];
    let ry = py + 60 + i * 100;
    let discovered = STATE.discoveredRecipes.has(r.output);

    if (discovered) {
      // 配方名称
      fill(r.tier === 1 ? 157 : r.tier === 2 ? 199 : 255, r.tier === 1 ? 157 : r.tier === 2 ? 125 : 255, r.tier === 1 ? 176 : r.tier === 2 ? 255 : 255);
      textSize(15);
      textAlign(LEFT, TOP);
      textStyle(BOLD);
      text(r.name + ' (' + r.nameEn + ')', px + 30, ry);
      textStyle(NORMAL);

      // 配方内容
      let inA = ELEMENT_INFO[r.inputs[0]].name;
      let inB = ELEMENT_INFO[r.inputs[1]].name;
      fill(CONFIG.PALETTE.ink);
      textSize(13);
      text(inA + ' + ' + inB + ' → ' + r.name, px + 30, ry + 24);

      // 描述
      fill(CONFIG.PALETTE.inkSoft);
      textSize(11);
      text(r.desc, px + 30, ry + 44, pw - 60);
    } else {
      // 未发现
      fill(180, 180, 180);
      textSize(15);
      textAlign(LEFT, TOP);
      textStyle(BOLD);
      text('??? — 未发现', px + 30, ry);
      textStyle(NORMAL);
      fill(200, 200, 200);
      textSize(12);
      text('继续探索洞窟，尝试不同的元素组合…', px + 30, ry + 24);
    }

    // 分隔线
    if (i < RECIPES.length - 1) {
      stroke(200, 200, 200);
      strokeWeight(0.5);
      line(px + 30, ry + 80, px + pw - 30, ry + 80);
      noStroke();
    }
  }

  fill(CONFIG.PALETTE.inkSoft);
  textSize(11);
  textAlign(CENTER, BOTTOM);
  text('按 B 关闭', px + pw / 2, py + ph - 10);
}

// ===== p5 交互 =====
function mousePressed() {
  try { AudioManager.resume(); } catch(e) {}

  if (STATE.showHelp) { STATE.showHelp = false; return; }
  if (STATE.showRecipes) { STATE.showRecipes = false; return; }

  if (cavern) cavern.handlePress(mouseX, mouseY);
}

function mouseDragged() {
  if (cavern) cavern.handleDrag(mouseX, mouseY);
}

function mouseReleased() {
  if (cavern) cavern.handleRelease();
}

function keyPressed() {
  if (key === 'h' || key === 'H') STATE.showHelp = !STATE.showHelp;
  if (key === 'b' || key === 'B') STATE.showRecipes = !STATE.showRecipes;
  if (key === 'd' || key === 'D') debugMode = !debugMode;
  if (key === 'r' || key === 'R') {
    if (cavern) {
      cavern.reset();
      try { AudioManager.init(); } catch(e) {}
      try { TextureManager.init(); } catch(e) {}
    }
  }
}
