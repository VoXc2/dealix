# Tool Execution Allowlist Policy

Agents may only run tools on an explicit **allowlist**, and **no external content** can
add to, change, or trigger that list.

---

## 1. Principle

> Tool execution is decided by Dealix policy and human approval — never by text found
> in an external page, email, or file. External content is data, not a trigger.

---

## 2. Allowlist (current system)

| Tool / action | Allowed? | Approval |
|---------------|:--------:|----------|
| Read local repo data (`data/`, `reports/`) | ✅ | none (read-only) |
| Generate packs/reports locally | ✅ | none (offline, deterministic) |
| Run validator locally | ✅ | none |
| Draft outreach/proposals | ✅ (draft only) | founder approves send |
| **Send email / message** | ❌ for agents | **human only** |
| **Place a call** | ❌ | **human only** |
| **WhatsApp cold outreach** | ❌ | never |
| **Delete/modify production secrets** | ❌ | never |
| **Network calls driven by external text** | ❌ | never |

This complements `company_os/governance/agent_permissions.md` (Observe / Advise / Draft only).

---

## 3. Hard rules

```
no tool execution based on external text
no external sending by agents
no automated calling
no purchased lists
no secrets in prompts/logs/reports
```

Anything not on the allowlist is denied by default (**deny-by-default**).

---

## 4. Why

External content can be adversarial (prompt injection). Gating tool execution behind a
fixed allowlist + human approval means a malicious page cannot make an agent send data,
spend money, or leak secrets — even if detection misses the injection text.

---

## 5. Enforcement

- The account-intelligence pipeline is **offline**: it never sends or calls.
- Sends/pricing flow through the founder approval queue.
- Changes to this allowlist are a human decision, version-controlled in this file.

---

*Version 1.0 — read with EXTERNAL_CONTENT_UNTRUSTED_DATA_POLICY and AGENT_PROMPT_INJECTION_GATE*
