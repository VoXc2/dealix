# Productization System — Operating Manual · CEO/CTO/CSO

**Layer:** Operating Manual · CEO/CTO/CSO
**Owner:** CTO
**Status:** Draft
**Last reviewed:** 2026-05-13
**Arabic mirror:** [PRODUCTIZATION_SYSTEM_AR.md](./PRODUCTIZATION_SYSTEM_AR.md)

## Context

Dealix becomes durable when manual work becomes reusable. The
Productization System is the rule set that decides what to
productize, when to productize it, and how far along the
productization ladder it should move. It implements the
"Sprint → Proof → Retainer → Product → Standard" sequence stated
in `docs/company/DEALIX_CEO_STRATEGY.md` and feeds the
`docs/product/PRODUCTIZATION_LEDGER.md`. It also enforces the
"no SaaS before proven repetition" rule from
`docs/BEAST_LEVEL_ARCHITECTURE.md`.

## Productization Triggers

A manual step becomes a **product candidate** if any of the
following is true:

- Repeated **3+ times** across two or more clients.
- Takes **2+ hours per occurrence**.
- Reduces delivery risk if standardized (eval, governance, QA).
- Improves margin meaningfully when standardized.
- Supports a sellable service that is already in the catalog.
- Can be tested with a deterministic eval (not "trust me").

If none of the above is true, do not productize yet.

## Productization Stages

Productization is a six-stage ladder. A step ascends one stage at a
time. A step cannot skip stages.

| Stage | Name | Definition | Built by |
|---|---|---|---|
| 1 | **Manual** | Done end-to-end by a human, no codified pattern | Delivery |
| 2 | **Template** | A documented template (doc, sheet, prompt) reused | Delivery + CSM |
| 3 | **Script** | Code that automates part of the step (cli, notebook) | CTO + Delivery |
| 4 | **Internal Tool** | A team-only tool with UI/CLI, evals, governance | CTO |
| 5 | **Client-visible Feature** | A surface inside the client workspace | CTO + Product |
| 6 | **SaaS Module** | A productized module with self-serve onboarding | CTO + Product |

The **rule of no SaaS without internal tool**: a step cannot move to
Stage 6 until Stage 4 has proven repeated value across at least two
clients with QA pass and evals.

## Feature Candidate Schema

Every product candidate is captured as a structured record in the
Productization Ledger.

```json
{
  "feature_id": "feat_2026_05_lead_dedupe",
  "name": "Arabic-aware lead dedupe",
  "current_stage": "template",
  "candidate_source": "Repeated 4x across 3 clients (RevOps Sprint)",
  "triggers_passed": [
    "repeated_3plus",
    "two_hours_plus",
    "deterministic_eval_possible"
  ],
  "expected_margin_impact_pct": 12,
  "owner": "ai_lead",
  "blocked_until": null,
  "evals_required": [
    "arabic_name_normalization_accuracy",
    "fp_rate_on_company_clones"
  ],
  "governance_required": [
    "audit_log_on_merge",
    "client_approval_on_destructive_merge"
  ],
  "next_stage_criteria": [
    "Script with CLI in repo",
    "Eval > 0.92 on labeled set"
  ],
  "last_reviewed": "2026-05-13"
}
```

## Decision Flow

1. **Spot the repetition** — Delivery flags a manual step.
2. **Score the triggers** — at least one must pass.
3. **Open a feature_candidate record** — write into the Ledger.
4. **Promote stage** — only after criteria for next stage met and
   reviewed by CTO.
5. **Cap at Stage 4 until 2-client proof** — enforced rule.

## Anti-Patterns

- Building an internal tool because "it would be cool" — fails
  trigger test.
- Building a client-visible feature off a single client request —
  violates Commandment 7 (`docs/company/COMMANDMENTS.md`).
- Skipping evals — every promotion above Stage 2 requires an eval.
- Calling something "productized" when it still needs founder
  intervention — Stage 3 minimum requires no founder during run.

## Cadence

- **Weekly** — Delivery flags repetition signals into the Ledger.
- **Monthly** — CTO promotes/declines stages based on criteria.
- **Quarterly** — CEO reviews top candidates for strategic build.

## Interfaces

| Inputs | Outputs | Owners | Cadence |
|---|---|---|---|
| Repetition signals, delivery logs | Feature candidate records | Delivery + CTO | Weekly |
| Stage criteria | Promote / decline | CTO | Monthly |
| Productization Ledger | Strategic build queue | CEO | Quarterly |

## Metrics

- **# active candidates in Ledger** — informational.
- **Average stage progression time** — track per stage.
- **# Stage 4+ items reused across 2+ clients** — target ≥3.
- **# SaaS modules built without Stage 4 proof** — target 0.

## Related

- `docs/BEAST_LEVEL_ARCHITECTURE.md` — architecture supporting productization.
- `docs/AI_STACK_DECISIONS.md` — AI stack choices.
- `docs/product/PRODUCTIZATION_LEDGER.md` — sibling live ledger.
- `docs/product/QUALITY_AS_CODE.md` — quality enforcement.
- `docs/product/PLATFORM_PATH.md` — platform path sibling.
- `docs/company/SERVICE_CATALOG_V1.md` — sellable services source.
- `docs/DEALIX_OPERATING_LAYERS_INDEX.md` — master index.

## Change log

| Date | Author | Change |
|---|---|---|
| 2026-05-13 | Sami | Initial draft. |
