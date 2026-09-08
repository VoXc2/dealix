# Capability Frontier V2 — Supplemental Backlog

Status: `BACKLOG_ONLY_NOT_ADMITTED`.

Canonical ranked frontier remains `config/oss/capability_frontier_v2.tsv` (51–100). This file harvests useful candidates from overlapping expansion work without creating a second registry or raising the active frontier beyond 100.

## Candidates worth future substitution/admission if a ranked 51–100 item is rejected

| Candidate | Measured use | Boundary |
|---|---|---|
| axllent/mailpit | local SMTP capture and email integration testing without delivery | never production MTA or send authority |
| mjmlio/mjml | deterministic responsive-email rendering | draft/render only |
| domainaware/parsedmarc | parse DMARC reports once reports exist | evidence only; no marketing truth store |
| hadolint/hadolint | Dockerfile/static shell quality | lint only; no image-security authority |
| sbdchd/squawk | PostgreSQL migration lock/downtime linting | no DB mutation |
| aboutcode-org/scancode-toolkit | license/copyright/package provenance | evidence only; legal review separate |
| OWASP/wstg | versioned web/API security test reference | reference, not scanner authority |
| microsoft/markitdown | lightweight office/document-to-Markdown conversion | compare with Docling/Frontier parsers |
| CAMeL-Lab/camel_tools | Arabic morphology/dialect/NER preprocessing | bounded NLP utility, not business truth |
| gotenberg/gotenberg | containerized HTML/Office/Markdown to PDF and PDF utilities | isolated renderer; no customer publication authority |
| UKGovernmentBEIS/inspect_ai | reproducible model/tool-use evaluation | not a second agent framework |
| invariantlabs-ai/mcp-scan | MCP tool-metadata poisoning/shadowing risk checks | Dealix-owned MCP configs only |
| stoplightio/spectral | OpenAPI/JSON/YAML contract linting | not runtime gateway |
| pact-foundation/pact-python | consumer/provider API contracts | pilot one boundary first |
| wiremock/wiremock | deterministic provider failure/signature/retry simulations | local/test only |
| CISOfy/lynis | VPS hardening assessment | read-only/bounded; no auto-remediation |
| nabla-c0d3/sslyze | TLS/certificate protocol evidence | Dealix-owned endpoints only |
| lycheeverse/lychee | broken-link verification | bounded Dealix docs/public URLs only |

## Replacement rule

A supplemental candidate may enter the ranked frontier only when:
1. a current ranked candidate is rejected/deferred for a documented measured-gap, duplication, license, security, data-boundary, or maintenance reason;
2. the replacement preserves ranks 51–100 and zero overlap with Top-50;
3. verifier/tests and license gates are updated in the same change;
4. only one benchmark is active;
5. `AUTO_INSTALL=false` remains true.

## Explicit duplicate/control-plane rejection remains

Do not admit parallel Company Brain, CRM, scheduler/orchestrator, approval authority, consent authority, proof store, model router, or permanent agent fleet. Tools such as Temporal, Prefect, Airflow, LangChain/LlamaIndex-as-platform, Renovate beside Dependabot, or another marketing CRM remain reject-by-default absent a future measured gap and architecture review.

`L5_EXECUTED=NONE`
