# Partner Pipeline Process — عملية pipeline الشراكات
**Dealix — Agent #3**

> **الغرض:** كيف ندير pipeline الشراكات، من source إلى closed-won.

---

## 1. The 7 Pipeline Stages

```
[1. Sourced] → [2. Qualified] → [3. Negotiating] → [4. Signed]
                                                     ↓
[7. Closed/Terminated] ← [6. Performance Review] ← [5. Active]
```

---

## 2. Stage 1: Sourced

### 2.1 What
- Partner identified
- Initial contact
- Source: network, content, event, referral

### 2.2 Owner
- Founder
- Partner Channel Agent

### 2.3 Output
- Partner record (CRM)
- Initial fit assessment
- Next step (research / qualify / skip)

### 2.4 Approval
- L1 (founder)

### 2.5 SLA
- < 7 days from source to qualify

---

## 3. Stage 2: Qualified

### 3.1 What
- Has client access
- Not selling spam
- Understands B2B
- Accepts approval-first
- Legal entity
- 3+ paid pilots (for white-label)

### 3.2 Owner
- Partner Channel Agent
- Founder

### 3.3 Output
- Qualification score
- Model recommendation
- Margin range
- Agreement draft

### 3.4 Approval
- L2 (founder)

### 3.5 SLA
- < 14 days from sourced to qualified

---

## 4. Stage 3: Negotiating

### 4.1 What
- Discussion of model
- Margin negotiation
- Term
- Responsibilities
- Legal review

### 4.2 Owner
- Founder
- Legal (counsel)

### 4.3 Output
- Term sheet
- Agreement draft
- Approval level identified

### 4.4 Approval
- L2-L5 per model

### 4.5 SLA
- < 30 days from qualified to signed

---

## 5. Stage 4: Signed

### 5.1 What
- Agreement signed
- Both parties
- Effective date

### 5.2 Owner
- Founder
- Legal

### 5.3 Output
- Executed agreement
- Partner onboarding initiated

### 5.4 Approval
- Per agreement

### 5.5 SLA
- < 7 days from signed to active

---

## 6. Stage 5: Active

### 6.1 What
- Partner operational
- Leads flowing
- Deals in pipeline
- Co-marketing active

### 6.2 Owner
- Partner Channel Agent
- Founder
- Partner

### 6.3 Output
- Pipeline updates
- Performance metrics
- Issue resolution

### 6.4 Approval
- L2 for routine
- L3+ for special

### 6.5 SLA
- 1-2 check-ins per month
- Quarterly review

---

## 7. Stage 6: Performance Review

### 7.1 What
- Quarterly review
- Performance against targets
- Adjust margin if needed
- Renew or adjust

### 7.2 Owner
- Founder
- Partner Channel Agent

### 7.3 Output
- Performance report
- Margin adjustment (if any)
- Renewal or termination

### 7.4 Approval
- L2 for review
- L3 for margin change

### 7.5 SLA
- Quarterly

---

## 8. Stage 7: Closed/Terminated

### 8.1 What
- Partner terminated (by either party)
- 30 days notice
- Handoff active clients
- Pay pending commissions

### 8.2 Owner
- Founder
- Partner Channel Agent

### 8.3 Output
- Termination agreement
- Client handoff
- Brand usage stop

### 8.4 Approval
- L3 for termination

### 8.5 SLA
- 30 days notice minimum

---

## 9. Pipeline Tracking

### 9.1 Where
- `data/partners/partner_opportunities.jsonl`
- `schemas/partner_opportunity.schema.json`
- CRM

### 9.2 What to Track
- Stage
- Owner
- Next step
- Due date
- Conversion
- Margin earned

---

## 10. Pipeline Metrics

| Metric | Target |
|--------|--------|
| Source → Qualified | 50%+ |
| Qualified → Signed | 60%+ |
| Active partner → Win | 1+ per quarter |
| Avg time to active | < 60 days |
| Active partner retention | > 80% (annual) |

---

## 11. The Partner Lifecycle

```
[New] → [Active] → [Strategic] → [Mature]
   ↓        ↓           ↓            ↓
[Terminate] [Pause]   [Re-negotiate] [Long-term]
```

---

## 12. Anti-Patterns

### 12.1 ❌ Don't Do
- ❌ Sign without qualification
- ❌ Skip legal review
- ❌ Accept vague terms
- ❌ Skip performance review
- ❌ Terminate without notice

### 12.2 ✅ Do
- ✅ Always qualify
- ✅ Always legal
- ✅ Clear terms
- ✅ Quarterly review
- ✅ Proper termination

---

## 13. Companion Files

- Model: `PARTNER_COMMERCIAL_MODEL_AR.md`
- Pricing: `PARTNER_PRICING_AND_MARGIN_AR.md`
- Enablement: `PARTNER_ENABLEMENT_KIT_AR.md`
- Qualification: `PARTNER_QUALIFICATION_AR.md`
- Schema: `schemas/partner_opportunity.schema.json`
- Data: `data/partners/partner_opportunities.jsonl`
- Existing: `docs/partners/PARTNER_PILOT_PIPELINE.yaml`
- Existing: `dealix/config/partner_rules.yaml`

---

**Pipeline = شريان الشراكات. كل شريك = قيمة محتملة. founder يبني، الشريك ينفذ، العميل يستفيد.**
