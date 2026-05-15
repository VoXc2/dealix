# العربية

Owner: قائد الحوكمة (Governance Lead)

## درجة الطبقة

طبقة الحوكمة (Layer 5): **79 من 100 — نطاق تجربة عميل**.

## قائمة التحقق المكوّنة من ثمانية أجزاء

| الجزء | الحالة | الدليل (كود حقيقي) |
|---|---|---|
| معمارية | متوفر | `platform/governance/architecture.md`، `auto_client_acquisition/governance_os/`، `dealix/trust/` |
| جاهزية | متوفر | هذه الوثيقة و`platform/governance/readiness.md` |
| اختبارات | متوفر | `readiness/governance/tests.md` |
| مراقبة | متوفر | `dealix/trust/audit.py`، `platform/governance/audit_engine.md` |
| حوكمة | متوفر | `auto_client_acquisition/governance_os/policy_registry.py`، `dealix/governance/approvals.py` |
| تراجع | متوفر | `auto_client_acquisition/governance_os/policy_registry.py` (إصدارات السياسات) |
| مقاييس | متوفر | `readiness/governance/scorecard.yaml` |
| مالك | متوفر | قائد الحوكمة |

## الفجوات المحددة

- **تمرين تراجع السياسة:** سجل السياسات قائم في `governance_os/`، لكن تمريناً متحقَّقاً يعيد إصدار سياسة سابق ضمن تراجع موحّد غير مُسجَّل (انظر `readiness/cross_layer/rollback_drill.md`).
- **اختبار الموافقة العابر:** ربط مصفوفة الموافقة بسير العمل والأدوات يحتاج اختبارات عابرة مُنفَّذة.

القواعد المكتوبة في `governance_os/rules/` — مثل `no_fake_proof.yaml` و`no_guaranteed_claims.yaml` و`no_scraping.yaml` و`no_cold_whatsapp.yaml` و`no_linkedin_automation.yaml` — مفروضة في الكود وتدعم اللاتفاوضيات.

## روابط ذات صلة

- `readiness/governance/tests.md`
- `readiness/governance/scorecard.yaml`
- `readiness/cross_layer/workflow_governance_test.md`
- `readiness/cross_layer/agent_tool_approval_test.md`

القيمة التقديرية ليست قيمة مُتحقَّقة.

# English

Owner: Governance Lead

## Layer score

Governance layer (Layer 5): **79 out of 100 — client pilot band**.

## The 8-part checklist

| Part | Status | Evidence (real code) |
|---|---|---|
| architecture | present | `platform/governance/architecture.md`, `auto_client_acquisition/governance_os/`, `dealix/trust/` |
| readiness | present | this document and `platform/governance/readiness.md` |
| tests | present | `readiness/governance/tests.md` |
| observability | present | `dealix/trust/audit.py`, `platform/governance/audit_engine.md` |
| governance | present | `auto_client_acquisition/governance_os/policy_registry.py`, `dealix/governance/approvals.py` |
| rollback | present | `auto_client_acquisition/governance_os/policy_registry.py` (policy versions) |
| metrics | present | `readiness/governance/scorecard.yaml` |
| owner | present | Governance Lead |

## Specific gaps

- **Policy rollback drill:** the policy registry exists in `governance_os/`, but a verified drill that restores a prior policy version within a unified rollback is not recorded (see `readiness/cross_layer/rollback_drill.md`).
- **Cross-layer approval test:** linking the approval matrix to workflows and tools needs executed cross-layer tests.

The written rules in `governance_os/rules/` — such as `no_fake_proof.yaml`, `no_guaranteed_claims.yaml`, `no_scraping.yaml`, `no_cold_whatsapp.yaml`, and `no_linkedin_automation.yaml` — are enforced in code and uphold the non-negotiables.

## Related links

- `readiness/governance/tests.md`
- `readiness/governance/scorecard.yaml`
- `readiness/cross_layer/workflow_governance_test.md`
- `readiness/cross_layer/agent_tool_approval_test.md`

Estimated value is not Verified value.
