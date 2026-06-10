# Human-in-the-Loop Matrix

| AI Action | Risk | Human Role | Approval Required |
|---|---|---|---|
| classify data | Low | reviewer spot-checks | No |
| score leads | Medium | delivery owner reviews top accounts | Yes before delivery |
| draft email | Medium | human approves before use | Yes |
| answer from knowledge base | Medium | source check required | For external use |
| update CRM stage | Medium | owner approval | Yes |
| send message | High | explicit approval + consent | Yes |
| publish claim | High | claim QA | Yes |
| autonomous external action | Critical | not allowed | Blocked |

## MVP rule

```text
Read, classify, draft, recommend = allowed with QA
Execute external action = blocked or approval-only
Autonomous external action = not allowed
```

This protects against “agentic chaos.”
