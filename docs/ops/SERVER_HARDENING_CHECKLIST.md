# Dealix Server Hardening Checklist

Use this checklist for the server or hosting platform that serves `dealix.me` and `api.dealix.me`.

## Network and access

- [ ] SSH access is disabled if the platform does not require it.
- [ ] If SSH is used, password login is disabled.
- [ ] Only required ports are open: 80/443 and platform-required management ports.
- [ ] Admin dashboards are protected by SSO/MFA.
- [ ] Deployment tokens are scoped and rotated.

## Runtime

- [ ] API runs with `ENVIRONMENT=production`.
- [ ] App secrets are injected from the platform secret manager.
- [ ] No `.env` file with production secrets exists in the repository or image.
- [ ] Database migrations are run intentionally, not by app startup in production.
- [ ] Health checks are enabled at the platform load balancer.
- [ ] Restart policy is configured.

## TLS and domain

- [ ] TLS is managed by the platform or trusted certificate manager.
- [ ] Certificates auto-renew.
- [ ] HTTP redirects to HTTPS.
- [ ] HSTS is enabled only after every required subdomain supports HTTPS.
- [ ] DNS records are documented.

## Logging and observability

- [ ] Structured logs are enabled.
- [ ] Request IDs are visible in logs.
- [ ] Error capture is configured if used.
- [ ] Logs do not include full API keys, admin keys, payment secrets, or customer personal data.
- [ ] Retention period matches the compliance posture.

## Backups and recovery

- [ ] Production database backups are enabled.
- [ ] Restore procedure has been tested.
- [ ] Backup retention is documented.
- [ ] Rollback path for API and frontend deployments is known.

## Verification commands

```bash
make env-check
make api-contract-check
make security-smoke
make production-smoke PRODUCTION_BASE_URL=https://api.dealix.me
```

## Arabic summary

السيرفر أو منصة الاستضافة لازم تكون محمية: أسرار خارج الكود، HTTPS، مراقبة، backups، rollback واضح، وعدم تسريب مفاتيح أو بيانات عملاء في اللوجات.
