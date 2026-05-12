# Incident response runbook

Authoritative playbook for on-call. Pair with `docs/sla.md` (severity
definitions + MTTA / MTTR) and `docs/ops/postmortem_template.md`.

## 1. Detection sources

In priority order:

1. **BetterStack uptime monitor** firing on `/healthz` failure.
2. **Sentry alert** matching the production project DSN.
3. **Grafana SLO burn-rate alert** (multi-window).
4. **Customer report** via `/api/v1/support/tickets` tagged `urgent`
   or in our shared Slack #customer-escalations.

## 2. Triage tree

```
incoming signal
├── /healthz returns 5xx?            → SEV-1 (full outage)
├── p95 > 3× baseline for 5 min?     → SEV-2 (degraded)
├── single tenant impacted?          → SEV-2
├── feature flag misconfig only?     → SEV-3
└── cosmetic UI bug?                 → P3 backlog, no SEV
```

## 3. Roles during an incident

| Role | Who | Responsibility |
| --- | --- | --- |
| **Incident Commander (IC)** | On-call (see OPS_ROTATION.md) | Drives the incident. Sole owner of decisions. |
| **Comms** | IC or designated | Posts to status page, customer email, Slack. |
| **Scribe** | Anyone present | Time-stamped notes in a shared doc; becomes postmortem source. |

## 4. Communication ladder

SEV-1:
1. T+0 — IC declares in #incidents Slack + opens an incident doc.
2. T+5 — status page banner: "We are investigating an outage on api.dealix.me".
3. T+15 — first customer email to all paying tenants (use the
   `outage_acknowledgement_v1` template in `dealix/templates/`).
4. Every 30 min until resolved — status update with what we know and
   what we're trying.
5. Post-resolution: customer email within 2 hours summarising what
   happened, impact window, what we changed.

SEV-2: status page + Slack only; customer email per affected tenant.

SEV-3: Slack thread; status page update only if customer-facing.

## 5. Decision checklist (IC)

- [ ] Are we shedding traffic safely? (rate-limit headers, error pages)
- [ ] Should we rollback the last deploy? (last deploy SHA in Sentry release)
- [ ] Is the DB the bottleneck? (connection pool / slow queries in Grafana)
- [ ] Is an upstream LLM provider failing? (Portkey fallback should
      handle automatically — verify in Portkey dashboard)
- [ ] Are we still serving authenticated traffic? (`/api/v1/auth/me`)
- [ ] Have we notified DPO if PII was exposed? (PDPL Art. 27 — 72h)

## 6. Common runbooks

| Symptom | Likely cause | First action |
| --- | --- | --- |
| `/healthz` 5xx | Postgres down or pool exhausted | Check Grafana pg_pool dashboard; restart API if pool starved. |
| `/api/v1/status` migrations=multiple_heads | Bad merge introduced a second alembic head | `alembic merge heads -m "..."` |
| Surge of 429s | Hot tenant / partner | Bump that tenant's bucket in `api/security/rate_limit.py` or contact them. |
| LLM cost spike | Prompt regression | Roll back the prompt YAML; verify with promptfoo. |
| Webhook signature failures | Vendor rotated their secret | Update env via Infisical; restart services. |

## 7. Resolution → postmortem

Every SEV-1 and SEV-2 gets a blameless postmortem within **5 business
days**, using `docs/ops/postmortem_template.md`, committed under
`docs/ops/postmortems/<YYYY-MM-DD>-<short-title>.md`.

Action items from postmortems land as GitHub issues with the
`postmortem` label; review at the next weekly ops sync.
