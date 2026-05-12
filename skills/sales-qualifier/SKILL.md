# Sales Qualifier (BANT + PDPL)

Qualifies an inbound lead against BANT (Budget / Authority / Need /
Timeline) **and** the Saudi PDPL contactability gate. Output is a
typed Pydantic model the platform consumes verbatim.

## When to use

- Public form submission lands a new lead.
- Daily targeting picks a lead from the pool.
- A partner registers a deal via `/api/v1/partners/deals/register`.

## Inputs

| Variable | Source |
| --- | --- |
| `lead_snapshot` | `LeadRecord` JSON envelope. |
| `compliance_signals` | `auto_client_acquisition/compliance_os/contactability` output. |
| `locale` | tenant default (`ar` / `en`). |

## Output schema

```yaml
decision: qualified | needs_enrichment | rejected
bant:
  budget: 0..1
  authority: 0..1
  need: 0..1
  timeline: 0..1
overall_fit: 0..1
reason: string (≤ 200 chars, locale-matched)
required_followups: [string]
```

## Rules

1. `allowed_use ∈ {unknown, ''}` → reject.
2. `risk_level = high` → reject.
3. Missing both phone AND business email → reject.
4. Personal email domain only → `needs_enrichment`.

## Linked code

- Prompt: `prompt.yaml`
- Adapter: `core/llm/typed_output.py`
- Compliance gate: `auto_client_acquisition/compliance_os/contactability.py`
- Evals: `evals/promptfoo/qualification.yaml` (existing).

## Permissions (Cerbos)

`agent_run.execute` on resource `lead` for roles `{owner, admin,
sales_rep, agent_operator}`.
