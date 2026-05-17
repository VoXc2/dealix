# عينة Proof Pack للوكالة / Sample Agency Proof Pack

> ⚠️ عينة توضيحية — بيانات تركيبية مُولّدة، ليست عميلاً حقيقياً ولا نتائج حقيقية. ILLUSTRATIVE SAMPLE — synthetic generated data, NOT a real client and NOT real outcomes.

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `DELIVERY_QA.md` · `REVENUE_TRUTH_LABELS.md`

---

## السياق / Context

وكالة تسويق تدير حملات إعلانية (ad campaigns) لعملائها، وتولّد عدداً من الـ leads أسبوعياً عبر هذه الحملات.

A marketing agency runs ad campaigns for its clients and generates a number of leads each week through those campaigns.

## المشكلة / Problem

الـ leads تصل، لكن المتابعة (follow-up) غير واضحة: لا يُعرف من يملك كل lead، ولا متى تمت آخر متابعة، ولا ما هي الخطوة التالية.

Leads arrive, but follow-up is unclear: it is not known who owns each lead, when it was last contacted, or what the next step is.

## المدخلات / Inputs

عيّنة من 10 leads تركيبية، بتسميات مجهّلة فقط — لا أسماء حقيقية، ولا شركات، ولا بريد، ولا أرقام هواتف.

A sample of 10 synthetic leads, anonymized labels only — no real names, companies, emails, or phone numbers.

| التسمية / Label | المصدر / Source | المالك / Owner | آخر متابعة / Last follow-up | الحالة / Status |
|---|---|---|---|---|
| Lead-01 | Ad campaign A | غير محدّد / unassigned | لا يوجد / none | غير واضحة / unclear |
| Lead-02 | Ad campaign A | Owner-1 | متأخرة / delayed | متابعة / in follow-up |
| Lead-03 | Ad campaign B | غير محدّد / unassigned | لا يوجد / none | غير واضحة / unclear |
| Lead-04 | Ad campaign B | Owner-2 | متأخرة / delayed | متابعة / in follow-up |
| Lead-05 | Ad campaign A | غير محدّد / unassigned | لا يوجد / none | متابعة / in follow-up |
| Lead-06 | Ad campaign C | Owner-1 | متأخرة / delayed | متابعة / in follow-up |
| Lead-07 | Ad campaign C | Owner-3 | حديثة / recent | جاهز لـ demo / demo-ready |
| Lead-08 | Ad campaign B | Owner-2 | متأخرة / delayed | متابعة / in follow-up |
| Lead-09 | Ad campaign A | Owner-3 | حديثة / recent | متابعة / in follow-up |
| Lead-10 | Ad campaign C | Owner-1 | حديثة / recent | متابعة / in follow-up |

## النتائج / Findings

كل عبارة تحمل تسمية تير من `value_os`. في هذه العيّنة لا توجد تسمية `verified` أو `client_confirmed` — البيانات تركيبية.

Every statement carries a `value_os` tier label. In this sample there is no `verified` or `client_confirmed` label — the data is synthetic.

- **3 leads بلا مالك** (Lead-01, Lead-03, Lead-05) — `observed` (ملحوظ في البيانات).
- **4 leads بمتابعة متأخرة** (Lead-02, Lead-04, Lead-06, Lead-08) — `observed`.
- **2 leads بحالة غير واضحة** (Lead-01, Lead-03) — `observed`.
- **1 lead جاهز لـ demo** (Lead-07) — `observed`.
- **فجوة المتابعة قد تكلّف فرصاً قابلة للتأهيل** — `estimated` (تقدير، لا رقم مضمون).

> Three leads have no owner, four have delayed follow-up, two have an unclear status, one is demo-ready (all `observed`). The follow-up gap may cost qualifiable opportunities (`estimated` — a projection, no guaranteed number).

## المخرجات / Outputs

### 1. قائمة أولويات المتابعة / Follow-up priority list

| الأولوية / Priority | التسمية / Label | السبب / Reason | التسمية / Tier |
|---|---|---|---|
| 1 | Lead-07 | جاهز لـ demo / demo-ready | `observed` |
| 2 | Lead-01 | بلا مالك + حالة غير واضحة | `observed` |
| 3 | Lead-03 | بلا مالك + حالة غير واضحة | `observed` |
| 4 | Lead-05 | بلا مالك / unassigned | `observed` |
| 5 | Lead-02 | متابعة متأخرة / delayed | `observed` |

### 2. مسودات الرسائل / Message drafts

مسودات فقط — لا إرسال آلي ولا واتساب بارد. القرار والإرسال عند الوكالة.

Drafts only — no automated send, no cold WhatsApp. The agency decides and sends.

- مسودة تعيين مالك للـ leads بلا مالك (Lead-01, Lead-03, Lead-05).
- مسودة إعادة تنشيط للـ leads المتأخرة (Lead-02, Lead-04, Lead-06, Lead-08).
- مسودة جدولة demo لـ Lead-07.

### 3. مخاطر الموافقة / Approval risks

- أي رسالة لا تُرسَل قبل موافقة صريحة من الوكالة — `observed`.
- مصدر البيانات يجب أن يكون مملوكاً للوكالة وبموافقة — `observed`.

### 4. الإجراءات التالية / Next actions

1. تعيين مالك لكل lead بلا مالك خلال يوم عمل واحد.
2. جدولة demo لـ Lead-07.
3. مراجعة مسودات الرسائل والموافقة عليها قبل أي إرسال.
4. تحديد قاعدة متابعة (مثلاً: تواصل خلال 24 ساعة من وصول الـ lead).

## الخطوة التالية / CTA

تريد نفس الـ Proof Pack على 10 من leads مشروعك الحقيقية؟ / Want the same Proof Pack on 10 of your own leads?

راجع القالب التشغيلي في `../templates/PROOF_PACK_TEMPLATE.md`، ومجلد القوالب `templates/`، وتقرير عيّنة الـ Sprint في `samples/LEAD_INTELLIGENCE_SPRINT_SAMPLE_REPORT_AR.md`.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
