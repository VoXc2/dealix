# العربية

Owner: قائد المراقبة (Observability Lead)

## درجة الطبقة

طبقة المراقبة (Layer 7): **75 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `platform/observability/architecture.md`، `dealix/observability/`، `auto_client_acquisition/observability_adapters/` |
| جاهزية | متوفر | هذه الوثيقة و`platform/observability/readiness.md` |
| اختبارات | متوفر | `readiness/observability/tests.md` |
| مراقبة | متوفر | `dealix/observability/otel.py`، `dealix/observability/sentry.py`، `platform/observability/dashboards.md` |
| حوكمة | متوفر | `auto_client_acquisition/observability_adapters/redaction.py` (حجب المعلومات الشخصية) |
| تراجع | متوفر | `platform/observability/incident_response.md` |
| مقاييس | متوفر | `readiness/observability/scorecard.yaml` |
| مالك | متوفر | قائد المراقبة |

## الفجوات المحددة

- **تمرين استجابة للحوادث:** خطة الاستجابة موثَّقة في `platform/observability/incident_response.md`، لكن تمريناً متحقَّقاً يثبت أن فشل تكامل يظهر في اللوحة وينبّه المالك غير مُسجَّل على وتيرة دورية.
- **تغطية المراقبة العابرة:** ربط فشل التكاملات بظهوره في اللوحة يحتاج اختباراً عابراً مُنفَّذاً (انظر `readiness/cross_layer/observability_coverage_test.md`).

## روابط ذات صلة

- `readiness/observability/tests.md`
- `readiness/observability/scorecard.yaml`
- `readiness/cross_layer/observability_coverage_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Observability Lead

## Layer score

Observability layer (Layer 7): **75 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `platform/observability/architecture.md`, `dealix/observability/`, `auto_client_acquisition/observability_adapters/` |
| readiness | present | this document and `platform/observability/readiness.md` |
| tests | present | `readiness/observability/tests.md` |
| observability | present | `dealix/observability/otel.py`, `dealix/observability/sentry.py`, `platform/observability/dashboards.md` |
| governance | present | `auto_client_acquisition/observability_adapters/redaction.py` (PII redaction) |
| rollback | present | `platform/observability/incident_response.md` |
| metrics | present | `readiness/observability/scorecard.yaml` |
| owner | present | Observability Lead |

## Specific gaps

- **Incident-response drill:** the response plan is documented in `platform/observability/incident_response.md`, but a verified drill proving an integration failure surfaces on the dashboard and alerts the owner is not recorded on a periodic cadence.
- **Cross-layer observability coverage:** linking an integration failure to its dashboard appearance needs an executed cross-layer test (see `readiness/cross_layer/observability_coverage_test.md`).

## Related links

- `readiness/observability/tests.md`
- `readiness/observability/scorecard.yaml`
- `readiness/cross_layer/observability_coverage_test.md`

Estimated value is not Verified value.
