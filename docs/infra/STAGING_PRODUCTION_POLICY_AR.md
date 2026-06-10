# سياسة فصل Staging / Production — Dealix

> وثيقة تشغيلية. كل نشر إنتاج يحتاج موافقة يدوية من المؤسس.

**الحالة:** مسودة — Phase 1 من Agent #12
**التاريخ:** 2026-06-03

---

## 1. القاعدة الذهبية

**Staging يحاكي الإنتاج في البنية، لا في البيانات ولا في الأسرار ولا في
الإرسال.**

## 2. ما يمكن أن يكون مشتركاً

- **نفس الكود** (نفس commit SHA).
- **نفس البنية** (Postgres + Redis + Mongo + PgBouncer).
- **نفس workflow templates** (CI matrix يحدد فقط الفروقات).
- **نفس Docker image** (نفس `Dockerfile` + نفس base image).

## 3. ما يجب أن يكون مختلفاً

| البُعد | Staging | Production |
| --- | --- | --- |
| **قاعدة البيانات** | DB منفصل، بيانات seed + بيانات اختبار | DB الإنتاج، بيانات حقيقية |
| **Moyasar** | sandbox mode (لا رسوم حقيقية) | live mode (عند التفعيل) |
| **WhatsApp** | `WHATSAPP_MOCK_MODE=true`، قوالب اختبار فقط | mock معطّل، قوالب Meta معتمدة |
| **Gmail / Email** | حساب Gmail اختبار مع list-unsubscribe وهمي | حساب الإنتاج، DNS موثق |
| **HubSpot** | HubSpot portal اختبار | HubSpot portal الإنتاج |
| **Calendly** | `CALENDLY_URL` يشير إلى صفحة اختبار | `CALENDLY_URL` الإنتاج |
| **PostHog** | project اختبار | project الإنتاج |
| **Sentry** | project اختبار | project الإنتاج + alert routing |
| **App URL** | `https://staging.dealix.me` | `https://dealix.sa` |
| **CORS** | يضيف staging domain | لا staging domain |
| **API keys** | مفاتيح staging فقط | مفاتيح الإنتاج (1Password) |
| **Webhook secrets** | قيم staging | قيم الإنتاج (1Password) |
| **Redis / Mongo** | بيانات اختبار فقط | بيانات حقيقية |
| **Backups** | اختياري (Tier 2 weekly) | إلزامي (5 tiers، see BACKUP_RESTORE.md) |
| **Restore drill** | ربع سنوي على staging | ربع سنوي على production data (sandbox restore) |

## 4. النشر

### 4.1 staging
- عبر `.github/workflows/staging-smoke.yml` (يدوي أو على push لـ
  `release/staging`).
- `railway.toml` (staging variant) يستخدم `startCommand` بدون
  workers متعددين.
- لا يفعّل live mode لأي قناة.

### 4.2 production
- عبر `.github/workflows/railway_deploy.yml` و
  `.github/workflows/railway_deploy_frontend.yml` (يدوي فقط).
- يمر عبر `preDeployCommand` (`scripts/railway_predeploy.sh`) الذي:
  1. يفحص Alembic head (`scripts/check_alembic_single_head.py`).
  2. يفحص env contract (`make env-check`).
  3. يفحص security smoke (`make security-smoke`).
- بعد النشر: `scripts/post_redeploy_verify_dealix.py` يفحص:
  - `/healthz` رجع 200 خلال 60 ثانية.
  - `/api/v1/founder/launch-status` رجع `READY` أو `READY_WITH_FLAG`.
  - DLQ فارغ.
  - workflow_daily jobs لم تفشل.

## 5. القفل المتبادل (Mutual Lockout)

- لا يمكن لـ workflow واحد أن ينشر إلى staging و production في نفس
  التشغيل. كل workflow له `environment` منفصل.
- `concurrency` group يُلغى النشر القديم تلقائياً لو بدأ نشر جديد
  (cancel-in-progress: true في معظم workflows).

## 6. الاختبارات

- **كل اختبار** (CI, integration, governance) يجب أن ينجح على staging
  قبل أن يُسمح بنشر production.
- `bash scripts/dealix_local_stack_verify.sh --skip-docker` يجب أن ينجح
  محلياً قبل الـ PR.

## 7. ترقية staging → production

1. **freeze window:** لا ينشر إنتاج يوم الجمعة بعد 16:00 (الرياض) أو
   في عطلات نهاية الأسبوع. (See `docs/LAUNCH_GATES.md`.)
2. **PR promotion:** merge من `release/staging` إلى `main` يفتح PR
   تلقائي للإنتاج.
3. **manual approval:** المؤسس يوافق على deploy في GitHub Environment
   `production`.
4. **verify:** `scripts/founder_production_smoke.sh` بعد النشر.
5. **window:** إذا فشل أي verify، rollback فوري عبر
   `scripts/railway_redeploy_checklist.py --rollback`.

## 8. المراجع

- `docs/infra/ENVIRONMENT_POLICY_AR.md` — سياسة البيئات الكاملة
- `docs/STAGING_DEPLOYMENT.md` — staging deploy
- `docs/RAILWAY_DEPLOY_GUIDE_AR.md` — Railway production deploy
- `docs/ops/BACKUP_RESTORE.md` — backup tiers
- `docs/LAUNCH_GATES.md` — launch gates
- `scripts/railway_predeploy.sh` — pre-deploy checks
- `scripts/post_redeploy_verify_dealix.py` — post-deploy verify
