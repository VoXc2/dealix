# العربية

# عملية الدعم — Layer 10 / مرحلة التسليم

**المالك:** قائد نجاح العملاء (Customer Success Lead)
**الجمهور:** فريق الدعم وأي عضو يستقبل طلب عميل بعد التسليم
**المراجع:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` (القسم 3) · `docs/CUSTOMER_SUCCESS_SOP.md` · `playbooks/handover/handover_pack.md` · `playbooks/monthly_optimization/monthly_review.md`

> الغرض: عملية دعم موحّدة باتفاقية مستوى خدمة واضحة — حتى يحصل كل عميل على نفس سرعة الاستجابة وجودتها.

## 1. متى تُستخدم هذه العملية

بعد التسليم النهائي وطوال فترة أي اشتراك. تحكم كل طلب دعم وارد.

## 2. اتفاقية مستوى الخدمة (Support SLA)

| نوع الطلب | وقت الإقرار | وقت الحل |
|---|---|---|
| عاجل (مخرَج توقّف) | < 2 ساعة | < 4 ساعات |
| طلب تعديل مخرَج | < 4 ساعات | < 24 ساعة |
| استفسار عام | < 8 ساعات | < 48 ساعة |
| تقرير إضافي | < 24 ساعة | < 72 ساعة |
| شكوى / تصعيد | < 1 ساعة | خطة < 24 ساعة |

**ساعات الدعم:** الأحد–الخميس 8 ص–6 م. الجمعة–السبت: محدود.

## 3. خطوات معالجة الطلب (خطوة بخطوة)

1. أقرّ باستلام الطلب ضمن وقت SLA المناسب.
2. صنّف نوع الطلب وحدّد المالك.
3. عالج الطلب — كل مخرَج جديد يمرّ بفحص الجودة قبل التسليم.
4. أكّد الحل مع العميل واحصل على إقراره.
5. سجّل الطلب وزمن حله في سجل الدعم.
6. إذا كان شكوى، نفّذ مسار التصعيد بخطة خلال 24 ساعة.

## 4. القواعد الحاكمة (Non-negotiables)

- كل مخرَج دعم بحالة `draft_only` حتى موافقة العميل.
- لا إرسال نيابة عن العميل في أي طلب دعم.
- لا وعود بأرقام أداء في الردود — «تقديري» فقط.
- لا كشط ولا رسائل باردة ولا أتمتة LinkedIn ضمن الدعم.
- كل تصعيد يُسجَّل ويُراجَع سببه الجذري.

## 5. معايير القبول (قائمة الجاهزية)

- [ ] كل طلب أُقرّ ضمن وقت SLA.
- [ ] كل مخرَج دعم مرّ بفحص الجودة.
- [ ] العميل أقرّ بالحل كتابياً.
- [ ] الطلب وزمنه مسجَّلان في سجل الدعم.
- [ ] كل شكوى لها خطة موثَّقة خلال 24 ساعة.

## 6. المقاييس

- نسبة الالتزام بـ SLA الإقرار (الهدف ≥ 95%).
- نسبة الالتزام بـ SLA الحل (الهدف ≥ 90%).
- متوسط زمن الحل لكل نوع طلب.
- رضا العميل عن الدعم (الهدف ≥ 4/5).

## 7. خطافات المراقبة (Observability)

- سجّل كل طلب: النوع، وقت الإقرار، وقت الحل، الحالة.
- علّم الحالة: `open` / `resolved` / `escalated`.
- مراجعة أسبوعية لالتزام SLA وأنواع الطلبات المتكررة.

## 8. إجراء التراجع (Rollback)

إذا تجاوز طلب وقت SLA:
1. أبلغ العميل باحترام بسبب التأخير وموعد جديد واقعي.
2. سجّل تجاوز SLA في سجل الحوكمة.
3. راجع السبب الجذري وحدّث العملية لمنع التكرار.

# English

# Support Process — Layer 10 / Handover Stage

**Owner:** Customer Success Lead
**Audience:** The support team and any member receiving a client request after handover
**References:** `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` (Section 3) · `docs/CUSTOMER_SUCCESS_SOP.md` · `playbooks/handover/handover_pack.md` · `playbooks/monthly_optimization/monthly_review.md`

> Purpose: a standard support process with a clear service-level agreement — so every client gets the same response speed and quality.

## 1. When to use this process

After final handover and throughout any subscription. It governs every incoming support request.

## 2. Service-level agreement (Support SLA)

| Request type | Acknowledgement time | Resolution time |
|---|---|---|
| Urgent (deliverable stalled) | < 2 hours | < 4 hours |
| Deliverable change request | < 4 hours | < 24 hours |
| General inquiry | < 8 hours | < 48 hours |
| Extra report | < 24 hours | < 72 hours |
| Complaint / escalation | < 1 hour | Plan < 24 hours |

**Support hours:** Sunday–Thursday 8am–6pm. Friday–Saturday: limited.

## 3. Request handling steps (step by step)

1. Acknowledge receipt within the relevant SLA time.
2. Classify the request type and assign the owner.
3. Handle the request — every new deliverable passes QA before delivery.
4. Confirm the resolution with the client and get their sign-off.
5. Log the request and its resolution time in the support log.
6. If it is a complaint, run the escalation path with a plan within 24 hours.

## 4. Governance rules (non-negotiables)

- Every support deliverable is `draft_only` until client approval.
- No sending on the client's behalf in any support request.
- No promises of performance figures in responses — "estimated" only.
- No scraping, cold messaging, or LinkedIn automation within support.
- Every escalation is logged and its root cause reviewed.

## 5. Acceptance criteria (readiness checklist)

- [ ] Every request acknowledged within SLA time.
- [ ] Every support deliverable passed QA.
- [ ] The client signed off the resolution in writing.
- [ ] Request and its time logged in the support log.
- [ ] Every complaint has a documented plan within 24 hours.

## 6. Metrics

- Acknowledgement SLA adherence (target ≥ 95%).
- Resolution SLA adherence (target ≥ 90%).
- Average resolution time per request type.
- Client satisfaction with support (target ≥ 4/5).

## 7. Observability hooks

- Log each request: type, acknowledgement time, resolution time, state.
- Tag the state: `open` / `resolved` / `escalated`.
- Weekly review of SLA adherence and recurring request types.

## 8. Rollback procedure

If a request exceeds its SLA time:
1. Respectfully inform the client of the cause of delay and a realistic new time.
2. Log the SLA breach in the governance log.
3. Review the root cause and update the process to prevent recurrence.
