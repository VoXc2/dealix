# سياسة ترحيل Alembic — Dealix

## الوضع الحالي

- سلسلة الترحيل في [db/migrations/versions](../../db/migrations/versions) تتضمن **دمجاً سابقاً** (`006` يربط `005` مع `0001`) ثم تطورات حتى **`009` كرأس وحيد** متوقع لـ `alembic heads`.
- التحقق الآلي في CI: `python scripts/check_alembic_single_head.py` (يفشل عند تعدد الرؤوس).
- نفّذ `alembic heads` محلياً قبل الإنتاج؛ إذا ظهر **أكثر من رأس** بعد PR جديد يضيف فرعاً، أنشئ **merge revision** قبل الاعتماد على `upgrade head`.
- في التطوير، قد يعتمد الفريق على `init_db` / `create_all` كما في [AGENTS.md](../../AGENTS.md).

## قواعد التشغيل

1. **لا تشغّل `alembic upgrade head` في الإنتاج** حتى تتحقق صراحة من أن `head` واحد أو أنك تستهدف revision محدد.
2. **قبل الدمج:** نفّذ `alembic heads` ووثّق المخرجات في وصف PR إذا غيّر الترحيل.
3. **دمج الفروع:** عند وجود رأسين، أنشئ **merge revision** يربط السلسلتين ثم اختبر `upgrade` على قاعدة فارغة + نسخة من بيانات staging.
4. **التراجع:** استخدم `alembic downgrade -1` أو revision محدد فقط ضمن نافذة متفق عليها؛ راجع [dealix/masters/incident_rollback_runbook.md](../../dealix/masters/incident_rollback_runbook.md).

## مراجع

- [alembic.ini](../../alembic.ini)
- مجلد [db/migrations](../../db/migrations)
- [scripts/check_alembic_single_head.py](../../scripts/check_alembic_single_head.py)
