# Pull Request

## Summary | الملخص
<!-- What does this PR change and why? -->

## Type of change | نوع التغيير
- [ ] 🐛 Bug fix
- [ ] ✨ New feature
- [ ] 💥 Breaking change
- [ ] 📝 Docs only
- [ ] ♻️ Refactor
- [ ] 🔒 Security

## Engineering cutover (only if env/backend persistence changes)

If this PR touches `PROOF_LEDGER_BACKEND`, `VALUE_LEDGER_BACKEND`, `DEALIX_OPERATIONAL_STREAM_BACKEND`, or `OTEL_CONTRACT_TRACE_EXPORT`:

```text
external_signal: <contract_signed|pilot_scope_locked|...>
contract_or_pilot_ref: <internal id or account name>
```

See [docs/transformation/CUTOVER_PR_CHECKLIST_AR.md](docs/transformation/CUTOVER_PR_CHECKLIST_AR.md) and [docs/transformation/ENGINEERING_CUTOVER_RUNBOOK_AR.md](docs/transformation/ENGINEERING_CUTOVER_RUNBOOK_AR.md).

## Checklist | قائمة التحقق
- [ ] Tests added / updated
- [ ] Docs updated (if needed)
- [ ] No secrets committed (verified via `gitleaks`)
- [ ] `make lint` passes
- [ ] `make test` passes
- [ ] Linked to an issue (if applicable)
- [ ] Cutover PR body validated (`python3 scripts/verify_cutover_pr_body.py`) if applicable

## How to test | كيف أختبر هذا
<!-- Steps to verify -->

## Screenshots / Logs (optional)
