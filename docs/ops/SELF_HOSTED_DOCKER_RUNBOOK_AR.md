# Dealix — Canonical Self-Hosted Runbook

> CURRENT_ONLY. المسار الوحيد المسموح للنشر الذاتي هو `deploy/selfhost/compose.yml`.
> `docker-compose.prod.yml` و`scripts/server_{deploy,healthcheck,backup}.sh` مداخل تاريخية متوقفة وتفشل مغلقًا.

## قانون السلطة

- GitHub = source/review/proof.
- VPS = build/runtime plane.
- `deploy/selfhost/compose.yml` = Compose authority الوحيد.
- أي canary يبقى على loopback ولا يفتح 80/443.
- HTTP 200 لا يثبت Production Green؛ يجب تطابق SHA للـWeb والـAPI.
- DNS/DB/secrets/public ingress/provider decommission = L5 action-bound فقط.

## فحص المصدر

```bash
python scripts/ops/verify_selfhosted_production_plane.py
```

يجب أن ينتهي بـ `SELFHOST_VERIFY=PASS`.

## Canary خاص ومعزول

```bash
SHA=$(git rev-parse HEAD)
DEALIX_EXPECTED_SHA="$SHA" \
DEALIX_SELFHOST_API_PORT=18001 \
DEALIX_SELFHOST_WEB_PORT=13001 \
DEALIX_SELFHOST_LOCAL_DB=1 \
bash scripts/ops/deploy_selfhosted_canary.sh
```

استخدم منافذ loopback مختلفة إذا كان هناك canary آخر؛ لا توقف canary سليمًا فقط لتحرير منفذ.

## Canary للـingress بدون نشر عام

```bash
DEALIX_EXPECTED_SHA="$SHA" \
DEALIX_SELFHOST_API_PORT=18001 \
DEALIX_SELFHOST_WEB_PORT=13001 \
DEALIX_SELFHOST_INGRESS_PORT=18081 \
bash scripts/ops/verify_selfhosted_ingress_canary.sh
```

القبول يتطلب `SELFHOST_INGRESS_CANARY=PASS` و`PUBLIC_PORTS_80_443=NOT_OPENED_BY_THIS_RUNNER`.

## قاعدة البيانات قبل الخروج من Railway

الترتيب الإلزامي:

1. snapshot من قاعدة Railway بدون طباعة URI/credentials.
2. SHA-256 checksum.
3. `pg_restore --list` بنجاح.
4. restore drill مع نفس extensions المطلوبة، حاليًا `pg_trgm` و`vector`.
5. schema/capability checks فقط؛ لا تُحوّل مجرد وجود backup إلى DB cutover authority.
6. DB production restore هو L5 مستقل وله rollback.

لا تستخدم PostgreSQL image لا تحتوي pgvector لاختبار dump يحتاج extension `vector`.

## ترتيب القطع العام

`SOURCE SHA -> BUILD -> CANARY Web/API SHA -> HEALTH -> CRITICAL ROUTES -> INGRESS -> TLS -> BACKUP/RESTORE -> PUBLIC CUTOVER -> RUNNING SHA PARITY -> SOAK -> PROVIDER DECOMMISSION`

كل انتقال مادي مستقل ويحتاج السلطة المناسبة. لا تلغِ Railway لمجرد نجاح canary.

## Rollback

قبل أي public cutover يجب أن تبقى Railway قابلة للاستعادة كمسار last-good، وأن تكون خطوات إعادة DNS/origin موثقة ومحدودة. بعد cutover لا يُسمح بإلغاء Railway حتى تمر فترة soak ويثبت أن Web/API/DB self-hosted مستقرة وقابلة للنسخ والاستعادة.

## ممنوع

- تشغيل `docker-compose.prod.yml` القديم.
- استخدام `.env.prod` كسلطة أسرار مفترضة.
- فتح Docker socket أو Ollama/OpenCode للعامة.
- نسخ secrets إلى GitHub أو logs.
- تشغيل public 80/443 من canary.
- اعتبار quote/invoice أو HTTP 200 دليل revenue/production parity.

المرجع التفصيلي: `docs/ops/SELFHOSTED_PRODUCTION_PLANE.md`.
