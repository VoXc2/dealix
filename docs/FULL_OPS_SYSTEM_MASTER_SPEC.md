# Dealix Full Ops System — Master Spec (الشكل النهائي)

> STATUS: architecture spec. This phase ships **documentation + config only** — no
> application code. It maps the founder's "Full Ops" vision onto the **existing**
> Dealix codebase, marks what is built vs. greenfield, and is the contract that the
> V1/V2/V3/V4 build phases implement against.
>
> Supersedes the earlier draft `docs/V12_FULL_OPS_ARCHITECTURE.md` as the single
> authoritative full-ops map.

## 1. Context & governing principle — السياق والمبدأ الحاكم

Dealix's final shape is **a governed, AI-native operating company**: it attracts,
qualifies, sells, serves, delivers, recruits partners/affiliates, and learns — under
one approval + evidence regime.

**The governing rule:**
> إذا لم يكن لكل فعل **مصدر**، **موافقة عند الخطر**، **دليل**، و**قياس** — فهو ليس
> Full Ops. هو مجرد أتمتة ناقصة.
> If an action lacks a **source**, **approval-at-risk**, **evidence**, and a
> **measurement**, it is not Full Ops — it is incomplete automation.

This spec adds **no new doctrine**. It inherits the 11 non-negotiables
([`NON_NEGOTIABLES.md`](./00_constitution/NON_NEGOTIABLES.md)) plus the affiliate/
partner extension ([`AFFILIATE_PARTNER_DOCTRINE.md`](./00_constitution/AFFILIATE_PARTNER_DOCTRINE.md)).

## 2. The 4 surfaces — الواجهات الأربع

| Surface | Audience | Status |
| --- | --- | --- |
| **Public Growth Frontend** | market / inbound leads | mostly greenfield |
| **Founder Ops Console** | founder | partially exists |
| **Customer Workspace** | paying customers | partial (`customer-portal`); V3 expansion |
| **Partner / Affiliate Portal** | partners + affiliates | greenfield (V3) |

## 3. Domain map — خريطة المجالات

Each domain maps to an **existing** canonical module or is **greenfield**. New domains
follow the canonical layout `auto_client_acquisition/<name>_os/` + `api/routers/`.
The founder spec's parallel `dealix/sales/`, `dealix/affiliates/` tree is **rejected**
to avoid duplication.

| Domain | Canonical home | Status | Notes |
| --- | --- | --- | --- |
| Governance / approvals | `dealix/governance/`, `auto_client_acquisition/governance_os/`, `approval_center/` | built | reuse as-is |
| Evidence / decision passport | `dealix/contracts/`, `evidence_control_plane_os/` | built | reuse as-is |
| Proof pack | `auto_client_acquisition/proof_os/`, `data/proofs/` | built | reuse as-is |
| Sales pipeline | `auto_client_acquisition/sales_os/`, `api/routers/domains/sales/` | built | extend |
| Growth / GTM | `auto_client_acquisition/gtm_os/`, `autonomous_growth/` | built | extend |
| Data / DQ / source passport | `auto_client_acquisition/data_os/` | built | reuse for lead scoring |
| Delivery | `auto_client_acquisition/delivery_os/` | built | extend |
| Value / referral ledger | `auto_client_acquisition/value_os/`, `partnership_os/referral_tracker.py` | built | reuse as the affiliate money path |
| Support autopilot | `auto_client_acquisition/support_os/`, `data/workflows/support.yaml` | partial | classifier + escalation greenfield |
| Marketing factory | `auto_client_acquisition/gtm_os/` + `autonomous_growth/` | partial | no `marketing_os`; use `gtm_os` |
| Partner network | `auto_client_acquisition/partnership_os/` | partial | portal greenfield |
| **Affiliate program** | `auto_client_acquisition/partnership_os/` (extends referral) | **greenfield** | no separate `affiliate_os`; rides referral ledger |
| Agent orchestration | `auto_client_acquisition/agent_os/`, `core/agents/` | partial | orchestrator greenfield — see spec below |

## 4. Event / approval / evidence model — نموذج الأحداث والموافقات والأدلة

No re-spec — these are built. Reference points:

- **Event envelopes & contracts:** `dealix/contracts/`
- **Approval gate:** `auto_client_acquisition/approval_center/`, `dealix/governance/approvals.py`
- **Evidence ledger:** `auto_client_acquisition/evidence_control_plane_os/`, `value_os/value_ledger.py`
- **Decision passport / golden chain:** `dealix/contracts/decision.py`, API `/api/v1/decision-passport/golden-chain`

Every important Full Ops action emits an evidence event; every revenue event requires
an `invoice_paid` proof; every customer-facing final output requires a review record.

## 5. Agent orchestration — تنسيق الوكلاء

See [`engineering/AGENT_ORCHESTRATOR.md`](./engineering/AGENT_ORCHESTRATOR.md).
Agent scopes and approval rules: [`data/config/agent_permissions.yaml`](../data/config/agent_permissions.yaml).

## 6. Frontend route map — خريطة مسارات الواجهة

All routes under `frontend/src/app/[locale]/` (locales: `ar`, `en`; RTL for `ar`).

| Route | Surface | Status |
| --- | --- | --- |
| `dashboard/` | Founder Ops | exists |
| `pipeline/` | Founder Ops | exists |
| `approvals/` | Founder Ops | exists |
| `agents/` | Founder Ops | exists |
| `clients/` | Founder Ops | exists |
| `analytics/` | Founder Ops | exists |
| `customer-portal/` | Customer Workspace | exists (partial) |
| `trust-check/` | Public Growth | exists |
| `offer/lead-intelligence-sprint/` | Public Growth | exists |
| `dealix-diagnostic/` | Public Growth | greenfield (V1) |
| `risk-score/` | Public Growth | greenfield (V1) |
| `proof-pack/` | Public Growth | greenfield (V2) |
| `partners/`, `affiliate/` | Public Growth | greenfield (V2) |
| `support/` | Public Growth | greenfield (V2) |
| `templates/`, `webinars/` | Public Growth | greenfield (V2) |
| `ops/founder/` (command center) | Founder Ops | greenfield — may consolidate `dashboard/` |
| `ops/evidence/` | Founder Ops | greenfield (V1) |
| `ops/marketing/`, `ops/support/`, `ops/partners/`, `ops/affiliates/` | Founder Ops | greenfield (V2) |
| `partner/dashboard/` | Partner/Affiliate Portal | greenfield (V3) |

## 7. Backend API map — خريطة الـ APIs

156 routers exist under `api/routers/`. Selected map (real prefix `/api/v1/...`):

| Endpoint area | Status |
| --- | --- |
| `dashboard/metrics`, `revenue-pipeline/summary` | exists |
| `approvals/pending`, `approvals/{id}/approve|reject` | exists |
| `v3/command-center/snapshot` | exists |
| `decision-passport/golden-chain` | exists |
| `public/risk-score`, `public/proof-pack-request` | greenfield (V1) |
| `public/partner-apply`, `public/affiliate-apply`, `public/support` | greenfield (V2) |
| `support/tickets/{id}/classify|draft-response|escalate` | greenfield (V2) |
| `ops/marketing/dashboard`, `ops/partners/dashboard`, `ops/affiliates/dashboard` | greenfield (V2) |
| `partners/{id}/referrals`, `commissions/calculate`, `payouts/mark-paid` | greenfield (V3) |

New routers keep the repo convention: prefix `/api/v1/<area>`, return a
`governance_decision` field, tenant-scoped.

## 8. Rollout — التنفيذ المرحلي

Mapped to **real modules**, not the founder spec's invented file tree.

- **V1 (~14 days)** — Public `dealix-diagnostic` + `risk-score` pages; lead capture
  + scoring via `data_os`; `ops/evidence` view; Founder Command Center consolidation.
  Touches: `data_os`, `sales_os`, `governance_os`, frontend public pages.
- **V2 (~30 days)** — `support_os` classifier + escalation; marketing factory in
  `gtm_os`; affiliate + partner application intake; `proof-pack` public page.
  Wires: `support_intents.yaml`, `marketing_cadence.yaml`, `affiliate_rules.yaml`,
  `partner_rules.yaml`.
- **V3 (~90 days)** — Agent Orchestrator (`agent_os/`); Partner/Affiliate Portal;
  commissions on the referral ledger (`value_os/`); Customer Workspace expansion;
  Full Ops Health dashboard (`reporting_os`).
- **V4 (after paid proof)** — Benchmark engine (`benchmark_os`), Decision Passport
  builder, multi-client modules.

## 9. Anti-duplication index — فهرس منع التكرار

These already exist. The build phases **extend** them; they are **not** re-authored.

| Topic | Existing source |
| --- | --- |
| Prior full-ops draft | `docs/V12_FULL_OPS_ARCHITECTURE.md`, `docs/FULL_OPS_10_LAYER_*.md` |
| Marketing system | `docs/MARKETING_AND_CONTENT_SYSTEM.md`, `docs/sales-kit/dealix_marketing_full_playbook.md` |
| Partner program | `docs/partners/`, `docs/40_partners/`, `docs/AGENCY_PARTNER_PROGRAM.md` |
| Referral program | `docs/sales-kit/dealix_referral_program.md` |
| Support KB | `docs/knowledge-base/support_faq_{ar,en}.md` |
| Offer ladder / pricing | `docs/OFFER_LADDER_AND_PRICING.md` |
| 90-day plan | `docs/90_DAY_BUSINESS_EXECUTION_PLAN.md` |
| Runtime workflows | `data/workflows/*.yaml` |

## 10. 11 non-negotiables compliance — التوافق مع غير القابل للتفاوض

| Surface | How it honors the doctrine |
| --- | --- |
| Public Growth | no hidden pricing (#8); lead capture needs consent (#6); no scraped lists (#4) |
| Founder Ops | every risky action routes through the approval center (#1, #2); audit chain kept (#11) |
| Support Autopilot | high/critical tickets escalate, never auto-answered (see `support_knowledge_risk.yaml`); no silent failures (#9) |
| Marketing factory | external assets stay drafts until approved (#1); claims need a source (#7) |
| Affiliate / Partner | commission only after `invoice_paid` (#2); disclosure mandatory; no cold WhatsApp (#3) — see `AFFILIATE_PARTNER_DOCTRINE.md` |
| Agents | every agent bounded by `agent_permissions.yaml` (#10); every run logged (#11) |

## 11. Config layer — طبقة الإعداد

New design-contract YAML under `data/config/` (mirrors `data/workflows/`).
Not yet code-wired — build phases consume them.

| File | Domain | Consumed in |
| --- | --- | --- |
| [`affiliate_rules.yaml`](../data/config/affiliate_rules.yaml) | affiliate | V2/V3 |
| [`partner_rules.yaml`](../data/config/partner_rules.yaml) | partner | V2/V3 |
| [`support_intents.yaml`](../data/config/support_intents.yaml) | support | V2 |
| [`support_knowledge_risk.yaml`](../data/config/support_knowledge_risk.yaml) | support | V2 |
| [`agent_permissions.yaml`](../data/config/agent_permissions.yaml) | agents | V3 |
| [`marketing_cadence.yaml`](../data/config/marketing_cadence.yaml) | marketing | V2 |

Policy that is already **hardcoded** (approval matrix, stage transitions, offer
ladder) is intentionally **not** duplicated as YAML here; extracting it to config is
a separate, optional future refactor.

## 12. Out of scope (this phase)

- All Python, FastAPI routers, and frontend pages/components.
- New `tests/test_no_*.py` gates (named as candidates in the config files + doctrine).
- Wiring the YAML configs to code.
- Customer Workspace & Partner/Affiliate Portal UIs (V3+).
