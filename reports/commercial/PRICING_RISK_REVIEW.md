# Pricing Risk Review — تقرير مخاطر التسعير
**Dealix — Agent #3**
**التاريخ:** 2026-06-03

> **الغرض:** تقييم ذاتي لمخاطر التسعير، الفجوات، الأنماط المضادة، والتوصيات.

---

## 1. Pricing Risk Inventory

### 1.1 High-Risk Scenarios

| Scenario | Risk | Likelihood | Impact |
|----------|------|------------|--------|
| Discount without approval | margin loss | medium | high |
| Out-of-range quote | market mismatch | medium | medium |
| Below margin floor | financial loss | low | critical |
| Custom at standard price | delivery failure | medium | high |
| Multi-stakeholder without alignment | churn | medium | medium |
| Partner discount misuse | relationship damage | low | high |
| Refund without approval | financial loss | low | medium |
| Unpaid POC / pilot | delivery burden | high | high |

### 1.2 Medium-Risk Scenarios

| Scenario | Risk | Likelihood | Impact |
|----------|------|------------|--------|
| Late payment | cash flow | medium | medium |
| Dispute over scope | reputation | low | medium |
| Currency fluctuation | pricing | low | low |
| VAT calculation error | legal | low | medium |

### 1.3 Low-Risk Scenarios

| Scenario | Risk | Likelihood | Impact |
|----------|------|------------|--------|
| Standard quote error | minor | medium | low |
| Currency conversion | minor | low | low |
| Invoice format | minor | low | low |

---

## 2. Margin Risk Analysis

### 2.1 By Tier
| Tier | Margin Floor | Risk if Discount |
|------|--------------|------------------|
| Readiness Scan | 100% | none (no discount) |
| Diagnostic | 50% | low (small scope) |
| Workflow | 50% | medium |
| AI Starter | 40% | medium-high |
| Full OS | 35% | high |
| Retainer | 60% | low |
| Custom | 30% | high |

### 2.2 Critical Discount Thresholds
- Diagnostic: max -10% before margin risk
- Workflow: max -10%
- AI Starter: max -8%
- Full OS: max -8%
- Retainer: max -10% (recurring = bigger LTV)
- Custom: max -5% (already low margin)

---

## 3. Approval Risk

### 3.1 L1 Risks
- 95% of quotes should be L1
- Risk: low (founder in loop)
- Mitigation: random audit

### 3.2 L2 Risks
- Mid-tier, mid-discount
- Risk: medium
- Mitigation: reason logged

### 3.3 L3+ Risks
- High tier, large discount
- Risk: high
- Mitigation: founder + CCO + reason

---

## 4. Common Failure Modes

### 4.1 Discount Without Reason
- Agent offers 15% to "close the deal"
- Founder approves without question
- Result: margin loss + bad precedent
- **Mitigation:** strict reason requirement

### 4.2 Out-of-Range Without Approval
- Agent quotes 30K for Workflow (max 18K)
- Founder didn't see
- Result: misaligned expectations
- **Mitigation:** auto-alert if out of range

### 4.3 Custom at Standard
- Client asks for "premium" at workflow price
- Agent says yes
- Result: delivery failure
- **Mitigation:** scope review at L2+

### 4.4 Late Payment Cascade
- Client pays late
- Delivery continues
- Result: cash flow + relationship damage
- **Mitigation:** auto-pause at day 7

### 4.5 Refund Without Process
- Client demands refund
- Agent agrees
- Result: precedent + financial loss
- **Mitigation:** L3 approval + process

---

## 5. Pricing Compliance

### 5.1 vs `approval_policy.yaml`
- ✅ All discount requests require approval (L2+)
- ✅ All invoice sends require approval
- ✅ All refund requests require approval
- ✅ All custom enterprise requires L4+

### 5.2 vs `claim_policy.yaml`
- ✅ No ROI guarantees
- ✅ Numeric claims with source or `is_estimate`
- ✅ Security claims require source + approval

### 5.3 vs `claim_policy.yaml`
- ✅ No "guaranteed revenue" claims
- ✅ All customer-facing numbers labeled

---

## 6. Coverage Gaps

### 6.1 What's Missing
- ⚠️ No automated margin check at quote time
- ⚠️ No automated approval routing
- ⚠️ No real-time pricing analytics
- ⚠️ No competitive pricing tracker
- ⚠️ No exchange rate handling (future)

### 6.2 Mitigations
- Manual approval (current)
- Founder review
- Quarterly review

---

## 7. Recommendations

### 7.1 Short-term
1. ✅ Document all approval levels (done in this PHASE)
2. ✅ Add discount log (PHASE 6 schema)
3. ⏳ Add tests for pricing rules (PHASE 15)

### 7.2 Medium-term
1. ⏳ Add automated margin check
2. ⏳ Build approval queue UI
3. ⏳ Real-time pricing dashboard

### 7.3 Long-term
1. ⏳ Predictive pricing
2. ⏳ Competitive tracking
3. ⏳ Dynamic pricing (founder-approved)

---

## 8. Companion Files

- Guardrails: `PRICING_GUARDRAILS_AR.md`
- Discount: `DISCOUNT_POLICY_AR.md`
- Terms: `PAYMENT_TERMS_AR.md`
- Anchoring: `PRICE_ANCHORING_GUIDE_AR.md`
- Approval: `QUOTE_APPROVAL_POLICY_AR.md`
- Data: `data/commercial/pricing_rules.yaml`
- Schema: `schemas/pricing_rule.schema.json`
- Existing: `dealix/config/pricing.yaml`

---

**مخاطر التسعير = الأكثر شيوعاً في الشركات. founder يحمي الهامش بـ guardrails صارمة + approval levels + log. لا "trust me" — وثّق.**
