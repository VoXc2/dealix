# Dealix Capability Frontier V2 — Ranks 51–100

Date: 2026-09-08 (Asia/Riyadh)

## Purpose

Extend the existing Top-50 admission radar without turning Dealix into a pile of tools.
This frontier is research/admission only. It preserves:

- ONE Company Machine / Brain / Opportunity Graph / Approval / Consent / Proof / Economic model.
- Exactly five permanent accountable agents.
- No bulk install.
- Maximum one active capability benchmark at a time.
- L5 material actions remain separate, exact and action-bound.

The v1 registry remains the first 50. This file adds 50 non-overlapping candidates (51–100) selected around measured gaps that are increasingly relevant to Dealix after the 2026-09-08 merge consolidation.

## High-value additions

### 1. AI evaluation and red-team

- DeepEval: agent task/tool/plan/safety metrics; useful for regression suites around the five canonical agents.
- Ragas: retrieval and RAG-specific quality metrics; only valuable if it adds signal beyond general agent evals.
- NVIDIA garak: LLM vulnerability scanner for injection, leakage, jailbreak and unsafe behavior.
- Microsoft PyRIT and Giskard: bounded comparison candidates for generative-AI red-team and application risk testing.

Admission rule: evaluation tools export receipts into existing Proof/Learning owners. They do not become a new observability truth store or runtime authority.

### 2. Browser and web intelligence

- Stagehand: hybrid Playwright + AI for unstable public research flows.
- Browser Use: exploratory read-only browser-agent candidate for flows where normal fetch/Playwright maintenance is poor.
- Playwright MCP: deferred unless connector interoperability is a measured gap; current Playwright/CLI/skills remain preferred for deterministic and token-efficient work.
- Trafilatura and Feedparser: low-complexity deterministic extraction/feeds are the most immediately useful additions.
- Firecrawl/Scrapy/ArchiveBox remain gap-triggered to avoid a second crawler/scheduler/truth store.

### 3. Document and entity intelligence

- MinerU / Marker / PaddleOCR are benchmark candidates against Docling on hard Arabic/English tender packs and scans.
- PyMuPDF and pypdf are bounded deterministic utilities for low-level PDF operations.
- Splink and Dedupe are controlled alternatives for probabilistic company/contact entity resolution; RapidFuzz remains the simple baseline and no match promotes a relationship or consent state.
- Pandera adds tabular/dataframe contract validation without replacing Pydantic at API boundaries.

### 4. Trust and blocked-CI recovery

- pip-audit and Bandit are cheap Python-specific cross-checks alongside OSV/Semgrep.
- OSV-SCALIBR is a pilot cross-check against Syft + OSV-Scanner.
- `nektos/act` is promoted to `ADOPT_FOR_ACCEPTANCE` because GitHub-hosted Actions have recently failed before repository steps. It may reproduce workflow step behavior locally, but its receipts must never claim equivalence with GitHub-hosted runners.
- Hyperfine, SQLFluff and SQLGlot improve deterministic benchmarking and SQL safety analysis.

### 5. Voice/realtime readiness

- LiveKit Agents and Pipecat are competing pilot candidates for a future governed inbound voice plane.
- faster-whisper, whisper.cpp and Silero VAD are local speech components to benchmark only with sanitized audio and after recording/consent policy is explicit.
- No live outbound dialing, no recording by default, and no new permanent agent fleet.

### 6. Sender/Web trust

- checkdmarc is an immediate read-only sender-health candidate. It must never mutate DNS automatically.
- axe-core, Lighthouse CI and Pa11y strengthen accessibility/performance/SEO acceptance for the public site.
- sitespeed.io is deeper diagnostics only after Lighthouse identifies a performance problem.
- Sentry CLI extends the existing Sentry authority for release/source-map/error correlation; it must not create a second observability service.

## Execution

Audit only:

```bash
bash scripts/ops/run_capability_frontier_v2_admission_v1.sh audit
```

Version-probe locally available tools without installation:

```bash
bash scripts/ops/run_capability_frontier_v2_admission_v1.sh pilot
```

The runner:

1. fetches current `origin/main` without cleaning/resetting the canonical workspace;
2. validates v1 and v2 registries and rejects duplicate ids/repos;
3. probes GitHub repository reachability;
4. checks likely duplicate references in current source;
5. probes versions only for already-installed local tools;
6. installs nothing;
7. writes proof receipts under `control/proof/capability-frontier-v2/<timestamp>`;
8. leaves `L5_EXECUTED=NONE`.

## Admission order

Do not benchmark all 50. Choose one measured gap using:

`value × fit × maturity × evidence quality × reuse`

÷

`duplication × maintenance × cost × security/privacy risk × founder minutes`

Suggested first benchmark sequence when the corresponding gap is active:

1. `nektos_act` — only while hosted Actions remain unavailable/pre-step blocked.
2. `checkdmarc` — read-only sender health before scaled email operations.
3. `axe_core` + Lighthouse CI — public-site acceptance strengthening.
4. `trafilatura` / Feedparser — deterministic market-source ingestion.
5. DeepEval or garak — one AI quality/security benchmark, not both at once.
6. MinerU vs Docling — only when hard Arabic/scanned tender documents justify it.
7. Stagehand — only for a real browser-maintenance gap.
8. Voice stack — only after inbound voice is a live commercial requirement and consent/recording policy is resolved.
