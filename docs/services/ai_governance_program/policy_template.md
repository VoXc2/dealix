# AI Governance Program — AI Usage Policy Template / قالب سياسة استخدام الذكاء الاصطناعي

Week-2 to Week-8 deliverable. Owner: HoLegal + customer's HoLegal/DPO. Output: a bilingual AI usage policy (12–25 pages) the customer can publish internally and reference in MSAs/DPAs. The template below is the scaffold; final wording is co-authored.

## 1. Preamble / تمهيد
- Customer's commitment to responsible AI in line with Saudi Vision 2030 and PDPL.
- Scope: every AI tool, model, and agent listed in `ai_tool_inventory.md`.
- Effective date, version, review cadence (default: every 6 months).

## 2. Definitions / تعاريف
- AI tool, foundation model, agent, RAG, sub-processor, evidence level, approval matrix.
- Bilingual canonical terms (AR + EN) — terminology is binding.

## 3. Lawful Basis & Transparency / الأساس القانوني والإفصاح (PDPL Art. 5, 13, 14)
- Article-5 lawful basis recorded for every data processing activity (cross-link `data_inventory.md`).
- Article-13 transparency notices used whenever personal data is collected.
- Article-14 explicit consent required for identifiable or sensitive PII.
- Right-to-erasure SLA: < 72 hours.

## 4. Acceptable Use / الاستخدام المسموح
- Permitted use cases per BU (whitelist).
- Prohibited use cases (blacklist): autonomous customer-facing send without approval, decisions in employment/credit without human review, scraping personal data, deepfake creation, model-output passed as human-only work in regulated reports.
- Bring-your-own-AI rule: any new tool routes through the approval matrix BEFORE use.

## 5. Data Handling / التعامل مع البيانات
- PII redaction rules: every input through `dealix/trust/pii_detector.py`.
- Storage residency: KSA-resident by default; cross-border requires explicit approval.
- Retention: tied to `docs/DATA_RETENTION_POLICY.md`.
- Sub-processor disclosure obligations.

## 6. Approval Matrix / مصفوفة الموافقات
- Every action with external side-effect routes through the approval matrix in `approval_matrix.md`.
- Evidence-level thresholds per action type (matches `dealix/trust/approval_matrix.py`).
- Override rules: only HoLegal + CEO can override; logged with reason.

## 7. Model Safety / سلامة النموذج
- "No source = no answer" required for any RAG-based customer-facing assistant.
- Prompt-injection mitigations.
- Hallucination guardrails: confidence + citation surfaced to the user.
- Forbidden-claims auto-check (`dealix/trust/forbidden_claims.py`).

## 8. Human Oversight / الإشراف البشري
- No fully autonomous outbound action in scope of this policy (initial posture).
- Tier-1 human review for any customer-facing AI output until evidence levels mature.
- Suggested-replies-only standard for support-desk use cases (cross-link AI Support Desk service docs).

## 9. Audit & Evidence / المراجعة والأدلة
- Immutable audit log for every AI invocation (`dealix/trust/audit.py`).
- Monthly evidence pack per `audit_requirements.md`.
- Regulator-inspection-ready dossier kept for 13 months minimum.

## 10. Incident Response / الاستجابة للحوادث
- AI-related incident classification.
- Notification timelines: NDMO within 72 hours where PDPL applies.
- Coordination with `docs/PDPL_BREACH_RESPONSE_PLAN.md` and `docs/trust/incident_response.md`.

## 11. Training & Awareness / التدريب
- Mandatory bilingual training for every employee using AI tools.
- Annual refresh; new-hire onboarding within 30 days.

## 12. Vendor Management / إدارة الموردين
- DPA required for every vendor in `ai_tool_inventory.md`.
- Sub-processor list maintained and published.
- Vendor renewal review against this policy.

## 13. Roles & Responsibilities / الأدوار والمسؤوليات
- CEO: ultimate accountability.
- DPO: PDPL compliance owner.
- CTO/CIO: technical controls owner.
- HoLegal: policy author + review.
- BU heads: use-case accountability.

## 14. Review & Amendment / المراجعة والتعديل
- Reviewed every 6 months.
- Amended on material change (new regulation, new AI tool class, major incident).
- Approved by board for enterprise tier.

## 15. Appendices / الملاحق
- A. Acceptable-use checklist (signable).
- B. Approval matrix snapshot.
- C. Standard AR + EN PDPL Art. 13/14 footers.
- D. Incident-reporting form.

## Cross-links / روابط ذات صلة
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Audit requirements: `docs/services/ai_governance_program/audit_requirements.md`
- Revenue OS policy rules: `docs/policy/revenue_os_policy_rules.md`
- Approval matrix engine: `dealix/trust/approval_matrix.py`
- PDPL readiness: `docs/PRIVACY_PDPL_READINESS.md`
- Data retention policy: `docs/DATA_RETENTION_POLICY.md`
- PDPL breach response: `docs/PDPL_BREACH_RESPONSE_PLAN.md`
- Trust pack — data governance: `docs/trust/data_governance.md`
- Enterprise risk register: `docs/legal/enterprise_risk_register.md`
