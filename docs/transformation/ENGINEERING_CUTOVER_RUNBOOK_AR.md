# دليل القطع الهندسي (JSONL → Postgres والمرايا)

## الغرض

ربط أي تفعيل إنتاجي لمسارات الحفظ (`VALUE_LEDGER_BACKEND`، `PROOF_LEDGER_BACKEND`، `DEALIX_OPERATIONAL_STREAM_BACKEND`، `OTEL_CONTRACT_TRACE_EXPORT`) بإشارة تجارية أو امتثال وفق [dealix/transformation/engineering_cutover_policy.yaml](dealix/transformation/engineering_cutover_policy.yaml).

## إشارة مقبولة (أي واحدة)

- عقد موقّع، نطاق بايلوت مقفل، مراجعة أمن/مشتريات بدأت، فاتورة صادرة، طلب أمان صريح من عميل.

## ما يجب أن يظهر في وصف PR

أضف سطرًا صريحًا مثل:

```text
external_signal: pilot_scope_locked
contract_or_pilot_ref: <معرف داخلي أو اسم الحساب>
```

## ترتيب تفعيل آمن (مقترح)

1. **Proof ledger**: `PROOF_LEDGER_BACKEND=dual` لفترة مراقبة، ثم `postgres` بعد التأكد من عدم أخطاء الكتابة.
2. **Value ledger**: `VALUE_LEDGER_BACKEND=dual` أو `postgres` مع مراقبة؛ يبقى JSONL مرجعًا حتى تثبت القراءة من Postgres.
3. **مرآة التدفقات التشغيلية**: `DEALIX_OPERATIONAL_STREAM_BACKEND=dual` ثم `postgres` عند الحاجة لأدلة audit فقط.
4. **OTel**: `OTEL_CONTRACT_TRACE_EXPORT=true` فقط مع tracer فعّال وبموافقة عميل/امتثال.

## التحقق قبل وبعد

- قبل الدمج: `python3 scripts/verify_global_ai_transformation.py`
- بعد الضبط في البيئة: `bash scripts/verify_ceo_signal_readiness.sh transformation` أو `all` حسب التغيير.

## استثناءات

مسموح بقطع بدون إشارة تجارية فقط لكسر CI أو تصحيح أمني، مع ملاحظة مراجعة أمن في وصف PR كما في السياسة.
