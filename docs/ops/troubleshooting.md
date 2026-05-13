# Troubleshooting — top 10 issues that will bite you in the first 30 days

> Grep this page on the first thing that breaks. Each row gives you
> a one-paragraph diagnosis + the exact fix command.

## 1. `/api/v1/skills` returns `count=0`

**Symptom.** Skills catalogue is empty even though
`/api/v1/skills/handlers` shows all 12.

**Diagnosis.** You deployed before commit `d45d347`. The pre-fix
loader resolved `_MANIFEST` to `<repo>/dealix/skills/MANIFEST.yaml`
(which doesn't exist) instead of `<repo>/skills/MANIFEST.yaml`.

**Fix.**
```bash
cd /opt/dealix && git pull origin claude/comprehensive-qa-review-ZLsYG
grep "_MANIFEST = " dealix/agents/skills/__init__.py
# must read "parents[3]" not "parents[2]"
docker compose -f deploy/docker-compose.prod.yml restart api
```

## 2. Moyasar webhook → 401 `bad_signature`

**Diagnosis.** `MOYASAR_WEBHOOK_SECRET` doesn't match the value in
the Moyasar dashboard. Or the webhook was registered for the *test*
environment but you swapped to live keys without re-registering.

**Fix.**
```bash
docker compose -f deploy/docker-compose.prod.yml logs api | grep moyasar_webhook_bad_signature
# Open dashboard.moyasar.com → webhooks → Re-copy "Secret token".
$EDITOR /opt/dealix/.env   # paste under MOYASAR_WEBHOOK_SECRET=
docker compose -f deploy/docker-compose.prod.yml restart api
```

## 3. Customer paid but no receipt email

**Diagnosis.** Either `RESEND_API_KEY` is unset OR the customer's
email never made it into the Moyasar payment metadata, so
`_send_receipt_email_best_effort` skips silently.

**Fix.**
```bash
docker compose logs api | grep -E 'receipt_email_(sent|skipped|failed)'
# If "skipped_no_buyer_email": your /checkout flow must pass
#   metadata.email   when creating the Moyasar invoice.
# If "failed":       Resend rejected — verify RESEND_API_KEY +
#                    your Resend "From" address is verified.
# If nothing logged: the webhook fingerprint says duplicate —
#   replay via the DLQ ops dashboard.
```

## 4. Invoice URL returns 401 `invoice_token_required`

**Diagnosis.** The link in the receipt email is auto-signed with the
`INVOICE_DOWNLOAD_SECRET` (falls back to `JWT_SECRET_KEY`). If the
secret rotated between sending the email and the customer clicking,
the signature becomes invalid.

**Fix.** Don't rotate `JWT_SECRET_KEY` after invoices have been emailed.
If you must rotate, set `INVOICE_DOWNLOAD_SECRET` to the OLD value
explicitly so existing links still verify.

## 5. Trial-expired upgrade button does nothing

**Diagnosis.** The Next.js frontend has no `NEXT_PUBLIC_API_BASE`,
so `fetch(${API_BASE}/api/v1/...)` hits the wrong host.

**Fix.**
```bash
cd /opt/dealix/frontend
NEXT_PUBLIC_API_BASE=https://api.dealix.me npm run build
docker compose -f /opt/dealix/deploy/docker-compose.prod.yml restart web
```

## 6. PostHog flags evaluate to default

**Diagnosis.** `POSTHOG_API_KEY` is set but to the *Personal* API key
(starts with `phx_`) instead of the *Project* API key (starts with
`phc_`). Or you pasted the project key from a different project.

**Fix.** Open `app.posthog.com` → settings → "Project API Key"
(the one that starts with `phc_`). Re-paste into `.env`, restart API.

## 7. Cerbos PDP unreachable

**Diagnosis.** Cerbos sidecar pod crashed or the network policy
blocks port 3593.

**Fix.** The codebase wraps Cerbos in `api/security/rbac.py` with a
static RBAC fallback, so the API keeps working with reduced policy
granularity. To restore Cerbos:
```bash
docker compose ps cerbos
docker compose logs cerbos --tail=40
docker compose restart cerbos
```

## 8. `/api/v1/health/deep` missing the `vendors` block

**Diagnosis.** Either the deep-health route fell through to the
lightweight one (rare — only on import error), or
`prometheus-fastapi-instrumentator` is missing and the deep route
short-circuited.

**Fix.**
```bash
docker compose exec api pip show prometheus-fastapi-instrumentator
# If missing:
docker compose exec api pip install 'prometheus-fastapi-instrumentator>=7.0'
docker compose restart api
```

## 9. WhatsApp webhook → 403 verify

**Diagnosis.** Meta's webhook verification handshake hasn't
completed — Meta sends a GET with `hub.verify_token` and we must
echo `hub.challenge`. If `WHATSAPP_VERIFY_TOKEN` mismatches between
Meta dashboard + your env, Meta gives up.

**Fix.** Re-do the verify dance:
1. Pick a fresh token: `python -c "import secrets; print(secrets.token_urlsafe(32))"`.
2. Paste it in both Meta's webhook subscription dashboard AND your
   `WHATSAPP_VERIFY_TOKEN` env. Restart API.
3. Click "Verify and save" in Meta.

## 10. ZATCA QR-code doesn't validate

**Diagnosis.** Seller VAT must be a 15-digit number starting with `3`
(per ZATCA Phase 2 rules), and the timestamp must be ISO 8601 with
explicit timezone (`+03:00` for KSA).

**Fix.**
```bash
$EDITOR /opt/dealix/.env
# DEALIX_VAT_NUMBER=310000000000003   (your real VAT, 15 digits, starts with 3)
docker compose restart api
# Validate with the helper:
docker compose exec api python -c "
from integrations.zatca import build_zatca_tlv
print(build_zatca_tlv(
    seller_name='Dealix For AI Co.',
    seller_vat='310000000000003',
    timestamp='2026-01-01T00:00:00+03:00',
    total=1.0, vat=0.15
))"
```

## When everything else fails

1. `docker compose -f deploy/docker-compose.prod.yml logs api --tail=200`.
2. Grep for `ERROR` and `exception`.
3. Open a Sentry issue (if `SENTRY_DSN` set) — every uncaught
   exception lands there.
4. Run the smoke script: `bash scripts/ops/post_deploy_smoke.sh
   --base-url https://api.<domain>`. The failing check is your
   smallest reproducer.
5. Rollback: `helm rollback dealix <prev>` (K8s) or
   `docker compose pull && docker compose up -d --force-recreate`
   to roll forward to the last-known-good tag.

## Escalation

- Internal incident response: `docs/ops/incident_response.md`.
- Founder on-call rotation: `docs/ops/OPS_ROTATION.md`.
- Security disclosure: `https://dealix.me/.well-known/security.txt`.
