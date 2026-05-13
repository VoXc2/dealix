# Knowledge Capital System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CTO + CSO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [KNOWLEDGE_CAPITAL_SYSTEM_AR.md](./KNOWLEDGE_CAPITAL_SYSTEM_AR.md)

## Context

Every Dealix engagement teaches us something. Without a system,
that knowledge dies on the engagement. The Knowledge Capital
System captures it as a structured asset so the next project starts
ahead. It implements the Knowledge axis of
`docs/company/DEALIX_CAPITAL_MODEL.md` and aligns with the strategic
decisions in `docs/AI_STACK_DECISIONS.md`. It is a peer to Trust and
Market capital systems.

## Knowledge Asset Types

The system tracks nine asset categories. Each is a row in the
Knowledge Ledger.

| Asset | Example |
|---|---|
| Vertical playbook | "Banking lead intelligence — 7 steps" |
| Objections | "Why we cannot trust AI on PII" — answers |
| Data patterns | "Saudi mobile numbers normalization rules" |
| Governance risks | "Approval lag patterns in regulated buyers" |
| Workflow patterns | "Sponsor → Operator → QA reviewer loop" |
| Report templates | "Monthly retainer report template v2" |
| Arabic wording examples | Approved phrasings for objections |
| Pricing insights | "Banking pays 30% Governance premium reliably" |
| Delivery lessons | "Data refresh on day 3 catches 80% of issues" |

Each asset has: title, type, source engagement, summary, evidence,
applicable verticals, owner, and reuse count.

## Post-Project Questions

Every engagement closes with five questions. Answers feed the
Knowledge Ledger.

1. What did we learn about this vertical that we did not know?
2. What new objection or risk surfaced?
3. What data or wording pattern can we reuse?
4. What pricing or scope signal informed the deal?
5. What governance or delivery lesson should be standard?

The CSM or Delivery Lead writes ≥3 entries before sign-off.

## Knowledge Update Schema

```json
{
  "knowledge_id": "kn_2026_05_acme_pdpl_lag",
  "type": "governance_risk",
  "title": "Approval lag on PDPL data exports in banks",
  "source_engagement": "eng_acme_lead_intel",
  "summary": "Banking sponsors require 2-stage internal approval
              before any PDPL-restricted dataset leaves their tenant.
              First stage is data office, second is compliance.
              Plan for 7-10 business days.",
  "evidence": [
    "Acme Bank exchange dated 2026-04-22",
    "Beta Bank email chain dated 2026-03-11"
  ],
  "applicable_verticals": ["banking", "insurance"],
  "owner": "compliance_lead",
  "reuse_count": 0,
  "first_logged": "2026-05-13",
  "last_used_in": null
}
```

## Reuse Loop

Knowledge is only capital if it gets reused.

- New proposals search the Ledger before being drafted.
- Sales scripts and battlecards refresh from top-cited objections.
- Pricing Engine premium bands recalibrate quarterly from pricing
  insights.
- Delivery checklists update from delivery lessons monthly.

Each reuse increments `reuse_count` on the source asset. Assets
with reuse_count = 0 after two quarters are archived (the lesson
did not generalize).

## Cadence

- **Per engagement close** — write ≥3 entries.
- **Weekly** — Knowledge Owner triages new entries.
- **Monthly** — top-cited objections feed sales updates.
- **Quarterly** — Ledger curation; archive stale assets.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Project retros, CSM notes | Knowledge entries | Delivery + CSM | Per close |
| Knowledge Ledger | Refreshed scripts, prompts, battlecards | CSO | Monthly |
| Pricing insights | Pricing Engine updates | CEO | Quarterly |

## Metrics

- **# knowledge entries written per close** — target ≥3.
- **Reuse rate** — % of entries reused at least once within 2
  quarters (target ≥60%).
- **Time from learning to scripted reuse** — target ≤60 days.
- **# verticals with ≥10 entries** — target ≥3.

## Related

- `docs/company/DEALIX_CAPITAL_MODEL.md` — capital model parent.
- `docs/AI_STACK_DECISIONS.md` — AI stack decisions.
- `docs/V14_COMPREHENSIVE_STRATEGIC_PLAN.md` — strategic plan.
- `docs/sales/BATTLECARDS.md` — battlecards refreshed from knowledge.
- `docs/company/IP_REGISTRY.md` — IP registry sibling.
- `docs/company/KNOWLEDGE_CAPITAL_SYSTEM.md` is paired with
  `docs/company/TRUST_CAPITAL_SYSTEM.md` and
  `docs/growth/MARKET_CAPITAL_SYSTEM.md`.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
