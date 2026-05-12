# Summary

> One-paragraph WHY. The diff is the WHAT.

## Touched areas

- [ ] api/
- [ ] core/
- [ ] dealix/
- [ ] frontend/
- [ ] infra/
- [ ] docs/
- [ ] tests/

## Checklist (AGENTS.md conventions)

- [ ] Test added (unit / integration / Promptfoo eval) for new behavior.
- [ ] `make mypy-strict` clean on touched modules.
- [ ] `make semgrep` green (or justified `# noqa` with reason).
- [ ] No new `except Exception` without an explicit reason comment.
- [ ] New env vars documented in `.env.example`.
- [ ] Endpoint changes paired with a `docs/api/*.mdx` update.
- [ ] AuditLogRecord written for any new mutation.
- [ ] Architectural change has an ADR under `docs/adr/`.
- [ ] CHANGELOG entry if customer-visible.

## Linked issues / decisions

Closes #
Implements ADR #
Mitigates SOC 2 control:
