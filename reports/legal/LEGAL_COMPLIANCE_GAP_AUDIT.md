# Agent #13 — Legal / Compliance Gap Audit

**Date:** 2026-06-03
**Auditor:** Agent #13 (Legal, Compliance, Contract Guard)
**Repository:** https://github.com/Dealix-sa/dealix

---

## 1. Executive Summary

`docs/legal/` has strong **document artifacts** (DPA, MSA, DPO, DSAR,
Sub-Processor, Compliance Certifications) and the founder risk register
is already in place. What is **missing** is the **operational handoff
machinery**: when does something need a lawyer/founder review, who
decides, and what is the trace? Agent #13 does **not** give legal advice
— it builds the **guardrails that route sensitive work to humans**.

## 2. Existing Legal/Compliance Inventory

| File | Purpose | Status |
| --- | --- | --- |
| `docs/legal/COMPLIANCE_CERTIFICATIONS.md` | PDPL, ZATCA, ISO, SOC 2 status | ✅ strong |
| `docs/legal/DPA_TEMPLATE_AR.md` | Data Processing Agreement template | ✅ strong |
| `docs/legal/DPA_PILOT_TEMPLATE.md` (in `docs/`) | Pilot DPA | ✅ |
| `docs/legal/ENTERPRISE_MSA_TEMPLATE.md` | Enterprise MSA | ✅ strong |
| `docs/legal/FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md` | Risk register + approval classes | ✅ strong |
| `docs/legal/DPO_APPOINTMENT_LETTER.md` | DPO appointment | ✅ |
| `docs/legal/DPO_APPOINTMENT_TEMPLATE.md` | DPO template | ✅ |
| `docs/legal/DSAR_RESPONSE_TEMPLATES.md` | DSAR response templates | ✅ |
| `docs/legal/SUB_PROCESSOR_NOTIFICATION_EMAIL.md` | Sub-processor notification | ✅ |
| `docs/PRIVACY_POLICY_v2.md` (in `docs/`) | Privacy policy v2 | ✅ |
| `docs/TERMS_OF_SERVICE_v2.md` (in `docs/`) | ToS v2 | ✅ |
| `docs/REFUND_POLICY.md` (in `docs/`) | Refund policy | ✅ |
| `docs/PARTNER_LEGAL_AGREEMENT.md` (in `docs/`) | Partner legal | ✅ |
| `docs/LEGAL_ENGAGEMENT.md` (in `docs/`) | Legal engagement | ✅ |
| `docs/LEGAL_FOUNDER_SELF_EXECUTION.md` (in `docs/`) | Founder legal self-execution | ✅ |
| `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md` (in `docs/`) | Cross-border transfer | ✅ |
| `docs/SECURITY_PDPL_CHECKLIST.md` (in `docs/`) | Security+PDPL | ✅ |
| `docs/PDPL_BREACH_RESPONSE_PLAN.md` (in `docs/`) | Breach response | ✅ |
| `docs/PDPL_DATA_SUBJECT_REQUEST_SOP.md` (in `docs/`) | DSAR SOP | ✅ |
| `docs/PRIVACY_PDPL_READINESS.md` (in `docs/`) | PDPL readiness | ✅ |
| `docs/DPA_DEALIX_FULL.md` (in `docs/`) | Full DPA | ✅ |
| `docs/COMMERCIAL_LAUNCH_MASTER_PLAN.md` (in `docs/`) | Commercial launch | ✅ |

## 3. Missing Operational Handoffs

| Missing | Why it matters |
| --- | --- |
| `docs/legal/LEGAL_REVIEW_POLICY_AR.md` | No trigger list for "when does this need a lawyer?" |
| `docs/legal/CONTRACT_HANDOFF_CHECKLIST_AR.md` | No handoff form to send to legal counsel |
| `docs/legal/COMMERCIAL_CLAIMS_REVIEW_AR.md` | No evidence tier for "is this claim safe to publish?" |
| `docs/legal/OUTBOUND_COMMUNICATION_COMPLIANCE_AR.md` | No pre-send compliance check |
| `docs/legal/PAYMENT_TERMS_REVIEW_AR.md` | No review of non-standard payment terms |
| `docs/legal/CASE_STUDY_PERMISSION_POLICY_AR.md` | No permission workflow for case studies |
| `docs/legal/CASE_STUDY_CONSENT_FLOW_AR.md` | No consent form template |
| `docs/legal/PARTNER_AGREEMENT_REVIEW_AR.md` | No partner agreement review checklist |
| `docs/legal/CLIENT_DATA_PROCESSING_CHECKLIST_AR.md` | No per-client data processing checklist |
| `docs/legal/CLAIMS_EVIDENCE_MATRIX_AR.md` | No claim ↔ evidence mapping |
| `schemas/legal_review.schema.json` | No machine-readable review record |
| `schemas/contract_handoff.schema.json` | No structured handoff |
| `schemas/case_study_permission.schema.json` | No permission record |
| `data/legal/contract_handoffs.jsonl` | No audit trail |
| `data/legal/legal_reviews.jsonl` | No review log |
| `data/legal/case_study_permissions.jsonl` | No permission log |
| `reports/legal/LEGAL_COMPLIANCE_REVIEW.md` | No synthesis report |
| `reports/legal/CONTRACT_HANDOFF_QUEUE.md` | No queue of pending handoffs |
| `reports/legal/CLAIMS_AND_CASE_STUDY_REVIEW.md` | No claims review log |
| `reports/legal/LEGAL_GUARD_FINAL_REPORT.md` | No agent final report |

## 4. High-Risk Claim Inventory (Spot Check)

The `FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md` already names "no-overclaim
register" as a control but does not enumerate the claims themselves. Agent
#13 will add an explicit claims register in `CLAIMS_EVIDENCE_MATRIX_AR.md`
covering:

- "نتائج مضمونة" / guaranteed outcomes → FORBIDDEN
- "ROI %" without scenario basis → requires founder + finance sign-off
- "أكبر في السعودية" / "first in KSA" → requires evidence + comparison date
- "آمن 100%" / security claims → requires evidence + PDPL sign-off
- "مدعوم من" / "backed by" without verifiable name → FORBIDDEN
- "معتمد" / "certified" without cert body → FORBIDDEN
- "تخفيض X%" without named baseline → requires evidence + baseline doc
- named case study without consent → requires `case_study_permissions.jsonl` entry
- hypothetical / composite case study → must be labeled "سيناريو افتراضي"
- sector-specific claims (e.g. "for healthcare only") → requires sector counsel

## 5. Recommendations

1. **Phase 1 priority:** `LEGAL_REVIEW_POLICY_AR.md` + the three checklist
   docs (`CONTRACT_HANDOFF_CHECKLIST_AR.md`, `CASE_STUDY_PERMISSION_POLICY_AR.md`,
   `PAYMENT_TERMS_REVIEW_AR.md`).
2. **Phase 2 priority:** schemas + JSONL files for audit trail.
3. **Phase 3 priority:** claims evidence matrix + consent flow.
4. **Phase 4:** final report with risk-weighted next actions.
