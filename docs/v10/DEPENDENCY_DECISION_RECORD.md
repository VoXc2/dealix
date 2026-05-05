# Dealix v10 — Dependency Decision Record

> Every time a tool moves from `optional_adapter` to `real_dependency`,
> the founder signs off here. **No real dependency installs without a
> matching entry.** Each section corresponds to a Decision Pack item.

**Date opened:** 2026-05-05
**Format:** append-only. Earlier decisions are immutable; new
decisions add new sections.

---

## §S5-prior — Already approved as `native_pattern`

| Tool | Module | Commit | Founder approval |
|---|---|---|---|
| Open Design | `auto_client_acquisition/designops/` + `design-systems/` + `design-skills/` | `bf9516e` | ✅ implicit (shipped during v7 closure) |

No real dependency installed; pattern is native + tested.

---

## §S6 — First `optional_adapter` approvals (gated on 3 paid Pilots)

**Status:** ☐ NOT yet eligible. Eligibility requires:
- 3 paying Pilots delivered (real Moyasar invoices, not test-mode)
- 3 signed Proof Packs (customer-attested, with explicit consent)
- No active customer complaint about Pilot delivery
- Founder review of LICENSE + supply-chain + version-skew per item

When eligible, the following adapters become available for opt-in.
Each requires this section's `Founder decision date` + `Founder
signature` to be filled.

### §S6-1. LiteLLM
- **Why now:** Native cost router + budget caps + model tiers proven over first 3 Pilots; real LiteLLM adds 100+ vendor coverage with virtual keys.
- **License:** MIT
- **Risks:** supply-chain footprint, version skew with vendor SDKs
- **Mitigations:** behind env flag `DEALIX_LITELLM_ENABLED=true`; native pattern stays default for fallback
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Module switched:** `auto_client_acquisition/llm_gateway_v10/`

### §S6-2. Langfuse
- **Why now:** Native trace schema in observability_v10 + observability_v6 produces 100s of traces; real Langfuse adds dashboards + dataset management + prompt version pinning
- **License:** MIT (core); EE for advanced features
- **Risks:** PII export risk if redactor mis-wired
- **Mitigations:** redactor runs BEFORE export; explicit allowlist of fields
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Module switched:** `auto_client_acquisition/observability_v10/`

### §S6-3. Qdrant
- **Why now:** Native retrieval contract proven; first paying customer's documents need a real vector DB
- **License:** Apache-2
- **Risks:** hosting cost, embedding cost, query latency
- **Mitigations:** behind env `DEALIX_QDRANT_URL`; native fallback for local dev
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Module switched:** `auto_client_acquisition/knowledge_v10/`

### §S6-4. Sentry (optional)
- **Why now:** error monitoring beyond log files
- **License:** BSL / FSL — verify before install
- **Risks:** PII in stack traces, paid tier above quota
- **Mitigations:** PII scrubbing before send; free tier default
- **Founder decision date:** ☐
- **Founder signature:** ☐

### §S6-5. Cal.com (optional)
- **Why now:** Diagnostic / Pilot booking link instead of manual scheduling
- **License:** AGPL-3 — verify
- **Risks:** AGPL — careful before commercial use
- **Mitigations:** SaaS-hosted Cal.com only; no self-host yet
- **Founder decision date:** ☐
- **Founder signature:** ☐

---

## §S7 — First `real_dependency` approvals (gated on 5+ paying customers)

**Status:** ☐ NOT yet eligible. Eligibility requires:
- 5+ paying customers
- 30+ days operating with the corresponding §S6 adapter
- Concrete failure mode that the native pattern can't cover
- Security review of the dependency documented here
- License compliance verified (no AGPL/GPL contagion if commercial)

### §S7-1. Real LiteLLM (gateway in production)
- **Eligibility prerequisite:** §S6-1 signed + 30 days of LiteLLM adapter usage
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐
- **License compliance:** ☐ MIT verified

### §S7-2. Real Langfuse (managed or self-hosted)
- **Eligibility prerequisite:** §S6-2 signed + 30 days of Langfuse adapter usage
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐
- **License compliance:** ☐ MIT (core) verified

### §S7-3. Real Qdrant (managed cluster)
- **Eligibility prerequisite:** §S6-3 signed + first paying customer's RAG queries served
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐
- **License compliance:** ☐ Apache-2 verified

### §S7-4. Real Promptfoo (CI integration)
- **Eligibility prerequisite:** native safety_v10 eval pack stable for 30 days
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐
- **License compliance:** ☐ MIT verified

### §S7-5. Real Twenty CRM (replacement for native CRM model)
- **Eligibility prerequisite:** 10+ customers + native CRM model proven
- **License:** AGPL-3 — careful — may dictate self-host only
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐
- **License compliance:** ☐ AGPL impact assessed

### §S7-6. Real Chatwoot (omnichannel inbox)
- **Eligibility prerequisite:** 5+ customers + WhatsApp Business API approved
- **License:** MIT
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐
- **License compliance:** ☐ MIT verified

### §S7-7. Real Temporal (workflow runtime)
- **Eligibility prerequisite:** native workflow_os_v10 produced documented Pilot-delivery failure
- **License:** MIT
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐

### §S7-8. Real PostHog (product analytics)
- **Eligibility prerequisite:** §S6 + 5+ customers + measurable funnel
- **License:** MIT
- **Founder decision date:** ☐
- **Founder signature:** ☐
- **Security review:** ☐

---

## §S8 — Defer / Reject list

Tools explicitly NOT considered for `real_dependency` until concrete demand justifies them:

| Tool | Reason |
|---|---|
| Supabase / Appwrite | Replacement risk for current FastAPI stack — not justified |
| Keycloak / Zitadel / Authentik | Multi-tenant + SSO not required at single-founder stage |
| Odoo / ERPNext / SuiteCRM | Stack mismatch (PHP/Frappe vs FastAPI); inspiration only |
| n8n | Privilege-escalation risk if exposed; defer pending security model |
| Browser-use | Hard rule: no live browser actions on customer's behalf |
| Mautic | Marketing automation gated on consent registry maturity |
| Crawl4AI / Firecrawl | Scraping policy enforces allowed-source list; defer adapter |
| Milvus / OpenSearch / Dagster | Heavyweight infra; defer until billions of rows |

Each entry can be revisited when a real customer requirement appears.

---

## §S9 — Append future decisions here

When a new decision is made, append a new section with:
- Tool name
- Eligibility prerequisite
- License
- Risks + mitigations
- Founder decision date
- Founder signature

---

## How decisions are signed

1. Founder reads the corresponding `§Sn-X` entry
2. Founder verifies all eligibility prerequisites met
3. Founder fills `Founder decision date` (`YYYY-MM-DD`)
4. Founder fills `Founder signature` (initials or full name)
5. Founder commits the change with message
   `chore(decision): §Sn-X — approve <tool>`
6. CI runs tests + secret scan
7. After merge, the corresponding adapter / dependency may be added
   in a separate PR by Claude Code

---

— Dependency Decision Record v1.0 · 2026-05-05 · Dealix
