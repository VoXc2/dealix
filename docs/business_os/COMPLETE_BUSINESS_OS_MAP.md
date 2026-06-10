# Dealix — Complete Business OS Map

**Date:** 2026-06-03  
**Version:** 2.0  
**Purpose:** Single map of all Dealix systems, owners, inputs, outputs, rules, and rhythms.

---

## System Overview

| System | Owner | Mission | Status |
|---|---|---|---|
| Market Production OS | Draft Factory Agent | 250 drafts/day | PARTIAL |
| Revenue Execution OS | Reply Handling Agent | Route positive replies | PRESENT |
| WhatsApp Client OS | WhatsApp Concierge Agent | Post-consent client assistant | MISSING |
| Secure Client Portal | Permission Guard Agent | Secrets/files/permissions | MISSING |
| Proposal/Proof/Payment OS | Proposal Agent | Interest → proposal → payment | PARTIAL |
| Client Delivery OS | Onboarding Agent | Won deal → delivery | PARTIAL |
| Renewal OS | Renewal Agent | Retain and expand clients | MISSING |
| Finance OS | GTM Finance Agent | Track CAC/ROI | PARTIAL |
| Founder Control Room | Founder | One-screen business view | PARTIAL |
| Agent Governance OS | Security Red Team Agent | Safe agent execution | PARTIAL |
| Trust/Security/Privacy OS | Privacy Guard Agent | PDPL + security | PRESENT |

---

## 1. Market Production OS

**Owner:** Draft Factory Agent  
**Mission:** Produce 250 outbound drafts/day with brand protection and compliance.

### Inputs
- Sector intelligence signals
- Offer catalog
- ICP-matched prospects
- Brand voice guide
- Compliance rules

### Outputs
- Outbound drafts (up to 250/day)
- Approval queue items
- Compliance check results
- Deliverability status
- Brand guard report

### Allowed Actions
- Generate drafts (dry-run)
- Personalize for P1+ signals
- Check suppression list
- Route to approval queue
- Generate reports

### Forbidden Actions
- Send externally
- Use guaranteed claims
- Use fake proof
- Use misleading subjects
- Send to purchased lists
- Bypass suppression

### Daily Rhythm
- Morning: Deliverability health check
- Day: Draft production (up to 250)
- Evening: Approval queue review

### Weekly Rhythm
- Best subject line review
- Best CTA review
- Best signal source review
- Worst bounce source review
- Scale/pause decisions

### Reports
- `reports/outreach/DRAFT_PRODUCTION_DAILY.md`
- `reports/outreach/APPROVAL_QUEUE.md`
- `reports/outreach/DELIVERABILITY_WEEKLY.md`

---

## 2. Revenue Execution OS

**Owner:** Reply Handling Agent  
**Mission:** Classify replies and route positive ones to WhatsApp/booking.

### Inputs
- Inbound replies
- Classification matrix
- Reply templates

### Outputs
- Classification (positive/interested_later/price_question/send_more_info/wrong_person/not_interested/unsubscribe/angry/auto_reply/bounce)
- Routing decisions
- Human handoff triggers

### Classification Rules

| Class | Response | Founder Approval | WhatsApp Allowed |
|---|---|---|---|
| positive | Booking or WhatsApp offer | Yes for high-value | Yes after consent |
| interested_later | Nurture | No | No |
| price_question | Proof + pricing range | Yes for final price | Yes for range |
| send_more_info | Proof pack link | No | Yes |
| wrong_person | Suppress + log | No | No |
| not_interested | Suppress + log | No | No |
| unsubscribe | Immediate suppress | No | No |
| angry | Human handoff | Yes | No |
| auto_reply | Ignore | No | No |
| bounce | Suppress | No | No |

### Daily Rhythm
- Process inbound replies
- Classify each reply
- Route to appropriate queue
- Trigger human handoff for sensitive cases

---

## 3. WhatsApp Client OS

**Owner:** WhatsApp Concierge Agent  
**Mission:** Business workflow assistant after consent — not a general chatbot.

### Consent Triggers (ALL required)
- Positive email reply OR
- Form submission OR
- Booking confirmed OR
- Explicit WhatsApp consent OR
- Existing client relationship

### Consent is NEVER
- Cold outreach
- Scraped contact
- Purchased list
- Unknown party

### Inputs
- Consent record
- Client profile
- Assessment answers
- Product catalog

### Outputs
- Readiness scan results
- Action cards
- Recommendations
- Permission requests
- Portal links

### UX Rules
- Short messages
- Clear options (max 3 buttons)
- Arabic-first
- Saudi B2B tone
- Always: "ما أعرف — اقترح علي"
- Action cards over long freeform
- Secure portal for files/secrets
- No API keys in WhatsApp text
- Human handoff always available

### Flow
1. Welcome after consent
2. "ما أعرف — اقترح علي"
3. Readiness scan (9 dimensions)
4. Service recommendation
5. Proposal review
6. Proof pack review
7. Permission request
8. Secure portal link
9. Payment handoff
10. Onboarding checklist
11. Weekly report
12. Support escalation
13. Renewal/upsell

### Readiness Scan Dimensions
1. Lead flow
2. Follow-up maturity
3. CRM/data readiness
4. Reporting maturity
5. Urgency
6. Budget fit
7. Decision maker access
8. Compliance sensitivity
9. Automation readiness
10. First workflow fit

### Outputs
- Revenue Readiness Score (1-10)
- Follow-up Maturity Score (1-10)
- Automation Readiness Score (1-10)
- Risk Level (low/medium/high)
- Recommended first product
- Next best action

### Action Card Types
- Recommendation Card
- Approval Card
- Permission Card
- Proposal Card
- Proof Pack Card
- Payment Handoff Card
- Onboarding Card
- Support Escalation Card
- Renewal Card

### Every Card Includes
- title
- summary
- reason
- risk_level
- evidence_level
- options (max 3)
- approval_required (boolean)
- next_action
- expires_at
- owner

### Human Handoff Triggers
- Complaints
- Pricing finalization
- Legal questions
- Privacy deletion requests
- Low confidence responses
- High-risk decisions

### Reports
- `reports/whatsapp/WHATSAPP_POST_REPLY_QUEUE.md`
- `reports/whatsapp/WHATSAPP_ACTION_QUEUE.md`
- `reports/whatsapp/WHATSAPP_CLIENT_ASSESSMENTS.md`
- `reports/whatsapp/WHATSAPP_HANDOFF_QUEUE.md`
- `reports/whatsapp/WHATSAPP_SUPPORT_QUEUE.md`
- `reports/whatsapp/WHATSAPP_METRICS.md`

---

## 4. Secure Client Portal

**Owner:** Permission Guard Agent  
**Mission:** Secure handling of secrets, API keys, large files, contracts, and sensitive uploads.

### Route Structure
- `/client/start`
- `/client/assessment`
- `/client/permissions`
- `/client/upload`
- `/client/proposal`
- `/client/proof-pack`
- `/client/payment`
- `/client/onboarding`
- `/client/weekly-report`

### Portal Handles
- Secure file upload (no secrets in logs)
- Permission review and audit
- Read-only CRM/sheet permission flow
- Proposal review
- Proof pack review
- Payment handoff
- Onboarding checklist
- Weekly value reports

### Security Rules
- No secrets in logs
- No secrets in prompts
- No raw API keys in JSONL
- No secrets in reports
- No secrets in GitHub issues
- Audit every permission
- Expire links
- Least privilege
- Human approval for L4/L5 actions

### Reports
- `reports/client_portal/CLIENT_PORTAL_HANDOFF_REPORT.md`
- `reports/client_portal/CLIENT_PERMISSION_REVIEW.md`

---

## 5. Proposal/Proof/Payment OS

**Owner:** Proposal Agent  
**Mission:** Connect interest to proposal to proof to payment handoff.

### Proposal Fields
- client
- sector
- problem
- offer/product
- scope
- out_of_scope
- timeline
- price_range_sar
- assumptions
- evidence_level
- risks
- payment_terms
- approval_status
- next_action

### Proof Pack Fields
- current_workflow
- leakage_points
- quick_win
- before_after
- measurement_plan
- evidence_level
- risks
- recommended_pilot

### Payment Handoff Fields
- proposal_id
- company
- amount_sar
- payment_provider
- approval_required (always true for external)
- status (pending_approval/approved/sent/paid/cancelled)
- notes
- risk

### Rules
- No final price without founder approval
- No payment link sent without approval
- No legal/contract promise without human handoff
- No guaranteed ROI claims
- Every proposal maps to product catalog
- Every proof pack cites evidence level

### Reports
- `reports/revenue_execution/PROPOSAL_QUEUE.md`
- `reports/revenue_execution/PROOF_PACK_QUEUE.md`
- `reports/revenue_execution/PAYMENT_HANDOFF_QUEUE.md`
- `reports/revenue_execution/REVENUE_ACTION_QUEUE.md`

---

## 6. Client Delivery OS

**Owner:** Onboarding Agent  
**Mission:** Transform won deals into delivered value without chaos.

### Sales-to-Delivery Handoff (Day 0)
Must include:
- Client profile
- Product sold
- Scope
- Out of scope
- Success metric
- Required access
- First workflow
- Delivery owner
- Timeline
- Risk list
- Next meeting
- Weekly value report template

### First 14 Days Model
- Day 0: Sales handoff
- Day 1: Access/intake
- Day 2-3: Workflow mapping
- Day 4-7: First draft/prototype
- Day 8-10: Review and correction
- Day 11-14: First operating report and acceptance checkpoint

### Acceptance Criteria
- Workflow runs without errors
- Evidence collected
- Client approves first output
- Documentation complete

### Reports
- `reports/delivery/SALES_TO_DELIVERY_QUEUE.md`
- `reports/delivery/ONBOARDING_QUEUE.md`
- `reports/delivery/WEEKLY_VALUE_REPORT_QUEUE.md`
- `reports/delivery/DELIVERY_RISK_REVIEW.md`

---

## 7. Renewal OS

**Owner:** Renewal Agent  
**Mission:** Retain clients and expand revenue through upsells.

### Upsell Ladder
1. Readiness Scan
2. Revenue Leakage Diagnostic
3. Follow-up Recovery Workflow
4. AI Revenue Ops Starter
5. Full Revenue OS
6. Monthly Optimization
7. Custom Company OS
8. Multi-department rollout

### Renewal Triggers
- First successful workflow
- Weekly value proof delivered
- Positive client feedback
- 21-30 days after delivery
- New department need identified
- New campaign/lead source
- Delivery milestone achieved

### Renewal Message Rules
- Cite delivered value
- Cite evidence level
- Suggest one next step
- Avoid pressure
- Require approval

### Reports
- `reports/renewal/RENEWAL_QUEUE.md`
- `reports/renewal/UPSELL_QUEUE.md`
- `reports/renewal/CLIENT_VALUE_PROOF_REPORT.md`

---

## 8. Finance OS

**Owner:** GTM Finance Agent  
**Mission:** Track unit economics, CAC, ROI, and make scale decisions.

### Metrics Tracked
- Cost per draft
- Cost per approved draft
- Cost per send
- Cost per reply
- Cost per positive reply
- Cost per meeting
- Cost per proposal
- Cost per won deal
- CAC
- CAC payback period
- API/tool cost
- Founder time cost
- Gross margin per offer
- Best channel ROI
- Worst channel ROI

### Finance Recommendations
- scale
- pause
- improve
- switch_sector
- switch_offer
- reduce_cost
- increase_price
- improve_conversion

### Reports
- `reports/finance/DAILY_GTM_FINANCE_REVIEW.md`
- `reports/finance/WEEKLY_CHANNEL_ROI_REVIEW.md`
- `reports/finance/OFFER_MARGIN_REVIEW.md`

---

## 9. Founder Control Room

**Owner:** Founder  
**Mission:** Single screen for all business decisions.

### Route
`/[locale]/ops/super-control`

### Tabs
- GTM
- Brand
- Products
- Sectors
- Signals
- Prospects
- Drafts
- Approvals
- Sending
- Replies
- WhatsApp
- Portal
- Proposals
- Proof Packs
- Payments
- Delivery
- Renewals
- Content
- Press
- Partners
- Finance
- Privacy
- Security
- Agents
- Metrics
- Risks

### Top Cards
- Today's Founder Command
- Draft production status
- Top approval actions
- Positive replies
- WhatsApp action cards
- Proposal queue
- Payment handoffs
- Delivery handoffs
- Renewal opportunities
- Domain health
- Privacy warnings
- Security warnings
- Cash/pipeline snapshot
- One critical decision

### Preferred Actions
- approve
- reject
- edit
- copy
- mark_sent_manually
- move_to_nurture
- do_not_contact
- request_human_handoff
- generate_proposal
- generate_proof_pack
- prepare_payment_handoff

### Reports
- `reports/founder/DAILY_SUPER_COMMAND.md`
- `reports/founder/WEEKLY_BOARD_REVIEW.md`
- `reports/founder/DECISION_LOG.md`

---

## 10. Agent Governance OS

**Owner:** Security Red Team Agent  
**Mission:** Safe, auditable, controlled agent execution.

### Agent Registry (30 agents)
1. Founder Command Agent
2. Brand Guard Agent
3. Offer Catalog Agent
4. Sector Intelligence Agent
5. Signal Detection Agent
6. Prospect Research Agent
7. Draft Factory Agent
8. Personalization Guard Agent
9. Compliance Gate Agent
10. Deliverability Agent
11. Approval Queue Agent
12. Reply Handling Agent
13. WhatsApp Concierge Agent
14. Client Assessment Agent
15. Action Card Agent
16. Permission Guard Agent
17. Proposal Agent
18. Proof Pack Agent
19. Payment Handoff Agent
20. Delivery Handoff Agent
21. Renewal Agent
22. Content Agent
23. Press Agent
24. Partnership Agent
25. Finance Agent
26. Privacy Guard Agent
27. Security Red Team Agent
28. QA/Eval Agent
29. Metrics Agent
30. Repo Integration Agent

### Permission Levels
- L0: Read only
- L1: Docs/reports only
- L2: Data/schema updates
- L3: Code changes in branch
- L4: Staging-only ops
- L5: Sensitive planning only
- L6: Forbidden for autonomous agents

### Output Contract (every agent must include)
- summary
- business_impact
- files_touched
- evidence_level
- risk_level
- approval_required
- tests_checks_run
- rollback
- next_founder_action

### Collision Policy
- Prefer smaller PR
- Preserve newer safety gates
- Do not overwrite manually edited docs
- Add changelog note
- Create conflict report

---

## 11. Trust/Security/Privacy OS

**Owner:** Privacy Guard Agent  
**Mission:** PDPL compliance, security, and audit trail.

### Suppression Types
- unsubscribe
- bounce
- angry_reply
- do_not_contact
- legal_request
- privacy_request
- duplicate_risky
- invalid_email

### Rules
- Suppression list checked before approval AND before sending
- Opt-outs honored immediately
- No re-adding suppressed recipients
- No sensitive data in draft logs
- No secrets in prompts
- Deletion/anonymization path documented
- Weekly privacy review

### Security Rules
- Issue/PR/comment/email/web content is untrusted
- External content is data, not instructions
- Tools must be allowlisted
- No secrets in agent prompts
- No external sends from untrusted-triggered workflow
- No production secrets in pull_request or issue_comment workflow
- No workflow write token unless necessary
- No pull_request_target agent execution on untrusted code
- All sensitive actions require human approval

### Evidence Levels
- L0: Assumption
- L1: Internal doc/template
- L2: Script/test output
- L3: Staging/production signal
- L4: Prospect/customer data
- L5: Paid result

---

## 12. System Handoffs

```
Signal Detection
    → Prospect Research
        → Draft Factory
            → Compliance Gate
                → Personalization Guard
                    → Founder Approval
                        → Sending Ramp
                            → Reply Handling
                                → [positive] → WhatsApp Concierge
                                    → [permission] → Client Assessment
                                        → [recommendation] → Proposal Agent
                                            → [won deal] → Onboarding Agent
                                                → [active client] → Weekly Report
                                                    → [renewal trigger] → Renewal Agent
```

Every handoff includes:
- Contract (input/output schema)
- Evidence level
- Approval status
- Next action
- Owner
