# Dealix — معيار SOAEN · The Dealix SOAEN Standard

**الحالة / Status:** DRAFT
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-17
**وثائق مرافقة / Companion docs:** `SALES_MOTIONS.md` · `OFFER_MATRIX.md` · `../07_governance/README.md` · `../14_proof/README.md`

---

## الغرض · Purpose

معيار SOAEN هو الاختبار الموحَّد الذي تطبّقه Dealix على أي سير عمل قبل اعتباره **جاهزاً للأتمتة (automation-ready)**. كل سير عمل جاهز للأتمتة يجب أن يملك العناصر الخمسة: **مصدر، مالك، موافقة، دليل، خطوة تالية**. سير عمل ينقصه أي عنصر من الخمسة **ليس جاهزاً للأتمتة**.

SOAEN is the single test Dealix applies to any workflow before calling it automation-ready. Every automation-ready workflow must have all five elements: **Source, Owner, Approval, Evidence, Next Action**. A workflow missing any one of the five is not ready for automation.

---

## العناصر الخمسة · The Five Elements

| الرمز · Letter | العنصر · Element | العنصر بالعربية | السؤال الذي يجيب عنه · Question it answers |
|---|---|---|---|
| S | Source | المصدر | من أين جاءت هذه البيانات، وهل مسموح استخدامها؟ · Where did this data come from, and is it consented? |
| O | Owner | المالك | من الشخص المسؤول عن هذا العنصر الآن؟ · Who is the named person accountable for this item now? |
| A | Approval | الموافقة | هل تمّت الموافقة البشرية قبل أي فعل خارجي؟ · Was human approval recorded before any external action? |
| E | Evidence | الدليل | أين الأثر القابل للتدقيق لما حدث؟ · Where is the auditable trail of what happened? |
| N | Next Action | الخطوة التالية | ما القرار أو الإجراء التالي، ومن يملكه؟ · What is the next decision or action, and who owns it? |

---

## أمثلة الفشل · Failure examples

الطريقة الأسرع لفهم المعيار هي رؤية ما يحدث عند غياب عنصر:

- **lead بلا مالك = ليس pipeline.** قائمة أسماء بلا شخص مسؤول هي ملف، وليست عملية بيع.
  A lead without an owner is not a pipeline — it is a list of names with nobody accountable.
- **متابعة بلا دليل = ليست عمليات.** إذا لم تستطع إظهار ما حدث بعد الـlead، فأنت تخمّن، لا تشغّل.
  A follow-up without evidence is not operations — it is a guess, not a documented decision.
- **فعل AI بلا موافقة = مخاطرة.** أي إجراء آلي يلمس طرفاً خارجياً قبل موافقة بشرية هو خطر تشغيلي ونظامي.
  An AI action without approval is a risk — an automated step touching an external party with no human sign-off.
- **لوحة بلا خطوة تالية = مجرد تقرير.** الأرقام التي لا تنتهي بقرار تستهلك انتباهاً ولا تنتج إيراداً.
  A dashboard without a next action is just a report — numbers that consume attention but produce no decision.

---

## ربط SOAEN بالمعمارية القائمة · Mapping SOAEN to the existing architecture

SOAEN ليس إطاراً منافساً. هو **تبسيط موجَّه للبيع (sales-facing simplification)** لمعمارية الحوكمة والدليل الموجودة فعلاً في Dealix. كل حرف يشير إلى مكوّن حقيقي:

SOAEN is not a competing framework. It is a sales-facing simplification of the governance and proof architecture that already exists inside Dealix. Each letter points to a real component.

| عنصر SOAEN · SOAEN element | المكوّن في المعمارية · Architecture component | ملاحظة · Note |
|---|---|---|
| Source / Owner — مصدر / مالك | `data_os` SourcePassport | يسجّل مصدر البيانات والموافقة والملكية · records data origin, consent, ownership |
| Approval — موافقة | `governance_os` GovernanceDecision (7 قيم · 7 values) | قرار حوكمة صريح قبل أي فعل خارجي · explicit governance decision before any external action |
| Evidence — دليل | `proof_os` ProofPack (14 قسماً · 14 sections) + `auditability_os` | حزمة الدليل والأثر القابل للتدقيق · the proof pack and the auditable trail |
| Next Action — خطوة تالية | طبقة الإجراء / التوصية · the action / recommendation layer | تحوّل اللوحة إلى قرار · turns the dashboard into a decision |

**صياغة موحّدة للفريق:** عند الحديث مع العميل، استخدم لغة SOAEN البسيطة. عند الحديث مع الهندسة، استخدم أسماء المكوّنات. الاثنان يصفان النظام نفسه.

For the team: speak SOAEN with customers, speak component names with engineering. Both describe the same system.

---

## قيم القيمة الأربع · The four value tiers

عند تسجيل أي نتيجة في طبقة الدليل، تُصنَّف ضمن أربع قيم فقط (`value_os`): `estimated`، `observed`، `verified`، `client_confirmed`. لا توجد قيمة خامسة. أي نتيجة تُعرَض على العميل يجب أن تحمل قيمتها بوضوح — لا نتائج بلا تصنيف.

When any outcome is recorded in the evidence layer, it carries exactly one of four value tiers: `estimated`, `observed`, `verified`, `client_confirmed`. There is no fifth tier. Every outcome shown to a customer must state its tier — no unlabelled results.

---

## استخدام المعيار في البيع · Using the standard in sales

- في التشخيص: مرّ على سير عمل العميل وحدّد أي حرف من SOAEN مفقود. الحرف المفقود هو نقطة دخول العرض.
  In discovery: walk the prospect's workflow and name the missing SOAEN letter — that gap is the entry point for the offer.
- في العرض التوضيحي: اعرض كيف يملأ ProofPack حرفي E وN معاً.
  In the demo: show how a ProofPack fills both E and N at once.
- في الاعتراضات: "عندنا CRM" يجيب عن O جزئياً فقط؛ A وE غالباً مفقودان. راجع [`OBJECTION_ENGINE.md`](OBJECTION_ENGINE.md).
  For objections: "we have a CRM" answers only part of O; A and E are usually missing.

راجع [`../07_governance/README.md`](../07_governance/README.md) لطبقة الموافقة و[`../14_proof/README.md`](../14_proof/README.md) لطبقة الدليل.

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
