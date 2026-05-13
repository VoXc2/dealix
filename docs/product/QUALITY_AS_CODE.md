# Quality as Code

> Quality at Dealix is not an aspiration in a sales deck. Every quality
> rule is an executable check that runs against AI outputs before they
> reach a customer. Phase-1 ships rules in code (`dealix/trust/*`,
> `dealix/reporting/*`); Phase-2 promotes them into a `quality_os/` module
> with rules, evaluators, and rubrics as first-class artefacts.

## The five customer-grade rules

Each rule below is *executable* — a function returns Pass / Fail / Warn,
and Fail blocks the output from shipping.

### 1. Every report must include exec summary + next action

- **Where**: `dealix/reporting/executive_report.py` validator + eval
  `EVL-REP-002` in `EVALUATION_REGISTRY.md`.
- **Check**: structural Pydantic round-trip on `ExecutiveReport` requires
  `exec_summary` (≥1, ≤5 bullets) and `next_action` (≥1 ordered action).
- **Failure**: rejected; ReportingAgent re-prompted; logged in
  `AI_RUN_LEDGER.md`.

### 2. Every proof pack must include inputs + outputs

- **Where**: `dealix/reporting/proof_pack.py` + eval `EVL-REP-001`.
- **Check**: `ProofPack` schema requires `inputs_redacted`,
  `outputs_summary`, `model_class`, `prompt_version`, `governance_decisions`.
  Missing field → blocked.
- **Failure**: pack not published; delivery owner notified; Control Tower
  alert (`AI_CONTROL_TOWER.md`).

### 3. Every Company Brain answer must include citation or "insufficient evidence"

- **Where**: KnowledgeAgent grounded-answer step + eval `EVL-BRN-001`
  (citation present = 100%).
- **Check**: Ragas faithfulness gate; if no source returned by retrieval,
  the agent must respond `"insufficient evidence — please add a source"`
  rather than free-generate. Hard rule in
  `auto_client_acquisition/company_brain/grounded_answer.py`.
- **Failure**: answer blocked; alert routed to KnowledgeAgent owner (HoP).

### 4. Every outreach draft must avoid guaranteed claims

- **Where**: `dealix/trust/forbidden_claims.py` runs on every draft;
  eval `EVL-LIS-002`.
- **Check**: zero matches against the forbidden pattern set (e.g.
  "نضمن", "guarantee", "100%", "best in", "risk-free"). One match → block.
- **Failure**: draft rejected; OutreachAgent re-prompted; the event is
  logged for the Friday review and customer-side approval workflow.

### 5. Every Arabic output must pass tone review

- **Where**: Arabic-tone rubric (1–5) in `EVALUATION_REGISTRY.md`
  (e.g. EVL-LIS-002, EVL-REP-002, EVL-SUP-001). Phase-1 uses a human
  panel; Phase-2 uses a DeepEval rubric grader with a human spot-check.
- **Check**: tone ≥ 4/5 for any external-facing Arabic output. Formal
  MSA; no machine-translated phrasing; sector-appropriate register.
- **Failure**: rejected for revision; localisation lead notified.

## Future location (Phase-2 layout)

```
quality_os/
├── rules/           # YAML / Python rules per the five rules above
├── evaluators/      # DeepEval / Ragas / promptfoo runners
├── rubrics/         # Arabic-tone / structural / safety rubrics
└── runners.py       # Per-output gate orchestrator
```

The PR that creates `quality_os/` is also the PR that migrates the
checks above out of `dealix/trust/*` and `dealix/reporting/*` into their
new home — without changing behaviour. Until then, those modules
*are* `quality_os`.

## Hard rules

- Quality rules ship with tests. A rule without a unit test does not
  enforce anything.
- A rule that throws (rather than returns Pass/Fail/Warn) is a bug —
  the workflow runtime treats throws as Fail and pages an operator.
- Customer-facing outputs that bypass the gates (e.g. emergency hot-fix)
  must be logged with a CTO sign-off in the Decision Ledger.

## Operating cadence

| Cadence | Action | Owner |
|---------|--------|-------|
| Per-PR | Quality rule regression suite | Agent owner |
| Daily | Failed-output review | HoP |
| Weekly | Rule false-positive trim | HoLegal + HoP |
| Quarterly | Rubric calibration with native Arabic reviewer | Localisation lead |

## Cross-links

- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/product/PROMPT_REGISTRY.md`
- `/home/user/dealix/docs/product/AI_CONTROL_TOWER.md`
- `/home/user/dealix/docs/product/AGENT_LIFECYCLE_MANAGEMENT.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/dealix/trust/forbidden_claims.py`
- `/home/user/dealix/dealix/trust/pii_detector.py`
- `/home/user/dealix/dealix/reporting/proof_pack.py`
- `/home/user/dealix/dealix/reporting/executive_report.py`
