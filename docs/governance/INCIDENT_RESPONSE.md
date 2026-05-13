# Incident Response

> When an AI-assisted workflow goes wrong, Dealix follows a single,
> rehearsed playbook. The playbook is bounded by Saudi PDPL: any personal
> data breach must be notified to SDAIA and affected individuals within
> **72 hours of awareness** (PDPL Art. 18). This document is the operator
> SOP that drives the longer-form
> `docs/PDPL_BREACH_RESPONSE_PLAN.md`.

## What counts as an incident

| Type | Example | Default severity |
|------|---------|:----------------:|
| PII exposure | National ID surfaced in an outbound report | Critical |
| Wrong AI output delivered | Customer received another customer's data or wrong analysis | Critical |
| Unsupported claim | "نضمن" / "guarantee" reached customer-facing copy | High |
| Unauthorized access | Agent or user read data outside their RBAC scope | Critical |
| Data mishandling | Restricted data sent to a non-allowed model provider | Critical |
| Automation misfire | Workflow side-effect ran without required approval | High |
| Vendor breach | Subprocessor (LLM, payments, cloud) discloses an incident | Critical |
| Cost runaway | LLM cost exceeded hard cap before manual stop | Medium |

Any "I'm not sure if this is an incident" is logged and triaged — never
silently ignored.

## Response steps (the 8-step playbook)

```
1. Stop      — halt the offending workflow; pause the agent
2. Preserve  — snapshot runs, prompts, inputs, outputs, audit log
3. Assess    — what happened, who is affected, what data is involved
4. Notify    — internal first (HoLegal + CTO + founder); then PDPL clock
5. Correct   — redact / retract / replace; recall outputs if possible
6. RCA       — root cause analysis in the Decision Ledger within 5 working days
7. Update    — controls, rules, prompts, evals; close the failure mode
8. Playbook  — update this SOP if the response surfaced a gap
```

## The 72-hour PDPL clock (Art. 18)

```
Hour 0   ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━ AWARENESS
Hour 1   Triage + initial classification (founder + HoLegal)
Hour 4   Containment plan in motion
Hour 8   Forensic scope known
Hour 24  Internal RCA draft started
Hour 48  Affected individuals identified
Hour 72  SDAIA notification submitted; affected individuals informed
```

If the incident is **not** a personal data breach (e.g. unsupported claim
only, no PII), the 72-hour SDAIA clock does not start — but the customer
must still be notified for any Critical or High severity that affected
their delivery.

## Roles during response

| Role | Responsibility |
|------|---------------|
| Founder / acting DPO | Owns the 72-hour clock; signs SDAIA notification |
| HoLegal | Determines PDPL trigger; drafts notifications |
| CTO | Forensic snapshot; technical containment |
| HoP | Customer communications; replacement deliverables |
| Agent owner | Reproduces the failure; proposes prompt / rule update |

## Notification templates

Customer notice: `docs/_templates/customer_incident_notice.md`. SDAIA /
regulator notice: `PDPL_BREACH_RESPONSE_PLAN.md` §6. Internal RCA:
`docs/_templates/rca_template.md`. This SOP is the runbook that points
to them.

## Post-incident

- Decision Ledger entry within 5 working days.
- Regression eval added in `EVALUATION_REGISTRY.md`.
- Rule update in `forbidden_claims.py` or `pii_detector.py` if pattern-based.
- Playbook update merged here if response surfaced a gap.

## Hard rules

- No silent fix. Every Critical / High incident has a written RCA.
- No customer-impacting incident is closed without customer notification.
- PDPL 72-hour clock is non-negotiable; missing it is itself an incident.
- The same failure pattern twice is a Critical-level governance failure,
  regardless of original severity.

## Cross-links

- `/home/user/dealix/docs/PDPL_BREACH_RESPONSE_PLAN.md`
- `/home/user/dealix/docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md`
- `/home/user/dealix/docs/governance/PDPL_DATA_RULES.md`
- `/home/user/dealix/docs/governance/AI_MONITORING_REMEDIATION.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/SECURITY_RUNBOOK.md`
- `/home/user/dealix/docs/trust/incident_response.md`
- `/home/user/dealix/dealix/trust/audit.py`
- `/home/user/dealix/dealix/trust/pii_detector.py`
