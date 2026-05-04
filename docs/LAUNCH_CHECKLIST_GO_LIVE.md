# Dealix — Launch-Online Checklist (one page)

> Run these three steps in order. Total time: ~10 minutes of waiting.
> Each step ends with a single curl/script that confirms green.

## Step 1 — Sync the website (`landing/` → `gh-pages`)

The website at `dealix.me` is served from the `gh-pages` branch.
Until now, it was a manually-curated stale subset. The new workflow
`.github/workflows/landing_deploy.yml` mirrors the entire `landing/`
directory on every push.

Trigger:

- **Automatic** — pushing this commit to
  `claude/launch-command-center-6P4N0` already triggered the workflow
  (filter: `paths: ['landing/**', 'CNAME', '.github/workflows/landing_deploy.yml']`).
- **Manual** — GitHub → Actions → "Deploy landing → gh-pages" →
  Run workflow → branch `claude/launch-command-center-6P4N0`.

Verify:

```bash
for p in / /index.html /services.html /operator.html /pricing.html \
         /trust-center.html /proof-pack.html /private-beta.html \
         /onboarding.html /agency-partner.html /command-center.html; do
  echo "$(curl -s -o /dev/null -w "%{http_code}" --max-time 10 "https://dealix.me$p")  $p"
done
```

Expected: every line shows `200`. The workflow itself runs this check
at the end and fails CI if any non-200 is found.

## Step 2 — Railway "Deploy Latest Commit"

The API at `api.dealix.me` needs the new code (the demo-request
LeadRecord write + the `/founder/today` `inbound_demo_requests` field).

Trigger:

- Railway → service "dealix" → Deployments → **"Deploy Latest Commit"**
  (NOT "Redeploy" on a previous row — that reuses the cached build).

Verify:

```bash
bash scripts/post_redeploy_verify.sh
```

Expected:

```
running git_sha = <new SHA — should start with the SHA of this commit>
STAGING_SMOKE: GREEN
PASS=13  FAIL=0
unsafe Arabic cold-WA blocked 4/4
operator response carries PR #132 wiring ... 4/4
unsafe English cold-WA blocked
OUTREACH_GO=yes
DEALIX_FINAL_VERDICT=FIRST_CUSTOMER_READY_REALISTIC
```

## Step 3 — Inbound flow check

Confirm a real visitor's form-submission turns into a tracked lead
and shows up in the founder's `/founder/today` aggregator.

Run:

```bash
bash scripts/verify_inbound_flow.sh
```

Expected:

```
[1/2] POST /api/v1/public/demo-request
  ✓ demo-request returned ok=true
  ✓ lead_id surfaced in response: lead_<hex>
[2/2] GET /api/v1/founder/today (polling for inbound counter)
  ✓ test company appears in /founder/today inbound list (count=N)
INBOUND_FLOW: GREEN
```

The test uses the `demo+test+<timestamp>@dealix-test.sa` email
namespace, so the founder can identify and remove the test row from
the DB if desired.

## Final verdict

| Step | Pass criterion | Status |
| --- | --- | --- |
| Step 1 | `dealix.me/services.html` and 9 other canonical pages return 200 | ☐ |
| Step 2 | `STAGING_SMOKE: GREEN` and `OUTREACH_GO=yes` | ☐ |
| Step 3 | `INBOUND_FLOW: GREEN` and the test lead is visible in `/founder/today` | ☐ |

When all three are checked: **DEALIX_LAUNCH_STATE=ONLINE_AND_INBOUND_WIRED**.

The founder is now cleared to:

1. Send the first 10 manual warm LinkedIn DMs per
   `docs/FIRST_10_WARM_LINKEDIN_EXECUTION.md`.
2. Watch `/api/v1/founder/today` daily for inbound demo requests
   (the new `inbound_demo_requests.recent` array shows the last 5
   non-PII rows).
3. Reply manually to every reply within 24 hours and run the
   Mini Diagnostic per `docs/MINI_DIAGNOSTIC_LIVE_TEMPLATE.md`.

## What did NOT change

- All eight live-action gates remain `false` on prod
  (`WHATSAPP_ALLOW_LIVE_SEND`, `MOYASAR_ALLOW_LIVE_CHARGE`,
   `GMAIL_ALLOW_LIVE_SEND`, `LINKEDIN_ALLOW_AUTOMATION`,
   `RESEND_ALLOW_LIVE_SEND`, `CALLS_ALLOW_LIVE_DIAL`,
   `WHATSAPP_ALLOW_INTERNAL_SEND`, `WHATSAPP_ALLOW_CUSTOMER_SEND`).
- No new product features.
- No live external send.
- No card capture.
- No fake customer data (the verifier's test row is namespaced).

## If anything is red

| Symptom | Most likely cause | Fix |
| --- | --- | --- |
| `dealix.me/services.html` is still 404 | gh-pages workflow not triggered | GitHub → Actions → Run workflow on `claude/launch-command-center-6P4N0` |
| `running git_sha = unknown` | Railway built before Dockerfile got the GIT_SHA arg | Click "Deploy Latest Commit" again, NOT "Redeploy" |
| `INBOUND_FLOW: RED` with "lead_id missing" | DB write failed silently — Postgres connection issue | Check Railway logs for `inbound_lead_write_skipped` |
| `INBOUND_FLOW: RED` with "test company NOT seen" | API picked up the lead but `/founder/today` schema not deployed | Confirm Railway deployed the latest commit; redeploy if not |
| `STAGING_SMOKE: RED` with Arabic cold-WA failing | PR #132 wiring missing — Railway is on an older image | "Deploy Latest Commit" again |
