# Partner Commercial Model — النموذج التجاري للشراكات
**Dealix — Agent #3**

> **الغرض:** 6 نماذج شراكة، responsibilities، margins، risks. مكمل لـ `dealix/config/partner_rules.yaml`.

---

## 1. The 6 Partnership Models

### 1.1 Referral Partner
- **Description:** Partner refers client, Dealix closes + delivers
- **Partner responsibility:** refer qualified leads
- **Dealix responsibility:** all sales + delivery + support
- **Margin:** 10-20% of first payment
- **Risk:** low
- **Approval:** L2 per `partner_rules.yaml`
- **Examples:** agency, accounting firm, consultant

### 1.2 Co-Selling
- **Description:** Partner + Dealix sell together
- **Partner responsibility:** part of sales process
- **Dealix responsibility:** lead + close + deliver
- **Margin:** split per agreement
- **Risk:** medium (shared accountability)
- **Approval:** L2
- **Examples:** CRM implementer, biz consultant

### 1.3 Implementation Partner
- **Description:** Partner implements Dealix
- **Partner responsibility:** delivery
- **Dealix responsibility:** diagnostic + proof + governance
- **Margin:** implementation fee retained by partner
- **Risk:** medium (delivery quality)
- **Approval:** L3
- **Examples:** agency, system integrator

### 1.4 Co-Delivery
- **Description:** Partner + Dealix deliver together
- **Partner responsibility:** some workflows
- **Dealix responsibility:** other workflows
- **Margin:** split per agreement
- **Risk:** medium (coordination)
- **Approval:** L3
- **Examples:** niche agencies, ops consultants

### 1.5 Channel Reseller
- **Description:** Partner resells Dealix as their product
- **Partner responsibility:** all sales + first-line support
- **Dealix responsibility:** delivery + escalation
- **Margin:** 30-40% channel margin
- **Risk:** high (brand control)
- **Approval:** L4
- **Examples:** software resellers, B2B service firms

### 1.6 White Label
- **Description:** Partner brands Dealix as their own
- **Partner responsibility:** all
- **Dealix responsibility:** backend
- **Margin:** per agreement (typically 40-50%)
- **Risk:** high (full brand risk)
- **Approval:** L5 (board-level)
- **Requirements:** 3+ paid pilots first, legal review, founder approval
- **Examples:** larger agencies

---

## 2. Model Selection

### 2.1 By Partner Type
| Partner Type | Default Model | Variation |
|--------------|---------------|-----------|
| Marketing agency | Referral / Co-sell | Implementation |
| CRM implementer | Referral | Implementation |
| Biz consultant | Referral | Co-delivery |
| Training company | Referral | — |
| Accounting firm | Referral | — |
| Web agency | Referral | Co-sell |
| Software reseller | Channel | — |
| Operations consultant | Co-delivery | Implementation |

### 2.2 By Partner Maturity
- **New partner:** Start with Referral (lowest risk)
- **Trusted partner (3+ months):** Add Co-sell
- **Strategic partner (6+ months, 3+ deals):** Add Implementation
- **Mature partner (12+ months, 5+ deals):** Consider Channel/White-label

### 2.3 By Client Size
- **SMB (5K-25K):** Referral
- **Mid (25K-90K):** Co-sell or Implementation
- **Enterprise (90K+):** Co-delivery or Channel

---

## 3. Margin Splits

### 3.1 Referral
- Partner: 10-20% of first payment
- Dealix: 80-90%
- Recurring: typically no (or 5-10% if renewal attributed)

### 3.2 Co-Sell
- Partner: 20-30% of total
- Dealix: 70-80%
- Per agreement

### 3.3 Implementation
- Partner: implementation fee (e.g., 50% of project)
- Dealix: diagnostic + proof (retain)
- Per agreement

### 3.4 Co-Delivery
- Per workflow split
- Typically 50-70% Dealix, 30-50% partner
- Per agreement

### 3.5 Channel Reseller
- Partner: 30-40% of total
- Dealix: 60-70%
- Recurring: 30-40% of retainer

### 3.6 White Label
- Partner: 40-50% of total
- Dealix: 50-60%
- Recurring: 40-50% of retainer

---

## 4. Approval Levels

| Model | Approval | Reason |
|-------|----------|--------|
| Referral | L2 | simple |
| Co-Sell | L2 | simple |
| Implementation | L3 | delivery quality |
| Co-Delivery | L3 | coordination |
| Channel Reseller | L4 | brand risk |
| White Label | L5 | full brand + legal |

---

## 5. Client Ownership

### 5.1 Default
- Dealix = client owner
- Partner = supporter
- Renewal handled by Dealix
- Unless otherwise agreed

### 5.2 Channel/White Label
- Partner = client owner
- Dealix = backend
- Renewal by partner

### 5.3 Co-Delivery
- Joint ownership
- Renewal jointly

---

## 6. Support Model

### 6.1 Default
- Dealix = primary support
- Partner = first line (if agreed)
- Escalation to Dealix

### 6.2 Channel/White Label
- Partner = all support
- Dealix = escalation only

---

## 7. Risk Distribution

### 7.1 Risk by Model
| Model | Partner Risk | Dealix Risk | Joint Risk |
|-------|--------------|-------------|------------|
| Referral | low | high | low |
| Co-Sell | medium | high | medium |
| Implementation | medium | high | medium |
| Co-Delivery | high | high | high |
| Channel | high | medium | medium |
| White Label | very high | low | low |

### 7.2 Mitigation
- Clear contracts
- KPIs and SLAs
- Termination clauses
- Quality audits

---

## 8. Termination

### 8.1 By Either Party
- 30 days written notice
- For material breach
- For non-performance
- For reputation damage

### 8.2 In Flight
- Finish in-flight projects
- Handoff active clients
- Pay pending commissions

### 8.3 Post-Termination
- Commission on existing clients
- Co-marketing removal
- Brand usage stop

---

## 9. The Partner Agreement

### 9.1 Key Terms
- Model + scope
- Margin split
- Responsibilities
- Term
- Termination
- Confidentiality
- IP
- Liability
- Dispute resolution

### 9.2 Legal Review
- All agreements: legal review
- Saudi law
- Founder + counsel

---

## 10. Partner Operations

### 10.1 Onboarding
- Qualify
- Sign agreement
- Train
- Co-brand materials
- First deal

### 10.2 Ongoing
- Monthly check-in
- Quarterly review
- Performance tracking
- Issue resolution

### 10.3 Offboarding
- 30 days notice
- Handoff clients
- Pay commissions
- Brand usage stop

---

## 11. Companion Files

- Pricing: `PARTNER_PRICING_AND_MARGIN_AR.md`
- Pipeline: `PARTNER_PIPELINE_PROCESS_AR.md`
- Enablement: `PARTNER_ENABLEMENT_KIT_AR.md`
- Qualification: `PARTNER_QUALIFICATION_AR.md`
- Existing: `dealix/config/partner_rules.yaml`
- Existing: `docs/partners/PARTNER_PILOT_PIPELINE.yaml`
- Schema: `schemas/partner_opportunity.schema.json`
- Data: `data/partners/partner_opportunities.jsonl`
- Report: `reports/partnerships/PARTNER_COMMERCIAL_REVIEW.md`

---

**النماذج = مرونة. كل شريك = نموذج مختلف. founder يختار، النظام يحمي، الـ margin يبقى.**
