# AI Governance Program — Scope / النطاق

## Included / متضمَّن
- AI tool inventory (every model, vendor, internal agent in the customer's stack).
- Data inventory + ROPA-aligned mapping (data sources, categories, lawful basis).
- Saudi-specific risk assessment per business unit (PDPL + SAMA + NCA where applicable).
- AI usage policy authored bilingual (AR + EN) and reviewed by HoLegal.
- Approval matrix tuned to the customer's actions, roles, and evidence thresholds.
- Audit-trail blueprint + monthly evidence-pack template.
- Bilingual training (3 hours recorded): 1 hour staff, 1 hour managers, 1 hour board briefing.
- Stage-6 handoff session + evidence pack.
- 30-day post-handoff support window (one tuning round).

## Excluded (out of scope) / مستثنى
- Software development of new AI governance tools (this is policy + program work).
- DPO appointment or outsourced DPO service (separate engagement — see `docs/legal/DPO_APPOINTMENT_TEMPLATE.md`).
- Legal opinion (we draft; customer legal counsel approves).
- Live regulator inspection representation.
- Cross-jurisdictional governance beyond KSA (e.g., GDPR / DIFC) without a contracted addendum.
- Ongoing managed-service auditing (separate retainer).

## Customer responsibilities / مسؤوليات العميل
- Designate program sponsor (CTO / CIO / COO) and DPO contact.
- Provide read access to current AI tool / vendor list and data flow diagrams.
- Schedule interviews: 30 minutes per BU lead + 60 minutes per data-system owner.
- Review and sign-off on inventories within 5 business days of delivery.
- Provide regulator inspection history (if any) and known audit findings.

## Hard stops / حدود فاصلة
- Customer refuses to inventory a major AI tool or data flow -> scope flagged "partial coverage" on every deliverable, surfaced to the sponsor.
- Customer asks to ship without an approval matrix -> halt; the approval matrix is a non-negotiable program element.
- PDPL Art. 13/14 obligations cannot be met given current data practices -> halt and rescope with HoLegal involvement.
- Identified high risk has no mitigation within program budget -> escalate and renegotiate scope.

## Boundaries by tier / الحدود حسب الباقة
- **SME (SAR 35,000 / 1 month):** 1 BU, <= 20 AI tools, <= 5 data systems.
- **Mid-market (SAR 75,000 / 2 months):** <= 3 BUs, <= 75 AI tools, <= 20 data systems.
- **Enterprise (SAR 150,000 / 3 months):** multi-BU, > 75 AI tools, multi-jurisdiction language, board reporting cadence.

## Quality bar / مستوى الجودة
- Every inventory entry traceable to a source-of-truth and an owner.
- Every risk has a likelihood, impact (SAR), owner, and mitigation.
- Approval matrix maps to `dealix/trust/approval_matrix.py` enums.
- Audit blueprint produces a monthly evidence pack repeatably.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_governance_program/offer.md`
- AI tool inventory: `docs/services/ai_governance_program/ai_tool_inventory.md`
- Data inventory: `docs/services/ai_governance_program/data_inventory.md`
- Risk assessment: `docs/services/ai_governance_program/risk_assessment.md`
- Policy template: `docs/services/ai_governance_program/policy_template.md`
- Approval matrix: `docs/services/ai_governance_program/approval_matrix.md`
- Audit requirements: `docs/services/ai_governance_program/audit_requirements.md`
- Trust pack: `docs/trust/data_governance.md`
- Revenue OS policy rules: `docs/policy/revenue_os_policy_rules.md`
- Enterprise risk register: `docs/legal/enterprise_risk_register.md`
- Compliance OS module: `auto_client_acquisition/compliance_os/`
- Agent governance module: `auto_client_acquisition/agent_governance/`
