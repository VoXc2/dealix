# Incident Response

Dealix needs an incident response process **before** enterprise. Every incident must produce a rule, a test, or a checklist update — that is how the firm becomes anti-fragile.

## 1. Incident types

- PII exposure
- Source misuse
- Unapproved external action
- Unsupported claim
- Hallucinated answer
- Wrong client data
- Partner violation

## 2. Response flow

```
Detect
→ Contain
→ Notify internal owner
→ Assess severity
→ Correct output
→ Log incident
→ Update rule
→ Add test
→ Update playbook
```

## 3. Severity levels

| Severity | Examples | Buyer notice |
| --- | --- | --- |
| Sev-1 | PII exposure; cross-tenant leak | within 24h, contract-bound |
| Sev-2 | Unapproved external action; unsupported claim | within 72h |
| Sev-3 | Hallucinated answer caught internally | within sprint review |
| Sev-4 | Cosmetic / non-impacting | logged only |

## 4. The rule

> Every incident must create a rule, a test, or a playbook update. Incidents that do not change the system happen again.

## 5. Operating discipline

- Sev-1 and Sev-2 incidents pause the affected agent and channel until cleared.
- A postmortem is written for every Sev-1 and Sev-2 incident.
- Incident records are immutable.
- The rule pack derived from incidents is versioned.

## 6. Anti-patterns

- Containment without root-cause analysis.
- Postmortems that blame the operator.
- Incident records that exist only in chat.
- Repeated incidents of the same type — that is a structural failure to update rules.

## 7. The principle

> Anti-fragility is the byproduct of disciplined incident response.
