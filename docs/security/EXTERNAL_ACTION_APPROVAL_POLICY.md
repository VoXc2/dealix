# External Action Approval Policy
## سياسة موافقة الإجراءات الخارجية

**Document Type:** Security Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines which external actions require human (founder) approval before execution. External actions are operations that affect systems outside the Dealix repository or affect external parties (clients, partners, public).

---

## 2. Core Principle

> **ALL EXTERNAL ACTIONS REQUIRE HUMAN APPROVAL BY DEFAULT.**

---

## 3. Action Classification

### 3.1 Action Risk Levels

| Risk Level | Definition | Approval Required |
|------------|------------|-------------------|
| Low | Read-only operations, internal data processing | No approval (auto) |
| Medium | Internal writes, non-sensitive external reads | Human review |
| High | External sends, sensitive data access, production changes | Founder approval |
| Critical | Payment, legal, contract, secrets | Founder + legal review |

### 3.2 Action Categories

| Category | Risk Level | Examples |
|----------|------------|----------|
| Internal Read | Low | Read docs, query data, generate reports |
| Internal Write | Medium | Create drafts, update data, modify files |
| External Read | Medium | Fetch external data (via SSRF guard) |
| External Send | High | Email, WhatsApp, SMS, LinkedIn |
| Sensitive Access | High | PII, financial data, secrets |
| Production Deploy | Critical | Deploy to production |
| Payment | Critical | Generate payment links, process payments |
| Legal/Contract | Critical | Contract terms, legal agreements |
| Secret Access | Critical | API keys, credentials, tokens |

---

## 4. Approval Requirements Matrix

| Action | Risk | Approval Required | Approver | Notes |
|--------|------|-------------------|----------|-------|
| Draft email | Medium | No | — | Draft only |
| Send email | High | Yes | Founder | No cold outreach |
| Draft WhatsApp | Medium | No | — | Draft only |
| Send WhatsApp | High | Yes | Founder + Consent | No cold WhatsApp |
| LinkedIn action | High | BLOCKED | — | Never allowed |
| Scraping | High | BLOCKED | — | Unless approved source |
| CRM write | Medium | Yes | Human | Governance check |
| Generate proposal | Medium | No | — | Draft only |
| Send proposal | High | Yes | Founder | Proof pack required |
| Generate payment link | Critical | Yes | Founder | Terms required |
| Process payment | Critical | Yes | Founder | Legal review |
| Contract terms | Critical | Yes | Founder + Legal | Never autonomous |
| Code change (branch) | Medium | Yes | Human review | PR review |
| Deploy to staging | Medium | No | — | CI/CD gate |
| Deploy to production | Critical | Yes | Founder | Approval gate |
| Access PII | High | Yes | Founder | Lawful basis required |
| Modify PII | Critical | Yes | Founder | Data protection review |
| Delete data | Critical | Yes | Founder | Audit trail required |
| Access secrets | Critical | BLOCKED | — | Never in autonomous |
| Expose secrets | Critical | BLOCKED | — | Never |

---

## 5. Channel-Specific Rules

### 5.1 Email

| Action | Approval | Notes |
|--------|----------|-------|
| Generate draft | No | Draft only |
| Review draft | No | Review path |
| Send email | Yes (Founder) | Trust gate required |
| Cold email | Yes (Founder) | ICP verified + unsubscribe + evidence |
| Warm email | Yes (Founder) | Consent + relationship |
| Follow-up | Yes (Founder) | Original approved |

**Cold Email Requirements (in addition to approval):**
- [ ] ICP verified
- [ ] Unsubscribe mechanism present
- [ ] No guaranteed claims
- [ ] No fake Re:/Fwd:
- [ ] Evidence level L3+ for claims
- [ ] Personalization present
- [ ] Not on suppression list

### 5.2 WhatsApp

| Action | Approval | Notes |
|--------|----------|-------|
| Generate draft | No | Draft only |
| Send template | Yes (Founder + Meta) | Pre-approved template |
| Send session message | Yes (Founder + Consent) | Consent required |
| Cold WhatsApp | BLOCKED | Never allowed |

**WhatsApp Requirements (in addition to approval):**
- [ ] Explicit consent on record
- [ ] Not from cold/prospected list
- [ ] Not bulk messaging
- [ ] Template approved by Meta (for outbound)
- [ ] Human handoff for sensitive topics

### 5.3 LinkedIn

| Action | Approval | Notes |
|--------|----------|-------|
| Any automation | BLOCKED | Never allowed |

### 5.4 Production Deploy

| Action | Approval | Notes |
|--------|----------|-------|
| Deploy to staging | No | CI/CD gate |
| Deploy to production | Yes (Founder) | Approval gate in CI |
| Auto-deploy from PR | BLOCKED | No autonomous production deploy |
| Rollback | Yes (Founder) | Emergency exception possible |

---

## 6. Approval Workflow

### 6.1 Standard Approval Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                    ACTION TRIGGERED                              │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│                   RISK CLASSIFICATION                            │
│  Is this action in the HIGH/CRITICAL category?                   │
└─────────────────────────────────────────────────────────────────┘
                              │
              ┌───────────────┴───────────────┐
              ▼                               ▼
        ┌───────────┐                   ┌───────────┐
        │   LOW/    │                   │  HIGH/    │
        │  MEDIUM   │                   │ CRITICAL  │
        └───────────┘                   └───────────┘
              │                               │
              ▼                               ▼
        ┌───────────┐                   ┌─────────────────────────────────┐
        │   AUTO    │                   │ 1. LOG APPROVAL REQUEST        │
        │   ALLOW   │                   │ 2. NOTIFY FOUNDER               │
        └───────────┘                   │ 3. WAIT FOR APPROVAL            │
                                        │ 4. APPROVE → EXECUTE            │
                                        │    DENY → BLOCK + LOG           │
                                        └─────────────────────────────────┘
```

### 6.2 Approval Request Template

```yaml
approval_request:
  action: "send_email | deploy_production | generate_payment_link | ..."
  risk_level: "high | critical"
  requester: agent_name
  timestamp: ISO8601
  justification: "Why this action is needed"
  
  details:
    recipient: "Email/WhatsApp/number if applicable"
    content_summary: "What will be sent/deployed/done"
    evidence_level: "L0-L5"
    compliance_checks:
      - check_name: "result"
  
  approval_required_from: founder
  status: "pending | approved | denied"
  response_timestamp: ISO8601
  response_notes: "Founder notes"
```

---

## 7. Emergency Exception Protocol

In genuine emergencies (system down, security incident), founder may pre-approve categories:

1. Founder defines emergency scope
2. Actions within scope auto-approved
3. All actions logged with emergency flag
4. Post-incident review required
5. Documentation updated

---

## 8. Governance OS Integration

### 8.1 approval_matrix.py

```python
def approval_for_action(action: str) -> tuple[Risk, str]:
    a = action.lower().strip()
    if "whatsapp" in a or "cold_whatsapp" in a:
        return "high", "human+consent"
    if "linkedin" in a and "automation" in a:
        return "high", "blocked"
    if "send" in a and "email" in a:
        return "medium", "human"
    if "pii" in a or "personal" in a:
        return "high", "lawful_basis_required"
    if "publish" in a or "claim" in a:
        return "medium", "claim_qa"
    if "deploy" in a and "production" in a:
        return "critical", "founder"
    if "payment" in a or "contract" in a:
        return "critical", "founder+legal"
    return "low", "auto"
```

### 8.2 approval_policy.py

```python
class ApprovalRequirement:
    EXTERNAL_SEND = "external_send"        # Founder approval
    LEGAL_REVIEW = "legal_review"          # Legal review
    CONSENT_VERIFIED = "consent_verified"  # Channel consent
    EVIDENCE_LEVEL = "evidence_level"      # Evidence L3+
    ICP_VERIFIED = "icp_verified"          # ICP match
    SUPPRESSION_CHECK = "suppression_check" # Not on suppression list
```

---

## 9. Non-Negotiable Rules

1. **No cold WhatsApp ever** — BLOCKED regardless of approval
2. **No LinkedIn automation ever** — BLOCKED regardless of approval
3. **No auto-production-deploy from PR** — BLOCKED regardless of approval
4. **No secrets access in autonomous mode** — BLOCKED regardless of approval
5. **No cold email without ICP verified** — BLOCKED regardless of approval
6. **No guaranteed claims** — BLOCKED regardless of approval
7. **No pricing/payment without founder approval** — BLOCKED regardless of approval

---

## 10. Related Documents

| Document | Purpose |
|----------|---------|
| `approval_matrix.py` | Risk routing implementation |
| `WHATSAPP_SAFETY_POLICY_AR.md` | WhatsApp-specific rules |
| `OUTBOUND_SAFETY_POLICY_AR.md` | Outbound channel rules |
| `PAYMENT_HANDOFF_SECURITY_POLICY.md` | Payment-specific rules |
| `BUSINESS_CLAIMS_SAFETY_POLICY_AR.md` | Claim evidence rules |

---

*Policy maintained by Agent #5 — Security Red Team*
*Review required: Quarterly or after any policy violation*
