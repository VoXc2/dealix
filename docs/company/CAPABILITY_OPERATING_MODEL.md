# Dealix Capability Operating Model

> **Shift in framing**: stop asking "what service are we selling?" — ask
> "what business capability are we building inside the customer?"
> 
> Dealix builds 7 repeatable AI-enabled business capabilities. Each Sprint
> is the **first step** toward maturing one of those capabilities — not a
> standalone deliverable.

## The 7 customer capabilities

1. **Revenue Capability** — identify, rank, and convert opportunities into pipeline.
2. **Customer Capability** — understand and respond to customers with quality and speed.
3. **Operations Capability** — automate recurring work; reduce errors.
4. **Knowledge Capability** — turn scattered knowledge into cited answers.
5. **Data Capability** — prepare data for decisions and AI.
6. **Governance Capability** — use AI safely with approvals, logs, lawful basis.
7. **Reporting Capability** — give executives the truth in time to act.

## Service ↔ Capability mapping

| Service | Capability built | Initial level target | After Retainer target |
|---------|------------------|---------------------:|----------------------:|
| Lead Intelligence Sprint | Revenue | L1 → L3 | L4–L5 |
| AI Quick Win Sprint | Operations | L0–L1 → L3 | L4 |
| Company Brain Sprint | Knowledge | L1 → L3 | L4 |
| AI Support Desk Sprint *(Phase 2)* | Customer | L1 → L3 | L4 |
| AI Governance Program *(Phase 3)* | Governance | L0–L2 → L4 | L5 |
| Data Cleanup Sprint | Data | L1 → L3 | L4 |
| Executive Reporting Automation *(Phase 2)* | Reporting | L1 → L3 | L4 |

## Capability Maturity Levels (per customer × capability)

| Level | Name | Description |
|------:|------|-------------|
| 0 | Absent | No process, owner, data, or metric |
| 1 | Manual | Work happens manually and inconsistently |
| 2 | Structured | Process, owner, inputs documented |
| 3 | AI-Assisted | AI helps produce drafts/reports/scoring |
| 4 | Governed AI Workflow | AI embedded with approvals + QA + audit |
| 5 | Optimized Operating System | Recurring, measured, improving, partially self-serve |

## Sales reframe

Stop: "We sell a Lead Intelligence Sprint."
Start: "We take your Revenue Capability from Level 1 to Level 3 in 10 days."

This reframe:
- Lifts the conversation from features to outcomes.
- Naturally creates the retainer path (Level 4 → 5).
- Justifies higher prices (capability-building, not deliverable-shipping).
- Distinguishes Dealix from agencies (who sell L1→L2 maintenance, not maturity transitions).

## Per-customer artifact: Capability Roadmap

Every paying customer gets `clients/<codename>/CAPABILITY_ROADMAP.md`:

```markdown
# Capability Roadmap — <codename>

## Current capability levels (assessment from Diagnostic)
- Revenue: __
- Customer: __
- Operations: __
- Knowledge: __
- Data: __
- Governance: __
- Reporting: __

## First Sprint
- Capability targeted:
- Target level after Sprint:

## Next 30 days (Pilot)
## Next 90 days (Retainer)
## Long-term (Enterprise)
```

## Cross-links

- `docs/services/ai_ops_diagnostic/offer.md` — Capability Assessment runs inside the Diagnostic
- `docs/company/SERVICE_REGISTRY.md` — each service's capability mapping
- `docs/strategy/dealix_maturity_and_verification.md` — Dealix-side 5-level maturity
- `docs/growth/CLIENT_JOURNEY.md` — capability progression aligns with journey
