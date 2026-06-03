# Launch Modes — لا تطلق عشوائيًا

أربعة أوضاع للإطلاق. كل وضع له هدف وشروط دخول واضحة. لا تنتقل لوضع أعلى قبل
استيفاء شروطه وموافقة المؤسس في بوابة Go/No-Go.

---

## 1. Internal Dry Run

```txt
الهدف: تجربة النظام داخليًا بدون أي إرسال خارجي.
الشروط:
  - الملفات موجودة (docs/launch + reports/launch)
  - السياسات موجودة (suppression + external content + permissions)
  - account pack dry-run يعمل
  - founder command dry-run يعمل
  - لا إرسال خارجي إطلاقًا
الحالة الحالية: مؤهّل (بانتظار موافقة المؤسس)
```

## 2. Soft Launch

```txt
الهدف: تشغيل على دفعة صغيرة جدًا (20–50 شركة) مختارة يدويًا.
الشروط:
  - Launch Score >= 75
  - الموقع يعمل
  - الأنظمة الأساسية جاهزة بسعر وتسليم
  - 20–50 Account Packs تجريبية
  - Mini Proposal Gate يعمل
  - Delivery Pack جاهز
الحالة الحالية: غير مؤهّل (Score ≈ 45)
```

## 3. Controlled Launch

```txt
الهدف: تشغيل يومي مضبوط.
الشروط:
  - Launch Score >= 85
  - Top 100 Queue يعمل
  - Contact Discovery لا يخترع
  - Email Quality Gate يعمل (تنفيذيًا)
  - Call Brief Queue يعمل
  - Delivery Pipeline يعمل
الحالة الحالية: غير مؤهّل
```

## 4. Full Launch

```txt
الهدف: تشغيل 400 Account Packs/day.
الشروط:
  - Launch Score >= 90
  - GitHub Actions green
  - npm build passes
  - schema checks pass
  - quality gates pass
  - security/privacy gates pass
  - delivery gates pass
الحالة الحالية: غير مؤهّل
```

---

## جدول الانتقال

| الوضع | الحد الأدنى للسكور | إرسال خارجي | الموافقة المطلوبة |
|-------|-------------------:|-------------|-------------------|
| Internal Dry Run | — (سلامة فقط) | لا | المؤسس |
| Soft Launch | 75 | يدوي فقط | المؤسس لكل رسالة |
| Controlled Launch | 85 | يدوي + gates | المؤسس + gates |
| Full Launch | 90 | بعد كل البوابات | المؤسس + كل البوابات خضراء |

---

## قاعدة ثابتة

> الانتقال لأعلى = صعود تدريجي. الهبوط لأسفل = فوري عند أي خرق أمني، أو سمعة دومين،
> أو اكتشاف contact مُخترَع، أو ادعاء مضمون. لا تتردد في النزول لوضع أدنى.

انظر شروط القرار في `docs/launch/LAUNCH_DECISION_GATE_AR.md`.
