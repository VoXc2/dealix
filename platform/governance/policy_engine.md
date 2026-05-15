# Governance Policy Engine

## Objective

Enforce runtime policy checks before any action with business, security, or compliance impact.

## Policy Evaluation Order

1. Identity validity
2. RBAC permission check
3. Tenant boundary check
4. Data sensitivity check
5. Action risk check
6. Approval requirement check
7. Execution decision
8. Audit write

## Mandatory Governance Pipeline

`risk scoring -> policy check -> approval check -> execution -> audit log`

No external side-effect action can skip this order.

## Policy Gate Definitions

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-POL-001 | policy engine invoked for all governed actions | T-POL-001 |
| G-POL-002 | blocked actions return machine-readable reason | T-POL-002 |
| G-POL-003 | policy versions are immutable and auditable | T-POL-003 |
| G-POL-004 | emergency deny rules override lower-priority allows | T-POL-004 |

## NIST AI RMF Mapping

- Govern: policy ownership, review cadence, accountability.
- Map: use-case and risk context mapping.
- Measure: policy violation and drift rates.
- Manage: mitigation actions, escalation, and rollback paths.
