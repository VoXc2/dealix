# Workflow Runtime Design

> Every Dealix workflow — manual today, automated tomorrow — has the same
> 8-step contract. Designing the workflow before building it forces
> clarity on inputs, outputs, governance, and human-in-the-loop points.

## The 8-step workflow contract

| # | Step | Question it answers |
|---|------|---------------------|
| 1 | Trigger | What starts this workflow? |
| 2 | Input | What data / files are required at start? |
| 3 | AI step | What does AI produce? (schema-bound) |
| 4 | Governance check | Which Runtime Governance checks apply? |
| 5 | Human review | Who reviews / approves before next step? |
| 6 | Output | What is delivered to whom? |
| 7 | Proof event | What evidence is logged to the event store / Proof Ledger? |
| 8 | Next action | What happens after this workflow completes? |

## Example workflow: Lead Scoring (Lead Intelligence Sprint)

```
1. Trigger        — customer uploads lead CSV
2. Input          — CSV + ICP definition + offer description
3. AI step        — RevenueAgent scores accounts; schema = LeadScore
4. Governance     — Data Source check + PII check + Forbidden-Claim check
5. Human review   — Delivery Owner reviews top-50 + top-10 actions
6. Output         — ranked Mini-CRM board delivered to customer
7. Proof event    — `delivery.proof_pack_created` written; rows scored = N
8. Next action    — outreach draft workflow OR pilot conversion conversation
```

## Example workflow: Knowledge Answer (Company Brain Sprint)

```
1. Trigger        — customer team-member asks a question
2. Input          — natural-language question + corpus access scope
3. AI step        — KnowledgeAgent retrieves; schema = Answer with citation
4. Governance     — Permission Mirroring + no-source-no-answer + PII check
5. Human review   — first 30 days: source check on each new doc cited
6. Output         — cited answer to the asker (or "insufficient evidence")
7. Proof event    — query, source IDs, confidence logged
8. Next action    — freshness check if doc cited is > 90 days old
```

## Example workflow: Outreach Draft (Lead Intelligence Sprint)

```
1. Trigger        — Delivery Owner approves top-10 actions
2. Input          — top-10 account context + ICP + sector playbook
3. AI step        — OutreachAgent drafts AR + EN messages; schema = Draft
4. Governance     — Forbidden-claim filter + PDPL Art. 13 footer + tone check
5. Human review   — AE reviews every draft; approves/rejects per draft
6. Output         — approved drafts handed to customer's CRM
7. Proof event    — drafts approved count + drafts rejected count logged
8. Next action    — customer sends through their own approved channels
```

## Workflow Registry

Tracked in `docs/product/WORKFLOW_REGISTRY.md`:

| Workflow | Capability | Service | Risk | Human review | Status |
|----------|-----------|---------|------|:------------:|--------|
| Lead Import Preview | Data / Revenue | Lead Intel | Medium | Yes | MVP |
| Account Scoring | Revenue | Lead Intel | Medium | Yes | MVP |
| Outreach Drafting | Revenue | Lead Intel | High | Yes (per draft) | MVP |
| Knowledge Answering | Knowledge | Company Brain | High | Yes (sources) | Beta |
| Report Generation | Reporting | All | Medium | Yes | MVP |
| Governance Check | Governance | All | Required | n/a (auto) | MVP |

Status ∈ {Designed / Manual / MVP / Production / Deprecated / Blocked}.

## Workflow SLA (per `docs/delivery/WORKFLOW_SLA.md` — to be added)

| Workflow | Expected time | Quality gate | Owner |
|----------|--------------:|--------------|-------|
| Import Preview | 24h | Data QA | Delivery |
| Lead Scoring | 48h | Revenue QA | Delivery |
| Outreach Drafts | 48h | Claims QA | Delivery |
| Executive Report | 72h | Full 5-gate QA | Reporting |
| Proof Pack | 24h | Proof QA | Delivery |

## Hard rules

- No workflow ships without all 8 steps documented.
- No workflow promotes to MVP status without a passing eval test (per `EVALUATION_REGISTRY.md`).
- Step 5 (Human review) is NEVER "n/a" for any side-effect action; only read-only / classify workflows may skip it.
- Step 7 (Proof event) is NEVER skipped — if there's nothing to log, the workflow shouldn't exist.

## Cross-links
- `docs/governance/RUNTIME_GOVERNANCE.md` — the 8 runtime checks
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/product/AI_AGENT_INVENTORY.md`
- `docs/product/AI_WORKFORCE_OPERATING_MODEL.md`
- `auto_client_acquisition/orchestrator/runtime.py` — Operations OS runtime
- `auto_client_acquisition/delivery_factory/stage_machine.py` — Delivery OS state machine
