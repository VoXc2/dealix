# Value OS — قياس القيمة

## الهدف

تسجيل **أحداث قيمة** مع تميين صريح بين:

- **Estimated** — تقديري، لا يُسوّق كحقيقة متحققة.
- **Observed** — ملاحَظ تشغيليًا ضمن النطاق المسموح توثيقه.
- **Verified** — يتطلب مسار تحقق (وموافقة عميل عند الاستخدام في case study).

## Value Event (مرجعي)

```json
{
  "value_event_id": "VAL-001",
  "project_id": "PRJ-001",
  "value_type": "Revenue Proof",
  "metric": "accounts_scored",
  "before": 0,
  "after": 50,
  "confidence": "observed",
  "limitations": "No external outreach executed by Dealix"
}
```

## التنفيذ في الريبو

- `auto_client_acquisition/proof_architecture_os/value_ledger.py`
- `auto_client_acquisition/value_capture_os/`
- بوابات المطالبة: `auto_client_acquisition/risk_resilience_os/claim_safety.py`

## روابط

- [INTELLIGENCE_OS.md](INTELLIGENCE_OS.md) — [CAPITAL_OS.md](CAPITAL_OS.md)
