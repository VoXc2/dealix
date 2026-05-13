# Runtime Governance Standard

## Decision vocabulary

```
ALLOW, ALLOW_WITH_REVIEW, DRAFT_ONLY, REQUIRE_APPROVAL, REDACT, BLOCK, ESCALATE
```

Fail-closed default: `DRAFT_ONLY`. `ALLOW` as failure default is a constitutional violation.

## Pre-action checks (8 questions)

source status, PII status, allowed use, claim risk, channel risk, agent autonomy, approval requirement, audit event.

## Typed surface

`endgame_os.governance_product.GovernanceDecision` + `institutional_control_os.governance_runtime.RuntimeEvaluationRecord` + `command_control_os.governance_command.GovernanceCommandRecord`.
