# Dealix — سياسة الادّعاءات (Brand Claims Policy)

> **الموقع (AR):** «Dealix — نظام تشغيل الإيرادات للشركات السعودية».
> **Positioning (EN):** "Saudi B2B Revenue Operating System".
> **الوضع الافتراضي:** `dry_run=true` · `approval_required=true` · `send_enabled=false`.

السياسة الملزمة لكل ادّعاء عام في Dealix (press · content · outbound · UI). المصدر
التقني للحظر: **`data/commercial/forbidden_claims.yaml`** (تفحصه
`scripts/draft-quality-gate.js` واختبارات `tests/`). هذا المستند يلخّص الفئات ويضيف
بوّابة العلامة؛ لا يكرّر القائمة الكاملة.

---

## 1. الفئات الممنوعة (ملخّص — المصدر هو forbidden_claims.yaml)

| الفئة | المنطق | أمثلة (من القائمة) |
|------|--------|---------------------|
| ضمان الإيرادات/النتائج | لا نضمن نتائج | «نضمن زيادة المبيعات» · «نتائج مضمونة» · "guaranteed revenue" |
| المضاعفة/التضخيم | لا وعود مضاعفة | «نضاعف الإيرادات» · «10x» · "double your revenue" · "10x your" |
| نفي المخاطرة | لا «بلا مخاطرة» | «بدون مخاطرة» · "no risk" · "risk-free" |
| الأتمتة الكاملة للبيع | لا «يبيع عنك» | «يبيع عنك بالكامل» · "fully autonomous selling" |
| عناوين بريد مزيّفة | لا threads وهمية | بادئات `re:` · `fwd:` · «رد:» · «إعادة توجيه:» على بريد بارد |

> القاعدة التقنية: مطابقة `case_insensitive_substring`. أي تطابق في مادّة outbound = **فشل بوّابة**.

---

## 2. الأفعال المسموحة فقط (Allowed claim verbs)

> المصدر: `allowed_claim_verbs_ar` في `data/commercial/forbidden_claims.yaml`.

نساعد · نجهّز · نرتّب · نقيس · نكشف فرص التحسين · نقترح · نجهّز مسودّات بموافقة.

أي وعد خارج هذه الأفعال يُرفض أو يُعاد صياغته.

---

## 3. قاعدة الدليل: كل ادّعاء يُربط بـ evidence_level

> المستويات: `none` · `assumed` · `observed` · `verified` (المصدر: `docs/gtm/MARKET_PRODUCTION_NAMING_CONVENTIONS.md`).

- كل عبارة كمّية تُنسب لأعلى مستوى دليل **صادق** فقط.
- `none` لا يُقدَّم كادّعاء؛ يُطرح كهدف أو سؤال.
- ممنوع رفع المستوى بلا دليل، وممنوع تقديم فرضية كأنها نتيجة مضمونة.
- الأمثلة العددية تحمل وسم «مثال توضيحي» وتستخدم أسماء placeholder المعتمدة فقط
  (Digital Rise Agency · Growth Labs SA · TrainMe KSA · Horizon Realty Team ·
  CloudShift Consulting · Nexus IT Solutions · SkillUp Arabia) — أبداً كعملاء أو نتائج حقيقية.
- لا PII: الأشخاص بالدور فقط.

---

## 4. بوّابة العلامة (Brand gate checklist)

كل مادّة عامة تجتاز هذه البنود قبل النشر/الإرسال:

- [ ] **النبرة (Tone):** مختصرة، واثقة، مؤسّسية، سعودية، بلا مبالغة.
- [ ] **الدليل (Evidence):** كل ادّعاء كمّي له `evidence_level` صادق؛ لا رفع بلا دليل.
- [ ] **الادّعاء (Claim):** أفعال مسموحة فقط؛ صفر عبارات من `forbidden_claims.yaml`.
- [ ] **الدعوة (CTA):** واضحة وصادقة؛ بلا وعود نتائج وبلا عناوين `Re:/Fwd:` وهمية.
- [ ] **ملاءمة B2B السعودي:** عربي أولاً، سياق سعودي/خليجي، حوكمة PDPL.
- [ ] **الموافقة (Approval):** `approval_required=true`؛ لا إرسال خارجي قبل الموافقة وبوّابات قابلية التسليم.

أي بند يفشل ⇒ المادّة `rejected` أو `needs_revision`.

---

*المرجع: `data/commercial/forbidden_claims.yaml` · `scripts/draft-quality-gate.js` · `docs/brand/BRAND_VOICE_AR.md` · `docs/brand/BRAND_OUTBOUND_SYSTEM_AR.md`.*
