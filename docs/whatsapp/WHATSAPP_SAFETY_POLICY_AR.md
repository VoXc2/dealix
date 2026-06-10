# WhatsApp Safety Policy
## سياسة أمان WhatsApp

**Document Type:** Safety Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines safety requirements for all WhatsApp communications.

---

## 2. Core Principle

> **WHATSAPP IS USED ONLY AFTER CONSENT OR EXISTING RELATIONSHIP. NO COLD WHATSAPP EVER.**

---

## 3. Consent Requirements

### 3.1 Approved Consent Sources

WhatsApp may be used when ONE of the following exists:

| Source | Description | Evidence Required |
|--------|-------------|-------------------|
| Positive reply | Customer replied to outbound email | Email thread |
| Form submission | Customer submitted form requesting contact | Form record |
| Booking confirmed | Customer booked meeting | Calendly/booking record |
| Explicit consent | Customer explicitly agreed | Signed consent |
| Existing client | Active client relationship | Client record |

### 3.2 No Consent Scenarios (BLOCKED)

| Scenario | Status | Notes |
|----------|--------|-------|
| From purchased list | BLOCKED | No consent |
| From scraped data | BLOCKED | No consent |
| From prospect database | BLOCKED | Without contact initiated |
| Cold outreach | BLOCKED | Never allowed |

---

## 4. Safety Rules

### 4.1 Never in WhatsApp

| Item | Rule | Enforcement |
|------|------|-------------|
| API keys | NEVER | No exceptions |
| Secrets | NEVER | No exceptions |
| Credentials | NEVER | No exceptions |
| Payment links (without approval) | NEVER | Founder approval required |
| Contract terms | NEVER | Human handoff required |
| Legal advice | NEVER | Human handoff required |
| Guaranteed claims | NEVER | Claim safety applies |
| Pricing finalization | NEVER | Founder approval required |

### 4.2 Always in WhatsApp

| Item | Rule | Enforcement |
|------|------|-------------|
| Human handoff option | Always available | Button/template |
| "ما أعرف — اقترح علي" | Always offered | Prompt |
| Secure portal for files | Offered for sensitive content | Template |
| Logging | All messages logged | System |

---

## 5. Human Handoff Triggers

Human handoff is REQUIRED for:

| Topic | Handoff Required | Notes |
|-------|------------------|-------|
| Pricing finalization | YES | Founder or sales |
| Legal questions | YES | Legal review |
| Contract terms | YES | Legal review |
| Complaints | YES | Support team |
| Privacy/deletion requests | YES | Privacy team |
| Payment disputes | YES | Finance team |
| Low confidence | YES | Agent uncertainty |
| Sensitive data requests | YES | Data protection |
| Out of scope topics | YES | Human judgment |

---

## 6. Action Card Requirements

Every WhatsApp action card must include:

```yaml
card:
  type: recommendation | approval | permission | proposal
  title: "عنوان البطاقة"
  summary: "ملخص قصير"
  risk_level: low | medium | high
  evidence_level: L0-L5
  approval_required: true | false
  next_action: "الخطوة التالية"
```

**Note:** `risk_level` and `approval_required` are mandatory fields.

---

## 7. Related Documents

| Document | Purpose |
|----------|---------|
| `docs/whatsapp/WHATSAPP_CLIENT_OS_AR.md` | WhatsApp operating guide |
| `docs/whatsapp/WHATSAPP_POST_REPLY_FLOW_AR.md` | Post-reply flow |
| `WHATSAPP_CONSENT_CHECKLIST_AR_EN.md` | Consent checklist |

---

*Policy maintained by Agent #5 — Security Red Team*
