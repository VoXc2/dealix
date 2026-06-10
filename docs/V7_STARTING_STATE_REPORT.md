# Dealix v7 — Starting State Report

**Date:** 2026-05-05
**Branch:** `claude/service-activation-console-IA2JK`
**Local HEAD:** `813ac19` (v6 batch 2 — final v6 commit)
**Production:** stale (Railway hasn't picked up the merge yet)

---

## What v6 left behind

- 12 / 12 v5 layers shipped real
- 7 v6 modules shipped real:
  - diagnostic_engine
  - company_brain_v6
  - approval_center
  - executive_reporting
  - diagnostic_workflow
  - observability_v6
  - founder dashboard v6 (extension on existing module)
  - proof_pack_v6 (HMAC + standard doc)
- 14+ founder operating docs
- ~1100 tests passing (40 batch-2 v6 tests added on top of 1067 v6 batch-1)
- Hard rules: all enforced with tests
- Forbidden-claims sweep: clean (4 REVIEW_PENDING founder-only)

## What v7 is NOT

- Not a rewrite of v6.
- Not a new architecture.
- Not a replacement of any existing module.
- Not a "more features" pass — every layer below v7 stays unchanged.

## What v7 IS

A thin orchestration layer that wires the existing 12 v5 layers + 7 v6
modules into an "AI Workforce" — 12 specialized agents under one
Orchestrator — exposed via a customer-facing demo + cost-controlled
runs + a launch board.

The 12 agents:
1. OrchestratorAgent — coordinates the rest
2. CompanyBrainAgent — wraps `company_brain_v6.build_company_brain_v6`
3. MarketRadarAgent — composes existing search_radar + geo_aio_radar
4. SalesStrategistAgent — maps brain → service → pilot offer
5. SaudiCopyAgent — Arabic/English warm-intro drafts (no cold)
6. PartnershipAgent — wraps existing partner_distribution_radar
7. DeliveryAgent — wraps `delivery_factory.build_delivery_plan`
8. ProofAgent — composes from real ProofEvent ledger
9. ComplianceGuardAgent — hard veto over forbidden actions
10. ExecutiveBriefAgent — wraps `executive_reporting.build_weekly_report`
11. FinanceAgent — wraps `finance_os.draft_invoice` (test-mode only)
12. CustomerSuccessAgent — wraps `customer_loop.advance` recommendations

Every agent has a fixed autonomy level + tool list. ComplianceGuardAgent
runs LAST and can block any output before it returns.

## Production reality

| Check | Expected | Actual | Status |
|---|---|---|---|
| `https://api.dealix.me/health` git_sha | recent SHA | `unknown` | ⏳ |
| `https://api.dealix.me/api/v1/founder/dashboard` | HTTP 200 | HTTP 404 | ⏳ |
| Local code → CI: green | green | confirmed | ✅ |

`PRODUCTION_REDEPLOY_REQUIRED=yes` — but v7 ships locally regardless.

## Hard rules that v7 must NOT break

- No live charge, no live WhatsApp/email send
- No LinkedIn automation
- No web scraping
- No purchased lists
- No cold WhatsApp
- No fake proof / fake testimonials
- No `نضمن` / `guaranteed` / `blast` / `scrape` in any output
- Pilot price 499 SAR locked until Decision Pack §S1
- Every external action: `blocked` / `draft_only` / `approval_required` / `approved_manual_action` (`approved_execute` only for internal-safe)

## v7 GO criteria

After v7 ships, the verdict block in `docs/V7_MASTER_EVIDENCE_TABLE.md`
must be:

```
DEALIX_V7_VERDICT=PASS
AI_WORKFORCE_REGISTRY=pass
ORCHESTRATOR=pass
COST_GUARD=pass
... (all PASS)
OUTREACH_GO=diagnostic_only OR yes
```

If `OUTREACH_GO=yes`: founder begins Phase E first warm intro.
If `=diagnostic_only`: founder runs free Diagnostics only until production redeploy.
If `=no`: production redeploy is hard blocker.

— Starting State Report v1.0 · 2026-05-05 · Dealix
