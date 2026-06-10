# Dealix Release Process

Use this process for production releases, public pilots, and major customer-facing changes.

## 1. Prepare

- Confirm `main` is green.
- Review `docs/ops/EXECUTION_BACKLOG.md` for linked P0/P1 work.
- Review `docs/architecture/REPO_GAP_AUDIT.md` for newly affected gaps.
- Update `CHANGELOG.md`.
- Confirm `.env.example` matches production expectations.

## 2. Verify

Run:

```bash
make env-check
make openapi-export
make security-smoke
make test
make prod-verify
```

For deployed environments, also run smoke tests with the production or staging `BASE_URL`.

## 3. Review risk

- Public claims updated? Check `dealix/registers/no_overclaim.yaml`.
- API behavior changed? Review OpenAPI output.
- Env changed? Update deployment platform variables and docs.
- Customer data touched? Confirm suppression, retention, and audit behavior.
- Frontend changed? Confirm `apps/web` build and critical browser flows.

## 4. Release

- Create or update the release tag.
- Record deployed commit SHA and Docker image digest where applicable.
- Record rollback target.
- Keep release notes concise and customer-readable.

## 5. Post-release

- Check `/health` and critical public endpoints.
- Review error telemetry and logs.
- Confirm demo request, pricing, checkout, and webhook flows.
- Record incidents or follow-up tasks in the execution backlog.

## Arabic summary

كل إطلاق لازم يكون قابل للتكرار: جهّز، تحقق، راجع المخاطر، أطلق، ثم راقب. لا تعتمد على الذاكرة أو خطوات غير مكتوبة.
