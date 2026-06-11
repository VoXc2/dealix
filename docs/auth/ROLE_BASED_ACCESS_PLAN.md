# Role-Based Access Plan (Dealix)

## Roles (V1)
- `founder` — full access
- `sales` — CRM, drafts, proposals
- `delivery_lead` — delivery, proof
- `viewer` — read-only

## Mapping
| Route | founder | sales | delivery_lead | viewer |
|-------|---------|-------|---------------|--------|
| /crm | ✓ | ✓ | ✓ | ✓ |
| /war-room | ✓ | — | — | — |
| /operator | ✓ | — | — | — |
| /data-room | ✓ | — | — | — |
| /outreach-lab | ✓ | ✓ | — | — |
| /proof-vault | ✓ | — | ✓ | — |
| /client-portal | ✓ | — | ✓ | — |

## V6 limitation
- Single-user gate (founder) only
- Full RBAC requires auth provider

## Migration
- Add `actor` field to all writes
- Add `role` field to session
- Filter routes by role
