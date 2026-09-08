# Dealix Internet Capability Harvest + Probability Engine

Date: 2026-09-08 Asia/Riyadh

## Authority

This document is an internal research/admission artifact. It does **not** authorize bulk installation, customer send, public publish, spend, payment, production deploy, DNS/DB/secret mutation, tender submission, contract, or legal commitment.

Canonical law remains:

- ONE Company Machine / Brain / Opportunity Graph / Approval / Consent / Proof / Economic / Scheduler / Model Router / Dev Factory / Learning Factory.
- Exactly five permanent agents: `dealix-pm`, `dealix-sales`, `dealix-delivery`, `dealix-engineer`, `dealix-content`.
- `TRUST`, `MONEY_NOW`, `COMPOUNDING` run in parallel.
- `AUTO_INSTALL=false`.
- Maximum one active tool benchmark at a time.
- Research != relationship; public contact != consent; draft != sent; quote != invoice; invoice != payment; synthetic proof != customer proof.

## Live truth checkpoint

At harvest time:

- GitHub `main=d3be2ff69668bcc2b681efde43275ee172e75121`.
- `main` protection remains disabled and there are no trusted required checks.
- Railway Web latest SUCCESS is a redeploy of historical commit `18d9030043dcd7ca838517d9bbe3fe8f4d163fc6`, not current-main parity.
- Railway API latest observed rebuild is a redeploy of historical commit `678f657897eecfb9cbcd74fbeb0e67ccd09068ee`, not current-main parity.
- Therefore `PRODUCTION_GREEN=false` until Web/API serving release identities equal current main and front-door acceptance passes.

## Canonical capability-frontier decision

PR #1580 is the canonical ranks 51-100 frontier because it has one contiguous registry, explicit measured problem, duplication guard, benchmark, acceptance and rollback per candidate.

PR #1581 contains useful companion research, but its capability registry overlaps #1580 on multiple repositories (`checkdmarc`, `act`, `sqlfluff`, `stagehand`, `browser-use`, `paddleocr`, `deepeval`, `garak`, `lighthouse-ci`, `axe-core`, `reuse-tool`, voice candidates). The two registries MUST NOT be merged concurrently as independent authorities. Unique #1581 candidates should be harvested into a later non-overlapping frontier or supporting documentation.

## Fresh Internet Harvest — tools and libraries

### A. Workflow / agent execution

**Official n8n Skills** — ADOPT_REFERENCE_NOW
- Source: https://github.com/n8n-io/skills
- n8n publishes 13 capability skills plus a routing meta-skill and 50+ reference/example documents for workflow lifecycle, sub-workflows, loops, credentials, data tables, debugging, AI agents and error handling.
- Dealix action: use them only to improve the existing n8n orchestration layer. They do not become a new Company Brain, Scheduler or agent fleet.

### B. Browser / web intelligence

**Crawlee 3.16 + StagehandCrawler** — PILOT_AFTER_STAGEHAND
- Source: https://github.com/apify/crawlee
- 3.16 adds StagehandCrawler, async Dataset/KeyValueStore iteration, sitemap discovery and configurable Cloudflare handling.
- Use case: source families that need queues, pagination, sessions and repeatable crawling after deterministic fetch/Playwright paths prove insufficient.
- Guard: no broad crawl by default; respect source terms/robots and provenance.

**Stagehand** — already frontier candidate; PILOT_ISOLATED
- Source: https://github.com/browserbase/stagehand
- Keep Playwright as deterministic acceptance authority; Stagehand is for unstable public/authorized navigation.

**Browser Use** — already frontier candidate; PILOT_ISOLATED
- Source: https://github.com/browser-use/browser-use
- Current project exposes a Rust-powered browser harness and recovery loops.
- Use only for exploratory public/authorized research where deterministic code is uneconomic.

**Firecrawl** — already frontier candidate; DEFER_MEASURED_GAP
- Source: https://github.com/firecrawl/firecrawl
- Search/scrape/map/crawl/interact are useful but overlap current fetch/Crawl4AI/changedetection/Stagehand candidates.

### C. Document / Arabic / tender intelligence

**Docling** — KEEP_FIRST_LINE_CANONICAL_CANDIDATE
- Source: https://github.com/docling-project/docling
- Supports PDF, DOCX, PPTX, XLSX, HTML, EPUB, audio captions, email files, images and advanced PDF layout/table/formula understanding.
- Use as first-line structured parser for tender/RFP/report/document intelligence.

**MinerU** — already frontier candidate; BENCHMARK_VS_DOCLING_ONLY_ON_HARD_DOCS
- Use only for hard scanned/complex Arabic/mixed-layout documents where Docling confidence is inadequate.

**PaddleOCR** — already frontier candidate; OCR_FALLBACK
- Source: https://github.com/PaddlePaddle/PaddleOCR
- Arabic/English OCR fallback for scanned tenders/forms/evidence packs.

**MarkItDown** — HARVEST_UNIQUE_FROM_1581
- Source: https://github.com/microsoft/markitdown
- Lightweight common-file to Markdown conversion; suitable before heavy parsers when the source format is simple.

**CAMeL Tools** — HARVEST_UNIQUE_FROM_1581
- Source: https://github.com/CAMeL-Lab/camel_tools
- Arabic normalization/morphology/dialect/NER candidate for Saudi entity and text normalization.

**Gotenberg** — HARVEST_UNIQUE_FROM_1581
- Source: https://github.com/gotenberg/gotenberg
- Containerized governed rendering/merge/convert candidate for commercial PDF artifacts.

### D. Email trust and zero-send testing

**checkdmarc** — ADOPT_NOW_BOUNDED
- Source: https://github.com/domainaware/checkdmarc
- Read-only SPF, DMARC, BIMI, MX, STARTTLS, DNSSEC, MTA-STS and TLS-reporting evidence.
- Explicitly no automatic DNS mutation.

**Mailpit** — ADOPT_NOW_BOUNDED
- Source: https://github.com/axllent/mailpit
- Local/test SMTP capture with UI/API. Use to test HTML, attachments, MIME and sender behavior without external delivery.

**MJML** — HARVEST_UNIQUE_FROM_1581
- Source: https://github.com/mjmlio/mjml
- Responsive HTML email rendering for Gmail draft/testing lanes only.

**parsedmarc** — PILOT_AFTER_REAL_DMARC_REPORTS_EXIST
- Source: https://github.com/domainaware/parsedmarc
- Parse DMARC reports only after Dealix has real reports; do not create a parallel marketing truth store.

### E. Database / release trust

**Squawk** — ADOPT_NOW_BOUNDED
- Source: https://github.com/sbdchd/squawk
- Postgres migration linter focused on avoiding unexpected downtime and unsafe schema changes.

**ShellCheck** — ADOPT_NOW_BOUNDED
- Source: https://github.com/koalaman/shellcheck
- Static analysis for Bash/sh installers, acceptance runners and VPS control scripts.

**Hadolint** — PILOT_ISOLATED
- Source: https://github.com/hadolint/hadolint
- Dockerfile linting and inline shell quality evidence.

**nektos/act** — already frontier candidate; ADOPT_FOR_ACCEPTANCE_NONAUTHORITATIVE
- Source: https://github.com/nektos/act
- Local workflow rehearsal while hosted Actions are unhealthy; never equivalent to GitHub-hosted execution or Railway release authority.

### F. AI evaluation / security

Use one benchmark at a time. Do not maintain multiple overlapping persistent eval stacks.

**Promptfoo** — baseline when already present/approved
- Source: https://github.com/promptfoo/promptfoo
- Declarative eval/red-team/CI integration.

**garak** — frontier candidate; PILOT_ISOLATED
- Source: https://github.com/NVIDIA/garak
- Vulnerability probes for leakage, prompt injection, jailbreak, hallucination and unsafe behavior against local/test Dealix endpoints only.

**Giskard** — frontier candidate; PILOT_ISOLATED
- Source: https://github.com/Giskard-AI/giskard
- Agent/RAG evaluation and AI vulnerability testing; admit only if it adds unique findings versus Promptfoo/garak.

### G. Observability

**OpenObserve** — DEFER_MEASURED_GAP
- Source: https://github.com/openobserve/openobserve
- OpenTelemetry-native logs/metrics/traces/RUM/SLO/LLM observability in one platform.
- Dealix already has Sentry/PostHog/OpenTelemetry direction; do not create another observability authority without a quantified cost/visibility gap.

## Fresh Saudi official signal sources

These are candidate or reinforcing sources for `dealix-sales` and the existing Saudi Opportunity Mesh. Runtime source authority remains the canonical market-source registry; a webpage discovery is not automatically a runtime source.

### FURAS — municipal / real-estate / city investment
- https://furas.momah.gov.sa/
- Official unified Saudi-city investment portal.
- Current public portal reports 65k+ investment opportunities and 99/100+ participating government agencies depending page refresh.
- Signal types: municipal projects, direct rental, telecom sites, development sites, operator opportunities.
- Classification: RESEARCH_ONLY until exact opportunity/eligibility is verified.

### Monsha'at Jadeer — procurement / supplier qualification
- https://www.monshaat.gov.sa/
- Jadeer Tour pages advertise high-value procurement access, on-the-spot supplier qualification and 100+ exclusive procurement opportunities for certain tours.
- Signal types: supplier qualification, procurement access, major-company buyer access.
- Supplier qualification != buyer intent and event registration != award.

### NCA — cybersecurity controls
- https://nca.gov.sa/en/regulatory-documents/
- ECC 2-2024 and Cloud Cybersecurity Controls remain key Saudi cyber readiness references; NCA also exposes Data, Critical Systems, OT and implementation guidance.
- Signal types: cyber gap assessments, cloud/data/control mapping, evidence packs, implementation partner needs.
- Controls are requirements/reference evidence, not proof that a specific company has a buying problem.

### SAMA Open Banking
- https://www.openbanking.sama.gov.sa/
- SAMA began licensing fintech companies for Open Banking services in March 2026 after sandbox completion.
- Framework includes business rules, technical standards, API specifications, operational guidelines and a conformance lab.
- Signal types: API readiness, conformance, consented data sharing, operating controls, integration/testing opportunities.

### Digital Government Authority GPaaS / Government OSS Repository
- https://dga.gov.sa/en/programs/GPaas
- Government GitLab PaaS/open-source software repository program focused on reuse, DevOps/DevSecOps, collaboration, efficiency and secure source-code management.
- Signal types: government software reuse, DevSecOps readiness, OSS governance, integration and delivery patterns.

### Saudi Exchange issuer announcements
- https://www.saudiexchange.sa/
- Official issuer/financial-advisor announcements can be filtered by company, sector, announcement type and time period.
- High-value trigger classes: contract award, acquisition, capex, facility expansion, financing, board/management changes, new project, results and material event.
- Announcement != Dealix opportunity until a relevant workflow/problem hypothesis is verified.

## Probability-Maximizing Commercial Engine

The user's desired strategy is to maximize the number of useful attempts without turning Dealix into a spam engine. The scalable interpretation is: maximize **research/verification/qualification attempts** broadly; keep deep commercial WIP narrow; execute external touches only through ChannelEligibility and exact authority.

### Funnel capacity targets (adaptive, not promises)

Per operating day, capacity should be allowed to scale approximately as:

1. 1,000+ raw economic/source signals discovered or refreshed.
2. 200 verified/relevant signals after provenance/freshness/deduplication.
3. 50 account-level hypotheses with evidence/unknown split.
4. 20 buying-committee/contact maps.
5. 10 personalized diagnostic packets/drafts.
6. Deep commercial WIP <= 3 accounts at a time.
7. External sends remain governed and action-bound; no automatic send authority is inferred from the funnel.

The numbers are capacity ceilings/targets, not evidence that the market contains that many valid opportunities each day.

### Expected-value score

Prioritize each candidate using a measurable expected-value model:

`EV = P(real_problem) * P(reach_decision_maker) * P(response|eligible_channel) * P(qualified_discovery) * P(close) * expected_margin * proof_value / (founder_minutes + delivery_risk + compliance_risk)`

Keep component probabilities empirical and update them from real outcomes. Unknown probabilities must be marked unknown rather than invented.

### Adaptive allocation / bandit policy

Use a bounded multi-armed-bandit style allocator across:

- sector / economic motion,
- offer,
- source family,
- role/persona,
- draft angle,
- eligible channel,
- partner vs prime route.

Exploration gets a small fixed budget; exploitation receives more capacity when real response/qualification/payment evidence improves. Synthetic scores never override opt-out, suppression, eligibility or legal/contract gates.

### Attempt ladder

For each account, the machine may prepare multiple attempt candidates, but stop immediately on hard opt-out/suppression or invalid eligibility.

Possible ladder:
1. Account trigger refresh.
2. Buying-committee enrichment.
3. Founder email draft #1.
4. Follow-up draft based on new evidence, not a blind bump.
5. Warm-introduction/partner route search.
6. Founder LinkedIn/manual relationship route when appropriate.
7. Call/WhatsApp only when relationship/consent/channel policy permits.
8. Recycle to nurture/research when timing is wrong.

Do not infer that a public email/phone number authorizes a specific channel.

### Stop-loss and learning

Stop or downgrade when:
- opt-out/suppression exists;
- evidence indicates no fit;
- no meaningful new information supports another attempt;
- delivery route cannot be executed credibly;
- expected founder minutes exceed expected economic value;
- compliance/contract risk dominates expected value.

Every loss produces one reusable artifact: targeting rule, objection, eligibility gap, partner need, missing capability, offer adjustment or delivery lesson.

## Immediate benchmark order

1. `checkdmarc` read-only audit of Dealix-owned sender domains.
2. `Mailpit` local/test Company Profile + attachment + MIME/email template acceptance.
3. `Squawk` on current migrations as report-only evidence.
4. `nektos/act` on one safe workflow subset while hosted Actions remain non-authoritative; label all receipts emulator-only.
5. `axe-core` + `Lighthouse CI` on local/current-candidate critical routes.
6. `Trafilatura`/Feedparser on 20 official Saudi sources for deterministic ingestion.
7. ONE LLM security/eval benchmark: garak or DeepEval/Giskard, not all simultaneously.
8. MinerU vs Docling only on a hard Arabic/scanned tender corpus.
9. Stagehand/Crawlee only after deterministic source adapters show a measured maintenance gap.
10. Voice/realtime/nurture tools remain deferred until a real approved use case exists.

## Merge / duplication rule

Before merging a frontier:

1. reconcile with current live main;
2. compare repositories/IDs against all already-merged frontier registries;
3. fail on duplicate canonical ownership;
4. run structural tests and one bounded benchmark only;
5. merge only with exact current-head authority;
6. post-merge run fresh reconciliation before installing or adopting anything.

No tool is installed merely because it appears in this file.