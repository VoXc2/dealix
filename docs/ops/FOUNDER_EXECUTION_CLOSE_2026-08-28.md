# Dealix Founder Execution Close — 2026-08-28

## Mission

Close the current trust/commercial train and redirect capacity to real relationships and the first verified paid Dealix pilot.

## Current source truth

- `main`: `dc51dfb11053424139c925144ab705c1706d7cbf`
- North Star: `FIRST_VERIFIED_PAID_DEALIX_PILOT`
- Infrastructure freeze remains in force unless a new verified regression appears.
- GitHub is code/backlog truth; Railway remains Production Core; VPS remains Command/AI/Engineering/Proof.
- One Company Brain, Opportunity Graph, Approval Center, Proof Ledger, Revenue Engine and scheduler.

## Active closure train

1. PR #1301 — current-main verifier truth repair.
2. PR #1297 — Growth Council / Company Delegation / Morning Revenue Command.
3. PR #1298 — public commercial truth + telemetry privacy defaults.

Do not open a parallel Company OS, CRM, agent fleet, scheduler, marketing engine, verification engine or public offer stack.

## Acceptance harness invariant

All isolated Git worktrees created on the founder VPS MUST be created and operated as the `dealix` OS user, or under a parent directory owned/traversable by `dealix`. Do not solve worktree ownership with global `safe.directory=*` or world-writable permissions.

A worktree/permission failure is classified as `ACCEPTANCE_HARNESS_PERMISSION_BLOCKER`, not a repository source failure.

## Remote CI truth

For the earlier PR #1301 head `2477a5a57fcaa1fe42e47344299586ca603bdaf7`, GitHub-hosted CI jobs were observed with `steps=[]`, `runner_id=0`, and no runner name. Until a runner actually executes a step, classify this as `REMOTE_CI_EXECUTION_PLANE_BLOCKED`, not as a proven compile/test/source regression.

Local exact-head acceptance remains required.

## Hosting / deployment truth

- Railway status on current `main` is successful and remains the Production Core signal.
- The connected Vercel project is on the `hobby` plan, reports `live=false`, and its latest READY deployment is from historical branch/PR work rather than current `main`.
- GitHub's Vercel failure target points to the private-organization-to-Hobby upgrade gate. Treat this as `VERCEL_PLAN_INTEGRATION_BLOCKED`, not a current-main build failure.
- Do not upgrade Vercel, deploy, change domains, or move production authority from Railway without a separate L5 decision.

## Capability acquisition policy

External tools enter Dealix only when they close a measured gap and do not create a parallel authority plane.

### Reuse / adopt when already available

- `actionlint`: workflow syntax/expression/action contract lint.
- `zizmor`: GitHub Actions security analysis.
- `Syft`: SBOM generation.
- `Trivy` / `OSV-Scanner`: vulnerability evidence and triage.

### Capability radar — do not install by default

- OpenTelemetry CI/CD semantic conventions for local verification observability.
- GitHub artifact attestations / SLSA provenance if the GitHub plan and hosted execution path make them usable.
- OpenSSF Scorecard checks as policy references for branch protection, dangerous workflows, token permissions and pinned dependencies.

No new collector, dashboard, scanner, daemon or scheduler is authorized merely because a tool exists.

## CRM adapter truth and forward compatibility

HubSpot remains `CRM_MIRROR` only.

Live property discovery on 2026-08-28 did not find the canonical Dealix truth fields requested for deals/contacts (`dealix_truth_class`, `dealix_evidence_id`, `dealix_relationship_state`, consent/suppression/payment-evidence equivalents). Search returned unrelated standard HubSpot properties instead. Therefore:

- do not store Dealix truth in semantically unrelated standard HubSpot fields;
- do not promote HubSpot records into verified relationships or revenue;
- keep the repository/Company OS as truth authority;
- add CRM schema only through an explicit, reviewed migration/write plan.

Before adopting HubSpot `/2026-09/`, validate Dealix writes against account-configured required properties, conditional requirements, and association rules; fail closed on HTTP 400 validation responses. Never relax Dealix truth rules to satisfy CRM writes.

## Revenue allocation through 3 September 2026

While production/security remains healthy:

- 70% — real interaction / events / inbound / partner conversations.
- 20% — diagnostic, discovery, proposal and proof preparation.
- 10% — engineering/trust only for verified blockers.

Big 5 Construct Saudi: 30 Aug–2 Sep 2026, Riyadh Front/ROSHN Front. Use the official exhibitor/app surfaces for routing and meeting planning, but keep directory entries `RESEARCH_ONLY` until a real conversation occurs.

LEAP: 31 Aug–3 Sep 2026. Event presence is an acquisition surface, not relationship proof.

## Economic truth firewall

- research != relationship
- CRM record != relationship
- event directory != relationship
- analytics event != payment
- proposal != revenue
- invoice != payment
- provider acceptance != delivery
- synthetic/demo != customer proof
- verified revenue requires payment evidence

## Canonical progression

`REAL_INTERACTION -> VERIFIED_RELATIONSHIP -> QUALIFIED_PROBLEM -> MINI_DIAGNOSTIC -> DISCOVERY -> CUSTOMER_SPECIFIC_QUOTE -> 30_DAY_REVENUE_COMMAND_PILOT -> PAYMENT_VERIFIED -> DELIVERY_PROOF -> EXPANSION/REFERRAL`

## Definition of done for this close

- #1301/#1297/#1298 exact-head integration acceptance is green or every blocker is classified with evidence.
- No new permanent agent or scheduler is introduced.
- Remote CI execution-plane failures are not misreported as source failures.
- Vercel plan/integration drift is not misreported as a Railway/production failure.
- Public commercial truth remains quote-only and evidence-scoped.
- HubSpot remains fail-closed CRM mirror and does not become economic authority.
- Founder Morning Revenue Command prioritizes only evidence-backed progression.
- Engineering returns to event-to-cash immediately after the current closure train is accepted.
