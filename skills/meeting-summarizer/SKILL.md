# Meeting Summarizer

Converts a Vapi voice transcript or a manually-uploaded meeting note
into a structured summary + action items + suggested CRM updates.

## Inputs

`transcript: string`, `locale`, optional `crm: hubspot | salesforce`.

## Output

```yaml
summary_ar: string
summary_en: string
action_items:
  - owner: string
    text: string
    due: ISO
deal_updates: {stage?: string, next_step?: string, notes?: string}
risks: [string]
```
