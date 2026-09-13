# Saudi AI Readiness Diagnostic Crosswalk — 2026

Status: `CURRENT_CANONICAL_INTERNAL_COMMERCIAL_ASSET`
Entry offer: `FREE_EXECUTION_DIAGNOSTIC`
Commercial path: `DIAGNOSTIC -> QUALIFIED_DISCOVERY -> CUSTOMER_SPECIFIC_QUOTE`

Purpose: turn current official Saudi AI-adoption, AI-cybersecurity and adjacent digital-integration evidence into one reusable, vendor-neutral **free diagnostic framework** for Dealix sector companies and arm pods. This document does not create buyer intent, relationship, consent, compliance certification, tax/legal advice, pipeline, quote, invoice, revenue or customer proof.

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
Current official dashboard reports broad AI-tool adoption in the Kingdom. Use that evidence only to justify market-level readiness research; it does not prove any named entity has an AI execution gap or buyer intent.

### NCA — AI Cybersecurity Guidelines public consultation
Published 2026-07-05; consultation deadline 2026-08-05. The document scope includes generative and agentic AI and is organized around four domains:

1. Cybersecurity governance
2. Cybersecurity defense
3. Cybersecurity resilience
4. Third-party cybersecurity

Official source: https://nca.gov.sa/en/news/2354/

Commercial interpretation: use these domains as **risk-discovery prompts**. The consultation is not treated as final binding regulation, certification or proof of Dealix compliance.

### ZATCA — Fatoora Wave 25 integration trigger
Published 2026-07-24. ZATCA states that Wave 25 of the e-invoicing Integration Phase covers notified taxpayers whose VAT-subject revenues exceeded **SAR 187,500** during 2022, 2023, 2024 or 2025, with integration to the Fatoora Platform required for notified taxpayers by **2027-02-01**. Phase Two adds platform integration, invoice-format and additional-field requirements beyond Phase One.

Official source: https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx

Commercial interpretation: this is a **workflow/integration-readiness trigger**, not proof that a company is in Wave 25, has received notice, is non-compliant, or needs Dealix. Use only after verifying entity-specific notification/obligation and current ZATCA requirements. Dealix does not provide tax/legal certification through this diagnostic.

## Best-fit trigger hypotheses

Promote this diagnostic only when there is evidence of at least one bounded trigger. Public evidence remains `RESEARCH_ONLY` until real interaction.

- management wants to introduce AI agents into an internal workflow;
- a team is already using LLM tools without clear authority boundaries;
- an AI POC exists but production ownership, data access or acceptance is unclear;
- employees manually move information between systems and approvals;
- Arabic/English knowledge automation or governed RAG is being considered;
- cyber, data, audit or third-party concerns are slowing AI adoption;
- multiple AI tools/providers exist without one decision/evidence layer;
- a regulated or high-consequence process needs human approval and traceability.

Likely owner roles are hypotheses until discovery proves them: CEO/COO, CIO/CTO, CISO, Head of Data/DMO, Product/Operations, Transformation/PMO.

## Free diagnostic research framework

### A. Business context and value
- Which workflow or decision is important enough to measure?
- What is the current baseline: time, errors, rework, delay, leakage or founder/manager minutes?
- What evidence would prove a useful outcome?
- What is the consequence of a wrong agent action?
- Where is human approval mandatory?
- Who owns the process and decision authority?

### B. Data readiness
- What data sources are required?
- Who owns them and what access is actually authorized?
- What data-quality gaps would invalidate automation?
- What is the sensitivity/classification of each input and output?
- What must remain private, local or redacted?
- What Arabic/English retrieval requirements exist?
- What provenance, freshness, retention or residency constraints apply?

### C. Infrastructure readiness
- What systems already exist: CRM, ERP, email, ticketing, BI, document stores, APIs?
- Can Dealix sit above them instead of replacing them?
- What identity/SSO/service-account model exists?
- What release identity, rollback, observability and backup evidence exists?
- What integration boundary can be tested without production mutation?
- What approved model/provider/deployment constraints exist?

### D. Skills and expertise readiness
- Who owns the business process?
- Who can verify output quality?
- Who can approve sensitive actions?
- Who owns data, security, platform and evaluation?
- Which tasks should remain deterministic or human-reviewed rather than model-driven?
- Which delivery dependencies require a qualified partner?

### E. Organizational culture and operating model
- What decisions are currently lost in chat/email/spreadsheets?
- How are approvals documented?
- What evidence is required before changing a workflow?
- What autonomy level is acceptable?
- What is the escalation path?
- What would make adoption reversible and low-risk?

### F. AI cybersecurity governance
- Is there a named owner for AI risk and approval authority?
- Are model/tool choices recorded with evidence and cost authority?
- Are external actions separated from analysis/drafting?
- Are secrets and customer data excluded from uncontrolled prompts?
- Is there an explicit human override / kill path?
- Are third-party responsibilities recorded?

### G. AI cybersecurity defense
- Are authentication, authorization, least privilege and audit controls defined?
- Are prompt/tool injection and unsafe tool-use paths bounded?
- Are software dependencies, model routes and external integrations inventoried?
- Are secrets isolated from workers and prompts?
- Are tool/API allowlists and action validation defined?
- Is tenant/workload isolation adequate for the proposed use case?

### H. AI cybersecurity resilience
- What happens when a model/provider/tool fails?
- Can the workflow fall back to deterministic/manual execution?
- Are retries bounded and idempotent?
- Is rollback tested rather than merely documented?
- Is evidence retained after failure?
- Is human escalation deterministic?

### I. Third-party AI risk
- Which model, SaaS, API, hosting and data processors are involved?
- What provider-side cost/data/retention authority is actually known?
- What contracts or customer-specific controls would be needed before production use?
- Can a local/private route reduce exposure for sensitive tasks?
- What is the exit/reversibility path if provider terms or availability change?

## Agent authority matrix

For every candidate agent workflow, answer explicitly:

1. What exact actions may the agent take without a human?
2. Which actions require a human approval gate?
3. Which actions are always denied?
4. What is the canonical source of truth for each decision?
5. What happens when the source is missing, stale or conflicting?
6. Can a prompt, worker, environment variable or provider default override model, data, cost or approval policy?
7. How is duplicate execution prevented?
8. Can one worker verify its own consequential output? It should not.
9. What receipt proves an action actually executed?
10. How is a bad release/model/tool rolled back or held?

Classify actions as:
- `ALLOW_BOUNDED`
- `HUMAN_APPROVAL_REQUIRED`
- `DENY`
- `UNKNOWN_HOLD`

## Readiness scoring and stop rule

Use scoring only as an internal diagnostic aid, never as certification.

For each CST readiness dimension:
- `0 = UNKNOWN / no usable evidence`
- `1 = MATERIAL_GAPS`
- `2 = BOUNDED_READY_WITH_CONTROLS`
- `3 = STRONG_EVIDENCED_READINESS`

Classify each material risk:
- `BLOCKER`
- `CONTROL_REQUIRED`
- `EXPERIMENT_REQUIRED`
- `ACCEPTABLE_FOR_BOUNDED_PILOT`

Never average away a hard blocker. Any unresolved authority, sensitive-data, security, legal, access, rollback, ownership, cost-authority or evidence-integrity blocker can keep the recommendation at HOLD even with a high numeric score.

## J. Saudi e-invoicing integration readiness — only when entity-specific relevance is verified
- Has the entity actually received a ZATCA Wave 25 or other integration notification, and is the notification evidence available?
- Which ERP/accounting/POS system is the source of invoice truth?
- Is the current invoice format/data model able to satisfy the applicable Phase Two fields and integration contract?
- Who owns certificate/credential handling and how are secrets isolated from automation agents?
- Is there a non-production Fatoora integration test path, retry/idempotence design, audit trail and rollback/continuity plan?
- What should remain deterministic and independently verified rather than model-driven?
- Which requirements need confirmation from the entity's tax/compliance advisor or current ZATCA materials before any production change?

## Output of the free diagnostic

Every sector-specific diagnostic derived from this crosswalk should produce:

1. Executive finding: highest-value use case and current decision state
2. Evidence collected vs assumptions still unverified
3. Current workflow map: people, systems, approvals and evidence points
4. Current-state baseline or explicit `BASELINE_NOT_PROVEN`
5. Five-dimension readiness matrix aligned to CST
6. Cybersecurity gap map aligned to NCA consultation domains where relevant
7. Agent authority matrix: ALLOW / HUMAN_APPROVAL / DENY / UNKNOWN_HOLD
8. Data/provider boundary and evidence gaps
9. Top failure modes with detection, containment, recovery and rollback
10. Three highest-value bounded opportunities
11. Candidate architecture: source -> retrieval/tools -> agent -> approval -> system action -> receipt
12. Acceptance plan and stop conditions
13. Delivery recommendation: `BUILD_DIRECT / ADAPT_EXISTING / INTEGRATE_EXISTING_PRODUCT / QUALIFIED_PARTNER / EXPERIMENT / HOLD / DECLINE`
14. Commercial next decision: `STOP / RESEARCH_MORE / DISCOVERY / CUSTOMER_SPECIFIC_QUOTE`

Only `DISCOVERY` may progress toward a customer-specific implementation/Outcome Sprint proposal. Scope, duration, price, provider/model, staffing, hosting, security obligations and acceptance criteria remain customer-specific.

## Sector adaptation rule

Do not maintain a separate diagnostic engine per sector. Reuse this canonical crosswalk and attach sector evidence, buyer roles, workflows, regulatory context and proof requirements from the live Dealix sector registry.

Examples:
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
- Diagnostic != discovery
- Discovery != quote
- Quote != invoice
- Invoice != payment
- Payment != revenue until evidence exists
- Delivery != customer value until accepted evidence exists
- Policy PASS != runtime capacity
- HTTP 200 != release identity

`EXTERNAL_EFFECT=NONE`
`PUBLIC_CLAIM_AUTHORITY=NONE`
`L5_EXECUTED=NONE`
