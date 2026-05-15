# العربية

# قائمة ما قبل الإطلاق — Layer 10 / مرحلة ضمان الجودة

**المالك:** قائد الجودة (QA Lead)
**الجمهور:** عضو الفريق الذي يفحص أي مخرَج قبل تسليمه للعميل
**المراجع:** `clients/_TEMPLATE/04_qa_review.md` · `clients/_TEMPLATE/delivery_approval.md` · `docs/PILOT_DELIVERY_SOP.md` · `playbooks/qa/client_acceptance_tests.md`

> الغرض: لا إطلاق بلا قائمة فحص. كل تسليم يمرّ بنفس بوابة الجودة قبل وصوله للعميل.

## 1. متى تُستخدم هذه القائمة

قبل تسليم أي مخرَج للعميل في أي مرحلة من سُلَّم الخدمات — تشخيص، Sprint، Data Pack، أو حزمة Managed Ops.

## 2. بوابة الجودة (سبع فحوص)

1. **فحص الدقة:** كل رقم وكل ادعاء مدعوم بمصدر من بيانات العميل.
2. **فحص اللغة:** عربية مهنية طبيعية، وثنائية اللغة عند الحاجة بطول متطابق.
3. **فحص الحوكمة:** لا «نضمن»، لا أرقام كحقيقة، لا بيانات شخصية، لا أسماء عملاء.
4. **فحص الحالة:** كل مخرَج معلَّم `draft_only` حتى موافقة العميل.
5. **فحص الإثبات:** كل إنجاز موثَّق بمصدر — لا إثبات مختلق.
6. **فحص النطاق:** المخرَج يطابق نطاق `clients/<client>/00_scope.md`.
7. **فحص الاكتمال:** كل بنود معايير القبول للمرحلة مستوفاة.

## 3. خطوات الفحص (خطوة بخطوة)

1. افتح المخرَج وقالب `clients/_TEMPLATE/04_qa_review.md`.
2. مرّ على الفحوص السبع بالترتيب وعلّم كل واحدة.
3. أي فحص لم يُجَز → أعِد المخرَج للتسليم مع ملاحظة محددة.
4. عند اجتياز الفحوص السبع، وقّع موافقة الجودة في `delivery_approval.md`.
5. سجّل نتيجة الفحص في سجل حوكمة العميل.

## 4. القواعد الحاكمة (Non-negotiables)

- لا تسليم لعميل دون اجتياز الفحوص السبع.
- لا «نضمن مبيعات» — استخدم «فرص مُثبتة بأدلة».
- لا أرقام أداء كحقيقة — «تقديري» فقط.
- لا بيانات شخصية ولا أسماء عملاء حقيقية في أي مخرَج عام.
- المُراجِع شخص غير كاتب المخرَج عند توفّر فردين.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] الفحوص السبع كلها أُجريت وعُلّمت.
- [ ] أي فحص فاشل عُولج قبل التسليم.
- [ ] موافقة الجودة موقّعة في `delivery_approval.md`.
- [ ] نتيجة الفحص مسجَّلة في `governance_events.md`.
- [ ] المخرَج معلَّم `draft_only`.

## 6. المقاييس

- معدل اجتياز الجودة من المحاولة الأولى (الهدف ≥ 90%).
- عدد المخالفات المكتشفة قبل التسليم مقابل بعده.
- زمن دورة الفحص لكل مخرَج (الهدف ≤ ساعتين).

## 7. خطافات المراقبة (Observability)

- سجّل كل فحص في `clients/<client>/04_qa_review.md`.
- علّم النتيجة: `passed` / `returned` / `escalated`.
- مراجعة أسبوعية لمعدل الاجتياز وأنواع المخالفات المتكررة.

## 8. إجراء التراجع (Rollback)

إذا وصل مخرَج للعميل دون اجتياز الجودة:
1. اسحب المخرَج وأبلغ العميل باحترام بنسخة مصححة خلال 24 ساعة.
2. سجّل الحادثة في سجل الحوكمة.
3. راجع سبب تجاوز البوابة وحدّث القائمة لمنع التكرار.

# English

# Pre-Launch Checklist — Layer 10 / QA Stage

**Owner:** QA Lead
**Audience:** Team member checking any deliverable before it goes to the client
**References:** `clients/_TEMPLATE/04_qa_review.md` · `clients/_TEMPLATE/delivery_approval.md` · `docs/PILOT_DELIVERY_SOP.md` · `playbooks/qa/client_acceptance_tests.md`

> Purpose: no launch without a checklist. Every delivery passes the same quality gate before it reaches the client.

## 1. When to use this checklist

Before delivering any output to the client at any rung of the service ladder — diagnostic, Sprint, Data Pack, or a Managed Ops pack.

## 2. The quality gate (seven checks)

1. **Accuracy check:** every figure and claim is backed by a source in the client's data.
2. **Language check:** natural professional Arabic, and bilingual where needed with matched length.
3. **Governance check:** no "guaranteed", no figures as fact, no PII, no client names.
4. **State check:** every deliverable tagged `draft_only` until client approval.
5. **Evidence check:** every achievement documented with a source — no fake proof.
6. **Scope check:** the output matches the scope in `clients/<client>/00_scope.md`.
7. **Completeness check:** all stage acceptance criteria are met.

## 3. Review steps (step by step)

1. Open the deliverable and the `clients/_TEMPLATE/04_qa_review.md` template.
2. Run the seven checks in order and mark each one.
3. Any failed check → return the deliverable to delivery with a specific note.
4. When all seven pass, sign QA approval in `delivery_approval.md`.
5. Log the review result in the client governance log.

## 4. Governance rules (non-negotiables)

- No delivery to a client without passing all seven checks.
- No "guaranteed sales" — use "evidenced opportunities".
- No performance figures as fact — "estimated" only.
- No PII and no real client names in any public deliverable.
- The reviewer is someone other than the deliverable's author when two people are available.

## 5. Acceptance criteria (readiness checklist)

- [ ] All seven checks run and marked.
- [ ] Any failed check resolved before delivery.
- [ ] QA approval signed in `delivery_approval.md`.
- [ ] Review result logged in `governance_events.md`.
- [ ] Deliverable tagged `draft_only`.

## 6. Metrics

- First-pass QA pass rate (target ≥ 90%).
- Violations caught before delivery vs. after.
- Review cycle time per deliverable (target ≤ 2 hours).

## 7. Observability hooks

- Log each review in `clients/<client>/04_qa_review.md`.
- Tag the result: `passed` / `returned` / `escalated`.
- Weekly review of pass rate and recurring violation types.

## 8. Rollback procedure

If a deliverable reached the client without passing QA:
1. Withdraw the output and respectfully send a corrected version within 24 hours.
2. Record the incident in the governance log.
3. Review why the gate was bypassed and update the checklist to prevent recurrence.
