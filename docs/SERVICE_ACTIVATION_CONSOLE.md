# Service Activation Console

The Service Activation Console (`/status.html`) is the public-facing
honesty page for Dealix. It renders every service in the catalog as a
rich bilingual card with: status, customer value, what's ready, what's
missing, the next activation step, proof metrics, safety boundaries,
and a status-appropriate CTA.

It replaces the previous hardcoded "Live / Pilot / Partial / Target"
table with a data-driven console fed from a single YAML source.

## Why this exists

A page that says "everything works" is weaker than a page that proves
Dealix knows how to run every service safely and in order. The console
forces every service to answer six questions at all times:

1. What's the customer value? (Arabic-first, English secondary)
2. What's ready right now?
3. What's missing before it can flip to Live?
4. What's the activation gate?
5. What's the proof metric?
6. What's the appropriate CTA for this status?

If a service can't answer those, it cannot ship.

## The 8 quality gates

A service may be marked `live` only after **all eight** gates are
explicitly true in the YAML registry under a `gates:` block. The
validator (`scripts/verify_service_readiness_matrix.py`) refuses to
pass otherwise.

| # | Gate | Meaning |
|---|---|---|
| 1 | `inputs` | Required inputs are documented and available. |
| 2 | `workflow` | Every step from receive → persist is wired. |
| 3 | `agent_role` | The AI/automation role is specified. |
| 4 | `human_approval` | Approval boundary exists where it must. |
| 5 | `safe_tool_gateway` | All external tool calls go through policy. |
| 6 | `deliverable` | A real, observable customer-visible output. |
| 7 | `proof_metric` | A metric records that the service ran. |
| 8 | `test_or_evidence` | Tests, smoke, or recorded evidence on disk. |

Until those eight gates are explicitly green, the service stays in
`partial`, `pilot`, `target`, or `blocked`.

## Status definitions

| Status | Meaning | CTA |
|---|---|---|
| `live` | All 8 gates pass; safe to invite real customers. | جرّب الآن · Try it now |
| `pilot` | Running in a hand-held trial with the founder. | اختبر مع مؤسس Dealix · Pilot with the founder |
| `partial` | Some pieces work; specific blockers documented. | شاهد خطة التفعيل · See the activation plan |
| `target` | On the roadmap; design known, not yet built. | في خارطة الطريق · On the roadmap |
| `blocked` | Cannot ship until an external cause clears. | محظور حتى يزول السبب · Blocked until the cause clears |
| `backlog` | Acknowledged but not currently prioritized. | في القائمة · In the backlog |

## How to add or change a service

1. Edit `docs/registry/SERVICE_READINESS_MATRIX.yaml`. Each service
   needs every field listed in `REQUIRED_SERVICE_FIELDS` inside
   `scripts/verify_service_readiness_matrix.py`.
2. Run the validator:
   ```
   python scripts/verify_service_readiness_matrix.py
   ```
   It must exit `0` and report the expected counts.
3. Run the exporter:
   ```
   python scripts/export_service_readiness_json.py
   ```
   It writes `landing/assets/data/service-readiness.json`.
4. Commit both the YAML and the regenerated JSON. CI runs both and
   fails if the JSON is stale relative to the YAML.

## Forbidden marketing claims

The validator scans every customer-visible field and rejects:

- Arabic: نضمن، مضمون
- English: guaranteed, blast, scrape, scraping, cold (whatsapp/outreach/email/messaging)

Documenting that we *don't* do these things is allowed in
`blocked_actions`, `safe_action_policy`, `risks`, and the
`next_activation_step_*` fields — those describe boundaries, not
promises.

## Bilingual copy guidelines

- Arabic is the primary surface. Saudi-executive register: short,
  confident, clear. Avoid awkward literal translation.
- English is the secondary line. Concise, not the main UX.
- Status labels and CTA text are bilingual side-by-side
  (e.g. "جرّب الآن · Try it now").

## Files

| File | Role |
|---|---|
| `docs/registry/SERVICE_READINESS_MATRIX.yaml` | Source of truth (32 services). |
| `scripts/verify_service_readiness_matrix.py` | Schema + safety validator. |
| `scripts/export_service_readiness_json.py` | YAML → JSON exporter. |
| `landing/assets/data/service-readiness.json` | Generated payload (committed). |
| `landing/assets/js/service-console.js` | Vanilla-JS renderer. |
| `landing/status.html` | Mount shell + counts/filter/cards regions. |
| `landing/styles.css` | `.service-card`, `.service-filter-chip`, etc. |
| `tests/test_service_readiness_matrix.py` | YAML schema + safety tests. |
| `tests/test_service_readiness_frontend_data.py` | Exporter + JSON shape tests. |
| `tests/test_service_activation_console.py` | HTML/JS integration tests. |

## Current state (2026-05-04)

```
SERVICES_TOTAL=32  LIVE=0  PILOT=1  PARTIAL=7  TARGET=24  BLOCKED=0
```

Zero Live is honest — no service has cleared all 8 gates yet. The
console's job is to show that honestly while making the path to Live
visible per-service.

## Top activation priorities

These services are closest to passing all 8 gates. They are listed for
transparency, not as commitments:

1. `lead_intake_whatsapp` — needs OTel traces + opt-out abuse test.
2. `consent_required_send` — needs default-deny test on missing consent.
3. `audit_trail` — needs unified `correlation_id` across all paths.
4. `release_gate` — needs OIDC + readiness validator wired in CI.
5. `enrichment` — needs real provider keys + confidence test.
6. `routing` — needs consent table + KSA quiet-hours test.
7. `outreach_drafts` — needs send-window enforcement test.

Each ships only after its 8 gates explicitly pass.
