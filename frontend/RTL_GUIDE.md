# دليل RTL — Dealix Frontend

هذا الدليل يحدد القواعد الإلزامية لدعم الاتجاه من اليمين إلى اليسار (RTL) في مشروع Dealix.

---

## 1. القاعدة الأساسية: الخصائص المنطقية

**لا تستخدم أبداً** الجهات المطلقة في CSS أو Tailwind (`left`, `right`, `ml`, `mr`, `pl`, `pr`).  
استخدم دائماً **Logical Properties** التي تتكيف تلقائياً مع اتجاه النص.

### Tailwind — جدول المقارنة

| ❌ تجنّب (مطلق) | ✅ استخدم (منطقي) | المعنى |
|---|---|---|
| `pl-4` | `ps-4` | padding-inline-start |
| `pr-4` | `pe-4` | padding-inline-end |
| `ml-2` | `ms-2` | margin-inline-start |
| `mr-2` | `me-2` | margin-inline-end |
| `left-0` | `start-0` | inset-inline-start |
| `right-0` | `end-0` | inset-inline-end |
| `text-left` | `text-start` | محاذاة بداية النص |
| `text-right` | `text-end` | محاذاة نهاية النص |
| `border-l` | `border-s` | حد الجانب البادئ |
| `border-r` | `border-e` | حد الجانب الختامي |
| `rounded-l` | `rounded-s` | زوايا الجانب البادئ |
| `rounded-r` | `rounded-e` | زوايا الجانب الختامي |

### مثال عملي

```tsx
// ❌ خطأ
<div className="pl-4 ml-2 text-left border-l">

// ✅ صحيح
<div className="ps-4 ms-2 text-start border-s">
```

---

## 2. إعداد HTML الصحيح

يجب ضبط الاتجاه واللغة على مستوى `<html>`:

```tsx
// src/app/layout.tsx
export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ar" dir="rtl">
      <body>{children}</body>
    </html>
  );
}
```

---

## 3. الخطوط العربية

### التكوين في tailwind.config.js

```js
fontFamily: {
  arabic: ['IBM Plex Sans Arabic', 'Tajawal', 'sans-serif'],
  sans: ['Inter', 'IBM Plex Sans Arabic', 'sans-serif'],
}
```

### تحميل الخطوط في layout.tsx

```tsx
import { IBM_Plex_Sans_Arabic } from 'next/font/google';

const arabicFont = IBM_Plex_Sans_Arabic({
  subsets: ['arabic'],
  weight: ['300', '400', '500', '600', '700'],
  variable: '--font-arabic',
});
```

---

## 4. أيقونات الأسهم في RTL

الأسهم يجب أن تُعكس اتجاهها في RTL. استخدم `rtl:rotate-180` أو `dir="rtl"`:

```tsx
// ✅ عكس السهم تلقائياً في RTL
<ArrowRight className="rtl:rotate-180 transition-transform" />

// ✅ أو باستخدام CSS
.icon-arrow {
  transform: scaleX(1);
}
[dir="rtl"] .icon-arrow {
  transform: scaleX(-1);
}
```

**الأيقونات التي تحتاج عكساً:** `ArrowLeft`, `ArrowRight`, `ChevronLeft`, `ChevronRight`, `ArrowBack`, `ArrowForward`  
**الأيقونات التي لا تحتاج عكساً:** `ArrowUp`, `ArrowDown`, `Close`, `Search`, `Settings`

---

## 5. النصوص المختلطة (عربي + إنجليزي)

عند خلط النصوص العربية والإنجليزية، استخدم `<bdi>` لعزل الاتجاه:

```tsx
// ✅ عزل النص الإنجليزي داخل نص عربي
<p>
  رقم الطلب: <bdi>ORD-2024-1234</bdi>
</p>

// ✅ عزل الاسم الأجنبي
<p>
  المطوّر: <bdi>John Smith</bdi>
</p>
```

### متى تستخدم `<bdi>` vs `<span dir="ltr">`؟

- `<bdi>`: عندما لا تعرف اتجاه النص مسبقاً (بيانات ديناميكية)
- `<span dir="ltr">`: عندما تعرف أن النص دائماً LTR (أسماء إنجليزية، أكواد، إلخ)

```tsx
// بيانات ديناميكية — اتجاه مجهول
<bdi>{userName}</bdi>

// نص دائماً إنجليزي
<span dir="ltr">API_KEY_12345</span>
```

---

## 6. الأرقام في RTL

### أرقام عربية مقابل غربية

```tsx
// عرض أرقام بالتنسيق السعودي (أرقام غربية مع فاصلة ألوف)
const formatNumber = (num: number) =>
  new Intl.NumberFormat('en-SA').format(num);

// عرض أرقام عربية (الخيار الثقافي)
const formatArabicNumber = (num: number) =>
  new Intl.NumberFormat('ar-SA').format(num);
```

### font-variant-numeric

لضبط مظهر الأرقام في CSS:

```css
/* أرقام بعرض ثابت (مفيد في الجداول) */
.tabular-nums {
  font-variant-numeric: tabular-nums;
}

/* أرقام بعرض متناسب */
.proportional-nums {
  font-variant-numeric: proportional-nums;
}
```

في Tailwind:

```tsx
<span className="tabular-nums">{price}</span>
```

---

## 7. المكوّنات الحساسة للاتجاه

### Flexbox

```tsx
// ✅ flex-row يعمل بشكل صحيح مع RTL تلقائياً
// (العناصر تبدأ من اليمين في RTL)
<div className="flex flex-row gap-4">
  <span>أول</span>
  <span>ثاني</span>
</div>

// ⚠️ تجنّب justify-start بشكل مطلق — استخدم معنى منطقي
// justify-start = justify-end في RTL بالفعل
```

### Grid

```tsx
// ✅ Grid يتكيف تلقائياً مع RTL
<div className="grid grid-cols-3 gap-4">
  {items.map(item => <Card key={item.id} {...item} />)}
</div>
```

---

## 8. الاختبار

### التحقق اليدوي

1. افتح DevTools في المتصفح
2. تأكد من `dir="rtl"` على `<html>`
3. تحقق من عدم وجود overflow أفقي
4. اختبر التنقل بالكيبورد (Tab/Shift+Tab) — يجب أن يسير من اليمين لليسار

### اختبار سريع في CSS

```css
/* أضف هذا مؤقتاً للكشف عن الخصائص المطلقة */
[dir="rtl"] [class*="pl-"],
[dir="rtl"] [class*="pr-"],
[dir="rtl"] [class*="ml-"],
[dir="rtl"] [class*="mr-"] {
  outline: 2px solid red !important;
}
```

---

## 9. أدوات مساعدة

- [RTL Styler (متصفح)](https://chrome.google.com/webstore/detail/rtl-styler) — لمعاينة RTL
- [Tailwind RTL Plugin](https://github.com/20lives/tailwindcss-rtl) — إن احتجت تحكماً أدق
- [MDN: CSS Logical Properties](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_logical_properties_and_values)

---

## ملخص سريع

```
✅ ps-/pe-     ❌ pl-/pr-
✅ ms-/me-     ❌ ml-/mr-
✅ start-/end- ❌ left-/right-
✅ text-start  ❌ text-left
✅ <bdi>       للنصوص المختلطة
✅ rtl:rotate-180  لأيقونات الأسهم
✅ dir="rtl"   على <html>
```
