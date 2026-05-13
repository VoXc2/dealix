# Capacity and Hiring

> Combined model. Replaces 2 fragmented docs (Delivery Capacity Model,
> Hiring Triggers).

## Delivery capacity model

### Capacity-unit cost per service

| Service | Capacity units |
|---------|---------------:|
| Lead Intelligence Sprint | 2 |
| AI Quick Win Sprint | 2 |
| Company Brain Sprint | 4 |
| AI Support Desk Sprint *(when Sellable)* | 3 |
| Workflow Automation Sprint *(Phase 2)* | 3 |
| AI Governance Program *(Phase 3)* | 4 |
| Monthly Retainer | 1 per retainer per month |
| Diagnostic | 1 |

### Founder solo capacity

- Max active capacity: **4–5 units** simultaneously.
- Quality drops if exceeded; QA Score falls; Decision Rule 1 violated (delivering below standard).

### Rule when capacity full

Do not accept a new sprint unless one of:
1. Delivery support (engineer / CS) onboarded.
2. Scope reduced (move part to next sprint).
3. Timeline extended (with customer agreement).
4. Price raised to discourage (i.e., capacity-based pricing).
5. Outsource subset to a vetted contractor.

## Capacity Ledger

Tracked in `docs/ledgers/CAPACITY_LEDGER.md`:

```markdown
| Week | Active Projects | Units Used | Max Units | Risk Level |
|------|-----------------|-----------:|----------:|------------|
| YYYY-W## | Lead-A1, QuickWin-B2 | 4 | 5 | Low |
```

Risk level: Low (≤ 80% util), Medium (80–100%), High (≥ 100%).

## Hiring triggers

Per `docs/company/SCALE_DECISION.md` — do not hire to fix chaos. Document
the work first, then hire.

### First Delivery Analyst
Hire when:
- 3+ active projects sustained for 4 weeks.
- Same delivery tasks (intake, QA, report) repeat.
- Templates and checklists exist.
- Margin supports the hire (≤ 30% of incremental MRR).

### First Product Engineer
Hire when:
- 3+ manual workflows have repeated.
- At least 2 internal tools save measurable time.
- Product Ledger has ≥ 3 candidates scoring > 80.

### First Customer Success Lead
Hire when:
- 3+ retainers active.
- Monthly reporting cycle becomes a bottleneck.
- Customer health-score tracking needs an owner.

### First Governance Reviewer
Hire when:
- Sensitive-data projects ≥ 2 per quarter.
- Enterprise interest is real (signed Diagnostic + procurement RFP received).
- HoLegal capacity stretched.

### First SDR
Hire when:
- Founder is spending > 30% of week on cold outreach.
- Outbound volume is the bottleneck (not conversion).
- Sales playbook is documented enough for handoff.

### First AE
Hire when:
- SDR has produced consistent qualified opportunities (≥ 6 / month for 3 months).
- Founder closes ≥ 50% of those opportunities (proving the SOW closes).

## Capacity → pricing feedback loop

When capacity > 100% utilized two months running and outbound queue keeps
growing, the right answer is usually: **raise list price 20–30%** (see
`PRICING_DECISION.md`). High demand is the signal the market values you
more than today's price reflects.

## Anti-patterns

- "Just one more project, we can squeeze it in" — that's how QA scores collapse.
- Hiring before the role's work is documented — chaos × 2 people.
- Hiring AE before SDR — top of funnel must work first.
- Hiring "head of growth" before sales process is productized.
- Outsourcing QA — QA stays in-house, always.

## Owner & cadence

- **Owner**: CEO + CFO.
- **Cadence**: monthly capacity + hiring review during operating cadence.

## Cross-links

- `docs/company/SCALE_DECISION.md`
- `docs/go-to-market/saudi_gtm_12m.md` §3.4 — hiring sequence
- `docs/company/PRICING_DECISION.md` — capacity → pricing trigger
- `docs/ledgers/CAPACITY_LEDGER.md` — running log
