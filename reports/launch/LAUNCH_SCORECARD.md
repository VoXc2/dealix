# Launch Scorecard

Evidence-based readiness score. Computed by `scripts/checks/check_launch_readiness.py`
from files that actually exist. Tiers: **present = 1.0**, **partial = 0.4**,
**missing = 0.0** of the weight.

**Last computed:** 2026-06-03 · **Score: 44.6 / 100 (≈ 45%) → Not Ready (band < 60)**

---

## Weighted scoring

| Domain | Weight | Tier | Points | Success condition |
|--------|------:|------|------:|-------------------|
| Website | 10 | present | 10.0 | Pages build and work |
| Core 5 Systems | 10 | partial | 4.0 | Each system has price + delivery |
| Business OS Catalog | 8 | missing | 0.0 | 40 internal systems linked |
| Business Need Intelligence | 12 | missing | 0.0 | 25 Needs + 50 Sprints |
| Account Intelligence | 12 | partial | 4.8 | Account Pack Contract |
| Contact Discovery | 8 | partial | 3.2 | No invented contacts |
| Outreach Quality | 8 | partial | 3.2 | No claims + Top 100 |
| Call / Proposal | 8 | partial | 3.2 | Call Brief + Proposal Gate |
| Delivery | 8 | partial | 3.2 | Delivery Gate + Weekly Report |
| Finance / Metrics | 5 | partial | 2.0 | Cash Priority + Metrics |
| Security / Privacy | 7 | present | 7.0 | Untrusted data + suppression |
| CI/CD | 4 | present | 4.0 | Actions + checks |
| **TOTAL** | **100** | | **44.6** | |

---

## Bands

```txt
90–100 = Full Launch Ready
85–89  = Controlled Launch Ready
75–84  = Soft Launch Ready
60–74  = Internal Dry Run Only
<60    = Not Ready
```

**44.6 → below 60.** Capability is not yet at Soft Launch. However, because the
**safety hard-gates pass** (no external sending, no invented contacts, no
guaranteed claims, suppression + untrusted-content policies present), an
**Internal Dry Run** (internal, review-only) is the recommended floor.

---

## Evidence per dimension

- **Website** — `index.html`, `src/pages/LandingPage.tsx`, `src/pages/Dashboard.tsx`; `npm run build` passes.
- **Core 5 Systems** — `company_os/marketing/one_pagers/one_pager_arabic.md`, `company_os/revenue/proposals.json` (P1=2,500 SAR, P2 retainers), `company_os/delivery/p1_delivery_sop.md`. Only 2 of 5 productized.
- **Business OS Catalog** — not present.
- **Business Need Intelligence** — not present.
- **Account Intelligence** — `company_os/revenue/prospects.csv` (basic list only).
- **Contact Discovery** — `data_handling_checklist.md`, `suppression_policy.md`; role-based contacts only.
- **Outreach Quality** — `outreach_queue.json`, `scripts/generate_outreach_queue.py`, `objections.json`; no executable gate.
- **Call / Proposal** — `proposals.json` templates; no call brief / proposal gate code.
- **Delivery** — `p1_delivery_sop.md`, `proof_pack_template.md`, `client_success_plan.md`.
- **Finance / Metrics** — `scripts/revenue_scorecard.py`, `company_os/finance/unit_economics.md`.
- **Security / Privacy** — `agent_permissions.md`, `pdpl_checklist.md`, `data_handling_checklist.md`, `external_content_policy.md`, `scripts/governance_check.py`.
- **CI/CD** — `.github/workflows/launch-readiness.yml`, `scripts/checks/check_launch_readiness.py`.

---

## How to raise the score (highest leverage first)

1. Business Need Intelligence (12) — largest single weight, currently 0.
2. Account Intelligence (12) — Account Pack Contract → partial→present.
3. Business OS Catalog (8) — currently 0.
4. Outreach / Call / Delivery (8 each) — build the executable gates.

> Re-run the checker after each change; this file is written to match its output.
