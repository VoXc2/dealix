# تسميات حقيقة الإيراد / Revenue Truth Labels

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `DELIVERY_QA.md` · `SAMPLE_PROOF_PACK.md`

---

## الغرض / Purpose

انضباط في تسمية المخرجات: كل عبارة قيمة في أي Proof Pack تحمل تسمية تير واحدة من `value_os`. هذا يمنع المبالغة ويجعل الدليل قابلاً للتدقيق.

Output-labelling discipline: every value statement in any Proof Pack carries exactly one `value_os` tier label. This prevents exaggeration and keeps evidence auditable.

## التيرز الأربعة / The four tiers

المصدر الوحيد للحقيقة هو `VALID_TIERS` في `value_os` — أربعة تيرز فقط، لا غير.

The single source of truth is `VALID_TIERS` in `value_os` — exactly four tiers, no others.

| التير / Tier | المعنى / Meaning | الدليل المطلوب / Evidence required |
|---|---|---|
| `estimated` / تقديري | إسقاط أو توقّع، بلا تأكيد. A projection, no confirmation. | لا شيء — لكن يجب وسمه `estimated` صراحة. None — but must be explicitly labelled. |
| `observed` / ملحوظ | ملحوظ مباشرة في البيانات أو سير العمل. Observed directly in the data or workflow. | الإشارة إلى البيان/الخطوة الملحوظة. A pointer to the observed data/step. |
| `verified` / مُتحقَّق | تم التحقق منه مقابل سجل. Verified against a record. | `source_ref` إلزامي (مرجع مستند/سجل). `source_ref` mandatory. |
| `client_confirmed` / مؤكَّد من العميل | أكّده العميل صراحةً. Explicitly confirmed by the client. | `source_ref` **و** `confirmation_ref` معاً. Both `source_ref` and `confirmation_ref`. |

قواعد الانضباط من الكود: تير `verified` يتطلب `source_ref`؛ تير `client_confirmed` يتطلب `source_ref` و`confirmation_ref` معاً. بدون هذه المراجع لا يُقبل التير الأعلى.

Discipline rules from the code: the `verified` tier requires a `source_ref`; the `client_confirmed` tier requires both `source_ref` and `confirmation_ref`. Without these references the higher tier is not accepted.

## ربط التسميات غير الرسمية / Mapping informal labels

الناس يستخدمون تسميات دارجة. اربطها على التيرز الأربعة فقط:

People use informal labels. Map them onto the four tiers only:

| التسمية الدارجة / Informal label | التير الرسمي / Official tier | الشرط / Condition |
|---|---|---|
| "Estimate" / تقدير | `estimated` | لا شرط. No condition. |
| "Observed" / ملحوظ | `observed` | إشارة إلى البيان. Pointer to the data. |
| "Payment-confirmed" / مؤكَّد بالدفع | `verified` | سجل الدفع هو الـ `source_ref`. The payment record is the `source_ref`. |
| "Client-confirmed" / مؤكَّد من العميل | `client_confirmed` | `source_ref` + `confirmation_ref`. |

## ليست تيرز قيمة / NOT value tiers

> **مهم / Important:** «Repeated workflow» (سير عمل متكرر) و«Retainer-ready» (جاهز للريتينر) **ليست تيرز قيمة**. هي إشارات تبنٍّ (adoption signals) يملكها `adoption_os`، لا `value_os`.

«Repeated workflow» and «Retainer-ready» are NOT value tiers. They are adoption signals owned by `adoption_os`, not `value_os`. لا توسم بها أي عبارة قيمة. راجع `../20_adoption/`.

## مثال مُطبّق على سطر Proof Pack / Worked example

سطر واحد من Proof Pack، كل جزء بتيره الصحيح:

A single Proof Pack line, each part with its correct tier:

> **lead follow-up gap: `observed` · potential value: `estimated` · client pain: `client_confirmed` · revenue: `verified` only.**

التفسير / Explanation:

- **lead follow-up gap → `observed`**: الفجوة ملحوظة مباشرة في بيانات المتابعة.
- **potential value → `estimated`**: القيمة المحتملة إسقاط، لا تأكيد — رقم تقديري وليس مضموناً.
- **client pain → `client_confirmed`**: الألم أكّده العميل، ومعه `source_ref` و`confirmation_ref`.
- **revenue → `verified` only**: لا يُوسم الإيراد إلا `verified` بوجود `source_ref` (مثل سجل دفع)؛ بدون ذلك يبقى `estimated`.

## قاعدة عملية / Practical rule

إذا غاب الدليل المطلوب لتير، اهبط للتير الأدنى. لا ترفع تيراً لأنك «واثق» — ارفعه لأن الدليل موجود ومُشار إليه.

If the evidence required for a tier is missing, drop to the lower tier. Do not raise a tier because you feel confident — raise it because the evidence exists and is referenced.

## مراجع / References

- منطق التيرز: `../../auto_client_acquisition/value_os/`
- توثيق طبقة القيمة: `../15_value/`
- إشارات التبنّي: `../20_adoption/`

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
