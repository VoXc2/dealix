# Dealix Capability Frontier V2 — Ranks 51–100

Date: 2026-09-08 (Asia/Riyadh)

## Purpose

Extend the merged Top-50 admission radar without turning Dealix into a pile of tools or rediscovering capabilities that current main already owns.

Permanent law:

- ONE Company Machine / Brain / Opportunity Graph / Approval / Consent / Proof / Economic model.
- Exactly five permanent accountable agents.
- No bulk install.
- Maximum one active capability benchmark at a time.
- Current `oss_capability_manifest_v2.json` has authority over already-admitted/catalogued capability state.
- L5 material actions remain separate, exact and action-bound.

The v1 registry remains ranks 1–50. This frontier adds ranks 51–100 after explicit reconciliation against both Top-50 and the current-main OSS manifest.

## Reconciliation correction

The first V2 draft incorrectly compared only with `capability_top50_v1.tsv`. Current main also owns `config/oss/oss_capability_manifest_v2.json`.

Direct re-admissions such as Trafilatura, Firecrawl, Scrapy, Marker, PaddleOCR, Splink, Dedupe, LiveKit Agents, Pipecat, faster-whisper, Silero VAD and checkdmarc were removed from the fresh frontier. Ragas and DeepEval remain only `DEFER_MEASURED_GAP`, consistent with the manifest's existing evaluation-alternative posture.

A dedicated current-manifest overlap verifier now fails closed if a future frontier edit repeats this mistake.

## High-value additions

### 1. AI evaluation and red-team

- garak: bounded LLM vulnerability scanning on Dealix-owned local/test endpoints.
- PyRIT and Giskard: isolated comparison candidates for generative-AI red-team/application risk.
- DeepEval/Ragas: deferred until a named metric gap exists beyond Promptfoo/native Dealix gates.

All evaluation output feeds existing Proof/Learning owners; no second observability or policy authority.

### 2. Browser/web intelligence

- Stagehand: hybrid deterministic + AI navigation when a real Playwright maintenance gap exists.
- Browser Use: exploratory public read-only research only.
- Playwright MCP: deferred until connector interoperability is a measured gap.
- Feedparser: deterministic attributable RSS/Atom ingestion.
- ArchiveBox: deferred durable source preservation, not a new truth store.

Existing current-main Trafilatura/Crawl4AI/changedetection authority is reused rather than re-added.

### 3. Document/data intelligence

- MinerU: hard Arabic/mixed-layout tender benchmark against Docling after license/attribution gate.
- PyMuPDF: headline decision is subordinate to explicit AGPL/commercial-license review.
- pypdf/pdfplumber: bounded deterministic PDF utility/fallback lanes.
- Pandera: dataframe/schema contracts without replacing Pydantic/API boundaries.

Existing Marker/PaddleOCR/Splink/Dedupe catalogue decisions remain in the current-main manifest and are not duplicated here.

### 4. Trust / release reliability / CI recovery

- ShellCheck: semantic shell analysis beyond `bash -n`.
- Hadolint: bounded Dockerfile linting.
- Squawk: Postgres migration/SQL lock-risk linting; real Postgres acceptance remains authority. Upstream itself states lint PASS alone is not proof a migration is safe.
- lychee: bounded broken-link checks on Dealix-owned/documented surfaces.
- SSLyze: read-only TLS/certificate evidence for Dealix-owned endpoints.
- Lynis: read-only hardening assessment; never automatic remediation.
- pip-audit/Bandit/OSV-SCALIBR: focused security cross-checks under existing TRUST.
- `nektos/act`: local non-authoritative workflow rehearsal while GitHub-hosted execution remains pre-step blocked.
- OpenSSF Scorecard: upstream security-practice evidence only.
- cosign / in-toto: deferred artifact provenance candidates; no automatic signing identity/key creation.
- GUAC: deferred unless current SBOM/provenance/vulnerability receipts become too fragmented; never a second Company Graph.
- ScanCode Toolkit: bounded license/copyright/package-origin evidence.

### 5. API contracts

- Spectral: deterministic OpenAPI/JSON/YAML linting.
- Pact Python: one bounded consumer/provider contract pilot.
- Schemathesis remains current behavioral API-test authority on main; no second API truth plane.

### 6. Voice and Web quality

- whisper.cpp is a potential CPU/portability fallback only because faster-whisper is already bounded on main.
- axe-core + Lighthouse CI + Pa11y strengthen public-site acceptance.
- sitespeed.io remains deeper diagnostics after a measured performance issue.
- Sentry CLI extends existing Sentry release/error correlation only.

No live outbound dialing, no recording authority, and no new permanent agent fleet.

## Execution

Audit only:

```bash
bash scripts/ops/run_capability_frontier_v2_admission_v1.sh audit
python3 scripts/ops/verify_capability_frontier_v2_current_manifest_v1.py
python3 -m pytest -q \
  tests/test_capability_frontier_v2_registry.py \
  tests/test_capability_frontier_v2_current_manifest_overlap.py
```

The runner installs nothing and leaves `L5_EXECUTED=NONE`.

## Admission order

Do not benchmark all 50. Select one measured gap using:

`value × fit × maturity × evidence quality × reuse`

÷

`duplication × maintenance × cost × security/privacy risk × founder minutes`

Current priority:

1. restore trustworthy CI execution or separately govern a non-authoritative rehearsal path;
2. exact-current-main Railway Web/API parity;
3. front-door/TLS/current-release acceptance;
4. only then consume the single benchmark slot for the measured gap with the highest expected value.

Candidate order after TRUST closes:

1. `nektos_act` only while hosted Actions is blocked and only as local rehearsal;
2. ShellCheck / Squawk when current shell or migration defects justify them;
3. axe-core + Lighthouse CI for Web acceptance;
4. Feedparser for attributable market-source ingestion;
5. ONE AI-eval/security benchmark such as garak;
6. MinerU vs Docling only on difficult documents after license gate;
7. Stagehand only for a proven browser-maintenance gap;
8. voice only after a real inbound use case plus consent/recording policy.

`AUTO_INSTALL=false`
`MAX_ACTIVE_BENCHMARKS=1`
`L5_EXECUTED=NONE`
