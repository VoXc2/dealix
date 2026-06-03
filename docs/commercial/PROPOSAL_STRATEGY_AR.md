# استراتيجية العرض التجاري — Dealix

> **المصدر:** [`schemas/commercial_proposal.schema.json`](../../schemas/commercial_proposal.schema.json) ·
> العروض [`product_catalog.yaml`](../../data/commercial/product_catalog.yaml) · الفرص [`opportunities.jsonl`](../../data/commercial/opportunities.jsonl).
> الافتراضات: `dry_run=true`، `approval_required=true`، `send_enabled=false` · السعر النهائي بموافقة المؤسّس.

المبدأ: العرض **يلخّص اتفاقاً** تكوّن في الاكتشاف، لا يبيع من جديد. كل عرض مرتبط
بفرصة مؤهّلة (`qualified=true`) ومُطابَقة لمنتج `DLX-L*`، وله success metric ونطاق
واضح وبند خارج النطاق. لا عرض بدون ذلك (انظر `PROPOSAL_APPROVAL_POLICY_AR.md`).

## الأركان الإلزامية (من schema)
كل عرض يحمل الحقول المطلوبة في `commercial_proposal.schema.json`:
`proposal_id` · `opp_id` · `company` · `product_match` (`^DLX-L[0-6]$`) · `pain_category`
· `success_metric` · `scope_clarity=true` · `includes_out_of_scope=true` ·
`price_range{min,max,currency}` · `approval_status` · `send_status`.
الحقل `final_price` يبقى `null` حتى موافقة المؤسّس.

## بنية العرض (الأقسام)
1. **السياق ونقطة الألم:** فئة `pain_category` واحدة محورية كما ظهرت في الاكتشاف، بدليلها و`evidence_level`.
2. **المنتج المطابق:** عرض واحد من السلّم (`DLX-L0..L6`) باسمه ووعده من الكتالوج.
3. **مقياس النجاح:** `success_metric` قابل للقياس (مثل: تحديد أكبر 3 نقاط تسرّب) — **فرضية تحسّن تُقاس**، لا نتيجة مضمونة.
4. **النطاق (scope):** بنود التنفيذ المضمّنة، منسوخة من حقل `scope` للعرض في الكتالوج.
5. **خارج النطاق (out_of_scope):** صريح وإلزامي — يحمي من تضخّم النطاق (انظر `SCOPE_CREEP_POLICY_AR.md`).
6. **المدّة:** `timeline_days` من الكتالوج (نطاق).
7. **المتطلّبات من العميل:** `requirements` (بيانات، مالك عملية، 30 دقيقة…).
8. **النطاق السعري:** `price_range` بالعملة `SAR` — **نطاق فقط**، والسعر النهائي بموافقة المؤسّس.
9. **الخطوة التالية والإثبات:** خطوة واحدة + proof pack بأدلة حقيقية فقط (انظر `PROOF_PACK_COMMERCIAL_GUIDE_AR.md`).

## ربط الألم بالعرض (مرجع سريع)
| `pain_category` | العرض المبدئي | success_metric (مثال من الكتالوج) |
|-----------------|---------------|-----------------------------------|
| `lead_leakage` | `DLX-L1` | تحديد أكبر 3 نقاط تسرّب قابلة للمعالجة |
| `follow_up_chaos` | `DLX-L2` | تغطية متابعة لكل lead ضمن SLA متفق عليه |
| `crm_data_disorder` | `DLX-L3` | مصدر واحد للحقيقة + تقرير أسبوعي ثابت |
| `weak_reporting` / `sales_team_inconsistency` | `DLX-L3` → `DLX-L5` | تحسّن مُقاس شهرياً في مقياس متفق عليه |
| نطاق مخصّص موقّع | `DLX-L6` | تسليم النطاق المخصّص بالكامل |

## استراتيجية الخطوة الأولى الصغيرة
نبدأ غالباً بـ `DLX-L1` (أو `DLX-L0`) كخطوة أولى منخفضة المخاطرة تثبت القيمة قبل
أي التزام أكبر، ثم نرتقي عبر `handoff`/`renewal_path` (انظر `RISK_REVERSAL_POLICY_AR.md`).
هذا ليس ضماناً، بل تقليص مخاطر عبر نطاق واضح وخطوة صغيرة.

## ممنوعات في نص العرض
- أي عبارة محظورة: نضمن / نضاعف الإيرادات / نتائج مضمونة / بدون مخاطرة / 10x / "guaranteed revenue" / "no risk".
- أي عميل أو دراسة حالة أو رقم مُختلق (انظر `CASE_STUDY_POLICY_AR.md`).
- أي رقم بلا `evidence_level`.
- أي سعر نهائي قبل موافقة المؤسّس.
- أي وعد بإرسال نيابة عن العميل خارج سياسة قابلية التسليم (يطابق OBJ-008).

## أمثلة «مثال توضيحي»
- «مثال توضيحي»: عرض لـ Digital Rise Agency — `DLX-L1`، `pain=lead_leakage`،
  success metric: تحديد أكبر 3 نقاط تسرّب، نطاق سعري 2,500–5,000 ر.س، السعر النهائي بموافقة المؤسّس (يطابق OPP-001).
- «مثال توضيحي»: عرض لـ Horizon Realty Team — `DLX-L2`، `pain=follow_up_chaos` (يطابق OPP-002).

## قائمة تحقّق قبل التجهيز
- [ ] الفرصة `qualified=true` ومُطابَقة لمنتج `DLX-L*`.
- [ ] `pain_category` + `success_metric` + `scope_clarity=true` + `includes_out_of_scope=true`.
- [ ] نطاق سعري بالعملة الصحيحة، `final_price=null`.
- [ ] لا عبارات محظورة، لا أرقام بلا دليل، لا عملاء مختلقون.
