/* ============================================
   audio.js — 全局视听：Web Audio 音效合成
   成员 D 负责模块
   ============================================
   使用 Web Audio API 合成音效，无需外部音频文件。
   模拟：纸张翻折声、风铃声、水晶共鸣、雨滴、发现提示、觉醒。
   ============================================ */

const AudioManager = {
  ctx: null,
  masterGain: null,
  enabled: true,

  init() {
    try {
      this.ctx = new (window.AudioContext || window.webkitAudioContext)();
      this.masterGain = this.ctx.createGain();
      this.masterGain.gain.value = 0.3;
      this.masterGain.connect(this.ctx.destination);
    } catch (e) {
      this.enabled = false;
    }
  },

  resume() {
    if (this.ctx && this.ctx.state === 'suspended') {
      this.ctx.resume();
    }
  },

  // --- 基础振荡器音 ---
  _tone(freq, duration, type, vol, attack, decay) {
    if (!this.enabled || !this.ctx) return;
    type = type || 'sine';
    vol = vol || 0.3;
    attack = attack || 0.01;
    decay = decay || duration;

    let osc = this.ctx.createOscillator();
    let gain = this.ctx.createGain();
    osc.type = type;
    osc.frequency.value = freq;

    let now = this.ctx.currentTime;
    gain.gain.setValueAtTime(0, now);
    gain.gain.linearRampToValueAtTime(vol, now + attack);
    gain.gain.exponentialRampToValueAtTime(0.001, now + decay);

    osc.connect(gain);
    gain.connect(this.masterGain);
    osc.start(now);
    osc.stop(now + decay + 0.1);
  },

  // --- 噪声脉冲（用于纸张声） ---
  _noise(duration, vol, filterFreq) {
    if (!this.enabled || !this.ctx) return;
    vol = vol || 0.15;
    filterFreq = filterFreq || 2000;

    let bufSize = this.ctx.sampleRate * duration;
    let buf = this.ctx.createBuffer(1, bufSize, this.ctx.sampleRate);
    let data = buf.getChannelData(0);
    for (let i = 0; i < bufSize; i++) {
      data[i] = (Math.random() * 2 - 1) * (1 - i / bufSize);
    }

    let src = this.ctx.createBufferSource();
    src.buffer = buf;

    let filter = this.ctx.createBiquadFilter();
    filter.type = 'lowpass';
    filter.frequency.value = filterFreq;

    let gain = this.ctx.createGain();
    gain.gain.value = vol;

    src.connect(filter);
    filter.connect(gain);
    gain.connect(this.masterGain);
    src.start();
  },

  // ===== 具体音效 =====

  // 纸张翻折声 — 短促的低频噪声
  paperFold() {
    this._noise(0.12, 0.08, 800);
    this._tone(180, 0.08, 'triangle', 0.06, 0.005, 0.08);
  },

  // 水晶共鸣 — 高频泛音，长衰减
  crystalChime() {
    this._tone(880, 1.2, 'sine', 0.12, 0.01, 1.2);
    this._tone(1320, 1.0, 'sine', 0.08, 0.02, 1.0);
    this._tone(1760, 0.8, 'sine', 0.05, 0.03, 0.8);
  },

  // 雨滴 — 短促的高频正弦
  rainDrop() {
    this._tone(1200 + Math.random() * 400, 0.1, 'sine', 0.08, 0.001, 0.1);
  },

  // 太阳/光源 — 温暖的中频
  sunGlow() {
    this._tone(523, 0.4, 'sine', 0.1, 0.05, 0.4);
    this._tone(784, 0.3, 'sine', 0.06, 0.08, 0.3);
  },

  // 发现提示 — 上升琶音
  discover() {
    let notes = [523, 659, 784, 1047];
    for (let i = 0; i < notes.length; i++) {
      setTimeout(() => this._tone(notes[i], 0.3, 'sine', 0.12, 0.01, 0.3), i * 80);
    }
  },

  // 合成成功 — 和弦
  synthSuccess() {
    this._tone(523, 0.5, 'sine', 0.1, 0.01, 0.5);
    this._tone(659, 0.5, 'sine', 0.08, 0.02, 0.5);
    this._tone(784, 0.5, 'sine', 0.06, 0.03, 0.5);
    this.crystalChime();
  },

  // 拖拽拾起 — 轻柔拨弦
  pick() {
    this._tone(440, 0.1, 'triangle', 0.06, 0.001, 0.1);
  },

  // 无效合成 — 低沉提示
  fail() {
    this._tone(200, 0.2, 'sawtooth', 0.06, 0.01, 0.2);
  },

  // 折纸之心觉醒 — 渐强和弦序列
  heartAwaken() {
    if (!this.enabled || !this.ctx) return;
    let chords = [
      { freqs: [261, 329, 392], time: 0 },
      { freqs: [294, 370, 440], time: 800 },
      { freqs: [330, 415, 494], time: 1600 },
      { freqs: [392, 494, 587], time: 2400 },
      { freqs: [523, 659, 784], time: 3200 },
    ];
    for (let chord of chords) {
      setTimeout(() => {
        for (let f of chord.freqs) {
          this._tone(f, 2.0, 'sine', 0.08, 0.5, 2.0);
        }
      }, chord.time);
    }
    // 最终的高频亮音
    setTimeout(() => {
      this._tone(2093, 3.0, 'sine', 0.1, 0.5, 3.0);
      this._tone(2637, 2.5, 'sine', 0.06, 0.8, 2.5);
    }, 4000);
  },
};
