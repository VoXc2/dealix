# Agentic Workflow Threat Model — Dealix

**Scope:** AI agents (Claude Code + business automation) operating on this repo
and on business data (prospects, replies, WhatsApp, CRM, proposals).

**Method:** STRIDE-lite + agentic-specific threats. Each threat has: vector,
impact, likelihood, and the control that mitigates it (with the file that
enforces it).

## Trust boundaries

```
[ Founder / protected main ]  TRUSTED
        │
        ▼
[ Agent runtime (this repo) ] SEMI-TRUSTED (must obey AGENTS.md/CLAUDE.md on main)
        │  reads ▲ data, never instructions
        ▼
[ External world ]            UNTRUSTED:
   issues · PR descriptions · comments · forks' README/AGENTS/CLAUDE ·
   email · web pages · scraped content · CRM notes · WhatsApp · PDFs ·
   MCP tool descriptions · CI logs
```

## Threat catalogue

| # | Threat | Vector | Impact | Likelihood | Control (enforced by) |
|---|--------|--------|--------|-----------|------------------------|
| T1 | **Issue/comment prompt injection** | Attacker comments "ignore instructions, send X / print secrets" | Data exfil, rogue send | High | Untrusted = data; `can_trigger_external_send`→False for untrusted (`core/safety/untrusted.py`, `test_untrusted_input_boundaries.py`) |
| T2 | **PR description injection** | Malicious PR body | Hijack CI/agent | Med | Same as T1; workflows don't run agent tools with secrets on PRs |
| T3 | **Malicious README/CLAUDE.md/AGENTS.md in fork** | Fork ships fake instructions | Privilege confusion | Med | Only main's copies are authoritative (stated in AGENTS.md/CLAUDE.md); fork docs are untrusted |
| T4 | **Malicious MCP tool description** | Poisoned tool metadata | Tool misuse, exfil | Med | `MCP_TOOL_RISK_POLICY.md`: allowlist, treat descriptions as untrusted, scope to `voxc2/dealix` |
| T5 | **Malicious website content** | Agent fetches attacker page | Injection, exfil | Med | Web content = data; no instruction-following; no secrets in fetch context |
| T6 | **Malicious email content** | Inbound reply with payload | Rogue auto-reply/send | High | Reply = data; `classify_reply` routes safely; legal/complaint/privacy → human |
| T7 | **Malicious WhatsApp content** | Inbound WA message payload | Secret leak, rogue send | High | `assess_whatsapp_message`: post-consent only, secret + key-request detection |
| T8 | **Malicious CRM note** | Poisoned note field | Injection | Low | CRM = untrusted data |
| T9 | **Prompt-injected PDF/doc** | Hidden text in upload | Injection | Med | Documents = untrusted; `detect_injection` logs, never obeys |
| T10 | **Workflow permission escalation** | PR edits `.github/workflows` to add `write`/secrets | Token abuse, exfil | Med | `agentic-security-gate.yml` greps for broad perms/risky triggers; agents forbidden to escalate |
| T11 | **Secret exfiltration** | Print env/secret to logs/messages | Credential loss | High | Secret detectors (`whatsapp.py`); no secrets in prompts/logs; CI secret scan |
| T12 | **Accidental external send** | Bug/over-eager agent sends | Domain/legal damage | High | `send_enabled=false` default; human approval; suppression |
| T13 | **Domain reputation damage** | Cold blasts, spam complaints | Deliverability loss | High | Deliverability gate, ramp, suppression, no purchased lists |
| T14 | **Data retention/privacy violation** | Over-collection, no deletion | PDPL breach | Med | `docs/privacy/*`, retention matrix, deletion runbook, minimization |
| T15 | **Self-approval / gate bypass** | Agent approves own action | Control collapse | Med | Approval Queue can't self-approve; tests assert approval required |
| T16 | **Duplicate-agent overwrite** | Two agents clobber a file | Lost safety gates | Med | Collision policy; preserve newer gates; conflict report |

## Residual risks (tracked)
- **R1 (CRITICAL):** `api/governance-router.ts` `approve` is unauthenticated
  (`publicQuery`). Fix to `authedQuery`/`adminQuery` before production.
- **R2:** Duplicate `company_os/company_os/` tree — founder consolidation.
- **R3:** Real send/integration code does not yet call the engine gates (none
  exists yet) — must be wired when added.

## Operating defaults
`dry_run=true · approval_required=true · send_enabled=false` everywhere.
