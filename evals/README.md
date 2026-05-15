# Evaluation harness (Dealix)

YAML packs describe **what “good” means** per workflow. They complement pytest and `scripts/verify_*.py`.

| Eval | File |
|------|------|
| Lead Intelligence | [`lead_intelligence_eval.yaml`](lead_intelligence_eval.yaml) |
| Company Brain | [`company_brain_eval.yaml`](company_brain_eval.yaml) |
| Outreach drafts | [`outreach_quality_eval.yaml`](outreach_quality_eval.yaml) |
| Governance | [`governance_eval.yaml`](governance_eval.yaml) |
| Arabic output | [`arabic_quality_eval.yaml`](arabic_quality_eval.yaml) |

**Why:** Scaling AI requires evaluation and workflow integration, not one-off demos — see [McKinsey — The state of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/).

Simulations: [`../simulations/README.md`](../simulations/README.md)
