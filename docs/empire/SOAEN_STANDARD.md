# SOAEN Standard — Source · Owner · Approval · Evidence · Next / معيار SOAEN

> SOAEN names the five things that must exist in any workflow *before* it can
> be automated: Source, Owner, Approval, Evidence, and Next Action. A workflow
> missing any of the five is not ready for automation — it is a risk waiting
> to be scaled.
>
> يحدد SOAEN الأشياء الخمسة التي يجب أن توجد في أي سير عمل *قبل* أتمتته:
> المصدر، المالك، الموافقة، الدليل، والخطوة التالية. أي سير عمل ينقصه واحد من
> الخمسة ليس جاهزاً للأتمتة — بل هو خطر ينتظر التوسيع.

**Date opened / تاريخ الفتح:** 2026-05-17
**Owner / المالك:** Founder
**Status / الحالة:** Strategic narrative — not a binding spec.

---

## 1. The five elements / العناصر الخمسة

| Element / العنصر | Question it answers / السؤال الذي يجيب عليه |
|---|---|
| Source / مصدر | Where did this come from? / من أين جاء هذا؟ |
| Owner / مالك | Who is responsible for it? / من المسؤول عنه؟ |
| Approval / موافقة | Who said it is allowed to proceed? / من أجاز المضي به؟ |
| Evidence / دليل | What proves it actually happened? / ما الذي يثبت أنه حدث فعلاً؟ |
| Next Action / خطوة تالية | What is the very next step, and when? / ما الخطوة التالية ومتى؟ |

---

## 2. The readiness rule / قاعدة الجاهزية

> A workflow that cannot answer all five questions is **not ready for
> automation**. Automating it only scales the gap faster.
>
> سير العمل الذي لا يستطيع الإجابة على الأسئلة الخمسة كلها **ليس جاهزاً
> للأتمتة**. أتمتته تُوسّع الفجوة أسرع فقط.

Automation does not fix a broken workflow. It multiplies whatever the workflow
already is. SOAEN is the gate that decides whether multiplication is safe.

الأتمتة لا تُصلح سير عمل معطوباً. بل تضاعف ما هو عليه أصلاً. SOAEN هي البوابة
التي تقرر ما إذا كانت المضاعفة آمنة.

---

## 3. What a missing element looks like / كيف يبدو نقص عنصر

| If this is missing / إذا غاب هذا | Then the thing is only / فإن الأمر يصبح |
|---|---|
| A lead without an owner / عميل بلا مالك | Not a pipeline — just a list / ليس خط أنابيب — مجرد قائمة |
| A follow-up without evidence / متابعة بلا دليل | Not operations — just a claim / ليست تشغيلاً — مجرد ادعاء |
| An AI action without approval / فعل ذكاء اصطناعي بلا موافقة | Not a feature — a risk / ليس ميزة — بل خطر |
| A dashboard without a next action / لوحة بلا خطوة تالية | Not a system — just a report / ليس نظاماً — مجرد تقرير |
| A number without a source / رقم بلا مصدر | Not proof — just an assertion / ليس دليلاً — مجرد تأكيد |

---

## 4. SOAEN as shared language / SOAEN كلغة مشتركة

SOAEN is not a delivery checklist hidden in operations. It is the shared
vocabulary that appears in every surface Dealix touches:

SOAEN ليس قائمة تحقق مخفية في التشغيل. إنه المفردات المشتركة التي تظهر في كل
سطح تلمسه Dealix:

- Website and demo — how value is explained.
- Proof Pack — how each line item is structured.
- Content and sales — how problems are named to a prospect.
- Partners and customer support — how requests are triaged.
- Delivery — how a workflow is accepted as automation-ready.

— الموقع والديمو — كيف تُشرح القيمة.
— حزمة الأدلة — كيف يُبنى كل بند.
— المحتوى والمبيعات — كيف تُسمّى المشكلات للعميل المحتمل.
— الشركاء ودعم العملاء — كيف تُصنّف الطلبات.
— التسليم — كيف يُقبل سير العمل كجاهز للأتمتة.

---

## 5. Ties to the repo / الارتباط بالمنصة

SOAEN is reflected in concrete modules, not just narrative:

SOAEN ينعكس في وحدات ملموسة، لا في السرد فقط:

| Element / العنصر | Module / الوحدة |
|---|---|
| Source / مصدر | `data_os/source_passport.py` — source attribution |
| Evidence / دليل | `evidence_control_plane_os/` — evidence control plane |

Owner, Approval, and Next Action are governed by the delivery and approval
controls referenced in the constitution.

المالك والموافقة والخطوة التالية محكومة بضوابط التسليم والموافقة المشار إليها
في الدستور.

---

## Doctrine alignment / المواءمة مع الدستور

- SOAEN exists to enforce approval and evidence — directly serving the
  non-negotiables on human approval and evidence trails.
- It blocks automation of unready workflows; no shortcut is offered.
- It produces no outcome promise — it is a readiness gate, not a result claim.
- No element of SOAEN may be marked complete with fabricated evidence.

## Related docs / مراجع ذات صلة

- [`DEALIX_METHOD.md`](DEALIX_METHOD.md) — SOAEN sits inside the Trust layer
- [`DEALIX_CATEGORY.md`](DEALIX_CATEGORY.md) — the five-question category story
- [`../PROOF_PACK_V6_STANDARD.md`](../PROOF_PACK_V6_STANDARD.md) — how evidence is packaged
- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — hard limits
