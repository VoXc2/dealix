# Dealix — بوّابات مخاطر الإرسال (Outbound Risk Gates)

> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`
> كل بوّابة فحص **pass/fail**. أي فشل يوقف المسودّة عن طابور الموافقة، ويجعل CI
> يحظر الإرسال غير الآمن.

البوّابات السبع هي خط الدفاع قبل أي عين بشرية. تنفيذها في
`scripts/draft-quality-gate.js` (وعبر `scripts/_lib/dealix.js#gateDraft`)، وتؤكّدها
اختبارات `tests/`. المسودّة الناجحة = صفر أسباب رفض.

---

## 1. البوّابات السبع (pass/fail)

| # | البوّابة | الفحص (pass = ) | سبب الفشل (`reason_code`) |
|---|----------|------------------|----------------------------|
| 1 | **brand gate** | لا عبارة من `data/commercial/forbidden_claims.yaml` في العنوان/الجسم | `forbidden_claim` |
| 2 | **offer match gate** | `offer_match` يطابق `^DLX-L[0-6]$` ويلائم `pain_hypothesis` | (يُعالَج كـ `missing_required_field` عند غياب الحقل) |
| 3 | **personalization gate** | `personalization_score` ≠ `P0` (الأرضية P1) | `below_p1` |
| 4 | **compliance gate (opt-out)** | المسودّة الباردة فيها `opt_out.included = true` | `missing_unsubscribe` |
| 5 | **compliance gate (no fake thread)** | العنوان لا يبدأ بـ `re:` · `رد:` · `fwd:` · `fw:` · `إعادة توجيه:` | `fake_thread` |
| 6 | **deliverability gate** | المستلِم (domain/company) ليس على `data/outreach/suppression_list.jsonl` | `suppressed` |
| 7 | **security/required-fields gate** | كل حقل في `REQUIRED_DRAFT_FIELDS` موجود؛ لا PII | `missing_required_field` |

> أسباب الرفض الست المعتمدة (من `gateDraft`): `forbidden_claim` · `fake_thread` ·
> `below_p1` · `missing_unsubscribe` · `suppressed` · `missing_required_field`.

---

## 2. الربط بالسكربت والاختبارات

| البوّابة | في الكود | يؤكّدها الاختبار |
|----------|----------|-------------------|
| brand / forbidden claims | `forbiddenClaims()` + `gateDraft` | `tests/test_no_guaranteed_revenue_claims.py` · `tests/test_outreach_no_guaranteed_claims.py` |
| personalization (P1 floor) | فحص `P0` في `gateDraft` | `tests/test_gtm_quality_gate.py` |
| opt-out (compliance) | `opt_out.included` في `gateDraft` | `tests/test_outreach_unsubscribe_required.py` |
| no fake thread | `subjectPrefixes` في `gateDraft` | `tests/test_gtm_quality_gate.py` |
| deliverability / suppression | `suppressionSet()` + `gateDraft` | `tests/test_outreach_suppression_blocks_send.py` |
| required fields / security | `REQUIRED_DRAFT_FIELDS` في `gateDraft` | `tests/test_gtm_quality_gate.py` |

تشغيل البوّابة: `node scripts/draft-quality-gate.js` (ملف المسودّات) ·
`node scripts/draft-quality-gate.js --eval` (حالات `data/evals/gtm_draft_eval_cases.jsonl`).
الخروج بقيمة غير صفرية يحظر الإرسال غير الآمن في CI.

---

## 3. منطق البوّابة (Pass/Fail Logic)

```
reasons = []
if أي حقل إلزامي ناقص            -> reasons += missing_required_field
if عبارة ممنوعة في العنوان/الجسم -> reasons += forbidden_claim
if العنوان يبدأ ببادئة Re/Fwd     -> reasons += fake_thread
if personalization_score == P0    -> reasons += below_p1
if مسودّة باردة بلا opt_out        -> reasons += missing_unsubscribe
if المستلِم على قائمة الإيقاف      -> reasons += suppressed
PASS  <=>  reasons == []
```

أي مسودّة `reasons != []` **لا** تدخل `APPROVAL_QUEUE.md`. النتائج تُلخَّص في
`reports/outreach/DRAFT_GATE_REVIEW.md` مع `forbidden_claim_hits=0` كشرط.

---

## 4. ما بعد البوّابات (لا إرسال تلقائي)

اجتياز البوّابات السبع **شرط ضروري لا كافٍ** للإرسال. الإرسال الحقيقي يتطلّب أيضاً:
- موافقة المؤسّس في `APPROVAL_QUEUE.md` (`approval_status: approved`).
- حكم قابلية تسليم ≥ `LIMITED_SEND_READY` (انظر `EMAIL_DELIVERABILITY_POLICY_AR.md`).
- `send_enabled=true` يدوياً وبموافقة — وهو **مُعطَّل افتراضياً**.

---

## 5. الحدود غير القابلة للتفاوض

- البوّابات لا تُضعَّف ولا تُتجاوَز لتمرير مسودّة.
- لا حذف اختبار لتمريره · `forbidden_claim_hits` يجب أن يبقى 0 في المخرجات.
- لا إرسال قبل: نجاح البوّابات + موافقة المؤسّس + حكم تسليم كافٍ.
- لا ادّعاءات ممنوعة · لا PII · كل مسودّة باردة تحمل opt-out.

---

*المرجع المركزي: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`. أسباب الرفض:
`docs/outreach/DRAFT_REJECTION_REASONS_AR.md`. مراجعة البوّابات:
`reports/outreach/DRAFT_GATE_REVIEW.md`.*
