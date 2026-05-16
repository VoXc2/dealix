# Tracing Standard (OpenTelemetry-aligned)

## Objective

Ensure every workflow and agent action is traceable end-to-end using vendor-neutral telemetry.

## Required Trace Context

- `trace_id`
- `span_id`
- `tenant_id`
- `workflow_id`
- `workflow_run_id`
- `agent_id` (when applicable)
- `approval_id` (when applicable)
- `policy_decision_id`

## Span Coverage Requirements

Minimum spans for governed lead flow:
1. lead intake
2. identity/permission resolution
3. agent qualification
4. retrieval and citation assembly
5. risk scoring
6. approval wait/decision
7. execution adapter call
8. eval write
9. dashboard projection update

## Mandatory Tests

| Test ID | Check | Pass Criteria |
|---|---|---|
| T-OBS-T-001 | end-to-end trace continuity | all required spans present |
| T-OBS-T-002 | trace-agent correlation | each agent action linked |
| T-OBS-T-003 | trace-governance correlation | policy + approval spans linked |
| T-OBS-T-004 | error path tracing | failed run has trace with error attrs |

## Alert Tie-In

Trace sampling and retention must still preserve all error traces for governed workflows.
