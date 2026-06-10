# Commercial Risk Register — سجل المخاطر التجارية
**Dealix — Agent #3**

> **الغرض:** كل المخاطر التجارية، severity، owner، mitigation، review cadence. مكمل لـ `dealix/transformation/risk_register.yaml` (existing).

---

## 1. Risk Categories

| Category | Description |
|----------|-------------|
| **Delivery risk** | Cannot deliver as promised |
| **Payment risk** | Client doesn't pay |
| **Privacy risk** | PDPL violation |
| **Reputation risk** | Brand damage |
| **Scope creep** | Uncontrolled expansion |
| **Unrealistic expectations** | Misaligned expectations |
| **Spam request** | Asked for spam behavior |
| **Legal/regulated claim** | Risky claim |
| **Low budget/high demand** | Scope vs price mismatch |
| **No decision maker** | Cannot close |
| **No data readiness** | Cannot implement |
| **Margin erosion** | Below margin floor |
| **Founder time** | Over capacity |
| **Channel risk** | Channel breaks |
| **Partner risk** | Partner damages brand |

---

## 2. Severity Levels

| Level | Impact | Action |
|-------|--------|--------|
| **Critical** | Business-ending | Immediate founder action |
| **High** | Major damage | Same-day action |
| **Medium** | Notable issue | Within week |
| **Low** | Minor issue | Track + mitigate |

---

## 3. The Risk Inventory

### 3.1 Delivery Risk
- **Severity:** High
- **Probability:** Medium
- **Trigger:** Scope unclear, client unavailable, data messy
- **Mitigation:** Scope review, change order, founder escalation
- **Owner:** Delivery Lead
- **Review:** Per delivery

### 3.2 Payment Risk
- **Severity:** High
- **Probability:** Low
- **Trigger:** Late payment, dispute
- **Mitigation:** Approval-first, terms clear, follow-up
- **Owner:** Billing Draft + Founder
- **Review:** Per payment

### 3.3 Privacy Risk (PDPL)
- **Severity:** Critical
- **Probability:** Low
- **Trigger:** Data mishandling, breach
- **Mitigation:** PDPL review, DPA, compliance
- **Owner:** Compliance + Founder
- **Review:** Per delivery

### 3.4 Reputation Risk
- **Severity:** Critical
- **Probability:** Low
- **Trigger:** Spam, fake claim, public failure
- **Mitigation:** No-spam policy, founder approval, crisis plan
- **Owner:** Founder
- **Review:** Continuous

### 3.5 Scope Creep
- **Severity:** Medium
- **Probability:** High
- **Trigger:** Client asks for more without change order
- **Mitigation:** Clear scope, change order process, founder discipline
- **Owner:** Delivery Lead + Founder
- **Review:** Per delivery

### 3.6 Unrealistic Expectations
- **Severity:** Medium
- **Probability:** High
- **Trigger:** Vague success metric, no discovery
- **Mitigation:** Discovery, success metric, evidence level
- **Owner:** Sales Lead + CS Agent
- **Review:** Per deal

### 3.7 Spam Request
- **Severity:** Critical
- **Probability:** Low
- **Trigger:** Client asks for spam behavior
- **Mitigation:** Hard disqualify, log
- **Owner:** Sales Lead
- **Review:** Per lead

### 3.8 Legal/Regulated Claim
- **Severity:** Critical
- **Probability:** Low
- **Trigger:** Client asks for risky claim
- **Mitigation:** Founder approval, legal review
- **Owner:** Founder + Legal
- **Review:** Per claim

### 3.9 Low Budget / High Demand
- **Severity:** Medium
- **Probability:** Medium
- **Trigger:** Want premium for low price
- **Mitigation:** Scope reduction, tier down, walk away
- **Owner:** Founder
- **Review:** Per deal

### 3.10 No Decision Maker
- **Severity:** Medium
- **Probability:** Medium
- **Trigger:** Champion can't close
- **Mitigation:** Identify DM, multi-stakeholder, walk away
- **Owner:** Sales Lead
- **Review:** Per deal

### 3.11 No Data Readiness
- **Severity:** Medium
- **Probability:** Medium
- **Trigger:** Client can't share data
- **Mitigation:** Readiness scan first, walk away if no data
- **Owner:** Sales Lead
- **Review:** Per deal

### 3.12 Margin Erosion
- **Severity:** High
- **Probability:** Medium
- **Trigger:** Discount, scope creep, custom at standard
- **Mitigation:** Guardrails, approval, scope review
- **Owner:** Founder
- **Review:** Per deal + monthly

### 3.13 Founder Time
- **Severity:** High
- **Probability:** Medium
- **Trigger:** Over capacity
- **Mitigation:** Hire, raise price, decline work
- **Owner:** Founder
- **Review:** Weekly

### 3.14 Channel Risk
- **Severity:** Medium
- **Probability:** Low
- **Trigger:** Channel breaks (DMARC, LinkedIn ban)
- **Mitigation:** Multi-channel, monitor, backup
- **Owner:** Founder
- **Review:** Weekly

### 3.15 Partner Risk
- **Severity:** Medium
- **Probability:** Low
- **Trigger:** Partner damages brand
- **Mitigation:** Approval, monitoring, termination
- **Owner:** Partner Channel Agent
- **Review:** Per partner

---

## 4. Risk Register Format

```yaml
- risk_id: "risk_001"
- category: "delivery"
- description: "Scope unclear, client unavailable"
- severity: high
- probability: medium
- impact: "Failed delivery, refund, reputation damage"
- trigger: "Client doesn't provide data"
- mitigation: "Scope review, change order, founder escalation"
- owner: "Delivery Lead"
- status: "open" # or "mitigated", "closed"
- created_at: "2026-06-03"
- updated_at: "2026-06-03"
- next_review: "2026-06-10"
```

---

## 5. Risk Review Cadence

| Severity | Review |
|----------|--------|
| Critical | Daily |
| High | Weekly |
| Medium | Monthly |
| Low | Quarterly |

---

## 6. Risk Response

### 6.1 Avoid
- Don't take the deal
- Don't enter the situation
- Best for high-severity

### 6.2 Mitigate
- Reduce probability or impact
- Best for medium severity

### 6.3 Transfer
- Insurance, contracts
- Best for specific risks

### 6.4 Accept
- Document and proceed
- Best for low severity

---

## 7. Risk Triggers

### 7.1 Immediate Action
- Spam request
- Privacy breach
- Payment dispute
- Public complaint
- Legal letter
- Founder burnout

### 7.2 Same-Day Action
- Major delivery issue
- High-severity risk
- Refund request
- Termination
- Crisis communication

### 7.3 Within-Week Action
- Medium risk
- Client concern
- Process issue
- Channel warning

---

## 8. The Top 5 Risks (Always Watch)

1. **PDPL violation** (Critical)
2. **Spam request accepted** (Critical)
3. **Margin erosion** (High)
4. **Founder burnout** (High)
5. **Delivery failure** (High)

---

## 9. Risk Owner

| Severity | Owner |
|----------|-------|
| Critical | Founder (only) |
| High | Founder + relevant lead |
| Medium | Relevant lead |
| Low | Anyone tracking |

---

## 10. Crisis Plan

### 10.1 PDPL Breach
1. Stop processing
2. Notify client
3. Notify authorities
4. Document
5. Mitigate
6. Review

### 10.2 Public Complaint
1. Acknowledge
2. Investigate
3. Respond publicly
4. Follow up privately
5. Document

### 10.3 Major Delivery Failure
1. Stop work
2. Founder outreach
3. Recovery plan
4. Refund consideration
5. Post-mortem

---

## 11. Companion Files

- Walk-away: `WALK_AWAY_RULES_AR.md`
- Bad-fit: `BAD_FIT_CLIENT_POLICY_AR.md`
- Scope: `SCOPE_CREEP_POLICY_AR.md`
- Existing: `dealix/transformation/risk_register.yaml`
- Existing: `auto_client_acquisition/governance_os/rules/`

---

**المخاطر = visibility. كل خطر = إجراء. founder يراقب، النظام يحمي، الـ crisis plan جاهز.**
