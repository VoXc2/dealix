# خطة استجابة فشل Railway — Dealix

هذه الخطة تختصر التعامل مع تنبيهات `Build failed` و`Deploy failed` بدون تخمين أو إصلاح الخدمة الخطأ.

## 1) ابدأ بهوية الخدمة لا باسمها الظاهر فقط

المرجع الكنسي: `dealix/config/railway_services.json`.

- `dealix-api`: `role=canonical_api`, `productionAuthority=true`, root=`.`.
- `dealix-apps-web`: `role=canonical_public_web`, `productionAuthority=true`, root=`apps/web`, provider Config File=`/apps/web/railway.toml`.
- `dealix-frontend`: `role=legacy_public_web`, `productionAuthority=false`, root=`frontend`.

أي تنبيه يذكر `Service: web` أو اسمًا عامًا آخر **لا يثبت** أنه فشل الواجهة الكنسية. قبل التصنيف سجّل read-only:

1. project/environment.
2. exact Railway service/id.
3. source repository.
4. branch/ref.
5. Root Directory.
6. effective Provider Config File.
7. deployment ID/status/source SHA/failure stage.
8. generated domain/healthcheck.

إذا ظهر repo آخر، أو root=`frontend`, أو SHA غير معروف، أو web Config File=`/railway.toml`، فالحالة HOLD إلى أن يثبت العكس. لا تنفذ redeploy/rollback/source/config change من إشعار البريد وحده.

## 2) إعدادات الخدمات الكنسية

### API — `dealix-api`

- Root Directory: repo root
- Builder: Dockerfile
- Dockerfile path داخل service root: `Dockerfile`
- Healthcheck: `/healthz`
- Production Authority: `true`
- Required production variables:
  - `APP_ENV=production`
  - `APP_SECRET_KEY`
  - `JWT_SECRET_KEY`
  - `API_KEYS`
  - `ADMIN_API_KEYS`
  - `DATABASE_URL` عند استخدام Postgres

### Canonical web — `dealix-apps-web`

- Role: `canonical_public_web`
- Production Authority: `true`
- Source repo: `Dealix-sa/dealix`
- Root Directory: `apps/web`
- Dockerfile path داخل service root: `Dockerfile`
- Repository Railway config: `apps/web/railway.toml`
- Effective provider Config File: `/apps/web/railway.toml`
- Pre-deploy: **none** for canonical web
- Healthcheck: `/healthz`
- Runtime port: `3000`
- Browser-safe env only:
  - `NEXT_PUBLIC_API_URL=https://api.dealix.me`
  - `NEXT_PUBLIC_SITE_URL=https://dealix.me`

لا تضف Admin/API private key داخل `NEXT_PUBLIC_*`.

**مهم:** repo-root `/railway.toml` قد يحمل backend/API `preDeployCommand`. لا تستخدمه كConfig File للويب ولا تحذف backend migration منه كحل لفشل web. أصلح فقط provider Config File للخدمة المرشحة بعد exact-head source acceptance وإجراء إنتاجي منفصل.

### Legacy web — `dealix-frontend`

- Role: `legacy_public_web`
- Production Authority: `false`
- Root Directory: `frontend`

قد يبقى buildable لأسباب compatibility، لكن **لا يصلح تلقائيًا كهدف `dealix.me`** ولا يجب إصلاحه قبل إثبات أن المشكلة تخصه فعلًا.

## 3) فحوصات source قبل أي production action

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

API عند الحاجة:

```bash
docker build -t dealix-api .
```

لا تجعل legacy `frontend/` build شرطًا لـcanonical web acceptance.

## 4) فحوصات runtime read-only

API:

```bash
curl -fsS https://api.dealix.me/healthz
curl -fsS https://api.dealix.me/ready
curl -fsS 'https://api.dealix.me/healthz?deep=1'
```

Public web بعد إثبات service identity:

```bash
curl -fsSIL https://dealix.me/
curl -fsSIL https://dealix.me/ar
curl -fsS https://dealix.me/healthz
```

قبل custom-domain/DNS cutover اختبر generated domain الخاص بـ`dealix-apps-web` نفسه على root و`/healthz` و`/ar`، واربط النتيجة بالـdeployment/source SHA وبـprovider Config File `/apps/web/railway.toml`.

HTTP reachable وحده لا يثبت service identity.

## 5) عند استمرار الفشل

استخرج **أول causal error حقيقي** من build/deploy logs، لا عنوان الإيميل فقط. افصل المراحل:

- source/snapshot.
- install/dependency.
- compile/typecheck/build.
- image export/push.
- pre-deploy.
- container start.
- port/healthcheck.
- routing/domain.

صنّفه إلى أحد الآتي:

- wrong service identity / legacy service.
- wrong repository or branch.
- wrong Root Directory.
- wrong effective Provider Config File.
- Dockerfile/Railway config mismatch.
- dependency/install failure.
- Next.js compile/type failure.
- pre-deploy failure.
- missing runtime env/startup secret.
- healthcheck failure بعد build success.
- provider/control-plane failure.

إذا كان build/image PASS ثم failureStage=`PRE_DEPLOY_COMMAND` والـweb effective config=`/railway.toml`، فالمشكلة المثبتة هي **wrong-layer config/pre-deploy contract**. لا تدّعِ shell subfailure أدق إذا provider logs لا تثبته.

لا تعالج الاحتمالات كلها دفعة واحدة؛ اربط كل إصلاح بالدليل الأول وexact SHA.

## 6) custom domain / DNS

لا تخمن CNAME/A/TXT.

قبل أي تغيير احفظ:

- Railway exact `dnsRecords`.
- TXT `verificationToken` إن وجد.
- certificate/custom-domain state.
- current apex/www/api DNS + TTL.
- rollback values.

ثم فقط بعد action-specific L5 approval يمكن تغيير apex/www. لا تغيّر `api.dealix.me` إذا كان API سليمًا، ولا تفعل DNSSEC في نفس cutover.

## 7) سياسة حماية الإنتاج

- لا تتجاوز production secret validation.
- API فقط يشغّل migrations عند readiness مثبتة وauthority مناسب.
- web لا يشغّل API predeploy migration.
- provider receipt للويب يجب أن يثبت `/apps/web/railway.toml`.
- أبقِ healthcheck سريعًا على `/healthz`.
- أي deployment fix يجب أن يمر `scripts/verify_railway_surfaces.py` + exact-source acceptance.
- أي service identity أو config file غير مثبت = `UNKNOWN_NOT_EVIDENCE_BACKED`.
- لا Deploy/Redeploy/Rollback/Domain/DNS/Secret mutation من runbook التشخيص نفسه.
