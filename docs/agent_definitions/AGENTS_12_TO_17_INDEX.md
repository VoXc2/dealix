# Agents #12 → #17 — Index & Coverage Map

**Date:** 2026-06-03
**Status:** Registered, gap audits in progress

This document maps the six newly-registered Dealix agents, their scope,
deliverables, and the current coverage state in the repository.

## Why These Six Agents

Agents 1 → 11 already built (or mapped) the **core operating fabric** of
Dealix: market, business, WhatsApp, commercial expansion, operations, security,
founder control, QA/E2E, analytics, customer success, partnerships, product
strategy. Agents 12 → 17 close the **governance, deployment, language,
service-productization, capital-readiness, and procurement** edges that are
needed before a real production launch.

## Coverage Map

| Pillar | Agent | Status |
| --- | --- | --- |
| السوق (Market) | prior agents | Done |
| التجارة (Commercial) | prior agents | Done |
| العمليات (Operations) | prior agents | Done |
| الأمان (Security) | prior agents | Done |
| الواجهة (UI/UX) | prior agents | Done |
| الاختبارات (QA/E2E) | prior agents | Done |
| التحليلات (Analytics) | prior agents | Done |
| الاحتفاظ (Retention) | prior agents | Done |
| الشراكات (Partnerships) | prior agents | Done |
| المنتج (Product) | prior agents | Done |
| **البنية (Infrastructure)** | **Agent #12 — Infra, Reliability & Deployment** | **Registered** |
| **القانون (Legal)** | **Agent #13 — Legal, Compliance & Contract Guard** | **Registered** |
| **التوطين (Localization)** | **Agent #14 — Saudi Localization & Arabic Experience** | **Registered** |
| **الخدمات القابلة للبيع (Productized Services)** | **Agent #15 — Productized Services & Delivery Templates** | **Registered** |
| **الجاهزية الاستراتيجية (Data Room)** | **Agent #16 — Data Room & Strategic Readiness** | **Registered** |
| **التكاليف والموردين (Procurement)** | **Agent #17 — Vendor, Procurement & Cost Optimization** | **Registered** |

## Agent Detail Cards

| # | Domain | Mission | First-Phase Files |
| - | --- | --- | --- |
| 12 | Infrastructure | Make Dealix deployable, observable, reliable, recoverable | `docs/infra/ENVIRONMENT_POLICY_AR.md`, `docs/infra/STAGING_PRODUCTION_POLICY_AR.md`, `docs/infra/SECRETS_MANAGEMENT_AR.md` |
| 13 | Legal | Build legal/compliance guardrails, route sensitive work to humans | `docs/legal/LEGAL_REVIEW_POLICY_AR.md`, `docs/legal/CONTRACT_HANDOFF_CHECKLIST_AR.md`, `docs/legal/CASE_STUDY_PERMISSION_POLICY_AR.md` |
| 14 | Localization | Make Dealix feel native to Saudi B2B | `docs/localization/SAUDI_LOCALIZATION_OS_AR.md`, `docs/localization/ARABIC_BRAND_VOICE_AR.md`, `docs/localization/TERMINOLOGY_GLOSSARY_AR.md` |
| 15 | Productized Services | Turn offers into sellable, deliverable, measurable services | `docs/productized_services/PRODUCTIZED_SERVICES_OS_AR.md`, `data/productized_services/services.yaml` |
| 16 | Data Room | Prepare for investors, partners, enterprise, grants | `docs/data_room/DATA_ROOM_INDEX_AR.md`, `docs/data_room/COMPANY_OVERVIEW_AR.md` |
| 17 | Procurement | Reduce cost, eliminate sprawl, control subscriptions | `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`, `data/procurement/vendors.jsonl` |

## Current State of Each Domain (Repo Audit)

| Domain | Directory | Existing Content | Gap |
| --- | --- | --- | --- |
| Infrastructure | `docs/infra/` | **Does not exist** | Full creation needed |
| Legal | `docs/legal/` | `COMPLIANCE_CERTIFICATIONS.md`, `DPA_TEMPLATE_AR.md`, `DPO_*`, `DSAR_*`, `ENTERPRISE_MSA_TEMPLATE.md`, `FOUNDER_RISK_AND_COMPLIANCE_REGISTER_AR.md`, `SUB_PROCESSOR_*` | Operational review policy & handoff flow missing |
| Localization | `docs/localization/` | `ARABIC_TONE_LIBRARY.md`, `SAUDI_MENA_LOCALIZATION_SYSTEM.md` | Brand voice, glossary, WhatsApp UX, proposal style missing |
| Productized Services | `docs/productized_services/` | **Does not exist** | Full creation needed |
| Data Room | `docs/data_room/` | `DEALIX_BOARD_BRIEF_AR.md`, `DEALIX_COMPANY_ONE_PAGER_AR.md`, `INVESTOR_PARTNER_MEMO_AR.md` | Structured index, full section coverage missing |
| Procurement | `docs/procurement/` | **Does not exist** | Full creation needed |

## Execution Order (Recommended)

1. **Agent 12** (Infra) — first, because infra gaps block any other
   operational work and CI / GitHub Actions are the highest-risk
   attack surface for agentic workflows.
2. **Agent 13** (Legal) — second, because legal handoffs gate the
   contract / case-study / claims work of every other agent.
3. **Agent 14** (Localization) — third, because every client-facing
   artifact depends on the tone glossary.
4. **Agent 15** (Productized Services) — fourth, because it consumes
   the localization glossary and the legal review triggers.
5. **Agent 16** (Data Room) — fifth, because it summarizes what the
   other agents have already produced.
6. **Agent 17** (Procurement) — last, because it depends on the
   finalized tool list from infra + ops agents.

## Cross-Cutting Security Posture (applies to ALL six agents)

The 2026 research on **Agentic Workflow Injection in GitHub Actions**
(`arXiv:2605.07135`) and **Indirect Prompt Injection in Tool-Augmented
Agents** (`arXiv:2604.11790`) makes the following rules non-optional for
any new agent in this repo:

- Treat all `issue_body`, `PR comment`, fetched web content, MCP
  responses, and skill files as **untrusted input**.
- Never let untrusted text reach a tool call that can mutate state,
  send messages, or move money.
- Defense lives at **tool-call boundaries** (allowlists, schema
  validation, allow/deny lists), not in the model prompt.
- Any new agent that needs to write to disk, run a script, call an
  API, or send a message must declare its **trust boundary** in
  `docs/16_agents/AGENT_TOOL_BOUNDARY.md` (existing) and reference it
  from its definition file.
