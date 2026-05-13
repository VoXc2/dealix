---
title: A/B Experimentation Framework — hypothesis, MDE, sample size, assignment, primary metric, guardrails, rollout
doc_id: W4.T26.ab-framework
owner: HoData
status: draft
last_reviewed: 2026-05-13
audience: [internal]
language: en
ar_companion: none
related: [W4.T23.slo-framework, W4.T24.model-cost-governance, W4.T12.event-taxonomy, W4.T13.executive-kpi-spec]
kpi: { metric: experiments_with_pre_registered_hypothesis_pct, target: 100, window: continuous }
rice: { reach: 0, impact: 2, confidence: 0.8, effort: 4pw, score: engineering }
---

# A/B Experimentation Framework

## 1. Purpose

Establish the minimum bar for running an experiment that influences a product, growth, pricing, or model-routing decision at Dealix. The bar is deliberately conservative: pre-registered hypothesis, computed sample size, guardrail metrics, and explicit stopping rules. Goal: zero experiments shipped on noise; zero customer harm from guardrail breaches.

## 2. Scope

Applies to any change that:

- Splits traffic between two or more variants (product, copy, model, pricing, dispatch policy).
- Affects a metric tracked in the executive KPI spec (W4.T13).
- Touches Revenue OS decisioning, policy thresholds, or model routing.

Out of scope: pure UI tweaks with no measurable behavior change (no exposure assignment needed), feature flags used purely for rollout (no analysis), and internal-tooling changes.

## 3. Hypothesis Template

Every experiment registers a hypothesis in `experiments/registry.yaml` **before** exposure starts. Template:

```yaml
id: EXP-2026-Q2-014
title: Sonnet vs. Haiku for signal normalization in KSA banking vertical
owner: HoData
hypothesis: |
  If we route KSA banking signals through Sonnet 4.7 instead of Haiku 4.5,
  then signal-normalization accuracy will increase by ≥ 2 percentage points
  with no more than +20% cost per signal.
exposure_unit: tenant_id          # never lead_id for high-stakes changes
allocation: { control: 0.5, variant: 0.5 }
primary_metric: signal_normalization_accuracy_pct
mde: 0.02                          # 2 percentage points absolute
alpha: 0.05
power: 0.80
expected_sample_per_arm: 8400      # computed below
guardrails:
  - llm_cost_per_signal_sar   {direction: not_worse_than, threshold: +20%}
  - p95_normalization_latency_ms {direction: not_worse_than, threshold: +30 ms}
  - data_quality_pass_rate_pct {direction: not_worse_than, threshold: -0.5pp}
stop_rules:
  - guardrail_breach: stop_immediately
  - sample_reached_and_inconclusive: extend_once_max
  - sample_reached_and_significant: stop_and_ship
duration_max_days: 21
start_at: 2026-05-15
end_at_max: 2026-06-05
```

The registry is human-reviewed before activation. PR review required: HoData + product owner of the affected surface.

## 4. Minimum Detectable Effect (MDE)

Choose MDE by **business significance**, not by what is statistically reachable in the available time.

Rule of thumb at Dealix:

- A metric is "moved" if the change in absolute terms would change a roadmap decision.
- For revenue metrics, MDE is typically 5–10% relative.
- For correctness/quality metrics, MDE is typically 1–3 percentage points absolute.
- For latency, MDE is typically 10–25% relative on p95.

If the team cannot articulate why the MDE threshold matters to a real decision, the experiment is rejected at hypothesis review.

## 5. Sample Size Calculation

For continuous metrics (latency, cost) — two-sample t-test:

```
n_per_arm = ( (Z_{1-α/2} + Z_{1-β})^2 * (σ_c^2 + σ_v^2) ) / (Δ^2)
```

For binary metrics (conversion, pass-rate) — proportion test:

```
n_per_arm = ( (Z_{1-α/2} + Z_{1-β})^2 * (p_c(1-p_c) + p_v(1-p_v)) ) / (Δ^2)
```

Defaults: α = 0.05 (two-sided), power = 0.80. We do **not** use one-sided tests. Variance estimates come from the prior 28 days of production data.

If `n_per_arm × 2 / weekly_traffic > 4 weeks`, the experiment is rejected — re-scope MDE or unit of analysis. Endless experiments lose institutional patience and risk guardrail decay.

## 6. Exposure Assignment

- **Unit**: prefer `tenant_id` for any change that crosses workflow boundaries; use `lead_id` only when the change is fully encapsulated within a single workflow and there is no leakage risk.
- **Assignment function**: deterministic hash `hash(experiment_id || unit_id) % 1000`.
- **Stickiness**: a unit is assigned once per experiment and stays in the assigned arm for the duration.
- **No cross-contamination**: a tenant in experiment X cannot be auto-enrolled in experiment Y on the same surface. The exposure service maintains a per-surface mutex.
- **Sovereign opt-out**: Sovereign tenants are excluded from experiments by default; opt-in is contractual and noted in the tenant config.
- **Service surface**: assignments are served by an `ExposureService` that records every exposure decision as an event (`experiment_exposure_assigned`) per the event taxonomy.

## 7. Primary Metric Registration

Every experiment names exactly one **primary metric**. Primary metrics must:

- Be pre-registered in `analytics/metric_catalog.yaml` (link below).
- Have a stable definition that has not changed in the prior 28 days.
- Be reported in the executive KPI spec or be one level down from it.

Secondary metrics may be added but are not used for the decision. Surprises in secondary metrics motivate follow-up experiments, not ship/no-ship calls.

## 8. Guardrails

Every experiment declares ≥ 2 guardrails. Standard guardrails (always considered):

- Availability: tenant 5xx error rate `not_worse_than` baseline + 0.1pp.
- Latency p95: `not_worse_than` baseline + 25%.
- LLM cost per workflow: `not_worse_than` baseline + 20%.
- Data quality pass rate: `not_worse_than` baseline − 0.5pp.
- Tenant churn signals (logout rate, support tickets per tenant): `not_worse_than` baseline + 15%.

Guardrails are monitored daily during the experiment. A guardrail breach at p < 0.05 for 24+ hours triggers immediate variant rollback.

## 9. Stopping Rules

| Condition | Action |
|---|---|
| Guardrail breach (significant for 24 h) | Stop, roll back to control, post-mortem. |
| Primary metric reaches significance early **and** sample ≥ 80% of planned | Stop and ship variant. |
| Primary metric reaches significance early **and** sample < 80% | Continue to full sample to avoid winner's curse. |
| Sample reached, primary metric inconclusive | Extend once (up to 50% additional sample) OR conclude no effect. Default: conclude no effect. |
| Duration max reached | Conclude. No further extensions. |

Sequential testing (peeking with adjustments) is allowed only with always-valid inference methods. Naive p-value peeking is forbidden.

## 10. Analysis and Reporting

- Analysis notebook template in `experiments/templates/analysis.ipynb`.
- Mandatory contents:
  - Pre-registered hypothesis and metric.
  - Per-arm sample size, exposure-unit count.
  - Primary metric point estimate + 95% CI.
  - Guardrail status for each guardrail.
  - SRM (sample ratio mismatch) check; experiment is void if SRM χ² p < 0.001.
  - Variance-reduction technique used (e.g. CUPED) and uplift.
  - Conclusion: ship / no-ship / extend.
- Report is reviewed in the weekly experiment review meeting; ship decisions require HoData + surface owner sign-off.

## 11. Rollout Policy

If "ship":

- Begin gradual rollout: 1% → 10% → 50% → 100% over 7 days, monitoring the same guardrails.
- Any guardrail breach during rollout pauses the next step and triggers re-evaluation.
- Once at 100%, the variant becomes the default; control code path remains for 30 days as rollback safety net.
- Update the metric catalog and any affected docs (model routing, policy, copy library).

If "no-ship":

- Variant is removed; assignments cleared.
- Result is logged in the experiment registry with conclusion + commentary.

## 12. Anti-Patterns (Forbidden)

- HARKing (Hypothesizing After Results are Known) — choosing a primary metric post-hoc.
- Stopping on a single peek without sequential-test adjustments.
- Running concurrent experiments on the same surface without mutex.
- Using `lead_id` as exposure unit for a tenant-wide change (causes leakage and inflates power illusively).
- Reporting only winning secondary metrics.

Any of these voids the experiment.

## 13. References

- Event taxonomy: `docs/analytics/event_taxonomy.md` — `experiment_*` events.
- Executive KPI spec: `docs/analytics/executive_kpi_spec.md`.
- Model cost governance: `docs/finops/model_cost_governance.md`.
- SLO framework: `docs/sre/slo_framework.md` — guardrail baselines.
- Code: `auto_client_acquisition/revenue_os/enrichment_waterfall.py` (most-experimented surface), `dealix/trust/policy.py` (policy threshold experiments).
- External: Kohavi, Tang, Xu — Trustworthy Online Controlled Experiments.
