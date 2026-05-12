# Billing flow

Gateway-agnostic checkout + invoice fan-in.

```mermaid
flowchart LR
    A[Customer] --> B{Currency?}
    B -- SAR --> C[Moyasar checkout<br/>api/routers/pricing.py]
    B -- USD/EUR/AED --> D[Stripe checkout<br/>api/routers/billing.py]
    C --> E[Moyasar hosted page]
    D --> F[Stripe hosted page]
    E -->|webhook| G[/api/v1/webhooks/moyasar]
    F -->|webhook| H[/api/v1/billing/webhooks/stripe]
    G & H --> I[Signature verify]
    I --> J[(AuditLogRecord entity_type=invoice)]
    I --> K[Lago meter event<br/>dealix/billing/lago_client.py]
    K --> L[Loops trigger<br/>payment_received]
    L --> M[Knock notify customer + founder]
    J --> N[GET /api/v1/customers/<id>/invoices<br/>renders in /billing page]
```

Reference paths:

- Moyasar: `dealix/payments/moyasar.py`, `api/routers/pricing.py`.
- Stripe: `dealix/payments/stripe_client.py`, `api/routers/billing.py`.
- Metering: `dealix/billing/lago_client.py`.
- Marketing trigger: `dealix/marketing/loops_client.py`.
- Audit row source: `api/middleware/http_stack.AuditLogMiddleware`.
