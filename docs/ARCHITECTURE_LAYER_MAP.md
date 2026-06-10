# Architecture Layer Map — خريطة الطبقات

> Purpose: the canonical-name → existing-folder mapping that tells builders how the conceptual Dealix layers (data_os, governance_os, revenue_os, proof_os, value_os, capital_os, client_os, adoption_os, friction_log, workflow_os, agent_os, evidence_control_plane_os) are realized in the current repository. Existing folders are **not renamed**. New canonical folders **compose** them.

The Dealix Constitution names twelve canonical operating modules. The repository, grown across many waves, contains those capabilities under their historical folder names. This document is the bridge.

## The map — الخريطة

| Canonical Module | Existing Repo Location | Status |
|------------------|------------------------|--------|
| `data_os` | `customer_data_plane/`, `consent_table.py`, `enrichment_provider.py`, `connectors/` | W |
| `governance_os` | `agent_governance/`, `compliance_os/`, `compliance_os_v12/`, `safety_v10/`, `channel_policy_gateway/`, `tool_guardrail_gateway/`, `safe_send_gateway.py`, `whatsapp_safe_send.py` | W |
| `revenue_os` | `revenue_os/` | E |
| `proof_os` | `proof_engine/`, `proof_ledger/`, `proof_to_market/` | W |
| `value_os` | (new) | N |
| `capital_os` | (new) | N |
| `client_os` | `customer_company_portal.py`, `customer_brain/`, `customer_inbox_v10/`, `customer_success/`, (new `badges.py`) | W |
| `adoption_os` | (new — wraps `customer_success.health_score.compute_adoption`) | W |
| `friction_log` | (new) | N |
| `workflow_os` | `workflow_os_v10/` | E |
| `agent_os` | `agents/`, `agent_governance/`, `agent_observability/`, `ai_workforce_v10/` | E (canonical wrap in Wave 4 backlog) |
| `evidence_control_plane_os` | `proof_ledger/evidence_export.py`, `proof_engine/evidence.py` | E (canonical wrap in Wave 3 backlog) |

### Status legend — الرموز

- **W — Wrapper.** The canonical module exists as a thin facade folder that imports from one or more existing folders. Existing folders keep their names and their tests. The wrapper exposes one stable surface that the rest of the system imports.
- **N — Net-new.** The canonical module does not yet exist in the repository and is being created fresh by the current wave. No existing folder is renamed.
- **E — Existing-named.** The canonical name already matches a folder in the repository. No wrapping needed. The folder is the canonical module.
- **E (canonical wrap in Wave X backlog)** — the folder exists under the canonical name, but a stricter facade is scheduled to land in a later wave.

## What "wrapper" means in practice — معنى الـ wrapper

A wrapper is a folder whose only job is to:

- Re-export a small set of public functions and classes from existing folders under a canonical namespace.
- Define a stable, documented surface (the API surface declared in the wave plan).
- Add canonical types and enums that did not exist before (e.g., `GovernanceDecision` for `governance_os`).
- Compose existing rules. For example, `governance_os.runtime_decision.decide()` calls into `channel_policy_gateway`, `safe_send_gateway`, `safety_v10.output_validator`, and `compliance_os_v12` and returns a single, strictest decision.

A wrapper **never**:

- Reimplements logic that already exists in an existing folder.
- Renames an existing folder.
- Removes or hides an existing public API in a way that breaks consumers.
- Drifts from its underlying folders silently — every wrapper imports the underlying capability rather than copying it.

## Why existing folders are not renamed — لماذا لا تُعاد التسمية

Rename churn is a recurring failure mode in fast-moving repositories: tests break, imports drift, search indexes go stale, blame trails are lost, and downstream consumers stop trusting that "the name on the door" is the right one to import.

The Layer Map avoids that entirely. Existing folders keep their names, their tests, their history, and their owners. New canonical folders compose them. When a builder asks "where do I import governance from", the answer is **`governance_os`** — a small, documented surface — regardless of whether the underlying logic lives in `safety_v10`, `compliance_os_v12`, `channel_policy_gateway`, or all three.

## How new canonical folders are introduced — كيف تُضاف الطبقات الجديدة

When the map shows a row as **N (net-new)**:

- The folder is created with the canonical name (e.g., `value_os/`, `capital_os/`, `friction_log/`).
- The folder ships with a single, documented surface aligned to the corresponding doc in this `docs/` tree. For example, `capital_os/capital_ledger.py` is the surface documented in [CAPITAL_LEDGER.md](./09_capital_os/CAPITAL_LEDGER.md).
- The folder may, over time, absorb logic that previously lived elsewhere — but only by explicit refactor PRs, never by silent migration.

When the map shows a row as **W (wrapper)**:

- The wrapper folder is created (e.g., `data_os/`, `proof_os/`, `client_os/`, `adoption_os/`).
- It re-exports the public surface from underlying folders, adds canonical types, and composes rules.
- Underlying folders remain the source of truth for tests and historical context.

When the map shows a row as **E (existing-named)**:

- No wrapper is needed today. The folder already matches the canonical name.
- If a stricter facade is scheduled (Wave 3 / Wave 4 backlog), the row makes that explicit.

## How to use the map — كيف تُستخدم

- **Builders:** before adding a new module, find the canonical row. Add to the existing folder when the row is **E**, add inside the wrapper when the row is **W**, or create the new folder when the row is **N**.
- **Reviewers:** if a PR creates a new folder that duplicates a canonical row, request a redirect to the canonical surface.
- **Docs writers:** when documenting a capability, link to the canonical doc in `docs/0X_*` and let the doc reference the underlying folders, not the other way around.

## Cross-references

- [Dealix Constitution](./00_constitution/DEALIX_CONSTITUTION.md) — the operating equation that lists the canonical layers.
- [Non-Negotiables](./00_constitution/NON_NEGOTIABLES.md) — the rules each layer is built to enforce.
- Layer docs: [Source Passport](./04_data_os/SOURCE_PASSPORT.md), [Runtime Governance](./05_governance_os/RUNTIME_GOVERNANCE.md), [Proof Pack Standard](./07_proof_os/PROOF_PACK_STANDARD.md), [Value Ledger](./08_value_os/VALUE_LEDGER.md), [Capital Ledger](./09_capital_os/CAPITAL_LEDGER.md), [Client Workspace MVP](./11_client_os/CLIENT_WORKSPACE_MVP.md), [Adoption Score](./12_adoption_os/ADOPTION_SCORE.md).
