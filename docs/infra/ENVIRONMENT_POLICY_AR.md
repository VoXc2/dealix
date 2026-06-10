# سياسة البيئات — Dealix Environment Policy (AR)

> **وثيقة تشغيلية، ليست استشارة قانونية أو نهائية.** كل قرار نهائي في الإنتاج يحتاج موافقة المؤسس.

**الحالة:** مسودة — Phase 1 من Agent #12
**التاريخ:** 2026-06-03
**المالك:** المؤسس + Agent #12

---

## 1. الغرض

هذه الوثيقة تحدد **البيئات الرسمية** في Dealix، صلاحيات كل بيئة، بيانات
كل بيئة، التكاملات المسموحة، آليات النشر، وآليات التراجع، ومن يملك
الموافقة على كل إجراء.

الفلسفة: **البيئات معزولة بالسياسة قبل أن تكون معزولة بالبنية التحتية**.

## 2. البيئات الرسمية

| # | البيئة | الغرض | المالك | موافقة النشر |
| - | --- | --- | --- | --- |
| 1 | **local** | تطوير على جهاز المطور | المطوّر | لا يحتاج |
| 2 | **preview** | PR / branch preview (Vercel / Railway ephemeral) | المطوّر | لا يحتاج (ephemeral) |
| 3 | **staging** | محاكاة الإنتاج ببيانات وهمية | المؤسس + Agent #2 | المؤسس |
| 4 | **production** | التشغيل الفعلي للعملاء | المؤسس | المؤسس (إلزامي) |

## 3. قواعد العزل (لكل بيئة)

### 3.1 local
- بيانات: بيانات وهمية أو seed فقط.
- تكاملات: **لا يوجد إرسال خارجي** — كل القنوات في وضع mock.
- أسرار: نسخة `.env` محلية فقط، **لا تُرفع إلى git أبداً**.
- نشر: لا يوجد (تشغيل مباشر).
- تراجع: لا يوجد (تشغيل مباشر).

### 3.2 preview
- بيانات: seed ثابت (نفس seed staging).
- تكاملات: **mock فقط** — لا Moyasar حي، لا WhatsApp حي، لا Gmail حي.
- أسرار: مفاتيح preview المخصصة (لو وُجدت) فقط، لا مفاتيح الإنتاج.
- نشر: تلقائي عند فتح PR (workflow `ci.yml`).
- تراجع: إغلاق الـ PR يكفي.

### 3.3 staging
- بيانات: بيانات seed + بيانات اختبار من staging DB.
- تكاملات: **تكاملات وضع الاختبار فقط**:
  - Moyasar sandbox فقط.
  - WhatsApp provider في وضع `WHATSAPP_MOCK_MODE=true`.
  - Gmail OAuth مع حساب اختبار.
  - Calendly URL اختبار.
- أسرار: staging-specific secrets، **لا أسرار إنتاج** تحت أي ظرف.
- نشر: المؤسس يوافق عبر `bash scripts/founder_production_smoke.sh` (في
  وضع `--env=staging`).
- تراجع: `scripts/post_redeploy_verify.sh` يكشف الفشل تلقائياً ويعيد
  الـ rollback خلال 5 دقائق.

### 3.4 production
- بيانات: بيانات حقيقية فقط (موجودة في DB الإنتاج).
- تكاملات: تكاملات الإنتاج الحقيقية — **مفعّلة فقط بعد موافقة المؤسس**.
- أسرار: **1Password vault** (`Dealix Production`)؛ لا أحد غير المؤسس
  يصل إليها.
- نشر: عبر Railway `preDeployCommand` → `scripts/railway_predeploy.sh` →
  `startCommand` `uvicorn api.main:app --workers 1`؛ **الموافقة يدوية
  من المؤسس** في `railway_deploy.yml`.
- تراجع: `restartPolicyType = "ON_FAILURE"` (10 محاولات)؛ rollback
  صريح عبر `scripts/railway_redeploy_checklist.py`.

## 4. القواعد العامة

1. **لا يُرفع أي `.env` إلى git.** أبداً. (`check_env_contract.py`
   يفشل البناء لو تم ذلك.)
2. **كل workflow يكتب للإنتاج** يجب أن يمر عبر:
   - `pull_request_target` ممنوع في workflows الإنتاج (دفاع ضد
     `arXiv:2605.07135`).
   - `workflow_run` ممنوع إلا مع allowlist صريح ومراجعة يدوية.
3. **لا إرسال خارجي تلقائي** من CI. كل إرسال حي يجب أن يكون:
   - من workflow `workflow_dispatch` يدوي، أو
   - عبر cron مع `environment: production` و approval gate.
4. **Production secret** في GitHub Actions: ممنوع. مفاتيح الإنتاج لا
   تظهر إلا في Railway environment variables، مرتبطة بـ
   `DEALIX_PRODUCTION` GitHub Environment.
5. **كل عملية نشر** لها **rollback** مُعرَّف قبل النشر.
6. **كل عملية نشر إنتاج** تُسجَّل في `audit_log` مع `actor`,
   `commit_sha`, `environment`, `timestamp`.
7. **لا أسرار في الـ logs أو التقارير أو الـ prompts.** أبداً.
8. **Defensive boundaries** للأدوات (per `arXiv:2604.11790`): أي tool
   call يأخذ untrusted input (PR body, issue text, fetched URL) يجب
   أن يكون خلف allowlist schema، وليس خلف model-only validation.

## 5. عقد البيئة (ENV_CONTRACT)

`scripts/check_env_contract.py` (3196 bytes) هو المرجع التنفيذي. كل
متغير في `.env.example` يجب أن يكون مُصنَّفاً على أحد المستويات:

| المستوى | الوصف | مثال |
| --- | --- | --- |
| `[REQUIRED]` | لا يقلع الإنتاج بدونه | `APP_SECRET_KEY`, `DATABASE_URL` |
| `[REVENUE]` | مطلوب لتدفق الدفع (Moyasar) | `MOYASAR_SECRET_KEY`, `MOYASAR_WEBHOOK_SECRET` |
| `[OPTIONAL]` | تحسين أداء/ميزة، التطبيق يتدهور gracefully بدونه | `SENTRY_DSN`, `POSTHOG_API_KEY` |

**الاختبار:** `make env-check` يجب أن يمر قبل أي merge إلى `main`.

## 6. الانجراف (Configuration Drift)

تعريف الانجراف: أي اختلاف بين `.env.example` (في main) وقيم staging أو
production في Railway environment variables.

**السياسة:**

1. الانجراف المسموح: إضافة متغير جديد في `.env.example` لم يصل بعد إلى
   staging (grace period: أسبوع).
2. الانجراف الممنوع:
   - متغير محذوف من `.env.example` ولا يزال موجوداً في staging/production.
   - قيمة في staging/production غير موجودة في `.env.example`.
   - اختلاف تصنيف بين `.env.example` و `.env.prod.example` /
     `.env.staging.example` / `.env.railway.example`.
3. **الكاشف:** `scripts/validate_railway_generated_env.py` +
   `scripts/sync_railway_generated_env.py`. يُشغَّل يومياً عبر
   `.github/workflows/watchdog_drift.yml`.
4. **المعالجة:** أي drift يُسجَّل في `reports/infra/drift_log.md` ويعمل
   PR تلقائي عند الحاجة (لا merge تلقائي).

## 7. الموافقات

| الإجراء | المطلوب |
| --- | --- |
| نشر إلى production | موافقة المؤسس (manual approval في GitHub Environment) |
| نشر إلى staging | موافقة المؤسس (manual) أو CI نجاح من branch موثوق |
| تشغيل cron في production | workflow_dispatch + موافقة |
| قراءة production secret | المؤسس فقط (لا SRE hire حالياً) |
| تعديل workflow يستخدم production secrets | PR + مراجعة المؤسس + CI |
| حذف backup | موافقة المؤسس + ticketing في 1Password |

## 8. المراجع

- `scripts/check_env_contract.py` — env contract enforcement
- `scripts/security_smoke.py` — security baseline
- `scripts/verify_railway_production_config.py` — Railway-specific
- `scripts/railway_launch_env_check.py` — env matrix
- `docs/ops/BACKUP_RESTORE.md` — backup tiers
- `docs/SLO.md` — service level objectives
- `docs/ON_CALL.md` — on-call coverage
- `docs/SECURITY_RUNBOOK.md` — incident response
- `docs/QUICK_DEPLOY_API_KEYS_ONLY.md` — fast deploy path
- `docs/RAILWAY_DEPLOY_GUIDE_AR.md` — Railway deploy (AR)
- `docs/STAGING_DEPLOYMENT.md` — staging deploy
- `docs/DEPLOY_CHECKLIST.md` — pre-deploy checklist
- `docs/contributing/DEPLOYMENT.md` — universal deploy
