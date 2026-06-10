# Dealix — Feature Priority Review

**Date:** 2026-03-01
**Period:** Q1-Q2 2026
**Reviewer:** Product Team
**Status:** Active

---

## Executive Summary

This report reviews all features in the product backlog using the ICE/RICE prioritization framework. The goal is to ensure we're building the right things at the right time.

**Key Findings:**
- 10 features in backlog
- 3 features P0 (launch blockers)
- 4 features P1 (revenue critical)
- 1 feature P2 (scale enabler)
- 2 features P5 (do not build)

---

## Prioritization Framework

### ICE Score Calculation
```
ICE = (Impact × Confidence × Ease) / Risk
```

| Score Range | Action |
|-------------|--------|
| 70+ | Build now |
| 40-70 | Backlog |
| <40 | Do not build |

---

## Feature Rankings

### Top Priority (P0-P1)

| Rank | Feature | ICE Score | Priority | Status |
|------|---------|-----------|----------|--------|
| 1 | Control Room Dashboard | 90 | P0 | Planned |
| 2 | Approval Queue v1 | 81 | P0 | In Progress |
| 3 | GTM Draft Factory | 72 | P0 | Planned |
| 4 | Weekly Reports v1 | 72 | P1 | Backlog |
| 5 | Renewal Engine | 72 | P1 | Backlog |
| 6 | Lead Scoring v1 | 56 | P1 | Planned |
| 7 | Client Secure Portal | 56 | P1 | Backlog |

### Lower Priority (P2+)

| Rank | Feature | ICE Score | Priority | Status |
|------|---------|-----------|----------|--------|
| 8 | Reply Classification | 42 | P2 | Backlog |
| 9 | WhatsApp Consent Flow | 15 | P3 | Backlog |
| 10 | LinkedIn Automation | 7.5 | P5 | Rejected |

---

## Detailed Feature Analysis

### P0 Features (Build Now)

#### 1. Control Room Dashboard
```
ICE Score: 90
Priority: P0
Status: Planned

Scores:
- Impact: 10 (Critical for founder)
- Confidence: 9 (Clear requirement)
- Ease: 5 (Complex but doable)
- Risk: 2 (Low technical risk)

Revenue Impact: Critical
Effort: Large (1-2 months)
Dependencies: None
```

**Why Build Now:**
- Direct founder request
- Enables faster decisions
- Foundation for all other features
- High ROI potential

**Acceptance Criteria:**
- Pipeline metrics visible
- Revenue metrics shown
- Alert system works
- Action items clearly displayed

---

#### 2. Approval Queue v1
```
ICE Score: 81
Priority: P0
Status: In Progress

Scores:
- Impact: 9 (Prevents mistakes)
- Confidence: 9 (Clear need)
- Ease: 6 (Well understood)
- Risk: 3 (Low compliance risk)

Revenue Impact: High
Effort: Medium (2-4 weeks)
Dependencies: None
```

**Why Build Now:**
- Compliance requirement
- Prevents reputation damage
- Customer demanded it
- Foundation for safe automation

**Acceptance Criteria:**
- Queue UI displays pending items
- Email notifications on new items
- Approve/reject functionality works
- Audit log captures all actions

---

#### 3. GTM Draft Factory
```
ICE Score: 72
Priority: P0
Status: Planned

Scores:
- Impact: 9 (Major efficiency gain)
- Confidence: 8 (Clear use case)
- Ease: 4 (Complex AI work)
- Risk: 4 (Moderate)

Revenue Impact: High
Effort: Large (1-2 months)
Dependencies: Approval Queue
```

**Why Build Now:**
- Major efficiency improvement
- Multiple customers requested
- Enables faster outreach
- Clear ROI

**Acceptance Criteria:**
- Draft generation API works
- Personalization based on ICP
- Quality scoring for drafts
- Integration with approval queue

---

### P1 Features (Build Next)

#### 4. Weekly Reports v1
```
ICE Score: 72
Priority: P1
Status: Backlog

Scores:
- Impact: 9 (Direct renewal impact)
- Confidence: 8 (Proven value)
- Ease: 6 (Well understood)
- Risk: 2 (Low)

Revenue Impact: High
Effort: Medium (2-4 weeks)
Dependencies: Client Portal
```

**Evidence:**
- Customer: "The weekly reports were very helpful in justifying the investment. This is a key reason we're renewing."
- Source: Renewal discussion with Client Eta

---

#### 5. Renewal Engine
```
ICE Score: 72
Priority: P1
Status: Backlog

Scores:
- Impact: 9 (Revenue protection)
- Confidence: 8 (Clear need)
- Ease: 6 (Straightforward logic)
- Risk: 3 (Low)

Revenue Impact: Critical
Effort: Medium (2-4 weeks)
Dependencies: Weekly Reports
```

**Evidence:**
- Lost customer: "We didn't renew because we didn't see clear value."
- Source: Churn risk feedback from Client Theta

---

#### 6. Lead Scoring v1
```
ICE Score: 56
Priority: P1
Status: Planned

Scores:
- Impact: 8 (Better prioritization)
- Confidence: 7 (Good signal)
- Ease: 6 (Standard logic)
- Risk: 3 (Low)

Revenue Impact: High
Effort: Medium (2-4 weeks)
Dependencies: None
```

**Evidence:**
- "كيف أحدد وين أركز؟ عندنا many leads بس ما نعرف وين نبدأ."
- Source: Discovery call with Prospect Beta

---

#### 7. Client Secure Portal
```
ICE Score: 56
Priority: P1
Status: Backlog

Scores:
- Impact: 7 (Client satisfaction)
- Confidence: 8 (Clear request)
- Ease: 4 (Complex auth)
- Risk: 4 (Security concerns)

Revenue Impact: Medium
Effort: Large (1-2 months)
Dependencies: None
```

**Evidence:**
- "أبي أشوف progress بمفردي. أبي portal أقدر أوصل له وأشوف كل شي."
- Source: Monthly check-in with Client Epsilon

---

### P2 Features (Backlog)

#### 8. Reply Classification
```
ICE Score: 42
Priority: P2
Status: Backlog

Scores:
- Impact: 7 (Efficiency)
- Confidence: 6 (Moderate)
- Ease: 6 (Moderate complexity)
- Risk: 4 (Moderate)

Revenue Impact: Medium
Effort: Medium (2-4 weeks)
Dependencies: None
```

**Decision:** Backlog - Important but not urgent. Can address with basic triage first.

---

### P3+ Features (Do Not Build / Investigate)

#### 9. WhatsApp Consent Flow
```
ICE Score: 15
Priority: P3
Status: Backlog

Scores:
- Impact: 6 (Nice to have)
- Confidence: 5 (Uncertain)
- Ease: 2 (Complex compliance)
- Risk: 8 (High)

Revenue Impact: Medium
Effort: Extra Large (2-3 months)
Blockers: Meta API approval, Legal clarity
```

**Decision:** Defer until legal clarity and Meta approval received.

---

#### 10. LinkedIn Automation
```
ICE Score: 7.5
Priority: P5
Status: Rejected

Scores:
- Impact: 5 (Moderate)
- Confidence: 3 (Low)
- Ease: 2 (Complex)
- Risk: 9 (Very High)

Revenue Impact: Medium
Effort: Extra Large (2-3 months)
Blockers: LinkedIn TOS, Legal risk
```

**Decision:** Do not build. High compliance risk and TOS violation.

---

## Feedback Analysis

### By Source

| Source | Count | Key Themes |
|--------|-------|------------|
| Delivery Blocker | 2 | Approval, Reply handling |
| Discovery Call | 1 | Lead prioritization |
| Customer Success | 2 | Portal, Reports |
| Renewal Reason | 1 | Weekly reports value |
| Churn Risk | 1 | Value visibility |
| Partner Feedback | 1 | White-label reports |
| Competitor Analysis | 1 | WhatsApp (not building) |
| Internal Request | 2 | LinkedIn (rejected), WhatsApp |

### By Module

| Module | Feedback Count | Priority |
|--------|---------------|----------|
| Control Room | 1 | P0 |
| Approval Queue | 1 | P0 |
| GTM Factory | 1 | P0 |
| Secure Portal | 1 | P1 |
| Weekly Reports | 2 | P1 |
| Renewal Engine | 1 | P1 |
| Reply Handling | 1 | P2 |
| WhatsApp OS | 1 | P3 |

---

## Recommendations

### Build Now
1. ✅ Control Room Dashboard (ICE: 90)
2. ✅ Approval Queue v1 (ICE: 81) - In progress
3. ✅ GTM Draft Factory (ICE: 72) - Start after Approval Queue

### Build Next
4. Weekly Reports v1 (ICE: 72)
5. Renewal Engine (ICE: 72)
6. Lead Scoring v1 (ICE: 56)
7. Client Secure Portal (ICE: 56)

### Backlog
8. Reply Classification (ICE: 42)

### Do Not Build
9. ❌ LinkedIn Automation (ICE: 7.5) - Rejected
10. ⏸️ WhatsApp (ICE: 15) - Deferred pending legal

---

## Next Steps

### This Week
- [ ] Complete Approval Queue
- [ ] Start Control Room requirements
- [ ] Finalize GTM Factory design

### Next Sprint
- [ ] Begin Control Room development
- [ ] Define Portal architecture
- [ ] Start Weekly Reports template

### Next Quarter
- [ ] Launch GTM Factory beta
- [ ] Pilot Portal with 3 customers
- [ ] Begin Renewal Engine development

---

## Appendix: Scoring Details

| Feature | Impact | Confidence | Ease | Risk | ICE Score |
|---------|--------|------------|------|------|-----------|
| Control Room | 10 | 9 | 5 | 2 | 90 |
| Approval Queue | 9 | 9 | 6 | 3 | 81 |
| GTM Factory | 9 | 8 | 4 | 4 | 72 |
| Weekly Reports | 9 | 8 | 6 | 2 | 72 |
| Renewal Engine | 9 | 8 | 6 | 3 | 72 |
| Lead Scoring | 8 | 7 | 6 | 3 | 56 |
| Client Portal | 7 | 8 | 4 | 4 | 56 |
| Reply Class. | 7 | 6 | 6 | 4 | 42 |
| WhatsApp | 6 | 5 | 2 | 8 | 15 |
| LinkedIn | 5 | 3 | 2 | 9 | 7.5 |

---

## _links

- Feature Data: `data/product/features.jsonl`
- Feedback Data: `data/product/feedback.jsonl`
- Feature Schema: `schemas/product_feature.schema.json`
- Product Strategy: `docs/product/PRODUCT_STRATEGY_AR.md`
- What Not to Build: `docs/product/WHAT_NOT_TO_BUILD_AR.md`
