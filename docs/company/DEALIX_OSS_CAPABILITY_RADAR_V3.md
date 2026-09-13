# Dealix Ω∞ V3 — Open-Source Capability Admission Radar

Generated: 2026-09-13 Asia/Riyadh
Authority: subordinate to `DEALIX_OMEGA_MASTER_PLAN_V3.md` and the canonical Software Acquisition/Evolution gates.

## Admission law

No tool is installed merely because it is popular or open source.

Every candidate must pass:

`Verified Gap -> Provenance -> Exact Version/SHA -> License -> Maintainer Activity -> CVE/KEV -> SBOM/Signature -> Security/Data Boundary -> Resource Cost -> Duplication Check -> Sandbox Benchmark -> Rollback/Removal -> 7-Day Benefit -> 30-Day Benefit -> ADOPT / HARVEST / WATCH / REJECT`.

Never use blind host installers. Prefer pinned containers/binaries/checksums/signatures and isolated labs. A tool never becomes a second CRM, scheduler, Company Brain, Opportunity Graph, Proof Ledger, Approval Authority or Model Router.

## Tier P0 — highest-value candidates

### Crawl4AI
State: `ADOPT_PILOT`
Use: public-web research, official-source extraction, Arabic/English evidence capture, bounded MCP/web context.
Boundary: public/authorized sources only; research does not establish relationship or consent.
Success metric: useful evidence per crawl, extraction accuracy, latency, RAM/CPU, source provenance.

### changedetection.io
State: `ADOPT_PILOT`
Use: cheap monitoring of official/regulatory/company pages; trigger deep crawl only after meaningful change.
Pattern: `Watch -> Delta -> Evidence Fetch -> Structured Signal -> Economic Queue`.
Success metric: useful deltas / total deltas, false-positive rate, compute saved versus repeated full crawling.

### OpenTelemetry
State: `ADOPT_CONTRACT`
Use: canonical vendor-neutral trace/metric/log contract.
Trace target:
`market_signal -> economic_decision -> sector/arm -> logical_agent -> model -> tool -> action -> verifier -> proof -> economic_result`.
Default privacy: do not record raw prompts, secret values or customer payloads.

### Promptfoo
State: `ADOPT_PILOT`
Use: LLM/agent/RAG evals, red teaming and coding-agent acceptance.
Initial attack/eval set should cover repo prompt injection, terminal-output injection, secret/environment access, sandbox escape, tool/MCP poisoning, privilege escalation, verifier sabotage, memory/retrieval poisoning and delayed side effects.
Promotion rule: no prompt/model/skill/tool-routing change is promoted when regression/eval evidence worsens materially without an explicit reviewed exception.

### OSV-Scanner
State: `ADOPT_PILOT`
Use: dependency and SBOM vulnerability cross-check.
Boundary: scanner findings require triage; scan result alone does not authorize package mutation.

### Trivy
State: `ADOPT_PILOT`
Use: vulnerabilities, secrets, misconfiguration, licenses and SBOM/container checks.
Boundary: keep source/runtime acceptance separate from scanner infrastructure failures.

### Syft
State: `ADOPT_PILOT`
Use: deterministic SBOM generation for images/filesystems/archives in SPDX/CycloneDX/Syft formats; optional signed attestation path.
Target chain:
`repo SHA -> SBOM -> vulnerability/license scan -> artifact digest -> release SHA -> production proof`.

### Gitleaks
State: `ADOPT_EXISTING_HARDEN`
Use: repository secret detection.
Policy: no broad test-directory exclusions; synthetic fixtures get narrow evidence-backed exceptions only.

### restic
State: `ADOPT_PILOT`
Use: encrypted snapshots for non-database critical control/config/workspace state.
Acceptance: backup alone is insufficient; periodic isolated restore drill required.

### pgBackRest
State: `ADOPT_PILOT`
Use: PostgreSQL full/differential/incremental backup and PITR candidate.
Acceptance: non-production restore/PITR drill, RPO/RTO measurement, storage/encryption/retention and rollback documented before production authority.

## Tier P1 — bounded pilots after P0 gaps are stable

### OpenObserve
State: `PILOT_IF_OBSERVABILITY_GAP`
Use: unified OTel logs/metrics/traces backend.
Do not add if existing observability already meets the trace/search/retention need at lower complexity.

### Uptime Kuma
State: `PILOT_OUTSIDE_IN`
Use: dealix.me / www / api health, HTTP/TCP/DNS and certificate monitoring.
Security: prefer loopback/private management; do not hand it an unrestricted Docker socket merely for convenience.

### SearXNG
State: `PILOT_PRIVATE_SEARCH`
Use: private metasearch/discovery diversity for Market Radar.
Boundary: discovery result is evidence input only; never relationship/consent.

### Semgrep
State: `PILOT_STATIC_ANALYSIS`
Use: additional source/security rules where current Ruff/Bandit/CodeQL/Trivy coverage shows a measurable gap.
Reject if it only duplicates existing high-signal gates with no incremental findings.

### Dagger
State: `PILOT_ACCEPTANCE_PORTABILITY`
Use: portable, repeatable containerized acceptance pipelines to reduce current host/CI execution-plane drift.
Boundary: it is not a second Dealix scheduler; it may package deterministic build/test/canary recipes only.
Success metric: lower environment-related false failures and lower acceptance setup time.

### Plausible / Umami
State: `BENCHMARK_CHOOSE_ONE`
Use: lightweight privacy-oriented website conversion analytics if current analytics do not answer qualified diagnostic conversion questions.
Do not install both. Neither becomes Economic Truth authority.
Metrics: qualified diagnostic starts/completions, sector-page conversion and source attribution without unnecessary personal-data collection.

### Langfuse
State: `PILOT_AFTER_OTEL`
Use: LLM traces, datasets, experiments, evaluation and cost/latency analysis where it provides value beyond canonical OTel evidence.
Boundary: no second company truth store; export/reference results back to current Proof/Learning contracts.

### Metabase
State: `PILOT_DASHBOARD_MIRROR`
Use: President/business dashboards over canonical data.
Boundary: visualization only, never source of truth.

## Tier WATCH / HARVEST ONLY

### Open Policy Agent (OPA)
State: `WATCH_POLICY_PDP`
Potential use: policy-as-code decision point for effect/tool/resource rules when current Approval/Authority contracts need a reusable evaluator.
Important: OPA may evaluate policy; it must not replace canonical Dealix authority/evidence state.

### OpenBao
State: `WATCH_SECRETS`
Potential use: encrypted secret engines, dynamic credentials, auth methods and audit devices if current secret-management architecture has a proven gap.
Gate: migration/rotation/availability/backup/rollback plan plus strict resource and operations review first.

### OpenFGA
State: `WATCH_AUTHZ`
Potential use: fine-grained relationship authorization for future SaaS tenant/org/resource policy only if existing authorization/RLS contracts become insufficient.
Do not add merely because it is a mature authorization project.

### LiteLLM
State: `HARVEST_OR_BENCHMARK_ONLY`
Potential use: provider abstraction/cost/rate-limit patterns.
Boundary: current Dealix Model Router remains authority; no second routing plane.

### vLLM
State: `FUTURE_GPU`
Potential use: local/private high-throughput model serving after GPU economics justify it.
Boundary: authenticated/private ingress only; not a current CPU-VPS priority.

### Qdrant
State: `HOLD_VECTOR_DB`
Potential use: vector/hybrid search only if PostgreSQL + pgvector + FTS is proven insufficient.
Default: avoid a second data service before benchmark evidence.

### GrowthBook
State: `WATCH_EXPERIMENTATION`
Potential use: product/site experimentation after Dealix has enough real traffic and trustworthy conversion instrumentation.
Boundary: feature/experiment state must not become Commercial/Economic Truth authority.

## Explicit REJECT_DUPLICATE defaults

- second CRM/platform truth database;
- second Company Machine;
- second agent-fleet authority;
- second general scheduler/orchestrator;
- second Opportunity Graph / Approval / Proof store;
- mass LinkedIn automation/scraping;
- unofficial WhatsApp-Web production automation;
- cold WhatsApp blast tools;
- tools requiring broad host/root authority when a bounded alternative exists;
- any tool whose value is only adding another dashboard over the same data.

## Benchmark receipt schema

Every evaluated tool records:
- candidate/project;
- exact version/tag/SHA/digest;
- source/provenance;
- license;
- maintenance/activity;
- CVE/KEV/security notes;
- SBOM/signature/checksum evidence;
- install method;
- CPU/RAM/disk baseline;
- network/data boundaries;
- secrets required;
- Arabic/English task quality where relevant;
- latency/throughput;
- task-success rate;
- evidence/provenance quality;
- integration effort;
- operating cost;
- duplication risk;
- rollback/removal steps;
- 7-day benefit;
- 30-day benefit;
- final decision `ADOPT / HARVEST / WATCH / RETEST / REJECT`.

## Immediate benchmark order

1. Promptfoo agent/coding-agent security eval in isolated environment.
2. Syft + Trivy + OSV-Scanner SBOM/security chain against a representative Dealix artifact.
3. pgBackRest canary-only PostgreSQL restore/PITR proof plus restic restore for control-state sample.
4. changedetection.io -> Crawl4AI signal pipeline against a bounded official-source sample.
5. OpenTelemetry trace prototype across one `signal -> job -> verifier -> receipt` canary.
6. Uptime Kuma outside-in private pilot after public release identity is known.
7. Dagger acceptance portability benchmark only if current sovereign harness still suffers environment drift.
8. Plausible vs Umami benchmark only after public-site conversion instrumentation requirements are frozen.

No candidate above is production-authorized merely by appearing in this radar.