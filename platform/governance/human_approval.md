# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة.

## الغرض

تصف هذه الوثيقة دور الإنسان في حلقة الحوكمة: متى يُطلب قرار بشري، وكيف يُعرض على المراجع، وما الذي يضمن أن القرار صريح وموثَّق. المبدأ الحاكم: لا يُنفَّذ أي إجراء عالي المخاطر أو مواجِه للعميل آلياً؛ الإنسان يبتّ، والنظام يُنفّذ بعد البتّ فقط.

## متى يُطلب قرار بشري

- كل إجراء بتصنيف موافقة A1 أو أعلى.
- كل إجراء بتصنيف R3 (غير عكوس) بصرف النظر عن محور الموافقة.
- كل إجراء يمسّ بيانات شخصية S3.
- كل إجراء خارجي مواجِه للعميل: يُعرض كمسوّدة فقط (draft-only) ولا يُرسَل دون موافقة.
- كل حملة صنّفها `auto_client_acquisition/compliance_os/risk_engine.py` كعالية المخاطر.

## كيف يُعرض على المراجع

يُنشئ `auto_client_acquisition/approval_center/approval_renderer.py` عرضاً يحوي: ملخص الإجراء، التصنيف A/R/S، السبب من محرّك السياسات، الأدلة المرتبطة، والقرار المطلوب. المراجع يرى ما يكفي للبتّ دون الحاجة لفتح النظام الكامل.

## ضمانات القرار

- القرار صريح: منح أو رفض؛ لا قرار ضمني سوى انتهاء المهلة الذي يُعامل كرفض.
- القرار موثَّق: هوية المراجع، الوقت، السبب — في قيد تدقيق عبر `dealix/trust/audit.py`.
- لا تفويض ذاتي: المراجع لا يبتّ في إجراء اقترحه هو.
- الموافقة المزدوجة للإجراءات A3: مراجعان مختلفان.

## قائمة الجاهزية

- [x] كل إجراء A1+ يتطلب قرار إنسان صريح.
- [x] الإجراءات الخارجية المواجِهة للعميل مسوّدة فقط.
- [x] كل قرار موثَّق بهوية ووقت وسبب.
- [x] لا تفويض ذاتي.
- [ ] إشعار المراجع عبر قناة فورية عند طلب A3 (مُخطَّط).

## المقاييس

- نسبة الإجراءات عالية المخاطر التي بتّ فيها إنسان: 100% (هدف).
- متوسط زمن البتّ.
- نسبة الطلبات المنتهية بالمهلة.

## خطاطيف المراقبة

- قيد تدقيق لكل قرار بشري عبر `dealix/trust/audit.py`.
- تتبّع دورة حياة الطلب عبر `dealix/observability/otel.py`.
- تنبيه عند تجاوز طلب نصف مدة صلاحيته دون بتّ.

## قواعد الحوكمة

- لا إرسال رسائل خارجية نيابة عن العميل دون موافقته الصريحة.
- قواعد المؤسس المسبقة لا تُلغي شرط الموافقة على الإجراءات A3.
- المراجع مسؤول عن قراره؛ القرار مرتبط بهويته في السجل.

## إجراء التراجع

1. تعليق منح القرارات الجديدة.
2. مراجعة القرارات الأخيرة المتأثرة وإعادة تقييمها.
3. عند خلل في العرض: إعادة `approval_renderer.py` لإصدار سابق.
4. تسجيل التراجع كقيد تدقيق.

## درجة الجاهزية الحالية

**الدرجة: 80 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/governance/approval_engine.md`، `governance/approval_rules/`.

---

# English

**Owner:** Governance Platform Lead — Privacy & Trust Plane.

## Purpose

This document describes the human role in the governance loop: when a human decision is required, how it is presented to the reviewer, and what guarantees the decision is explicit and documented. The governing principle: no high-risk or customer-facing action auto-executes; the human decides, and the system executes only after the decision.

## When a human decision is required

- Every action classified A1 or higher.
- Every R3 (irreversible) action regardless of the approval axis.
- Every action touching S3 personal data.
- Every external, customer-facing action: presented draft-only and never sent without approval.
- Every campaign scored high-risk by `auto_client_acquisition/compliance_os/risk_engine.py`.

## How it is presented to the reviewer

`auto_client_acquisition/approval_center/approval_renderer.py` produces a view holding: the action summary, the A/R/S classification, the reason from the Policy Engine, the linked evidence, and the requested decision. The reviewer sees enough to decide without opening the full system.

## Decision guarantees

- The decision is explicit: grant or reject; the only implicit decision is timeout, treated as a rejection.
- The decision is documented: reviewer identity, time, reason — in an audit entry via `dealix/trust/audit.py`.
- No self-approval: a reviewer does not decide on an action they proposed.
- Dual approval for A3 actions: two distinct reviewers.

## Readiness checklist

- [x] Every A1+ action requires an explicit human decision.
- [x] External customer-facing actions are draft-only.
- [x] Every decision is documented with identity, time, and reason.
- [x] No self-approval.
- [ ] Reviewer notification via an instant channel on an A3 request (planned).

## Metrics

- Share of high-risk actions decided by a human: 100% (target).
- Mean time-to-decision.
- Share of requests ending in timeout.

## Observability hooks

- Audit entry per human decision via `dealix/trust/audit.py`.
- Request lifecycle tracing via `dealix/observability/otel.py`.
- Alert when a request crosses half its TTL undecided.

## Governance rules

- No external messages are sent on a customer's behalf without their explicit approval.
- Pre-set founder rules do not override the approval requirement for A3 actions.
- The reviewer is accountable for their decision; the decision is bound to their identity in the log.

## Rollback procedure

1. Suspend new decision grants.
2. Review recent affected decisions and re-evaluate them.
3. On a rendering fault: restore `approval_renderer.py` to a prior version.
4. Record the rollback as an audit entry.

## Current readiness score

**Score: 80 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/governance/approval_engine.md`, `governance/approval_rules/`.
