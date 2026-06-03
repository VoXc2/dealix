---
name: dealix-delivery-workflow-report
mode: report
scenario: operations
version: 1
input_requirements:
  - customer_handle
  - service_id
  - delivery_task_ids
  - period_start
  - period_end
output_format:
  - summary_ar
  - summary_en
  - task_table
  - blockers_ar
  - blockers_en
  - next_steps_ar
  - next_steps_en
safety_rules:
  - approval_required_before_send
  - no_guaranteed_claims
  - no_fake_metrics
  - no_external_http
  - bilingual_arabic_primary
approval_mode: approval_required
evidence_requirements:
  - all_task_ids_must_resolve_in_delivery_factory
  - all_completion_events_must_be_in_proof_ledger
arabic_first: true
english_secondary: true
forbidden_claims:
  - نضمن
  - guaranteed
  - blast
  - scrape
example_prompt: |
  Weekly delivery report for Acme-Saudi-Pilot-EXAMPLE,
  service_id=svc_diagnostic_v1, period 2026-04-28..2026-05-04.
  Reference delivery tasks task_001..task_005. Visual: growth_control_tower.
acceptance_checklist:
  - period dates present
  - task table has status per task
  - blockers explicit (or "none")
  - next steps tied to delivery_factory
  - bilingual
---

# dealix-delivery-workflow-report

Weekly/biweekly delivery status report. Audience: founder + customer
PoC. Manual send only.

## Why this skill exists

Operational transparency is the cheapest customer-trust lever. This
report mirrors the delivery_factory state truthfully — no
"on track" claims unless tasks are actually progressing per the
proof_ledger.

## Safety

- Every "completed" status MUST resolve to a `DELIVERY_TASK_COMPLETED`
  ProofEvent.
- No projected percentages without an explicit "estimate" label.
