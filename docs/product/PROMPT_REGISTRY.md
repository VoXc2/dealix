# Prompt Registry — Capability Operating Model

**Layer:** L2 · Capability Operating Model
**Owner:** Founder / Prompt Owner per service
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PROMPT_REGISTRY_AR.md](./PROMPT_REGISTRY_AR.md)

## Context
Prompts are production code. Treating them as throwaway strings is how
AI-enabled businesses lose quality, safety, and capital value. The
Prompt Registry is the versioned, owner-bound, eval-attached catalogue
of every prompt Dealix uses on client work. It plugs into the
observability and evals stack in `docs/AI_OBSERVABILITY_AND_EVALS.md`,
the model routing in `docs/AI_MODEL_ROUTING_STRATEGY.md`, and the
stack decisions in `docs/AI_STACK_DECISIONS.md`.

## Registry Table
The canonical registry shape:

| Prompt | Version | Service | Purpose | Owner | Eval |
|---|---|---|---|---|---|
| lead_scoring_prompt | v1.0 | Lead Intelligence | score account fit | Sami | lead_eval |
| outreach_draft_prompt | v1.0 | Lead Intelligence | generate safe drafts | Sami | claims_eval |
| citation_answer_prompt | v1.0 | Company Brain | answer with source | Sami | rag_eval |

Every prompt has a stable name, a semantic version (`vMAJOR.MINOR`), a
named service, a single purpose, a named owner, and at least one eval.

## Required Content per Prompt
Each prompt record must contain:

- **Purpose** — one sentence describing what the prompt does.
- **Input schema** — fields, types, and required redactions.
- **Output schema** — exact structure the caller relies on.
- **Forbidden behaviour** — claims and actions the model must not
  produce (e.g. "must not guarantee outcomes", "must not invent
  testimonials").
- **Examples** — at least 3 worked examples spanning happy path, edge
  case, and refusal case.
- **Eval tests** — the eval IDs from `EVALUATION_REGISTRY.md` that gate
  release.
- **Version history** — change log linking changes to incidents,
  evals, and capability decisions.

## Lifecycle
1. **Draft** — written in a feature branch with examples and forbidden
   behaviour.
2. **Eval** — runs against the registered evals; must hit the gating
   thresholds.
3. **Pilot** — used on at most one project for at most one week, with
   100% human review.
4. **Release** — promoted to `v1.0` (or next semver) and added to the
   registry.
5. **Deprecate** — replaced by a newer version; old version remains
   queryable for audit.

## Governance Rules
- No client-facing run may use an unregistered prompt.
- Bumping a major version requires re-eval; bumping a minor version
  requires regression eval on the existing eval suite.
- Every prompt change must be linked to the AI Run Ledger so the
  prompt-to-output trace remains intact.
- High-risk prompts (Action Taxonomy Level ≥ 4) require a second
  reviewer before release.

## Storage and Distribution
- The registry lives in the platform and is exposed via the Management
  API.
- The LLM Gateway only loads prompts by ID and version; ad-hoc strings
  in code are rejected.
- Prompts are part of the Dealix Capital Ledger: they accrue value as
  evals harden and incidents shape forbidden behaviour.

## Interfaces
| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Prompt drafts, eval results, incident notes | Versioned prompt records | Prompt Owner | Per change |
| Registry | Prompt fetched by ID+version at runtime | LLM Gateway | Per call |
| Audit query | Prompt usage trace | Governance Lead | On demand |

## Metrics
- **Registered Coverage** — share of client-facing runs using a
  registered prompt (target = 100%).
- **Eval Pass Rate at Release** — share of prompt releases that pass
  the gating eval on first attempt (target ≥ 80%).
- **Forbidden-Behaviour Incidents** — count of incidents traced to a
  forbidden behaviour breach (target = 0).
- **Time-to-Promote** — median hours from draft to release (target ≤ 5
  working days).

## Related
- `docs/AI_OBSERVABILITY_AND_EVALS.md` — observability surface for
  prompts.
- `docs/AI_MODEL_ROUTING_STRATEGY.md` — model routing that pairs with
  prompt versions.
- `docs/AI_STACK_DECISIONS.md` — stack decisions referencing the
  registry.
- `docs/product/EVALUATION_REGISTRY.md` — sibling evaluation registry.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log
| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft |
