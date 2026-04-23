# Dealix Launch Gates — v3.0.0 Primitive Launch

**Snapshot date:** 2026-04-23
**Current status:** 12/30 gates closed. **Launch is NOT complete.**
**Rule:** no "launched" claim until **≥24/30** gates closed, including all P0 items.

---

## Legend
- ✅ **Closed** — implemented, verified, measurable, connected to a real outcome
- 🟡 **Partial** — code exists but not wired / not measured / not verified in prod
- 🔴 **Open** — not started or explicitly incomplete
- 🚫 **Blocked** — waiting on external dependency

---

## Technical Readiness (5/8 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| T1 | `/health/deep` green in prod | ✅ | `postgres 23ms, redis 80ms, llm_providers` all green |
| T2 | v3.0.0 tagged + released | ✅ | [Release v3.0.0](https://github.com/VoXc2/dealix/releases/tag/v3.0.0) |
| T3 | CI green on main | ✅ | `gh run list --repo VoXc2/dealix --branch main` all success |
| T4 | SSH hardened | ✅ | PasswordAuth=no, PermitRootLogin=prohibit-password, MaxAuthTries=3 |
| T5 | DLQ + retry + idempotency wired in prod | 🟡 | Code merged in `feat/launch-hardening`; needs prod deploy + fault-injection test |
| T6 | k6 load test run against prod | 🔴 | DoD: 100 rps sustained for 5 min with p95 <500ms |
| T7 | Rollback procedure tested end-to-end | 🔴 | DoD: Scenario 2 in RUNBOOK executed, ≤5 min |
| T8 | Backup restore tested on staging | 🔴 | DoD: Scenario 5 drill executed, row counts validated |

## Security (4/7 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| S1 | Webhook signatures enforced | ✅ | HubSpot, Calendly, Moyasar all verify HMAC or secret_token |
| S2 | API keys + rate limits | ✅ | `APIKeyMiddleware` + `slowapi` applied on all routers |
| S3 | UFW + fail2ban active | ✅ | 22/80/443 only; sshd jail banned 15 IPs |
| S4 | Secrets rotated post-tag | ✅ | `scripts/rotate_secrets.sh` run 2026-04-23 (API_KEYS, HUBSPOT, CALENDLY, N8N, JWT) |
| S5 | Secrets vault (not `.env`) | 🔴 | P1 — after first paid deal |
| S6 | CORS origin review | 🟡 | Settings use `cors_origin_list`; needs explicit prod allowlist audit |
| S7 | Pen test (external) | 🔴 | P2 — post-launch |

## Observability (2/5 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| O1 | OpenTelemetry + Sentry instrumented | ✅ | `dealix.observability.setup_sentry/setup_tracing` active in `create_app` |
| O2 | `/admin/costs` endpoint live | ✅ | Returns per-model spend, cache hit ratio |
| O3 | PostHog funnel live (7 events) | 🟡 | Client code + event constants ready; no event fired from prod yet |
| O4 | Daily cost alert | 🔴 | DoD: Slack/email ping if daily spend >$10 |
| O5 | SLO defined + dashboarded | 🔴 | DoD: e.g. 99.5% availability on `/health`; tracked in status page |

## GTM / Funnel (0/5 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| G1 | Pricing endpoint accessible | 🟡 | `/api/v1/pricing/plans` merged in `feat/launch-hardening`; needs prod deploy |
| G2 | Checkout functional (1 SAR pilot) | 🔴 | DoD: live Moyasar invoice → payment_url → webhook → PostHog PAYMENT_SUCCEEDED |
| G3 | E2E Calendly + HubSpot with real lead | 🔴 | DoD: 1 real lead traverses Calendly→HubSpot→PostHog end-to-end |
| G4 | 10 real leads captured | 🔴 | Commercial top bottleneck |
| G5 | 1 paid deal | 🔴 | **The only gate that matters commercially** |

## Support / Incident (0/4 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| I1 | Runbook (5 scenarios) | 🟡 | `docs/RUNBOOK.md` merged in `feat/launch-hardening`; needs review by Sami |
| I2 | On-call / incident contact | 🔴 | DoD: single contact + escalation documented |
| I3 | Public status page | 🔴 | Can use UptimeRobot public page initially |
| I4 | Customer support channel | 🔴 | DoD: published email / WhatsApp number |

## Governance (1/2 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| GV1 | Approvals Gate on outbound >50 / risk ≥0.7 / critical actions | 🟡 | `dealix/governance/approvals.py` + admin endpoints merged in `feat/launch-hardening`; 11/11 unit tests pass; needs prod deploy + policy audit log |
| GV2 | Change discipline (no direct prod edits) | ✅ | `main` protected, runbook forbids in-place edits except documented `.env` LLM failover |

## Rollback / Recovery (1/3 closed)

| # | Gate | Status | Evidence / DoD |
|---|---|---|---|
| R1 | Backup branch preserved | ✅ | `server-backup-20260423-084442` with 20 historical commits |
| R2 | DB restore tested | 🔴 | Covered by T8 drill |
| R3 | Previous version rollback <5 min | 🔴 | Covered by T7 drill |

---

## Summary

- **Closed:** 13/30
- **Partial:** 5/30 (need deploy/verification)
- **Open:** 12/30
- **Blocked:** 0/30

**Gap to Launch Claim (24/30):** 11 gates.
**Gap to Paid-Validated Launch (G5):** 1 real deal.

## Next 72-hour execution plan

**Day 0 (today, D0):**
- Merge `feat/launch-hardening` → deploy → closes T5, O3 (partial→full), G1, I1, GV1.
  - Target: **+5 gates → 18/30**

**Day 1 (D+1):**
- T8 backup restore drill on staging → closes T8.
- T7 rollback drill (via staging deploy+rollback) → closes T7.
- G2 Moyasar 1 SAR pilot → closes G2 + sends first real PAYMENT_SUCCEEDED PostHog event.
  - Target: **+3 gates → 21/30**

**Day 2 (D+2):**
- G3 E2E with 1 real lead (Sami or friend) → closes G3.
- O4 daily cost Slack ping → closes O4.
- I2/I3 on-call + UptimeRobot public page → closes I2, I3.
- T6 k6 run → closes T6.
  - Target: **+5 gates → 26/30**

**After D+2:** remaining 4 gates (S5, S7, G4, G5) are commercial, not technical. They close with real customers, not with code.
