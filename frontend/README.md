# Dealix Frontend

واجهة مستخدم منصة **Dealix** مبنية بـ **Next.js 15** و**React 19**، مع دعم RTL أولاً للغة العربية.

---

## المكدس التقني

| المكوّن | الإصدار |
|---|---|
| Next.js | 15.1.0 |
| React | 19.0.0 |
| TypeScript | 5.7.3 |
| Tailwind CSS | 3.4.17 |
| Framer Motion | ^11 |
| Recharts | ^2 |

---

## المتطلبات الأساسية

- Node.js `>=20.10.0 <21.0.0`
- pnpm `9.12.0` (مدير الحزم الرسمي للمشروع)

---

## التثبيت

```bash
# استنساخ المستودع
git clone <repo-url>
cd dealix-clean/frontend

# نسخ متغيرات البيئة
cp .env.example .env.local

# تثبيت الحزم
pnpm install
# أو باستخدام npm (للتوافق مع Makefile)
npm ci
```

عدّل `.env.local` وأدخل رابط الـ API الصحيح:

```env
NEXT_PUBLIC_API_URL=http://localhost:8000
NEXT_PUBLIC_APP_ENV=development
NEXT_PUBLIC_DEFAULT_LOCALE=ar
```

---

## التشغيل في بيئة التطوير

```bash
pnpm dev
# أو
make dev
```

الموقع يعمل على: [http://localhost:3000](http://localhost:3000)

---

## البناء للإنتاج

```bash
pnpm build
# أو
make build
```

الناتج في مجلد `.next/standalone/` (وضع `standalone` مُفعَّل).

---

## فحص الجودة

```bash
# فحص ESLint
make lint

# تنسيق Prettier
make format

# تشغيل الاختبارات
make test

# اختبارات E2E (Playwright)
pnpm test:e2e
```

---

## قواعد RTL (يمين لليسار)

المشروع مبني على مبدأ **RTL first** — العربية هي اللغة الأساسية.

### الخط

- الخط الأساسي: **IBM Plex Sans Arabic** + Tajawal (fallback)
- الخط الثانوي (إنجليزي): Inter

### الاتجاه

يجب ضبط `dir="rtl"` على عنصر `<html>` في `layout.tsx`:

```tsx
<html lang="ar" dir="rtl">
```

### Tailwind — الخصائص المنطقية

استخدم دائماً الخصائص المنطقية بدلاً من الجهات المطلقة:

```
ps-4 pe-4   ← بدلاً من pl-4 pr-4
ms-2 me-2   ← بدلاً من ml-2 mr-2
start-0     ← بدلاً من left-0
end-0       ← بدلاً من right-0
```

راجع [RTL_GUIDE.md](./RTL_GUIDE.md) للتفاصيل الكاملة.

---

## البنية العامة

```
frontend/
├── src/
│   ├── app/          # App Router (Next.js 15)
│   ├── components/   # مكونات React
│   ├── contexts/     # React Contexts
│   ├── hooks/        # Custom Hooks
│   ├── i18n/         # ترجمات ar/en
│   ├── lib/          # مكتبات مساعدة
│   └── styles/       # CSS مخصص وتوكنز
├── public/           # ملفات ثابتة
├── e2e/              # اختبارات Playwright
└── tests/            # اختبارات إضافية
```

---

## روابط مفيدة

- [توثيق Next.js 15](https://nextjs.org/docs)
- [React 19 changelog](https://react.dev/blog/2024/12/05/react-19)
- [Tailwind CSS Logical Properties](https://tailwindcss.com/docs/padding#using-logical-properties)
- [دليل RTL للمشروع](./RTL_GUIDE.md)
