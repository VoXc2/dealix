# Sales Process — عملية المبيعات
**Dealix — Agent #3**

> **الغرض:** كيف نأخذ lead من أول contact إلى closed-won + delivery handoff. كل خطوة لها owner، output، وapproval.

---

## 1. The 7-Step Sales Process

```
[1. Signal Detected] → [2. Qualified] → [3. Discovery] → [4. Proposal]
                                                          ↓
[7. Closed-Won] ← [6. Negotiation] ← [5. Proposal Sent]
   ↓
[Delivery Handoff] → [Active Delivery] → [Renewal]
```

---

## 2. Step 1: Signal Detected

### 2.1 What It Is
- Lead form fill
- Inbound demo request
- Warm email reply
- Partner referral
- Event contact
- Content engagement

### 2.2 Owner
- ICPScoringAgent (auto)
- LeadCaptureAgent (auto)

### 2.3 Output
- Lead record in CRM
- ICP score (0-20+)
- Initial segment assignment
- First next action

### 2.4 Approval
- None (internal)
- GDPR/PDPL consent capture required

### 2.5 Time SLA
- < 1 hour (warm)
- < 24 hours (cold)

### 2.6 Tools
- `POST /api/v1/leads`
- `icp_primary.yaml` (existing)
- `data/commercial/icp_segments.yaml` (PHASE 2)

---

## 3. Step 2: Qualified

### 3.1 What It Is
- ICP score ≥ 15 → qualified_A
- ICP score 10-14 → qualified_B
- ICP score 6-9 → nurture
- ICP score < 6 → disqualify

### 3.2 Owner
- ICPScoringAgent
- Sales Lead (manual review)

### 3.3 Output
- Status: qualified_A/B/nurture/lost
- Pain hypothesis
- Initial offer match
- Next step proposal

### 3.4 Approval
- L1 (founder) for A → discovery booking
- L1 (founder) for B → if special
- L2 (founder + reason) for nurture with budget

### 3.5 Time SLA
- < 24 hours after signal

### 3.6 Tools
- `stage_transitions.yaml` (existing)
- `lead_scoring.yaml` (existing)
- `QUALIFICATION_RULES_AR.md` (PHASE 6)

---

## 4. Step 3: Discovery

### 4.1 What It Is
- 30-60 min call
- Pain discovery
- ICP validation
- Budget/timing/authority
- Initial offer pitch

### 4.2 Owner
- Discovery Agent (drafts questions)
- Founder (calls + summary)
- Sales Lead (alternative)

### 4.3 Output
- Discovery note (structured)
- Pain category confirmed
- Decision maker identified
- Budget range
- Timeline
- Next step (proposal? nurture? disqualify?)

### 4.4 Approval
- Discovery schedule: L1 (founder)
- Discovery note: internal (no approval needed)
- Next step (proposal): L1 (founder)

### 4.5 Time SLA
- Schedule within 7 days
- Complete within 14 days

### 4.6 Tools
- `os/14_DISCOVERY_CALL_TEMPLATE.md` (existing)
- `data/commercial/discovery_notes.jsonl` (PHASE 6)
- `schemas/discovery_note.schema.json` (PHASE 6)
- `DISCOVERY_PROCESS_AR.md` (PHASE 6)

---

## 5. Step 4: Proposal

### 5.1 What It Is
- Internal: Proposal Agent drafts
- Founder review + approval
- Sent to client
- Client reviews (7-14 days)

### 5.2 Owner
- Proposal Agent (draft)
- Founder (review + approve)
- Sales Lead (alternative)

### 5.3 Output
- Proposal document (AR)
- Quote (with approval level)
- Scope, deliverables, timeline, price, terms

### 5.4 Approval
- L1-L5 per `QUOTE_APPROVAL_POLICY_AR.md`
- All proposals require founder approval

### 5.5 Time SLA
- Draft within 3 days of discovery
- Send within 5 days

### 5.6 Tools
- `os/15_PROPOSAL_TEMPLATE.md` (existing)
- `data/templates/proposal_499_sar_ar.md` (existing, adapt)
- `PROPOSAL_STRATEGY_AR.md` (PHASE 7)

---

## 6. Step 5: Proposal Sent

### 6.1 What It Is
- Client receives proposal
- Client reviews internally
- May have questions
- May negotiate
- May accept or reject

### 6.2 Owner
- Founder (relationship)
- Sales Lead (alternative)

### 6.3 Output
- Client response
- Negotiation points
- Decision (accept / negotiate / reject / delay)

### 6.4 Approval
- Follow-up messages: L1 (founder)
- Negotiation: L1-L3 per discount level

### 6.5 Time SLA
- Follow-up: 3 days if no response
- Decision: 14 days typical
- After 30 days: re-evaluate

### 6.6 Tools
- Email tracking
- CRM
- Next step rules (PHASE 6)

---

## 7. Step 6: Negotiation

### 7.1 What It Is
- Client wants changes
- We adjust scope/price/terms
- Re-quote
- Final agreement

### 7.2 Owner
- Founder (negotiation)
- Sales Lead (alternative)

### 7.3 Output
- Revised proposal
- Or rejection
- Or re-quote

### 7.4 Approval
- L2-L4 per changes
- All changes logged

### 7.5 Time SLA
- 1-2 rounds of negotiation
- Total negotiation: < 14 days
- After: walk away or close

### 7.6 Tools
- Discount policy (PHASE 5)
- Scope policy (PHASE 4)
- Founder + legal if custom

---

## 8. Step 7: Closed-Won + Delivery Handoff

### 8.1 What It Is
- Client accepts (signed)
- Invoice issued
- Payment received
- Handoff to delivery OS
- Active delivery starts

### 8.2 Owner
- Founder (close)
- Delivery Lead (delivery)
- CS Lead (post-delivery)

### 8.3 Output
- Signed agreement
- Paid invoice
- Delivery kickoff
- CS agent assigned

### 8.4 Approval
- Close: L1 (founder)
- Invoice: L2 (founder)
- Delivery handoff: L1 (founder)

### 8.5 Time SLA
- Invoice: same day
- Payment: per terms (Net 7-30)
- Delivery kickoff: 1-3 days after payment

### 8.6 Tools
- `MANUAL_PAYMENT_SOP.md` (existing)
- `os/18_HANDOVER_TEMPLATE.md` (existing)
- `os/16_CLIENT_ONBOARDING_TEMPLATE.md` (existing)

---

## 9. Failure Modes

### 9.1 Why Deals Are Lost
- ❌ Bad fit (ICP mismatch)
- ❌ No pain (just curious)
- ❌ No budget
- ❌ No decision maker
- ❌ Bad timing
- ❌ Price too high
- ❌ Lost to competitor
- ❌ Internal politics
- ❌ Went silent

### 9.2 Why Deals Are Won
- ✅ Clear pain
- ✅ Strong ICP fit
- ✅ Budget confirmed
- ✅ DM accessible
- ✅ Good timing
- ✅ Value clear
- ✅ Trust built
- ✅ Right offer match

### 9.3 Lost Deal Process
- Log reason in CRM
- Re-evaluate ICP
- Update if pattern
- Consider re-engage (3-6 months later)

---

## 10. Process Metrics

| Metric | Target |
|--------|--------|
| Lead → Qualified | 30%+ |
| Qualified → Discovery | 50%+ |
| Discovery → Proposal | 60%+ |
| Proposal → Won | 25%+ |
| End-to-end | 7-30 days |
| Average deal size | track |
| Win rate | track |

---

## 11. Sales Cadence (Founder)

### 11.1 Daily
- 2-3 discovery calls
- 5-10 follow-ups
- 1-2 proposal reviews
- 1-2 negotiations

### 11.2 Weekly
- Pipeline review
- Conversion analysis
- Best offer/channel/ICP check

### 11.3 Monthly
- Quota check
- Pattern analysis
- ICP refresh

---

## 12. Companion Files

- Pipeline: `PIPELINE_STAGES_AR.md`
- Qualification: `QUALIFICATION_RULES_AR.md`
- Discovery: `DISCOVERY_PROCESS_AR.md`
- Next Step: `NEXT_STEP_RULES_AR.md`
- Data: `data/commercial/opportunities.jsonl`
- Data: `data/commercial/discovery_notes.jsonl`
- Schema: `schemas/opportunity.schema.json`
- Schema: `schemas/discovery_note.schema.json`
- Report: `reports/commercial/PIPELINE_REVIEW.md`

---

**العملية واضحة، الـ owners واضحين، الـ SLAs محددة. founder يتبع، النظام يقيس، الفريق يحسّن.**
