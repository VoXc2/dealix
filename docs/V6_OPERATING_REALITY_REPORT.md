# Dealix v6 — Operating Reality Report

**Generated:** 2026-05-05
**Branch:** `claude/service-activation-console-IA2JK`
**Local HEAD:** `d08b291b3eaa177a8b3cb6dbf825e8fdc9343f48`

---

## What is this report?

The first deliverable of v6 — Operating Revenue Loop. This is the
honest answer to: *can the founder start selling tomorrow?*

The format is fixed:
- Local code reality (git, tests, linters)
- Production reality (curl /health, sample v5 endpoint)
- Founder tooling reality (each CLI runs cleanly)
- GO / NO-GO for first 3 diagnostics

No prose. No narrative. Just measurements.

---

## 1. Local code reality

| Check | Expected | Actual | Status |
|---|---|---|---|
| Branch | `claude/service-activation-console-IA2JK` | `claude/service-activation-console-IA2JK` | ✅ |
| Local HEAD | latest tip | `d08b291` | ✅ |
| Bytecode compiles | no syntax error | passes (`python -m compileall`) | ✅ |
| Full pytest | ≥ 1022 passed, ≤ 8 skipped, ≤ 3 xfailed | 1022 passed, 6 skipped, 3 xfailed | ✅ |
| Forbidden-claims sweep | clean (4 REVIEW_PENDING founder-only) | clean | ✅ |
| Service Readiness Matrix | 32 / 0 live / 1 pilot / 7 partial / 24 target | as expected | ✅ |
| SEO required-gap | 0 | 0 | ✅ |

---

## 2. Production reality

| Check | Expected | Actual | Status |
|---|---|---|---|
| `https://api.dealix.me/health` | HTTP 200 + `git_sha=<latest>` | HTTP 200 + `git_sha=unknown` | ⚠️ |
| `https://api.dealix.me/api/v1/customer-loop/status` | HTTP 200 | HTTP 404 | ⏳ |
| `https://api.dealix.me/api/v1/founder/dashboard` | HTTP 200 | HTTP 404 | ⏳ |
| `https://api.dealix.me/api/v1/diagnostic/status` | HTTP 200 | HTTP 404 | ⏳ |

**Verdict:** Production runs the **pre-PR-139 build**. Founder must
trigger Railway "Redeploy from latest commit" to pick up the merged
v5 + Phase H/I/J/K/L/M code.

---

## 3. Founder tooling reality (local)

| Tool | Run-clean? | Notes |
|---|---|---|
| `python scripts/dealix_status.py` | ✅ | bilingual snapshot prints, exit 0 |
| `python scripts/dealix_smoke_test.py --base-url <local>` | ✅ | (cross-platform) |
| `python scripts/dealix_snapshot.py --print` | ✅ | JSON snapshot well-formed |
| `python scripts/dealix_diagnostic.py --list-bundles` | ✅ | catalog renders |
| `python scripts/dealix_diagnostic.py --company X --sector b2b_services --region riyadh --pipeline-state Y` | ✅ | bilingual brief renders |
| `python scripts/dealix_invoice.py --email A --amount-sar 499 --description "..."` | ✅ | refuses sk_live_ without `--allow-live` |
| `python scripts/dealix_morning_digest.py --print` | ✅ | digest markdown renders |
| `python scripts/dealix_proof_pack.py --customer-handle X` | ✅ | exit 1 on no events; 0 on assemble |
| `bash scripts/post_redeploy_verify.sh` | ⏳ | requires production redeploy first |
| `make help` | ✅ | shows all v5- targets |

---

## 4. v5 endpoint perimeter (local in-process)

| Layer | `/status` reachable | guardrails advertised |
|---|---|---|
| customer_loop | ✅ | ✅ |
| role_command | ✅ | ✅ |
| service_quality | ✅ | ✅ |
| agent_governance | ✅ | ✅ |
| reliability | ✅ | ✅ |
| vertical_playbooks | ✅ | ✅ |
| customer_data | ✅ | ✅ |
| finance | ✅ | ✅ |
| delivery_factory | ✅ | ✅ |
| proof_ledger | ✅ | ✅ |
| gtm | ✅ | ✅ |
| security_privacy | ✅ | ✅ |
| diagnostic | ✅ | ✅ |
| company_brain | ✅ | ✅ |
| founder | ✅ | ✅ |
| search_radar | ✅ | ✅ |
| self_growth | ✅ | ✅ |

(Re-verified by `tests/test_v5_endpoint_perimeter.py` — 34 cases passing.)

---

## 5. Production blockers

| # | Blocker | Owner | Fix |
|---|---|---|---|
| 1 | Railway hasn't picked up `5dfea2d` (PR #139 merge) or any subsequent commit | Founder | Open Railway → Deployments → "Redeploy from latest commit" |
| 2 | After redeploy, `git_sha` should switch from `"unknown"` to the real SHA | Founder | Verify via `curl /health` |
| 3 | After redeploy, `bash scripts/post_redeploy_verify.sh` must return verdict ✅ | Founder | Run after step 2 |

**No code blockers.** All 17 v5 + v6 modules ship green locally.

---

## 6. GO / NO-GO for first 3 diagnostics

| Pre-condition | Pass? |
|---|---|
| All v5 endpoints reachable LOCALLY | ✅ |
| Diagnostic CLI runs end-to-end | ✅ |
| No live action enabled (charge / WhatsApp / email / LinkedIn / scrape) | ✅ |
| Forbidden-claims sweep clean | ✅ |
| Founder runbook + Phase E checklist + day-by-day playbook in place | ✅ |
| SCHEMA.example.json + ANNOTATED_EXAMPLE.md exist | ✅ |
| Production redeploy complete | ⏳ (founder action) |

**Verdict for diagnostics:** **GO — even before Production redeploy.**
The Diagnostic CLI is local; the founder runs `python scripts/dealix_diagnostic.py`
directly. Production redeploy is required only for the founder
dashboard at `dealix.me/founder-dashboard.html` to fetch live data.

**Verdict for first paying pilot:** **GO once production redeployed.**
Manual Moyasar test-mode invoice via `scripts/dealix_invoice.py` works
without production. Live customer-facing dashboard requires production.

---

## 7. What's NOT yet measured

The following are not yet wired into the operating reality report
(scheduled for future v6 phases):

- ⏳ Time-to-first-response per inbound lead
- ⏳ Lead → Diagnostic conversion rate
- ⏳ Diagnostic → Pilot conversion rate
- ⏳ Pilot → Paid conversion rate
- ⏳ Founder time per customer

These metrics begin populating from real Pilot #1 data (Phase E execution).

---

## Final operating reality verdict

```
DEALIX_V6_OPERATING_REALITY=GO_FOR_DIAGNOSTICS_PENDING_PRODUCTION_REDEPLOY
LOCAL_BUILD_HEALTH=pass
PRODUCTION_BUILD_HEALTH=stale (waiting on Railway redeploy)
LOCAL_TOOLING_HEALTH=pass
TESTS=1022_passed_6_skipped_3_xfailed
NEXT_FOUNDER_ACTION=Trigger Railway redeploy, then start Phase E with first warm intro.
```

— Operating Reality Report v1.0 · 2026-05-05 · Dealix
