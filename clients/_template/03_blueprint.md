# Phase 3: Operating Blueprint

**Client:** [Company Name]
**Date:** [YYYY-MM-DD]
**Designed by:** [Team Member]
**Approved by client:** [ ] Yes / [ ] Pending

---

## Blueprint Summary

_What operating systems will be built, in what order, and what the client will be able to do when complete._

## System Architecture

### Systems to Build

| System | Scope | Priority | Sprint |
|--------|-------|----------|--------|
| Revenue Command Room | | 1 | Sprint 1 |
| Company Brain | | 2 | Sprint 2 |
| WhatsApp Follow-up | | 3 | Sprint 2 |
| Client Delivery | | 4 | Sprint 3 |

### System 1: Revenue Command Room

**Objective:** Give the founder a daily cockpit for pipeline, approvals, and follow-up.

**Components:**
- [ ] Pipeline view by stage
- [ ] Draft message queue with approval
- [ ] Daily action summary
- [ ] Booking flow for inbound leads
- [ ] WhatsApp conversation overview

**Success Criteria:**
- Founder can see all active deals in one screen
- No outbound message leaves without approval
- Daily review takes less than 15 minutes

### System 2: Company Brain

**Objective:** Create structured decision discipline.

**Components:**
- [ ] Signal capture (market, competitor, customer, internal)
- [ ] Decision register with owner and metrics
- [ ] Risk register with severity tracking
- [ ] Opportunity register with potential scoring
- [ ] Assumption log

**Success Criteria:**
- Key decisions are documented with context
- Risks are visible before they become crises
- Weekly brain review takes 20 minutes

### System 3: WhatsApp Follow-up

**Objective:** Move from ad-hoc messaging to governed communication.

**Components:**
- [ ] WhatsApp Cloud API connection
- [ ] Template management
- [ ] Conversation tracking
- [ ] Draft-only mode by default
- [ ] Webhook integration for status updates

**Success Criteria:**
- All outbound WhatsApp is reviewable
- No message sent without explicit approval
- Response tracking is automated

### System 4: Client Delivery (if applicable)

**Objective:** Standardize how the client delivers to their own clients.

**Components:**
- [ ] Delivery lifecycle templates
- [ ] Progress tracking
- [ ] Proof pack generation

## Data Architecture

| Data Entity | Source | Storage | Access |
|------------|--------|---------|--------|
| Prospects | Intake / booking | MySQL | Command Room |
| Deals | Pipeline | MySQL | Command Room |
| Messages | WhatsApp API | MySQL | WhatsApp OS |
| Signals | Manual / AI | MySQL | Brain OS |
| Decisions | Manual | MySQL | Brain OS |

## Integration Points

| Integration | Status | Notes |
|------------|--------|-------|
| WhatsApp Cloud API | | |
| Email (future) | | |
| Calendar / Booking | | |

## Timeline

| Sprint | Duration | Deliverables |
|--------|----------|-------------|
| Sprint 1 | 1-2 weeks | |
| Sprint 2 | 1-2 weeks | |
| Sprint 3 | 1-2 weeks | |

## Client Responsibilities

- [ ] Provide WhatsApp Business API access (if applicable)
- [ ] Designate a daily operator for Command Room
- [ ] Participate in weekly review sessions
- [ ] Provide feedback within 48 hours of each sprint delivery

---

**Previous phase:** [02_diagnosis.md](02_diagnosis.md)
**Next phase:** [04_sprint_plan.md](04_sprint_plan.md)
