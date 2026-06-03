# Board Decision Loop

## النموذج

```text
Collect signals
→ Score signals
→ Generate decision options
→ Choose action
→ Assign owner
→ Execute
→ Measure proof
→ Update system
```

## إشارات داخلة (taxonomy في الكود)

`BOARD_DECISION_INPUT_SIGNALS` في `board_decision_os/board_signal_inputs.py`:

```text
sales_signals
client_adoption_signals
proof_signals
governance_events
data_patterns
workflow_friction
productization_candidates
partner_signals
market_trends
financial_metrics
```

## قرارات خارجة

Scale، Build، Pilot، Hold، Kill، Raise Price، Offer Retainer، Create Playbook، Create Benchmark، Create Business Unit، Create Venture Candidate — راجع [`DECISION_TYPES.md`](DECISION_TYPES.md) و`intelligence_compounding_os` / `board_decision_os`.

**صعود:** [`STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md`](STRATEGIC_INTELLIGENCE_BOARD_SYSTEM.md)
