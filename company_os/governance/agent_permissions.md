# AI Agent Permissions Matrix

---

## Permission Levels

| Level | Description | Can Do AI? | Human Required? |
|-------|-------------|-----------:|-----------------|
| **Observe** | Read and analyze data | ✅ Yes | ❌ No |
| **Advise** | Make recommendations | ✅ Yes | ❌ No |
| **Draft** | Write drafts for review | ✅ Yes | ❌ No |
| **Act with Approval** | Execute after human approval | ✅ Yes | ✅ Yes |
| **Autonomous** | Full self-execution | ❌ NO | N/A |

---

## Agent Roles & Permissions

### prospect_research Agent
| Action | Level | Notes |
|--------|-------|-------|
| Research companies | Observe | Public data only |
| Score prospects | Observe | Based on defined criteria |
| Draft outreach messages | Draft | Requires approval before send |
| Find contact info | Observe | Respect privacy |
| **Send messages** | **NOT ALLOWED** | **Human only** |

### war_room Agent
| Action | Level | Notes |
|--------|-------|-------|
| Read pipeline data | Observe | Internal data |
| Generate reports | Draft | Auto-generated, human reviews |
| Score pipeline health | Advise | Recommendations only |
| **Update CRM** | **NOT ALLOWED** | **Human only** |
| **Send client data externally** | **NOT ALLOWED** | **Never** |

### delivery Agent
| Action | Level | Notes |
|--------|-------|-------|
| Analyze client data | Observe | Anonymized where possible |
| Generate report drafts | Draft | Human review before delivery |
| Create visualizations | Draft | Human review |
| **Send deliverables to client** | **Act with Approval** | **Founder approves first** |
| **Access raw PII** | **NOT ALLOWED** | **Anonymized only** |

### finance Agent
| Action | Level | Notes |
|--------|-------|-------|
| Calculate metrics | Observe | From approved data |
| Generate scorecards | Draft | Internal use |
| Track invoices | Observe | Read-only monitoring |
| **Create invoices** | **NOT ALLOWED** | **Human only** |
| **Process payments** | **NOT ALLOWED** | **Human only** |

### governance Agent
| Action | Level | Notes |
|--------|-------|-------|
| Review AI actions | Observe | Audit trail |
| Flag compliance risks | Advise | Alerts only |
| Verify PDPL compliance | Observe | Checklist validation |
| **Override human decisions** | **NOT ALLOWED** | **Never** |

---

## Critical Rules

### NEVER (Red Lines)

| # | Rule | Violation Consequence |
|---|------|----------------------|
| 1 | AI never sends external messages without approval | Immediate shutdown |
| 2 | AI never processes raw PII in public tools | Immediate shutdown |
| 3 | AI never makes pricing decisions | Immediate shutdown |
| 4 | AI never deletes data | Immediate shutdown |
| 5 | AI never modifies production secrets | Immediate shutdown |
| 6 | AI never gives legal/compliance advice directly to clients | Immediate shutdown |
| 7 | AI never operates autonomously on client accounts | Immediate shutdown |

### ALWAYS

| # | Rule |
|---|------|
| 1 | Human approves all external communications |
| 2 | Human approves all pricing and proposals |
| 3 | Human approves all deliverables before client delivery |
| 4 | All AI actions logged in ai_action_ledger |
| 5 | All client data anonymized before AI analysis |
| 6 | Weekly governance review of all AI actions |

---

## Approval Workflow

```
AI drafts → Human reviews → Approve/Reject → If approved: execute → Log
                        → If rejected: revise or discard
```

### Escalation Matrix

| Decision Type | Approver |
|---------------|----------|
| Outreach messages | Founder |
| Pricing below 5,000 SAR | Founder |
| Pricing above 5,000 SAR | Founder + 24hr cooling |
| Client data handling | Founder + compliance check |
| Deliverable delivery | Founder review |
| System changes | Founder |

---

*Version: 1.0 | Last Updated: 2026-05-31 | Enforced: YES*
