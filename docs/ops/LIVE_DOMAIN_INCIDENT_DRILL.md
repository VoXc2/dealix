# Dealix Live Domain Incident Drill

Use this drill when `dealix.me`, `api.dealix.me`, checkout, demo requests, or public smoke checks fail.

## Incident severity

| Severity | Examples | First action |
|---|---|---|
| SEV-1 | API down, checkout down, admin auth bypass, public site unavailable during launch | Freeze deploys, assign incident lead, start rollback evaluation. |
| SEV-2 | One critical public flow broken, partial API outage, webhook failures | Disable affected automation if possible, patch or rollback. |
| SEV-3 | Non-critical endpoint failure, copy issue, analytics issue | Create backlog item and fix in normal release flow. |

## First 5 minutes

1. Identify failing surface: public website, API, database, DNS, TLS, payment, webhook, or frontend.
2. Check GitHub Actions `Production Smoke` report.
3. Check hosting provider deployment status and recent deploy SHA.
4. Check `/health` on the API domain.
5. Decide whether to rollback, patch forward, or isolate a feature.

## Domain failure path

If public website fails:

- Check DNS target.
- Check hosting frontend deployment.
- Check TLS certificate state.
- Check redirect from `www` to canonical host if configured.
- Roll back frontend deployment if the host is healthy but app is broken.

If API domain fails:

- Check API service deployment.
- Check `/health` and logs.
- Check database connectivity.
- Check CORS and API gateway/reverse proxy settings.
- Roll back API deployment if a recent change caused the failure.

## Payment or checkout failure path

- Confirm checkout endpoint is reachable.
- Confirm Moyasar production key is configured only on the server.
- Confirm webhook secret matches the provider dashboard.
- Confirm callback URL uses the live domain.
- Pause paid acquisition until flow is verified.

## Trust or approval failure path

If a high-stakes action bypasses approval:

1. Disable the affected route, job, or automation.
2. Preserve logs and audit records.
3. Rotate exposed keys if any external action was sent incorrectly.
4. Add an incident item to `docs/ops/EXECUTION_BACKLOG.md`.
5. Add a regression test before re-enabling.

## Rollback checklist

- [ ] Rollback target SHA or image digest identified.
- [ ] Database migration compatibility checked.
- [ ] Feature flags or automation toggles checked.
- [ ] Rollback executed.
- [ ] `python scripts/dealix_smoke_test.py --base-url https://api.dealix.me` passes.
- [ ] Public website loads.
- [ ] Incident notes recorded.

## Post-incident review

Within 24 hours:

- What failed?
- Why did detection happen when it happened?
- What prevented faster rollback?
- What test or monitor would have caught it earlier?
- What exact PR closes the prevention gap?

## Arabic summary

عند فشل الدومين أو الإنتاج: حدد السطح المتعطل، افحص smoke report، راجع آخر deploy، قرر rollback أو patch، وثّق السبب، وأضف اختبار يمنع تكرار المشكلة.
