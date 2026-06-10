# Pipeline Stages — مراحل الـ Pipeline
**Dealix — Agent #3**

> **الغرض:** كل stage في pipeline، تعريفها، شروط الدخول، شروط الخروج، owner، next step، وقت SLA.

---

## 1. The 21 Pipeline Stages (توسعة لـ stage_transitions.yaml)

| # | Stage | الوصف | Owner |
|---|-------|--------|-------|
| 1 | signal_detected | lead جديد وصل | ICPScoringAgent |
| 2 | researched | بحث أولي (manual) | Sales Lead |
| 3 | qualified | ICP fit, score 10+ | ICPScoringAgent |
| 4 | drafted | outreach draft created | OutreachDraftAgent |
| 5 | approved_for_outreach | founder approved send | Founder |
| 6 | contacted | first outreach sent | Founder (manual) |
| 7 | replied | client responded | Sales Lead |
| 8 | discovery_scheduled | meeting booked | Sales Lead |
| 9 | discovery_completed | call done, note added | Discovery Agent |
| 10 | proposal_needed | trigger proposal | Founder |
| 11 | proposal_sent | proposal delivered | Founder |
| 12 | negotiation | client wants changes | Founder |
| 13 | payment_handoff | invoice + payment | Billing Draft Agent |
| 14 | won | closed-won | Founder |
| 15 | delivery_handoff | to delivery OS | Delivery Lead |
| 16 | active_delivery | implementation ongoing | Delivery Lead |
| 17 | renewal_candidate | 30 days before end | CS Agent |
| 18 | renewed | client continues | Founder |
| 19 | lost | closed-lost | Founder |
| 20 | nurture | long-term follow-up | Sales Lead |
| 21 | do_not_contact | blacklist | Founder |

**Source:** امتداد لـ `dealix/config/stage_transitions.yaml` (16 stages → 21)

---

## 2. Stage Definitions

### 2.1 signal_detected
- Lead form, demo request, partner referral
- **Entry:** any new lead
- **Exit:** to researched OR nurture OR lost

### 2.2 researched
- Manual research on company
- **Entry:** from signal_detected
- **Exit:** to qualified OR nurture OR lost

### 2.3 qualified
- ICP score 10+ (A or B)
- **Entry:** from researched
- **Exit:** to drafted OR nurture OR lost

### 2.4 drafted
- Outreach draft created
- **Entry:** from qualified
- **Exit:** to approved_for_outreach OR lost

### 2.5 approved_for_outreach
- Founder approved draft for sending
- **Entry:** from drafted
- **Exit:** to contacted OR revised

### 2.6 contacted
- First outreach sent
- **Entry:** from approved_for_outreach
- **Exit:** to replied OR nurture (no reply) OR lost

### 2.7 replied
- Client responded (positive or neutral)
- **Entry:** from contacted
- **Exit:** to discovery_scheduled OR nurture OR lost

### 2.8 discovery_scheduled
- Meeting on calendar
- **Entry:** from replied
- **Exit:** to discovery_completed OR lost (no show)

### 2.9 discovery_completed
- Call done, note logged
- **Entry:** from discovery_scheduled
- **Exit:** to proposal_needed OR nurture OR lost

### 2.10 proposal_needed
- Decision: send proposal
- **Entry:** from discovery_completed
- **Exit:** to proposal_sent (after draft + approval)

### 2.11 proposal_sent
- Proposal delivered to client
- **Entry:** from proposal_needed
- **Exit:** to negotiation OR won OR lost OR nurture

### 2.12 negotiation
- Client wants changes
- **Entry:** from proposal_sent
- **Exit:** to proposal_sent (revised) OR won OR lost

### 2.13 payment_handoff
- Invoice issued, awaiting payment
- **Entry:** from negotiation (agreed) OR won (immediate)
- **Exit:** to won (paid) OR lost (unpaid)

### 2.14 won
- Closed-won, paid
- **Entry:** from payment_handoff
- **Exit:** to delivery_handoff

### 2.15 delivery_handoff
- Handed to delivery team
- **Entry:** from won
- **Exit:** to active_delivery

### 2.16 active_delivery
- Implementation ongoing
- **Entry:** from delivery_handoff
- **Exit:** to renewal_candidate (near end) OR lost (terminated)

### 2.17 renewal_candidate
- 30 days before contract end
- **Entry:** from active_delivery
- **Exit:** to renewed OR lost (declined)

### 2.18 renewed
- Client continues (re-signed or auto)
- **Entry:** from renewal_candidate
- **Exit:** to active_delivery (new term) OR won (new deal)

### 2.19 lost
- Closed-lost
- **Entry:** from any stage
- **Exit:** terminal (except reactivation by founder)

### 2.20 nurture
- Long-term follow-up
- **Entry:** from any non-won stage
- **Exit:** to qualified (re-engaged) OR lost

### 2.21 do_not_contact
- Blacklist (spam, abuse, etc.)
- **Entry:** from any stage
- **Exit:** terminal (founder only override)

---

## 3. Stage Transitions (State Machine)

```
signal_detected → researched
researched → qualified
qualified → drafted
drafted → approved_for_outreach
approved_for_outreach → contacted
contacted → replied | nurture | lost
replied → discovery_scheduled | nurture | lost
discovery_scheduled → discovery_completed | lost
discovery_completed → proposal_needed | nurture | lost
proposal_needed → proposal_sent
proposal_sent → negotiation | won | lost | nurture
negotiation → proposal_sent | won | lost
payment_handoff → won | lost
won → delivery_handoff
delivery_handoff → active_delivery
active_delivery → renewal_candidate | lost
renewal_candidate → renewed | lost
nurture → qualified | lost
(any) → do_not_contact (founder only)
```

**Note:** مكمل لـ `stage_transitions.yaml` (16 stages → 21)

---

## 4. Time in Stage (SLA)

| Stage | Max Days | Reason |
|-------|----------|--------|
| signal_detected | 1 | quick response |
| researched | 3 | manual research |
| qualified → drafted | 7 | outreach prep |
| approved_for_outreach | 1 | founder queue |
| contacted | 7 | wait for reply |
| replied | 3 | schedule quickly |
| discovery_scheduled | 14 | calendar time |
| discovery_completed | 3 | write note |
| proposal_needed | 3 | founder decision |
| proposal_sent | 14 | client decision |
| negotiation | 14 | back and forth |
| payment_handoff | 7 | payment received |
| won → delivery_handoff | 3 | kickoff |
| active_delivery | per package | — |
| renewal_candidate | 30 | before end |

---

## 5. Conversion Targets

| Transition | Target % |
|-----------|----------|
| Signal → Qualified | 30%+ |
| Qualified → Drafted | 80%+ |
| Drafted → Contacted | 90%+ |
| Contacted → Replied | 20%+ |
| Replied → Discovery | 60%+ |
| Discovery → Proposal | 70%+ |
| Proposal → Won | 30%+ |
| Won → Delivery | 95%+ |
| Delivery → Renewal | 70%+ |

**Tune from actual data over time.**

---

## 6. Pipeline Views

### 6.1 By Stage (count)
```
[signal] 50 → [researched] 30 → [qualified] 20 → ...
```

### 6.2 By Value (SAR)
```
qualified 200,000 SAR
proposal_sent 80,000 SAR
won 35,000 SAR
```

### 6.3 By Owner
```
Founder: 5 active
Sales Lead: 3 active
Discovery: 2 active
```

### 6.4 By ICP
```
Agency: 10
Clinic: 5
Education: 3
```

---

## 7. Pipeline Hygiene

### 7.1 Daily
- Move stuck opportunities
- Log today's activities
- Update next step

### 7.2 Weekly
- Stale > 14 days → action
- Stale > 30 days → close
- Lost analysis

### 7.3 Monthly
- Conversion by stage
- Cycle time analysis
- ICP performance

---

## 8. Pipeline Reports

- `reports/commercial/PIPELINE_REVIEW.md` (PHASE 6)
- `data/commercial/opportunities.jsonl` (PHASE 6)
- CRM dashboards

---

## 9. Companion Files

- Process: `SALES_PROCESS_AR.md`
- Qualification: `QUALIFICATION_RULES_AR.md`
- Discovery: `DISCOVERY_PROCESS_AR.md`
- Next Step: `NEXT_STEP_RULES_AR.md`
- Data: `data/commercial/opportunities.jsonl`
- Schema: `schemas/opportunity.schema.json`
- Existing: `dealix/config/stage_transitions.yaml`

---

**Pipeline = حقيقة واحدة. كل lead له stage، كل stage له شرط، كل انتقال له approval. founder يراقب، النظام ينبه.**
