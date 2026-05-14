# Dealix Governance Pyramid — هرْم الحوكمة الخمسة

**القاعدة:** الحوكمة طبقات — ليست ملف PDF واحد.

## Level 1 — Policy

وثائق واضحة للبشر:

- [`../governance/FORBIDDEN_ACTIONS.md`](../governance/FORBIDDEN_ACTIONS.md)
- [`../governance/AI_USAGE_POLICY.md`](../governance/AI_USAGE_POLICY.md)
- [`../governance/DATA_HANDLING_RULES.md`](../governance/DATA_HANDLING_RULES.md)
- [`../company/DEALIX_CONSTITUTION.md`](../company/DEALIX_CONSTITUTION.md)

## Level 2 — Runtime Rules

قواعد في الكود YAML + فحوصات — `auto_client_acquisition/governance_os/rules/`:

`no_cold_whatsapp` · `no_linkedin_automation` · `no_scraping` · `no_fake_proof` · `no_guaranteed_claims` · `no_pii_in_logs` · `no_source_no_answer` · `external_action_requires_approval`

## Level 3 — Human Approval

إجراءات خارجية أو حساسة: `approval_required` · `approval_owner` (مثلاً delivery owner) — [`../governance/APPROVAL_MATRIX.md`](../governance/APPROVAL_MATRIX.md)

## Level 4 — Audit + Proof

تتبع: `audit_event_id` · `proof_event_id` · `ai_run_id` — [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md) · [`../product/AI_RUN_PROVENANCE.md`](../product/AI_RUN_PROVENANCE.md)

## Level 5 — Governance Intelligence

النظام يتعلم: أنماط مخاطر → قواعد جديدة → اختبارات → بنود checklist → playbook → محتوى ثقة.

مرتبط بـ: [`ANTIFRAGILITY_AND_DECISION_LAW.md`](ANTIFRAGILITY_AND_DECISION_LAW.md) · [`../governance/INCIDENT_RESPONSE.md`](../governance/INCIDENT_RESPONSE.md)
