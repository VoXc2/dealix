# Dealix Commercial Go-Live Gate

Use this gate before paid traffic, public launch, enterprise pilots, or founder-led demos.

## 1. Public website

- [ ] `https://dealix.me` loads successfully.
- [ ] `/status` loads successfully.
- [ ] `/robots.txt` and `/sitemap.xml` are reachable.
- [ ] Homepage copy matches current offer and no-overclaim policy.
- [ ] CTA paths route to the intended demo, checkout, or contact flow.

## 2. API and smoke

- [ ] `https://api.dealix.me/health` returns healthy.
- [ ] `make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me` passes.
- [ ] Production Smoke workflow has a recent successful run.
- [ ] Admin routes reject missing or invalid credentials.
- [ ] Webhook routes verify signatures where applicable.

## 3. Demo request flow

- [ ] Demo request endpoint responds successfully.
- [ ] Lead notification reaches the intended inbox, CRM, or calendar flow.
- [ ] Arabic and English request fields are handled.
- [ ] No personal data is logged unnecessarily.
- [ ] Follow-up owner and SLA are known.

## 4. Checkout and payment

- [ ] Pricing copy matches the approved offer.
- [ ] Checkout amount and currency match approved packaging.
- [ ] Payment provider is using production mode intentionally.
- [ ] Callback URL uses the live domain.
- [ ] Webhook secret matches provider dashboard.
- [ ] Failed payment behavior is customer-safe.

## 5. Trust and compliance

- [ ] `dealix/registers/no_overclaim.yaml` is current.
- [ ] PDPL posture is reflected in public copy and operational flow.
- [ ] High-stakes outbound actions require approval.
- [ ] Evidence packs and audit logs are available for customer-facing claims.
- [ ] Data suppression/opt-out path is known before outreach.

## 6. Observability

- [ ] Errors are visible to the operator.
- [ ] Request IDs are present in logs.
- [ ] Demo and checkout failures are observable.
- [ ] Cost/provider failures are observable for AI-dependent flows.
- [ ] Incident and rollback path is documented.

## Go-live decision

Go live only when all P0 items are complete or explicitly risk-accepted by the owner.

## Arabic summary

لا تبدأ حملات أو ديمو رسمي إلا بعد التأكد من الموقع، API، الديمو، الدفع، الامتثال، والمراقبة. الهدف أن يكون الإطلاق قابل للقياس والرجوع، وليس مجرد نشر ناجح.
