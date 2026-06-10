# Dealix Event Taxonomy — Arabic
## تصنيف أحداث ديلوكس

**Version:** 1.0
**Date:** 2026-06-03
**Owner:** Head of Data / Agent 8

---

## 1. Overview

This document extends the base event taxonomy from `auto_client_acquisition/revenue_memory/events.py` with additional events, required properties, and validation rules.

---

## 2. Core Event Categories

### 2.1 Lead Lifecycle Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `lead.created` | New lead enters system | sector, source, icp_match_score |
| `lead.qualified` | Lead meets ICP criteria | tier (A/B/nurture/disqualify), budget_confirmed, dm_accessible |
| `lead.disqualified` | Lead doesn't meet criteria | disqualify_reason, was_qualified_before |
| `lead.enriched` | Lead data enriched | enrichment_sources, enrichment_depth |
| `lead.merged` | Duplicate leads merged | merged_lead_ids, master_lead_id |

### 2.2 Company State Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `company.created` | New company record | sector, company_size, region |
| `company.enriched` | Company enriched | enrichment_sources, employee_count, revenue_estimate |
| `company.scored` | Company scored for ICP | icp_score, pain_signals_count, readiness_level |

### 2.3 Signal Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `signal.detected` | Market signal found | signal_type, source, confidence, sector |
| `signal.expired` | Signal no longer valid | reason, was_actioned |
| `signal.confirmed` | Signal confirmed actionable | confirmation_source, priority |

### 2.4 Outreach Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `message.drafted` | Draft created | channel (email/whatsapp), sector, offer_id, template_used |
| `message.approved` | Founder approved | approval_notes, approved_by, revision_number |
| `message.rejected` | Founder rejected | rejection_reason, suggested_changes |
| `message.sent` | Message delivered | channel, recipient_id, send_method, bounce_risk |
| `message.bounced` | Message bounced | bounce_type (hard/soft), bounce_reason |
| `message.opened` | Message opened | open_count, first_open_at, device_type |
| `message.clicked` | Link clicked | link_url, click_count |
| `message.replied` | Reply received | reply_channel, reply_has_interest |

### 2.5 Reply Classification Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `reply.received` | Reply incoming | reply_type, sentiment_score, requires_action |
| `reply.classified` | Reply categorized | classification (positive/interested_later/price_question/more_info/wrong_person/unsubscribe/angry/bounce) |

### 2.6 Meeting Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `meeting.requested` | Meeting requested | meeting_type, proposed_times, requestor |
| `meeting.booked` | Meeting scheduled | scheduled_at, duration, meeting_link |
| `meeting.held` | Meeting occurred | actual_duration, attendees, notes_added |
| `meeting.no_show` | Meeting missed | no_show_reason, rescheduled |

### 2.7 Deal Lifecycle Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `deal.created` | New opportunity | deal_value, deal_currency, offer_id, sector |
| `deal.stage_changed` | Deal moved stages | from_stage, to_stage, move_reason |
| `deal.proposal_sent` | Proposal delivered | proposal_id, proposal_value, delivery_method |
| `deal.won` | Deal closed won | final_value, contract_length, won_reason |
| `deal.lost` | Deal closed lost | lost_reason, competitors_mentioned, was_competitive |
| `deal.stalled` | Deal stalled | stall_duration, stall_reason, recovery_plan |

### 2.8 Customer Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `customer.onboarded` | Onboarding complete | onboarding_duration, modules_completed |
| `customer.health_changed` | Health score updated | previous_score, new_score, change_reason |
| `customer.qbr_generated` | QBR created | qbr_period, qbr_type, sent_at |
| `customer.expansion_detected` | Expansion signal | expansion_type, expansion_value_estimate |
| `customer.churn_predicted` | Churn risk flagged | churn_probability, risk_factors, recommended_action |
| `customer.churned` | Customer churned | churn_reason, churn_type (voluntary/involuntary), renewal_history |

### 2.9 Compliance Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `compliance.consent_recorded` | Consent captured | consent_type, consent_method, consent_source |
| `compliance.opt_out_received` | Opt-out received | opt_out_type, source_channel |
| `compliance.blocked` | Action blocked | blocked_reason, blocking_rule, was_override |
| `compliance.dsr_received` | Data subject request | dsr_type (access/deletion/correction), received_at |
| `compliance.dsr_completed` | DSR fulfilled | completion_method, completion_time_days |

### 2.10 Agent Lifecycle Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `agent.action_requested` | Action queued | action_type, task_id, priority, estimated_duration |
| `agent.action_approved` | Action approved | approver, approval_notes |
| `agent.action_rejected` | Action rejected | rejection_reason, safety_gate_failure |
| `agent.action_executed` | Action completed | execution_duration, result_summary |
| `agent.action_failed` | Action failed | failure_reason, retry_count, escalation_needed |

### 2.11 AI Quality Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `ai.eval_run` | Evaluation executed | eval_type, eval_score, passed, failure_reasons |
| `ai.regression_detected` | Quality regression | previous_score, current_score, affected_metrics |

### 2.12 Pulse Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `pulse.published` | Dashboard updated | pulse_type, metrics_included, anomaly_count |

---

## 3. WhatsApp-Specific Events

### 3.1 Session Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `whatsapp.session_started` | WhatsApp session initiated | session_id, trigger_type, contact_id |
| `whatsapp.session_active` | Session actively engaged | session_duration_seconds, message_count |
| `whatsapp.session_ended` | Session concluded | end_reason, outcome_type |
| `whatsapp.readiness_scan_started` | Readiness assessment begun | scan_type, estimated_duration |
| `whatsapp.readiness_scan_completed` | Readiness assessment done | readiness_score, areas_assessed |

### 3.2 Action Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `whatsapp.action_card_clicked` | CTA card tapped | card_type, card_position, session_id |
| `whatsapp.proposal_card_viewed` | Proposal card opened | proposal_id, view_duration, scroll_depth |
| `whatsapp.payment_handoff_requested` | Payment requested | payment_amount, payment_method, invoice_id |

### 3.3 Handoff Events

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `whatsapp.human_handoff_initiated` | Handoff to human | handoff_reason, queue_position |
| `whatsapp.human_handoff_completed` | Handoff accepted | handling_agent, resolution_time |
| `whatsapp.handoff_feedback` | Feedback on handoff | satisfaction_score, feedback_notes |

---

## 4. Experiment Events

### 4.1 Experiment Lifecycle

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `experiment.created` | Experiment defined | experiment_id, hypothesis, test_type |
| `experiment.started` | Experiment launched | start_date, sample_size_target, segment |
| `experiment.paused` | Experiment paused | pause_reason, elapsed_duration |
| `experiment.resumed` | Experiment resumed | resume_date, remaining_duration |
| `experiment.completed` | Experiment ended | end_date, actual_sample_size, statistical_significance |

### 4.2 Experiment Results

| Event | Description | Required Properties |
|-------|-------------|---------------------|
| `experiment.variant_assigned` | User assigned to variant | experiment_id, variant_id, user_segment |
| `experiment.conversion_recorded` | Conversion tracked | experiment_id, variant_id, conversion_type |
| `experiment.result_calculated` | Results analyzed | winner_variant, confidence_level, uplift_pct |

---

## 5. Required Event Properties

### 5.1 Universal Properties (All Events)

| Property | Type | Required | Description |
|----------|------|----------|-------------|
| event_id | string | yes | Unique event identifier |
| event_type | string | yes | Event name from taxonomy |
| customer_id | string | yes | Dealix customer identifier |
| occurred_at | datetime | yes | UTC timestamp |
| subject_type | string | yes | Entity type (lead/company/deal/customer/agent) |
| subject_id | string | yes | Entity identifier |
| sector | string | yes | Business sector (REQUIRED) |
| offer_id | string | conditional | Required for deal-related events |
| funnel_stage | string | yes | Current funnel stage |
| evidence_level | string | yes | L0-L5 evidence level |
| approval_status | string | conditional | Required for outreach events |
| channel | string | conditional | Required for message events |
| correlation_id | string | no | Groups related events |
| causation_id | string | no | Parent event that triggered this |
| actor | string | yes | Who/what triggered the event |
| schema_version | integer | yes | Schema version (1) |

### 5.2 Property Validation Rules

```python
# Sector validation
VALID_SECTORS = [
    "technology", "healthcare", "finance", "retail",
    "manufacturing", "education", "government", "real_estate",
    "logistics", "hospitality", "construction", "energy"
]

# Offer validation
VALID_OFFERS = [
    "offer_diagnostic", "offer_pilot", "offer_proof",
    "offer_retainer", "offer_training", "offer_consulting"
]

# Funnel stages
VALID_FUNNEL_STAGES = [
    "signal_detected", "researched", "qualified", "drafted",
    "approved_for_outreach", "contacted", "replied", "positive_reply",
    "discovery_scheduled", "discovery_completed", "proposal_needed",
    "proposal_sent", "negotiation", "payment_handoff", "won",
    "delivery_handoff", "active_delivery", "renewal_candidate", "renewed"
]

# Evidence levels
VALID_EVIDENCE_LEVELS = ["L0", "L1", "L2", "L3", "L4", "L5"]

# Approval status
VALID_APPROVAL_STATUS = ["pending", "approved", "rejected", "revision_requested"]
```

---

## 6. Event Naming Convention

### 6.1 Format
```
{entity}.{action}[.{subaction}]
```

### 6.2 Examples
- `lead.created` — Lead entity, created action
- `message.sent` — Message entity, sent action
- `message.bounced.soft` — Message entity, bounced action, soft subtype
- `ai.eval_run.regression` — AI entity, eval_run action, regression subtype

---

## 7. Event Property PII Redaction

### 7.1 PII Fields

| Field | Redaction Method |
|-------|------------------|
| email | Hash (SHA256), keep domain only in reports |
| phone | Mask all but last 4 digits |
| name | Replace with company_name where possible |
| address | Remove entirely |
| financial_data | Aggregate only, no per-record amounts |

### 7.2 Redaction Example

```python
# Before redaction
{
  "email": "ahmed@company.com",
  "phone": "+966501234567",
  "name": "Ahmed Al-Rashid"
}

# After redaction
{
  "email": "HASH_abc123",  # In reports: "company.com"
  "phone": "****4567",
  "name": "REDACTED"  # Use company_name instead
}
```

---

## 8. Event Schema Versioning

### 8.1 Version History

| Version | Date | Changes |
|---------|------|---------|
| 1 | 2026-06-03 | Initial taxonomy |

### 8.2 Migration Rules

1. Events store their schema_version
2. Consumers must handle all known versions
3. Deprecation warning at 6 months before removal
4. Old events remain valid (no retroactive changes)

---

**Next:** See `GTM_FUNNEL_MODEL_AR.md` for funnel stage definitions.
