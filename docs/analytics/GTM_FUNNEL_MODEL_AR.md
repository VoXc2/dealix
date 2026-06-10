# GTM Funnel Model — Arabic
## نموذج قمع GTM

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Funnel Overview

```
Signal Detected
      ↓
Prospect Researched
      ↓
Qualified (A/B Tier)
      ↓
Draft Generated
      ↓
Quality Passed (QA)
      ↓
Founder Approved
      ↓
Sent (Email/WhatsApp)
      ↓
Replied
      ↓
Positive Reply
      ↓
Discovery Booked
      ↓
Discovery Completed
      ↓
Proposal Needed
      ↓
Proposal Sent
      ↓
Negotiation
      ↓
Payment Handoff
      ↓
WON
      ↓
Delivery Handoff
```

---

## 2. Stage Definitions

### Stage 1: Signal Detected

| Attribute | Value |
|-----------|-------|
| Event Name | `signal.detected` |
| Required Fields | sector, signal_type, source, confidence |
| Owner | Market Radar Agent |
| Next Action | Research company |
| Drop-off Signal | No company match within 48 hours |
| Conversion Metric | Signals → Researched % |
| Risk | Signal expired before action |

### Stage 2: Prospect Researched

| Attribute | Value |
|-----------|-------|
| Event Name | `company.scored` |
| Required Fields | sector, company_size, icp_score, pain_signals |
| Owner | Research Agent |
| Next Action | ICP qualification check |
| Drop-off Signal | ICP score < 40 |
| Conversion Metric | Researched → Qualified % |
| Risk | Low ICP match |

### Stage 3: Qualified

| Attribute | Value |
|-----------|-------|
| Event Name | `lead.qualified` |
| Required Fields | tier (A/B), budget_confirmed, dm_accessible |
| Owner | Sales Ops |
| Next Action | Draft generation |
| Drop-off Signal | Tier C or disqualified |
| Conversion Metric | Qualified → Drafted % |
| Risk | Budget not confirmed |

### Stage 4: Draft Generated

| Attribute | Value |
|-----------|-------|
| Event Name | `message.drafted` |
| Required Fields | channel, offer_id, template_used, sector |
| Owner | AI Agent |
| Next Action | Quality check |
| Drop-off Signal | QA failure |
| Conversion Metric | Drafted → QA Passed % |
| Risk | Quality below threshold |

### Stage 5: Quality Passed

| Attribute | Value |
|-----------|-------|
| Event Name | `ai.eval_run` (result=pass) |
| Required Fields | eval_type, eval_score, failure_reasons |
| Owner | QA System |
| Next Action | Founder approval |
| Drop-off Signal | Founder rejection |
| Conversion Metric | QA Passed → Approved % |
| Risk | Founder overloaded |

### Stage 6: Founder Approved

| Attribute | Value |
|-----------|-------|
| Event Name | `message.approved` |
| Required Fields | approval_notes, approved_by, revision_number |
| Owner | Founder |
| Next Action | Send message |
| Drop-off Signal | Not sent within 24 hours |
| Conversion Metric | Approved → Sent % |
| Risk | Delay in sending |

### Stage 7: Sent

| Attribute | Value |
|-----------|-------|
| Event Name | `message.sent` |
| Required Fields | channel, recipient_id, send_method |
| Owner | Outreach Agent |
| Next Action | Wait for reply |
| Drop-off Signal | Bounce |
| Conversion Metric | Sent → Replied % |
| Risk | Bounce, spam flags |

### Stage 8: Replied

| Attribute | Value |
|-----------|-------|
| Event Name | `reply.received` |
| Required Fields | reply_type, sentiment_score |
| Owner | Sales Ops |
| Next Action | Reply classification |
| Drop-off Signal | No classification within 24 hours |
| Conversion Metric | Replied → Positive % |
| Risk | Wrong person, unsubscribe |

### Stage 9: Positive Reply

| Attribute | Value |
|-----------|-------|
| Event Name | `reply.classified` (classification=positive) |
| Required Fields | classification, sentiment_score |
| Owner | Sales Agent |
| Next Action | Book discovery meeting |
| Drop-off Signal | Meeting not booked within 72 hours |
| Conversion Metric | Positive → Meeting Booked % |
| Risk | Interest lost |

### Stage 10: Discovery Booked

| Attribute | Value |
|-----------|-------|
| Event Name | `meeting.booked` |
| Required Fields | scheduled_at, duration, meeting_link |
| Owner | Sales Agent |
| Next Action | Hold meeting |
| Drop-off Signal | No-show |
| Conversion Metric | Booked → Held % |
| Risk | No-show |

### Stage 11: Discovery Completed

| Attribute | Value |
|-----------|-------|
| Event Name | `meeting.held` |
| Required Fields | actual_duration, attendees, notes_added |
| Owner | Sales Agent |
| Next Action | Determine if proposal needed |
| Drop-off Signal | Not moving to proposal within 7 days |
| Conversion Metric | Held → Proposal % |
| Risk | Deal stalled |

### Stage 12: Proposal Needed

| Attribute | Value |
|-----------|-------|
| Event Name | `deal.stage_changed` (to=proposal_needed) |
| Required Fields | deal_value, offer_id, sector |
| Owner | Sales Agent |
| Next Action | Send proposal |
| Drop-off Signal | Proposal not sent within 48 hours |
| Conversion Metric | Proposal Needed → Sent % |
| Risk | Proposal delayed |

### Stage 13: Proposal Sent

| Attribute | Value |
|-----------|-------|
| Event Name | `deal.proposal_sent` |
| Required Fields | proposal_id, proposal_value, delivery_method |
| Owner | Sales Agent |
| Next Action | Follow up, handle objections |
| Drop-off Signal | No response within 7 days |
| Conversion Metric | Proposal → Negotiation % |
| Risk | Proposal rejected |

### Stage 14: Negotiation

| Attribute | Value |
|-----------|-------|
| Event Name | `deal.stage_changed` (to=negotiation) |
| Required Fields | negotiation_topics, decision_makers |
| Owner | Sales Agent |
| Next Action | Close deal |
| Drop-off Signal | Not closed within 30 days |
| Conversion Metric | Negotiation → Payment Handoff % |
| Risk | Price negotiation, competitor |

### Stage 15: Payment Handoff

| Attribute | Value |
|-----------|-------|
| Event Name | `deal.stage_changed` (to=payment_handoff) |
| Required Fields | payment_amount, payment_method, invoice_id |
| Owner | Finance |
| Next Action | Process payment |
| Drop-off Signal | Payment not received within 14 days |
| Conversion Metric | Payment Handoff → Won % |
| Risk | Payment failure |

### Stage 16: WON

| Attribute | Value |
|-----------|-------|
| Event Name | `deal.won` |
| Required Fields | final_value, contract_length, won_reason |
| Owner | Sales Agent |
| Next Action | Handoff to delivery |
| Conversion Metric | Win rate = WON / (WON + LOST) |
| Risk | Post-win cancellation |

### Stage 17: Delivery Handoff

| Attribute | Value |
|-----------|-------|
| Event Name | `customer.onboarded` |
| Required Fields | onboarding_duration, modules_completed |
| Owner | Delivery |
| Next Action | Begin delivery |
| Conversion Metric | Won → Active % |
| Risk | Client dissatisfaction |

---

## 3. Conversion Benchmarks

| Stage Transition | Target | Good | Excellent |
|-------------------|--------|------|------------|
| Signal → Researched | 60% | 70% | 80% |
| Researched → Qualified | 40% | 50% | 60% |
| Qualified → Drafted | 80% | 90% | 95% |
| Drafted → QA Passed | 70% | 80% | 90% |
| QA Passed → Approved | 60% | 70% | 80% |
| Approved → Sent | 90% | 95% | 98% |
| Sent → Replied | 5% | 8% | 10% |
| Replied → Positive | 30% | 40% | 50% |
| Positive → Booked | 50% | 60% | 70% |
| Booked → Held | 80% | 85% | 90% |
| Held → Proposal | 70% | 80% | 90% |
| Proposal → Negotiation | 50% | 60% | 70% |
| Negotiation → Payment | 70% | 80% | 90% |
| Payment → Won | 90% | 95% | 98% |
| Won → Delivery | 95% | 98% | 100% |

---

## 4. Drop-off Analysis

### 4.1 Common Drop-off Points

| Drop-off Point | Primary Cause | Solution |
|----------------|---------------|----------|
| Signal → Researched | No matching company | Expand signal sources |
| Qualified → Drafted | Budget not confirmed | Better qualification |
| QA → Approved | Quality issues | Improve templates |
| Approved → Sent | Delay in sending | Automate sending |
| Sent → Replied | Targeting issues | Improve ICP |
| Replied → Positive | Message quality | Improve content |
| Positive → Booked | No follow-up | Automate booking |
| Held → Proposal | Poor discovery | Improve discovery |
| Proposal → Negotiation | Price objections | Better pricing |
| Negotiation → Payment | Contract terms | Streamline contract |

### 4.2 Drop-off Alerts

```python
# Alert thresholds (generate decision)
DROPOFF_ALERTS = {
    "signal_to_researched": {"threshold": 0.5, "alert": "LOW_SIGNAL_MATCH"},
    "qualified_to_drafted": {"threshold": 0.6, "alert": "QUALIFICATION_TOO_STRICT"},
    "drafted_to_qa_passed": {"threshold": 0.5, "alert": "QUALITY_ISSUES"},
    "sent_to_replied": {"threshold": 0.03, "alert": "LOW_REPLY_RATE"},
    "positive_to_booked": {"threshold": 0.4, "alert": "BOOKING_BOTTLENECK"},
    "held_to_proposal": {"threshold": 0.5, "alert": "DISCOVERY_ISSUES"},
}
```

---

## 5. Funnel Velocity

### 5.1 Time-in-Stage Targets

| Stage | Target | Max Acceptable |
|-------|--------|----------------|
| Signal → Researched | 24 hours | 48 hours |
| Researched → Qualified | 48 hours | 72 hours |
| Qualified → Drafted | 4 hours | 24 hours |
| Drafted → QA Passed | 1 hour | 4 hours |
| QA Passed → Approved | 4 hours | 24 hours |
| Approved → Sent | 1 hour | 4 hours |
| Sent → Replied | 72 hours | 168 hours |
| Replied → Positive | 24 hours | 48 hours |
| Positive → Booked | 48 hours | 72 hours |
| Booked → Held | 0 (meeting day) | 7 days |
| Held → Proposal | 72 hours | 168 hours |
| Proposal → Negotiation | 7 days | 14 days |
| Negotiation → Payment | 14 days | 30 days |
| Payment → Won | 7 days | 14 days |

### 5.2 Velocity Alerts

```python
# Stuck pipeline alerts
STUCK_ALERTS = {
    "in_draft": {"days": 3, "alert": "DRAFT_STUCK"},
    "in_qa": {"days": 1, "alert": "QA_STUCK"},
    "in_approval": {"days": 2, "alert": "APPROVAL_STUCK"},
    "in_negotiation": {"days": 30, "alert": "DEAL_STALLED"},
}
```

---

**Next:** See `REVENUE_FUNNEL_MODEL_AR.md` for revenue-specific funnel.
