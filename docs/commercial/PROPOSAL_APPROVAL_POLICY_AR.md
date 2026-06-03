# سياسة اعتماد العرض التجاري — Dealix

> **المصدر:** [`schemas/commercial_proposal.schema.json`](../../schemas/commercial_proposal.schema.json) ·
> [`schemas/opportunity.schema.json`](../../schemas/opportunity.schema.json) ·
> الاختبار المُلزِم: [`tests/test_proposal_requires_qualified_opportunity.py`](../../tests/test_proposal_requires_qualified_opportunity.py).
> الافتراضات: `dry_run=true`، `approval_required=true`، `send_enabled=false`.

## القاعدة الذهبية (غير قابلة للتجاوز)
**لا عرض بدون:** فرصة مؤهّلة (`qualified=true`) **+** فئة ألم (`pain_category`) **+**
مطابقة منتج (`product_match` ضمن `DLX-L0..L6`) **+** مقياس نجاح (`success_metric`) **+**
وضوح نطاق (`scope_clarity=true`) **+** **موافقة المؤسّس**.

هذه القاعدة مفروضة آلياً بـ `tests/test_proposal_requires_qualified_opportunity.py`،
وتعكس الحقول المطلوبة في `commercial_proposal.schema.json` حيث
`scope_clarity` و`includes_out_of_scope` ثابتان `const: true`.

## البوّابات الست (لا يُتجاوز أي منها)
| # | البوّابة | الحقل / المصدر | الشرط |
|---|---------|----------------|-------|
| 1 | تأهيل | `opportunity.qualified` | `= true` |
| 2 | فئة ألم | `pain_category` | محدّدة من القائمة المعتمدة |
| 3 | مطابقة منتج | `product_match` | يطابق `^DLX-L[0-6]$` |
| 4 | مقياس نجاح | `success_metric` | نصّ قابل للقياس، غير فارغ |
| 5 | وضوح نطاق | `scope_clarity` + `includes_out_of_scope` | كلاهما `true` |
| 6 | موافقة المؤسّس | `approval_status` | `= approved` قبل أي إرسال |

إن سقطت أي بوّابة → الفرصة لا تنتقل إلى `proposal_needed`/`proposal_sent`، وتبقى في
`discovery_completed` أو تعود إلى `nurture`.

## مسار الاعتماد (workflow)
1. **تجهيز مسودّة العرض (آلي):** النظام يبني العرض من الفرصة المؤهّلة والكتالوج → `approval_status=pending`، `send_status=not_sent`.
2. **مراجعة المؤسّس:** فحص البوّابات الست + السلامة (لا عبارات محظورة، لا أرقام بلا دليل، لا عميل مختلق).
3. **القرار:** `approved` / `needs_revision` / `rejected`.
4. **التسعير النهائي:** عند `approved` فقط يُحدّد `final_price` بموافقة المؤسّس (يبقى `null` قبلها).
5. **الإرسال:** يدوي وبموافقة، ووفق سياسة قابلية التسليم؛ `send_status` لا يتجاوز `approved_for_send` إلا بقرار بشري.

## ممنوعات
- تجهيز أو إرسال عرض لفرصة `qualified=false` (مثل OPP-003 TrainMe KSA، OPP-005 Nexus IT Solutions — كلاهما `book_discovery` أولاً).
- تثبيت `final_price` قبل موافقة المؤسّس.
- أي عبارة محظورة أو رقم بلا `evidence_level` أو عميل/دراسة حالة مختلقة.
- إرسال خارجي تلقائي أو نيابة عن العميل خارج السياسة.

## «مثال توضيحي»
- **مسموح:** OPP-001 (Digital Rise Agency) — `qualified=true`، `product_match=DLX-L1`،
  `success_metric` و`scope_clarity=true` → يجوز تجهيز عرض، ثم موافقة المؤسّس قبل الإرسال.
- **ممنوع:** OPP-003 (TrainMe KSA) — `qualified=false`، `product_match=null` → لا عرض؛ الخطوة `book_discovery`.

## قائمة تحقّق المؤسّس قبل الاعتماد
- [ ] البوّابات الست مستوفاة.
- [ ] النطاق وخارج النطاق واضحان.
- [ ] النطاق السعري صحيح و`final_price` لم يُثبّت بعد.
- [ ] لا عبارات محظورة، لا أرقام بلا دليل، لا عملاء مختلقون، لا PII.
