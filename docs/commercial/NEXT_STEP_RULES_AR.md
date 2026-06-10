# Next Step Rules — قواعد الخطوة التالية
**Dealix — Agent #3**

> **الغرض:** في كل نقطة في الـ pipeline، ما هي الخطوة التالية المسموحة، والممنوعة، والموصى بها.

---

## 1. The Rule

**كل مرحلة في الـ pipeline يجب أن تنتهي بـ next step محدد، قابل للقياس، له due date.**

**لا lead بدون next step. لا next step بدون due date.**

---

## 2. Next Step by Stage

### 2.1 signal_detected
- **Default:** research
- **Within:** 24 hours
- **Action:** research company, check ICP
- **Owner:** ICPScoringAgent + Sales Lead

### 2.2 researched
- **Default:** qualify
- **Within:** 3 days
- **Action:** apply ICP scoring, decide qualified_A/B/nurture/lost
- **Owner:** ICPScoringAgent

### 2.3 qualified
- **Default:** draft outreach
- **Within:** 7 days
- **Action:** OutreachDraftAgent creates personalized draft
- **Owner:** OutreachDraftAgent

### 2.4 drafted
- **Default:** founder approval
- **Within:** 1-2 days
- **Action:** founder reviews and approves/rejects
- **Owner:** Founder

### 2.5 approved_for_outreach
- **Default:** send
- **Within:** 1-2 days
- **Action:** founder manually sends (warm)
- **Owner:** Founder

### 2.6 contacted
- **Default:** wait for reply
- **Within:** 7 days
- **Action:** if no reply → follow-up #1, then nurture
- **Owner:** Sales Lead

### 2.7 replied
- **Default:** schedule discovery
- **Within:** 3 days
- **Action:** propose meeting time
- **Owner:** Sales Lead

### 2.8 discovery_scheduled
- **Default:** run call
- **Within:** 14 days (calendar)
- **Action:** attend, take notes
- **Owner:** Founder

### 2.9 discovery_completed
- **Default:** decide + next action
- **Within:** 3 days
- **Action:** proposal_needed / nurture / lost
- **Owner:** Founder

### 2.10 proposal_needed
- **Default:** draft proposal
- **Within:** 3 days
- **Action:** Proposal Agent drafts
- **Owner:** Proposal Agent

### 2.11 proposal_sent
- **Default:** wait for response
- **Within:** 14 days
- **Action:** follow-up if no response, then re-evaluate
- **Owner:** Founder

### 2.12 negotiation
- **Default:** resolve + close
- **Within:** 14 days
- **Action:** 1-2 rounds of negotiation, then accept/lost
- **Owner:** Founder

### 2.13 payment_handoff
- **Default:** receive payment
- **Within:** 7 days (default terms)
- **Action:** follow up on payment
- **Owner:** Billing Draft Agent

### 2.14 won
- **Default:** delivery handoff
- **Within:** 3 days
- **Action:** handoff to delivery OS
- **Owner:** Delivery Lead

### 2.15 delivery_handoff
- **Default:** kickoff
- **Within:** 3-7 days
- **Action:** kickoff meeting, first value
- **Owner:** Delivery Lead

### 2.16 active_delivery
- **Default:** weekly report + check-in
- **Within:** 7-day cadence
- **Action:** CS Agent
- **Owner:** CS Agent

### 2.17 renewal_candidate
- **Default:** renewal discussion
- **Within:** 30 days before end
- **Action:** renewal draft
- **Owner:** Renewal Agent

### 2.18 renewed
- **Default:** back to active
- **Within:** same day
- **Action:** new term
- **Owner:** Founder

### 2.19 lost
- **Default:** archive + learn
- **Within:** 7 days
- **Action:** log reason, update ICP if pattern
- **Owner:** Sales Lead

### 2.20 nurture
- **Default:** quarterly check-in
- **Within:** 90 days
- **Action:** content / event / new offer
- **Owner:** Sales Lead

### 2.21 do_not_contact
- **Default:** terminal
- **Within:** —
- **Action:** founder override only
- **Owner:** Founder

---

## 3. Next Step Quality Standards

### 3.1 Good Next Step
- ✅ Specific (not "follow up")
- ✅ Actionable (who does what)
- ✅ Time-bound (due date)
- ✅ Measurable (what success looks like)

### 3.2 Bad Next Step
- ❌ "Follow up later" (vague)
- ❌ "Send info" (no spec)
- ❌ "Wait" (no action)
- ❌ "Eventually" (no due)

---

## 4. Next Step Templates

### 4.1 Outreach
```
"Next: Send LinkedIn message to [Name] referencing [specific event]. 
Due: 2026-06-05. Owner: Founder."
```

### 4.2 Follow-up
```
"Next: Follow-up email if no reply. 
Due: 2026-06-10. Owner: Sales Lead."
```

### 4.3 Discovery
```
"Next: Discovery call (60 min, Zoom). 
Due: 2026-06-12. Owner: Founder. Pre-call: read note + prepare 3 pain hypotheses."
```

### 4.4 Proposal
```
"Next: Send proposal (4,999 SAR, 7-day diagnostic). 
Due: 2026-06-15. Owner: Founder. Approval: L1."
```

### 4.5 Negotiation
```
"Next: Send revised proposal (-10%, scope reduced). 
Due: 2026-06-13. Owner: Founder. Approval: L2."
```

### 4.6 Close
```
"Next: Receive payment + kickoff. 
Due: 2026-06-17. Owner: Founder + Delivery Lead."
```

---

## 5. Stuck Lead Recovery

### 5.1 Stale > 7 days
- ⚠️ Add follow-up action
- ⚠️ Move to next stage if appropriate

### 5.2 Stale > 14 days
- ⚠️ founder attention
- ⚠️ Re-evaluate qualification
- ⚠️ Move to nurture if appropriate

### 5.3 Stale > 30 days
- ⚠️ Close (lost or nurture)
- ⚠️ Update ICP if pattern
- ⚠️ Document reason

---

## 6. Next Step Hygiene

### 6.1 Daily
- Update next step on each touch
- Set due dates
- Move stuck leads

### 6.2 Weekly
- Review all open next steps
- Re-allocate resources
- Pipeline cleanup

### 6.3 Monthly
- Pattern analysis
- Process improvement

---

## 7. The "What Now" Question

في أي وقت تسأل "What now?" — أجب بـ:
1. **Stage** — وين الـ lead؟
2. **Next step** — وش الخطوة التالية؟
3. **Owner** — من المسؤول؟
4. **Due** — متى؟
5. **Outcome** — ما المخرج المتوقع؟

---

## 8. Companion Files

- Process: `SALES_PROCESS_AR.md`
- Pipeline: `PIPELINE_STAGES_AR.md`
- Qualification: `QUALIFICATION_RULES_AR.md`
- Discovery: `DISCOVERY_PROCESS_AR.md`
- Data: `data/commercial/opportunities.jsonl`
- Schema: `schemas/opportunity.schema.json`

---

**Next step = engine الـ pipeline. بدون next step = stuck. founder يضبط، النظام يذكّر، الـ team ينفّذ.**
