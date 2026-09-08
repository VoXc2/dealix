# Dealix Delivery Substrate Catalog — 2026-09-08

Status: `SOLUTION_RESEARCH_NOT_CORE_DEPENDENCIES`.

Purpose: help Dealix solve customer problems through `BUILD / CONFIGURE_ADAPT / INTEGRATE / QUALIFIED_PARTNER / SUBCONTRACT / REFER / DECLINE` instead of assuming every requirement should become new Dealix core code.

## Non-duplication law

- These products/libraries are **customer-delivery substrates**, not a second Company Brain, CRM, data truth plane, scheduler, proof store or agent fleet.
- Do not install on Dealix Production merely because a customer solution may use them.
- Exact version, license, security posture, hosting/data boundary and commercial support must be reviewed per project.
- A successful technical pilot does not prove customer eligibility, procurement compliance, relationship, consent or award.

## 1. Data Office / governance / catalog / lineage

### DataHub — `datahub-project/datahub`
Candidate route: `INTEGRATE_EXISTING_PRODUCT / QUALIFIED_PARTNER`.

Useful when a customer needs a production-grade metadata catalog/context platform spanning discovery, governance, lineage, ownership, observability and AI-ready context across many data systems. Current upstream describes 80+ connectors, APIs/SDKs and Apache-2.0 open-source licensing.

Dealix role:
- discovery and source-system mapping;
- implementation/integration architecture;
- ownership/glossary/classification/data-product model;
- connector and lineage rollout;
- operating workflow, acceptance and proof;
- RAG/agent context integration where appropriate.

Do not position DataHub as Dealix Company Brain; it would be a customer-side data-governance substrate.

### OpenMetadata — `open-metadata/OpenMetadata`
Candidate route: `INTEGRATE_EXISTING_PRODUCT / QUALIFIED_PARTNER`.

Useful for metadata, lineage, data quality, governance, glossaries/classifications, data contracts, data products, semantic context, APIs/SDKs and MCP-enabled data context. Current upstream describes 130+ connectors and Apache-2.0 licensing.

Benchmark rule:
For a concrete Data Office requirement, compare **DataHub vs OpenMetadata** on the customer's actual systems, mandatory features, deployment model, Arabic/business glossary needs, NDMO/tender mapping, operating burden and support route. Admit one primary substrate for the project unless a measured integration boundary requires both.

### Existing Dealix components that complement either product
- Great Expectations / Pandera: data-quality contracts.
- OpenLineage candidate: execution lineage interoperability.
- pgvector + Ragas + Phoenix/Promptfoo: bounded RAG/evaluation path.
- Presidio: PII detection/redaction candidate.
- Docling/PaddleOCR/MinerU/Marker candidates: document intake, not metadata-catalog authority.

## 2. AI governance / ethics / fairness

### Fairlearn — `fairlearn/fairlearn`
Candidate route: `BUILD_DIRECT_COMPONENT / INTEGRATE_EXISTING_LIBRARY`.

Use for technical fairness assessment/mitigation where a model/use case and relevant groups/harms are explicitly defined. It can provide measurable fairness evidence; it is **not** a Saudi AI-governance authority or compliance certificate.

### AI Fairness 360 — `Trusted-AI/AIF360`
Candidate route: `PILOT_ALTERNATIVE`.

Use only when its metrics/mitigation set adds unique value beyond Fairlearn for the customer's model and governance plan. Avoid carrying two fairness stacks without a measured need.

### Existing Dealix governance/eval components
- SDAIA AI Ethics / Saudi Delivery Reference Map: regulatory/reference layer.
- Giskard / DeepEval / garak / PyRIT frontier: model/application evaluation and red-team evidence.
- Presidio / LLM Guard candidate: privacy/output scanning evidence.
- Probability/Truth Firewall / Proof Ledger: Dealix operating authority, not replaced by fairness libraries.

For HRDF-style AI governance work, the deliverable is primarily **governance operating design + policies/controls + lifecycle evidence + evaluation framework**; a fairness library is one technical instrument inside that program, not the offer itself.

## 3. FM / assets / field operations / IoT

### ThingsBoard — `thingsboard/thingsboard`
Candidate route: `INTEGRATE_EXISTING_PRODUCT / QUALIFIED_PARTNER`.

Apache-2.0 upstream IoT platform for device management, data collection, processing and visualization. Useful when an FM/industrial scope includes telemetry, meters, sensors, alarms or device-to-workflow integration.

Dealix role:
- integrate telemetry/events into work-order/exception/approval/proof flows;
- normalize data and escalation semantics;
- connect the chosen CAFM/CMMS/BMS/product to executive command and evidence;
- acceptance around SLA/event/work-order/proof outcomes.

ThingsBoard is **not a complete CAFM replacement by itself**.

### CAFM/CMMS route
For a tender requiring full facility, space, security, safety, asset and work-order management, Dealix should first perform a product/partner fit matrix rather than build an entire CAFM suite from scratch.

Required comparison dimensions:
- facility/space/asset/work-order/PPM scope;
- contractor/SLA/mobile/offline capabilities;
- BMS/IoT/GIS/ERP/identity integrations;
- Arabic/English UX;
- hosting/data-localization/security requirements;
- API/webhook/export contract;
- implementation partner capability in Saudi Arabia;
- licensing/TCO and support;
- tender compliance, references and acceptance evidence.

Candidate open-source/ERP-derived products may be researched, but restrictive licenses, support maturity and Saudi implementation capability must be reviewed before selection. Default route is `QUALIFIED_PRODUCT_PARTNER + DEALIX_INTEGRATION/PROOF` when that reduces delivery risk.

## 4. API / integration delivery

Use the existing or Frontier tools as evidence helpers:
- Schemathesis / Hurl / Playwright: runtime/API acceptance.
- Spectral + oasdiff supplemental: OpenAPI quality and breaking-change evidence.
- Pact Python / WireMock supplemental: consumer/provider contracts and failure/retry simulation.
- Testcontainers / Toxiproxy: disposable integration and failure-path tests.
- OpenTelemetry / Sentry / PostHog: existing observability authorities where applicable.

No new API gateway/service mesh is admitted by this catalog.

## 5. Document / RFP / evidence delivery

Canonical strategy:
1. native text/parser first;
2. Docling/current deterministic route;
3. one difficult-document benchmark if needed;
4. OCR only when scan quality requires it;
5. human review for low-confidence/legally material fields.

Candidate tools:
- MarkItDown: lightweight Office/document normalization.
- Docling: first-line structured document candidate.
- PaddleOCR: Arabic/English OCR fallback.
- MinerU / Marker: difficult-layout benchmark under license gates.
- CAMeL Tools: Arabic normalization/entity assistance.
- Gotenberg: isolated document/PDF rendering/conversion.
- pypdf/pdfplumber/pikepdf: deterministic low-level PDF operations.

`OCR_OUTPUT != VERIFIED_FACT` and `DOCUMENT_MENTION != BUYER_INTENT`.

## Top-3 application

### Imam Turki — Data Office / RAG / AI Agents
First substrate decision to test after eligibility:
`DataHub vs OpenMetadata` for catalog/governance/lineage/context + current Dealix RAG/eval stack for the AI layer. Do not prematurely build a custom catalog.

### HRDF — AI Governance & Ethics
Use Dealix governance operating model + Saudi reference map + bounded model/fairness/eval instruments. Do not sell a red-team/fairness library as a complete governance program.

### Eastern Province — Facility Management System
Prioritize proven CAFM/product/implementation partner selection. Use ThingsBoard only when IoT/telemetry integration is materially in scope. Dealix adds integration, governed workflow, command and proof.

## Promotion / project-cell rule

A delivery substrate enters a customer project only after:
1. mandatory requirement mapping;
2. Build/Integrate/Partner comparison;
3. license/security/data-boundary review;
4. project-specific benchmark/proof where needed;
5. commercial/support/partner route;
6. explicit customer-specific scope and exclusions;
7. exact material authority for commitments/deployment.

`CORE_DEALIX_INSTALL_AUTHORITY=false`
`CUSTOMER_DEPLOYMENT_AUTHORITY=false`
`PARTNER_RELATIONSHIP_NOT_INFERRED=true`
`L5_EXECUTED=NONE`
