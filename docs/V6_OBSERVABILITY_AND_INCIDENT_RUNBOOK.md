# V6 Observability & Incident Runbook

> Every action in Dealix produces a structured trace. Every incident
> has a tier (P0/P1/P2/P3) and a runbook entry. No PII in logs.

**Date:** 2026-05-05
**Owner:** Founder + on-call (initially: Founder)

---

## 1. The trace contract

Every action emits these fields (where applicable):

| Field | Meaning |
|---|---|
| `correlation_id` | UUID for the user-visible request |
| `audit_id` | UUID for the durable audit record |
| `agent_run_id` | UUID for the agent invocation |
| `tenant_id` | Customer handle (anonymized in logs) |
| `object_id` | The thing being acted on (lead, draft, invoice, etc.) |
| `action_mode` | `read_only` / `draft_only` / `approval_required` / `approved_execute` / `blocked` |
| `approval_status` | `none` / `pending` / `approved` / `rejected` / `blocked` |
| `risk_level` | `low` / `medium` / `high` / `blocked` |
| `proof_event_id` | If the action created a ProofEvent, its ID |
| `latency_ms` | total wall-clock |
| `cost` | optional — LLM tokens, $$, etc. |
| `error_type` | populated only on failure |

These map to the OpenTelemetry tracing model (`structlog`-friendly).

---

## 2. PII rules in logs

- ❌ NEVER log: emails, phones, Saudi IDs, names, raw lead bodies
- ✅ ALWAYS log: customer_handle (anonymized), object_id, action_mode
- The `redact_log_entry` helper at
  `auto_client_acquisition.security_privacy.log_redaction` is wired
  into the structlog pipeline; tests pin the redaction.

If you suspect PII in a log file:
1. Stop the affected service if active
2. Run `python scripts/dealix_smoke_test.py --json | jq '.'`
3. Search the log file with `grep -E '\\b[0-9]{10}\\b|@'` (basic sanity)
4. Report to founder with the offending event_id (NOT the raw payload)

---

## 3. Incident severity tiers

| Tier | Definition | Response time | Example |
|---|---|---|---|
| **P0** | Production down / live action fired without approval / PII leak | <15 min | `whatsapp_allow_live_send` accidentally True; PII in proof export |
| **P1** | Customer-visible degradation or mis-sent draft | <2 hours | Draft sent to wrong customer; founder dashboard 500 |
| **P2** | Layer broken but no customer impact yet | <24 hours | One v5 endpoint returns 500; daily digest fails |
| **P3** | Stale telemetry, cosmetic, low-priority | <7 days | typo in bilingual brief; status badge mis-aligned |

---

## 4. P0 runbook — Live action fired without approval

**Symptoms:**
- Customer-facing action observable externally that wasn't in `approved` state
- E.g. WhatsApp sent without ApprovalGate approval
- E.g. Moyasar charge processed without `--allow-live` flag

**Immediate response:**
1. **Stop the service:** `git revert HEAD; git push` (then redeploy)
2. **Find the breach:** `grep -r "send_whatsapp\|charge_payment_live" auto_client_acquisition/ scripts/`
3. **Confirm scope:** `python scripts/dealix_smoke_test.py --json | jq '.results[] | select(.ok==false)'`
4. **Notify customer:** if a real customer was affected, manual founder apology; offer Pilot refund
5. **Postmortem:** within 24h, write `docs/incidents/P0-YYYY-MM-DD.md`

**Verify the rollback:**
- `is_live_charge_allowed()['allowed'] == False`
- `whatsapp_allow_live_send == False`
- All `FORBIDDEN_TOOLS` rejected for every autonomy level

---

## 5. P0 runbook — PII leak

**Symptoms:**
- Email/phone/national ID visible in any committed file
- PII in `docs/proof-events/*.jsonl` raw text
- PII in any GitHub Issue / PR comment

**Immediate response:**
1. **Stop committing:** `git stash`
2. **Identify the leak:** `grep -rE '\\b[0-9]{10}\\b|@[a-z]+\\.' docs/proof-events/`
3. **If already pushed:** rewrite history (`git filter-branch` or BFG); force-push (founder approval required)
4. **Rotate any exposed credentials:** new API keys for Moyasar/Resend/etc.
5. **Notify the customer** within 72 hours per PDPL (founder direct)
6. **Postmortem:** write `docs/incidents/P0-YYYY-MM-DD-pii.md`

**Prevent next time:**
- Verify `tests/test_pii_redaction_perimeter.py` runs in CI
- Verify `tests/test_proof_ledger_redacts_on_export.py` runs
- Add a `gitleaks` rule for the leaked pattern shape

---

## 6. P1 runbook — Reliability OS reports a degraded subsystem

**Symptoms:**
- `python scripts/dealix_status.py` shows `overall: degraded`
- Or `/api/v1/reliability/health-matrix` returns a non-ok subsystem

**Triage table:**

| Subsystem | Likely cause | First step |
|---|---|---|
| `email_provider` | `RESEND_API_KEY` missing/expired | Check Railway env vars |
| `payment_provider` | `MOYASAR_SECRET_KEY` missing or sk_live_ | Verify it's `sk_test_*` |
| `safe_publishing_gate` | New forbidden phrase leaked into a doc | `pytest tests/test_landing_forbidden_claims.py` |
| `service_activation_matrix` | YAML invalid | `python scripts/verify_service_readiness_matrix.py` |
| `seo_perimeter` | New page missing required tags | `python scripts/seo_audit.py` |
| `proof_ledger_in_process` | `docs/proof-events/` not writable | Check FS permissions |
| `redis_client_available` | Redis down | (informational; not blocking) |

---

## 7. P2 runbook — Daily digest workflow failed

**Symptoms:**
- GitHub Action `daily_digest.yml` red
- No email at 7AM KSA

**Triage:**
1. View workflow run logs in Actions tab
2. If "RESEND_API_KEY not set" → set in repo Secrets
3. If "EmailClient.send raised" → check Resend dashboard for rate-limit/quota
4. If "daily_growth_loop.build_today raised" → run locally: `python scripts/dealix_morning_digest.py --print`
5. Re-run the workflow from Actions tab once root cause fixed

---

## 8. P3 runbook — Stale telemetry

**Symptoms:**
- `docs/snapshots/<date>.json` not regenerated for >24h
- `git_sha` field stuck

**Triage:**
- Check `daily_snapshot.yml` workflow status
- Check Railway env (`GIT_SHA` or `RAILWAY_GIT_COMMIT_SHA` populated)
- If lagging, manually trigger workflow

---

## 9. Alerting (today + future)

**Today:**
- Daily digest email = lightweight monitor; absence = signal
- Founder runs `dealix_status.py` each morning

**Future (post-customer-#5):**
- Sentry / Tempo for live error capture
- Slack alert for any `risk_level=high` ProofEvent
- PagerDuty for P0 (when team grows beyond founder)

---

## 10. Where to file an incident

- Create `docs/incidents/<TIER>-YYYY-MM-DD-<slug>.md`
- Include: detection method, customer impact, timeline, root cause, fix, prevention
- For P0 / P1: also open a GitHub Issue with the `incident` label
- Keep PII OUT of the issue/incident doc (use placeholders)

---

## 11. Compliance with NIST AI RMF

The runbook supports the four NIST AI RMF functions:

| Function | How Dealix supports it |
|---|---|
| **Govern** | This runbook + Decision Pack §V approval gates |
| **Map** | Trace contract (§1) covers context → action → outcome |
| **Measure** | Reliability OS + dealix_status + smoke tests |
| **Manage** | P0–P3 tiers + postmortem requirement |

NIST AI RMF reference: `https://www.nist.gov/itl/ai-risk-management-framework`

---

— Observability & Incident Runbook v1.0 · 2026-05-05 · Dealix
