# DNS dealix.me → Railway Canonical Apps Web

> تحديث تشغيلي/أمني: 2026-09-05. هذا runbook للتحضير والتحقق فقط. Deploy/Redeploy أو domain/DNS أو secrets أو API/Postgres يبقى إجراء مادي مستقل. تحديث هذا المستند ليس نشرًا أو قبولًا تشغيليًا.

## 0) سلطة الواجهة الكنسية

المالك الكنسي للواجهة العامة في Dealix هو:

- Service contract: `dealix-apps-web`
- Role: `canonical_public_web`
- Source repository: `Dealix-sa/dealix`
- Root directory: `apps/web`
- Dockerfile: `apps/web/Dockerfile`؛ وداخل build root يظهر `Dockerfile`
- Repository config: `apps/web/railway.toml`
- **Expected provider Config File: `/apps/web/railway.toml`**
- Pre-deploy: **none** للويب الكنسي
- Healthcheck: `/healthz`
- Expected runtime port: `3000`
- Public domains after proof: `dealix.me`, `www.dealix.me`

`frontend/` هو Legacy/compatibility فقط و`productionAuthority=false`. اسم Railway service مثل `web` ليس بحد ذاته الهوية الكنسية؛ provider receipt يجب أن يثبت repo/root/config/deployment SHA والدومينات.

المرجع الآلي الأعلى هو `dealix/config/railway_services.json`. يجب أن يمر `python scripts/verify_railway_surfaces.py` قبل أي packet إنتاجي.

---

## 1) Live Railway provider truth — 2026-09-05

المشروع:

```text
project=Dealix
project_id=03e6bb4b-bdf5-4aa7-86ed-bc94fa293c0e
environment=production
environment_id=38e3d38f-53b2-44fa-a3f9-ef91d863bd83
```

### 1.1 Current `web` service

```text
service_name=web
service_id=8a640431-abc0-443f-848d-d968fbff147e
source_repo=Dealix-sa/dealix
branch=main
root_directory=apps/web
generated_domain=web-production-380c3.up.railway.app
custom_domains=dealix.me,www.dealix.me
current_effective_config_file=/apps/web/railway.toml
expected_canonical_config_file=/apps/web/railway.toml
```

Source repo/root/provider Config File أصبحت **canonical at the provider configuration layer**. لا تكرر Config File mutation؛ defect الاختيار السابق مغلق في الإعداد الحالي.

### 1.2 Active web deployment

```text
deployment_id=37e0a3ee-234c-45cc-bbd3-fb364d6fffa5
status=SUCCESS
deployment_sha=ad90255264183a7547b865e41be4e719306c0d76
```

هذا النشر active لكنه **stale** بالنسبة إلى current `main=7274c766dd43a23ec391b4cfbeb4fae8ae665763`. تصحيح Config File لم ينشئ deployment جديدًا، لذلك لا يثبت أن الواجهة الحالية تعمل بعقد TOML الصحيح.

### 1.3 Historical exact-main web deployment failure قبل تصحيح Config File

```text
deployment_id=00df1045-233e-4e1f-8623-9ee1fbe596fd
source_sha=7274c766dd43a23ec391b4cfbeb4fae8ae665763
status=FAILED
failure_stage=PRE_DEPLOY_COMMAND
failure_error=Pre-deploy command failed
effective_config_file_at_failure=/railway.toml
```

Provider logs/evidence prove أن snapshot/source checkout وDocker build و`npm ci` وNext.js compile/type/lint و`117/117` static pages وimage export/push نجحت قبل الفشل. **Build ليس blocker الحالي.**

Provider logs لم تحفظ shell-level stdout/stderr كافيًا لتحديد الأمر الداخلي الدقيق؛ لذلك:

```text
EXACT_SHELL_SUBFAILURE=UNKNOWN_NOT_EVIDENCE_BACKED
```

لا تدّعِ سببًا أدق من ذلك.

### 1.4 Config-selection incident classification

repo-root `/railway.toml` ينتمي لعقد backend/API وقد يحمل `preDeployCommand`. الويب الكنسي يجب أن يستخدم `/apps/web/railway.toml` الذي لا يحتوي API/DB pre-deploy.

الحالة الحالية:

```text
CONFIG_SELECTION_DEFECT=CORRECTED
CURRENT_PROVIDER_CONFIG_FILE=/apps/web/railway.toml
REDEPLOY_AFTER_CORRECTION=NOT_DONE
EXACT_ACCEPTED_RELEASE_DEPLOYED=NOT_PROVEN
PRODUCTION_SHA_PARITY=FAIL
```

لا تعالج الحادثة الآن بحذف backend/API migration من `/railway.toml` ولا بإعادة تعديل Config File. الخطوة التالية بعد acceptance هي **redeploy exact accepted release باستخدام Config File الحالي الصحيح**.

### 1.5 API truth

الخدمة الحالية:

```text
service_name=dealix
service_id=67be1b8c-b823-490a-a317-b3c3fbf44658
source_repo=Dealix-sa/dealix
branch=main
custom_domain=api.dealix.me
target_port=8080
active_deployment=f78114e8-0888-440c-831e-5a909842f693
active_sha=678f657897eecfb9cbcd74fbeb0e67ccd09068ee
status=SUCCESS
```

الـSHA كذلك stale بالنسبة إلى current main. لا تغير API أو Postgres ضمن إصلاح الويب ما لم يظهر blocker مستقل مثبت.

---

## 2) Source acceptance قبل أي Railway deploy/redeploy

على **exact #1497 head**:

```bash
python scripts/verify_railway_surfaces.py
python -m py_compile \
  scripts/verify_railway_surfaces.py \
  scripts/railway_frontend_dns_gate.py \
  scripts/railway_production_identity_gate.py
pytest -q \
  tests/test_railway_web_config_contract.py \
  tests/test_railway_frontend_dns_gate_truth.py \
  tests/test_railway_production_identity_gate_truth.py \
  tests/test_production_ops_gates.py
cd apps/web
npm ci
npm run typecheck
npm run build
cd ../..
```

PASS هنا يثبت source contract فقط. لا يثبت live provider deployment.

Hosted CI الأحمر لا يُعتبر code failure إذا كانت الوظائف `steps=[]` و`runner_id=0`; يجب استخدام exact-head sovereign/VPS acceptance في هذه الحالة بدل false PASS أو false FAIL.

---

## 3) Provider-bound receipt المطلوب للويب

قبل Production Green يجب أن يثبت receipt جديدًا دون أسرار:

```text
schema=dealix.railway-frontdoor-evidence.v1
provider=railway
project_id=03e6bb4b-bdf5-4aa7-86ed-bc94fa293c0e
environment_id=38e3d38f-53b2-44fa-a3f9-ef91d863bd83
environment_name=production
service=dealix-apps-web
role=canonical_public_web
repository=Dealix-sa/dealix
root_directory=apps/web
config_file=/apps/web/railway.toml
deployment_sha=<exact accepted release SHA>
deployment_status=SUCCESS
service_id=<provider id>
deployment_id=<provider id>
captured_at=<fresh UTC timestamp>
```

ويجب أن يحتوي domain evidence لكل من `dealix.me` و`www.dealix.me`:

```text
routing_verified=true
ownership_verified=true
certificate_verified=true
```

HTTP 200 أو Config File الصحيح وحدهما لا يثبت هذا receipt.

---

## 4) أسرار ومتغيرات الويب

ممنوع وضع أي Admin/API private key داخل `NEXT_PUBLIC_*`.

ممنوع:

```text
NEXT_PUBLIC_DEALIX_ADMIN_API_KEY=...
```

المفتاح الإداري يبقى على السيرفر فقط:

```text
DEALIX_ADMIN_API_KEY=<server-side only>
NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1
```

الحد الأدنى:

```text
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
```

لا تنسخ أسرار API/DB/payment إلى خدمة الويب لمجرد وجودها في المشروع.

secret mutation منفصل عن redeploy ولا يدخل تلقائيًا في نفس action packet.

---

## 5) Minimal production action packet — غير منفذ

بعد exact-head source acceptance والمراجعة المستقلة فقط:

1. التقط before-state جديدًا لخدمة `web`: source/root/config/deployment/domain/certificate metadata دون أسرار.
2. اثبت accepted release SHA الذي سيتم نشره؛ moving `main` ليس بديلًا عن SHA محدد.
3. **لا تغيّر Config File**؛ هو صحيح حاليًا `/apps/web/railway.toml`.
4. Redeploy/deploy الخدمة `web` على **نفس exact accepted release** باستخدام إعدادها الحالي.
5. لا تلمس API/Postgres/DB/DNS/secrets في هذه الحركة.
6. اختبر generated domain أولًا قبل اعتبار apex/www ناجحين.
7. إذا فشل redeploy، ارجع إلى before-state/deployment السابق حسب rollback packet؛ لا توسع التغيير تلقائيًا.

هذا المستند لا يمنح التنفيذ المادي نفسه.

---

## 6) Generated-domain acceptance قبل public declaration

على candidate الجديد:

- provider deployment status = `SUCCESS`.
- provider Config File = `/apps/web/railway.toml`.
- source/deployment SHA = accepted release SHA.
- generated-domain `/` = 2xx.
- generated-domain `/healthz` = 200.
- generated-domain `/ar` = 2xx/3xx إلى canonical destination.
- CTA/public commercial truth صحيح.
- no browser-secret leakage.
- web receipt صالح وحديث.

إذا أي بند غير مثبت: HOLD.

---

## 7) API + same-release production gate

`Production Green` يتطلب web وAPI provider receipts صالحين، وعلى نفس accepted release SHA حسب عقد #1497 الحالي، مع API `/healthz` ناجح.

إذا API public health يفشل أو API SHA لا يطابق accepted release contract، لا تعتبر نجاح web وحده Production Green.

---

## 8) Public Truth قبل الإعلان العام

حتى بعد نجاح runtime، يجب التحقق من:

- `dealix.me/` و`/ar` على الواجهة الكنسية.
- `academy.html` لم يعد ينشر الأسعار/الشهادات/ادعاءات العملاء القديمة.
- `customer-portal.html` لم يعد يعرض legacy demo/KPI/approval/outbound surfaces كحقيقة عامة.
- لا synthetic/demo evidence يُعرض كcustomer proof.
- لا fixed public price أو checkout authority غير معتمد.

#1496 هو المالك المحدود لإغلاق legacy Public Truth؛ لا توسع إصلاح Railway إلى إعادة كتابة تلك الأسطح من مسار آخر.

---

## 9) DNS/custom domain packet

لا تخمن CNAME/A/TXT.

قبل أي تغيير public routing احفظ:

- Railway exact domain/routing records إذا كان المزود يعرضها.
- ownership verification state.
- certificate state.
- current apex/www/api DNS + TTL.
- rollback values.

قد لا تحتاج DNS mutation إذا custom domains الحالية ظلت مرتبطة بالخدمة الصحيحة بعد redeploy؛ أثبت ذلك أولًا. لا تغير `api.dealix.me` ضمن إصلاح الويب إلا إذا كان هناك incident مستقل.

---

## 10) Post-redeploy / post-cutover acceptance

```bash
curl -fsSIL --max-time 20 https://dealix.me/
curl -fsSIL --max-time 20 https://dealix.me/ar
curl -fsS --max-time 20 https://dealix.me/healthz
curl -fsS --max-time 20 https://api.dealix.me/health
curl -fsS --max-time 20 https://api.dealix.me/healthz
python scripts/railway_frontend_dns_gate.py \
  --provider-receipt <fresh-web-receipt.json> \
  --accepted-sha <accepted-sha>
python scripts/railway_production_identity_gate.py \
  --web-provider-receipt <fresh-web-receipt.json> \
  --api-provider-receipt <fresh-api-receipt.json> \
  --accepted-sha <accepted-sha>
```

PASS يحتاج:

- canonical web exact accepted SHA.
- provider Config File `/apps/web/railway.toml`.
- API accepted-release receipt + health.
- routing/ownership/TLS evidence.
- no legacy server signal.
- no browser-exposed secret.
- Public Truth closure.
- rollback receipt.

---

## 11) Rollback

إذا فشل exact-release redeploy أو generated-domain acceptance أو public routing:

1. استخدم before-state المسجل فقط.
2. أعد deployment/service state حسب rollback packet المصرح.
3. لا تغيّر Config File مرة أخرى إلا إذا أثبتت الأدلة أنه سبب جديد؛ الحالة الحالية صحيحة.
4. لا تغيّر API/database/secrets كجزء من rollback إلا بدليل مستقل.
5. أعد probes وسجل النتيجة في Proof Ledger/#1476/#1497.

---

## 12) مراجع canonical

- `dealix/config/railway_services.json`
- `apps/web/railway.toml`
- `apps/web/Dockerfile`
- `scripts/verify_railway_surfaces.py`
- `scripts/railway_frontend_dns_gate.py`
- `scripts/railway_production_identity_gate.py`
- `tests/test_railway_web_config_contract.py`
- `tests/test_railway_frontend_dns_gate_truth.py`
- `tests/test_railway_production_identity_gate_truth.py`
- `docs/ops/RAILWAY_SERVICE_ENV_MATRIX_AR.md`
- `docs/ops/RAILWAY_FAILURE_RESPONSE_AR.md`
- `docs/ops/FOUNDER_A_TO_Z_LAUNCH_RUNBOOK_AR.md`

Legacy references لا تملك production authority:

- `frontend/`
- `frontend/railway.json`
- repo-root `/railway.toml` كConfig File للويب

*آخر تحديث: 2026-09-05 — provider Config File corrected live; exact accepted release redeploy still pending; production mutation not executed by this runbook.*
