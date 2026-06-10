# نظام الطباعة | Dealix Typography System

## فلسفة الطباعة
نظام الطباعة لـ Dealix يجمع بين **الوقار المؤسسي** للخطوط الكو豪ية (Kufi) وال**وضوح القراءة** للخطوط اللاتينية الحديثة، مع احترام تام لخصوصية اللغة العربية.

---

## 1. مجموعة الخطوط | Font Stack

### العربية
| الاستخدام | الخط الأساسي | الخط البديل |
|-----------|-------------|-------------|
| **العناوين الرئيسية** | Noto Kufi Arabic | Cairo, sans-serif |
| **النصوص الطويلة** | Noto Naskh Arabic | Noto Sans Arabic, sans-serif |
| **النصوص العامة** | Cairo | Noto Sans Arabic, Tajawal, sans-serif |
| **الشفرات** | IBM Plex Mono | —— |

### Latin / English
| الاستخدام | الخط الأساسي | الخط البديل |
|-----------|-------------|-------------|
| **العناوين** | Poppins | Inter, sans-serif |
| **النصوص** | Inter | system-ui, sans-serif |
| **الشفرات** | JetBrains Mono | IBM Plex Mono, monospace |

### Stack الكامل
```css
--font-arabic:   "Noto Kufi Arabic", "Noto Naskh Arabic", "Cairo", "IBM Plex Sans Arabic", system-ui, sans-serif;
--font-display:  "Cairo", "Noto Kufi Arabic", "Poppins", system-ui, sans-serif;
--font-body:     "Inter", "Noto Sans Arabic", "Tajawal", system-ui, sans-serif;
--font-mono:     "JetBrains Mono", "IBM Plex Mono", "Fira Code", monospace;
--font-heading:  "Noto Kufi Arabic", "Cairo", "Inter", system-ui, sans-serif;
```

---

## 2. مقياس الأحجام | Size Scale

| الاسم | حجم الخط (rem) | حجم الخط (px) | ارتفاع السطر | تباعد الحروف | السمك |
|-------|---------------|---------------|--------------|-------------|-------|
| **7xl** | 4.5rem | 72px | 1.05 | -0.03em | 700 |
| **6xl** | 3.75rem | 60px | 1.05 | -0.025em | 700 |
| **5xl** | 3rem | 48px | 1.1 | -0.02em | 700 |
| **4xl** | 2.25rem | 36px | 1.15 | -0.015em | 700 |
| **3xl** | 1.875rem | 30px | 1.2 | -0.01em | 600 |
| **2xl** | 1.5rem | 24px | 1.3 | 0 | 600 |
| **xl** | 1.25rem | 20px | 1.35 | 0 | 600 |
| **lg** | 1.125rem | 18px | 1.5 | 0 | 400 |
| **base** | 1rem | 16px | 1.6 | 0 | 400 |
| **sm** | 0.875rem | 14px | 1.5 | 0 | 400 |
| **xs** | 0.75rem | 12px | 1.5 | 0.02em | 500 |

---

## 3. شبكة الخطوط (Modular Scale)

تستخدم Dealix مقياس الخط النمطي (Modular Scale) بنسبة 1.25 Major Third للعناوين:

```
7xl: 4.5rem  ← 6xl × 1.2
6xl: 3.75rem ← 5xl × 1.25
5xl: 3rem    ← 4xl × 1.333
4xl: 2.25rem ← 3xl × 1.2
3xl: 1.875rem ← 2xl × 1.25
2xl: 1.5rem  ← xl × 1.2
xl:  1.25rem ← lg × 1.111
lg:  1.125rem ← base × 1.125
base: 1rem   (أساس)
sm:  0.875rem ← base × 0.875
xs:  0.75rem ← base × 0.75
```

---

## 4. أوزان الخطوط | Font Weights

| الاسم | القيمة | العربية | English |
|-------|--------|---------|---------|
| Thin | 100 | نادر الاستخدام | Headings |
| ExtraLight | 200 | نادر | —— |
| Light | 300 | نصوص كبيرة فاتحة | Body |
| Regular | 400 | النصوص العامة | Body |
| Medium | 500 | نصوص مهمة | Buttons |
| SemiBold | 600 | عناوين فرعية | Subheadings |
| Bold | 700 | عناوين رئيسية ★ | Headings ★ |
| ExtraBold | 800 | عناوين عرض | Display |
| Black | 900 | نادر جداً | Display Large |

---

## 5. أزواج الخطوط | Font Pairings

### للصفحات الرئيسية (Landing Pages)
```
العنوان: Noto Kufi Arabic Bold
النص: Inter Regular
الأزرار: Inter SemiBold
```

### للوحات القيادة (Dashboards)
```
العنوان: Cairo Bold
النص: Noto Sans Arabic Light
الأرقام: Poppins SemiBold
```

### للمحتوى الطويل (Blog/Articles)
```
العنوان: Noto Kufi Arabic Bold
النص: Noto Naskh Arabic Regular
اقتباسات: Noto Naskh Arabic Italic (للاتيني فقط)
```

### للعروض التقديمية
```
العنوان: Poppins Bold (للاتيني) / Cairo Black (عربي)
النص: Inter Light / Noto Sans Arabic Light
الأرقام: Poppins Bold → JetBrains Mono
```

---

## 6. الاستجابة (Responsive Typography)

```css
/* العناوين (clamp) */
h1 { font-size: clamp(2rem, 5vw, 3.75rem); }
h2 { font-size: clamp(1.5rem, 3.6vw, 2.75rem); }
h3 { font-size: clamp(1.25rem, 2.5vw, 1.875rem); }
h4 { font-size: clamp(1.125rem, 1.8vw, 1.5rem); }
```

| الجهاز | حجم h1 | حجم h2 | حجم h3 | حجم النص |
|--------|--------|--------|--------|---------|
| **جوال صغير** (320px) | 32px | 24px | 20px | 14px |
| **جوال كبير** (414px) | 36px | 28px | 22px | 15px |
| **جهاز لوحي** (768px) | 44px | 32px | 26px | 16px |
| **سطح مكتب** (1280px) | 52px | 38px | 28px | 16px |
| **شاشة كبيرة** (1536px) | 60px | 44px | 30px | 18px |

---

## 7. RTL و LTR

### إعدادات RTL للعربية
```css
[dir="rtl"] {
  text-align: right;
  letter-spacing: 0; /* إلغاء تباعد الحروف للعربية */
  font-variant-numeric: traditional; /* للأرقام العربية */
}
```

### قواعد مهمة
- **للغة العربية**: لا تستخدم الخط المائل (Italic) — معظم الخطوط العربية لا تدعمه
- **للغة العربية**: تجنب التباعد الزائد بين الحروف (Letter-spacing)
- **للغة الإنجليزية**: استخدم التباعد السلبي للعناوين الكبيرة
- **للغة الإنجليزية**: الخطوط sans-serif مثل Inter و Poppins هي الخيار الأساسي

---

## 8. قواعد الطباعة العامة

| الخاصية | القيمة | ملاحظة |
|---------|--------|--------|
| ارتفاع السطر (عناوين) | 1.05 - 1.3 | ضيق للعناوين الكبيرة |
| ارتفاع السطر (نصوص) | 1.5 - 1.7 | مريح للقراءة الطويلة |
| تباعد الفقرات | 1em | مسافة كافية بين الفقرات |
| عرض الفقرة الأمثل | 45-75 حرفاً | لسهولة القراءة |
| تنسيق الأرقام | Tabular figures | للمقارنة الرقمية في الجداول |

---

## 9. توفر الخطوط | Font Loading

### استراتيجية التحميل
1. **Preconnect** → خوادم Google Fonts
2. **Preload** → Arabic + Latin fonts (WOFF2)
3. **CSS font-display: swap** → لتفادي FOUT مرئي
4. **Fallback fonts** → خطوط النظام كخطة احتياطية

```html
<link rel="preconnect" href="https://fonts.googleapis.com" />
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
<link rel="preload" as="style" href="https://fonts.googleapis.com/css2?family=Noto+Kufi+Arabic:wght@400;600;700&family=Inter:wght@400;500;600;700&display=swap" />
<link rel="stylesheet" href="..." media="print" onload="this.media='all'" />
```

---

## 10. أمثلة طباعية

### 1. الصفحة الرئيسية
```
عرض (7xl): غرفة قيادة النمو والإيراد
ترويسة (2xl): وقتها نحقق إيرادات حقيقية
جسم (base): نظام تشغيل مؤسسي للإيراد والصفقات
تسمية (xs): Saudi-first · Arabic-first
```

### 2. بطاقة خدمة
```
عنوان البطاقة (xl): سرعة القرار
وصف (sm): الموافقات التي تستغرق أسابيع تُنجز في ساعات
Badge (xs): APPROVED / PENDING / ACTION REQUIRED
```

### 3. لوحة القيادة
```
عنوان القسم (2xl): الفرص الحالية
رقم KPI (5xl): 42
ملصق KPI (sm): فرص أولوية عالية
جدول (sm): شركة · القيمة · الحالة · تاريخ المتابعة
```

---

> **آخر تحديث**: 1 يونيو 2026 | **الإصدار**: 2.0 | **الخطوط المطلوبة**: 8 عائلات
