# Dealix Capability Radar — Research Addendum — 2026-08-28

## Executive decision

Do **not** expand Dealix by installing popular infrastructure by default. The highest-value external capabilities are those that strengthen the existing Revenue Mesh / Company OS / verification spine without creating a second truth store, scheduler, agent fleet, CRM, observability backend, or model gateway.

North Star remains:

`REAL_INTERACTION -> VERIFIED_RELATIONSHIP -> QUALIFIED_PROBLEM -> DIAGNOSTIC -> DISCOVERY -> CUSTOMER_SPECIFIC_PILOT -> PAYMENT_PROOF -> DELIVERY_PROOF`

This addendum extends `CAPABILITY_RADAR_2026-08-28.md` with a researched second-pass shortlist.

---

## A. Schemathesis — `PILOT_ISOLATED`, likely `ADOPT_NOW_WITHIN_VERIFICATION_OWNER`

### Why it fits
Schemathesis generates property-based tests from OpenAPI/GraphQL schemas, checks server errors/schema violations/validation bypasses, and supports stateful multi-step workflows. Its CLI can be executed with `uvx`, which fits the existing Dealix decision to prefer isolated tooling.

### Dealix use
- API contract fuzzing for public/internal Dealix APIs in an isolated exact-head environment.
- Validate negative/edge cases that ordinary smoke tests may miss.
- Produce JUnit/reproducible failure receipts for sovereign verification.
- Use stateful workflows only against synthetic/non-production data.

### Guardrails
- never fuzz production write endpoints with real customer/payment credentials;
- no Railway/DNS/payment/GitHub-write secrets in the runner;
- sanitize generated/reproduction artifacts before persistence;
- a Schemathesis finding is a technical finding, not customer/business proof.

### Acceptance
One exact-head non-production run must find a seeded contract/validation defect and reproduce it deterministically before the tool becomes a standard gate.

References:
- https://github.com/schemathesis/schemathesis
- https://github.com/schemathesis/schemathesis/blob/master/docs/tutorials/cli.md

---

## B. Docling — `PILOT_ISOLATED`

### Why it fits
Docling parses PDF, DOCX, PPTX, XLSX, images and other formats into a unified structured document representation. This is directly useful for tenders, customer discovery material, proposal inputs, vendor documents and proof-pack source ingestion.

### Dealix use
- NELC/Etimad and other tender document extraction.
- Client-provided discovery packs and operating documents.
- Normalize tables/layout into structured source-bound evidence before Company Brain ingestion.
- Create a deterministic document manifest: source hash, document type, page/table provenance, extraction timestamp, parser version.

### Guardrails
- parsed content remains `SOURCE_MATERIAL`, never `FACT` solely because extraction succeeded;
- no private document is sent to a cloud parser without explicit data classification/approval;
- do not create a second vector database or memory store;
- preserve original file hash and page/table provenance for every extracted claim.

### Acceptance
Run against a synthetic/sample PDF + PPTX + XLSX pack and prove deterministic extraction of headings/tables plus source hashes. Keep only if it reduces manual tender/proposal preparation time measurably.

References:
- https://github.com/docling-project/docling
- https://docling-project.github.io/docling/usage/supported_formats/

---

## C. DuckDB — `ADOPT_NOW_AS_READ_ONLY_QUERY_LAYER`

### Why it fits
DuckDB is an in-process analytical SQL engine that reads CSV, JSON, Parquet and other formats directly. It can analyze Dealix receipts, proof artifacts, campaign/event exports and local economic evidence without deploying another database server.

### Dealix use
- query timestamped JSON/CSV/Parquet receipts;
- reconcile agent/workload cost/latency with verified commercial stage movement;
- analyze experiment/event/campaign outputs locally;
- generate compact founder scorecards from existing artifacts.

### Architectural rule
DuckDB is a **query layer only**, not a new source of truth. Canonical Company OS / Opportunity Graph / Proof Ledger ownership remains unchanged.

### Guardrails
- read-only by default over immutable/timestamped evidence paths;
- no customer PII replication into a new persistent database unless explicitly required;
- no long-running DuckDB server introduced;
- pin a stable 1.x release for any gate; do not adopt the preview 2.0 line as a dependency before its breaking-change surface is appropriate.

References:
- https://duckdb.org/
- https://duckdb.org/docs/current/data/json/overview
- https://duckdb.org/docs/current/guides/file_formats/query_parquet

---

## D. Firecrawl / firecrawl-agent — `DEFER`, then `PILOT_ISOLATED` only if research throughput becomes a proven bottleneck

### Why it is interesting
Firecrawl provides Search/Scrape/Crawl/Map/Parse/Interact primitives and an open-source research-agent stack. It can turn dynamic web pages and documents into clean context.

### Why not adopt now
Dealix already has web research paths and the current bottleneck is **verified relationships and commercial conversion**, not raw page retrieval. A new web-data credential/service and another autonomous web agent would add maintenance and compliance surface before proving incremental revenue value.

### Allowed future pilot
- public company/competitor/tender research only;
- no personal LinkedIn/social scraping or automated messaging;
- honor site/platform terms and data-classification rules;
- source URL + observed timestamp + extraction method required;
- research output remains `RESEARCH_ONLY` until independent evidence promotes it.

### Trigger to revisit
Revisit only when a measured account-research SLA or coverage problem cannot be solved with current search/browser tooling.

References:
- https://github.com/firecrawl/
- https://www.firecrawl.dev/
- https://www.firecrawl.dev/blog/firecrawl-agent-open-source

---

## E. MCP reference servers — `REFERENCE_ONLY`, not production dependencies

The official `modelcontextprotocol/servers` repository explicitly describes its servers as reference implementations/educational examples and warns developers to apply their own production threat model.

### Dealix rule
- use MCP reference servers to learn protocol patterns and test isolated integrations;
- never treat a reference server as production-ready merely because it is official;
- any production MCP adapter must have explicit tool allowlists, input validation, identity/auth, secret boundaries, rate limits, receipts and rollback semantics.

Reference:
- https://github.com/modelcontextprotocol/servers

---

## F. OpenTelemetry GenAI semantic conventions — strengthen the existing `PILOT_ISOLATED`

The GenAI semantic conventions have moved into a dedicated OpenTelemetry repository and now cover model, agent and MCP operations. The project still marks important areas as development/fast-moving.

### Dealix rule
Use the conventions as a vocabulary/schema influence for Dealix receipts first; do not couple core business truth to unstable telemetry field names.

Recommended stable Dealix-owned fields remain:
- `workload_id`
- `agent_role`
- `operation`
- `provider`
- `model`
- `duration_ms`
- `result_class`
- `retry_count`
- `fallback_count`
- `governance_block_class`
- `input_tokens` / `output_tokens` only when source-supported
- `verified_stage_movement_id` only when a real evidence event exists

References:
- https://github.com/open-telemetry/semantic-conventions-genai
- https://github.com/open-telemetry/semantic-conventions-genai/blob/main/docs/gen-ai/README.md

---

## G. Renovate — `REJECT_DUPLICATE_FOR_NOW`

Renovate is a strong dependency-update system with grouping, schedules, dashboards and merge-confidence features. However, Dealix already has GitHub dependency/security ownership and a known hosted Actions execution-plane problem. Adding a second dependency PR bot now creates noise without solving the execution-plane blocker.

### Revisit only if
- current dependency automation cannot group/schedule updates adequately;
- local/sovereign verification is stable enough to judge update PRs;
- a bounded trial shows materially lower founder maintenance time.

If revisited, use delayed/minimum-release-age policies and **never auto-merge** based solely on bot confidence.

References:
- https://github.com/renovatebot/renovate
- https://github.com/renovatebot/renovate/blob/main/docs/usage/upgrade-best-practices.md

---

## H. LiteLLM — `REJECT_DUPLICATE`

LiteLLM provides model gateway, routing, retries, budgets, rate limits and logging. Dealix already has a hybrid LLM router plus OpenClaw provider/fallback ownership. Adopting LiteLLM now would create a second model-routing authority and another credential/config surface.

Revisit only if the existing router fails a documented provider/budget/observability requirement that cannot be added safely in-place.

Reference:
- https://github.com/BerriAI/litellm

---

## I. Langfuse — `DEFER / REJECT_DUPLICATE_BY_DEFAULT`

Langfuse offers LLM tracing, latency/cost monitoring and prompt/response observability. Dealix already has receipts, PostHog for product/marketing telemetry, and a planned OpenTelemetry-compatible operational schema.

Do not add another observability database/UI until a measured debugging/trace gap remains after the lightweight receipt/OTel pilot. Prompt/response capture also increases privacy and secret/PII risk.

Reference:
- https://github.com/langfuse/langfuse

---

## J. Temporal — `REJECT_DUPLICATE`

Temporal is a mature durable-execution platform for long-running workflows and retry/recovery semantics. It is powerful, but Dealix already has systemd/Hermes/n8n/current queue/scheduler ownership. Introducing Temporal would create a second orchestration plane and migration burden.

Revisit only if a proven workflow durability requirement cannot be expressed by current owners and the migration has a quantified business case.

Reference:
- https://github.com/temporalio/temporal

---

## K. Browser-use — `REJECT_PRODUCTION_DUPLICATE`; Playwright remains preferred

Browser-use is powerful agentic browser automation, but its own production guidance highlights scalable browser infrastructure, fingerprinting/proxy/CAPTCHA considerations. Dealix already selected Playwright for deterministic QA and browser acceptance.

### Dealix rule
- keep Playwright as the committed/reproducible browser QA path;
- do not introduce browser-use as a production outreach/social automation layer;
- reconsider only for a specific internal browser task Playwright cannot reasonably cover.

Reference:
- https://github.com/browser-use/browser-use

---

## Revised adoption order

### Adopt / execute now
1. `uv` / `uvx` isolation policy.
2. OpenCode V2 `AGENTS.md` + explicit child-agent permissions.
3. DuckDB as a read-only local analytical query layer over existing evidence.
4. OSV normalization inside the existing security owner.

### Pilot in isolated environments
1. Schemathesis for API contract/property testing.
2. Docling for tender/customer-document normalization.
3. n8n MCP authoring against disabled/non-live workflows.
4. Playwright Test/MCP for #1298 deterministic public-surface QA.
5. OpenTelemetry GenAI-compatible receipt vocabulary.
6. Promptfoo only inside credential-scrubbed sandboxing.

### Defer until a measured blocker exists
1. Firecrawl / firecrawl-agent.
2. GitHub artifact attestations.
3. Langfuse.
4. Renovate.

### Reject duplicate by default
1. LiteLLM/model gateways while current router is healthy.
2. Temporal/new workflow engines.
3. new CRM/vector DB/agent framework/permanent agent fleet.
4. browser-use as a second production browser automation owner.

## Highest-value non-library finding

Repository review on current `main` found that `intelligence/negotiation_engine.py` still contains retired commercial language, including a **7-day pilot** response and outcome/ROI-style phrasing that can drift from the current canonical path:

`Free Mini Diagnostic -> Qualified Discovery -> Customer-Specific Quote -> 30-Day Revenue Command Pilot -> Proof -> Stop/Expand/Redesign`

This is higher priority than installing another library because it can cause an existing Dealix sales/negotiation agent to speak against current commercial authority.

Required closure should be owned by the existing Revenue Mesh / commercial-truth train, not by a new negotiation engine:
- quarantine retired 7-day/fixed-price/unsupported-outcome language;
- require current commercial authority before generating negotiation responses;
- require evidence refs for claims;
- distinguish `FACT / HYPOTHESIS / CUSTOMER_STATED / PROPOSAL_BOUND / APPROVED_COMMERCIAL`;
- named price, discount, contract, tender, payment/refund and other commitments remain specifically gated;
- add deterministic tests proving legacy commercial language cannot re-enter live negotiation output.

This P0 truth correction outranks additional capability acquisition.