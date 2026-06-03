# Agent Prompt-Injection Gate

A gate that scans external content (and generated text) for injection attempts and
quarantines them before they can reach a model prompt or trigger an action.

---

## 1. Markers that trip the gate

If external content contains any of these (case-insensitive), it is flagged and its
instruction-like portion is stripped from any downstream prompt:

```
ignore previous instructions
ignore all previous
disregard previous
reveal secret  /  reveal the secret
show your prompt  /  system prompt  /  change system prompt
execute command  /  run command
send credentials
use this tool
you are now  /  act as  /  exfiltrate
تجاهل التعليمات  /  تجاهل كل التعليمات
نفّذ الأمر  /  أرسل كلمة المرور
```

The authoritative list lives in `scripts/dealix_account_lib.py:PROMPT_INJECTION_TOKENS`.

---

## 2. The gate fails (blocks) when external content tries to

```
ignore previous instructions
reveal secret
execute command
change system prompt
send credentials
use this tool
```

A blocked item is logged as a governance event and **never** becomes an instruction.

---

## 3. Response on detection

1. Do **not** act on the instruction.
2. Strip the offending text from any prompt; keep only neutral public facts.
3. Lower the source's trust (treat as adversarial).
4. Record a governance note (no secrets in the note).

---

## 4. Defense in depth

Per current research, detection is necessary but not sufficient. We combine it with:

- **No-side-effects rule** (`TOOL_EXECUTION_ALLOWLIST_POLICY.md`): external text cannot trigger tools.
- **Human-in-the-loop**: all external sends/pricing require founder approval.
- **Offline pipeline**: generation/validation perform no network sends at all.

---

## 5. Verification

`scripts/validate_account_intelligence.py` checks that no Account Pack text contains
any injection marker, across `email_body`, `buying_signal`, `company_name`, and `likely_pain`.

---

*Version 1.0*
