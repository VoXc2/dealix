# Dealix Capability Radar — 2026-08-28

## Purpose

This radar is a bounded adoption layer for external libraries, tools, templates and infrastructure ideas. It exists to maximize founder leverage without creating duplicate architecture, unbounded operational burden or new sources of business truth.

## Operating law

Every candidate must be classified before adoption:

- `ADOPT_NOW` — high ROI, low architectural duplication, bounded rollback.
- `PILOT_ISOLATED` — useful but must prove value in an isolated branch/worktree or non-production workflow.
- `DEFER` — potentially useful, but blocked by timing, dependency or lack of measurable benefit.
- `REJECT_DUPLICATE` — duplicates an existing Dealix capability or adds more operational complexity than value.

No candidate may create a second Company Brain, Opportunity Graph, Approval Center, Proof Ledger, CRM truth store, scheduler owner or permanent agent fleet.

## Current decisions

### 1. OpenCode V2 governance alignment — ADOPT_NOW

Use the existing repo `AGENTS.md` as the durable project instruction surface, and align future OpenCode agent configs to V2 semantics:

- `permissions` ordered rules, not legacy V1 fields;
- `shell` and `subagent` action names in V2;
- each child/subagent receives its own explicit permission boundary;
- deny rules remain explicit for production, secrets, payment and unsafe external actions;
- no shell interpolation with untrusted customer/branch/URL data.

Value: reduces context drift and prevents a powerful engineering agent from inheriting accidental broad authority.

Official references:
- https://opencode.ai/v2/docs/instructions
- https://opencode.ai/v2/docs/agents
- https://opencode.ai/v2/docs/permissions

### 2. n8n MCP workflow authoring — PILOT_ISOLATED

n8n's MCP server can build and update workflows from an AI client. Use this only as an authoring adapter over the existing n8n ownership model.

Pilot rules:

- existing n8n instance remains the workflow runtime owner;
- MCP may create/update a workflow only in a non-live or disabled state first;
- validate workflow structure and execute synthetic canaries before activation;
- no duplicate scheduler or parallel queue;
- no customer send/payment/production mutation during authoring acceptance;
- promotion to live follows existing Dealix approval/evidence gates.

Value: removes manual JSON/workflow assembly while keeping deterministic runtime ownership.

Official reference:
- https://blog.n8n.io/n8n-mcp-server/

### 3. `uv` / `uvx` for one-shot Python tooling — ADOPT_NOW

Prefer isolated tool execution using `uvx`/`uv tool run` for CLI scanners and utilities that do not need to become project dependencies. Use `uv run` when a tool must execute inside the Dealix project environment.

Rules:

- do not mutate Ubuntu system Python;
- pin versions for repeatable verification receipts when a tool becomes part of a gate;
- persistent installation only when another systemd/script owner requires a stable executable path;
- do not replace the existing Dealix `.venv` blindly.

Value: faster, cleaner tool experimentation with lower dependency collision risk.

Official references:
- https://docs.astral.sh/uv/concepts/tools/
- https://docs.astral.sh/uv/concepts/projects/run/

### 4. GitHub artifact attestations / build provenance — DEFER

Artifact attestations can attach signed build provenance to release artifacts using GitHub OIDC and support SLSA-oriented provenance.

Do not make this a current revenue blocker. Introduce it when the release/build execution plane is stable and Dealix has customer-consumed distributable artifacts that materially benefit from provenance verification. GitHub's own guidance says attestations are most useful for software artifacts consumers will verify, and not for frequent test-only builds or ordinary source/docs files.

Value later: stronger enterprise/security proof and verifiable software supply-chain provenance.

Official references:
- https://docs.github.com/en/actions/concepts/security/artifact-attestations
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations

### 5. OpenTelemetry Python / GenAI-compatible receipt schema — PILOT_ISOLATED

OpenTelemetry Python has stable traces and metrics. Use it first as a schema and lightweight instrumentation standard over existing Dealix receipts/logs, not as permission to add another observability database or dashboard.

Pilot fields:

- `workload_id` / `agent_role`
- provider + model when applicable
- operation name
- start/end/duration
- result class
- retry/fallback count
- governance/truth block class
- token/cost only when source-supported
- correlation to a verified commercial stage movement when one exists

Privacy and truth rules:

- prompt/system/retrieval/customer content capture is OFF by default;
- no PII or customer conversation bodies in generic telemetry;
- telemetry is operational evidence, never payment/customer-proof authority;
- primary business measure is `cost + latency + founder_minutes per verified stage movement`, not token count.

Acceptance: instrument one local/non-production workflow for 30 days. Keep only if MTTR, cost attribution or stage-decision quality improves measurably.

Official references:
- https://opentelemetry.io/docs/languages/python/
- https://opentelemetry.io/docs/languages/python/instrumentation/

### 6. Promptfoo / adversarial LLM evals — PILOT_ISOLATED_WITH_SANDBOX

Promptfoo is useful for deterministic prompt/model regression and red-team cases, but its OSS security model explicitly allows user-provided code/hooks/providers/transforms to execute with the runner user's permissions. Treat it as an eval runner, not a sandbox.

Dealix rules:

- run only in an isolated worktree/container/credential-scrubbed environment;
- never expose Railway, GitHub write, Telegram, payment, DNS or customer credentials to adversarial evals;
- no arbitrary remote fixtures/providers without source review;
- output becomes a verification receipt, not a business-truth event;
- use it to test truth-firewall prompts, unsupported-claim resistance, prompt injection, tool-selection boundaries and refusal correctness.

Acceptance: one bounded eval pack must detect seeded truth inflation / unsafe-tool / unsupported-claim regressions before the capability can be added to sovereign verification.

Official reference:
- https://github.com/promptfoo/promptfoo/blob/main/SECURITY.md

### 7. Playwright Test Agents / Playwright MCP — PILOT_ISOLATED

Use browser agents only for deterministic QA and test generation around approved properties. Prefer committed/reproducible Playwright tests and traces over opaque autonomous browsing.

Dealix use:

- #1298 public-surface commercial-truth acceptance;
- Arabic/English navigation and CTA parity;
- pricing/offer/claim drift canaries;
- screenshot/trace artifacts for review;
- connector/admin UI smoke tests only in explicitly authorized environments.

Boundaries:

- never turn browser automation into outreach or social-account automation;
- no personal LinkedIn scraping/messaging;
- no untrusted PR browser session with production/payment/DNS credentials.

### 8. OSV-Scanner V2 normalization — ADOPT_NOW_WITHIN_EXISTING_SECURITY_OWNER

Use OSV as another evidence source inside the existing supply-chain/security ownership, not as a new scheduler or independent risk score.

Requirements:

- pin a verified release/tool version when it becomes a gate;
- machine-readable JSON/SARIF receipts;
- reconcile duplicate findings with Trivy/Syft;
- distinguish `scanner_error`, `finding_present`, `reachable/exploitable`, `transitive_vendor_residual`, `fix_available`, `accepted_exception`;
- automated fixes remain proposals until independently verified.

### 9. New workflow engines / agent frameworks / CRMs / vector databases — REJECT_DUPLICATE by default

Examples include adding another scheduler, Temporal-style workflow ownership, another agent orchestration framework, a second CRM truth store, or another vector database simply because it is popular.

Admit only when a documented capability gap cannot be solved by the existing Dealix stack and a bounded benchmark shows a measurable improvement.

## Adoption score

Each candidate is scored 0–5 on:

1. Direct revenue leverage
2. Founder time saved
3. Reliability / proof improvement
4. Security improvement
5. Integration fit
6. Operational simplicity

Subtract 0–5 for each:

1. Architecture duplication
2. New credential surface
3. Ongoing maintenance burden
4. Migration risk
5. Vendor lock-in

`net_score >= 12` may enter `PILOT_ISOLATED` or `ADOPT_NOW`; otherwise defer/reject unless a proven blocker changes the economics.

## Current execution priority

The Capability Radar is subordinate to the commercial North Star:

`REAL_INTERACTION -> VERIFIED_RELATIONSHIP -> QUALIFIED_PROBLEM -> DIAGNOSTIC -> DISCOVERY -> CUSTOMER_SPECIFIC_PILOT -> PAYMENT_PROOF -> DELIVERY_PROOF`

Immediate execution order:

1. Close #1301 truth-verifier false positives with exact-head VPS evidence.
2. Close #1298 public commercial truth with type/build/public-surface/browser acceptance.
3. Reconcile #1297 against current `main` and preserve connector-nonfatal Morning Command semantics.
4. Use Playwright only to strengthen #1298 acceptance, not to open another automation lane.
5. Normalize OSV findings into the existing sovereign security receipt model.
6. Pilot the tiny OpenTelemetry-compatible schema against existing receipts before installing any backend.
7. Add Promptfoo only after an isolated, credential-scrubbed execution profile exists.
8. Do not adopt another workflow engine/CRM/vector DB/agent fleet without a measured blocker.

No capability acquisition may displace the highest-value current revenue action unless it removes a proven blocker on that path.
