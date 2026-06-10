# Cold Email Trust Gate
## بوابة الثقة للبريد الإلكتروني البارد

**Document Type:** Safety Gate
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This document defines the trust gate that must pass before any cold email can be sent.

---

## 2. Trust Gate Checklist

### 2.1 Pre-Draft Gates

| Gate | Description | Pass/Fail |
|------|-------------|-----------|
| ICP Match | Company matches Dealix ICP | Required |
| Not on suppression | Not on suppression list | Required |
| Evidence level | Evidence level L3+ for claims | Required |

### 2.2 Draft Review Gates

| Gate | Description | Pass/Fail |
|------|-------------|-----------|
| Unsubscribe present | Working unsubscribe link | Required |
| No guaranteed claims | No "guaranteed", "10x", "risk-free" | Required |
| No fake Re:/Fwd: | No deceptive threading | Required |
| Personalization | Company-specific personalization | Required |
| Evidence cited | Claims supported by evidence | Required |
| No spam language | No spam trigger words | Required |
| Appropriate tone | Sector-appropriate language | Required |
| Length | Under 150 words | Recommended |

### 2.3 Approval Gates

| Gate | Description | Pass/Fail |
|------|-------------|-----------|
| Founder approval | Founder has reviewed and approved | Required |
| Evidence attached | Evidence level documented | Required |

---

## 3. Implementation

### 3.1 Draft Generation

Draft can be generated automatically if all pre-draft gates pass.

### 3.2 Send Status

```
Draft Status: PASS (all pre-draft gates pass)
Send Status: FAIL (approval gates not yet passed)

To achieve send-ready status:
1. Founder reviews draft
2. Founder approves
3. All gates pass
4. Send authorized
```

---

## 4. Related Documents

| Document | Purpose |
|----------|---------|
| `OUTBOUND_SAFETY_POLICY_AR.md` | General outbound policy |
| `SUPPRESSION_ENFORCEMENT_POLICY_AR.md` | Suppression list |

---

*Gate maintained by Agent #5 — Security Red Team*
