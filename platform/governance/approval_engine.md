# Approval Engine Specification

## Purpose

Route high-risk actions to human approval before execution and record full decision trail.

## Approval States

- `not_required`
- `pending`
- `approved`
- `rejected`
- `expired`
- `cancelled`

## Rule Model

Approval rule fields:
- `rule_id`
- `risk_level`
- `action_type`
- `approver_roles`
- `sla_seconds`
- `escalation_policy`

## Mandatory Gates

| Gate ID | Requirement | Test ID |
|---|---|---|
| G-APR-001 | high-risk action cannot execute without approval | T-APR-001 |
| G-APR-002 | approval decision captures actor/time/reason | T-APR-002 |
| G-APR-003 | expired approvals auto-cancel execution | T-APR-003 |
| G-APR-004 | approval events correlated to trace and audit ids | T-APR-004 |

## Execution Contract

- If `pending`: workflow pauses (`paused_for_approval`).
- If `approved`: execution resumes with approval token.
- If `rejected` or `expired`: action blocked and compensated as needed.

## Evidence

- Approval request/response records.
- Audit logs linking `approval_id` to `action_id`.
- Test report covering approve/reject/expire paths.
