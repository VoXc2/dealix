# Dealix Ω∞ Autonomous Company Master Plan V3

Generated/adopted: 2026-09-13 Asia/Riyadh
Status: CANONICAL EXECUTION PRIORITY
Repository baseline at adoption: `d4cd30458a28a4e89bb3f1abbc99ee9cccaaa7b2`

## 0. Authority and continuation law

This document is the primary execution plan for Dealix until superseded by a later explicit architecture/operating decision.

Older plans, fixed-five-agent assumptions, historical global `DEEP_WIP_MAX=3` runtime ceilings, stale public pricing, old Railway-first deployment assumptions, and superseded execution strategies are historical only when they conflict with this plan.

Live truth precedence remains:
1. live VPS/runtime;
2. live production/release identity;
3. live GitHub `main`;
4. exact-head PR/worktree;
5. canonical Company Machine contracts;
6. Company Brain / Opportunity Graph / Approval / Proof / Economic Truth;
7. this plan;
8. historical chats/docs.

Truth firewall is mandatory:
`research != relationship`; `public contact != consent`; `signal != qualified problem`; `draft != sent`; `quote != invoice`; `invoice != payment`; `payment != revenue`; `delivery != customer value`; `customer value != public proof`; `merged != deployed`; `HTTP 200 != release identity`.

## 1. North Star

`CASH_READY_AUTONOMOUS_DEALIX_COMPANY`

Optimize simultaneously for:
- verified economic movement;
- customer value;
- production trust;
- founder minutes saved;
- execution speed;
- reliability;
- security;
- cost efficiency;
- Saudi market relevance;
- compounding company intelligence.

## 2. Canonical operating architecture

One Company Machine only:

`Dealix Holding -> Company Control Plane -> Sector Companies -> Arm Pods -> Specialist Logical Agents -> Bounded Runtime Workers`

Shared canonical services only:
- Company Brain;
- Opportunity Graph;
- Economic Truth;
- Approval/Authority;
- Consent/Relationship truth;
- Proof Ledger;
- Session Factory;
- Scheduler/Hermes orchestration;
- Resource Governor;
- Model/Cost Router;
- Observability/Tracing.

Hermes is the founder/control/execution interface over canonical Dealix truth. It must never become a second Company Machine.

OpenCode is the bounded execution fabric through Session Factory and isolated worktrees/sessions. Logical agent count must never imply one OS process per agent.

## 3. Autonomy law

- L0 Observe: autonomous.
- L1 Analyze: autonomous.
- L2 Draft: autonomous.
- L3 Internal Execute: autonomous.
- L4 Repo Execute: autonomous within acceptance gates.
- L5 Material External Effect: exact-action authority required.

L5 includes merge to protected/canonical main when governance requires exact authority, production deploy/cutover, DNS, production DB/schema mutation, secret/firewall mutation, customer send, public publish, payment/spend/refund, binding contract/quote/tender submission, destructive provider/account actions.

No cold WhatsApp. No LinkedIn scraping/mass automation. No fabricated relationship, consent, pipeline, proof, ROI, compliance certification or government access.

## 4. Execution systems / squads

1. President OS — economic ordering, portfolio allocation, conflict resolution.
2. Production Trust — VPS/Web/API/DB/TLS/release/backup/rollback.
3. Runtime OS — Hermes, Session Factory, Resource Governor, workers.
4. Model Economics — model quality/cost/quota/no-paid-spill.
5. Engineering OS — backend/web/integration/tests/refactors.
6. Security OS — AppSec, agent security, dependencies, supply chain.
7. Market Intelligence — Saudi official-source/sector intelligence.
8. Account Intelligence — organizations, buyers, signals, problem hypotheses.
9. B2G & Partnerships — Etimad, procurement, partners, suppliers.
10. Website & Growth — public truth, UX, SEO/AEO, conversion.
11. Diagnostic OS — free diagnostics and discovery preparation.
12. Commercial OS — customer-specific offer/pricing/negotiation.
13. Delivery OS — solution architecture, implementation, acceptance.
14. Proof OS — baseline, KPI, telemetry, customer value/proof.
15. Data/Knowledge OS — retrieval, memory, company knowledge.
16. Distribution OS — evidence-backed content/distribution drafts.
17. Learning OS — evals, experiments, lifecycle/promotion/kill.
18. Software Acquisition — OSS discovery, license/security/sandbox/benefit.

## 5. Sector-company pattern

Every canonical Dealix sector remains intelligence-active. Deep execution is allocated dynamically to the highest economic opportunities.

Each Sector Company exposes logical roles:
- sector-president;
- market-scout;
- account-intelligence;
- buyer-intelligence;
- problem-miner;
- diagnostic-agent;
- solution-architect;
- commercial-agent;
- delivery-agent;
- proof-agent;
- partner-agent;
- content-agent.

These are logical identities/capabilities, not permanent OS workers.

## 6. Arm-Pod contract

Every active arm must have:
- mission;
- buyer/problem;
- evidence inputs;
- input/output contract;
- tools/model policy;
- autonomy ceiling/effect classes;
- diagnostic path;
- commercial path;
- delivery path;
- proof/economic objective;
- verifier;
- success metric;
- promotion criteria;
- kill/suspend criteria;
- rollback/removal path where software is involved.

Arm pattern:
`Scout -> Planner -> Operator/Builder -> Independent Verifier -> Proof`.

## 7. Job contract

Every executable job requires:
- `job_id`;
- `trace_id`;
- sector/company/arm;
- logical owner;
- economic priority;
- effect class;
- exact base SHA/data version;
- worktree/session;
- model/tool policy;
- resource budget;
- max runtime/retries;
- acceptance criteria;
- verifier identity;
- proof required;
- rollback/kill condition;
- idempotency metadata where effects are possible.

Unknown authority, cost, owner, base SHA or effect classification must fail closed for modifying work.

## 8. OpenCode execution roles

OpenCode roles must be permission-separated:
- Scout/Explore: read/search/web, no repo edits.
- Analyst: read/analysis/drafts, no source mutation by default.
- Builder: bounded edits/tests only inside isolated worktree.
- Verifier: read/tests/review only; cannot edit reviewed work.

Builder may not independently approve its own work.

Preferred flow:
`Logical Agent -> Session Factory -> lease -> isolated worktree/session -> OpenCode role -> tests -> independent verifier -> receipt -> Company Brain`.

## 9. Resource Governor

Runtime capacity is determined from live evidence, not arbitrary agent counts:
- CPU headroom/load;
- available RAM/swap pressure;
- I/O pressure;
- active writer count;
- worktree capacity;
- provider quota/cost authority;
- incident state;
- task value/risk/latency.

Work weights should distinguish cheap research/static checks from builds, heavy model jobs and modifying writers.

Never allow uncontrolled process/worker explosion.

## 10. Economic ordering

Re-rank queued work frequently using an evidence-backed function such as:

`Priority = EconomicValue × Urgency × Confidence × BuyerAccess × DealixFit × ProofPotential × ReusePotential / TimeToValue / Cost / Risk / Contention`.

Do not optimize for PR count, agent count, lead count, message volume, impressions or token usage.

## 11. Current GitHub portfolio at adoption

Live `main`: `d4cd30458a28a4e89bb3f1abbc99ee9cccaaa7b2`.

Canonical dependency/order at adoption:
1. #1789 — clean FastMCP/httpx compatibility floor.
2. #1790 — self-host Production Trust stacked on clean dependency fix.
3. #1791 — exact-SHA sovereign acceptance harness for #1790.
4. #1783 — Session Factory canonical registry/resource-governed runtime cleanup.
5. #1784 — commercial truth authority / retrieval quarantine.
6. #1785 — Money-Now market dispatch + software-evolution dispatch.

No blind merges. Every PR requires exact-head/source-movement guards and relevant acceptance. Stale/duplicate branches are harvested or superseded rather than force-merged.

## 12. First 72-hour War Room

### Hours 0–6: Truth and trust
Parallel lanes:
- live source/runtime inventory;
- production Web/API/TLS/release identity;
- Hermes/Session Factory/Resource Governor/model broker health;
- dependency/security/source scans;
- public website crawl/truth inventory;
- Saudi official-source refresh;
- Company Brain/Opportunity Graph integrity.

Outputs:
- `LIVE_TRUTH_RECEIPT`;
- production PASS/HOLD matrix;
- runtime matrix;
- security matrix;
- public-truth inventory;
- market signal snapshot.

### Hours 6–18: Repair highest blockers
- close dependency resolver blockers;
- run exact-SHA Production Trust acceptance;
- reconcile Session Factory runtime ownership/capacity;
- remove/redirect/rewrite stale public claims;
- refresh official-source watches;
- generate structured market signals;
- score sector opportunities;
- create account/buyer research packets.

### Hours 18–36: Revenue/market machine
- all sectors intelligence ON;
- top economic sectors receive deep execution;
- B2G/Etimad intelligence;
- partner intelligence;
- account dossiers;
- buyer/problem hypotheses;
- free diagnostic packets;
- customer-specific offer skeletons;
- negotiation simulations;
- delivery/acceptance architectures.

### Hours 36–54: Proof, observability, security
- baseline/KPI/proof contracts;
- OpenTelemetry trace contract;
- uptime/TLS/DNS monitors;
- supply-chain/security gates;
- backup/restore drills in canary/non-production scope;
- agent/eval datasets;
- independent review.

### Hours 54–72: Learning and convergence
- score results;
- root-cause failures;
- run bounded improvement experiments;
- promote proven workflows to skills/tests/policy/routing;
- suspend/kill low-value or unsafe lanes;
- publish internal President economic order for next 7 days.

## 13. Permanent cadence

- Event-driven: urgent production/customer/market events wake owning lane.
- Hourly: health/queue/blocker/source-delta reconciliation.
- Every ~4 hours: economic reallocation based on current evidence.
- Daily morning: President economic order.
- Daily: market/account/diagnostic/commercial/delivery execution.
- Nightly: tests/security/evals/learning/backups.
- Weekly: sector/arm/agent lifecycle review; proof pack; OSS benchmark decisions.
- Monthly: constitution/market/risk/infrastructure/productization review.

Use one canonical scheduler/orchestrator. Do not create one cron per idea or a second workflow engine.

## 14. Saudi Market Intelligence

Official/current signal categories should include, where applicable:
- ZATCA/Fatoora waves;
- CST AI adoption/ICT guidance;
- NCA private-sector cyber controls;
- SAMA/open-banking/fintech signals;
- Ministry of Commerce business formation/activity;
- Etimad procurement/tenders;
- Invest Saudi sector opportunities;
- authorized first-party inbound/referrals/events;
- official company sites/newsrooms/hiring/expansion/partner signals.

A public/official signal creates research hypotheses only. It never creates relationship, consent, qualified problem, pipeline or revenue.

## 15. Automated targeting

Targeting state machine:
`SIGNAL_ONLY -> ACCOUNT_VERIFIED -> RESEARCHED -> PROBLEM_HYPOTHESIS -> BUYER_HYPOTHESIS -> RELATIONSHIP_ROUTE_FOUND -> REAL_INTERACTION -> QUALIFIED_PROBLEM -> FREE_DIAGNOSTIC -> DISCOVERY -> CUSTOMER_SPECIFIC_OFFER -> DECISION -> VERIFIED_PAYMENT -> DELIVERY -> CUSTOMER_VALIDATED_PROOF`.

Automate research, scoring, account dossiers, diagnostics, proposal drafts, B2G/partner discovery and follow-up drafts. External send remains effect/consent governed.

## 16. Commercial law

- all initial diagnostics are FREE/card-free;
- no public fixed-price authority;
- pricing/terms are customer-specific after qualified discovery;
- customer-specific pricing considers scope, cost, value, sector, urgency, risk, integrations and market evidence;
- quote != invoice; invoice != payment; payment != revenue;
- no fabricated testimonials/ROI/pipeline/consent/compliance/government access.

## 17. Website and public truth

Public website must remain simpler than the internal factory.

Target information architecture:
`Home -> Problems -> Sectors -> Capabilities -> Free Diagnostic -> Proof -> Trust -> How We Work -> B2G/Partners`.

Do not market agent counts, arm counts or internal architecture complexity as the value proposition.

Public claims must be classified:
- `VERIFIED_CURRENT`;
- `SUPPORTED_WITH_QUALIFIER`;
- `HISTORICAL`;
- `UNVERIFIED_REMOVE`.

Regression gates must prevent stale fixed prices, fixed-five public staffing guarantees, synthetic customer proof and false live/compliance claims from reappearing.

## 18. Delivery and Proof

Capability sellability states:
- `SELLABLE_VERIFIED`;
- `SELLABLE_WITH_CONSTRAINTS`;
- `PILOT_ONLY`;
- `RESEARCH_ONLY`;
- `BLOCKED`.

Every engagement should follow:
`Baseline -> Intervention -> Telemetry -> Acceptance -> Business Outcome -> Customer Validation -> Expansion/Productization Decision`.

Proof states:
- `NOT_PROOF`;
- `INTERNAL_EVIDENCE`;
- `CUSTOMER_ACCEPTED`;
- `PUBLIC_PROOF_APPROVED`.

## 19. Observability

OpenTelemetry is the preferred telemetry contract, not a single vendor lock-in.

Trace path:
`market_signal -> economic_decision -> sector/arm -> logical_agent -> model -> tool -> action -> verification -> proof -> economic_result`.

Do not record raw prompts, secrets, tokens or sensitive customer payloads by default.

## 20. Agent lifecycle / self-improvement

Score at minimum:
- accepted result rate;
- economic movement;
- proof quality;
- latency;
- model/tool/compute cost;
- retries;
- regressions;
- policy violations;
- founder intervention;
- reuse value.

Lifecycle recommendations:
`PROMOTE / KEEP / IMPROVE / CHANGE_MODEL / CHANGE_TOOLS / SPLIT / MERGE / SUSPEND / RETIRE`.

Failure loop:
`failure -> classify -> reproduce -> root-cause hypothesis -> bounded experiment -> independent eval -> regression guard -> promote/reject`.

No self-improvement may weaken authority, secrets, consent, independent verification, no-paid-spill or production-trust gates.

## 21. OSS acquisition policy

Every OSS candidate passes:
`Gap -> Provenance -> License -> Maintenance -> Security/CVE/KEV -> Supply-chain posture -> Sandbox -> Benchmark -> Resource footprint -> Data boundary -> Rollback -> 7-day benefit -> 30-day benefit -> ADOPT/HARVEST/WATCH/REJECT`.

No blind `curl | sudo bash`. No direct production-host install before sandbox acceptance. No second scheduler/CRM/Company Brain/model router/observability truth owner.

### High-priority candidates
- Crawl4AI — public-web extraction/research.
- changedetection.io — cheap official-source change watches.
- SearXNG — optional private metasearch front door.
- OpenTelemetry Collector — telemetry transport/normalization.
- OpenObserve — unified logs/metrics/traces benchmark.
- Promptfoo — agent/LLM eval and red-team regression gates.
- OSV-Scanner + Trivy — vulnerabilities/SBOM/misconfiguration/license scanning.
- Gitleaks — hardcoded-secret scanning.
- Semgrep Community Edition — source SAST/custom rules.
- Open Policy Agent/Conftest — bounded policy-as-code benchmark for authority/config gates.
- restic — encrypted file/config backup candidate.
- pgBackRest — PostgreSQL full/diff/incremental/PITR candidate.
- Uptime Kuma — outside-in HTTP/TLS/DNS monitoring.
- Renovate — sandboxed dependency-update candidate; never high-privilege production runtime.
- uv + Ruff + Pyright — Python feedback/dependency/type/lint workflow.
- pgvector — prefer extending PostgreSQL before adding a separate vector DB.
- Metabase — business/President dashboards only if it remains a view over canonical truth.
- Langfuse — later eval/trace pilot after OTEL contract is stable; do not create duplicate truth.

### Explicit hold/reject-until-gap-proven
- Temporal, Windmill, Airflow, Dagster, CrewAI, AutoGen, LangGraph as parallel orchestration stacks;
- Qdrant/vector DB before PostgreSQL/pgvector is proven insufficient;
- another CRM or operational truth DB;
- unofficial WhatsApp-Web automation;
- mass LinkedIn automation/scraping;
- public local-LLM endpoints.

## 22. Security architecture

Adopt agent-control principles:
- agent identity;
- tool authority;
- data authority;
- action/effect authority;
- economic authority;
- delegation authority;
- expiry;
- trace/receipt;
- least privilege;
- independent verification.

Policy enforcement should be machine-readable where useful. Candidate policy engines must complement, not replace, canonical Approval Authority.

## 23. Backup / disaster recovery

Backups are not proven until restore drills pass.

Require:
- source/config/control-state backup;
- PostgreSQL backup/restore strategy;
- non-production restore drills;
- rollback reference for every production release;
- backup retention/expiry policy;
- evidence receipt for backup + restore.

## 24. Metrics / President dashboard

North-star metrics:
- verified cash;
- real interactions;
- qualified problems;
- completed diagnostics;
- customer-specific offers;
- verified payments/paid pilots;
- delivery acceptance;
- customer-validated proof;
- expansion/referral;
- time-to-value;
- founder minutes per verified movement;
- cost per accepted result;
- production trust;
- agent accepted-result rate;
- security/policy violations.

## 25. Seven-day Definition of Done

By end of the first execution week, prove or truthfully block:
- exact current production/source identity;
- dependency resolver + focused acceptance;
- one Hermes -> Company Machine -> logical agent -> Session Factory -> OpenCode -> independent verifier -> receipt canary;
- resource-governed logical-agent execution;
- market watchers across priority Saudi sources;
- all canonical sectors current-intelligence capable;
- top account/buyer/problem dossiers;
- free diagnostic generation;
- customer-specific offer/negotiation/delivery packets;
- B2G/partner intelligence;
- public truth regression gate;
- security/supply-chain scan gate;
- backup/restore drill evidence;
- end-to-end tracing proof;
- agent/eval scorecards and first promotion/kill recommendations.

## 26. Thirty-day objective

Do not optimize for feature count. Target evidence-backed movement:
- real interactions;
- qualified problems;
- diagnostics;
- customer-specific proposals;
- verified payment/pilot;
- customer-validated proof.

Only productize patterns that repeat across real problems, interventions, acceptance and outcomes.

## 27. Final company loop

`Saudi/Customer Signal -> Market Intelligence -> Opportunity Graph -> Economic Governor -> Sector Company/Arm/Specialist -> Hermes/Session Factory -> OpenCode/MCP/Tools -> Independent Verifier -> Delivery -> Proof -> Economic Truth -> Learning -> Reallocation -> Next Economic Move`.

This loop, not agent count, PR count or automation volume, is the operating definition of an autonomous Dealix.