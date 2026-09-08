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
| oasdiff/oasdiff | OpenAPI breaking-change and changelog diffing between exact specs | local/CI evidence only; disable/untrust external refs by default; no runtime/API authority |
| open-policy-agent/conftest | policy tests against structured configuration files | static config verification only; must not become Dealix runtime policy/approval authority |
| cue-lang/cue | schema/config validation across JSON/YAML/TOML/OpenAPI/Protobuf | pilot only for a measured config-drift gap; no second configuration control plane |
| python-jsonschema/check-jsonschema | lightweight JSON Schema and GitHub-workflow/config validation | complement Spectral/actionlint only where schema validation adds unique signal |
| seddonym/import-linter | enforce Python architectural layer/import contracts | use to protect One-Company boundaries; report/test only, no code rewrite authority |
| webpro-nl/knip | find unused TypeScript/JavaScript files, dependencies and exports | report-only first; do not auto-delete application code |
| osprey-oss/deptry | detect unused/missing/transitive/mis-scoped Python dependencies | isolated current-project scan; no dependency mutation or auto-removal |
| jendrikseipp/vulture | detect likely dead Python code | report-only with confidence review; no automatic deletion |
| modelcontextprotocol/inspector | official MCP server testing/debugging via web/CLI/TUI | Dealix-owned/test MCP servers only; not a production proxy or security authority |
| pgtap/pgtap | PostgreSQL unit/assertion testing inside disposable test databases | never Production DB; complements real-Postgres acceptance, does not replace it |
| jtesta/ssh-audit | SSH server/client configuration and crypto audit | Dealix-owned host only, read-only evidence, no automatic hardening mutation |
| in-toto/in-toto | software supply-chain step/attestation integrity evidence | defer operational adoption until release execution plane stabilizes; not a signer/merge authority by itself |
| slsa-framework/slsa-github-generator | SLSA provenance generation in GitHub workflows | defer until trustworthy hosted Actions execution is restored; never use current blocked CI as provenance authority |
| pikepdf/pikepdf | deterministic QPDF-backed PDF read/write/repair/optimization utility | fallback only for low-level PDF cases not covered by pypdf/frontier parser stack; preserve MPL-2.0 obligations |
| ocrmypdf/OCRmyPDF | searchable-PDF OCR pipeline for scan-heavy documents | pilot only on public/authorized documents after language/model/dependency/license review; compare with PaddleOCR/Docling/MinerU |

## Replacement rule

A supplemental candidate may enter the ranked frontier only when:
1. a current ranked candidate is rejected/deferred for a documented measured-gap, duplication, license, security, data-boundary, or maintenance reason;
2. the replacement preserves ranks 51–100 and zero overlap with Top-50;
3. verifier/tests and license gates are updated in the same change;
4. only one benchmark is active;
5. `AUTO_INSTALL=false` remains true.

## Supplemental triage order

Do not benchmark this backlog in parallel. If a ranked candidate is rejected and a replacement is needed, prefer the smallest tool that closes the measured gap:

1. `oasdiff` for API breaking-change evidence after OpenAPI contract ownership is clear.
2. `import-linter` for architectural boundary enforcement if dependency drift threatens One-Company Law.
3. `deptry` or `knip` for dependency hygiene in the language where a concrete unused/missing-dependency problem is measured.
4. `mcp-inspector` for Dealix-owned MCP development/debugging when MCP metadata/tooling changes materially.
5. `pgTAP` only if SQL/database invariants are hard to prove through the existing Python + disposable-Postgres acceptance stack.
6. `ssh-audit` only as bounded read-only evidence for the Dealix VPS.
7. `in-toto` / SLSA provenance only after the release execution plane is trustworthy.
8. OCR/PDF fallback candidates only on a failing document corpus with ground truth.

## Explicit duplicate/control-plane rejection remains

Do not admit parallel Company Brain, CRM, scheduler/orchestrator, approval authority, consent authority, proof store, model router, or permanent agent fleet. Tools such as Temporal, Prefect, Airflow, LangChain/LlamaIndex-as-platform, Renovate beside Dependabot, another marketing CRM, another analytics authority, or another uptime/status truth store remain reject-by-default absent a future measured gap and architecture review.

`L5_EXECUTED=NONE`
