# 🔷 Dealix Brand Guidelines v1.0

> **Saudi B2B Revenue Operations · AI-Powered · Trust-First**

---

## Brand Identity

**Dealix** هو نظام تشغيل إيرادات AI مبني خصيصاً للشركات B2B السعودية. هويتنا البصرية تعبّر عن:

- **الاحترافية**: Navy العميق — ثقة، سلطة، جدية
- **الفخامة**: Gold الذهبي — قيمة مضافة، تميز، نجاح
- **الحداثة**: خطوط نظيفة، تصميم مسطّح، واجهات ذكية

---

## الألوان الأساسية

| الاسم | HEX | Tailwind | الاستخدام |
|-------|-----|----------|-----------|
| **Dealix Navy** | `#001F3F` | `bg-dealix-navy` | الخلفيات الرئيسية، Headers، Buttons |
| **Dealix Gold** | `#D4AF37` | `bg-dealix-gold` | Accents، CTAs، Active states |
| **Dealix Black** | `#0A0A0A` | `text-dealix-black` | النصوص الداكنة |
| **White** | `#FFFFFF` | `text-white` | النصوص على الخلفيات الداكنة |

### الألوان الثانوية

| الاسم | HEX | Tailwind | الاستخدام |
|-------|-----|----------|-----------|
| Slate | `#364558` | `text-dealix-slate` | النصوص الثانوية |
| Ocean | `#0066FF` | `text-dealix-ocean` | Links، Info |
| Emerald | `#10B981` | `text-dealix-emerald` | Success، Active |
| Coral | `#EF4444` | `text-dealix-coral` | Error، Danger |
| Amber | `#F59E0B` | `text-dealix-amber` | Warning، Pending |

---

## الخطوط

### العناوين (Display)
```
font-family: 'Poppins', 'Cairo', system-ui, sans-serif;
font-weight: 700–900
class: font-display
```

### النصوص (Body)
```
font-family: 'Inter', 'Tajawal', system-ui, sans-serif;
font-weight: 400–600
class: font-body
```

### الكود (Mono)
```
font-family: 'IBM Plex Mono', monospace;
class: font-mono
```

---

## استخدام اللون الأساسي

### ✅ صحيح
```tsx
// خلفية Navy
<div className="bg-dealix-navy text-white">

// Accent ذهبي
<button className="bg-dealix-gold text-dealix-navy font-bold">

// بوردر ذهبي
<div className="border border-dealix-gold">

// نص ذهبي كـ Gradient
<h1 className="gradient-text">
```

### ❌ خاطئ
```tsx
// لا تستخدم ألوان Emerald كـ primary
<button className="bg-emerald-500">

// لا تستخدم ألواناً خارج الـ palette
<div className="bg-blue-700">

// لا تستخدم النصوص بدون contrast كافٍ
<p className="text-gray-400" style={{ background: "#fff" }}>
```

---

## قواعد Typography

| مستوى | Class | الاستخدام |
|-------|-------|-----------|
| H1 | `text-5xl font-black font-display` | Hero headlines |
| H2 | `text-4xl font-black font-display` | Section titles |
| H3 | `text-2xl font-bold font-display` | Card headers |
| Body Large | `text-lg text-white/80` | Lead paragraphs |
| Body | `text-base text-white/70` | Content |
| Caption | `text-xs text-white/50` | Labels, metadata |

---

## المكونات الرئيسية

### Button Primary
```tsx
<Button className="bg-dealix-gold text-dealix-navy hover:bg-yellow-400 font-bold shadow-gold">
```

### Button Secondary
```tsx
<Button variant="outline" className="border-white/20 text-white hover:border-dealix-gold">
```

### Card
```tsx
<Card className="bg-white/5 border-white/10 hover-gold shadow-none">
```

### Badge
```tsx
<Badge className="bg-dealix-gold/20 text-dealix-gold border border-dealix-gold/30">
```

---

## الـ CSS Utilities المتاحة

```css
.gradient-text    /* Gradient ذهبي على النص */
.navy-surface     /* خلفية Navy gradient */
.dot-pattern      /* نقاط ذهبية خفيفة كـ background */
.glass            /* Glassmorphism effect */
.hover-gold       /* Border + glow ذهبي عند hover */
.animate-gold-pulse /* نبضة ذهبية مستمرة */
.animate-fade-up  /* ظهور مع حركة للأعلى */
```

---

## Accessibility

- **Navy + White**: نسبة تباين `12.6:1` — WCAG AAA ✅
- **Gold + Navy**: نسبة تباين `7.4:1` — WCAG AAA ✅
- جميع العناصر التفاعلية تدعم **keyboard navigation**
- Focus ring: `ring-dealix-gold`

---

## RTL / Arabic

```html
<!-- دائماً أضف dir="rtl" على الصفحات العربية -->
<div dir="rtl" className="...">

<!-- الخطوط العربية تُحدَّد تلقائياً عبر الـ font stack -->
font-family: 'Poppins', 'Cairo', sans-serif;
```

---

**Version**: 1.0 · **Date**: May 2026 · **Status**: Production ✅
