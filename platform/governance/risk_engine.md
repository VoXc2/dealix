# العربية

**Owner:** مالك طبقة الحوكمة (Governance Platform Lead) — قسم الخصوصية والثقة.

## الغرض

محرّك المخاطر يُسند لكل إجراء مقترح تصنيف مخاطر قبل أن يصل إلى محرّك السياسات. التصنيف هو الذي يحدد ما إذا كان الإجراء يُنفَّذ آلياً أو يتطلب موافقة أو يُحجب. لا إجراء بلا تصنيف؛ المجهول يُصنَّف افتراضياً عند الحد الأعلى للحذر.

## نموذج التصنيف الثلاثي

يستخدم محرّك المخاطر ثلاثة محاور مستقلة، معرّفة في `dealix/classifications/__init__.py`:

- **A — الموافقة (Approval):** A0 لا موافقة، A1 موافقة فردية، A2 موافقة مدير، A3 موافقة مزدوجة.
- **R — قابلية التراجع (Reversibility):** R0 عكوس فوري، R1 عكوس بجهد، R2 عكوس جزئياً، R3 غير عكوس.
- **S — الحساسية (Sensitivity):** S0 عام، S1 داخلي، S2 سرّي، S3 بيانات شخصية تخضع لـ PDPL.

درجة المخاطر النهائية هي أعلى محور بين الثلاثة. مثال: إجراء A1/R3/S2 يُعامل كإجراء عالي المخاطر بسبب R3.

## مخاطر الحملات

بالإضافة إلى تصنيف الإجراء الفردي، يُقيّم `auto_client_acquisition/compliance_os/risk_engine.py` مخاطر الحملة قبل إطلاقها: مدى القناة، الأساس النظامي، وحجم البيانات الشخصية. الحملات عالية المخاطر تُرفع للموافقة قبل أي تنفيذ.

## آلية العمل

1. يستقبل المحرّك إجراءً عبر عقد القرار.
2. يستدعي `classify()` لإسناد A/R/S.
3. الإجراء غير المعروف يُسند له افتراضياً A2/R2/S2 (fail-closed).
4. الإجراءات المدرجة في قائمة `NEVER_AUTO_EXECUTE` تُرفع للموافقة بصرف النظر عن أي محور.
5. يُمرَّر التصنيف لمحرّك السياسات ويُكتب كقيد تدقيق.

## قائمة الجاهزية

- [x] كل إجراء يحمل تصنيف A/R/S واحداً على الأقل.
- [x] المجهول يُصنَّف افتراضياً عند الحذر الأعلى.
- [x] الإجراءات R3 لا تُنفَّذ آلياً مطلقاً.
- [x] الحملات تُقيَّم قبل الإطلاق عبر `compliance_os/risk_engine.py`.
- [ ] إعادة معايرة دورية لأوزان المخاطر بناءً على بيانات الحوادث (مُخطَّطة).

## المقاييس

- نسبة الإجراءات الحاملة لتصنيف صريح: 100% (هدف).
- توزيع الإجراءات على درجات المخاطر.
- عدد الإجراءات المصنّفة افتراضياً (مؤشر فجوة تغطية).

## خطاطيف المراقبة

- قيد تدقيق بالتصنيف لكل إجراء عبر `dealix/trust/audit.py`.
- مقياس توزيع المخاطر في `dealix/observability/`.
- تنبيه عند ارتفاع نسبة التصنيف الافتراضي فوق عتبة محددة.

## قواعد الحوكمة

- لا تخفيض تصنيف يدوياً دون موافقة مالك الطبقة وقيد تدقيق.
- تصنيف S3 يستوجب التحقق من الأساس النظامي في `dealix/registers/compliance_saudi.yaml`.
- درجة المخاطر النهائية = أعلى المحاور الثلاثة، لا متوسطها.

## إجراء التراجع

1. تحديد التغيير في منطق التصنيف المسبّب للخلل.
2. استعادة الإصدار السابق من `dealix/classifications/__init__.py` عبر سجل الإصدارات.
3. إعادة تصنيف الإجراءات المعلّقة المتأثرة.
4. تسجيل التراجع كقيد تدقيق.

## درجة الجاهزية الحالية

**الدرجة: 79 / 100 — تجريبي للعميل (Client Pilot).**

مقياس النطاقات الخمسة: 0–59 نموذج أولي / 60–74 بيتا داخلي / 75–84 تجريبي للعميل / 85–94 جاهز للمؤسسات / 95+ حرج للمهمة.

انظر أيضاً: `governance/risk_models/risk_levels.md`، `governance/risk_models/action_risk_matrix.md`.

---

# English

**Owner:** Governance Platform Lead — Privacy & Trust Plane.

## Purpose

The Risk Engine assigns a risk classification to every proposed action before it reaches the Policy Engine. The classification determines whether the action auto-executes, requires approval, or is blocked. No action is unclassified; the unknown is defaulted to the upper bound of caution.

## Three-axis classification model

The Risk Engine uses three independent axes, defined in `dealix/classifications/__init__.py`:

- **A — Approval:** A0 none, A1 single approval, A2 manager approval, A3 dual approval.
- **R — Reversibility:** R0 instantly reversible, R1 reversible with effort, R2 partially reversible, R3 irreversible.
- **S — Sensitivity:** S0 public, S1 internal, S2 confidential, S3 personal data subject to PDPL.

The final risk grade is the highest of the three axes. Example: an A1/R3/S2 action is treated as high-risk because of R3.

## Campaign risk

Beyond per-action classification, `auto_client_acquisition/compliance_os/risk_engine.py` scores campaign risk before launch: channel reach, lawful basis, and personal-data volume. High-risk campaigns are raised for approval before any execution.

## How it works

1. The engine receives an action via the decision contract.
2. It calls `classify()` to assign A/R/S.
3. An unknown action is defaulted to A2/R2/S2 (fail-closed).
4. Actions on the `NEVER_AUTO_EXECUTE` list are raised for approval regardless of any axis.
5. The classification is passed to the Policy Engine and written as an audit entry.

## Readiness checklist

- [x] Every action carries at least one A/R/S classification.
- [x] The unknown is defaulted to the upper bound of caution.
- [x] R3 actions never auto-execute.
- [x] Campaigns are scored before launch via `compliance_os/risk_engine.py`.
- [ ] Periodic recalibration of risk weights from incident data (planned).

## Metrics

- Share of actions carrying an explicit classification: 100% (target).
- Distribution of actions across risk grades.
- Count of default-classified actions (a coverage-gap indicator).

## Observability hooks

- Audit entry with classification per action via `dealix/trust/audit.py`.
- Risk-distribution metric in `dealix/observability/`.
- Alert when the default-classification share crosses a defined threshold.

## Governance rules

- No manual downgrade of a classification without the layer owner's approval and an audit entry.
- An S3 classification requires lawful-basis verification in `dealix/registers/compliance_saudi.yaml`.
- Final risk grade = the highest of the three axes, not their average.

## Rollback procedure

1. Identify the classification-logic change that caused the fault.
2. Restore the prior version of `dealix/classifications/__init__.py` via the release log.
3. Re-classify affected pending actions.
4. Record the rollback as an audit entry.

## Current readiness score

**Score: 79 / 100 — Client Pilot.**

Five-band scale: 0–59 prototype / 60–74 internal beta / 75–84 client pilot / 85–94 enterprise-ready / 95+ mission-critical.

See also: `governance/risk_models/risk_levels.md`, `governance/risk_models/action_risk_matrix.md`.
