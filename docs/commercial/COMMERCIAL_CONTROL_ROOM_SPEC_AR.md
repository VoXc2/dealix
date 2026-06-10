# Commercial Control Room Spec — مواصفات غرفة التحكم التجارية
**Dealix — Agent #3**

> **الغرض:** تصميم غرفة التحكم التجارية التي يطلع عليها المؤسس يومياً/أسبوعياً. تكملة لـ `/[locale]/ops/founder` (existing).

---

## 1. Route

**Primary:** `/[locale]/ops/commercial-control`
**Arabic:** `/ar/ops/commercial-control`
**English:** `/en/ops/commercial-control`

**Access:** founder + admin key (per `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY`)

---

## 2. The 14 Tabs

| # | Tab | Description |
|---|-----|-------------|
| 1 | **ICP** | Client segments, scores, priority |
| 2 | **Offers** | Product catalog, performance |
| 3 | **Pricing** | Pricing rules, approvals, discounts |
| 4 | **Pipeline** | All stages, value, conversion |
| 5 | **Prospects** | Active leads, qualification |
| 6 | **Proposals** | Sent, pending, accepted |
| 7 | **Proof Packs** | Delivered, used in sales |
| 8 | **Payments** | Pending, received, refunds |
| 9 | **Delivery Handoffs** | Won → Delivery transition |
| 10 | **Renewals** | Coming, in progress, completed |
| 11 | **Partnerships** | Active, sourced, terminated |
| 12 | **Channel ROI** | Performance by channel |
| 13 | **Finance** | Revenue, margin, runway |
| 14 | **Risks** | Active, mitigated, walked away |

---

## 3. Top Cards (Always Visible)

```
┌──────────────────────────────────────────┐
│  Pipeline Value (qualified): 145,000 SAR │
│  Proposals Awaiting: 3                   │
│  Payment Handoffs: 1                     │
│  Won This Month: 35,000 SAR              │
│  Active Risks: 2                         │
│  Renewals in 30 days: 3                  │
│  Best Channel: Inbound (5x ROI)          │
│  Best Offer: Diagnostic 9,999 (45%)     │
│  Founder Decision: Discount approval X  │
└──────────────────────────────────────────┘
```

---

## 4. The 4-View Layout

### 4.1 Daily View (founder)
- Top cards
- Today's calendar
- Pending approvals (action required)
- Active risks
- Pipeline movement

### 4.2 Weekly View (founder)
- All daily
- Weekly metrics
- Conversion
- Best/worst
- Next week plan

### 4.3 Monthly View (founder + CCO)
- All weekly
- Monthly close
- Cohort analysis
- Finance review
- ICP refresh

### 4.4 Quarterly View (founder + board)
- All monthly
- Strategy review
- New segments
- Pricing review
- Annual plan

---

## 5. Tab Specifications

### 5.1 ICP Tab
- List of 10 segments
- Score per segment
- Priority rank
- Performance metrics
- Disqualifiers
- Update button (founder)

### 5.2 Offers Tab
- 7 products
- Price, margin, performance
- Conversion rate
- Active count
- Sunset candidates

### 5.3 Pricing Tab
- Pending approvals
- Recent quotes
- Discount log
- Margin tracking
- Out-of-range flags

### 5.4 Pipeline Tab
- 21 stages
- Count + value
- Avg age
- Conversion
- Stale alerts

### 5.5 Prospects Tab
- Active leads
- Qualification status
- Discovery scheduled
- Pain category
- Next step

### 5.6 Proposals Tab
- Sent (with status)
- Pending approval
- Accepted
- Rejected
- Avg time to decision

### 5.7 Proof Packs Tab
- Delivered (per client)
- Templates
- Anonymized examples
- Permission status
- L-level breakdown

### 5.8 Payments Tab
- Pending
- Received
- Refunds
- Disputes
- Aging report

### 5.9 Delivery Handoffs Tab
- Won → Delivery
- Handoff checklist
- Status
- Issues
- Time to kickoff

### 5.10 Renewals Tab
- Coming (30 days)
- In discussion
- Pending signature
- Completed
- Lost
- Expansion opportunities

### 5.11 Partnerships Tab
- Active partners
- Sourced deals
- Performance
- Margins
- Termination alerts

### 5.12 Channel ROI Tab
- Per channel
- Cost
- Customers
- CAC
- ROI
- Trend

### 5.13 Finance Tab
- Revenue (today/week/month/quarter)
- MRR
- Margin
- Burn
- Runway
- Forecast

### 5.14 Risks Tab
- Active (by severity)
- Mitigated
- Walked away
- Bad-fit
- Scope creep
- Margin erosion

---

## 6. Cross-Cutting Features

### 6.1 Filters
- Date range
- ICP
- Offer
- Channel
- Owner
- Status

### 6.2 Sort
- By value
- By age
- By status
- By owner

### 6.3 Export
- CSV
- PDF
- JSON

### 6.4 Drill-Down
- Click → detail view
- Back to list

### 6.5 Approval Actions
- Approve / Reject / Revise
- Reason required
- Logged

---

## 7. Permissions

| Role | View | Edit | Approve |
|------|------|------|---------|
| Founder | All | All | All |
| Admin | All | Limited | Limited |
| CS Agent | Limited (clients) | Limited | None |
| Sales Lead | Most | Yes | L1 only |
| Partner | Own | Own | None |
| Client | Own | Own | N/A |

---

## 8. Real-Time Updates

- Pipeline changes → live
- Approvals → live
- Risks → live
- Payments → live (webhook)
- Daily/weekly → refreshed hourly

---

## 9. Mobile View

- Key cards
- Today's actions
- Pending approvals
- Mobile-friendly

---

## 10. Notifications

### 10.1 Push
- New approval needed
- Risk critical
- Payment received
- Renewal window

### 10.2 Email
- Daily digest (optional)
- Weekly summary
- Critical alerts

---

## 11. Companion Files

- Daily: `COMMERCIAL_DAILY_COMMAND.md`
- Weekly: `COMMERCIAL_WEEKLY_REVIEW.md`
- Existing: `/[locale]/ops/founder` (route)
- Existing: `/[locale]/ops/war-room`
- Existing: `/[locale]/ops/marketing`
- Existing: `/[locale]/ops/sales`
- Existing: `/[locale]/ops/partners`
- Existing: `/[locale]/ops/evidence`
- Existing: `/[locale]/ops/approvals`

---

**غرفة التحكم = 14 tab + 9 top cards + 4 views + permissions + real-time. founder يفتح، يعرف، يقرّر، يتابع.**
