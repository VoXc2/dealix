# Quality Review Board

The "lawful authority" that can block a delivery. Even if the founder is the
only reviewer today, the role of QA Reviewer is separate from the role of
Delivery Owner. The QA Reviewer's signature is required on every handoff.

## Mandate

> No client-facing output is delivered below Dealix standard. The Quality
> Review Board has the authority to block any delivery that fails the 5 QA
> gates or scores below 80/100. This authority cannot be overridden by the
> Delivery Owner — only by the CEO with written exception.

## Composition

- **QA Reviewer** (named per project). Cannot be the same person as the Delivery Owner.
- **Compliance Reviewer** (optional second pair of eyes for high-risk deliveries — outbound communication, PII, regulated industries).
- **CEO** (final escalation; rarely invoked).

## The 5 QA gates (per `auto_client_acquisition/delivery_factory/qa_review.py`)

### Business QA
- Does the output answer the customer's actual problem?
- Is the KPI clearly stated?
- Is the next action explicit?
- Is the executive summary clear to a non-technical reader?
- Is the upsell path documented?

### Data QA
- Is every record sourced?
- Are duplicates handled (and reported)?
- Are missing fields documented?
- Is PII detected and (where required) redacted via `dealix/trust/pii_detector.py`?
- Is lawful basis (PDPL Art. 5) recorded?
- Is the Data Quality Score ≥ 90 on the cleaned dataset?

### AI QA
- Are outputs accurate (sampled against truth set when available)?
- Are hallucinations caught (citations where applicable, "no source = no answer" honored)?
- Is the AR tone professional and sector-appropriate?
- Are edge cases tested (empty input, malformed input, foreign characters)?

### Compliance QA
- Are there any forbidden claims (auto-checked via `dealix/trust/forbidden_claims.py`)?
- Is PDPL Art. 13/14 compliance honored for any outbound action?
- Is PII absent from reports?
- Is human approval logged for side-effect actions?
- Is the audit trail complete and queryable in the event store?

### Delivery QA
- Are all SOW-listed deliverables present?
- Is the executive report clear to a non-technical reader?
- Does the customer know the next 30-day action in writing?
- Is the handoff session scheduled or completed?
- Is the renewal / next-step proposal drafted?

## Scoring

Total score / 100 per `docs/quality/SERVICE_READINESS_SCORE.md`. Floor for shipping: **80**. Target: **85+** (Sellable). World-class: **90+** (Scalable).

## Decision options

- **APPROVED** — ship.
- **REVISE** — return to Delivery Owner with a numbered list of specific fixes; cannot ship until re-reviewed.
- **BLOCKED** — Hard Fail triggered. Cannot ship even with revisions until the underlying violation is resolved AND root-cause documented.

## Hard Fails (instant block — no matter the score)

- PII surfaced in any deliverable.
- Forbidden claim ("نضمن", "guarantee", "100%", "best in", "risk-free") in any output.
- Source-less answer in Company Brain.
- Unsafe automation (external action without approval) shipped.
- No Proof Pack in `clients/<client>/proof_pack.md`.
- Customer doesn't know the next action.

## Process

```
Output produced
  → QA Reviewer fills 5-gate checklist
  → Score computed (use qa_review.py if pure-Python, or manual on `docs/services/<offer>/qa_checklist.md`)
  → Decision: APPROVED / REVISE / BLOCKED
  → Decision recorded in `clients/<client>/delivery_approval.md`
  → On APPROVED: Delivery Owner runs handoff
  → On REVISE: fix-loop with timestamped iterations
  → On BLOCKED: CEO escalation within 24 hours
```

## Delivery Approval template

Lives at `clients/<client_codename>/delivery_approval.md`:

```markdown
# Delivery Approval — <client_codename> — <service>

| Gate | Status | Notes |
|------|:------:|-------|
| Business QA | PASS / REVISE / FAIL | |
| Data QA | PASS / REVISE / FAIL | |
| AI QA | PASS / REVISE / FAIL | |
| Compliance QA | PASS / REVISE / FAIL | |
| Delivery QA | PASS / REVISE / FAIL | |

| Quality Score | /100 |
| Hard Fail triggered | yes / no |

Decision: APPROVED / REVISE / BLOCKED
Reviewer: __________  Date: ____
Delivery Owner: __________
```

## Cadence

- Reviews happen per project at end of Stage 5 (Validate).
- Weekly QA scoreboard reported in `WEEKLY_OPERATING_REVIEW.md`.
- Monthly: which gate caught the most issues? → drives template/process improvement.

## Cross-links

- `auto_client_acquisition/delivery_factory/qa_review.py` — code-side QA model
- `docs/strategy/dealix_delivery_standard_and_quality_system.md` — canonical 5-gate + 100-pt rubric
- `docs/quality/QUALITY_STANDARD.md`
- `docs/quality/SERVICE_READINESS_SCORE.md`
- `docs/governance/APPROVAL_MATRIX.md`
