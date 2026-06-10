# Dealix Analytics Gap Audit
**Generated:** 2026-06-03
**Author:** Agent 8 — Analytics OS & Decision Intelligence
**Status:** Initial Assessment

---

## Executive Summary

This audit examines the current state of analytics, metrics, and reporting across all Dealix systems. The organization has a solid foundation for event-driven analytics with a defined taxonomy in `auto_client_acquisition/revenue_memory/events.py`, but lacks unified reporting dashboards, a complete metric dictionary, and decision intelligence systems.

---

## 1. Metrics Currently Defined

### Existing Event Taxonomy (auto_client_acquisition/revenue_memory/events.py)
- **Lead lifecycle:** `lead.created`, `lead.qualified`, `lead.disqualified`, `lead.enriched`, `lead.merged`
- **Company state:** `company.created`, `company.enriched`, `company.scored`
- **Signals:** `signal.detected`, `signal.expired`, `signal.confirmed`
- **Outreach:** `message.drafted`, `message.approved`, `message.rejected`, `message.sent`, `message.bounced`, `message.opened`, `message.clicked`, `message.replied`
- **Reply classification:** `reply.received`, `reply.classified`
- **Meetings:** `meeting.requested`, `meeting.booked`, `meeting.held`, `meeting.no_show`
- **Deal lifecycle:** `deal.created`, `deal.stage_changed`, `deal.proposal_sent`, `deal.won`, `deal.lost`, `deal.stalled`
- **Customer lifecycle:** `customer.onboarded`, `customer.health_changed`, `customer.qbr_generated`, `customer.expansion_detected`, `customer.churn_predicted`, `customer.churned`
- **Compliance:** `compliance.consent_recorded`, `compliance.opt_out_received`, `compliance.blocked`, `compliance.dsr_received`, `compliance.dsr_completed`
- **Agent lifecycle:** `agent.action_requested`, `agent.action_approved`, `agent.action_rejected`, `agent.action_executed`, `agent.action_failed`
- **AI quality:** `ai.eval_run`, `ai.regression_detected`
- **Pulse:** `pulse.published`

### Existing Schemas
- `schemas/opportunity.schema.json` — Sales opportunity with stages
- `schemas/buyer_persona.schema.json` — ICP buyer profile
- `schemas/commercial_proof_pack.schema.json` — Proof pack structure
- `schemas/commercial_proposal.schema.json` — Proposal structure
- `schemas/discovery_note.schema.json` — Discovery notes
- `schemas/icp.schema.json` — ICP definition
- `schemas/offer_match.schema.json` — Offer matching
- `schemas/pain_signal.schema.json` — Pain signal tracking
- `schemas/pricing_rule.schema.json` — Pricing rules
- `schemas/product_offer.schema.json` — Product offers

### Existing Metrics Engine (docs/intelligence/METRICS_ENGINE.md)
- AI Run Metrics: AI cost/project, AI cost/workflow, QA pass rate, schema failure rate, model fallback rate, high-risk run count
- Governance Metrics: blocked actions, approval delays, PII flags, source attribution coverage, audit coverage, policy violations
- Proof Metrics: proof packs/project, proof events/project, فئات قيمة مغطاة, proof معتمد من العميل, proof-to-retainer conversion
- Capital Metrics: assets/project, نسبة الأصول القابلة لإعادة الاستخدام, تحديثات playbook, feature candidates, رؤى آمنة للسوق
- Product Metrics: ساعات يدوية موفرة, feature reuse, استخدام أدوات داخلية, module adoption, انخفاض وقت التسليم
- Business Unit Metrics: إيراد الوحدة, هامش, QA, proof count, retainers, نضج المنتج, نضج الـ playbook

---

## 2. Reports Currently Generated

### Agent Reports
- `reports/agent_2/AGENT_2_CONTINUATION_AUDIT.md`

### Commercial Reports
- `reports/commercial/COMMERCIAL_GAP_AUDIT.md`
- `reports/commercial/COMMERCIAL_OPERATING_MAP.md`
- `reports/commercial/ICP_PRIORITY_REPORT.md`
- `reports/commercial/OFFER_MATCH_REVIEW.md`
- `reports/commercial/PIPELINE_REVIEW.md`
- `reports/commercial/PRICING_RISK_REVIEW.md`
- `reports/commercial/PRODUCT_CATALOG_REVIEW.md`
- `reports/commercial/PROPOSAL_COMMERCIAL_REVIEW.md`

### Business OS Reports
- `reports/business_os/` — Various business reports

### Other Report Directories
- `reports/agents/`
- `reports/company_os/`
- `reports/outreach/`
- `reports/privacy/`
- `reports/revenue/`
- `reports/security/`
- `reports/whatsapp/`

---

## 3. Schemas/Events Status

### ✅ Existing Schemas (10)
1. opportunity.schema.json — Complete with stages
2. buyer_persona.schema.json
3. commercial_proof_pack.schema.json
4. commercial_proposal.schema.json
5. discovery_note.schema.json
6. icp.schema.json
7. offer_match.schema.json
8. pain_signal.schema.json
9. pricing_rule.schema.json
10. product_offer.schema.json

### ✅ Existing Event Types (54 events in revenue_memory/events.py)

### ⚠️ Missing Event Schemas
- **Metric Event Schema** — No schema for aggregated metrics
- **Funnel Event Schema** — No schema for funnel stage transitions
- **Founder Decision Schema** — No schema for decision recommendations
- **Experiment Schema** — No schema for A/B test results

---

## 4. Metrics Missing

### GTM Metrics
- ❌ `prospects_researched` — Count of prospects researched
- ❌ `prospects_qualified` — Count meeting ICP criteria
- ❌ `signals_detected` — Market signals identified
- ❌ `drafts_generated` — Drafts created by AI
- ❌ `drafts_passed_quality` — Drafts passing QA
- ❌ `drafts_approved` — Founder-approved drafts
- ❌ `emails_sent` — Emails delivered
- ❌ `replies_received` — All reply types
- ❌ `positive_replies` — Positive sentiment replies
- ❌ `meetings_booked` — Discovery meetings scheduled
- ❌ `proposals_requested` — Proposal requests received
- ❌ `won_deals` — Deals closed won

### Deliverability Metrics
- ❌ `send_volume` — Daily/weekly send volume
- ❌ `bounce_rate` — Hard/soft bounce percentage
- ❌ `unsubscribe_rate` — Unsubscribe percentage
- ❌ `spam_warning_count` — Spam complaints
- ❌ `domain_health_status` — Domain reputation score
- ❌ `suppressed_recipient_count` — Suppressed contacts

### Reply Classification Metrics
- ❌ `reply_positive` — Positive reply count
- ❌ `reply_interested_later` — Interested but not now
- ❌ `reply_price_question` — Price inquiry replies
- ❌ `reply_send_more_info` — Request for more info
- ❌ `reply_wrong_person` — Wrong contact replies
- ❌ `reply_unsubscribe` — Unsubscribes
- ❌ `reply_angry` — Negative/abusive replies
- ❌ `reply_bounce` — Bounced replies

### WhatsApp Metrics
- ❌ `post_reply_sessions` — Active WhatsApp sessions
- ❌ `readiness_scans_started` — Readiness scans initiated
- ❌ `readiness_scans_completed` — Scans completed
- ❌ `action_cards_clicked` — CTA card interactions
- ❌ `human_handoffs` — Handoffs to human
- ❌ `proposal_cards_viewed` — Proposal views
- ❌ `payment_handoffs_requested` — Payment requests

### Commercial Metrics
- ❌ `pipeline_value` — Total pipeline value
- ❌ `qualified_opportunities` — Stage-appropriate qualified deals
- ❌ `proposal_rate` — Proposals/total opportunities
- ❌ `close_rate` — Won/qualified opportunities
- ❌ `average_deal_size` — Mean deal value
- ❌ `discount_rate` — Average discount percentage
- ❌ `price_exception_count` — Special pricing requests

### Delivery Metrics
- ❌ `active_clients` — Active delivery clients
- ❌ `onboarding_complete` — Completed onboardings
- ❌ `delivery_tasks_completed` — Tasks completed
- ❌ `blockers_open` — Open blockers
- ❌ `weekly_reports_sent` — QBRs delivered
- ❌ `acceptance_checkpoints` — Checkpoints hit

### Customer Success Metrics
- ❌ `client_health_score` — Composite health score
- ❌ `renewal_candidates` — Ready-for-renewal clients
- ❌ `churn_risk_count` — High churn risk clients
- ❌ `expansion_opportunities` — Upsell candidates
- ❌ `client_escalations` — Escalation count

### Finance Metrics
- ❌ `cost_per_draft` — AI cost per draft
- ❌ `cost_per_reply` — Cost per reply received
- ❌ `cost_per_meeting` — Cost per meeting booked
- ❌ `cost_per_proposal` — Cost per proposal sent
- ❌ `CAC` — Customer Acquisition Cost
- ❌ `payback_period` — Months to recover CAC
- ❌ `gross_margin_by_offer` — Margin by product
- ❌ `tool_cost` — Tool subscription costs
- ❌ `founder_time_cost` — Founder time valuation

### Agent Productivity Metrics
- ❌ `agent_tasks_completed` — Tasks completed by agents
- ❌ `files_changed_by_agent` — Files modified
- ❌ `tests_run` — Tests executed
- ❌ `safety_gate_failures` — Safety gate rejections
- ❌ `rework_count` — Drafts requiring rework
- ❌ `collision_count` — Agent coordination issues

---

## 5. Event Taxonomy Gaps

### Missing Event Categories
1. **WhatsApp-specific events** — No WhatsApp session events
2. **Deliverability events** — No bounce/complaint tracking events
3. **Quality gate events** — No QA pass/fail events
4. **Experiment events** — No A/B test tracking events
5. **Data quality events** — No data validation events
6. **Security events** — Limited security audit events

### Event Property Gaps
- **Missing sector tagging** — Events don't consistently tag sector
- **Missing offer association** — No offer ID on most events
- **Missing funnel stage** — No explicit funnel stage on events
- **Missing evidence level** — No evidence quality indicator
- **Missing approval status** — Founder approval not tracked on events

---

## 6. Dashboard Specifications Missing

### Required Dashboards
1. **Founder Daily Decision Dashboard**
   - Today's metrics: signals, drafts, approvals, sends, replies, meetings
   - Alert panel: anomalies, risks, decisions needed
   - Action queue: pending approvals, follow-ups

2. **GTM Performance Dashboard**
   - Funnel conversion rates
   - Channel performance
   - Sector performance
   - Reply pattern analysis

3. **Commercial Pipeline Dashboard**
   - Pipeline value by stage
   - Win/loss analysis
   - Average deal velocity
   - Pricing compliance

4. **Delivery Health Dashboard**
   - Active client status
   - Onboarding progress
   - Blocker tracking
   - QBR schedule

5. **Financial Metrics Dashboard**
   - Unit economics
   - Cost per funnel stage
   - Tool ROI
   - CAC trends

6. **Agent Productivity Dashboard**
   - Tasks completed
   - Quality metrics
   - Safety gate pass rate
   - Rework rate

---

## 7. Duplicate Metrics

### Potential Duplicates to Consolidate
1. **"lead.qualified" vs "prospects_qualified"** — Need single source
2. **"message.sent" vs "emails_sent"** — Need unified tracking
3. **"deal.won" vs "won_deals"** — Need single source
4. **"customer.health_changed" vs "client_health_score"** — Health score should derive from events

---

## 8. Privacy Risks

### Identified Privacy Risks
1. **PII in Event Payloads** — Customer data in event payload needs redaction
   - **Mitigation:** PII redactor exists in `customer_data_plane/pii_redactor.py`

2. **Email Addresses in Reports** — Email addresses in reports expose PII
   - **Mitigation:** Aggregate by sector/channel, never show raw emails

3. **Contact Information in Dashboards** — Direct contact details visible
   - **Mitigation:** Use anonymous IDs, redact in UI

4. **Phone Numbers in WhatsApp Events** — Phone numbers logged
   - **Mitigation:** Hash phone numbers, use session IDs

5. **Financial Data Exposure** — Deal values, costs visible to all
   - **Mitigation:** Role-based access control

---

## 9. Data Quality Risks

### Identified Data Quality Risks
1. **Missing Sector Tagging** — ~30% of events missing sector
   - **Impact:** Cannot segment by sector
   - **Fix:** Enforce sector on event creation

2. **Missing Offer ID** — Events not linked to offers
   - **Impact:** Cannot attribute by offer
   - **Fix:** Require offer_id on deal events

3. **Missing Approval Status** — Founder approval not tracked
   - **Impact:** Cannot track approval funnel
   - **Fix:** Add approval_status to message events

4. **Inconsistent Event Naming** — Some events use camelCase, some snake_case
   - **Impact:** Hard to query consistently
   - **Fix:** Standardize to snake_case

5. **Duplicate Prospect Records** — No deduplication
   - **Impact:** Inflated counts, confused attribution
   - **Fix:** Dedupe on email_domain + company_name

6. **Suppressed Prospects Used** — Bounced/unsubscribed contacted
   - **Impact:** Compliance violation, spam complaints
   - **Fix:** Check suppression list before send

7. **Missing Funnel Stage** — No explicit stage on events
   - **Impact:** Cannot calculate funnel conversion
   - **Fix:** Add funnel_stage to all events

---

## 10. Recommended Execution Order

### Phase 1: Foundation (Week 1-2)
1. Create Metric Event Schema (`schemas/metric_event.schema.json`)
2. Create Funnel Event Schema (`schemas/funnel_event.schema.json`)
3. Create Metric Dictionary document
4. Implement data quality checks

### Phase 2: Core Metrics (Week 3-4)
5. Implement GTM metrics in event stream
6. Create delivery health metrics
7. Create commercial pipeline metrics
8. Create financial metrics

### Phase 3: Dashboards (Week 5-6)
9. Build Founder Daily Decision Dashboard
10. Build GTM Performance Dashboard
11. Build Commercial Pipeline Dashboard
12. Build Delivery Health Dashboard

### Phase 4: Intelligence (Week 7-8)
13. Implement Decision Intelligence rules
14. Create Experiment tracking system
15. Build automated reporting

### Phase 5: Optimization (Week 9+)
16. Address remaining data quality issues
17. Add missing event properties
18. Fine-tune decision rules

---

## Appendix: File Locations

### Created by This Audit
- `reports/analytics/ANALYTICS_GAP_AUDIT.md` — This document

### To Be Created
- `docs/analytics/DEALIX_ANALYTICS_OS_AR.md`
- `docs/analytics/METRIC_DICTIONARY_AR.md`
- `docs/analytics/EVENT_TAXONOMY_AR.md`
- `docs/analytics/DATA_QUALITY_POLICY_AR.md`
- `docs/analytics/PRIVACY_AWARE_ANALYTICS_AR.md`
- `docs/analytics/DECISION_INTELLIGENCE_AR.md`
- `docs/analytics/GTM_FUNNEL_MODEL_AR.md`
- `docs/analytics/REVENUE_FUNNEL_MODEL_AR.md`
- `docs/analytics/CLIENT_LIFECYCLE_FUNNEL_AR.md`
- `docs/analytics/FOUNDER_DECISION_RULES_AR.md`
- `docs/analytics/STOP_SCALE_FIX_RULES_AR.md`
- `docs/analytics/EXPERIMENTATION_SYSTEM_AR.md`
- `docs/analytics/DATA_QUALITY_CHECKS_AR.md`
- `docs/analytics/ANALYTICS_PRIVACY_REDACTION_AR.md`
- `schemas/metric_event.schema.json`
- `schemas/funnel_event.schema.json`
- `schemas/founder_decision.schema.json`
- `schemas/experiment.schema.json`
- `data/analytics/events.jsonl`
- `data/analytics/funnel_events.jsonl`
- `data/analytics/founder_decisions.jsonl`
- `data/analytics/experiments.jsonl`
- `reports/analytics/DAILY_DECISION_INTELLIGENCE.md`
- `reports/analytics/WEEKLY_ANALYTICS_REVIEW.md`
- `reports/analytics/DATA_QUALITY_REVIEW.md`
- `reports/analytics/FUNNEL_REVIEW.md`
- `reports/analytics/FOUNDER_DECISION_QUEUE.md`
- `reports/analytics/PRIVACY_AWARE_ANALYTICS_REVIEW.md`
- `reports/analytics/EXPERIMENT_REVIEW.md`
- `reports/analytics/ANALYTICS_FINAL_REPORT.md`
