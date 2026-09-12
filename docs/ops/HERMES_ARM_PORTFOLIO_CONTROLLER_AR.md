# Hermes Arm Portfolio Controller (مراقب محفظة الأذرع)

One deterministic planning pass over the canonical Dealix 44-arm registry. It
ranks arms, selects the deep wedges, and hands executable work to the existing
Hermes session factory. It is **not** a scheduler and never performs an external
effect.

## Canonical sources (no parallel taxonomy)

| Source | Path |
|---|---|
| Arm registry (44 arms, 5 agents, `deep_wip_max=3`) | `config/company/dealix_arm_registry.json` |
| Execution playbooks (one per arm) | `config/company/dealix_arm_execution_playbooks.json` |
| Evidence ledger (optional) | `data/ops/arm_portfolio_evidence_v1.json` |
| Controller | `scripts/ops/hermes_arm_portfolio_controller.py` |
| One-shot runner | `scripts/ops/run_hermes_arm_portfolio_once.py` |
| Canonical scheduler (unchanged) | `scripts/ops/session_factory.py` (+ watchdog) |

## Hard invariants (fail closed)

- Exactly the five permanent agents; the controller refuses non-permanent owners.
- `ACTIVE_DEEP = ARM-001/ARM-002/ARM-003` and `DEEP_WIP_MAX = 3` are preserved.
- The deep set only changes on **real customer/economic evidence**: a stop-loss
  demotes (recommendation only), and a freed slot may be filled only by an arm
  with `CUSTOMER` or `ECONOMIC` evidence.
- Research alone can only rank `LIGHT` or `HOLD` — it never promotes to `DEEP`.
- No ROI, pipeline, revenue, or amount is invented; scores are a
  `PRIORITIZATION_HEURISTIC_NOT_FORECAST`.
- L5 material effects (send / publish / pay / deploy / DNS / DB / secret) are
  never executed. They are emitted as `authority_level=L5` and parked by the
  factory at `WAITING_L5`.
- If any external-effect env switch is enabled, the plan is `BLOCKED` and the
  runner refuses to enqueue.

## Classification law

| Class | Rule |
|---|---|
| `DEEP` | Preserved deep arm, or an evidence-backed promotion filling a free deep slot (≤ 3 total). |
| `LIGHT` | Near-term arm with real (research or better) evidence, or a registry `ACTIVE_LIGHT`/`VALIDATE` arm. |
| `HOLD` | `BLOCKED`, `HOLD` horizon, stop-loss evidence, `WATCH` with no evidence, or no justifiable evidence. |

## Transparent output per arm

Every record emits: `score` (total + weighted positive factors + penalties with
basis), `classification`, `next_safe_action`, `evidence_refs`, `evidence.tier`,
`model_job_class` (job class / model class / execution mode / authority level /
`auto_executable`), `cost` (`compute_class`, `cash_class=NONE`), `risk`
(`LOW|MEDIUM|HIGH` + basis), `founder_minutes` (`reported|None`, band, basis),
and `proof_gap` (required gate, available tier, missing evidence). The plan also
emits `top3`, `deep_wedge_ids`, counts, and truth flags (`counts_as_revenue=false`,
`counts_as_pipeline=false`).

Score = `sum(factor.value × weight) − sum(penalty_score × weight)`, clamped to
`[0,100]`. Weights: evidence 0.32, priority 0.20, horizon 0.18, state 0.18,
gate 0.12; penalties: risk 0.15, founder-minutes 0.10, proof-gap 0.10.

## Evidence ledger (optional, never fabricated)

```json
{
  "schema": "dealix.arm_portfolio_evidence.v1",
  "arms": {
    "ARM-004": {
      "research_evidence_refs": ["evidence://..."],
      "customer_evidence_refs": ["evidence://..."],
      "economic_evidence_refs": ["evidence://..."],
      "stop_loss_evidence_refs": [],
      "founder_minutes": 120,
      "requires_external_send": false,
      "proof_gap_notes": ""
    }
  }
}
```

Absent ledger or absent arm entry = no evidence = `LIGHT`/`HOLD` only. Reference
IDs point at real artifacts; the controller never generates them.

## One-shot usage

```bash
# Plan only (default; safe)
python3 scripts/ops/run_hermes_arm_portfolio_once.py --summary

# Plan + enqueue safe (non-L5) work into the canonical session factory queue
python3 scripts/ops/run_hermes_arm_portfolio_once.py --enqueue --max-jobs 5
```

The runner performs one pass and exits; it never loops or installs a
cron/systemd unit. Enqueue is idempotent per arm via the
`arm_portfolio:<ARM-ID>` marker. The plan is written to the factory state dir by
default (`HERMES_ARM_PORTFOLIO_PLAN.json`), outside the git checkout.

## Job receipt acceptance (fail-closed)

Every enqueued arm job is non-modifying and carries a prompt with the arm's
evidence/context refs, the truth laws (`research != relationship`, `invoice !=
payment`, no invented ROI/pipeline/revenue), and hard constraints (no external
effect, no repository modification). Acceptance requires **both**:

- `exit_zero`, and
- `stdout_contains` the exact marker `ARM_PORTFOLIO_RECEIPT:<ARM-ID>`.

The receipt must also report `FINDINGS`, `EVIDENCE_REFS_USED`,
`RELATIONSHIP_TRUTH`, `PIPELINE_TRUTH`, `REVENUE_TRUTH`, `NEXT_SAFE_ACTION` and
`L5_REQUIRED`. A run that exits zero but omits the marker fails closed. L5 jobs
still park at `WAITING_L5`.

## Verify

```bash
pytest tests/test_hermes_arm_portfolio_controller.py tests/test_hermes_arm_portfolio_runner.py \
       tests/test_session_factory.py tests/test_session_factory_watchdog.py -q
ruff check scripts/ops/hermes_arm_portfolio_controller.py scripts/ops/run_hermes_arm_portfolio_once.py
```
