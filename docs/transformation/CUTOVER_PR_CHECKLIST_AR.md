# قائمة تحقق PR — قطع هندسي (Cutover)

استخدم مع [ENGINEERING_CUTOVER_RUNBOOK_AR.md](ENGINEERING_CUTOVER_RUNBOOK_AR.md) و[engineering_cutover_policy.yaml](../../dealix/transformation/engineering_cutover_policy.yaml).

## قبل فتح PR

- [ ] إشارة خارجية واحدة على الأقل (عقد، بايلوت مقفل، مراجعة أمن، فاتورة، طلب أمان)
- [ ] `external_signal:` و`contract_or_pilot_ref:` في وصف PR
- [ ] `python3 scripts/verify_global_ai_transformation.py` أخضر محليًا

## متغيرات شائعة

| متغير | ترتيب مقترح |
| --- | --- |
| `PROOF_LEDGER_BACKEND` | `dual` → مراقبة → `postgres` |
| `VALUE_LEDGER_BACKEND` | `dual` → مراقبة → `postgres` |
| `DEALIX_OPERATIONAL_STREAM_BACKEND` | عند الحاجة لـ audit فقط |
| `OTEL_CONTRACT_TRACE_EXPORT` | فقط بطلب عميل/امتثال |

## تحقق آلي لوصف PR

```bash
python3 scripts/verify_cutover_pr_body.py --file /path/to/pr_body.md
```

## استثناء

كسر CI أو تصحيح أمني: ملاحظة مراجعة أمن في PR بدون إشارة تجارية.
