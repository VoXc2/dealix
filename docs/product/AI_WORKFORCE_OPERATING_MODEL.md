# AI Workforce Operating Model

> AI agents in Dealix are **not autonomous employees**. They are governed
> workers inside controlled workflows. Every agent has a named role, a
> bounded scope, schema-validated I/O, and a ComplianceGuard pass-through.

## The 6 agent types

| Type | Role | Examples |
|------|------|----------|
| Analyst Agents | Classify, summarize, score | DataQualityAgent, RevenueAgent |
| Drafting Agents | Create drafts, reports, scripts | OutreachAgent, ReportingAgent |
| Retrieval Agents | Search knowledge with citations | KnowledgeAgent |
| Workflow Agents | Move tasks through defined workflows | WorkflowAgent, DeliveryManagerAgent |
| Guardrail Agents | Check safety, claims, PII, policy | ComplianceGuardAgent |
| Reporting Agents | Generate reports + Proof Packs | ReportingAgent |

## Agent Card standard

Every agent has an Agent Card in `docs/product/agent_cards/<name>.md`. Required fields:

- **Role** — one-sentence purpose.
- **Allowed inputs** — which datasets / fields the agent may read.
- **Allowed outputs** — what the agent may produce (schema-bound).
- **Forbidden actions** — what the agent must never do.
- **Required runtime checks** — which of the 8 Runtime Governance checks must pass before output is accepted.
- **Output schema** — Pydantic model name.
- **Approval requirement** — human approval before customer-facing use? yes/no.
- **Eval test** — which entry in `docs/product/EVALUATION_REGISTRY.md` covers it.

### Example: RevenueAgent

```markdown
# Agent Card: RevenueAgent
## Role
Score accounts and recommend revenue actions.

## Allowed inputs
- Customer-approved datasets only.
- ICP definition.
- Service offer description.
- Sector playbook.

## Allowed outputs
- Account score + reasons.
- Segment recommendation.
- Recommended next action (NOT autonomous send).

## Forbidden
- Sending any message externally.
- Scraping.
- Creating guaranteed-outcome language.
- Using unsourced personal data.

## Required runtime checks
- Data source check.
- PII check.
- Forbidden-claim check on any text output.

## Output schema
LeadScore (from auto_client_acquisition/revenue_os/lead_scoring.py).

## Approval
Human review required before delivery to customer.

## Eval test
lead_scoring_eval (per EVALUATION_REGISTRY).
```

## Hard rules (enforced at runtime)

- **AI proposes, human approves** for any side-effect.
- **Output is always schema-validated** (Pydantic). Unstructured text is wrapped in a typed model before downstream use.
- **Every agent action passes through ComplianceGuardAgent** before completing.
- **No agent calls a model directly** — every model call goes through the LLM Gateway (Phase 2) which enforces PII redaction, cost guard, prompt versioning, and run logging.
- **No web scraping. No cold WhatsApp. No LinkedIn automation. No fake proof. No guaranteed claims. No PII in logs.**

## The 10 named agents (Phase-1 catalog)

| Agent | Module(s) it serves |
|-------|---------------------|
| StrategyAgent | Strategy OS (Phase 3) |
| DataQualityAgent | Data OS |
| RevenueAgent | Revenue OS |
| OutreachAgent | Revenue OS, Marketing OS |
| SupportAgent | Customer OS (Phase 2) |
| KnowledgeAgent | Knowledge OS |
| WorkflowAgent | Operations OS |
| ReportingAgent | Reporting OS |
| ComplianceGuardAgent | Governance OS (mandatory gate) |
| DeliveryManagerAgent | Delivery OS |

## Cross-links
- `docs/governance/RUNTIME_GOVERNANCE.md` — the 8 runtime checks
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md` *(below)*
- `docs/product/EVALUATION_REGISTRY.md` *(to be added in eval framework expansion)*
- `docs/product/internal_os_modules.md` — module ↔ agent mapping
- `docs/product/CAPABILITY_MATRIX.md`
