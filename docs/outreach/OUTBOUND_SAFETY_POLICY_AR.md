# Outbound Safety Policy
## سياسة أمان الاتصالات الخارجية

**Document Type:** Safety Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines safety requirements for all outbound communications (email, WhatsApp, SMS, LinkedIn) to prevent unauthorized sends, spam, and compliance violations.

---

## 2. Core Principle

> **ALL OUTBOUND COMMUNICATIONS REQUIRE HUMAN APPROVAL. NO AUTONOMOUS SENDS.**

---

## 3. Channel Rules

### 3.1 Email

| Action | Allowed? | Requirements |
|--------|----------|--------------|
| Generate draft | Yes | Draft only |
| Send cold email | Yes (with approval) | ICP verified, unsubscribe present, no guaranteed claims |
| Send warm email | Yes (with approval) | Consent on record, relationship exists |
| Send follow-up | Yes (with approval) | Original approved |

**Cold Email Requirements:**
- [ ] ICP verified (company matches target profile)
- [ ] Unsubscribe mechanism present
- [ ] No guaranteed claims (revenue, sales, ROI)
- [ ] No fake Re:/Fwd:
- [ ] Evidence level L3+ for claims
- [ ] Personalization present
- [ ] Not on suppression list
- [ ] SPF, DKIM, DMARC configured
- [ ] Founder approval obtained

### 3.2 WhatsApp

| Action | Allowed? | Requirements |
|--------|----------|--------------|
| Generate draft | Yes | Draft only |
| Send template | Yes (with approval + Meta) | Pre-approved template, consent |
| Send session message | Yes (with approval + consent) | Explicit consent on record |
| Cold WhatsApp | **BLOCKED** | Never allowed regardless of approval |

**WhatsApp Requirements:**
- [ ] Explicit consent on record (reply/form/booking/client)
- [ ] Not from cold/prospected list
- [ ] Not bulk messaging
- [ ] Human handoff for sensitive topics
- [ ] No API keys or secrets shared

### 3.3 LinkedIn

| Action | Allowed? | Requirements |
|--------|----------|--------------|
| Any automation | **BLOCKED** | Never allowed |
| Manual connection (founder) | Founder discretion | Personal responsibility |

### 3.4 SMS

| Action | Allowed? | Requirements |
|--------|----------|--------------|
| Any automated SMS | **BLOCKED** | Saudi CITC regulations |

---

## 4. Trust Gates

Before any outbound send:

| Gate | Check | Required |
|------|-------|----------|
| Consent gate | Explicit consent on record | Yes |
| ICP gate | Company matches ICP | Yes (cold) |
| Unsubscribe gate | Unsubscribe mechanism present | Yes (email) |
| Suppression gate | Not on suppression list | Yes |
| Evidence gate | Evidence level sufficient | Yes |
| Claim gate | No guaranteed claims | Yes |
| Approval gate | Founder approval obtained | Yes |

---

## 5. Deliverability Requirements

### 5.1 Email Deliverability

| Requirement | Standard |
|-------------|----------|
| SPF | Valid record required |
| DKIM | Valid record required |
| DMARC | Policy configured |
| Unsubscribe header | List-Unsubscribe required |
| Daily cap | Based on domain reputation |

### 5.2 Implementation

See `test_engine12_security_v1.py` for email deliverability tests:
- SPF validation
- DKIM validation
- DMARC policy check
- Unsubscribe header check

---

## 6. Forbidden Practices

| Practice | Reason |
|----------|--------|
| Fake Re:/Fwd: | Misleading |
| Purchased lists | No consent |
| Missing unsubscribe | Compliance violation |
| Guaranteed claims | False advertising |
| Cold WhatsApp | No consent |
| LinkedIn automation | Against ToS |
| Purchased followers | Fake engagement |
| Misleading subject lines | Spam |

---

## 7. Related Documents

| Document | Purpose |
|----------|---------|
| `COLD_EMAIL_TRUST_GATE_AR.md` | Cold email specific rules |
| `DELIVERABILITY_SAFETY_GATE_AR.md` | Email deliverability |
| `SUPPRESSION_ENFORCEMENT_POLICY_AR.md` | Suppression list management |
| `WHATSAPP_SAFETY_POLICY_AR.md` | WhatsApp specific rules |

---

*Policy maintained by Agent #5 — Security Red Team*
