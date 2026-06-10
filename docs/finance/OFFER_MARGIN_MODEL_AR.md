# Offer Margin Model — نموذج هامش العروض
**Dealix — Agent #3**

> **الغرض:** كيف نحسب margin لكل عرض، ونقرر متى نرفع السعر، ومتى نوقف.

---

## 1. Margin Calculation

### 1.1 Formula
```
Margin = (Price - Total Cost) / Price × 100
Total Cost = Delivery + Sales + Support + Overhead
```

### 1.2 Components

**Delivery cost:**
- Founder time × hourly rate
- Tool costs
- Subcontractor (if any)
- Materials

**Sales cost:**
- Founder time × hourly rate
- Content (allocated)
- Tools (CRM, etc.)

**Support cost:**
- CS time × hourly rate
- Tools

**Overhead:**
- Allocated per client
- Office, software, etc.

---

## 2. Per-Offer Margin (Estimated)

| Offer | Avg Price | Delivery | Sales | Support | Overhead | Margin |
|-------|-----------|----------|-------|---------|----------|--------|
| Readiness Scan | 499 | 50 | 25 | 10 | 15 | 80% |
| Diagnostic | 3,500 | 1,750 | 350 | 50 | 175 | 50% |
| Workflow | 12,000 | 6,000 | 1,200 | 300 | 600 | 50% |
| AI Starter | 25,000 | 15,000 | 2,500 | 1,000 | 1,500 | 40% |
| Full OS | 60,000 | 40,000 | 6,000 | 3,000 | 4,000 | 33% |
| Retainer/mo | 7,000 | 2,800 | 700 | 700 | 700 | 60% |
| Custom | 120,000 | 85,000 | 12,000 | 6,000 | 8,000 | 30% |

**All is_estimate: true**

---

## 3. Margin Floor

### 3.1 Per Tier
| Tier | Min Margin | Reason |
|------|-----------|--------|
| Entry | 80% | just time |
| Standard | 50% | small effort |
| Pro | 40% | mid effort |
| Premium | 30% | high effort |
| Retainer | 50% | recurring, relationship |
| Custom | 25% | complex |

### 3.2 If Below Floor
- Stop offer
- Raise price
- Reduce scope
- Reduce delivery cost

---

## 4. Margin Erosion Patterns

### 4.1 Common Causes
- Discount without reason
- Custom at standard price
- Scope creep
- High delivery cost
- High sales cost
- Long cycle time
- High partner commission

### 4.2 Detection
- Track per deal
- Monthly margin review
- Flag below-floor
- Founder decision

---

## 5. Margin Improvement

### 5.1 Levers
- Raise price (within range, no anchor change)
- Reduce scope (without losing core)
- Reduce delivery time (templates, automation)
- Reduce sales time (better funnel)
- Volume discount (per unit)

### 5.2 Trade-offs
- Higher price → fewer leads
- Less scope → less value
- Faster delivery → less quality
- Less sales → fewer leads

---

## 6. Margin by ICP

| ICP | Avg Margin | Reason |
|-----|-----------|--------|
| Marketing Agency | 55% | efficient delivery |
| Clinic | 45% | PDPL review adds cost |
| Education | 50% | seasonal efficiency |
| Local SaaS | 40% | higher scope |
| Real Estate | 50% | mid-effort |
| Training | 50% | clear scope |

---

## 7. Margin by Channel

| Channel | Avg Margin | Reason |
|---------|-----------|--------|
| Inbound | 50% | low sales cost |
| Warm email | 50% | medium sales cost |
| LinkedIn | 45% | high sales cost |
| Partners | 40% | commission reduces |
| Content | 55% | low direct cost |

---

## 8. The Decision Matrix

| Margin | Decision |
|--------|----------|
| > 50% | Scale |
| 30-50% | Maintain |
| 20-30% | Optimize |
| < 20% | Stop or Raise |

---

## 9. Margin Erosion Triggers

### 9.1 Stop Trigger
- Margin < 20% for 3+ months
- Volume < 1 per month
- Discount needed > 20%
- Delivery time > 2x estimate

### 9.2 Raise Trigger
- Margin stable 30-40%
- Demand > supply
- Founder time > 50% on delivery
- Quality feedback positive

---

## 10. The Review Cadence

- **Per deal:** track actual margin
- **Weekly:** review at-risk deals
- **Monthly:** by-offer review
- **Quarterly:** by-ICP + by-channel review
- **Yearly:** strategy review

---

## 11. Companion Files

- Unit Econ: `COMMERCIAL_UNIT_ECONOMICS_AR.md`
- CAC: `CAC_PAYBACK_MODEL_AR.md`
- Channel: `CHANNEL_ROI_MODEL_AR.md`
- Capacity: `SALES_CAPACITY_MODEL_AR.md`
- Retainer: `RETAINER_REVENUE_MODEL_AR.md`
- Pricing: `PRICING_GUARDRAILS_AR.md` (PHASE 5)

---

**Margin = صحة. كل ريال = قيمة. founder يقيس، النظام يحسب، العرض يستمر أو يتوقف.**
