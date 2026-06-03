# عملية البيع من البداية للنهاية — Dealix

> الحقيقة المرجعية للمراحل: [`MARKET_PRODUCTION_NAMING_CONVENTIONS.md`](../gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md) ·
> الفرص [`opportunities.jsonl`](../../data/commercial/opportunities.jsonl) (schema [`opportunity.schema.json`](../../schemas/opportunity.schema.json)) ·
> العروض [`product_catalog.yaml`](../../data/commercial/product_catalog.yaml).
> الافتراضات: `dry_run=true`، `approval_required=true`، `send_enabled=false` · السعر النهائي بموافقة المؤسّس.

الهدف: مسار واحد واضح من إشارة إلى تجديد، يحرسه مبدأ ثابت —
**الـ AI يجهّز ويرتّب ويقترح؛ المؤسّس يعتمد؛ إنسان يرسل.** نحن نساعد، نرتّب، نقيس، نكشف فرص التحسين، ونجهّز مسودّات بموافقة — بلا وعد بنتائج مضمونة.

---

## 1) المراحل الإحدى والعشرون (مرتّبة)

`signal_detected` → `researched` → `qualified` → `drafted` → `approved_for_outreach` →
`contacted` → `replied` → `discovery_scheduled` → `discovery_completed` →
`proposal_needed` → `proposal_sent` → `negotiation` → `payment_handoff` → `won` →
`delivery_handoff` → `active_delivery` → `renewal_candidate` → `renewed`.

مراحل جانبية/نهائية: `lost` · `nurture` · `do_not_contact`.

تعريف كل مرحلة ومعايير الدخول/الخروج في [`PIPELINE_STAGES_AR.md`](./PIPELINE_STAGES_AR.md).

---

## 2) ما هو قابل للأتمتة وما يتطلّب موافقة

| المرحلة | المنفّذ | قابل للأتمتة؟ | بوابة الموافقة |
|---------|---------|----------------|-----------------|
| `signal_detected` | AI | نعم (رصد وتجميع) | — |
| `researched` | AI | نعم (إثراء، تخصيص) | — |
| `qualified` | AI يقترح / المؤسّس يؤكّد | جزئياً | تأكيد التأهيل |
| `drafted` | AI | نعم (تجهيز مسودّة) | — |
| `approved_for_outreach` | **المؤسّس** | لا | **موافقة قبل أي إرسال** |
| `contacted` | **إنسان** | لا | إرسال بشري فقط |
| `replied` | AI يسجّل / إنسان يردّ | جزئياً | ردّ بشري على المحتوى |
| `discovery_scheduled` | إنسان | لا | — |
| `discovery_completed` | إنسان + AI يلخّص | جزئياً | — |
| `proposal_needed` | AI يتحقّق من الجاهزية | نعم (فحص الشروط) | لا عرض دون استيفاء الشروط |
| `proposal_sent` | **المؤسّس يعتمد / إنسان يرسل** | لا | **اعتماد المؤسّس + إرسال بشري** |
| `negotiation` | إنسان | لا | تعديل السعر بموافقة المؤسّس |
| `payment_handoff` | **إنسان** | لا | بشري فقط — لا فواتير آلية |
| `won` | إنسان | لا | — |
| `delivery_handoff` | إنسان + AI يجهّز | جزئياً | — |
| `active_delivery` | فريق التسليم | جزئياً | — |
| `renewal_candidate` | AI يرشّح | نعم (رصد إشارات) | — |
| `renewed` | **المؤسّس يعتمد** | لا | اعتماد قيمة التجديد |

> خطوط الحوكمة الحمراء: «AI never sends external messages without approval» · «AI never makes pricing decisions» · «AI never processes payments».

---

## 3) مسار الحوكمة الموحّد

```
AI drafts → Human reviews → Approve / Reject → If approved: human executes → Log
```

كل قرار خارجي (إرسال، سعر، عرض، دفع، تجديد) يمرّ بهذا المسار، ويُقيَّد في
`company_os/governance/ai_action_ledger.jsonl`. أي إجراء يتجاوز البوابة = خرق حوكمة.

---

## 4) بوابة العرض (لا عرض بلا استيفاء)

لا يُجهَّز أي عرض إلا بعد توفّر **كل** الشروط الستة:

1. فرصة **مؤهَّلة** (`qualified=true`).
2. **فئة ألم** واحدة (`pain_category`).
3. **مطابقة منتج** من السلّم (`product_match` بنمط `DLX-L[0-6]`).
4. **مقياس نجاح** (`success_metric`).
5. **وضوح النطاق** (`scope_clarity=true`).
6. **اعتماد المؤسّس** (`approval_status`).

يفرض هذه القاعدة `tests/test_proposal_requires_qualified_opportunity.py`، والتفاصيل في
[`PROPOSAL_APPROVAL_POLICY_AR.md`](./PROPOSAL_APPROVAL_POLICY_AR.md).

---

## 5) المخارج الجانبية

- `lost`: لا ملاءمة الآن أو فاز غيرنا — نسجّل السبب ونترك الباب مفتوحاً.
- `nurture`: مناسب لكن التوقيت غير مناسب — متابعة منخفضة الإيقاع بموافقة.
- `do_not_contact`: طلب إيقاف أو سبب امتثال — يُحترم فوراً ويُسجَّل.
- استبعاد لعدم الملاءمة: [`WALK_AWAY_RULES_AR.md`](./WALK_AWAY_RULES_AR.md) و[`BAD_FIT_CLIENT_POLICY_AR.md`](./BAD_FIT_CLIENT_POLICY_AR.md).

> سطر واحد: مسار واحد من إشارة إلى تجديد؛ الـ AI يجهّز، والمؤسّس يعتمد، والإنسان يرسل — بلا ادّعاءات مضمونة.
