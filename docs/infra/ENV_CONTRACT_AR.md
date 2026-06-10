# عقد البيئة — Dealix Environment Contract (AR)

> **المرجع التشغيلي لقواعد .env.** كل env var في `.env.example` يجب أن
> يطابق القواعد هنا. `scripts/check_env_contract.py` ينفّذ هذا العقد.

**الحالة:** مسودة — Phase 1 من Agent #12
**التاريخ:** 2026-06-03

---

## 1. مستويات التصنيف (Variable Tiers)

| المستوى | الوصف | السلوك عند الغياب |
| --- | --- | --- |
| `[REQUIRED]` | لا يقلع الإنتاج بدونه | `_validate_production_secrets` يفشل |
| `[REVENUE]` | مطلوب لتدفق الدفع | الإنتاج يقلع لكن checkout يفشل |
| `[OPTIONAL]` | تحسين أداء/ميزة | التطبيق يتدهور gracefully |

## 2. القواعد التركيبية (Syntax Rules)

1. **القيم النصية بدون اقتباس** إلا إذا احتوت على مسافات أو أحرف خاصة.
2. **السرية** لا تُطبع أبداً (تبدأ بـ `sk_`, `phc_`, `key-`, أو
   `REPLACE_ME`).
3. **Placeholders** دائماً بهذا الشكل: `REPLACE_ME`, `CHANGE_ME_to_*`.
4. **القيم الافتراضية** مسموحة فقط لـ `[OPTIONAL]`.
5. **البيئة** (staging/production) يجب أن تكون مرئية في اسم الملف
   (`.env.prod.example`, `.env.staging.example`).

## 3. قواعد التسمية (Naming)

- الأحرف الكبيرة + underscores (snake_case).
- prefix دالّ على المزوّد: `MOYASAR_`, `ANTHROPIC_`, `WHATSAPP_`.
- secrets لا تحتوي `DEMO` أو `TEST` (إلا staging).

## 4. عقد staging vs production (Parity)

| المتغير | staging | production |
| --- | --- | --- |
| `ENVIRONMENT` | `staging` | `production` |
| `MOYASAR_LIVE_MODE` | `0` | `1` (عند التفعيل) |
| `WHATSAPP_MOCK_MODE` | `true` | `false` |
| `DATABASE_URL` | staging DB | production DB |
| `APP_URL` | `https://staging.dealix.me` | `https://dealix.sa` |
| `CORS_ORIGINS` | staging + localhost | production فقط |
| `POSTHOG_API_KEY` | test project | production project |
| `SENTRY_DSN` | test project | production project |

**ممنوع** استخدام staging secret في production أو العكس.

## 5. عملية الإضافة (Adding a New Variable)

1. أضف المتغير في `.env.example` (placeholder).
2. صنّفه في أحد المستويات الثلاثة في التعليق.
3. أضفه في `.env.prod.example` و `.env.staging.example` إن لزم.
4. شغّل `make env-check` — يجب أن يمر.
5. وثّقه في `docs/infra/ENV_CONTRACT_AR.md` (هذا الـ doc).
6. أخبر الفريق في `#deploys`.

## 6. عملية الحذف (Removing a Variable)

1. احذف من `.env.example`.
2. شغّل `make env-check` — سيُظهر متغيرات قديمة في staging/production.
3. نظّف staging → production بالترتيب.
4. بعد أسبوعين: حذف نهائي من الكود.

## 7. المراجع

- `docs/infra/ENVIRONMENT_POLICY_AR.md` — policy
- `docs/infra/STAGING_PRODUCTION_POLICY_AR.md` — staging/production
- `docs/infra/SECRETS_MANAGEMENT_AR.md` — secrets
- `docs/infra/CONFIGURATION_DRIFT_POLICY_AR.md` — drift
- `scripts/check_env_contract.py` — enforcer
- `.env.example` — master template
- `.env.prod.example`, `.env.staging.example`, `.env.railway.example`
