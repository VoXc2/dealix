# Saudi Vision 2030 — Dealix alignment

The Kingdom's Vision 2030 elevates **digital economy transformation**,
**Saudi-sovereign data residency**, **PDPL compliance**, and
**non-oil-sector productivity** as pillars. This document maps each
Dealix capability to the relevant Vision 2030 / SDAIA / NTP KPI so a
government tender, NEOM RFP, or a tenant in a Vision-2030-aligned
sector can validate fit in minutes.

## Pillar A — Digital Saudi Arabia

| Vision 2030 ambition | Dealix capability | Code path |
| --- | --- | --- |
| Bilingual (Arabic-first) digital services | Arabic RTL across landing + dashboard, Hijri-Gregorian dual calendar, Arabic NLP | `frontend/src/i18n/`, `frontend/src/lib/hijri.ts`, `auto_client_acquisition/agents/nlp/arabic.py` |
| Native Saudi identity & auth | Nafath integration (admin actions + DPA signing) | `dealix/identity/nafath_client.py` |
| Government data integration | Wathq commercial registry, Yakeen identity | `dealix/enrichment/wathq_client.py`, `dealix/identity/yakeen_client.py` |
| ZATCA Phase 2 e-invoicing | UBL 2.1 + Fatoorah + TLV QR + CSR rotation | `integrations/zatca.py`, `scripts/infra/zatca_csr_rotate.sh` |
| Data sovereignty | Saudi-region deploy runbook (STC / Mobily / AWS me-central-1) | `docs/ops/saudi_region.md` |
| AI for Government / SDAIA-aligned | Per-tenant LLM cost guardrails + audit log + DPO notifications | `core/llm/cost_guard.py`, `db/models.AuditLogRecord` |

## Pillar B — PDPL compliance + data subject rights

| PDPL Article | Dealix capability | Code path |
| --- | --- | --- |
| 5 — Lawful basis | Consent ledger | `db/models.ConsentRequestRecord`, `auto_client_acquisition/compliance_os/contactability.py` |
| 6 — Explicit consent | DPA capture at onboarding step 3 | `api/routers/onboarding.py` |
| 18 — Audit trail | AuditLogRecord on every mutation | `api/security/audit_writer.py` |
| 22 — Access / portability | DSR API | `api/routers/pdpl_dsr.py` |
| 23 — Deletion | DSR delete with 14-day grace | `api/routers/pdpl_dsr.py` |
| 27 — Breach notification | Incident response runbook with 72-h DPO clock | `docs/ops/incident_response.md` |
| 29 — Cross-border transfer | Addendum + sub-processor list | `docs/CROSS_BORDER_TRANSFER_ADDENDUM.md`, `docs/compliance/SUB_PROCESSORS.md` |

## Pillar C — Saudi commercial enablement

| KPI | Dealix capability | Code path |
| --- | --- | --- |
| SMEs digitised | Self-serve onboarding wizard | `api/routers/onboarding.py`, `[locale]/onboarding/page.tsx` |
| Saudi payment ubiquity (Mada / STC Pay / Tabby / Tamara) | Multi-gateway payment stack | `dealix/payments/{moyasar,tap,tabby,tamara,stripe}_client.py` |
| Salla / Zid integration | E-commerce connectors | `dealix/connectors/{salla,zid}_client.py` |
| Open Banking (post-licence) | SAMA OB stub | `dealix/integrations/sama_open_banking.py` |

## Pillar D — Talent + national content

- Arabic-first transactional emails (`dealix/templates/ar/*.j2`).
- Bilingual ADR + ops runbooks (`docs/adr/`, `docs/ops/`).
- AGENTS.md conventions for Arabic + English code review.

## Pillar E — Trust + transparency

- SOC 2 controls map: `docs/compliance/CONTROLS.md`.
- GDPR ↔ PDPL article-to-code map: `docs/compliance/GDPR_PDPL_MAPPING.md`.
- Sub-processor live page: `landing/trust/sub-processors.html`.
- RFC 9116 security.txt: `landing/.well-known/security.txt`.
- Public roadmap: `landing/roadmap/index.html`.

## What's still gated on regulator action

| Item | Owner | ETA |
| --- | --- | --- |
| Nafath production credential | SDAIA service licensing | depends on tender |
| Yakeen API key | NIC / Elm | per-tenant via Saudi Business Gateway |
| SAMA Open Banking participant licence | SAMA | post-licence |
| ZATCA production CSID | ZATCA Fatoora portal | after KYC |
| Saudi-region cloud contract | STC / Mobily / AWS | per-customer |

Dealix is technically ready for all of the above — the code paths are
wired, returning 503 `not_configured` until the regulator issues
keys. **No additional engineering is needed** to flip them on.
