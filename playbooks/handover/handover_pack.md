# العربية

# حزمة التسليم النهائي — Layer 10 / مرحلة التسليم

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي يسلّم الارتباط رسمياً للعميل
**المراجع:** `clients/_TEMPLATE/07_next_steps.md` · `clients/_TEMPLATE/06_proof_pack.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` (القسم 8) · `playbooks/handover/support_process.md` · `docs/scorecards/PROJECT_SCORECARD.md`

> الغرض: حزمة تسليم موحّدة تضمن أن العميل يملك كل شيء — لا يبقى أي شيء عالقاً مع Dealix.

## 1. متى تُستخدم هذه الحزمة

عند نهاية أي ارتباط: نهاية Sprint، أو نهاية Data Pack، أو إنهاء/تجميد اشتراك Managed Ops.

## 2. مكوّنات حزمة التسليم

| المكوّن | المصدر |
|---|---|
| كل المخرجات النهائية الموافق عليها | ملف العميل |
| Proof Pack الموقّع | `06_proof_pack.md` |
| سجل الموافقات | `delivery_approval.md` |
| أدلة المستخدم والمسؤول السريعة | مرحلة التدريب |
| توصية الخطوة التالية | `07_next_steps.md` |
| تأكيد إعادة/حذف البيانات (PDPL) | سجل الحوكمة |

## 3. خطوات التسليم (خطوة بخطوة)

1. اجمع كل المخرجات النهائية الموافق عليها في مجلد منظَّم.
2. أرفق Proof Pack الموقّع وسجل الموافقات.
3. أرفق أدلة التدريب السريعة من مرحلة التدريب.
4. اكتب توصية خطوة تالية واحدة في `07_next_steps.md`.
5. أكّد إعادة أو حذف بيانات العميل وفق PDPL خلال 7 أيام.
6. أجرِ اجتماع تسليم 30 دقيقة وسلّم الحزمة.
7. حدّث `docs/scorecards/PROJECT_SCORECARD.md` بحالة الاكتمال.

## 4. القواعد الحاكمة (Non-negotiables)

- العميل يملك نسخة كاملة من كل مخرَج — لا احتجاز.
- لا نشر اسم العميل دون إذن مكتوب صريح.
- بيانات العميل تُعاد أو تُحذف وفق PDPL خلال 7 أيام.
- لا upsell أثناء التسليم قبل اكتمال معايير القبول.
- توصية الخطوة التالية بلا أرقام أداء كحقيقة.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] كل المخرجات النهائية مُسلَّمة للعميل.
- [ ] Proof Pack الموقّع وسجل الموافقات مرفقان.
- [ ] أدلة التدريب السريعة مرفقة.
- [ ] اجتماع التسليم 30 دقيقة تمّ.
- [ ] تأكيد إعادة/حذف البيانات موثَّق.
- [ ] `PROJECT_SCORECARD.md` محدَّث.

## 6. المقاييس

- زمن التسليم النهائي: من القبول إلى اكتمال الحزمة (الهدف ≤ 3 أيام).
- نسبة الارتباطات المُسلَّمة بحزمة كاملة (الهدف 100%).
- نسبة بيانات العملاء المُعادة/المحذوفة في الموعد (الهدف 100%).

## 7. خطافات المراقبة (Observability)

- سجّل اكتمال التسليم في `clients/<client>/07_next_steps.md`.
- علّم الحالة: `handover_complete` / `pending`.
- مراجعة شهرية لعدد التسليمات وزمنها.

## 8. إجراء التراجع (Rollback)

إذا اكتُشف نقص مكوّن بعد التسليم:
1. أرسل المكوّن الناقص للعميل خلال 24 ساعة.
2. سجّل الحادثة في سجل الحوكمة.
3. راجع قائمة المكوّنات لمنع تكرار النقص.

# English

# Handover Pack — Layer 10 / Handover Stage

**Owner:** Delivery Lead
**Audience:** Team member formally handing the engagement to the client
**References:** `clients/_TEMPLATE/07_next_steps.md` · `clients/_TEMPLATE/06_proof_pack.md` · `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` (Section 8) · `playbooks/handover/support_process.md` · `docs/scorecards/PROJECT_SCORECARD.md`

> Purpose: a standard handover pack that ensures the client owns everything — nothing stays stuck with Dealix.

## 1. When to use this pack

At the end of any engagement: end of a Sprint, end of a Data Pack, or end/freeze of a Managed Ops subscription.

## 2. Handover pack components

| Component | Source |
|---|---|
| All approved final deliverables | Client folder |
| Signed Proof Pack | `06_proof_pack.md` |
| Approval log | `delivery_approval.md` |
| User and admin quick-reference guides | Training stage |
| Next-step recommendation | `07_next_steps.md` |
| Data return/deletion confirmation (PDPL) | Governance log |

## 3. Handover steps (step by step)

1. Gather all approved final deliverables into one organized folder.
2. Attach the signed Proof Pack and the approval log.
3. Attach the training quick-reference guides from the training stage.
4. Write one next-step recommendation in `07_next_steps.md`.
5. Confirm return or deletion of client data per the PDPL within 7 days.
6. Run a 30-minute handover meeting and deliver the pack.
7. Update `docs/scorecards/PROJECT_SCORECARD.md` with completion status.

## 4. Governance rules (non-negotiables)

- The client owns a full copy of every deliverable — no withholding.
- No publishing the client's name without explicit written permission.
- Client data is returned or deleted per the PDPL within 7 days.
- No upsell during handover before acceptance criteria are met.
- The next-step recommendation carries no performance figures as fact.

## 5. Acceptance criteria (readiness checklist)

- [ ] All final deliverables handed to the client.
- [ ] Signed Proof Pack and approval log attached.
- [ ] Training quick-reference guides attached.
- [ ] The 30-minute handover meeting completed.
- [ ] Data return/deletion confirmation documented.
- [ ] `PROJECT_SCORECARD.md` updated.

## 6. Metrics

- Final handover time: acceptance to pack completion (target ≤ 3 days).
- Share of engagements handed over with a complete pack (target 100%).
- Share of client data returned/deleted on time (target 100%).

## 7. Observability hooks

- Log handover completion in `clients/<client>/07_next_steps.md`.
- Tag the state: `handover_complete` / `pending`.
- Monthly review of handover count and time.

## 8. Rollback procedure

If a missing component is found after handover:
1. Send the missing component to the client within 24 hours.
2. Record the incident in the governance log.
3. Review the component list to prevent the gap from recurring.
