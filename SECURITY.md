# Security Policy | سياسة الأمن

## Supported versions

| Version | Supported |
|---|---|
| 3.x | Yes |
| 2.x | Security fixes only |
| 1.x | End of life |

## Reporting a vulnerability

Do **not** open a public issue for security vulnerabilities.

Use GitHub Security Advisories:

- Repository security advisory: `https://github.com/VoXc2/dealix/security/advisories/new`

Include:

1. Vulnerability description.
2. Steps to reproduce.
3. Expected impact.
4. Affected files, endpoints, or deployment surface.
5. Suggested fix if known.

## Current security automation

| Control | Location |
|---|---|
| CodeQL static analysis | `.github/workflows/security.yml` |
| Dependency review for PRs | `.github/workflows/security.yml` |
| Dependabot updates | `.github/dependabot.yml` |
| Environment contract check | `scripts/check_env_contract.py` |
| Repository security smoke check | `scripts/security_smoke.py` |
| Python security lint | `make security` / Bandit |
| Secret baseline scan when configured | `make security` / detect-secrets |
| Production verification bundle | `make prod-verify` |

## Secret handling rules

- Never commit `.env`, production credentials, customer exports, or private keys.
- `.env.example` is the only committed env-like file expected at the repository root.
- Browser-exposed `NEXT_PUBLIC_*` variables must not contain admin or privileged credentials.
- Privileged frontend operations should be proxied through a server-side route when possible.
- Rotate keys immediately if accidental exposure is suspected.

## Key rotation guidance

If a key may have been exposed:

1. Revoke or rotate the provider key.
2. Update the deployment platform secret.
3. Redeploy the affected service.
4. Run repository and platform secret scanning.
5. Review logs for suspicious use.
6. Record the incident and follow-up tasks in the execution backlog.

## Maintainer checklist

Before merging security-relevant or production-facing changes:

- [ ] `make env-check`
- [ ] `make security-smoke`
- [ ] `make security` when dependencies are installed
- [ ] `make openapi-export` for API changes
- [ ] No production data, customer personal data, or live secrets are included
- [ ] Public claims are updated in the no-overclaim register when needed

## Arabic summary

لا تفتح issue عام للثغرات. استخدم GitHub Security Advisories. لا ترفع أسرار أو بيانات عملاء. أي تغيير إنتاجي لازم يمر على فحص البيئة، فحص الأمن السريع، ومراجعة الادعاءات العامة قبل الدمج.
