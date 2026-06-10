# AI Action Control

## Action classes

### Class A — Internal Insight

Examples: summarize, classify, score, extract.  
**Default:** Allowed with logging.

### Class B — Client-Facing Output

Examples: report, draft, recommendation.  
**Default:** QA required.

### Class C — Internal System Change

Examples: update CRM stage, create task, change workflow status.  
**Default:** Approval required.

### Class D — External Communication

Examples: send email, WhatsApp, publish content.  
**Default:** Explicit approval required. Some channels restricted.

### Class E — Autonomous External Action

**Default:** Blocked.

---

## Dealix MVP policy

```text
A: allowed
B: QA required
C: approval required
D: restricted
E: blocked
```

This keeps product boundaries explicit.

Related: [`AI_ACTION_TAXONOMY.md`](AI_ACTION_TAXONOMY.md).
