# Governance Stack — Seven Layers

Governance inside Dealix is a stack of seven explicit layers. A capability that touches any of them without the corresponding controls is rejected.

## 1. Source Governance

Every data source carries a **Source Passport**:

- source type
- owner
- allowed use
- PII status
- sensitivity
- retention
- AI access allowed
- external use allowed

## 2. Data Governance

Every dataset entering the system passes through:

- Data Quality Score
- PII Detection
- Deduplication
- Allowed Use Check
- Retention Policy

## 3. Model Governance

Every AI call passes through:

- LLM Gateway
- Model Router
- Prompt Registry
- Output Schema
- Cost Guard
- Eval Hook
- AI Run Ledger

## 4. Agent Governance

Every agent carries:

- identity
- owner
- purpose
- allowed tools
- forbidden actions
- autonomy level
- approval requirement
- audit requirement

## 5. Workflow Governance

Every workflow carries:

- human owner
- inputs
- outputs
- approval path
- QA rubric
- proof metric
- operating cadence

## 6. Output Governance

Every output carries one decision:

```
ALLOW
ALLOW_WITH_REVIEW
DRAFT_ONLY
REQUIRE_APPROVAL
REDACT
BLOCK
ESCALATE
```

The fail-closed default is `DRAFT_ONLY`. Any module that defaults to `ALLOW` on error is a doctrine violation.

## 7. Proof Governance

Every claim has proof; every proof has a limitation.

- No proof, no claim.
- No proof, no public case.
- No proof, no retainer push.

## 8. Operating discipline

- Each layer has a named owner.
- The stack is shared across all BUs — forks are forbidden.
- The Command Center reads the live state of each layer.
- Telemetry from each layer feeds the AI Run Ledger and the Audit Trail.

## 9. Anti-patterns

- A capability that bypasses any layer "just this once."
- BU-specific layer forks driven by speed.
- Layers that exist in slides but not at runtime.
- Layer owners who do not have the authority to halt a release.

## 10. The principle

> Seven layers, one operating model. No layer is optional.
