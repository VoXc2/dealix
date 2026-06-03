# MCP / Tool Risk Review — Findings (2026-06-03)

## In-session MCP servers
- **GitHub MCP** — scoped to `voxc2/dealix`. Read tools low-risk; write tools
  (PR/push/comment) gated behind explicit intent; PRs open as draft.
- **Notion MCP** — present but **not used** in this hardening pass; no Dealix
  data pushed to Notion.

## Findings
| Item | Status |
|------|--------|
| Tool allowlist / least-tool | ✅ policy in `docs/security/MCP_TOOL_RISK_POLICY.md` |
| Tool descriptions treated as untrusted | ✅ |
| No secrets passed as tool args | ✅ |
| Repo scope respected (`voxc2/dealix`) | ✅ |
| Destructive tools (merge/delete) require explicit instruction | ✅ |
| Secret scanning available (`run_secret_scanning`) | ✅ recommend running in CI |

## Residual
- 🟡 No in-repo MCP server today. If one is added, it must ship a tool allowlist,
  no-secrets policy, and its tool descriptions must be reviewed (T4).

**Verdict:** Tool usage is least-privilege and scoped. Low residual risk.
