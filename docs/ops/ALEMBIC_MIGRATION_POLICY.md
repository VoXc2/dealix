# سياسة ترحيل Alembic — Dealix

## الوضع الحالي

- مثال محلي لـ `alembic heads`: قد يظهر أكثر من رأس (مثل `0001` و `004`) — **لا تستخدم `upgrade head` دون دمج أو استهداف revision صريح**.
- في التطوير، قد يعتمد الفريق على `init_db` / `create_all` كما في [AGENTS.md](../../AGENTS.md).

## قواعد التشغيل

1. **لا تشغّل `alembic upgrade head` في الإنتاج** حتى تتحقق صراحة من أن `head` واحد أو أنك تستهدف revision محدد.
2. **قبل الدمج:** نفّذ `alembic heads` ووثّق المخرجات في وصف PR إذا غيّر الترحيل.
3. **دمج الفروع:** عند وجود رأسين، أنشئ **merge revision** يربط السلسلتين ثم اختبر `upgrade` على قاعدة فارغة + نسخة من بيانات staging.
4. **التراجع:** استخدم `alembic downgrade -1` أو revision محدد فقط ضمن نافذة متفق عليها؛ راجع [dealix/masters/incident_rollback_runbook.md](../../dealix/masters/incident_rollback_runbook.md).

## مراجع

- [alembic.ini](../../alembic.ini)
- مجلد [db/migrations](../../db/migrations)
