# Governance as Code — Value Realization System

**Layer:** L3 · Value Realization System
**Owner:** Head of Compliance
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [GOVERNANCE_AS_CODE_AR.md](./GOVERNANCE_AS_CODE_AR.md)

## Context
Policy documents alone do not stop unsafe AI behavior. Governance must be
executable at runtime — by the Compliance Guard Agent and inside CI. This
file defines the rule grammar Dealix uses and the planned engine layout.
It complements the constitution in
`docs/DEALIX_OPERATING_CONSTITUTION.md` and the eval discipline in
`docs/AI_OBSERVABILITY_AND_EVALS.md` and `docs/EVALS_RUNBOOK.md`.

## Principle

> Governance rules should be **executable**, **versioned**, and
> **testable** — never only "policy PDFs."

## Rule grammar (illustrative)

- `no_cold_whatsapp`
  - IF `channel = whatsapp` AND `relationship_status != consented_or_existing`
  - THEN `block`.
- `no_guaranteed_claims`
  - IF `output contains guaranteed_sales_language`
  - THEN `rewrite_or_block`.
- `no_source_no_answer`
  - IF `answer has no source`
  - THEN `insufficient_evidence`.
- `pii_redaction_required`
  - IF `output contains phone | email | person_name`
  - AND `destination in {report, public}`
  - THEN `redact_or_require_basis`.

## Future structure

```
governance_os/
  rules/
    no_cold_whatsapp.yaml
    no_guaranteed_claims.yaml
    no_source_no_answer.yaml
    pii_redaction_required.yaml
  engine.py
  tests/
```

- `rules/*.yaml` — declarative rules with id, version, trigger, action.
- `engine.py` — evaluates rules and emits a `GuardVerdict`.
- `tests/` — fixtures that lock behavior; CI runs them on every change.

## Rule lifecycle

```
propose → review → test → publish → pin → monitor → deprecate
```

Each rule has an owner, a public ID, and a version. Changes ship via PR
with new fixtures. The Compliance Guard Agent loads the pinned policy
bundle and reports the version inside every verdict.

## Anti-patterns

- Hidden rules baked into prompts.
- Rules without tests.
- Rules without owners.
- Changing rules in production without a versioned bundle.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Rule proposals | Reviewed YAML rules | Head of Compliance | Per change |
| Engine + rules | GuardVerdict | Compliance Guard Agent | Per action |
| Test fixtures | CI pass/fail | Eng + Compliance | Per PR |
| Production runs | Rule effectiveness telemetry | Control Tower | Continuous |

## Metrics
- Rule Coverage — % of action classes mapped to at least one rule.
- Test Coverage — % of rules with fixtures.
- Rule Drift — diff between intended policy and shipped YAML.
- Block-to-Cause Closure — rules removed/refactored after root cause fix.

## Related
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — source of rules
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — eval coverage
- `docs/EVALS_RUNBOOK.md` — eval execution
- `docs/product/agent_cards/compliance_guard_agent.md` — runtime executor
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
