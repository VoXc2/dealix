# Data flow

End-to-end path of a customer lead through Dealix.

```mermaid
flowchart LR
    A[Web form / WhatsApp / CSV / Partner] -->|POST| B[/api/v1/public/demo-request<br/>or /api/v1/leads/]
    B --> C[Pydantic + rate limit + tenant isolation middleware]
    C --> D[(LeadRecord)]
    D --> E[Enrichment chain]
    E -->|Wathq → Apollo → Clearbit| F[(LeadRecord.meta_json.enrichment)]
    F --> G[Scoring + ICP match]
    G -->|fit_score, urgency_score| H[(LeadScoreRecord)]
    H --> I{Score >= threshold?}
    I -->|yes| J[Inngest workflow:<br/>proposal_draft]
    I -->|no| K[Outreach queue with approval flag]
    J --> L[Knock notification → founder]
    K --> M[Approval Center UI]
```

Reference paths:

- Public surface: `api/routers/public.py`, `api/routers/leads.py`.
- Middleware: `api/middleware/tenant_isolation.py`,
  `api/middleware/bopla_redaction.py`, `api/security/rate_limit.py`.
- Enrichment: `dealix/enrichment/{wathq,apollo,clearbit}_client.py`.
- Scoring: `auto_client_acquisition/pipelines/scoring.py`.
- Durable workflows: `dealix/workflows/inngest_app.py`.
- Notifications: `dealix/integrations/knock_client.py`.
