# Permission Mirroring

AI may only access data and perform actions that the **requesting human or service principal** is authorized to access or perform. This is foundational for **enterprise** trust.

## Rules

1. **AI inherits** the authenticated user’s permissions (workspace / tenant / role).
2. AI **cannot bypass** RBAC or break isolation between tenants.
3. AI **cannot** send, publish, delete, or modify **externally** without **explicit** permission path (often approval), even if the user “could” do it manually.
4. **Sensitive** actions may require **approval** in addition to raw role access (defense in depth).
5. **Log** material actions per [`AUDIT_LOG_POLICY.md`](AUDIT_LOG_POLICY.md).

## Examples

| User / role | AI allowed (typical) |
|-------------|----------------------|
| Sales rep | Leads/opportunities in **their** territory only |
| Support lead | Support KB + tickets in **their** scope—not finance vault |
| Executive | Exec dashboards **they** are entitled to |
| External client user | **Their** company workspace only—not other tenants |

**Taxonomy:** map risky behaviors to [`AI_ACTION_TAXONOMY.md`](AI_ACTION_TAXONOMY.md).
