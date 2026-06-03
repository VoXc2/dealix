# Secrets Handling Policy

Secrets are API keys, access tokens, passwords, payment credentials, and signing
keys. They have exactly one safe home: a secrets manager / environment variables on
the server. They never appear anywhere an agent can read or echo them.

---

## Never (red lines)

| # | Rule |
|---|------|
| 1 | No secrets in prompts sent to any model |
| 2 | No secrets in logs, reports, or the `ai_action_ledger` |
| 3 | No secrets in `data/` JSON / JSONL / CSV |
| 4 | No secrets in GitHub issues, PRs, or comments |
| 5 | No `.env` files committed (see `.gitignore`) |
| 6 | No API keys requested over WhatsApp / chat — use the secure portal |
| 7 | No production secrets exposed to PR / `issue_comment` workflows |

---

## Where secrets live

| Layer | Mechanism |
|-------|-----------|
| Local dev | `.env` (git-ignored), copied from `.env.example` |
| CI | GitHub Actions secrets — only for trusted, `push`-triggered jobs |
| Production | Host secret store / environment variables |

`.env.example` documents *names only*, never values.

---

## Client-supplied secrets

A client never pastes a key into chat. The flow is:

```
Client needs to connect a tool
   → secure portal link (expiring)
   → least-privilege, read-only where possible
   → access recorded + auditable
   → revoke when the task is done
```

L4/L5 access requires founder approval.

---

## Detection

- `scripts/safety_gate.py` flags secret-request patterns (`api key`, `مفتاح api`,
  `كلمة المرور`, tokens) in outbound copy → `OUT-SECRET-REQUEST`.
- `tests/test_safety_gate.py` asserts those patterns are caught.
- Recommended: enable GitHub secret scanning / push protection on the repo.

---

## If a secret is exposed

1. Treat as a CRITICAL incident.
2. Rotate the secret immediately.
3. Purge it from the offending location.
4. Review how it got there; add a guard so it can't recur.

---

*Version 1.0 | 2026-06-03 | Related: G002, G007, R003*
