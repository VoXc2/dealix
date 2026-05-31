# Unit Economics — Dealix

## Overview
Financial model and unit economics for Dealix operations.

**Last Updated**: 2026-05-31
**Currency**: SAR (Saudi Riyal)

---

## Revenue Model

### P1: Revenue Intelligence Sprint
| Package | Price | Delivery Hours | Cost | Gross Margin |
|---|---|---|---|---|
| Basic | 2,500 SAR | 8 hours | 800 SAR | 68% |
| Standard | 5,000 SAR | 12 hours | 1,200 SAR | 76% |
| Premium | 7,500 SAR | 16 hours | 1,600 SAR | 79% |

### P2: AI Sales Ops Retainer
| Tier | Monthly Price | Monthly Hours | Cost | Gross Margin |
|---|---|---|---|---|
| Small | 3,000 SAR | 6 hours | 600 SAR | 80% |
| Medium | 8,000 SAR | 12 hours | 1,200 SAR | 85% |
| Large | 15,000 SAR | 20 hours | 2,000 SAR | 87% |
| Enterprise | 30,000 SAR | 40 hours | 4,000 SAR | 87% |

---

## Cost Structure

### Variable Costs (per engagement)
| Cost Item | Sprint | Retainer (Monthly) |
|---|---|---|
| AI tools & APIs | 200 SAR | 400 SAR |
| Cloud infrastructure | 100 SAR | 200 SAR |
| Analyst time | 500 SAR | 2,000 SAR |
| Founder time (review) | 200 SAR | 800 SAR |
| **Total Variable** | **1,000 SAR** | **3,400 SAR** |

### Fixed Costs (Monthly)
| Cost Item | Amount |
|---|---|
| Office/co-working | 2,000 SAR |
| Software licenses | 1,500 SAR |
| Legal & compliance | 1,000 SAR |
| Marketing | 2,000 SAR |
| Insurance | 500 SAR |
| **Total Fixed** | **7,000 SAR** |

---

## Unit Economics Calculator

### CAC (Customer Acquisition Cost)
```
CAC = Total Sales & Marketing Spend / New Customers

Target: < 2,500 SAR per P1 client
Method: Organic outreach + content
```

### LTV (Lifetime Value)
```
LTV = (Monthly Profit × Gross Margin × Average Retention Months)

For Small Retainer:
- Monthly revenue: 3,000 SAR
- Monthly cost: 3,400 SAR (variable) + 583 SAR (fixed share)
- Monthly profit: -983 SAR (initially)

For Medium Retainer:
- Monthly revenue: 8,000 SAR
- Monthly cost: 3,400 SAR (variable) + 583 SAR (fixed share)
- Monthly profit: 4,017 SAR

Target: Positive by Month 3
```

### Payback Period
```
Target: < 3 months for P1 → P2 conversion

P1 Sprint profit: ~3,500 SAR (standard)
P2 setup cost: ~1,000 SAR
Net: ~2,500 SAR recoverable

If P1 client converts to Small Retainer:
- Break even: Month 1-2
- Profitable: Month 3+
```

### Gross Margin Target
```
Overall target: > 60%
Sprint-only: > 70%
With Retainer: > 80%

Current: N/A (pre-revenue)
```

---

## Financial Targets

### Month 1 (June 2026)
| Metric | Target |
|---|---|
| P1 Sprints sold | 2 |
| Revenue | 10,000 — 15,000 SAR |
| Costs | 8,000 SAR |
| Net | 2,000 — 7,000 SAR |

### Month 2 (July 2026)
| Metric | Target |
|---|---|
| P1 Sprints sold | 3 |
| P2 Retainers signed | 1 |
| Revenue | 25,000 — 35,000 SAR |
| Costs | 12,000 SAR |
| Net | 13,000 — 23,000 SAR |

### Month 3 (August 2026)
| Metric | Target |
|---|---|
| P1 Sprints sold | 3 |
| P2 Retainers active | 2-3 |
| Revenue | 40,000 — 60,000 SAR |
| Costs | 15,000 SAR |
| Net | 25,000 — 45,000 SAR |

### 90-Day Target
- **Total Revenue**: 75,000 — 110,000 SAR
- **MRR by end of Month 3**: 11,000 — 30,000 SAR
- **Total Clients**: 8-10 P1 + 2-3 P2

---

## Break-Even Analysis

### Monthly Break-Even
```
Fixed Costs: 7,000 SAR
Target Gross Margin: 75%

Break-even revenue = Fixed Costs / Gross Margin
= 7,000 / 0.75
= 9,333 SAR/month

With P1 only (5,000 SAR avg):
- Need ~2 P1 sprints/month

With P1 + P2:
- 1 P1 + 1 Small Retainer = 8,000 SAR (close)
- 1 P1 + 1 Medium Retainer = 13,000 SAR (profitable)
```

### Cash Runway
```
Current Cash: To be determined
Monthly Burn: ~7,000 SAR (fixed) + variable
Runway Target: 6 months minimum
```

---

## Key Financial Metrics Dashboard

| Metric | Formula | Target | Current |
|---|---|---|---|
| Gross Margin | (Revenue - COGS) / Revenue | > 60% | N/A |
| MRR Growth | (MRR this month - MRR last) / MRR last | > 20% | N/A |
| CAC | S&M Spend / New Customers | < 2,500 SAR | N/A |
| LTV | Avg Profit × Retention Months | > 15,000 SAR | N/A |
| LTV:CAC Ratio | LTV / CAC | > 3:1 | N/A |
| Payback Period | Months to recover CAC | < 3 months | N/A |
| Net Revenue Retention | (Start + Expansion - Churn) / Start | > 100% | N/A |
| Cash Collected | Actual cash received | > Projected | N/A |

---

## Revenue Scorecard Formula

Weekly tracking via `revenue_scorecard.py`:

```python
# Key calculations
c conversion_rate = proposals_won / proposals_sent
reply_rate = replies_received / outreach_sent
meeting_rate = calls_booked / replies_received
avg_deal_size = revenue_collected / proposals_won
pipeline_value = sum(all_prospects.offer_value)
```

---

## Notes
- All costs estimated until actual data available
- Update this file weekly with actual figures
- Flag any metric below target immediately
