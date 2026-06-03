# Agent Tool-Use Boundaries

> What agents may touch, and the hard limits around tools.
> AI drafts. Human approves. System logs.

---

## 1. Principle

Agents are **Observe / Advise / Draft** only. Any outward or irreversible
action requires a human. Tool selection itself can be a target of attack
(tool-selection manipulation), so tools are constrained by allow-list, not by
model judgement over untrusted text.

---

## 2. Allowed vs. forbidden

| Capability | Allowed? | Note |
|------------|----------|------|
| Read public/internal data | ✅ | Observe |
| Score & rank prospects/drafts | ✅ | Advise |
| Write drafts & reports to repo | ✅ | Draft (version-controlled) |
| Send email / WhatsApp / SMS | ❌ NOT ALLOWED | Human only |
| Place phone calls | ❌ NOT ALLOWED | No automated calling |
| Make pricing decisions | ❌ NOT ALLOWED | Founder only |
| Delete data / modify secrets | ❌ NOT ALLOWED | Red line |
| Execute shell from external text | ❌ NOT ALLOWED | Injection vector |
| Ingest purchased lists | ❌ NOT ALLOWED | Compliance |

---

## 3. Tool-call guardrails

```txt
Tool arguments come from trusted, extracted fields — never raw external text.
No tool runs because a web page / email "asked" for it.
No secret is read into a prompt or a tool argument.
Every consequential action is logged in ai_action_ledger.jsonl.
```

---

## 4. Mapping to existing roles

These boundaries match the per-agent matrix in
`company_os/governance/agent_permissions.md` (prospect_research, war_room,
delivery, finance, governance). This file is the security-side restatement of
those limits for tool use specifically.

---

## 5. Enforcement

The daily control check (`npm run commercial:check`) asserts the governance red
lines are intact and writes `reports/security/DAILY_AGENT_SECURITY_REVIEW.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Enforced: YES*
