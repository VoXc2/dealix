# Dealix — العلامة في الـ Outbound (Brand Outbound System)

> **الموقع (AR):** «Dealix — نظام تشغيل الإيرادات للشركات السعودية».
> **Positioning (EN):** "Saudi B2B Revenue Operating System".
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`.

كيف تنطبق العلامة على التواصل الخارجي. الـ Brand OS (الطبقة 1) لا يكتب رسائل؛ يضبط
كيف تُبنى وتُعتمد. مصنع المسودّات والبوّابات: `docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md`
· `scripts/draft-quality-gate.js`.

---

## 1. حقول إلزامية لكل مسودّة (Required draft fields)

كل مسودّة في `data/outreach/drafts.jsonl` تحمل:

| الحقل | المعنى | مرجع القيم |
|------|--------|------------|
| `prospect_id` | معرّف العميل المحتمل | `data/prospects/prospects.jsonl` |
| `company` | اسم الشركة | placeholder المعتمد فقط في الأمثلة |
| `sector` | القطاع | enum `sector` |
| `pain_hypothesis` | فرضية الألم | `pain_category` |
| `offer_match` | العرض المطابق | سلّم `DLX-L0`…`DLX-L6` |
| `personalization_score` | درجة التخصيص | `P0`…`P4` (الأرضية `P1`) |
| `evidence_level` | مستوى الدليل | `none`/`assumed`/`observed`/`verified` |
| `risk_level` | مستوى المخاطرة | `low`/`medium`/`high` |
| `opt_out` status | حالة إلغاء الاشتراك | تُحترم دائماً (suppression) |
| `approval_status` | حالة الموافقة | `pending` افتراضياً |
| `send_status` | حالة الإرسال | `not_sent` افتراضياً |

أي مسودّة تنقصها هذه الحقول ⇒ ترفضها البوّابة.

---

## 2. القواعد المرتبطة بالعلامة

- **الأرضية:** `personalization_score ≥ P1` للدخول في طابور الموافقة.
- **الادّعاءات:** أفعال مسموحة فقط؛ صفر عبارات من `data/commercial/forbidden_claims.yaml`.
- **العناوين:** لا `Re:`/`Fwd:`/«رد:» وهمية إطلاقاً.
- **الدليل:** كل عبارة كمّية تطابق `evidence_level` صادقاً.
- **الخصوصية:** بالدور فقط، لا PII مخترَع، احترام opt-out وقوائم suppression.

---

## 3. السقوف والافتراضات

- **250 مسودّة/يوم مسموحة ومطلوبة. 250 إرسالة/يوم ممنوعة** حتى تجتاز بوّابات قابلية التسليم.
- الافتراض لأي إجراء خارجي: `dry_run=true` · `approval_required=true` · `send_enabled=false`.
- الإرسال الفعلي يتطلّب حكم قابلية تسليم ≥ `LIMITED_SEND_READY` (المرجع: `docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md`).
- مزيج المسودّات اليومي: المرجع `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md` (`draft_type`).

---

## 4. سلسلة الموافقة (Approval chain)

`AI researches → AI drafts → AI scores → Founder approves → Human sends → System tracks → AI learns`

ما يُؤتمت: البحث، التلخيص، الصياغة، الترتيب.
ما يحتاج موافقة بشرية: الإرسال، التسعير، العقود.

البوّابات قبل الموافقة: بوّابة الجودة (`scripts/draft-quality-gate.js`) ←
بوّابة الامتثال (`scripts/governance_check.py`) ← بوّابة قابلية التسليم ←
طابور موافقة المؤسّس (`reports/outreach/APPROVAL_QUEUE.md`).

---

*المرجع: `docs/outreach/COLD_EMAIL_DRAFT_FACTORY_AR.md` · `docs/outreach/EMAIL_DELIVERABILITY_POLICY_AR.md` · `docs/brand/BRAND_CLAIMS_POLICY_AR.md`. لا إرسال خارجي بلا موافقة وبلا اجتياز البوّابات.*
