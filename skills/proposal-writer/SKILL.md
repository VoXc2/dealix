# Proposal Writer (Khaliji Arabic + ZATCA-aware)

Drafts a Saudi-business-appropriate proposal in Arabic Khaliji tone.
Pricing references are ZATCA-Phase-2-compatible (line items with
VAT 15%).

## Inputs

| Variable | Source |
| --- | --- |
| `lead` | enriched `LeadRecord`. |
| `customer_tenant` | the seller's TenantRecord (logo, voice, pricing). |
| `pricing_plan_id` | which plan we're proposing. |
| `locale` | `ar` (default) / `en`. |
| `recipient_email` | the one email allowed to appear verbatim. |

## Output schema

```yaml
subject: string (≤ 80 chars)
body_ar: string (≤ 1200 chars)
next_steps: [string]  # 1..3 items
suggested_meeting_window_riyadh: ISO start/end
expected_value_sar: number | null
```

## Rules

1. No invented metrics or testimonials.
2. No PII (no NID, no IBAN, no VAT, no email other than `recipient_email`).
3. Formal Khaliji Arabic.
4. No all-caps. No exclamation marks.

## Linked code

- Prompt: `prompt.yaml` (mirrors `dealix/prompts/proposal.yaml`).
- Guardrails: `core/llm/guardrails.guard_proposal_output`.
- ZATCA invoice generator: `integrations/zatca.py`.
- Evals: `evals/promptfoo/proposal.yaml`.
