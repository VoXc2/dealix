# Dealix — Founder A-to-Z Launch Runbook

هذا المستند هو مسار التشغيل النهائي من source truth إلى إنتاج مستقر. الهدف: أي فشل Railway/GitHub يكون قابلًا للعزل بدون تخمين، وأي إطلاق يثبت **الخدمة الكنسية + exact SHA + provider config + health + public truth** قبل تغيير النطاق.

## 0) قاعدة التشغيل

- GitHub `Dealix-sa/dealix` هو source authority للكود.
- `dealix/config/railway_services.json` هو service/authority contract.
- لا تحفظ أسرار حقيقية داخل الريبو أو issue/chat/log.
- لا تستخدم `NEXT_PUBLIC_*` لأي Admin/API private key.
- API فقط هو الذي يشغل migrations/predeploy.
- `dealix-apps-web` هو الواجهة العامة الكنسية؛ `frontend/` Legacy compatibility فقط.
- اسم Railway service مثل `web` لا يثبت الهوية.
- لا Deploy/Redeploy/DNS/Domain/Secret mutation من مرحلة التشخيص.

## 1) خريطة الخدمات الكنسية

| الخدمة | Role | Authority | Root Directory | Dockerfile | Repository config | Provider Config File | Healthcheck |
|---|---|---:|---|---|---|---|---|
| `dealix-api` | `canonical_api` | `true` | `.` | `Dockerfile` | `railway.json` | provider evidence required | `/healthz` |
| `dealix-apps-web` | `canonical_public_web` | `true` | `apps/web` | `Dockerfile` | `apps/web/railway.toml` | `/apps/web/railway.toml` | `/healthz` |

Compatibility only:

| الخدمة | Role | Authority | Root Directory |
|---|---|---:|---|
| `dealix-frontend` | `legacy_public_web` | `false` | `frontend` |

**قاعدة front-door:** لا تربط `dealix.me`/`www` إلا بعد إثبات أن Railway candidate = `dealix-apps-web`, repo=`Dealix-sa/dealix`, root=`apps/web`, provider Config File=`/apps/web/railway.toml`, exact deployment/source SHA مقبول.

**قاعدة pre-deploy:** repo-root `/railway.toml` ليس Config File للويب؛ قد يحتوي backend/API pre-deploy. إذا كان effective provider Config File للـweb = `/railway.toml` فالحالة HOLD ولا تعالجها بحذف backend migration من الجذر. أصلح Config File للخدمة المرشحة فقط بعد source acceptance وإجراء إنتاجي محدد.

## 2) متغيرات الإنتاج

### API

```text
APP_ENV=production
APP_SECRET_KEY=<strong server-side secret>
JWT_SECRET_KEY=<strong server-side secret>
API_KEYS=<private service keys>
ADMIN_API_KEYS=<admin-only keys>
```

حسب runtime الفعلي:

```text
DATABASE_URL=<Railway Postgres URL>
REDIS_URL=<Railway Redis URL>
SENTRY_DSN=<optional>
OPENAI_API_KEY=<optional provider>
ANTHROPIC_API_KEY=<optional provider>
GROQ_API_KEY=<optional provider>
GOOGLE_API_KEY=<optional provider>
```

### Canonical web — `dealix-apps-web`

```text
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
```

`apps/web` لا يحتاج Admin key في browser config. `/api/v1/*` proxying/rewrite يبقى بدون public admin credential.

### Legacy frontend

أي `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY` / `DEALIX_OPS_PROXY_SECRET` تخص legacy compatibility فقط إذا كان proxy المقابل مثبتًا على exact legacy SHA؛ لا تنقل هذا العقد إلى `apps/web` تلقائيًا.

## 3) قبل أي production action

### 3.1 Reconcile source

```bash
git fetch origin main --prune
git rev-parse HEAD
git rev-parse origin/main
python scripts/verify_railway_surfaces.py
```

أي mismatch في الـSHA = HOLD حتى تفهم السبب.

### 3.2 Canonical web acceptance

```bash
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

### 3.3 API acceptance عند الحاجة

```bash
docker build -t dealix-api .
```

لا تجعل build `frontend/` legacy شرطًا للإطلاق الكنسي.

## 4) Railway read-only identity packet

قبل إصلاح أي service أو إعادة نشر، سجّل:

1. project/environment.
2. exact service name/id.
3. source repo.
4. branch/ref.
5. Root Directory.
6. effective Provider Config File.
7. deployment ID/status/source SHA/failure stage.
8. generated domain.
9. healthcheck path/status.
10. custom-domain/certificate state.

لـpublic web يجب أن يثبت packet:

```text
service=dealix-apps-web
role=canonical_public_web
productionAuthority=true
repo=Dealix-sa/dealix
root=apps/web
config_file=/apps/web/railway.toml
healthcheck=/healthz
```

إذا لم يثبت ذلك: `UNKNOWN_NOT_EVIDENCE_BACKED` / HOLD.

## 5) إذا ظهر Build failed / Deploy failed

لا تستخدم عنوان البريد كroot cause.

افصل المراحل:

- snapshot/source checkout.
- dependency/install.
- compile/type/build.
- image export/push.
- pre-deploy.
- container start.
- healthcheck.
- routing/domain.

إذا نجح build/image ثم فشل deploy، لا تعدّل dependencies عشوائيًا. اقرأ provider metadata لتحديد `failureStage`. وإذا كان `PRE_DEPLOY_COMMAND` افحص effective Config File أولًا؛ web يجب ألا يرث backend/API pre-deploy من `/railway.toml`.

صنّف فقط:

- legacy/wrong service.
- wrong repo/ref/root.
- wrong provider config file.
- dependency/install.
- compile/typecheck/build.
- pre-deploy.
- startup/port/healthcheck.
- provider/control-plane.

لا redeploy قبل تحديد أي فئة تنطبق.

## 6) Runtime proof قبل domain cutover

على Railway-generated domain للـ`dealix-apps-web` candidate:

- root = 2xx.
- `/healthz` = 200.
- `/ar` = 2xx/3xx.
- canonical CTA/public truth صحيح.
- deployment/source SHA مثبت.
- provider receipt يثبت Config File `/apps/web/railway.toml`.

وعلى API:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
```

لا تستخدم reachability على `dealix.me` الحالية كدليل أن candidate Railway web صحيح قبل cutover.

## 7) DNS/custom domain packet — بدون تنفيذ

اقرأ من Railway نفسه:

- exact `dnsRecords` لكل `dealix.me` و`www`.
- TXT `verificationToken` إن وجد.
- certificate state.
- target port/domain.

وسجّل DNS الحالي:

- apex.
- `www`.
- `api`.
- TTL.
- rollback values.

لا تخمن CNAME/A/TXT ولا تغير `api.dealix.me` إذا كان API سليمًا. لا تفعّل DNSSEC في نفس حركة cutover.

## 8) Production/DNS execution — L5 action packet مستقل

فقط بعد exact approval على:

- service/deployment SHA.
- effective Provider Config File.
- before/after DNS diff.
- exact Railway records.
- rollback.
- smoke plan.

نفذ أقل تغيير ممكن على web candidate ثم apex/`www` حسب الحاجة. لا تلمس API/Postgres كجزء من تصحيح الويب إذا لم يثبت blocker مستقل.

## 9) Acceptance بعد cutover

```bash
curl -fsSIL --max-time 20 https://dealix.me/
curl -fsSIL --max-time 20 https://dealix.me/ar
curl -fsS --max-time 20 https://dealix.me/healthz
curl -fsS --max-time 20 https://api.dealix.me/health
curl -fsS --max-time 20 https://api.dealix.me/healthz
python scripts/railway_frontend_dns_gate.py
python scripts/railway_production_identity_gate.py
python scripts/verify_frontend_railway_dns.py
python scripts/production_layers_verify.py --strict --write-cache
```

PASS يحتاج:

- `dealix.me` ليس GitHub Pages/Legacy.
- public web = `dealix-apps-web` exact accepted SHA.
- provider Config File = `/apps/web/railway.toml`.
- root و`/ar` و`/healthz` صحيحة.
- API healthy وعلى accepted release contract.
- TLS صحيح.
- no CORS regression.
- no browser-exposed secret.
- public commercial truth صحيح.
- ثلاثة probes متتالية Green.

## 10) الأعطال الشائعة

| العرض | التصنيف الصحيح | Safe next action |
|---|---|---|
| `Build failed` لخدمة اسمها `web` | identity غير مثبتة | اقرأ repo/root/SHA/config أولًا؛ لا تفترض canonical web |
| legacy `frontend` build failed | legacy incident | لا تصلحه كـlaunch blocker إلا إذا evidence يثبت dependency حقيقية |
| canonical web build/image pass ثم `PRE_DEPLOY_COMMAND` fail | provider config/predeploy incident | أثبت effective Config File؛ `/railway.toml` للويب = HOLD |
| `dealix-apps-web` build failed | canonical source/build incident | first causal log + exact SHA ثم bounded source repair |
| build pass / deploy fail | predeploy/startup/health/env | افصل build logs عن deploy logs؛ لا تعطل secret guards |
| `/ar` 3xx | قد يكون صحيحًا | canonical config يسمح redirect؛ تحقق destination/public truth |
| `dealix.me` ما زال GitHub Pages/Legacy | front-door not cut over | حضّر exact Railway domain/DNS packet؛ لا تخمن records |
| API health fail | API incident مستقل | لا تحرك frontend DNS كعلاج تلقائي |

## 11) Definition of Done

لا يكفي `FOUNDER_LAUNCH_FINAL_CHECK=ok` منفردًا. الإطلاق النهائي يحتاج evidence bundle يثبت:

- canonical service identities.
- exact source/deployed SHAs.
- effective provider Config File لكل خدمة كنسية.
- source builds/verifiers.
- Railway runtime health.
- DNS/TLS/front-door ownership.
- draft-only/external-send safety status.
- public commercial truth.
- rollback receipt.

المسار التالي بعد Production Green هو controlled commercial launch، وليس فتح mass outbound أو self-serve pricing تلقائيًا.
