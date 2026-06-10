# Enterprise Risk Register Summary — Dealix (AR)

> نسخة مختصرة من risk register كاملة (في `docs/governance/RISK_REGISTER.md`).
> تُحدّث كل ربع سنة.

---

## Risk Scoring

- **L** = Likelihood (1–5)
- **I** = Impact (1–5)
- **Score** = L × I
- **Tier:** Low ≤ 6, Medium 7–12, High 13–19, Critical ≥ 20

## Top Enterprise Risks

| ID | Risk | L | I | Score | Tier | Owner | Mitigation |
|----|------|---|---|-------|------|-------|------------|
| R-E1 | Prompt injection bypasses controls | 3 | 5 | 15 | High | Founder + Agent 19 | Layered defense, allowlist, audit, red team |
| R-E2 | Secrets leak into LLM prompts | 2 | 5 | 10 | Med | Founder | Redaction middleware, schema validation |
| R-E3 | Data breach | 2 | 5 | 10 | Med | Security Officer | Encryption, access control, incident runbook |
| R-E4 | Untrained AI sends bad message | 2 | 4 | 8 | Med | Founder | Approval workflow, eval suite, opt-out |
| R-E5 | Outage longer than SLA | 2 | 4 | 8 | Med | Tech Lead | Backups, monitoring, DR plan |
| R-E6 | Vendor (LLM/email) outage | 3 | 3 | 9 | Med | Tech Lead | Fallback paths, multi-provider |
| R-E7 | Sub-processor DPA lapse | 2 | 4 | 8 | Med | Founder | DPA register, renewal alerts |
| R-E8 | Scope creep in pilot | 3 | 3 | 9 | Med | Delivery | Change control, SOW signoff |
| R-E9 | Champion turnover at client | 3 | 3 | 9 | Med | Account Lead | Multi-stakeholder, exec sponsor |
| R-E10 | PDPL non-compliance | 2 | 5 | 10 | Med | Privacy Officer | PDPL rules, data minimization, subject rights |
| R-E11 | Internal control weakness | 2 | 4 | 8 | Med | Founder | Audit log, segregation of duties, change control |
| R-E12 | Capacity bottleneck | 3 | 3 | 9 | Med | Tech Lead | Auto-scaling, capacity forecasts |
| R-E13 | Pricing leak / undercut | 2 | 3 | 6 | Low | Founder | Tiered pricing, NDA |
| R-E14 | Reputation damage from incident | 2 | 5 | 10 | Med | Founder | Incident response, comms plan |
| R-E15 | Currency / payment friction | 2 | 2 | 4 | Low | Ops | Moyasar + multiple rails |

## Risks by Category

### Security (R-E1, R-E2, R-E3)
- Layered defense (Agent 19 security framework)
- Continuous eval
- Pen-test roadmap

### Privacy (R-E10)
- PDPL program
- Data minimization
- Subject rights workflow

### Operational (R-E4, R-E5, R-E6, R-E11, R-E12)
- SLAs, SLOs
- Incident response
- DR planning
- Capacity forecasts

### Commercial (R-E8, R-E13)
- Change control
- Pricing discipline

### Reputational (R-E9, R-E14)
- Multi-stakeholder engagement
- Incident comms

## Risk Treatment

| Strategy | Used for |
|----------|----------|
| Avoid | R-E1 (auto-execute), R-E13 (price leak) |
| Mitigate | معظم المخاطر |
| Transfer | R-E14 (insurance مُخطط) |
| Accept | R-E15, R-E6 (vendor risk partial) |

## Risk Review Cadence

- **Weekly:** top 5 risks في founder review
- **Monthly:** كل risks في ops review
- **Quarterly:** تحديث كامل + Council review
- **Annually:** independent review (post-E4)

## Escalation Triggers

- Risk score changes by ≥ 3
- New risk identified at High or above
- Incident materializes a risk

---

> **Owner:** Founder + Council · **Review:** كل ربع سنة
> **Full register:** `docs/governance/RISK_REGISTER.md`
