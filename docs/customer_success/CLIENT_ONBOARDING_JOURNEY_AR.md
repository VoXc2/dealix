# Client Onboarding Journey
# رحلة تأهيل العميل

> **النسخة:** 1.0  
> **التاريخ:** 2026-06-03  
> **Owner:** Customer Success Lead  
> **الغرض:** تأهيل كل عميل فاز بشكل متسق من الصفقة المغلقة إلى أول قيمة مُسلَّمة

---

## 1. Journey Overview

### 1.1 مراحل التأهيل

```
Stage 1: won          → Contract signed, payment incoming
Stage 2: payment_confirmed → Payment cleared
Stage 3: delivery_handoff_created → Handoff to CS
Stage 4: kickoff_scheduled → Kickoff meeting set
Stage 5: access_requested → Client access requested
Stage 6: access_received → Access credentials received
Stage 7: first_workflow_mapped → Workflow requirements defined
Stage 8: first_draft_delivered → First output delivered
Stage 9: client_feedback_received → Feedback collected
Stage 10: first_weekly_report_sent → Value report sent
Stage 11: success_checkpoint → Day 30 check
Stage 12: renewal_path_identified → Next steps defined
```

### 1.2 SLA لكل مرحلة

| المرحلة | SLA | Owner |
|---------|-----|-------|
| won → payment_confirmed | 1 يوم | Sales |
| payment_confirmed → delivery_handoff | 1 يوم | CS Lead |
| delivery_handoff → kickoff_scheduled | 2 أيام | CS Lead |
| kickoff_scheduled → kickoff_done | 3 أيام | CS Lead |
| kickoff_done → access_received | 5 أيام | Client + CS |
| access_received → first_workflow | 7 أيام | Delivery |
| first_workflow → first_feedback | 3 أيام | Client |
| feedback → first_report | 2 أيام | CS Lead |
| first_report → checkpoint | 21 يوم | CS Lead |

---

## 2. Client Profile Template

### 2.1 Required Fields

```json
{
  "client_id": "string (uuid)",
  "company_name": "string",
  "contact_name": "string",
  "contact_title": "string",
  "contact_email": "string",
  "contact_phone": "string",
  "contact_whatsapp": "string",
  "key_stakeholders": [
    {
      "name": "string",
      "title": "string",
      "role": "decision_maker | influencer | user | champion",
      "email": "string"
    }
  ],
  "product_sold": "string (offer_id)",
  "package": "string (tier)",
  "contract_value": "number (SAR)",
  "payment_status": "paid | pending | partial",
  "success_metric": "string",
  "success_target": "string (measurable)",
  "timeline": {
    "start_date": "date",
    "end_date": "date",
    "delivery_weeks": "number"
  },
  "required_access": {
    "crm": "boolean",
    "email": "boolean",
    "whatsapp": "boolean",
    "data_files": "boolean",
    "other": "string"
  },
  "communication_channel": "email | whatsapp | both",
  "language_preference": "ar | en | both",
  "owner": "string (CS Lead name)",
  "risks": [
    {
      "risk": "string",
      "probability": "high | medium | low",
      "impact": "high | medium | low"
    }
  ]
}
```

---

## 3. Stage-by-Stage Process

### 3.1 Stage 1: won

**Trigger:** Contract signed by both parties

**Actions:**
1. Mark opportunity as `won` in CRM
2. Assign CS Lead to account
3. Create client folder: `clients/<client_id>/`
4. Create client profile document
5. Send internal notification to CS team
6. Schedule handoff meeting with delivery team

**Output:** `client_profile.json` created

**Owner:** Sales → CS Lead

---

### 3.2 Stage 2: payment_confirmed

**Trigger:** Payment cleared (Moyasar confirmation)

**Actions:**
1. Update payment status in CRM
2. Create engagement ID: `<YYYYMMDD>-<CLIENT_HANDLE>`
3. Generate welcome email
4. Prepare kickoff invitation
5. Notify delivery team of payment

**Output:** Welcome email drafted (pending founder approval)

**Owner:** CS Lead

---

### 3.3 Stage 3: delivery_handoff_created

**Trigger:** Handoff meeting completed

**Actions:**
1. Create delivery handoff document
2. Share client profile with delivery team
3. Confirm delivery timeline
4. Assign delivery owner
5. Schedule kickoff with client
6. Create success plan skeleton

**Output:** `handoff_document.json`, `success_plan_draft.json`

**Owner:** CS Lead + Delivery Lead

---

### 3.4 Stage 4: kickoff_scheduled

**Trigger:** Kickoff meeting confirmed

**Actions:**
1. Send kickoff invitation
2. Prepare kickoff agenda
3. Confirm required attendees
4. Prepare kickoff deck
5. Share pre-read materials with client

**Output:** Kickoff invitation sent

**Owner:** CS Lead

---

### 3.5 Kickoff Meeting Agenda (60 min)

| الوقت | الموضوع | الهدف |
|-------|--------|-------|
| 0-10 | Introduction + Overview | Alignment |
| 10-25 | Client goals deep-dive | Understanding |
| 25-40 | Workflow mapping | Clarity |
| 40-50 | Success metrics agreement | Commitment |
| 50-60 | Next steps + Q&A | Action |

**Kickoff Outputs:**
- Confirmed success metrics
- Mapped first workflow
- Defined approval process
- Agreed communication cadence

---

### 3.6 Stage 5: access_requested

**Trigger:** Post-kickoff

**Actions:**
1. Send access request email/WhatsApp
2. List all required access clearly
3. Set deadline for access
4. Explain why access is needed
5. Confirm data sensitivity handling

**Access Request Template:**
```
Subject: [ACTION REQUIRED] Access needed for <engagement_id>

Dear <contact_name>,

To begin work on your engagement, we need the following access:

1. <Access Type 1>
   - Why: <reason>
   - Deadline: <date>

2. <Access Type 2>
   - Why: <reason>
   - Deadline: <date>

All data will be handled according to our data protection policy.
No data leaves your environment without your explicit approval.

Please reply to confirm when access is ready.
```

**Owner:** CS Lead

---

### 3.7 Stage 6: access_received

**Trigger:** All required access provided

**Actions:**
1. Verify all access is working
2. Document access credentials (secure)
3. Confirm data quality
4. Notify delivery team
5. Start delivery phase

**Output:** `access_log.json`, delivery can begin

**Owner:** CS Lead + Delivery Lead

---

### 3.8 Stage 7: first_workflow_mapped

**Trigger:** Delivery team confirms requirements

**Actions:**
1. Document workflow specifications
2. Confirm with client
3. Set delivery timeline
4. Identify blockers
5. Update success plan

**Output:** `workflow_spec.json`, `delivery_timeline.json`

**Owner:** Delivery Lead

---

### 3.9 Stage 8: first_draft_delivered

**Trigger:** First workflow output ready

**Actions:**
1. Internal QA review
2. Prepare for client delivery
3. Get founder approval to send
4. Deliver to client
5. Request feedback

**Output:** Draft delivered to client

**Owner:** Delivery Lead + CS Lead

---

### 3.10 Stage 9: client_feedback_received

**Trigger:** Client provides feedback

**Actions:**
1. Document all feedback
2. Prioritize changes
3. Plan revisions
4. Communicate timeline
5. Update success plan

**Output:** `feedback_log.json`

**Owner:** CS Lead + Delivery Lead

---

### 3.11 Stage 10: first_weekly_report_sent

**Trigger:** First delivery complete + feedback resolved

**Actions:**
1. Compile weekly value report
2. Include delivery summary
3. Include value created
4. Get founder approval
5. Send to client
6. File report

**Output:** `weekly_report_<week1>.json`

**Owner:** CS Lead

---

### 3.12 Stage 11: success_checkpoint (Day 30)

**Trigger:** 30 days since delivery start

**Actions:**
1. Compile 30-day summary
2. Calculate health score
3. Assess success metrics
4. Identify risks
5. Propose next steps
6. Schedule checkpoint meeting

**Checkpoint Agenda:**
1. What was delivered
2. What value was created
3. What challenges occurred
4. What metrics improved
5. Next 30-day plan
6. Renewal/expansion discussion

**Output:** `30_day_checkpoint.json`, `health_score_<day30>.json`

**Owner:** CS Lead

---

### 3.13 Stage 12: renewal_path_identified

**Trigger:** Post checkpoint

**Actions:**
1. Assess renewal readiness
2. If ready: initiate renewal conversation
3. If not ready: create improvement plan
4. If expansion ready: initiate expansion proposal
5. Document next steps

**Output:** `renewal_proposal.json` OR `expansion_proposal.json` OR `improvement_plan.json`

**Owner:** CS Lead + Founder

---

## 4. Onboarding Checklist

### 4.1 CS Lead Checklist

```
□ Client profile created
□ Handoff document created
□ Kickoff scheduled
□ Kickoff meeting completed
□ Access requested
□ Access received
□ First workflow mapped
□ First draft delivered
□ Feedback received
□ First weekly report sent
□ Day 30 checkpoint scheduled
□ Health score calculated
□ Success plan updated
□ Renewal path identified
```

### 4.2 Client Checklist

```
□ Welcome email received
□ Kickoff meeting attended
□ Goals and metrics agreed
□ Access credentials provided
□ First workflow requirements confirmed
□ Feedback provided on drafts
□ Checkpoint meeting attended
```

---

## 5. Common Blockers

| Blocker | Solution | Owner |
|---------|----------|-------|
| No response from client | WhatsApp follow-up after 24h | CS Lead |
| Access delayed | Escalate to champion | CS Lead |
| Unclear requirements | Re-schedule requirements call | CS Lead |
| Stakeholder disagreement | Identify decision maker | CS Lead + Founder |
| Scope creep | Reference SOW, get approval | CS Lead |
| Payment issues | Pause delivery | CS Lead |

---

## 6. Templates

### 6.1 Welcome Email Template

```
Subject: Welcome to Dealix — Let's Get Started

Dear <contact_name>,

Welcome to Dealix! We're excited to work with <company_name>.

Your engagement ID: <engagement_id>
CS Lead: <cs_name>
Project timeline: <start_date> to <end_date>

Next step: Kickoff meeting
Date: <kickoff_date>
Time: <kickoff_time>
Link: <meeting_link>

Before our kickoff:
- Prepare a brief on your current <workflow_type> challenges
- Identify who will be your main point of contact
- Think about your top 3 goals for this engagement

See you soon!

<cs_name>
Customer Success Lead | Dealix
```

### 6.2 Access Request Template

```
Subject: Access Required — <engagement_id>

Hello <contact_name>,

To begin work on your engagement, we need the following:

1. <Access Type>
   Details: <specifics>
   Deadline: <date>

2. <Access Type>
   Details: <specifics>
   Deadline: <date>

Please let us know if you have any questions about these requirements.

Thank you,
<cs_name>
```

### 6.3 Kickoff Confirmation Template

```
Subject: Confirmed — Kickoff Meeting <date>

Hello <contact_name>,

Your kickoff meeting is confirmed:

Date: <date>
Time: <time>
Duration: 60 minutes
Link: <link>

Agenda:
1. Introduction and goals (10 min)
2. Current state review (15 min)
3. Workflow mapping (15 min)
4. Success metrics (10 min)
5. Next steps (10 min)

Please confirm your attendance.

Best,
<cs_name>
```

---

## 7. Governance

### 7.1 Approval Required

| Action | Approver |
|--------|----------|
| Send welcome email | Founder |
| Proceed without complete access | Founder |
| Change delivery timeline | Founder |
| Send first report to client | Founder |

### 7.2 Escalation Triggers

- No response for 48h → CS Lead outreach
- No response for 5 days → Founder outreach
- Access not received in 7 days → Escalate to champion
- Client requests scope change → Founder approval

---

**Last Updated:** 2026-06-03  
**Next Review:** 2026-07-03
