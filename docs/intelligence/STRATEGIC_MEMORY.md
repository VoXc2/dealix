# Strategic Memory — Intelligence · Operating Brain

**Layer:** Intelligence · Operating Brain
**Owner:** Chief of Staff
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [STRATEGIC_MEMORY_AR.md](./STRATEGIC_MEMORY_AR.md)

## Context
Strategic Memory captures what Dealix learns. Every project, every win,
every loss writes structured lessons into a small, named set of memory
files that downstream functions read before pitching, pricing, delivering,
or building. Without this discipline, lessons live in the heads of the
founders and the next hire repeats every mistake. The Capital Ledger
stores reusable artefacts; Strategic Memory stores the reasoning behind
them. See `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` and
`docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` for the downstream consumers of
these lessons, and `docs/DEALIX_OPERATING_CONSTITUTION.md` for the
constitutional requirement to compound learning.

## Memory files
Seven canonical files live in `docs/memory/`. Each is a curated, dated,
ledger-linked log — not a free-form scratchpad.

| File | Purpose | Primary consumer |
|---|---|---|
| `docs/memory/sales_lessons.md` | Sales motion learnings | Head of Revenue |
| `docs/memory/delivery_lessons.md` | Delivery execution learnings | Head of Delivery |
| `docs/memory/governance_lessons.md` | Governance and PDPL learnings | Head of Governance |
| `docs/memory/pricing_lessons.md` | Pricing experiments + outcomes | Head of Revenue |
| `docs/memory/product_lessons.md` | Product / module learnings | Head of Product |
| `docs/memory/sector_patterns.md` | Sector-specific patterns | CEO + Heads |
| `docs/memory/objections_library.md` | Sales objections + responses | Head of Revenue |

These paths are reserved. Adding a new memory file requires a written
proposal to the Chief of Staff.

## Per-project capture template
At project close (and at the end of every significant pilot or pitch),
the project owner files a Lessons Capture against the matching memory
files. The template:

```
Project: PRJ-<id>
Client: CL-<id>
Sector: <sector>
Closed: <YYYY-MM-DD>
Outcome: <won | lost | extended | churned>

What worked:
- ...

What failed:
- ...

What repeated (already seen in prior projects):
- ...

What surprised (genuinely new):
- ...

What the client valued (in their words):
- ...

What risk appeared (governance, delivery, regulatory):
- ...

What should become a template (delivery artefact):
- ...

What should become a product (module candidate):
- ...

What should become content (market-safe insight):
- ...

Linked ledger entries:
- <ledger>:<entry_id>
```

Each section is at most five bullet points. Discipline is enforced by the
Chief of Staff at the weekly review.

## Capture routing
Each section routes to specific memory files:
- "What worked / what failed / what client valued" → `sales_lessons.md`
  and `delivery_lessons.md`.
- "What risk appeared" → `governance_lessons.md` and incident review.
- "What surprised" → `sector_patterns.md` if patterned, else
  `delivery_lessons.md`.
- "What should become a template" → `delivery_lessons.md` + Capital
  Ledger asset.
- "What should become a product" → `product_lessons.md` + Productization
  Ledger candidate.
- "What should become content" → `sector_patterns.md` or
  `objections_library.md` if a recurring objection, plus
  market-safe asset in Capital Ledger.
- Pricing outcomes (win at price X, loss at price Y) →
  `pricing_lessons.md`.

## Memory hygiene
- **Dated.** Every entry carries the close date and a project ID. No
  undated lessons.
- **Ledger-linked.** Lessons reference at least one ledger entry that
  evidences them.
- **Reviewed.** The Chief of Staff reviews memory diffs weekly and flags
  unsupported claims.
- **Pruned.** Quarterly, lessons older than 18 months are reviewed for
  promotion to a playbook, demotion to an archive, or deletion when
  superseded.
- **PDPL-safe.** Client identifiers are opaque IDs; client names appear
  only where contractually permitted.

## Reading patterns
- **Before a pitch.** Revenue reads `sales_lessons.md`,
  `pricing_lessons.md`, `objections_library.md`, and the sector entry in
  `sector_patterns.md`.
- **Before kickoff.** Delivery reads `delivery_lessons.md` filtered by
  the matching sector and offer.
- **Before a new module.** Product reads `product_lessons.md` and the
  Capital Ledger for prior modules.
- **Before a governance approval.** Governance reads
  `governance_lessons.md` for prior incidents in the same shape.

## Failure modes
- **Tribal memory.** Lessons exist only in chat threads. Mitigation:
  enforced project-close capture.
- **Vanity memory.** Only wins captured. Mitigation: losses are a
  required block in the template.
- **Stale memory.** Patterns from 2024 still drive 2026 pitches.
  Mitigation: quarterly pruning.
- **Untraced claims.** "We learned X" with no ledger backing. Mitigation:
  weekly diff review.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Per-project Lessons Captures | Memory file updates | Project owner | Per project close |
| Memory files | Pre-pitch / pre-kickoff briefs | Heads | Per use |
| Memory + Capital Ledger | Productization candidates | Head of Product | Per candidate |
| Quarterly review | Pruned / promoted lessons | Chief of Staff | Quarterly |

## Metrics
- **Capture Rate** — share of closed projects with a complete Lessons
  Capture (target: 100%).
- **Memory Hit Rate** — share of pitches/kickoffs preceded by a
  documented memory read (target: 100%).
- **Ledger Link Rate** — share of memory entries with at least one
  ledger reference (target: 100%).
- **Pruning Rate** — share of >18-month entries reviewed quarterly
  (target: 100%).

## Related
- `docs/CUSTOMER_SUCCESS_PLAYBOOK.md` — downstream playbook consuming delivery lessons
- `docs/DEALIX_REVENUE_PLAYBOOK_FINAL.md` — downstream playbook consuming sales + pricing lessons
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — constitutional learning mandate
- `docs/COMPETITIVE_POSITIONING.md` — sector_patterns informs positioning
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
