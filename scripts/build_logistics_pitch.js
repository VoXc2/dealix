/**
 * Dealix Logistics Pitch Deck — Arabic RTL
 * Target: Major Saudi logistics company (Bahri / Almajdouie / SMSA / Saudia Cargo / Napco class)
 */

const pptxgen = require('pptxgenjs');
const path = require('path');
const fs = require('fs');

const OUT = '/home/user/workspace/dealix-clean/assets/Dealix_Logistics_Pitch_AR.pptx';
const SCREENSHOTS = '/home/user/workspace/dealix-clean/dashboard/assets';

// ===== Palette =====
const C = {
  navy: '0A1628',
  navyDeep: '060E1A',
  navySoft: '13233F',
  gold: 'D4A574',
  goldDeep: 'B8874C',
  cream: 'FAF8F3',
  creamAlt: 'F2EEE4',
  text: '1A1A1A',
  textMuted: '55606E',
  textFaint: '8B95A3',
  onDark: 'F5F5F5',
  onDarkMuted: 'B9C2CD',
  line: 'D4D1CA',
  lineSoft: 'E8E3D6',
  success: '2F7A3D',
  danger: 'A12C4A',
};

const FH = 'Calibri'; // headings
const FB = 'Calibri'; // body
const FS = 'Georgia'; // emphasis / serif

// ===== Setup =====
const pres = new pptxgen();
pres.layout = 'LAYOUT_WIDE'; // 13.333 x 7.5
pres.title = 'Dealix — Logistics Pitch AR';
pres.author = 'Dealix';
pres.rtlMode = true;

const W = 13.333;
const H = 7.5;

// ===== Helpers =====
const rtl = { align: 'right', rtlMode: true };
const ltr = { align: 'left' };

function ar(text, opts = {}) {
  return { text, options: { fontFace: FB, rtlMode: true, align: 'right', ...opts } };
}

function lightBg(slide) {
  slide.background = { color: C.cream };
}

function darkBg(slide) {
  slide.background = { color: C.navy };
}

// Page frame for light slides: section marker top-right, page number bottom-left
function lightFrame(slide, sectionLabel, pageNum) {
  // Gold section marker (top-right)
  slide.addShape('rect', { x: W - 0.5, y: 0.35, w: 0.08, h: 0.45, fill: { color: C.gold }, line: { type: 'none' } });
  slide.addText(sectionLabel, {
    x: W - 4.5, y: 0.3, w: 3.9, h: 0.4,
    fontFace: FH, fontSize: 12, color: C.textMuted, bold: true,
    align: 'right', rtlMode: true,
  });
  // Brand bottom-left
  slide.addText('Dealix · ديلكس', {
    x: 0.5, y: H - 0.45, w: 2.5, h: 0.3,
    fontFace: FH, fontSize: 9, color: C.textFaint, align: 'left',
  });
  // Page number bottom-right
  slide.addText(String(pageNum).padStart(2, '0'), {
    x: W - 1.2, y: H - 0.45, w: 0.7, h: 0.3,
    fontFace: FH, fontSize: 9, color: C.textFaint, align: 'right', bold: true,
  });
}

function darkFrame(slide, sectionLabel, pageNum) {
  slide.addShape('rect', { x: W - 0.5, y: 0.35, w: 0.08, h: 0.45, fill: { color: C.gold }, line: { type: 'none' } });
  slide.addText(sectionLabel, {
    x: W - 4.5, y: 0.3, w: 3.9, h: 0.4,
    fontFace: FH, fontSize: 12, color: C.gold, bold: true,
    align: 'right', rtlMode: true,
  });
  slide.addText('Dealix · ديلكس', {
    x: 0.5, y: H - 0.45, w: 2.5, h: 0.3,
    fontFace: FH, fontSize: 9, color: C.onDarkMuted, align: 'left',
  });
  slide.addText(String(pageNum).padStart(2, '0'), {
    x: W - 1.2, y: H - 0.45, w: 0.7, h: 0.3,
    fontFace: FH, fontSize: 9, color: C.onDarkMuted, align: 'right', bold: true,
  });
}

// Right-aligned Arabic title
function titleAR(slide, text, y = 1.0, opts = {}) {
  slide.addText(text, {
    x: 0.6, y, w: W - 1.2, h: 0.9,
    fontFace: FH, fontSize: opts.size || 34, bold: true, color: opts.color || C.navy,
    align: 'right', rtlMode: true, valign: 'middle', ...opts,
  });
}

function subtitleAR(slide, text, y = 1.85, opts = {}) {
  slide.addText(text, {
    x: 0.6, y, w: W - 1.2, h: 0.45,
    fontFace: FB, fontSize: opts.size || 15, color: opts.color || C.textMuted,
    align: 'right', rtlMode: true, valign: 'middle', ...opts,
  });
}

// Source footer (hyperlinked)
function sourceFooter(slide, sources, dark = false) {
  const parts = [{ text: 'المصدر: ', options: { fontFace: FB, rtlMode: true, color: dark ? C.onDarkMuted : C.textFaint, fontSize: 9 } }];
  sources.forEach((s, i) => {
    parts.push({
      text: s.name,
      options: { fontFace: FB, rtlMode: true, color: dark ? C.gold : C.goldDeep, fontSize: 9, hyperlink: { url: s.url } },
    });
    if (i < sources.length - 1) {
      parts.push({ text: ' · ', options: { fontFace: FB, color: dark ? C.onDarkMuted : C.textFaint, fontSize: 9 } });
    }
  });
  slide.addText(parts, {
    x: 0.5, y: H - 0.75, w: W - 2, h: 0.28,
    align: 'right', rtlMode: true,
  });
}

// ===== Slide registry =====
const slides = [];
function addSlide(build) { slides.push(build); }

// Export helper to extend via other files
module.exports = { pres, addSlide, slides, C, FH, FB, FS, W, H, SCREENSHOTS,
  ar, lightBg, darkBg, lightFrame, darkFrame, titleAR, subtitleAR, sourceFooter, OUT };
