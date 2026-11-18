/* ============================================
   config.js — 折光之森 共享约定
   场景三：水晶洞窟 (The Crystal Cavern)
   成员 D：场景三与全局视听
   ============================================ */

// --- 画布常量 ---
const CONFIG = {
  CANVAS_W: 900,
  CANVAS_H: 600,

  // 调色板 — 暖棕/卡其色剪纸洞窟（参照目标图）
  PALETTE: {
    // 洞窟背景（深邃暖棕星空卡纸）
    cavernDeep:    '#1a120e',
    cavernDark:    '#2a1e18',
    cavernMid:     '#3d2d24',
    cavernLight:   '#4f3a2f',
    cavernWall:    '#2d211a',
    cavernWallLit: '#4a372b',
    // 洞窟剪纸层次
    paperShadow:   '#0d0907',
    paperEdge:     '#5c4235',
    paperHi:       '#7a5a4a',
    // 水晶色系（暖粉/桃白金属光泽，图中水晶呈粉白发光）
    crystalCore:   '#f9e4d8',
    crystalGlow:   '#f8c6c6',
    crystalLight:  '#ffd1dc',
    crystalHi:     '#fff8f5',
    crystalDeep:   '#b87b8a',
    // 元素色
    rock:          '#a68b6a',
    rockDark:      '#7a6350',
    rockLight:     '#c4b090',
    rainCloud:     '#a09890',
    rainDrop:      '#a8c4d4',
    sun:           '#ffe4a1',
    sunGlow:       '#fff4d6',
    sunDeep:       '#f5c26b',
    flowers:       '#f2a6a6',
    flowersAlt:    '#f5c58c',
    flowersPink:   '#f8c8d8',
    flowersWhite:  '#fff8f0',
    // 纸 & UI
    paper:         '#FDFBF5',
    paperShadow:   '#E8E0D0',
    ink:           '#3D3833',
    inkSoft:       '#7A7268',
    accent:        '#f8c6c6',
    accentWarm:    '#f5c58c',
    starWhite:     '#E8E8F8',
  },

  // 洞窟墙壁区域
  WALL_LEFT:  0,
  WALL_RIGHT: 900,
  WALL_TOP:   0,
  CAVERN_FLOOR: 520,
};

// --- 共享状态 ---
const STATE = {
  notifications: [],
  showHelp: false,
  showRecipes: false,
  discoveredRecipes: new Set(),
  cavernLit: 0,        // 0=漆黑, 1=完全点亮
  heartActivated: false,
  heartActivationProgress: 0, // 0~1
  cameraZoom: 1,       // 镜头缩放（折纸之心激活时拉远）
  cameraTargetZoom: 1,
  elementsPulse: 0,    // 全局元素律动（结局时）
};

// --- 事件总线 ---
const EventBus = {
  _events: {},
  on(e, cb) { (this._events[e] = this._events[e] || []).push(cb); },
  emit(e, d) { (this._events[e] || []).forEach(cb => cb(d)); },
  clear() { this._events = {}; },
};

// --- 通知 ---
function notify(text, color) {
  STATE.notifications.push({
    text: text,
    life: 3.0,
    maxLife: 3.0,
    color: color || CONFIG.PALETTE.accent,
  });
}

// --- 合成配方表 (Recipe JSON) ---
// 场景三的三步递进合成链
const RECIPES = [
  {
    inputs: ['rock', 'rain'],
    output: 'raw_stone',
    name: '原石',
    nameEn: 'Raw Stone',
    desc: '洞窟墙壁上生长出立体的多面体折纸矿石',
    tier: 1,
  },
  {
    inputs: ['raw_stone', 'sun'],
    output: 'crystal',
    name: '发光水晶',
    nameEn: 'Luminous Crystal',
    desc: '太阳的光芒被折进多面体内部，水晶散发温暖的粉白色光晕',
    tier: 2,
  },
  {
    inputs: ['crystal', 'flowers'],
    output: 'heart',
    name: '折纸之心',
    nameEn: 'The Origami Heart',
    desc: '洞窟中央巨大的白色折纸核心被激活，化作生命之树',
    tier: 3,
  },
];

// --- 基础元素（场景三可用） ---
// 按目标图布局：岩石在左下角、春雨云在上方垂下、太阳在右上窗框、野花丛在右下
const BASE_ELEMENTS = [
  { type: 'rock',     name: '岩石',   x: 135, y: 500, color: '#a68b6a' },
  { type: 'rain',     name: '春雨',   x: 265, y: 150, color: '#a8c4d4' },
  { type: 'sun',      name: '太阳',   x: 725, y: 185, color: '#ffe4a1' },
  { type: 'flowers',  name: '野花丛', x: 765, y: 500, color: '#f2a6a6' },
];

// --- 元素描述（用于绘制和提示） ---
const ELEMENT_INFO = {
  rock:       { name: '岩石',   nameEn: 'Rock',          tier: 0, color: '#a68b6a' },
  rain:       { name: '春雨',   nameEn: 'Spring Rain',   tier: 0, color: '#a8c4d4' },
  sun:        { name: '太阳',   nameEn: 'Sun',           tier: 0, color: '#ffe4a1' },
  flowers:    { name: '野花丛', nameEn: 'Wildflowers',   tier: 0, color: '#f2a6a6' },
  raw_stone:  { name: '原石',   nameEn: 'Raw Stone',     tier: 1, color: '#c4b090' },
  crystal:    { name: '发光水晶', nameEn: 'Luminous Crystal', tier: 2, color: '#f8c6c6' },
  heart:      { name: '折纸之心', nameEn: 'Origami Heart',  tier: 3, color: '#ffd1dc' },
};

// --- 辅助函数 ---
function lerpHex(a, b, t) {
  let ca = color(a), cb = color(b);
  return lerpColor(ca, cb, t);
}

function hexToRgb(hex) {
  if (!hex || typeof hex !== 'string') return { r: 255, g: 255, b: 255 };
  let c = color(hex);
  return { r: red(c), g: green(c), b: blue(c) };
}

// 查找合成配方
function findRecipe(typeA, typeB) {
  for (let r of RECIPES) {
    if (r.inputs.includes(typeA) && r.inputs.includes(typeB) && typeA !== typeB) {
      return r;
    }
    if (r.inputs[0] === typeA && r.inputs[1] === typeB) return r;
    if (r.inputs[0] === typeB && r.inputs[1] === typeA) return r;
  }
  return null;
}
