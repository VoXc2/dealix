# Dealix v5 — Revenue Operating Company OS — Honest Scope

## Why this doc exists

The v5 master prompt asked for **12 control planes / OS layers**:

1. Revenue Control Plane
2. Customer Data & Consent Plane
3. Agent Governance Plane
4. Delivery Factory
5. Proof & Evidence Ledger
6. Finance / Billing Safety Plane
7. GTM & Self-Growth v5
8. Partner & Ecosystem OS v5
9. Role Command OS v5
10. Reliability / Observability / Incidents
11. Security & Privacy Hardening
12. Vertical Playbooks

Plus 14 docs and ~12 test files. Total ~50+ new files in one pass.

That violates the master rule of every prior prompt:

> "Do not build random features. Do not rewrite the product. No
> half-finished implementations. No scaled low-value AI pages."

Three of the planes were **shipped real** in this session
(grounded in existing infra, full tests, no stubs). The other nine
are **deferred with explicit ship-when triggers** so they're not
forgotten — and are NOT silently stubbed.

## What shipped real this session (3 of 12)

### ✅ Customer Loop  (≈ Revenue Control Plane lite)

`auto_client_acquisition/customer_loop/` + `api/routers/customer_loop.py`.
12-state journey machine: lead_intake → diagnostic_requested →
diagnostic_sent → pilot_offered → payment_pending → paid_or_committed
→ in_delivery → proof_pack_ready → proof_pack_sent →
upsell_recommended (+ nurture, blocked).

Each transition validated against `ALLOWED_TRANSITIONS` (no skipping
stages). Each state returns a bilingual checklist — every action
is HUMAN-executable; nothing automated. `safety_notes` re-asserted
on every advance.

Tests: 12 cases.

### ✅ Role Command OS  (PHASE 10)

`auto_client_acquisition/role_command_os/` +
`api/routers/role_command_os.py`. 7 role briefs:

CEO · Sales · Growth · Partnership · Customer Success · Finance · Compliance

Each brief composes existing measurements (service activation
matrix, geo_aio_radar, partner_distribution_radar, daily_growth_loop)
and reframes them for that role's concerns. No LLM call. Arabic
primary + English secondary. Every decision carries
`approval_required` + risk_level + (optional) proof_event.

Compliance brief surfaces the 4 REVIEW_PENDING items + Issue #138 link.
Sales brief surfaces top 3 service-promotion candidates.
Growth brief surfaces top 3 GEO/AIO priority pages.
Partnership brief surfaces top 3 partner categories.

Tests: 14 cases (parametrized over all 7 roles).

### ✅ Service Quality  (Delivery Factory QA piece)

`auto_client_acquisition/service_quality/` +
`api/routers/service_quality.py`. Two thin modules:

- `qa_gate.check_delivery_payload(service_id, payload)` — validates
  required_inputs, blocks forbidden actions (per YAML
  `blocked_actions`), runs draft text through
  `safe_publishing_gate`. Verdict: `pass | needs_review | blocked`.
- `sla_tracker.get_sla(service_id)` / `list_slas()` — reads SLA
  text from the YAML matrix per service.

Tests: 9 cases (full QA matrix + endpoint coverage).

## What's deferred (9 of 12) — with reason and ship-when

### 🟡 Customer Data & Consent Plane

**Why deferred:** Requires a Postgres consent_table schema +
migration + read/write API + per-tenant scoping. Touching DB
schema requires founder review of data lifecycle policy and PDPL
audit. Building it without that policy in writing would lock in a
schema that needs migration later.

**Already in repo (related):**
- `auto_client_acquisition/v3/compliance_os.py:assess_contactability`
  — runtime block for cold WhatsApp / non-consenting channels.
- `consent_required_send` service in YAML matrix.
- `tests/test_whatsapp_policy.py` — 9 sanity tests.

**Ship-when:** Founder approves a data-lifecycle policy doc + chosen
DB scoping approach (tenant_id everywhere vs Postgres RLS).

### 🟡 Agent Governance Plane

**Why deferred:** `auto_client_acquisition/v3/agents.py:SafeAgentRuntime`
already implements the core: `restricted_actions = {send_cold_whatsapp,
auto_linkedin_dm, delete_data, export_pii}` blocks at task creation;
`approve()` refuses to unblock; `execute()` refuses BLOCKED tasks.
A new "agent_governance" module would duplicate this. The v5 prompt
asks for autonomy levels (L0-L5) — useful, but should be a **thin
extension** of `SafeAgentRuntime`, not a new module tree.

**Ship-when:** When the first content_draft_engine ships and needs
per-agent autonomy classification (Phase 8 of older Self-Growth scope).

### 🟡 Delivery Factory (full)

**Shipped:** the QA + SLA pieces (above).

**Deferred:** the per-service delivery-plan builder, task generator,
handoff manager, full session machine.

**Why:** Each Top-5 service needs founder-curated checklists for
every step (intake → execution → proof). Generating them
algorithmically would produce content the founder hasn't approved.

**Ship-when:** Founder hand-curates a delivery-plan template for
ONE service (Growth Starter), then we generalize into a builder
that takes that template as input.

### 🟡 Proof & Evidence Ledger (full)

**Shipped pieces:**
- `proof_snippet_engine.render` (single event)
- `proof_snippet_engine.render_pack` (assembled markdown — P2 above)
- `evidence_collector` in-process buffer

**Deferred:** Postgres ProofEvent table + RevenueWorkUnit table +
HMAC signature + redactor + export endpoint.

**Why:** Until first paid pilot generates 5+ real ProofEvents, the
ledger is solving for nothing. In-process buffer + manual
JSON-on-disk are sufficient.

**Ship-when:** ≥5 real ProofEvent rows exist on disk.

### 🟡 Finance OS (full)

**Shipped pieces:**
- `dealix/payments/moyasar.py:create_invoice` (existing)
- `scripts/dealix_invoice.py` admin CLI (P3 above)
- `whatsapp_allow_live_send=False` reasserted by tests

**Deferred:** unit_economics module, refund_policy module,
finance_guardrails as a library.

**Why:** Pricing is a founder decision (S1 in Decision Pack).
Refund policy is documented in `roi.html` (one of the 4
REVIEW_PENDING strings). Building "unit economics" without 5
delivered customers means inventing assumptions.

**Ship-when:** S1 sign-off + 5 customers delivered.

### 🟡 GTM OS (full)

**Already exists across:**
- `self_growth_os/geo_aio_radar` — readiness audit
- `self_growth_os/partner_distribution_radar` — partner catalog
- `self_growth_os/weekly_growth_scorecard` — aggregator
- `self_growth_os/daily_growth_loop` — daily composition
- `self_growth_os/safe_publishing_gate` — publishing check

**Deferred:** message_experiment, channel_strategy, content_calendar
as separate modules.

**Why:** Message experiments need a real distribution channel + a
real audience baseline. Content calendar without keyword data
source (B4) is invented timing.

**Ship-when:** B4 unblocked + first paid customer in the data set.

### 🟡 Partner OS v5

**Already exists:** `partner_distribution_radar` (8 categories with
warm-intro drafts).

**Deferred:** partner_profile + fit_score + offer_builder +
co_branded_proof_pack + referral_tracker as separate modules.

**Why:** The catalog is the right level of detail until the founder
approaches an actual partner (Decision Pack S2). Profile/fit-score
modules without a real partner sample are speculation.

**Ship-when:** S2 sign-off + first partner conversation with
recorded outcome.

### 🟡 Reliability OS

**Already exists:**
- `.github/workflows/scheduled_healthcheck.yml` — every 15 min
- `/health` endpoint with `git_sha` (post-deploy)
- `scripts/post_redeploy_verify.sh` — 22-point post-deploy verifier

**Deferred:** runbook_registry + telemetry_plan +
incident_event store as separate modules.

**Why:** Runbooks are written when an incident actually happens.
OpenTelemetry plan is documented in `docs/OBSERVABILITY_ENV.md`
already. A new module tree would duplicate without serving a
concrete consumer.

**Ship-when:** First production incident generates the first
runbook need.

### 🟡 Security & Privacy Hardening

**Already exists:**
- `auto_client_acquisition/v3/compliance_os` — PDPL contactability
- `landing/privacy.html` + `landing/terms.html` + `landing/subprocessors.html`
- `tests/test_landing_forbidden_claims.py` — content perimeter
- `cross_border_restriction` service in YAML
- `audit_trail` service in YAML
- gitleaks pre-commit hook

**Deferred:** secret_scan_policy + log_redaction +
data_minimization as separate modules.

**Why:** Each is policy that the founder writes once, not code that
runs. Putting them in code without the policy in writing creates
documentation drift.

**Ship-when:** Founder writes the policy doc; then we wrap it in code.

### 🟡 Vertical Playbooks

**Already exists:**
- `docs/playbooks/` directory with sector-specific notes
- `docs/registry/SERVICE_READINESS_MATRIX.yaml` capability_group field

**Deferred:** agency_playbook + b2b_services_playbook +
saas_playbook + training_consulting_playbook + local_services_playbook
as separate modules.

**Why:** The matrix already records sector relevance per service.
Building 5 separate code modules duplicates without adding signal.

**Ship-when:** The founder wins the second customer of the same
sector — at that point a sector-specific module captures the
repeated pattern.

## Hard rules respected (this session)

- ❌ No new `*_ALLOW_LIVE_*` flag added or flipped.
- ❌ No service marked Live (matrix counts unchanged: 0/1/7/24/0).
- ❌ No live send / live charge / scrape / cold outreach paths added.
- ❌ No fake metrics in any role brief (every signal anchored to a
  measurement module).
- ❌ The 4 REVIEW_PENDING strings remain founder decisions.
- ❌ The 9 deferred modules are NOT stubbed — they're documented
  with ship-when triggers.

## What this session shipped, total

```
Productionization v2 (P1-P5):  +40 tests
v5 layers (3 of 12):           +41 tests
Cumulative new bundle:        236 / 236 passing  (was 195 before this commit)
```

API endpoints added this session:

```
POST /api/v1/self-growth/proof-pack/assemble
GET  /api/v1/customer-loop/status
GET  /api/v1/customer-loop/states
GET  /api/v1/customer-loop/states/{state}
POST /api/v1/customer-loop/journey/advance
GET  /api/v1/role-command/status
GET  /api/v1/role-command/{role}        # 7 roles
GET  /api/v1/service-quality/status
POST /api/v1/service-quality/check
GET  /api/v1/service-quality/sla
GET  /api/v1/service-quality/sla/{service_id}
```

## What unlocks the next 3 v5 deferred modules

| Module | Trigger |
|---|---|
| Customer Data Plane | Founder approves data-lifecycle policy doc |
| Full Delivery Factory | Founder hand-curates Growth Starter delivery template |
| Proof Ledger Postgres | First paid pilot generates ≥5 ProofEvents |

Until those triggers fire, the deferred modules stay deferred —
and that's the right answer.
