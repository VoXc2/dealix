# Operating System Map — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Platform Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [OPERATING_SYSTEM_MAP_AR.md](./OPERATING_SYSTEM_MAP_AR.md)

## Context
Dealix is built and sold as an operating system, not a set of point
tools. The Operating System Map is the single picture of how a request
enters Dealix, gets decided on, is delivered, governed, surfaced, and
fed back into learning. It is the architectural contract referenced by
`docs/BEAST_LEVEL_ARCHITECTURE.md`,
`docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`, and the operating
constitution in `docs/DEALIX_OPERATING_CONSTITUTION.md`. Every Layer-3
service slots into one or more of these layers.

## Layered Map
Dealix systems map across six layers. Every product, workflow, and
service belongs in exactly one primary layer.

### Input Layer
- **Request Intake** — inbound requests from web, partners, agencies.
- **Client Intake** — qualified clients onboarded into workspaces.
- **Data Intake** — pulls and uploads of operational data (CSV, CRM
  export, API).
- **Document Intake** — file ingestion for the Knowledge Capability.

### Decision Layer
- **Qualification** — is this client a fit?
- **Sellability** — does this request match our service ladder?
- **Scope** — what is the exact deliverable and capability uplift?
- **Governance** — what risk class, what approvals, what controls?
- **Build** — buy vs build, model choice, prompt selection.
- **Pricing** — service price from `OFFER_LADDER_AND_PRICING.md`.
- **Retainer** — convert Sprint into Pilot/Retainer when conditions met.

### Execution Layer
- **Delivery Workbench** — internal cockpit where projects run.
- **AI Workforce** — set of agents per capability.
- **Workflow Engine** — orchestrates steps, approvals, timeouts.
- **LLM Gateway** — single chokepoint for model calls, attaches ACL,
  enforces taxonomy.

### Trust Layer
- **Runtime Governance** — the checks in
  `governance/RUNTIME_GOVERNANCE.md`.
- **PII Redaction** — detection and redaction service.
- **Permission Mirroring** — see `governance/PERMISSION_MIRRORING.md`.
- **Audit Logs** — append-only event log.
- **Proof Ledger** — client-facing proof events.

### Output Layer
- **Reports** — periodic management reports.
- **Dashboards** — live dashboards inside the workspace.
- **Drafts** — generated drafts awaiting human review.
- **Workflows** — running automations.
- **Assistants** — chat assistants per capability.
- **Proof Packs** — delivery proof packages for clients.

### Learning Layer
- **Post-Project Review** — structured retro per engagement.
- **Capital Ledger** — accumulated IP, datasets, prompts.
- **Feature Backlog** — feature_candidates table.
- **Playbook Updates** — versioned playbooks per service.
- **Market Intelligence** — signals from won/lost deals.

## Layer Rules
- Every system has exactly one primary layer; secondary layers are
  documented but not duplicated.
- The Trust Layer sits between Execution and Output: nothing reaches
  Output without passing Trust.
- The Learning Layer reads from every other layer but only writes back
  through playbooks and prompt updates.
- New systems require an explicit layer assignment before they can be
  built.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| All inbound requests, data, documents | Routed projects, workspaces, datasets | Platform Lead | Continuous |
| Decision Layer outputs | Sprint plans, governance memos, pricing | Founder, Delivery Lead | Per engagement |
| Execution Layer state | Reports, dashboards, drafts, proof packs | Delivery Lead | Per delivery |
| Learning Layer signals | Updated playbooks, feature candidates | Founder | Monthly |

## Metrics
- **Layer Conformance** — share of systems with one documented primary
  layer (target = 100%).
- **Trust Layer Coverage** — share of Output-Layer artefacts that
  passed Trust (target = 100%).
- **Decision Layer Cycle Time** — median hours from intake to
  decision (target ≤ 48 hours).
- **Learning Layer Yield** — count of playbook updates per month
  (target ≥ 2).

## Related
- `docs/BEAST_LEVEL_ARCHITECTURE.md` — deeper architecture document
  this map summarises.
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability plan whose
  surfaces map onto the layers above.
- `docs/DEALIX_OPERATING_CONSTITUTION.md` — operating rules that bind
  the layers.
- `docs/product/MANAGEMENT_API_SPEC.md` — sibling API spec that surfaces
  these layers programmatically.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
