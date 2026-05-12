# Authentication & authorization

Three concurrent surfaces — JWT, API key, WorkOS SSO — all resolve to the
same tenant_id / user_id pair on `request.state`.

```mermaid
flowchart TD
    subgraph Inbound
      A[Browser / API caller / Partner]
    end
    A --> B{Auth header?}
    B -- Bearer JWT --> C[JWT verify<br/>api/security/jwt.py]
    B -- X-API-Key --> D[API key match<br/>api/security/api_key.py]
    B -- SSO callback --> E[/auth/sso/callback<br/>api/routers/sso.py]
    C & D --> F[request.state.tenant_id<br/>request.state.user_id]
    E --> G[WorkOS profile<br/>dealix/identity/workos_client.py]
    G --> H[Tenant lookup<br/>by meta_json.workos_org_id]
    H --> I[Mint JWT pair]
    I --> F
    F --> J{Cerbos PDP configured?}
    J -- yes --> K[core/authz.allowed<br/>→ Cerbos /api/check/resources]
    J -- no --> L[core/authz._static_rbac<br/>mirrors cerbos/policies/*.yaml]
    K & L --> M[Endpoint handler runs<br/>or 403 cross_tenant_access_denied]
```

Reference paths:

- JWT: `api/security/jwt.py`, `api/routers/auth.py`.
- API key + tenant resolution: `api/security/api_key.py`,
  `api/middleware/tenant_isolation.py`.
- SSO: `api/routers/sso.py`, `dealix/identity/workos_client.py`.
- Authorization adapter: `core/authz.py`,
  `cerbos/policies/dealix_resources.yaml`.
