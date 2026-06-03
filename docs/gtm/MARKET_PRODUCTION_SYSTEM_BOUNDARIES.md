# Market Production OS — System Boundaries

Defines what the Market Production OS **may do automatically**, what **requires
founder approval**, and what is **never permitted**. This is the contract every
script, agent, and document in `docs/gtm`, `docs/outreach`, and `docs/commercial`
must respect. It inherits from `company_os/governance/agent_permissions.md` (the
canonical permission matrix) and never weakens it.

## Trust boundary defaults

| Flag | Default | Meaning |
|------|---------|---------|
| `dry_run` | `true` | Produce artifacts only; never act on the outside world |
| `approval_required` | `true` | Founder must approve before any external-facing action |
| `send_enabled` | `false` | Real sending is off until deliverability gates pass |

## Allowed automatically (Observe / Advise / Draft)

- Research companies from **public** data only.
- Detect and classify buying signals.
- Score and rank prospects against a documented rubric.
- Match pain → product offer.
- Generate up to **250 drafts/day** (emails, follow-ups, proposal intros).
- Run quality / compliance / deliverability gates and write gate reports.
- Build approval queues, batch **plans**, daily/weekly GTM reports.
- Draft content, press angles, partner outreach (for review).

## Requires founder approval (Act with Approval)

- Any **send** of an external message (email / WhatsApp / DM).
- Any **final price**, discount, proposal, or quote.
- Enabling `send_enabled=true` for any mailbox.
- Publishing any external content, press pitch, or case study.
- Handling any client raw data / new data-processing scope.

## Never permitted (Red lines)

- Real external sending without approval.
- Cold WhatsApp automation; LinkedIn automation.
- Scraping in violation of terms; purchased lists.
- Storing secrets/API keys in code, logs, prompts, JSONL, reports, or GitHub.
- Exposing PII in logs/reports.
- Fabricated clients, case studies, or metrics.
- Guaranteed-revenue or "10x" claims; fake `Re:/Fwd:` subjects.
- Deleting or weakening tests, security, or approval gates.

## Enforcement points

| Boundary | Enforced by |
|----------|-------------|
| Forbidden claims | `tests/test_no_guaranteed_revenue_claims.py`, `scripts/draft-quality-gate.js` |
| Unsubscribe present | `tests/test_outreach_unsubscribe_required.py` |
| Suppression blocks send | `tests/test_outreach_suppression_blocks_send.py` |
| Pricing approval | `tests/test_pricing_requires_approval.py`, `governance_check.py` |
| Proposal needs mapping | `tests/test_proposal_requires_qualified_opportunity.py` |
| Send readiness ≥ P1 | `tests/test_gtm_quality_gate.py` |

A change that would let any "Never permitted" item happen is a release blocker.
