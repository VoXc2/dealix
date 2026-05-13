# Agent Experience (AX) — Enterprise Governance

**Layer:** L5 · Enterprise Governance
**Owner:** Product Design Lead
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [AGENT_EXPERIENCE_AX_AR.md](./AGENT_EXPERIENCE_AX_AR.md)

## Context
Enterprise AI adoption fails not because the model is wrong but because the experience is opaque. Users do not trust outputs they cannot question, sources they cannot see, or actions they cannot stop. Agent Experience (AX) is the user-facing surface of governance: it converts agent identity, autonomy, provenance, and approval flow into a credible, controllable interaction. AX builds on the design grammar in `docs/DEALIX_DESIGN_LANGUAGE.md`, the brand in `docs/BRAND_PRESS_KIT.md`, and the observability surface in `docs/AI_OBSERVABILITY_AND_EVALS.md`.

## What good AX means
- **Knows the limits.** The user can tell at a glance what the agent can and cannot do.
- **Explains uncertainty.** Confidence and risk are surfaced; the agent does not pretend to know what it doesn't.
- **Shows sources.** Every claim is traceable to a source the user can inspect.
- **Asks for approval when needed.** No silent escalations; every Class-C/D action surfaces an approval moment.
- **Logs actions.** What was done, when, by whom, and for which user is visible.
- **Allows correction.** The user can correct, reject, or override the agent's output, and the correction is captured for learning.

## UI principles
Every Dealix-built or Dealix-recommended AI UI surface must show:

- **Task status** — what the agent is doing, what stage it is in, expected completion.
- **Data sources** — which records, datasets, or documents the agent used.
- **Confidence / risk** — explicit, not implied; ideally a score and a one-line reason.
- **Required approval** — when applicable, who is the approver and what is the approval scope.
- **Audit trail** — link from the output back to its `ai_run_id` and provenance record.
- **Correction path** — easy way to dispute, edit, or reject the output.

## Sample UI
A representative compact output rendering:

```
RevenueAgent result:
Score: 82
Reasons: sector fit, city priority, estimated value
Risks: source missing for phone
Approval: required before outreach
```

The block is rendered consistently across reports, dashboards, and inline assistant surfaces. The provenance link and the correction action are always one click away.

## Anti-patterns
The following patterns are explicitly disallowed in Dealix-built UIs:

- A confident-sounding answer with no source link.
- A "go" button that triggers a Class-D action without explicit approval moment.
- A confidence number with no human-readable reason.
- A status indicator that pretends success when the underlying run was blocked.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Provenance record, action class, approval state | UI block rendering rules | Design + Tech | Per surface |
| User corrections | Learning signals + correction logs | Tech + Governance | Continuous |
| Design language updates | Updated AX patterns | Design Lead | Per release |

## Metrics
- Approval-Moment Compliance — % of Class-C/D actions that surfaced an explicit approval moment.
- Source-Link Coverage — % of factual claims in outputs that carry a clickable source link.
- Correction Capture Rate — % of user corrections recorded with reason for learning.
- User-Trust Pulse — quarterly survey score on "I trust the AI agents I work with" (1–5).

## Related
- `docs/DEALIX_DESIGN_LANGUAGE.md` — visual + interaction grammar
- `docs/BRAND_PRESS_KIT.md` — brand tone for AI surfaces
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability surface AX exposes
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
