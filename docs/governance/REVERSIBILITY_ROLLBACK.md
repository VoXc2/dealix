# Reversibility & Rollback — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Delivery Owner
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [REVERSIBILITY_ROLLBACK_AR.md](./REVERSIBILITY_ROLLBACK_AR.md)

## Context
Every AI-assisted action can be wrong. The governance question is not "can this go wrong?" but "can we undo it, or at least mitigate it, if it does?" This file defines Dealix's reversibility and rollback obligations for AI-assisted workflows. It binds to the incident discipline in `docs/ops/INCIDENT_RUNBOOK.md`, the observability stack in `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md`, and the reliability practices in `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md`. It exists to honor the enterprise principle that *no AI action ships without a known undo or mitigation path*.

## Core principle
An AI-assisted workflow must define rollback or mitigation *before* execution. If an action class cannot be reversed or mitigated, it is escalated and either redesigned or moved to a higher-control class (manual approval, restricted channel, or blocked entirely).

## Internal actions
For AI-driven internal actions (CRM update, internal task, data write):

- **Previous state stored.** The runtime captures the pre-action state for the affected entity, with a retention window long enough to enable rollback.
- **Change log created.** Every action creates a log entry with actor (agent), approver, timestamp, before/after diff, and link to the source run.
- **Rollback owner assigned.** A named Dealix role is responsible for executing rollback within the defined window.
- **Rollback window declared.** Each action class has an expected window (typically minutes to hours) during which rollback is straightforward.

## External actions
For AI-driven external actions (email, message, post, third-party API call):

- **Approval recorded.** Every Class-D action carries an explicit approval token tied to a named human.
- **Preview confirmed.** The final payload and recipient list are confirmed in the approval moment, not at draft time.
- **Recipient list reviewed.** No external send to a list that hasn't been compared against do-not-contact and consent records.
- **Mitigation plan ready.** If the action proves wrong, a documented mitigation (correction email, retraction, follow-up) is executed by a named owner within an agreed time.

## Reports
For AI-assisted reports delivered to clients:

- **Version history.** Every delivered report is versioned with hash and provenance.
- **Correction process.** A documented correction flow that issues a v2 report and notifies the client.
- **Client notification.** When a correction materially changes a decision-relevant fact, the client is notified by the Delivery Owner within an agreed SLA.

## Hard rule
**No action without rollback or mitigation plan.** If neither is feasible, the action is not approved.

## Rollback evidence
Each agent card lists rollback evidence per action class it touches:

| Action Class | Reversible? | Rollback Mechanism | Owner | Window |
|---|---|---|---|---|
| A | n/a | Versioned output replacement | QA Reviewer | n/a |
| B | Yes | Issue v2 with correction note | Delivery Owner | 48h |
| C | Yes | Restore previous state from change log | Technical Owner | 24h |
| D | Mitigation | Correction / retraction message | Delivery Owner | 24h |
| E | Blocked | — | — | — |

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Agent card and workflow definition | Rollback plan per action class | Delivery + Technical | Per release |
| Incident reports | Triggered rollback or mitigation | Incident Owner | Within SLA |
| Client notification triggers | Versioned correction + client comms | Delivery + Client Success | As needed |

## Metrics
- Rollback-Plan Coverage — % of action-producing workflows with documented rollback (target: 100%).
- Mean-Time-to-Rollback — minutes from incident detection to executed rollback or mitigation.
- Mitigation-After-Send Rate — % of mistaken external actions where mitigation was executed within window.
- Client-Notified-After-Correction Rate — % of material report corrections that resulted in formal client notification.

## Related
- `docs/ops/INCIDENT_RUNBOOK.md` — incident runbook this file plugs into
- `docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md` — observability + incident reference
- `docs/BACKEND_RELIABILITY_HARDENING_PLAN.md` — reliability hardening behind rollback infra
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
