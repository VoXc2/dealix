# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة.

## الغرض

محرّك الموافقات هو المسار الذي تمرّ عبره كل إجراء عالي المخاطر قبل التنفيذ. لا ينفّذ المحرّك أي عمل بنفسه؛ بل يُنشئ طلب موافقة، ويوجّهه إلى المراجع البشري المناسب، وينتظر قراراً صريحاً. الإجراءات الخارجية المواجِهة للعميل تكون دائماً مسوّدة فقط (draft-only) ولا تُرسَل دون موافقة موثَّقة.

## المكوّنات

- مركز الموافقات `auto_client_acquisition/approval_center/` — إنشاء الطلبات وعرضها وتخزينها (`approval_store.py`, `approval_renderer.py`, `schemas.py`).
- سياسة الموافقة `auto_client_acquisition/governance_os/approval_policy.py` و`auto_client_acquisition/approval_center/approval_policy.py` — تحدّد من يوافق على ماذا.
- مصفوفة الموافقات `auto_client_acquisition/governance_os/approval_matrix.py` — تربط تصنيف A0–A3 بعدد المراجعين ودورهم.
- سير عمل الموافقة `dealix/trust/approval.py` — حالة الطلب: `pending` / `granted` / `rejected` / `expired`.
- قواعد المؤسس `auto_client_acquisition/approval_center/founder_rules.py` و`founder_rules_integration.py` — تفويضات يحددها المؤسس مسبقاً.

## آلية العمل

1. يصل إجراء بتصنيف موافقة A1 أو أعلى من محرّك السياسات بقرار `require_approval`.
2. تحدّد مصفوفة الموافقات الدور المطلوب وعدد المراجعين حسب التصنيف:
   - A0 لا يتطلب موافقة (إجراء داخلي عكوس منخفض الحساسية).
   - A1 موافقة مراجع واحد.
   - A2 موافقة مدير الفريق المعني.
   - A3 موافقة مزدوجة (مالك الطبقة + المالك التجاري) للإجراءات غير العكوسة أو الحساسة S3.
3. يُنشأ `ApprovalRequest` بمدة صلاحية (TTL) محددة؛ انتهاء المهلة يساوي رفضاً ضمنياً (fail-closed).
4. عند المنح يُسلَّم الإجراء إلى Execution Plane مع مرجع الموافقة.
5. كل تغيير حالة يُكتب كقيد تدقيق عبر `dealix/trust/audit.py`.

## قائمة الجاهزية

- [x] كل إجراء A1+ لا يُنفَّذ دون قرار موافقة صريح.
- [x] انتهاء المهلة يُعامل كرفض (fail-closed).
- [x] الإجراءات A3 تتطلب موافقة مزدوجة.
- [x] كل قرار موافقة يحمل هوية المراجع ووقته وسببه.
- [ ] لوحة طوابير الموافقات الحية (مُخطَّطة).

## المقاييس

- نسبة الإجراءات عالية المخاطر التي مرّت بموافقة: 100% (هدف).
- متوسط زمن البتّ في الموافقة.
- نسبة الطلبات المنتهية بالمهلة.
- نسبة الموافقات المزدوجة المكتملة للإجراءات A3.

## خطاطيف المراقبة

- قيد تدقيق عند إنشاء/منح/رفض/انتهاء كل طلب عبر `dealix/trust/audit.py`.
- تتبّع الطلب عبر `dealix/observability/otel.py`.
- تنبيه عند تجاوز طلب A3 نصف مدة صلاحيته.

## قواعد الحوكمة

- لا تفويض ذاتي: المراجع لا يوافق على إجراء اقترحه هو.
- قواعد المؤسس لا تُلغي قاعدة `external_action_requires_approval` لإجراءات A3.
- لا إرسال رسائل خارجية نيابة عن العميل دون موافقته الصريحة.

## إجراء التراجع

1. تعليق منح الموافقات الجديدة.
2. مراجعة الطلبات المعلّقة وإعادة تقييمها يدوياً.
3. استعادة الإصدار السابق من `approval_matrix.py` إن كان السبب تغييراً في المصفوفة.
4. تسجيل التراجع كقيد تدقيق.

## درجة الجاهزية الحالية

**الدرجة: 80 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `platform/governance/architecture.md`، `platform/governance/human_approval.md`، `governance/approval_rules/sales_approval_rules.md`.

---

# English

**Owner:** Governance Platform Lead — Privacy & Trust Plane.

## Purpose

The Approval Engine is the path every high-risk action passes before execution. The engine executes no work itself; it creates an approval request, routes it to the right human reviewer, and waits for an explicit decision. External, customer-facing actions are always draft-only and are never sent without a documented approval.

## Components

- Approval Center `auto_client_acquisition/approval_center/` — request creation, rendering, and storage (`approval_store.py`, `approval_renderer.py`, `schemas.py`).
- Approval policy `auto_client_acquisition/governance_os/approval_policy.py` and `auto_client_acquisition/approval_center/approval_policy.py` — define who approves what.
- Approval matrix `auto_client_acquisition/governance_os/approval_matrix.py` — maps A0–A3 classification to reviewer count and role.
- Approval workflow `dealix/trust/approval.py` — request state: `pending` / `granted` / `rejected` / `expired`.
- Founder rules `auto_client_acquisition/approval_center/founder_rules.py` and `founder_rules_integration.py` — pre-set delegations defined by the founder.

## How it works

1. An action classified A1 or higher arrives from the Policy Engine with a `require_approval` decision.
2. The approval matrix determines the required role and reviewer count by class:
   - A0 requires no approval (internal, reversible, low-sensitivity action).
   - A1 requires one reviewer.
   - A2 requires the relevant team manager.
   - A3 requires dual approval (layer owner + commercial owner) for irreversible or S3-sensitive actions.
3. An `ApprovalRequest` is created with a defined TTL; expiry equals an implicit rejection (fail-closed).
4. On grant, the action is handed to the Execution Plane with the approval reference.
5. Every state change is written as an audit entry via `dealix/trust/audit.py`.

## Readiness checklist

- [x] Every A1+ action does not execute without an explicit approval decision.
- [x] Timeout is treated as a rejection (fail-closed).
- [x] A3 actions require dual approval.
- [x] Every approval decision carries reviewer identity, time, and reason.
- [ ] Live approval queue dashboard (planned).

## Metrics

- Share of high-risk actions passing through approval: 100% (target).
- Mean time-to-decision for approvals.
- Share of requests ending in timeout.
- Share of completed dual approvals for A3 actions.

## Observability hooks

- Audit entry on create / grant / reject / expire of every request via `dealix/trust/audit.py`.
- Request tracing via `dealix/observability/otel.py`.
- Alert when an A3 request crosses half its TTL.

## Governance rules

- No self-approval: a reviewer cannot approve an action they proposed.
- Founder rules do not override the `external_action_requires_approval` rule for A3 actions.
- No external messages are sent on a customer's behalf without their explicit approval.

## Rollback procedure

1. Suspend new approval grants.
2. Review pending requests and re-evaluate them manually.
3. Restore the prior version of `approval_matrix.py` if a matrix change caused the issue.
4. Record the rollback as an audit entry.

## Current readiness score

**Score: 80 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `platform/governance/architecture.md`, `platform/governance/human_approval.md`, `governance/approval_rules/sales_approval_rules.md`.
