# Service Readiness Matrix

The single dashboard for "which services can we sell today?" Refreshed weekly
by the CEO using `scripts/verify_dealix_ready.py` output + manual scoring of
each evidence column.

## Status legend
- ✅ = evidence present and sufficient
- ⚠️ = evidence partial or under improvement
- ❌ = evidence missing

## Decision rules
- **Sellable**: total score ≥ 85 AND Governance evidence ✅ AND Demo evidence ✅
- **Beta**: total score 70–84 — single-pilot only, customer told it is pilot
- **Not Ready**: total score < 70 — do not sell, do not advertise

## Matrix (refresh weekly)

| Service | Offer | Scope | Intake | QA | Demo | Product Module | Governance | Proof Pack | Sales Page | **Score** | **Status** |
|---|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|:---:|---:|---|
| Lead Intelligence Sprint | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ | **92** | **Sellable** |
| AI Quick Win Sprint | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | **86** | **Sellable** |
| Company Brain Sprint | ✅ | ✅ | ✅ | ✅ | ✅ | ⚠️ | ✅ | ✅ | ✅ | **85** | **Sellable** |
| AI Support Desk Sprint | ✅ | ✅ | ✅ | ✅ | ❌ | ❌ | ✅ | ⚠️ | ❌ | **62** | **Not Ready** |
| AI Governance Program | ✅ | ✅ | ✅ | ⚠️ | ❌ | ⚠️ | ✅ | ⚠️ | ❌ | **64** | **Not Ready** |
| Workflow Automation Sprint | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ❌ | ❌ | **30** | **Not Ready** |
| Executive Reporting Automation | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ⚠️ | ❌ | ❌ | **28** | **Not Ready** |
| Monthly RevOps OS (retainer) | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ✅ | ❌ | ❌ | **34** | **Not Ready** |
| Monthly AI Ops (retainer) | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ⚠️ | ✅ | ❌ | ❌ | **34** | **Not Ready** |
| Enterprise AI OS | ⚠️ | ⚠️ | ❌ | ❌ | ❌ | ❌ | ⚠️ | ❌ | ❌ | **20** | **Not Ready** |

## Sellable today (3)
1. **Lead Intelligence Sprint** — SAR 9,500 — 10 days
2. **AI Quick Win Sprint** — SAR 12,000 — 7 days
3. **Company Brain Sprint** — SAR 20,000 — 21 days

## Do NOT sell yet (publicly advertise)
- Workflow Automation Sprint (Phase 2 capability)
- Executive Reporting Automation (Phase 2)
- AI Support Desk Sprint (no demo, no module — Phase 2)
- AI Governance Program (no demo — Phase 3)
- Monthly retainers as standalone first-sale (only after a successful Sprint)
- Enterprise AI OS (Phase 4)

## Beta pilots permitted (single customer, with explicit "pilot" framing)
- None currently. AI Support Desk Sprint becomes Beta once `customer_os` consolidation lands.

## Score weights (per `docs/quality/SERVICE_READINESS_SCORE.md`)

| Criterion | Weight |
|-----------|------:|
| Offer clear | 10 |
| Scope clear | 10 |
| Intake ready | 10 |
| QA checklist ready | 15 |
| Demo / sample output | 15 |
| Backing product module | 15 |
| Governance checks | 10 |
| Proof pack template | 10 |
| Sales / upsell path | 5 |
| **Total** | **100** |

## Owner & cadence
- **Owner**: CEO + HoCS.
- **Review**: weekly Monday operating cadence.
- **Escalation**: any service flipping from Sellable → Beta within a quarter is a Friday QA-board agenda item.
