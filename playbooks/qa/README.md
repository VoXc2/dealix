# QA Playbook (Revenue OS)

## Outcome

Ensure task quality, governance compliance, and reliability before scale-up.

## QA Coverage

1. Functional checks for workflow steps.
2. Governance checks for risk/policy/approval.
3. Tenant-isolation negative tests.
4. Observability checks (trace/metrics/logs).
5. Eval checks (quality + compliance + impact).

## Test Pack (Minimum)

- 10 sample leads across different quality tiers
- 2 approval-required cases
- 2 policy-denied cases
- 1 CRM retry scenario
- 1 rollback drill

## Exit Criteria

- Pass all governance gates
- Zero cross-tenant leakage
- Eval report generated and reviewed
