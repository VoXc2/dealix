# Evaluation harness (Dealix)

Two layers: **automated probes** that gate CI, and **YAML checklists** for
human review of LLM-generated output.

## 1. Automated probe harness — `runner.py`

`evals/runner.py` runs deterministic, offline probes (no LLM keys, no
network) against the real engines and produces a scored report.

```bash
python evals/runner.py            # markdown report; exit 1 on failure
python evals/runner.py --json     # machine-readable report
```

Probe packs (`evals/probes/*.jsonl`):

| Pack | Category | What it proves |
|------|----------|----------------|
| `governance_probes.jsonl` | governance | scraping / cold-WhatsApp / guaranteed-sales / unsafe-method requests are **rejected**; Source-Passport gate decisions are correct |
| `value_discipline_probes.jsonl` | value_discipline | estimated value is never auto-promoted; verified/client_confirmed tiers require evidence refs |
| `arabic_quality_probes.jsonl` | arabic_quality | bilingual output renders without mojibake |

**CI gate:** `tests/test_evals.py` runs the harness. Any governance-probe
failure fails the build; overall pass rate must stay ≥ 0.90.

## 2. YAML review checklists

YAML packs describe **what "good" means** per LLM workflow — used by a human
reviewer until an automated rubric is calibrated.

| Eval | File |
|------|------|
| Lead Intelligence | [`lead_intelligence_eval.yaml`](lead_intelligence_eval.yaml) |
| Company Brain | [`company_brain_eval.yaml`](company_brain_eval.yaml) |
| Outreach drafts | [`outreach_quality_eval.yaml`](outreach_quality_eval.yaml) |
| Governance | [`governance_eval.yaml`](governance_eval.yaml) |
| Arabic output | [`arabic_quality_eval.yaml`](arabic_quality_eval.yaml) |

## LLM wiring (honest status)

Live LLM calls go through `core/llm/router.py` (`get_router()` / `ModelRouter`
— provider fallback + Anthropic prompt caching). Real callsites today are the
agents under `auto_client_acquisition/agents/` (outreach, proposal,
qualification, follow-up, pain extraction, prospecting). Most OS modules are
deterministic by design — the probe harness above gates that deterministic
core. RAG (`core/memory/embedding_service.py`) uses OpenAI embeddings with
pure-Python cosine similarity; on API failure it logs a warning and returns a
zero-vector so callers never crash (degraded, not silent-broken).

**Why automated evals matter:** scaling AI requires evaluation and workflow
integration, not one-off demos — see
[McKinsey — The state of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/).

Simulations: [`../simulations/README.md`](../simulations/README.md)
