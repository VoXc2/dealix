# Dealix Capability Frontier V2 — Unique Harvest

Date: 2026-09-08
Canonical frontier owner: PR #1580

## Purpose

Preserve useful, non-duplicative findings discovered in concurrent capability-expansion lanes without creating a second capability registry or a second control plane.

This document is an **annex/backlog**, not an installation list and not an authority surface.

Permanent rules:

- `AUTO_INSTALL=false`
- `MAX_ACTIVE_BENCHMARKS=1`
- ONE Company Machine / Brain / Scheduler / Model Router / Approval / Consent / Proof authority.
- Exactly five permanent agents: `dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer`, `dealix-content`.
- Tool discovery != admission != production deployment.
- External send, publish, payment, merge, deploy, DNS, production DB, secrets and identity remain exact action-bound material actions.

## Unique candidates harvested from concurrent expansion work

These items are intentionally kept outside the canonical ranks 51–100 until a measured gap admits a next-frontier rank. They must not be installed in bulk.

### TRUST / release reliability

- **ShellCheck** — bounded static analysis for Bash/sh installers, acceptance runners and VPS control scripts.
- **Hadolint** — Dockerfile linting; pilot only if it adds signal beyond existing Docker/build checks.
- **Squawk** — PostgreSQL migration safety linting for locking/downtime hazards before isolated acceptance.
- **lychee** — bounded broken-link verification for repository docs and Dealix-owned public surfaces.
- **SSLyze** — TLS/certificate/protocol evidence for Dealix-owned endpoints only.
- **Lynis** — read-only VPS hardening assessment normalized into the existing TRUST proof lane; never automatic remediation.
- **OpenSSF Scorecard** — read-only upstream/repository security-practice evidence for dependencies and partner OSS; use as one evidence source, never as automatic admission or rejection authority.
- **Sigstore cosign** — candidate for signing/verifying Dealix-built container/artifact provenance after a measured release-integrity gap; signing-key/identity setup is a separate material authority surface and must not be auto-created.
- **in-toto Attestations** — candidate standard for verifiable build/test/release claims feeding the existing Dealix Proof model; do not create a second proof store or treat attestation presence as deployment correctness.
- **GUAC** — candidate graph for correlating SBOM/provenance/vulnerability evidence only if current Syft/OSV/Grype receipts become too fragmented; it must not become a second Company Graph or operational source of truth.

### GitHub Actions execution-plane recovery

- **nektos/act** is already represented in the canonical frontier. It is suitable only as non-authoritative local workflow rehearsal while GitHub-hosted execution is blocked; local PASS != GitHub-hosted PASS.
- **Self-hosted GitHub runner** — architecture option, not an auto-install candidate. It can avoid hosted-minute consumption, but registration tokens, repository access, patch execution and persistent runner security make activation a separately reviewed infrastructure/identity action. Prefer ephemeral/isolated execution if ever adopted.

### Email trust / test-only delivery quality

- **checkdmarc** is already represented in the canonical frontier; retain it as read-only sender health evidence only.
- **parsedmarc** — parse DMARC reports after reports exist; no second marketing/customer truth store.
- **Mailpit** — local/test SMTP sink for templates, MIME, attachments and retry behavior with zero external send.
- **MJML** — responsive HTML-email rendering for draft/testing lanes only.

### Saudi Arabic and document intelligence

- **MarkItDown** — lightweight file-to-Markdown conversion; use narrow converters and isolate untrusted inputs.
- **PaddleOCR** is already represented in the canonical frontier; benchmark only on difficult Arabic/English scans.
- **CAMeL Tools** — Arabic normalization/morphology/dialect/NER pilot for Saudi text extraction.
- **Gotenberg** — isolated document-render/PDF conversion candidate where current artifact tooling has a measured gap.

### Security / OSS evidence

- **ScanCode Toolkit** — license/copyright/package-provenance evidence; compare with Syft/REUSE before admission.
- **OWASP WSTG** — reference scenarios for Dealix-owned web/API testing.
- **OWASP ZAP** — bounded DAST against Dealix-owned local/staging/public surfaces only; never third-party scanning.
- **REUSE** is already represented in the canonical frontier.

### AI / MCP evaluation and security

- **Inspect AI** — reproducible model/tool-use evaluation candidate; receipts must feed existing Proof/Learning owners.
- **garak** is already represented in the canonical frontier.
- **MCP Scan** — isolated inspection of Dealix-owned MCP configurations/tool metadata for prompt injection, tool poisoning, shadowing and tool-change/rug-pull signals. Prefer passive/local-only evaluation first. Its non-local scan path can disclose tool names/descriptions to a third-party service, so data-boundary review is mandatory before any connected scan. Runtime proxy/guardrail mode must not silently become a second policy authority.

### API contracts

- **Spectral** — OpenAPI/JSON/YAML linting; no runtime gateway authority.
- **Pact Python** — isolated consumer/provider contract testing on one high-value boundary.
- **WireMock** — local provider simulation for retries, signatures, failures and error mapping; never a production proxy.

### Browser research

- **Stagehand** and **Browser Use** are already represented in the canonical frontier as isolated pilots. Playwright remains deterministic acceptance authority.

## Candidate admission law

`Measured Gap -> Canonical Owner -> Duplication Check -> License/Security/Data Boundary -> Isolated Pilot -> Benchmark -> Receipt -> ADOPT / REJECT / DEFER`

No candidate in this annex may create a second scheduler, CRM, browser authority, observability truth store, policy authority, agent fleet or proof store.

## Immediate order

Production/release TRUST remains ahead of capability expansion. If a single benchmark slot is available, prefer the candidate tied directly to the current measured gap; otherwise run no benchmark.

Current priority order:

1. restore trustworthy CI execution or establish a separately governed ephemeral substitute;
2. close exact-current-main Railway Web/API release parity;
3. front-door/TLS acceptance for Dealix-owned domains;
4. only then consume the single capability-benchmark slot for a measured gap.

`L5_EXECUTED=NONE`
