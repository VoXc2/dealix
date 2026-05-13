# Dealix Operating Kernel

> **Constitution**: Dealix is operated through gates, not assumptions. No
> service can be sold, delivered, or scaled unless it passes the required
> readiness gates with documented evidence.

## The 8 operating components

1. **Readiness Registry** — `DEALIX_READINESS.md` + `scripts/verify_dealix_ready.py`. Tracks which services are Sellable / Beta / Not Ready / Enterprise-only.
2. **Service Registry** — `docs/company/SERVICE_REGISTRY.md`. Single canonical entry per service: promise, price, duration, deliverables, exclusions, KPI, upsell.
3. **Delivery Engine** — `auto_client_acquisition/delivery_factory/` + `docs/delivery/*` + `docs/services/<offer>/delivery_checklist.md`. Turns scope into a 8-stage state machine with QA gates.
4. **Quality Engine** — `auto_client_acquisition/delivery_factory/qa_review.py` + `docs/quality/*`. Scores every output against 5 QA gates + 100-point rubric (floor 80, target 85).
5. **Governance Engine** — `dealix/trust/` + `docs/governance/*`. Blocks forbidden actions, enforces PDPL, redacts PII, requires approvals.
6. **Proof Engine** — `dealix/reporting/proof_pack.py` + `docs/services/<offer>/proof_pack_template.md`. Generates Stage-7 evidence per project; entries become Proof Ledger.
7. **Sales Engine** — `docs/sales/*` + `templates/sow/*` + `templates/outbound_messages.md`. Closes deals by linking each service to script + objection bank + SOW.
8. **Learning Engine** — Feature Candidate Log + monthly retro. Turns repeated manual steps into product features once they (a) recur ≥ 3 times, (b) a customer has paid for them.

## Hard rules (binding; violation blocks shipping)

- No data without source.
- No AI output without QA review.
- No external action without approval (per `dealix/trust/approval_matrix.py`).
- No source → no answer (Knowledge OS).
- No project closes without a Proof Pack.
- No feature ships before it repeated 3× in real delivery.

## How the kernel decides

```
new request
  → classify (against Service Registry)
  → check readiness (against Readiness Registry)
  → if Sellable → Service Pack
  → if Beta → Pilot only (labeled)
  → if Designed → discovery-paid only
  → if Idea → polite no
```

## Cross-links

- `DEALIX_READINESS.md` — 11-Gate scorecard
- `docs/company/EVIDENCE_SYSTEM.md` — what counts as "evidence"
- `docs/company/SERVICE_READINESS_MATRIX.md` — per-service status table
- `docs/company/DECISION_RULES.md` — binding CEO rules
- `docs/company/SELLABILITY_POLICY.md` — what we are allowed to sell
- `docs/strategy/dealix_delivery_standard_and_quality_system.md` — 8-stage + 5-gate canonical

## Owner & cadence

- **Owner**: CEO.
- **Constitution review**: quarterly.
- **Amendment**: requires CTO + HoLegal sign-off.
