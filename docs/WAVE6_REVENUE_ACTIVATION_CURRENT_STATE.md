# Wave 6 — Revenue Activation · Current State (Phase 0)

**Date:** 2026-05-07
**Pre-Wave-6 HEAD:** `2e13ea5 feat(product): finalize non-breaking ultimate productization upgrade (Wave 5)`
**Branch:** `claude/service-activation-console-IA2JK`

---

## Pre-flight verifier baseline

| Verifier | Result |
|---|---|
| Wave 5 ULTIMATE_UPGRADE | PASS (30/30) |
| Wave 4 INTEGRATION_UPGRADE | PASS (26/26) |
| Wave 3 FULL_OPS_10_LAYER | PASS (18/18) |
| Customer Experience Final Audit | PASS |
| test_constitution_closure.py | 16/16 |
| test_landing_forbidden_claims.py | 3/3 |
| Cumulative test count | 340+ green |

## What's ready for demo (today)

**Customer-facing surfaces that work in DEMO mode immediately:**
- `/customer-portal.html` — 9 sections + 3-state UX (DEMO/SIGNED_UP/LIVE)
- `/executive-command-center.html` — 15 sections + 4-state UX
- `/launchpad.html` — closed-package strategic depth
- `/diagnostic.html` + `/diagnostic-real-estate.html` — 6-question intake
- `/start.html` — Sprint signup form (manual confirmation)
- `/proof.html` — Proof Pack flywheel (empty until first paid customer)

**Backend endpoints used in the demo:**
- `GET /api/v1/full-ops-radar/score` — Full-Ops Score (1 number CEO understands)
- `GET /api/v1/full-ops-radar/weaknesses` — Weakness Radar
- `GET /api/v1/executive-command-center/{handle}` — 15-section ECC view
- `GET /api/v1/customer-portal/{handle}` — 8-section portal + 14-key enriched_view
- `POST /api/v1/whatsapp-decision/brief` — internal admin Saudi-Arabic brief
- `POST /api/v1/leadops/run` — qualify a single warm-intro lead
- `POST /api/v1/support-journey/answer` — 7-stage support routing demo
- `POST /api/v1/tool-guardrails/check` — show every tool call gated

## What's ready for pilot (after first paid customer)

- 7-Day Revenue Proof Sprint workflow (Wave 3 service_sessions)
- Manual payment confirmation flow (Wave 3 payment_ops)
- Daily Decisions queue (Wave 3 approval_center)
- Customer Brain snapshot per customer (Wave 3 customer_brain)
- Proof Ledger with consent_signature hash-binding (Wave 3 proof_ledger)
- Case Study Engine with sales library (Wave 3 case_study_engine)
- Revenue Profitability + Gross Margin per service (Wave 5)
- Tool Guardrail Gateway (Wave 5)
- Support Journey 7-stage routing (Wave 5)

## What stays MANUAL after Wave 6

- All external WhatsApp / Email / LinkedIn / call sends (NO_LIVE_SEND)
- Moyasar payment confirmation (NO_LIVE_CHARGE — founder uploads evidence + flips state)
- Case study consent signature acquisition
- LinkedIn outreach (NO automation, NO scraping)
- P0 support escalations (founder reviews each)
- First 3 paid pilots — founder onboards personally

## What must NOT be automated yet

- WhatsApp customer outbound (NO_LIVE_SEND constitutional gate)
- Gmail live send (NO_LIVE_SEND)
- LinkedIn anything (NO_LINKEDIN_AUTO)
- Moyasar live charge (NO_LIVE_CHARGE — must use bank transfer + manual confirm or moyasar_test mode)
- Scraping competitor sites (NO_SCRAPING)
- Cold WhatsApp / email / LinkedIn outreach (NO_COLD_X)
- Fake testimonials / case studies (NO_FAKE_PROOF)
- Guaranteed revenue claims (Article 8)
- LLM-generated narratives without forbidden-token scrub (Wave 5 P11 already enforces)

## Demo entrypoints (founder uses these for warm-intro #1)

### Public demo (no auth)
```
https://dealix.me/customer-portal.html
https://dealix.me/executive-command-center.html
```

### Signed-up state (after diagnostic)
```
https://dealix.me/customer-portal.html?org=<handle>
https://dealix.me/executive-command-center.html?org=<handle>
```

### LIVE state (after paid pilot)
```
https://dealix.me/customer-portal.html?org=<handle>&access=<token>
https://dealix.me/executive-command-center.html?org=<handle>&access=<token>
```

### Internal admin (founder only, never customer)
```
POST /api/v1/whatsapp-decision/brief        — "وش الوضع اليوم؟"
GET  /api/v1/full-ops-radar/score           — Full-Ops Score
GET  /api/v1/full-ops-radar/weaknesses      — Weakness Radar
GET  /api/v1/leadops/reliability            — pipeline health
GET  /api/v1/revenue-profitability/radar    — at-risk + unprofitable services
```

## Wave 6 deliverables (this addendum)

| Phase | Deliverable | What it produces |
|---|---|---|
| 1 | Real Demo Runbook (AR/EN) | 15-min script for warm-intro demo |
| 2 | First Prospect Intake template | gitignored JSON for one prospect |
| 3 | AI Ops Diagnostic generator | deterministic 1-page diagnostic |
| 4 | 499 SAR Pilot Brief generator | markdown brief with terms |
| 5 | Manual Payment Confirmation script | enforces no-fake-revenue state machine |
| 6 | Delivery Session Kickoff script | gates delivery on payment_confirmed |
| 7 | Proof Pack generator (post-pilot) | empty if no proof events |
| 8 | Demo Outcome Logger | gitignored JSONL with redacted PII |
| 9 | Pilot→Monthly Upsell Script (AR/EN) | objection-handling crib sheet |
| 10 | Revenue Activation Verifier | wave6_revenue_activation_verify.sh |
| 11 | Evidence Table | this Wave's proof |
| 12 | Run all | full pytest + verifiers |
| 13 | Commit + push | single commit |

## Acceptance for Phase 0

- [x] HEAD recorded: `2e13ea5`
- [x] Wave 5 verifier still PASS confirmed
- [x] Working tree clean
- [x] No code changes in this phase
- [x] Demo entrypoints captured
