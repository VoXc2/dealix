# Support Model — Dealix (AR)

---

## 1. Support Tiers

| Tier | Channel | Response | Resolution | Price |
|------|---------|----------|------------|-------|
| **Community** | Docs, academy, FAQ | Self-serve | Self-serve | Free |
| **Standard** | Email, portal | < 24 business hours | < 5 business days | Included |
| **Priority** | Email + WhatsApp business hours | < 4 business hours | < 24 business hours | Add-on |
| **Enterprise** | Dedicated channel + Slack/Teams | < 1 business hour | < 4 business hours (Sev1) | Premium |
| **Embedded** | Founder-attached, weekly sync | < 30 min | Same day | Custom |

## 2. Severity Levels

| Sev | Definition | Examples | Target response |
|-----|------------|----------|-----------------|
| Sev1 | Service down, multiple clients affected | API down, data corruption | < 1 hour |
| Sev2 | Major feature broken, single client | Approval flow stuck, AI not responding | < 4 hours |
| Sev3 | Minor issue, workaround exists | UI bug, slow report | < 1 business day |
| Sev4 | Cosmetic / enhancement | typo, color tweak | Next release |

## 3. Channels

- **Email:** `support@dealix.sa` (مُخطط)
- **Portal:** built-in ticket system (post-E3)
- **WhatsApp Business:** priority+enterprise (business hours)
- **Phone:** enterprise only

## 4. Hours

- **Standard:** Sun–Thu, 9:00–18:00 AST
- **Priority:** Sun–Thu, 9:00–18:00 AST (faster SLA)
- **Enterprise:** extended hours, on-call by agreement
- **Sev1:** 24/7 on-call (post-E3)

## 5. Escalation Path

```
L1 (Support) → L2 (Tech Lead) → L3 (Founder) → L4 (Outside expert)
```

كل escalation = audit row + client notification.

## 6. Client Responsibilities

- Provide accurate info on intake
- Test in sandbox before production
- Train internal users
- Report issues with context (logs, screenshots)
- Designate a primary contact

## 7. What We Don't Support

- ❌ Custom development for one client at expense of platform
- ❌ Ad-hoc consulting (delivered as paid engagements)
- ❌ Free training beyond academy content
- ❌ Integration with software we haven't vetted

## 8. Self-Service Resources

- `docs/academy/`
- `docs/ops/FOUNDER_OPERATING_SYSTEM_AR.md` (internal, but model helps clients)
- Help articles in portal (مُخطط)
- Video library (مُخطط، Agent 28)

## 9. SLAs (مبدئية — قابلة للتفاوض)

| Metric | Target |
|--------|--------|
| Uptime (E3+) | 99.5% monthly |
| API response (p95) | < 500ms |
| AI response (p95) | < 10s |
| Support response (Standard) | < 24h business |
| Incident post-mortem | within 5 business days |

## 10. Termination / Offboarding

- Data export قبل 30 يوم
- Audit log retention 90 يوم post-termination
- DPA obligations continue per its terms

---

> **Owner:** Founder + (يُعيَّن) Support Lead
