# Offer + Revenue Architecture

> Combined view of how Dealix's offers ladder and how revenue diversifies
> across them. Replaces 4 fragmented docs (Offer Architecture, Revenue
> Architecture, Margin Control, Risk-Adjusted Pricing) with one.

## Offer ladder

```
Diagnostic → Sprint → Pilot → Retainer → Enterprise
```

Customers move up the ladder by demonstrating fit, paying, and earning proof.
Never quote Enterprise as the first sale.

### Front-end offers (entry, low-risk)
- **AI Ops Diagnostic** — SAR 7,500–25,000 · 5–10d.
- **Revenue Diagnostic** — SAR 3,500–7,500 · 3–5d.

### Core offers (cash engine)
- **Lead Intelligence Sprint** — SAR 9,500 · 10d.
- **AI Quick Win Sprint** — SAR 12,000 · 7d.
- **Company Brain Sprint** — SAR 20,000 · 21d.
- *(Phase 2)* **AI Support Desk Sprint** — SAR 12,000–30,000 · 14d.
- *(Phase 2)* **Workflow Automation Sprint** — SAR 15,000–50,000 · 2–4w.

### Continuity offers (recurring)
- **Monthly RevOps OS** — SAR 15,000–60,000 / mo.
- **Monthly AI Ops** — SAR 15,000–60,000 / mo.
- **Monthly Support AI** — SAR 8,000–25,000 / mo.
- **Monthly Company Brain Management** — SAR 8,000–35,000 / mo.

### Enterprise offers (custom high-value)
- **Enterprise AI OS** — SAR 85,000–300,000+ setup + SAR 35–150K/mo.
- **AI Governance Program** — SAR 35,000–150,000.
- **Multi-Branch RevOps** — Enterprise pricing.

## Revenue distribution targets

| Stage (M+) | Diagnostic | Sprint | Pilot | Retainer | Enterprise |
|-----------|----------:|-------:|------:|---------:|----------:|
| Year 1 H1 | 10% | 70% | 10% | 10% | 0% |
| Year 1 H2 | 10% | 55% | 10% | 20% | 5% |
| Year 2 | 5% | 35% | 10% | 35% | 15% |
| Year 3+ | 5% | 25% | 5% | 40% | 25% |

Long-term goal: retainers + enterprise dominate revenue; Sprints stay as
the entry pattern.

## Margin discipline

Per `docs/company/PRICING_DECISION.md`:

| Offer kind | Gross margin floor |
|-----------|-------------------:|
| Sprint | 55% |
| Retainer | 70% |
| Enterprise | 60% (higher SLA/governance burden) |
| Diagnostic | 80% (mostly time, low cost) |

Any deal below floor needs CFO + CEO sign-off + a documented reason
(strategic, anchor logo, case study rights).

### Risk-adjusted pricing premiums

| Risk added | Premium |
|-----------|--------:|
| High data sensitivity (regulated, health, financial) | +20–40% |
| Complex stakeholder approvals (≥ 3 sign-offs) | +15–30% |
| Tight timeline (compressed) | +20–50% |
| Integration required mid-sprint | Separate scope / SOW |
| Enterprise compliance (SLA + audit export) | Enterprise pricing only |
| Customer data is not AI-ready | Diagnostic or Data Cleanup first |

Never absorb risk silently. Price it or refuse it.

## Cross-links

- `docs/pricing/pricing_packages_sa.md` — detailed SAR price list
- `docs/pricing/value_metrics.md` — value-metric pricing
- `docs/company/PRICING_DECISION.md` — when to raise
- `docs/company/SERVICE_REGISTRY.md` — per-service detail
- `docs/company/MATURITY_BOARD.md` — service readiness gating
