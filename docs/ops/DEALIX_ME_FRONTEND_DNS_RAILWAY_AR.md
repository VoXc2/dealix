# DNS dealix.me → Railway Frontend (Next.js)

> تحديث أمني: 2026-08-26. هذه الحزمة للتحضير والتحقق فقط. تغيير DNS أو Railway production/domain يبقى إجراء L5 ويتطلب موافقة صريحة عند التنفيذ.

## الهدف

`https://dealix.me/ar` يجب أن يصل إلى Railway Frontend (Next.js) ويعيد استجابة صحيحة، مع بقاء `https://api.dealix.me` على Railway API.

لا تعتمد على حالة تاريخية للمجال. قبل أي cutover، أعد التحقق من DNS الحالي، Railway custom-domain target، root، `/ar`، CTA، API/CORS ومسار rollback.

---

## 1) عقد الأسرار — إلزامي

ممنوع وضع أي مفتاح admin في متغير `NEXT_PUBLIC_*` لأن هذه المتغيرات قد تُضمَّن في bundle المتصفح.

**ممنوع:**

```text
NEXT_PUBLIC_DEALIX_ADMIN_API_KEY=...
```

الحد الأدنى للـfrontend:

```text
NEXT_PUBLIC_API_URL=https://api.dealix.me
NEXT_PUBLIC_SITE_URL=https://dealix.me
NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1
DEALIX_ADMIN_API_KEY=<server-side only>
DEALIX_API_KEY=<server-side only>
```

`DEALIX_ADMIN_API_KEY` و`DEALIX_API_KEY` يظلان server-side في Railway Frontend ويستخدمهما `/api/dealix-proxy/...`. لا تطبع قيمهما ولا تنسخهما إلى ملفات عامة أو browser env.

قبل أي نشر:

```bash
python scripts/sync_railway_generated_env.py --dry-run
python scripts/validate_railway_generated_env.py --from-railway-env
python scripts/check_env_contract.py
```

`sync_railway_generated_env.py` يجب أن يزيل أي `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` قديم وأن يحافظ على فصل service/admin credentials.

---

## 2) Railway Frontend — تحقق قبل التنفيذ

| الإعداد | القيمة المطلوبة |
|---|---|
| Root directory | `frontend` |
| Public API URL | `https://api.dealix.me` |
| Site URL | `https://dealix.me` |
| Ops proxy | `NEXT_PUBLIC_USE_DEALIX_OPS_PROXY=1` |
| Admin credential | server-side only |
| Service credential | server-side only |
| Custom domains | `dealix.me`, `www.dealix.me` بعد موافقة L5 |

لا تنفذ Deploy أو Redeploy أو domain attach من هذا runbook تلقائيًا. أولًا أثبت أن Railway frontend المرشح على نفس commit المطلوب ينجح على رابط Railway المؤقت/custom-domain candidate.

---

## 3) Pre-cutover proof packet

سجّل دون أسرار:

1. GitHub current main SHA.
2. Railway frontend deployment/commit SHA المرشح.
3. HTTP status لـ Railway frontend root و`/ar`.
4. CTA الأساسي موجود ويشير إلى المسار التجاري الحالي.
5. `NEXT_PUBLIC_API_URL=https://api.dealix.me`.
6. API `/health` و`/healthz` ناجحان.
7. CORS يسمح بـ`https://dealix.me` و`https://www.dealix.me` عند الحاجة.
8. DNS الحالي لـ apex و`www` مسجل كـbefore-state.
9. Railway يعرض **القيم الدقيقة** المطلوبة لكل custom domain؛ لا تفترض أن الهدف `<project>.up.railway.app` قبل قراءته من Railway.
10. rollback records معروفة ومكتوبة قبل cutover.

إذا أي بند UNKNOWN أو FAIL، يكون القرار HOLD.

---

## 4) DNS cutover — L5 فقط

بعد موافقة صريحة فقط:

- عدّل **فقط** سجلات `dealix.me`/`www` المطلوبة للـRailway frontend.
- استخدم القيم الدقيقة التي يعرضها Railway Custom Domains.
- لا تغيّر `api.dealix.me` إذا كان API الحالي سليمًا.
- لا تحذف سجلات غير مرتبطة.
- احتفظ بالـbefore-state للrollback.

لا يوجد في هذا المستند إذن ضمني للنشر، أو DNS mutation، أو billing/plan change.

---

## 5) Acceptance بعد cutover

```bash
curl -fsSIL --max-time 20 https://dealix.me/
curl -fsSIL --max-time 20 https://dealix.me/ar
curl -fsS --max-time 20 https://api.dealix.me/health
curl -fsS --max-time 20 https://api.dealix.me/healthz
python scripts/verify_frontend_railway_dns.py
python scripts/production_layers_verify.py --from-railway-env --strict --write-cache
```

PASS يحتاج على الأقل:

- root و`/ar` يعملان عبر Railway frontend.
- TLS صالح.
- الصفحة ليست GitHub Pages القديمة.
- CTA والمسار التجاري صحيحان.
- API health سليم.
- لا CORS regression.
- لا secret ظاهر في browser bundle/config.

---

## 6) Rollback

إذا فشل TLS أو root أو `/ar` أو API integration أو CTA بعد cutover:

1. أعد سجلات DNS إلى before-state المسجل.
2. لا تغيّر API أو database كجزء من rollback إلا إذا كان هناك دليل مستقل وموافقة منفصلة.
3. أعد acceptance checks وسجل النتيجة في Proof Ledger.

---

## مراجع canonical

- `scripts/sync_railway_generated_env.py`
- `scripts/validate_railway_generated_env.py`
- `scripts/check_env_contract.py`
- `scripts/railway_frontend_dns_gate.py`
- `scripts/verify_frontend_railway_dns.py`
- `frontend/src/app/api/dealix-proxy/[...path]/route.ts`

*آخر تحديث: 2026-08-26*
