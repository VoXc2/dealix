# Dealix Launch Operator Runbook

This is the final operator page for moving Dealix from repository-ready to live-production-ready.

## Current repository state

The repository is prepared with:

- CI for Python and web verification.
- Security workflow with CodeQL and dependency review.
- Repository hardening workflow.
- OpenSSF Scorecard workflow.
- Production Smoke workflow.
- Generate Web Lockfile workflow.
- Backend and frontend environment contract checks.
- API contract check.
- Dependency inventory exporter.
- Release manifest exporter.
- Frontend security headers, SEO metadata, sitemap, robots, manifest, and status page.
- Production, commercial, domain, monitoring, incident, frontend, server hardening, and supply-chain runbooks.

## Required access

The operator needs access to:

1. GitHub Actions.
2. GitHub repository settings.
3. Railway or the active hosting platform.
4. DNS provider for the public and API domains.
5. Payment and webhook provider dashboards when those flows are enabled.

## Launch order

### 1. Generate and commit the web lockfile

Run:

- Actions → Generate Web Lockfile → Run workflow.

Download the artifact and commit it as:

```text
apps/web/package-lock.json
```

Then rerun CI.

### 2. Configure runtime settings

Use:

- `docs/ops/PRODUCTION_SECRETS_CHECKLIST.md`
- `.env.example`
- `apps/web/.env.example`

Confirm public site URL, API URL, database URL, app secret, admin credentials, and provider credentials are configured in the correct private settings UI.

### 3. Run required workflows

Run or review:

- CI
- Security
- Repository Hardening
- OpenSSF Scorecard
- Production Smoke

### 4. Verify hosting

Confirm Railway or the active host reports success for production services.

Observed Railway status contexts to watch:

- `Dealix - cv`
- `pleasant-determination - web`
- `adorable-learning - web`

### 5. Verify live domains

Confirm:

- Public website loads.
- API health endpoint responds.
- TLS certificates are valid.
- HTTP redirects to HTTPS where applicable.
- Old DNS records are removed or documented.

### 6. Verify commercial flows

Use `docs/ops/COMMERCIAL_GO_LIVE_GATE.md`.

Check:

- Demo request flow.
- Checkout/payment flow when enabled.
- Webhook verification.
- Customer notification routing.
- No-overclaim register for public copy.

### 7. Final release handoff

Run locally or on the server:

```bash
make env-check
make api-contract-check
make security-smoke
make dependency-inventory
make release-manifest
make prod-verify
```

Archive generated files under `docs/generated/` if they are used as release evidence.

## Stop rules

Do not launch paid traffic or enterprise pilots if any of these are true:

- CI is failing without accepted risk notes.
- Production smoke fails.
- DNS or TLS is uncertain.
- Demo request routing is not confirmed.
- Checkout or webhook verification is not confirmed.
- Admin credentials are exposed in browser/public variables.
- Public claims do not match implemented controls.
- Rollback path is unknown.

## Arabic summary

هذه صفحة التشغيل النهائية للإطلاق. الريبو جاهز، لكن التدشين الكامل يحتاج تشغيل Actions، ضبط الإعدادات الخاصة، التحقق من Railway/DNS/TLS، ثم اختبار الديمو والدفع والويبهوكس. لا تبدأ حملات أو ديمو رسمي إذا فشل أي بند من stop rules.
