# ProofEvent — مثال مشروح / Annotated Example

> هذا المستند يفسّر كل حقل في `SCHEMA.example.json`، حقلاً حقلاً، باللغتين.
> One-page walk-through of `SCHEMA.example.json` — Arabic primary, English secondary.

**المصدر / Source schema:** `auto_client_acquisition/proof_ledger/schemas.py::ProofEvent`

---

## 1. كل حقل بمعناه / Field-by-field meaning

| الحقل / Field | المعنى بالعربية | Meaning (EN) |
|---|---|---|
| `id` | معرّف فريد للحدث (auto). | Unique event identifier (auto-generated). |
| `event_type` | نوع الحدث من `ProofEventType` (مثل `delivery_task_completed`). | Event kind from the `ProofEventType` enum. |
| `customer_handle` | اسم رمزي للعميل. **لا اسم حقيقي قبل موافقة كتابية.** | Customer handle. **Never a real name without written consent.** |
| `service_id` | معرّف الخدمة (مثلاً `svc_growth_starter_pilot`). | Service identifier from the offer ladder. |
| `summary_ar` | ملخّص عربي قصير لما حدث. | Short Arabic summary of the event. |
| `summary_en` | ملخّص إنجليزي قصير. | Short English summary. |
| `evidence_source` | مصدر الإثبات (Moyasar dashboard, founder notebook, …). | Where the evidence came from. |
| `confidence` | درجة الثقة 0.0–1.0. الافتراضي 1.0. | Confidence score. |
| `consent_for_publication` | هل وافق العميل كتابياً على نشر الحدث؟ الافتراضي `false`. | Written customer consent to publish? Default `false`. |
| `redacted_summary_ar` / `redacted_summary_en` | نسخة مُنقّحة من الـ PII. تُملأ تلقائياً عند الكتابة على القرص. | PII-redacted summaries — filled automatically on persist. |
| `approval_status` | الافتراضي `approval_required`. لا يصبح `approved` إلّا بعد إذن صريح. | Default `approval_required`. Promoted to `approved` only after explicit sign-off. |
| `risk_level` | `low` / `medium` / `high`. الافتراضي `low`. | Risk classification. Default `low`. |
| `payload` | بيانات إضافية بصيغة dict — تفاصيل اليوم، عدد الفرص، إلخ. | Free-form structured payload — daily counts, channel, founder notes. |
| `created_at` | UTC timestamp ISO-8601. | UTC ISO-8601 timestamp. |

---

## 2. لماذا التنقيح إلزامي / Why redaction matters

- **PII لا تُكتب على القرص أبداً بصيغتها الخام.** `FileProofLedger.record()` يمرّر كلّ
  `summary_ar` و `summary_en` عبر `pii_redactor.redact_text` قبل الكتابة.
- لو وصل التسجيل إلى auditor خارجي بدون تنقيح: تسريب بيانات عميل = خرق ثقة + خطر قانوني.
- النسخة المنقَّحة (`redacted_summary_*`) هي ما يصدّر إلى Proof Pack افتراضياً، حتّى عند موافقة جزئية.
- **English:** Customer summaries are routed through the PII redactor on every write. The redacted form is what reaches an audit export. Raw text is never the disk-of-record.

---

## 3. متى تُحوَّل الموافقة إلى `true` / When to set `consent_for_publication: true`

✅ **اجعل القيمة `true` فقط** عندما تجتمع كل هذه الشروط:

1. العميل وقّع نموذج إذن كتابي (إيميل أو PDF موقَّع — ليس رسالة WhatsApp مفتوحة).
2. النص المنشور مُراجَع من العميل قبل النشر، وليس مجرد نقل من ملاحظتك.
3. `approval_status` مرفوع يدوياً إلى `approved` بعد المراجعة.
4. `risk_level` ≤ `low` بعد فحص النشر.

❌ **اتركه `false` افتراضياً** في كلّ المراحل الداخلية: التسليم اليومي، فاتورة Moyasar، قرارات الـ pilot.

**English:** Flip to `true` only after a written consent form, customer-reviewed copy, manual approval-status promotion, and a low risk score. Default to `false` everywhere internal.

---

## 4. القيم الممنوعة قطعياً / Forbidden values

لا يجوز أن تظهر أيّ من هذه السلاسل في `summary_ar` أو `summary_en` أو `payload`:

| ممنوع / Forbidden | السبب / Reason |
|---|---|
| `نضمن` | ادّعاء ضمان نتائج — مخالف لميثاق Phase E. |
| `guaranteed` | Marketing guarantee claim. Violates Phase E charter. |
| `blast` | يوحي بإرسال جماعي تلقائيّ — خارج النطاق. |
| `scrape` / `scraping` | مصادر بيانات غير مأذونة — مرفوضة. |

أيّ ProofEvent يحتوي إحدى هذه الكلمات يُرفض قبل الكتابة. اختبار الوحدة في
`tests/test_proof_event_sample_validates.py` يحرس هذا العقد.

**English:** Any sample event containing the strings above must be rejected before persistence. The unit test guards this contract.

---

## 5. خطوات التحقّق السريعة / Quick verification

```bash
python -c "
import json
from auto_client_acquisition.proof_ledger import ProofEvent
data = json.load(open('docs/proof-events/SCHEMA.example.json'))
ev = ProofEvent.model_validate(data)
assert not ev.consent_for_publication, 'Sample must stay internal'
assert ev.approval_status == 'approval_required'
print('sample OK:', ev.id)
"
```

— Annotated Example v1.0 · 2026-05-04 · Dealix
