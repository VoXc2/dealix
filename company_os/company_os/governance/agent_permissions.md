# AI Agent Permissions — Dealix

## Governance Model
**Core Principle**: AI drafts. Human approves. System logs. Company learns.

**Gartner Alignment**: Observe → Advise → Act with Approval → Act Autonomously (not yet)

---

## Permission Levels

### Level 1: Observe (READ ONLY)
**Description**: AI can read and analyze data only
**Status**: ACTIVE

#### Allowed Actions
- Read CRM data and lead exports
- Analyze conversation patterns
- Calculate pipeline metrics
- Generate insights and observations
- Create data visualizations
- Flag anomalies

#### Restrictions
- No data modification
- No external communication
- No recommendations without human review

---

### Level 2: Advise (RECOMMENDATIONS)
**Description**: AI can generate recommendations and insights
**Status**: ACTIVE

#### Allowed Actions
- Generate follow-up recommendations
- Suggest message improvements
- Recommend priority actions
- Create analysis reports
- Propose offer optimizations
- Draft improvement plans

#### Restrictions
- All recommendations flagged as "AI-generated"
- Human must review before acting
- No automatic implementation

---

### Level 3: Draft (CREATE DRAFTS)
**Description**: AI can create drafts for human review
**Status**: ACTIVE

#### Allowed Actions
- Draft outreach messages
- Draft proposals
- Draft follow-up sequences
- Draft executive summaries
- Draft Proof Pack sections
- Draft response scripts

#### Restrictions
- All drafts go to approval queue
- Human must approve before sending
- Sensitive drafts require additional review
- All drafts logged in AI action ledger

---

### Level 4: Act with Approval (EXECUTE WITH SIGN-OFF)
**Description**: AI can execute actions after human approval
**Status**: NOT YET ACTIVE (Planned for Q4 2026)

#### Planned Actions
- Send approved messages
- Update CRM records
- Generate scheduled reports
- Trigger follow-up sequences
- Update dashboards

#### Requirements for Activation
- 6 months of safe operations
- Zero governance incidents
- Client explicit consent
- Enhanced monitoring
- Rollback capability

---

### Level 5: Autonomous (FULL AUTONOMY)
**Description**: AI operates with minimal human oversight
**Status**: NOT ACTIVE (No timeline)

#### Not Allowed Until
- Regulatory framework clear
- Client trust established
- 12+ months of safe operations
- Independent audit passed
- SDAIA approval obtained

---

## Agent Roles and Permissions

### outreach_draft_agent
- **Level**: 3 (Draft)
- **Can**: Draft outreach messages
- **Cannot**: Send messages without approval
- **Logs**: All drafts in approval_queue.json
- **Approval Required**: Yes (all messages)

### pipeline_analysis_agent
- **Level**: 2 (Advise)
- **Can**: Analyze pipeline, score prospects, recommend actions
- **Cannot**: Modify pipeline data
- **Logs**: Analysis actions in ai_action_ledger.jsonl
- **Approval Required**: No (read-only analysis)

### proof_generator
- **Level**: 3 (Draft)
- **Can**: Draft Proof Pack sections, generate insights
- **Cannot**: Deliver to client without review
- **Logs**: Generation actions in ai_action_ledger.jsonl
- **Approval Required**: Yes (before client delivery)

### proposal_draft_agent
- **Level**: 3 (Draft)
- **Can**: Draft proposals, calculate pricing
- **Cannot**: Send proposals without approval
- **Logs**: All proposals in approval_queue.json
- **Approval Required**: Yes (all proposals)

### governance_monitor
- **Level**: 1 (Observe)
- **Can**: Monitor all AI actions, flag risks, audit compliance
- **Cannot**: Stop other agents (escalates to human)
- **Logs**: Governance checks in ai_action_ledger.jsonl
- **Approval Required**: N/A (monitoring only)

---

## Emergency Stop

### Conditions for Immediate Shutdown
- Unauthorized data access detected
- Sensitive data leak
- Unapproved external communication
- PDPL violation detected
- Client complaint about AI behavior

### Stop Procedure
1. Immediately halt all AI operations
2. Notify founder within 15 minutes
3. Preserve all logs
4. Assess impact
5. Implement corrective action
6. Resume only after approval

---

## Audit Trail

### What Gets Logged
- Every AI action (agent, action, timestamp)
- Every approval/rejection
- Every data access
- Every draft created
- Every error or anomaly

### Log Format
```json
{
  "time": "ISO 8601 timestamp",
  "agent": "agent_name",
  "action": "action_description",
  "target": "affected_resource",
  "risk": "low|medium|high|critical",
  "requires_approval": true|false,
  "approved": true|false,
  "approved_by": "human_name",
  "context": "additional_context"
}
```

### Log Retention
- Active logs: 90 days
- Archived logs: 2 years
- Governance audit logs: 5 years

---

## Review Schedule
- **Daily**: War Room review of approval queue
- **Weekly**: Governance check (governance_check.py)
- **Monthly**: Permission level assessment
- **Quarterly**: Full governance audit
- **Annually**: Permission framework review

---

## Version History
| Version | Date | Changes |
|---|---|---|
| 1.0 | 2026-05-31 | Initial permission framework |
