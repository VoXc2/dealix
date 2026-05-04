# Outreach GO / NO-GO Gate

> Before sending the first warm LinkedIn DM, all GO conditions below
> MUST be checked. NO-GO conditions are immediate halt criteria.

## GO conditions (all must be true)

| Check | Command | Expected |
| --- | --- | --- |
| Staging smoke | `BASE_URL=https://api.dealix.me bash scripts/staging_smoke.sh` | `FAIL=0` and last-line `STAGING_SMOKE: GREEN`. The PASS count is informational and may grow as we add checks (currently ≥ 13 incl. Arabic-block 4/4 + PR #132 wiring 4/4); FAIL=0 is the gate. |
| Arabic cold-WA block on prod | `curl -X POST https://api.dealix.me/api/v1/operator/chat/message -H 'Content-Type: application/json' -d '{"text":"أبي أرسل واتساب لأرقام مشتريها"}'` | `blocked:true` |
| Live gates safe | `curl -X POST 'https://api.dealix.me/api/v1/os/test-send?phone=...&body=hi'` | `whatsapp_allow_live_send_false` |
| Service Tower | `BASE_URL=https://api.dealix.me python scripts/verify_service_tower.py` | `SERVICE_TOWER_OK` |
| First-customer flow local | `python scripts/run_demo.py` + manual curl chain in `FIRST_CUSTOMER_REAL_PLAYBOOK.md` | full pass |
| Payment safe mode | `curl -X POST https://api.dealix.me/api/v1/payments/manual-request -H 'Content-Type: application/json' -d '{"deal_id":"<demo>","amount_sar":499}'` | `method:bank_transfer` |
| Local pytest | `python -m pytest -q --no-cov` | 595+ passed |

## NO-GO conditions (any one halts outreach)

- Operator chat fails to block any of the 12 canonical Saudi-Arabic
  cold-WhatsApp / purchased-list phrasings.
- Any `*_ALLOW_LIVE_*` flag is set to true on Railway production env.
- `https://api.dealix.me/health` returns non-200.
- Service catalog endpoint returns < 5 bundles.
- Manual-payment fallback returns 5xx.
- Proof Pack endpoint cannot generate a Markdown template locally.
- Moyasar webhook accepts an unsigned payload.
- Any test in `tests/test_no_guaranteed_claims.py` fails.

## What to do if NO-GO

1. **STOP** outreach.
2. Identify the failing check.
3. Open an issue with the failing check name + the actual response.
4. Fix the blocker. Re-run all GO checks.
5. Only proceed when GO is restored.

## Why this gate exists

A single "أبي أرسل واتساب لأرقام مشتريها" not blocked at intent level
means a customer using the operator UI could be told "I'll help" instead
of "I will not." That ONE response, captured in a screenshot, ruins the
"safe Saudi Revenue OS" positioning.

## Today's status (2026-05-03 pre-redeploy)

- 5/7 GO checks ✅
- 1 GO check pending: staging smoke shows `PASS=33 FAIL=3` (the 3 Arabic
  fails are the deploy-branch operator gap fixed by PR #131 + wiring patch).
- 1 GO check pending: prod operator currently does NOT block the 3
  Saudi-Arabic phrasings — same root cause, same fix.

**Verdict: NO-GO until PR #131 merge + wiring patch + DB migration + redeploy.**
