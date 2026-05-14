# Adoption Score and Retainer Readiness — درجة التبني وأهلية الـ retainer

> Purpose: define how Dealix measures client adoption, the five-tier classification, the drivers and trend reporting, and the RetainerReadiness gate that determines when a client may move from a one-time sprint to a monthly RevOps OS retainer.

Adoption is the single best leading indicator of whether a Dealix engagement will become a healthy long-term relationship or a one-off project. Adoption Score is the measured number. RetainerReadiness is the deterministic gate that uses it.

## Score math — حساب الدرجة

The adoption score wraps two existing functions in `customer_success.health_score`:

```
adoption_score = round(
    0.6 * compute_adoption()    # breadth — how many parts of Dealix are in use
  + 0.4 * compute_engagement()  # activity — how regularly they are used
)
```

Components:

- **`compute_adoption()` (breadth, weight 0.6)** — measures how many Dealix capabilities are in active use by the client: Source Passports declared, workflows with named owners, drafts reviewed, approvals logged, Proof Packs received, value entries reviewed. Breadth is the dominant component because a client using one capability heavily is not yet adopting Dealix — they are using a single feature.
- **`compute_engagement()` (activity, weight 0.4)** — measures the regularity of use over a rolling window: logins, approvals, draft reviews, governance event resolutions. Activity is the smaller weight because spikes of activity without breadth do not indicate adoption.

Both functions already exist in `customer_success.health_score`. The adoption_os wrapper composes them into a single score on `[0, 100]`. See [ARCHITECTURE_LAYER_MAP.md](../ARCHITECTURE_LAYER_MAP.md).

## Tier classification — التصنيف

The score maps to one of five tiers:

| Score range | Tier | Reading |
|-------------|------|---------|
| < 20 | **latent** | Client signed but not operating Dealix yet. |
| 20 – 39 | **exploring** | Some capabilities in use; no full loop yet. |
| 40 – 69 | **active** | Full loop in use occasionally; gaps in breadth or regularity. |
| 70 – 89 | **embedded** | Full loop in regular use; client treats Dealix as an operating layer. |
| ≥ 90 | **power** | Full loop in regular use across multiple workflows; high reuse of capital assets. |

Tier transitions are not celebratory by themselves. The tier matters because it gates retainer eligibility.

## Drivers — المحركات

Each adoption score is reported alongside its **top 3 drivers**: the three components that contributed most to the current score (positively or negatively). Drivers are concrete, e.g.:

- "+ 9: three Source Passports declared this period"
- "+ 7: two Proof Packs reviewed by workflow owner"
- "− 5: no approvals logged in last 14 days"

Drivers turn an abstract number into a specific next action and feed the `adoption_push` recommendation in [CLIENT_WORKSPACE_MVP.md](../11_client_os/CLIENT_WORKSPACE_MVP.md).

## Trend reporting — الاتجاه

The score is reported with a **trend vs the previous period**:

```json
{
  "adoption_score": 73,
  "tier": "embedded",
  "trend_vs_previous": "+6",
  "top_drivers": [
    "+ 9: ...",
    "+ 4: ...",
    "- 2: ..."
  ]
}
```

Trend windows are configured per engagement type. A retainer client typically sees a monthly trend; a sprint client sees a per-milestone trend.

## RetainerReadiness gate — بوابة الـ retainer

The RetainerReadiness gate determines whether a client may move from a one-time [Revenue Intelligence Sprint](../03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md) to a monthly RevOps OS retainer. The gate is deterministic and conjunctive:

```python
def retainer_readiness(state) -> RetainerReadinessResult:
    eligible = (
        state.adoption_score >= 70
        and state.proof_score >= 80
        and state.workflow_owner_present
        and state.governance_risk_controlled
    )
    return RetainerReadinessResult(
        eligible=eligible,
        gaps=collect_gaps(state),
        recommended_offer=choose_offer(state),
    )
```

Each predicate:

- **`adoption_score >= 70`** — the client is in `embedded` or `power` tier.
- **`proof_score >= 80`** — at least one Proof Pack from the prior engagement reached the **case candidate** or strong **sales support** tier. See [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).
- **`workflow_owner_present`** — a named human at the client owns the workflow and has approved at least one external action.
- **`governance_risk_controlled`** — the engagement has no open `BLOCK` or `ESCALATE` events older than the configured threshold.

If any predicate is false, `eligible = false`. The gate then returns:

- **`gaps`** — the specific predicates that failed, with one short remediation line each (e.g., "adoption score 64; needs +6 in breadth").
- **`recommended_offer`** — one of: a second sprint focused on a specific workflow, a targeted remediation engagement, or "pause until adoption catches up". The recommendation is deterministic given the gap pattern.

If all predicates are true, the gate returns `eligible = true` and `recommended_offer = "monthly_revops_retainer"`.

## Why the gate is conjunctive — لماذا تكون كل الشروط مطلوبة

Each predicate guards a distinct failure mode:

- High adoption with low proof → the client is busy but value is unproven. A retainer would compound noise.
- High proof with low adoption → the project succeeded but the client is not operating. A retainer would be unused.
- Both scores high without a workflow owner → there is no one inside the client to receive the operating cadence. A retainer would stall.
- All three with open governance risk → unresolved blocks become production incidents in a retainer. A retainer would crystallize them.

Any single weakness collapses the retainer. The gate is the constitutional refusal to "sell into a hole".

## What this file does not do — حدود هذا المستند

- It does not define the retainer's scope or price. That lives behind the gate.
- It does not change the score formula casually. Changes require a constitutional amendment and a re-baselining of historical scores.
- It does not bypass the gate for commercial reasons. A client below the gate gets a remediation path, not a retainer.

## Cross-references

- [Revenue Intelligence Sprint](../03_commercial_mvp/REVENUE_INTELLIGENCE_SPRINT.md), [Proof Pack Standard](../07_proof_os/PROOF_PACK_STANDARD.md), [Client Workspace MVP](../11_client_os/CLIENT_WORKSPACE_MVP.md), [Architecture Layer Map](../ARCHITECTURE_LAYER_MAP.md).
