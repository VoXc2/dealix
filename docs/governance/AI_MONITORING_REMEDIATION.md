# AI Monitoring & Remediation

> Monitoring catches failure, remediation contains it. This document is the
> contract between the AI Control Tower (`AI_CONTROL_TOWER.md`) and the
> on-call operator. Aligned with Gartner's guidance on managing agent
> sprawl: detect early, contain fast, learn always.

## What we monitor

| Signal | Source | Detection cadence |
|--------|--------|-------------------|
| AI run failures | LLM gateway + `auto_client_acquisition/agent_observability/` | Real-time |
| Low QA scores | `EVALUATION_REGISTRY.md` runners + per-delivery rubric | Nightly + per-delivery |
| Governance blocks | `dealix/trust/policy.py` decisions | Real-time |
| PII flags | `dealix/trust/pii_detector.py` | Real-time |
| Source missing | Runtime governance check #1 | Real-time |
| Cost overrun | LLM gateway vs. `MODEL_PORTFOLIO.md` budgets | Hourly |
| Hallucination risk | Ragas faithfulness (Company Brain) | Per-run |
| Approval delays | `dealix/trust/approval.py` queue age | Hourly |

## Remediation actions (the operator's toolkit)

| Action | When to use | Reversible? | Logged where |
|--------|-------------|:-----------:|--------------|
| Pause agent | Eval fail / repeated blocks / cost runaway | Yes | Decision Ledger + `AI_AGENT_INVENTORY.md` status |
| Request source | Source-missing on a Brain answer | Yes | `SOURCE_REGISTRY.md` proposal queue |
| Redact + retry | PII leaked into output | Yes | `AI_RUN_LEDGER.md` (redaction note) |
| Rerun with stronger model | Quality dip on a high-stakes output | Yes | Run logged with model class delta |
| Escalate to HoLegal | Governance block / unsupported claim / PII exposure | Yes | `INCIDENT_RESPONSE.md` ticket |
| Update prompt | Pattern of failures across runs | Yes (version bump) | `PROMPT_REGISTRY.md` MINOR/MAJOR bump |
| Update rule | New forbidden claim / new PII pattern | Yes | `dealix/trust/forbidden_claims.py` PR |
| Log incident | Anything customer-impacting | n/a | `INCIDENT_RESPONSE.md` |

## Detection → Remediation playbook

```
1. Detect (Control Tower alert)
2. Triage (operator confirms signal is real, not noise)
3. Contain (pause / redact / escalate as appropriate)
4. Repair (rerun / update prompt / update rule)
5. Verify (eval re-pass + spot-check)
6. Learn (RCA in Decision Ledger; rule or test added)
```

Steps 1–3 happen in minutes. Steps 4–6 happen within the workday.

## Severity matrix

| Severity | Examples | Containment SLA | Escalation |
|---------:|----------|----------------:|-----------|
| Critical | PII exposure, unsupported claim reached customer | 1 hour | HoLegal + CTO + founder |
| High | Eval below threshold, customer-facing block, hallucination risk on Brain | 4 hours | Agent owner + HoP |
| Medium | Cost overrun, approval overdue, source missing | 1 working day | Agent owner |
| Low | Latency spike, single failed run | 3 working days | Agent owner |

## Pause-agent rule (the safest default)

When in doubt, pause the agent. A paused agent:

- Stops accepting new workflow steps (returns `paused` from runtime).
- Existing in-flight runs complete and are reviewed by the owner.
- The pause is announced on the Control Tower with reason + ETA.
- Resume requires owner sign-off and (if eval-driven) a re-pass.

## Sprawl controls (Gartner alignment)

Inventory in `AI_AGENT_INVENTORY.md`. Lifecycle in
`AGENT_LIFECYCLE_MANAGEMENT.md`. Promotion gate requires eval +
governance pass. Quarterly retirement review. Permission Mirroring
prevents shadow agents from over-reading.

## Phase 2 wiring

Alerts route to Slack + on-call rotation. Pause/resume becomes a one-click
action in the Control Tower. Remediation actions write structured events
into the event store so RCAs are reproducible.

## Cross-links

- `/home/user/dealix/docs/product/AI_CONTROL_TOWER.md`
- `/home/user/dealix/docs/product/AGENT_LIFECYCLE_MANAGEMENT.md`
- `/home/user/dealix/docs/product/AI_AGENT_INVENTORY.md`
- `/home/user/dealix/docs/product/EVALUATION_REGISTRY.md`
- `/home/user/dealix/docs/governance/RUNTIME_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/AI_INFORMATION_GOVERNANCE.md`
- `/home/user/dealix/docs/governance/INCIDENT_RESPONSE.md`
- `/home/user/dealix/docs/ledgers/AI_RUN_LEDGER.md`
- `/home/user/dealix/dealix/trust/policy.py`
- `/home/user/dealix/dealix/trust/approval.py`
- `/home/user/dealix/auto_client_acquisition/agent_observability/`
