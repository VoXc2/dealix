# Core OS — Global Edition

The same Core OS map that grounds the endgame doctrine, restated here with **enterprise scope** notes and the constitutional technical rules.

## 1. Layout

```
auto_client_acquisition/
  core_os/
    ids.py
    events.py
    schemas.py
    audit.py
    registry.py
  data_os/
    source_passport.py
    import_preview.py
    data_quality_score.py
    pii_detection.py
  governance_os/
    policy_check.py
    runtime_guardrails.py
    approval_matrix.py
    audit_log.py
    rules/
  llm_gateway/
    model_router.py
    prompt_registry.py
    run_log.py
    cost_guard.py
    eval_hook.py
  revenue_os/
    account_scoring.py
    outreach_drafts.py
    pipeline.py
  brain_os/
    source_registry.py
    retrieval.py
    answer_with_citations.py
    knowledge_eval.py
  operations_os/
    workflow_builder.py
    sop_generator.py
    approval_flow.py
  reporting_os/
    proof_pack.py
    value_metrics.py
    executive_report.py
  capital_os/
    capital_ledger.py
    productization_ledger.py
    playbook_updates.py
  intelligence_os/
    metrics_engine.py
    decision_engine.py
    capital_allocator.py
    venture_signal.py
  command_os/
    group_scorecard.py
    client_scorecard.py
    red_team.py
    kill_criteria.py
```

## 2. Constitutional technical rules

- **No AI call outside `llm_gateway`.**
- **No client-facing output outside `governance_os`.**
- **No project close outside `reporting_os.proof_pack`.**
- **No repeated work outside `capital_os.productization_ledger`.**
- **No strategic decision outside `intelligence_os`.**

These rules are enforced by code review, runtime checks, and engineering on-call.

## 3. Enterprise scope notes

| Module | Enterprise expectation |
| --- | --- |
| `core_os` | Append-only audit; signed events; ID schemes that survive multi-tenant sharding |
| `data_os` | Source Passport mandatory; PII detection with metrics; quality scoring per source |
| `governance_os` | Decision vocabulary, runtime guardrails, immutable audit, exportable artifacts |
| `llm_gateway` | Model routing with policy, cost guard, eval hook, full run log |
| `revenue_os` | Draft-only outputs by default; no auto-send without approval |
| `brain_os` | Citation coverage tracked; insufficient-evidence rate tracked |
| `operations_os` | Approvals first-class; SOP versioning |
| `reporting_os` | Proof Pack format frozen; deltas computed against baselines |
| `capital_os` | Capital Ledger as the single source of truth for reusable assets |
| `intelligence_os` | Decisions logged immutably with their inputs |
| `command_os` | Scorecards drive operator and BU performance |

## 4. Cross-cutting concerns

- **Identity** — agents and users have stable IDs; all events carry both.
- **Tenancy** — never share state across tenants.
- **Residency** — modules respect per-tenant region pins.
- **Observability** — every module emits structured events to `core_os.audit`.
- **Reliability** — circuit breakers around external models and partner APIs.

## 5. Anti-fork rule

Business Units and Ventures **inherit** the Core OS. Forking the runtime is forbidden. Rule packs and templates are the legitimate way to specialize behavior.

## 6. Migration discipline

- New modules are introduced via the productization ledger after repeated demand.
- Module deprecation requires a sunset plan and a Capital Sweep.
- API breakages require a migration note in `CHANGELOG.md`.
