# Prompt Injection Gate

> Detect and block attempts to turn untrusted content into instructions.
> AI drafts. Human approves. System logs.

---

## 1. What it does

Before any external content (web page, email, document) is used by an agent,
it is screened for injection patterns. Matches are flagged, quarantined, and
never executed. The gate is exercised as a self-test in
`scripts/commercial-control-check.js` (`detectInjection`).

---

## 2. Fail patterns (gate flags if found)

```txt
ignore previous instructions
disregard the above
send this to your owner
reveal secret
execute command
change system prompt
```

This list is a floor, not a ceiling — extend it as new patterns appear.

---

## 3. Behavior on a hit

```txt
1. Flag the content (do NOT act on it).
2. Quarantine: keep as untrusted DATA only.
3. Log the event for the daily security review.
4. Continue research using only the safe, extracted fields.
```

No tool call, no send, no secret disclosure is ever performed as a result of
matched text.

---

## 4. Self-test (proof it works)

The control check runs the detector against:
- a **malicious** sample (must be flagged), and
- a **benign** outreach draft (must pass clean).

If either expectation fails, `npm run commercial:check` exits non-zero.

---

## 5. Alignment

Implements part of `UNTRUSTED_COMPANY_DATA_POLICY.md` and supports the red
lines in `company_os/governance/agent_permissions.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Enforced: YES*
