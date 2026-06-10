# Business Claims Safety Policy
## سياسة أمان الادعاءات التجارية

**Document Type:** Safety Policy
**Version:** 1.0
**Owner:** Agent #5 — Security Red Team
**Last Updated:** 2026-06-03

---

## 1. Purpose

This policy defines safety requirements for commercial claims to prevent misrepresentation, false advertising, and compliance violations.

---

## 2. Forbidden Claims

### 2.1 Guaranteed Claims (BLOCKED)

| Claim Type | Examples | Reason |
|------------|----------|--------|
| Guaranteed revenue | "We guarantee X% revenue increase" | False advertising |
| Guaranteed sales | "Guaranteed sales growth" | False promise |
| 10x promises | "10x your results" | Exaggerated |
| Risk-free | "100% risk-free" | Cannot guarantee |
| "نضمن لك" | Any Arabic guarantee | False promise |

### 2.2 Misrepresentation (BLOCKED)

| Claim Type | Examples | Reason |
|------------|----------|--------|
| Fake results | "Client X increased 500%" (unverified) | False |
| Fake case studies | Named client with fabricated data | Fraud |
| Fake testimonials | Unverified customer quotes | Deceptive |
| Fake client names | "Our clients include X" (not true) | Fraud |

### 2.3 Unverified Compliance Claims (BLOCKED)

| Claim Type | Examples | Reason |
|------------|----------|--------|
| "100% compliant" | Without evidence | False claim |
| "GDPR certified" | Without certification | Fraud |
| "PDPL compliant" | Without documentation | Fraud |

---

## 3. Evidence Requirements

### 3.1 Evidence Levels

| Level | Definition | Use for Claims |
|-------|------------|----------------|
| L0 | Assumption | Internal only |
| L1 | Internal doc/template | Internal only |
| L2 | Test/script output | Demo, POC |
| L3 | Staging/demo signal | Marketing with caveat |
| L4 | Prospect engagement | Sales with evidence |
| L5 | Paid/revenue | Public case study |

### 3.2 Claim Approval Matrix

| Claim Type | Evidence Required | Approval |
|------------|-------------------|----------|
| General capability | L2 | No |
| Specific result | L3+ | Yes |
| Client reference | L4+ | Yes |
| Case study | L5 | Yes + permission |
| Named client | L5 | Yes + explicit permission |

---

## 4. Case Study Requirements

### 4.1 Truth Label

All case studies must include:
- Evidence level clearly stated
- Methodology explained
- Results contextualized
- Limitations acknowledged

### 4.2 Permission Requirements

| Element | Permission Required |
|---------|---------------------|
| Client name | Explicit written permission |
| Client logo | Written permission |
| Specific metrics | Verified data |
| Testimonial quote | Written quote |

---

## 5. Claim Review Process

```
Claim identified
     ↓
Evidence level assessed (L0-L5)
     ↓
Sufficient evidence? → No → Remove or cite
     ↓
Yes
     ↓
Permission obtained? → No → Anonymize or remove
     ↓
Yes
     ↓
Founder review
     ↓
Approved → Use with proper labeling
```

---

## 6. Implementation

### 6.1 Claim Safety Tests

```python
def test_no_guaranteed_revenue_claims():
    """Guaranteed revenue claims must be blocked."""
    claims = [
        "We guarantee 10x ROI",
        "Guaranteed sales increase",
        "Risk-free guarantee",
        "نضمن لك مبيعات",
    ]
    for claim in claims:
        result = audit_claim_safety(claim)
        assert result.suggested_decision == GovernanceDecision.BLOCK
```

---

## 7. Related Documents

| Document | Purpose |
|----------|---------|
| `CLAIMS_EVIDENCE_POLICY_AR.md` | Evidence requirements |
| `CASE_STUDY_TRUTH_POLICY_AR.md` | Case study rules |
| `claim_safety.py` | Implementation |

---

*Policy maintained by Agent #5 — Security Red Team*
