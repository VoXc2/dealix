# Saudi AI Readiness Diagnostic Crosswalk — 2026

Status: `RESEARCH_ONLY`

Purpose: turn current official Saudi AI-adoption, AI-cybersecurity and adjacent digital-integration evidence into a reusable **free diagnostic research framework** for Dealix sector companies and arm pods. This document does not create buyer intent, relationship, consent, compliance certification, tax/legal advice, pipeline, quote, invoice, revenue or customer proof.

## Current official evidence

### CST — AI adoption guidance for technology companies
Published 2026-07-27. The guide frames responsible AI adoption across internal operations, customer-facing solutions and AI-enabled implementation models including AI agents. It starts with organizational readiness across five dimensions:

1. Context readiness
2. Data readiness
3. Infrastructure readiness
4. Skills and expertise readiness
5. Organizational culture readiness

Official source: https://www.cst.gov.sa/en/media-center/news/N2026072701

Commercial interpretation: these dimensions are suitable as **diagnostic lenses**, not as proof that a specific company has a problem or intends to buy.

### CST — Saudi Internet Report 2025
Current official dashboard reports:
- 45.2% AI-tool adoption among internet users in the Kingdom;
- adoption more than doubled versus the previous year;
- 17.3% work-related AI-tool use;
- 13.5% programming/technical-task use.

Commercial interpretation: broad AI adoption is high enough to justify readiness/operationalization research, but the lower work/technical-use shares support a hypothesis that many organizations may still have an execution gap between experimentation and governed business use. This remains a hypothesis until customer-specific discovery.

### NCA — AI Cybersecurity Guidelines public consultation
Published 2026-07-05; consultation deadline 2026-08-05. The document scope includes generative and agentic AI and is organized around four domains:

1. Cybersecurity governance
2. Cybersecurity defense
3. Cybersecurity resilience
4. Third-party cybersecurity

Official source: https://nca.gov.sa/en/news/2354/

Commercial interpretation: use these domains as **risk-discovery prompts**. The consultation is not treated as final binding regulation, certification or proof of Dealix compliance.

### ZATCA — Fatoora Wave 25 integration trigger
Published 2026-07-24. ZATCA states that Wave 25 of the e-invoicing Integration Phase covers notified taxpayers whose VAT-subject revenues exceeded **SAR 187,500** during 2022, 2023, 2024 or 2025, with integration to the Fatoora Platform required for notified taxpayers by **2027-02-01**. ZATCA also notes that Phase Two adds integration, invoice-format and additional-field requirements beyond Phase One.

Official source: https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx

Commercial interpretation: this is a **workflow/integration-readiness trigger**, not proof that a company is in Wave 25, has received notice, is non-compliant, or needs Dealix. Use only after verifying the entity-specific notification/obligation and the current ZATCA requirements. Dealix does not provide tax/legal certification through this diagnostic.

## Free diagnostic research framework

### A. Business context and value
- Which workflow or decision is important enough to measure?
- What is the current baseline: time, errors, rework, delay, leakage or founder/manager minutes?
- What evidence would prove a useful outcome?
- Where is human approval mandatory?

### B. Data readiness
- What data sources are required?
- Who owns them and what access is actually authorized?
- What data-quality gaps would invalidate automation?
- What must remain private, local or redacted?

### C. Infrastructure readiness
- What systems already exist: CRM, ERP, email, ticketing, BI, document stores, APIs?
- Can Dealix sit above them instead of replacing them?
- What release identity, rollback, observability and backup evidence exists?
- What integration boundary can be tested without production mutation?

### D. Skills and expertise readiness
- Who owns the business process?
- Who can verify output quality?
- Who can approve sensitive actions?
- Which tasks should remain deterministic or human-reviewed rather than model-driven?

### E. Organizational culture and operating model
- What decisions are currently lost in chat/email/spreadsheets?
- How are approvals documented?
- What evidence is required before changing a workflow?
- What would make adoption reversible and low-risk?

### F. AI cybersecurity governance
- Is there a named owner for AI risk and approval authority?
- Are model/tool choices recorded with evidence and cost authority?
- Are external actions separated from analysis/drafting?
- Are secrets and customer data excluded from uncontrolled prompts?

### G. AI cybersecurity defense
- Are authentication, authorization, least privilege and audit controls defined?
- Are prompt/tool injection and unsafe tool-use paths bounded?
- Are software dependencies, model routes and external integrations inventoried?
- Is there a no-paid-spill / no-unknown-provider policy where needed?

### H. AI cybersecurity resilience
- What happens when a model/provider/tool fails?
- Can the workflow fall back to deterministic/manual execution?
- Are retries bounded and idempotent?
- Is rollback tested rather than merely documented?

### I. Third-party AI risk
- Which model, SaaS, API, hosting and data processors are involved?
- What provider-side cost/data/retention authority is actually known?
- What contracts or customer-specific controls would be needed before production use?
- Can a local/private route reduce exposure for sensitive tasks?

### J. Saudi e-invoicing integration readiness — only when entity-specific relevance is verified
- Has the entity actually received a ZATCA Wave 25 or other integration notification, and is the notification evidence available?
- Which ERP/accounting/POS system is the source of invoice truth?
- Is the current invoice format/data model able to satisfy the applicable Phase Two fields and integration contract?
- Who owns certificate/credential handling and how are secrets isolated from automation agents?
- Is there a non-production Fatoora integration test path, retry/idempotence design, audit trail and rollback/continuity plan?
- What should remain deterministic and independently verified rather than model-driven?
- Which requirements need confirmation from the entity's tax/compliance advisor or current ZATCA materials before any production change?

## Output of the free diagnostic

Every sector-specific diagnostic derived from this crosswalk should produce:

1. Executive summary of the workflow/problem hypothesis
2. Evidence collected vs assumptions still unverified
3. Current-state baseline or explicit `BASELINE_NOT_PROVEN`
4. Readiness gaps mapped to CST dimensions
5. Cybersecurity/risk questions mapped to NCA consultation domains where relevant
6. Saudi integration/compliance triggers mapped only where entity-specific applicability is independently verified
7. Three highest-value bounded opportunities
8. Quick wins that do not require production or L5 effects
9. A customer-specific Outcome Sprint hypothesis only if qualified discovery supports it
10. Acceptance criteria and stop conditions
11. Explicit next decision: STOP / RESEARCH_MORE / DISCOVERY / CUSTOMER_SPECIFIC_QUOTE

## Sector adaptation rule

Do not maintain a separate diagnostic engine per sector. Reuse this canonical crosswalk and attach sector evidence, buyer roles, workflows, regulatory context and proof requirements from the live Dealix sector registry.

Examples of sector adaptations:
- SaaS / technology: support, onboarding, renewals, product ops, internal knowledge workflows
- Financial services: approval evidence, model/tool governance, auditability, third-party risk
- Logistics/distribution: exception handling, partner onboarding, document flow, operating visibility
- Manufacturing/industrial: maintenance knowledge, work-order evidence, procurement/admin workflows
- Healthcare/life sciences: governed non-clinical operational workflows, evidence and access boundaries
- Government/semi-government: procurement/readiness, evidence trails, data governance and partner-first delivery where prime eligibility is unproven
- VAT-registered businesses with independently verified ZATCA integration scope: invoice-system readiness, deterministic integration controls, credential isolation, non-production testing and evidence trails

## Truth firewall

- Research != relationship
- Public signal != buyer intent
- Public contact != consent
- Diagnostic != customer proof
- Demo/synthetic != customer outcome
- Consultation != final binding regulation
- Design alignment != certification/accreditation
- Public ZATCA wave criteria != proof an entity is notified or non-compliant
- Diagnostic != tax/legal advice or compliance certification
- Quote != invoice
- Invoice != payment
- Payment != revenue until evidence exists
- Delivery != customer value until accepted evidence exists

`EXTERNAL_EFFECT=NONE`
`PUBLIC_CLAIM_AUTHORITY=NONE`
`L5_EXECUTED=NONE`
