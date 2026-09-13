# Saudi AI Agent Readiness & Governance — Free Execution Diagnostic

Status: `CURRENT_INTERNAL_COMMERCIAL_ASSET`
Market: Saudi Arabia
Entry offer: `FREE_EXECUTION_DIAGNOSTIC`
Commercial authority: `DIAGNOSTIC -> QUALIFIED_DISCOVERY -> CUSTOMER_SPECIFIC_QUOTE`

## Purpose

Give a Saudi organization a fast, evidence-backed view of whether an AI-agent initiative is ready to move from interest to a bounded implementation without pretending that readiness, compliance, security, ROI, or production value has already been proven.

This diagnostic is intentionally vendor-neutral. It evaluates the operating conditions around an agentic use case before Dealix recommends build, integration, partner, defer, or stop.

## Why this exists now

Saudi official guidance has moved beyond generic AI awareness and explicitly discusses AI-enabled implementation models, including AI agents.

The CST Awareness Guide for AI Adoption in Technology Companies frames organizational readiness across five connected dimensions:

1. Context Readiness
2. Data Readiness
3. Infrastructure Readiness
4. Skills and Expertise Readiness
5. Organizational Culture Readiness

The National Cybersecurity Authority's 2026 AI Cybersecurity Guidelines consultation explicitly includes generative AI and agentic AI and organizes the security problem around four primary domains:

1. Cybersecurity Governance
2. Cybersecurity Defense
3. Cybersecurity Resilience
4. Third-Party Cybersecurity

Official references:
- CST AI adoption guide: https://www.cst.gov.sa/knowledge-center/reports/ai-adoption-guide-for-tech-companies
- CST launch notice: https://www.cst.gov.sa/en/media-center/news/N2026072701
- NCA AI Cybersecurity Guidelines consultation: https://nca.gov.sa/en/news/2354/

These sources are readiness/governance inputs, not a Dealix certification, legal opinion, regulatory attestation, or guarantee of compliance.

## Best-fit buyers / owners

Use role hypotheses only until a real interaction proves ownership.

- CEO / COO / General Manager: operating-value and governance owner
- CIO / CTO / Head of Digital: architecture and execution owner
- CISO / Cybersecurity: authority, control and third-party risk owner
- Head of Data / DMO: data authority, quality and provenance owner
- Product / Operations leader: workflow and acceptance owner
- Transformation / PMO: portfolio, dependency and rollout owner

## Best-fit triggers

Promote this diagnostic when there is evidence of at least one trigger:

- management wants to introduce AI agents into an internal workflow;
- a team is already using LLM tools without clear authority boundaries;
- an AI POC exists but production ownership, data access or acceptance is unclear;
- employees manually move information between systems and approvals;
- the organization wants Arabic/English knowledge automation or governed RAG;
- cyber, data, audit or third-party concerns are slowing AI adoption;
- multiple AI tools/providers exist without a single decision and evidence layer;
- a regulated or high-consequence process needs human approval and traceability.

Public evidence of a trigger remains `RESEARCH_ONLY` until a real interaction exists.

## Diagnostic truth boundary

This diagnostic may establish:
- observed current-state facts supplied or demonstrated by the customer;
- evidence gaps;
- use-case hypotheses;
- readiness risks;
- a bounded candidate workflow;
- a recommended next decision.

It must not establish without direct evidence:
- regulatory compliance;
- cybersecurity certification;
- production readiness;
- buyer intent;
- guaranteed ROI or savings;
- customer value;
- a fixed implementation price;
- a fixed implementation duration;
- permission to access systems or data.

## Evidence collection

Request the minimum evidence needed for the candidate workflow. Examples:

### Context
- target business outcome;
- current workflow and actors;
- current cycle time / backlog / error indicators if available;
- consequence of a wrong agent action;
- process owner and decision authority;
- current tools and integrations.

### Data
- systems of record;
- data classes and sensitivity;
- access-control model;
- Arabic/English content requirements;
- source quality and freshness;
- retention / residency / third-party constraints;
- provenance requirements.

### Infrastructure
- deployment constraints;
- identity / SSO / service-account model;
- API / integration availability;
- observability and logging;
- approved model/provider constraints;
- rollback and incident path.

### Skills & expertise
- workflow SME availability;
- data / platform / security ownership;
- evaluation capability;
- operational support ownership;
- vendor / partner dependencies.

### Culture & operating model
- human-approval expectations;
- change ownership;
- escalation path;
- acceptable autonomy level;
- audit / assurance expectations;
- adoption and training constraints.

## Cybersecurity overlay

Map evidence gaps to the four NCA AI-cyber domains without claiming formal compliance.

### Governance
Check:
- named system/business owner;
- approved use case and authority boundary;
- data classification;
- model/provider decision authority;
- acceptable autonomous actions;
- human override / kill path;
- third-party responsibility model.

### Defense
Check:
- identity and least privilege;
- secret handling;
- tool/API allowlists;
- prompt/input validation where applicable;
- output/action validation;
- data leakage controls;
- isolation between tenants/workloads;
- logging of tool calls and consequential decisions.

### Resilience
Check:
- failure modes;
- deterministic fallback / HOLD behavior;
- retry/idempotency boundaries;
- recovery and rollback;
- model/provider outage handling;
- audit evidence retained after failure;
- human escalation.

### Third party
Check:
- provider purpose and data handling;
- retention/training terms where relevant;
- subcontractor dependencies;
- cost/overage authority;
- API/service availability commitments;
- exit/reversibility path;
- evidence owner for changing provider terms.

## Agent-specific control questions

1. What exact actions may the agent take without a human?
2. Which actions require a human approval gate?
3. Which actions are always denied?
4. What is the canonical source of truth for each decision?
5. What happens when the source is missing, stale or conflicting?
6. Can a prompt/user/worker override model, data, cost or approval policy?
7. How is duplicate execution prevented?
8. Can one worker verify its own consequential output?
9. What evidence proves an action actually executed?
10. How is a bad release/model/tool rolled back?

## Readiness scoring

Use this score only as an internal diagnostic aid, never as a certification.

For each of the five CST readiness dimensions score:
- `0 = UNKNOWN / no usable evidence`
- `1 = MATERIAL_GAPS`
- `2 = BOUNDED_READY_WITH_CONTROLS`
- `3 = STRONG_EVIDENCED_READINESS`

Also classify each material risk:
- `BLOCKER`
- `CONTROL_REQUIRED`
- `EXPERIMENT_REQUIRED`
- `ACCEPTABLE_FOR_BOUNDED_PILOT`

Never average away a hard blocker. A single unresolved authority, sensitive-data, security, legal, access, rollback or ownership blocker can keep the recommendation at HOLD even when the numeric total is high.

## Output pack

Produce one concise evidence pack:

1. **Executive finding** — the highest-value use case and current decision state.
2. **Current workflow map** — people, systems, approvals and evidence points.
3. **Five-dimension readiness matrix** — CST-aligned.
4. **AI cybersecurity gap map** — NCA-domain aligned, non-certifying.
5. **Agent authority matrix** — ALLOW / HUMAN_APPROVAL / DENY.
6. **Data and provider boundary** — classification, residency/retention evidence gaps and allowed processing paths.
7. **Top failure modes** — consequence, detection, containment and rollback.
8. **Candidate bounded architecture** — source -> retrieval/tools -> agent -> approval -> system action -> receipt.
9. **Acceptance plan** — tests and evidence required before production value claims.
10. **Recommendation** — BUILD_DIRECT / ADAPT_EXISTING / INTEGRATE_EXISTING_PRODUCT / QUALIFIED_PARTNER / EXPERIMENT / HOLD / DECLINE.

## Optional Saudi operational wedges

Only apply when the customer's real workflow makes them relevant.

### ZATCA e-invoicing readiness
For a relevant notified taxpayer/workflow, inspect integration, reconciliation, exception handling and evidence around Phase Two/Fatoora readiness. ZATCA Wave 25 covers taxpayers whose VAT-subject revenue exceeded SAR 187,500 in 2022, 2023, 2024 or 2025 and requires notified Wave 25 entities to integrate by 1 February 2027.

Official source:
https://zatca.gov.sa/en/MediaCenter/News/Pages/Wave25-E-invoicing.aspx

Do not claim Dealix tax certification or presume that a researched entity is in the wave without entity-specific evidence/notification.

### Data-office / governed knowledge automation
When an organization has DMO, NDMO/NDI, enterprise knowledge, RAG or agent requirements, evaluate a bounded Dealix role around governed retrieval, Arabic/English knowledge automation, approval orchestration, provenance, evaluation and proof rather than pretending Dealix must replace the customer's DMO, SI or data platform.

## Conversion rule

The free diagnostic is complete when the evidence supports exactly one next decision:

- `NO_FIT / STOP`
- `HOLD_FOR_MISSING_EVIDENCE`
- `BOUNDED_EXPERIMENT`
- `QUALIFIED_DISCOVERY`

Only `QUALIFIED_DISCOVERY` may progress toward a customer-specific implementation/Outcome Sprint proposal. Scope, duration, price, provider/model, staffing, hosting, security obligations and acceptance criteria remain customer-specific.

## Dealix proof law

`DIAGNOSTIC != DISCOVERY`
`DISCOVERY != QUOTE`
`QUOTE != INVOICE`
`INVOICE != PAYMENT`
`PAYMENT != REVENUE`
`DELIVERY != CUSTOMER_VALUE`
`CUSTOMER_VALUE != PUBLIC_PROOF`
`POLICY_PASS != RUNTIME_CAPACITY`
`HTTP_200 != RELEASE_IDENTITY`

Every promotion requires the evidence for that state.