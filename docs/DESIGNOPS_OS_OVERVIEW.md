# DesignOps OS — Overview

## What it is
DesignOps OS turns each Dealix service into a **customer-ready artifact** —
a Mini Diagnostic, a Proposal, a Pricing reference, a Proof Pack, a Weekly
Executive Pack. Each artifact is generated locally, reviewed by the founder,
and only then sent manually. No artifact leaves the machine without explicit
founder action.

DesignOps OS is the **packaging + safety + export** layer on top of the
service modules already in `auto_client_acquisition/`. It does not replace
them — it composes them.

## Module map (`auto_client_acquisition/designops/`)
| File | Role |
|---|---|
| `__init__.py` | Public re-exports (`export_artifact`). |
| `exporter.py` | Writes manifest+content to disk as md/html/json. **No upload.** |
| `design_system.py` *(planned)* | Tokens (color, type, spacing) + bilingual primitives. |
| `safety_gate.py` *(planned)* | Forbidden-token + claim scan; defaults `safe_to_send=False`. |
| `skill_registry.py` *(planned)* | The 15 skills + scenario metadata. |
| `brief_builder.py` *(planned)* | Normalizes a service call into a render brief. |
| `generators/` *(planned)* | One file per artifact type (mini_diag, proposal, ...). |

## The 15 skills
Names + scenario only. Full table is in `DESIGNOPS_SKILL_CATALOG.md`.

1. `mini_diagnostic` — first-call summary for a warm intro.
2. `full_diagnostic` — paid diagnostic deliverable.
3. `proposal_page` — scope + price + next step, bilingual.
4. `pricing_reference` — internal pricing card, founder-only.
5. `invoice_draft` — Moyasar-ready draft (no live charge).
6. `proof_pack` — day-7 evidence bundle for the customer.
7. `executive_weekly_pack` — founder weekly review.
8. `objection_handler` — bilingual reply to a known objection.
9. `warm_intro_message` — first-touch DM template.
10. `pilot_recap` — end-of-pilot summary + decision ask.
11. `landing_block` — single landing-page section, copy + layout.
12. `case_card` — one-pager for a closed engagement (anonymized).
13. `rfp_one_pager` — bid response one-pager.
14. `internal_decision_pack` — founder decision memo.
15. `ops_runbook_card` — operational checklist for a recurring task.

## Endpoint map (`/api/v1/designops/*`) — planned
- `POST /api/v1/designops/generate/<skill_id>` — render an artifact (returns manifest + content).
- `POST /api/v1/designops/export` — write manifest+content to local disk.
- `GET  /api/v1/designops/skills` — list registered skills.
- `GET  /api/v1/designops/safety/check` — run the safety gate against a draft.

All endpoints are local + admin-only. None upload or send.

## Hard rules baked in
1. **Default `safe_to_send=False`.** Every generated manifest carries it.
   Founder must flip it after review.
2. **Eight forbidden tokens.** See `DESIGNOPS_ARTIFACT_SAFETY.md` — any
   match blocks the safe-to-send flip.
3. **No upload, no send, no external HTTP** in `designops/`. Exporter
   writes to disk only.
4. **Filename sanitization.** `artifact_id` is reduced to `[a-zA-Z0-9_-]`
   before any file is touched.
5. **Bilingual where customer-facing** (AR + EN side-by-side).
6. **No marketing claim** ("guaranteed", "best", "#1") in any artifact.
7. **No real customer name** in any committed doc or example.
8. **PDF/PPTX deferred.** Local md/html/json only until a founder
   explicitly approves a sandboxed PDF renderer.

## How it composes with v5 / v6
- `diagnostic_engine` → feeds `mini_diagnostic` + `full_diagnostic`.
- `finance_os.invoice_draft` → backs `invoice_draft` skill (still no live charge).
- `finance_os.pricing_catalog` → backs `pricing_reference` skill.
- `proof_ledger` → feeds `proof_pack`.
- `executive_reporting` → feeds `executive_weekly_pack`.
- `compliance_os` → enforced by `safety_gate` (PDPL alignment).
- `approval_center` → owns the founder review banner.

DesignOps OS is the customer-facing veneer. The underlying numbers and
records still come from the v5/v6 modules.
