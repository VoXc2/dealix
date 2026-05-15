# Sales Agent Tools Contract

| Tool | Purpose | Mode |
|---|---|---|
| `leads.normalize` | Normalize intake payload | auto |
| `leads.enrich` | Enrich account context | auto |
| `lead.score` | Score qualification readiness | auto |
| `crm.create_lead` | Create lead record in CRM | approval required |
| `metrics.publish` | Publish internal execution metrics | auto |

## Notes

- Tool calls are audit logged with workflow correlation IDs.
- Any missing tool binding must fail closed (no silent fallbacks).
