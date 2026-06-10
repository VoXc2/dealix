# File Ownership Map — Dealix

> **Last updated:** 2026-06-03 · **Owner:** Agent #35 (Final Integration) · **Version:** v1.0
> **Purpose:** explicit owner per file. Prevents "everyone owns it, nobody owns it" anti-pattern.
> **Owners:** founder / sales_lead / csm / engineer / data_lead / ai_governance_lead / marketing / legal / partnerships

---

## 1) Owners (Roster)

| Code | Owner | Scope |
|------|-------|-------|
| `founder` | Founder (CEO) | strategic decisions, final approval, all systems |
| `sales_lead` | Head of Sales | pipeline, deal risk, ABM, pricing |
| `csm` | Customer Success Lead | delivery, renewal, expansion, client health |
| `engineer` | Engineering Lead | code, schema, infra, deploys |
| `data_lead` | Data Lead | data products, benchmarks, learning loop |
| `ai_gov_lead` | AI Governance Lead | agent registry, permissions, evals, incidents |
| `marketing` | Marketing Lead | offers, FAQ, CTAs, public pages |
| `legal` | Legal Lead | contracts, PDPL, compliance |
| `partnerships` | Partnerships Lead | partners, channel |

---

## 2) New Wave 29-33 — File Ownership

### 2.1 Enterprise Sales (Agent 29) — owner: `sales_lead`

| File | Owner | Last Review | Change Control |
|------|-------|-------------|----------------|
| `docs/enterprise_sales/ENTERPRISE_SALES_OS_AR.md` | sales_lead | 2026-06-03 | needs founder sign-off |
| `docs/enterprise_sales/ACCOUNT_BASED_SELLING_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/TARGET_ACCOUNT_PROFILE_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/STAKEHOLDER_MAPPING_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/BUYING_COMMITTEE_PLAYBOOK_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/ENTERPRISE_DISCOVERY_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/MUTUAL_ACTION_PLAN_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/EXECUTIVE_BUSINESS_CASE_AR.md` | sales_lead | 2026-06-03 | — |
| `docs/enterprise_sales/PILOT_TO_EXPANSION_PLAYBOOK_AR.md` | sales_lead + csm | 2026-06-03 | — |
| `docs/enterprise_sales/PROCUREMENT_SALES_PLAYBOOK_AR.md` | sales_lead + legal | 2026-06-03 | — |
| `docs/enterprise_sales/ENTERPRISE_DEAL_RISK_REVIEW_AR.md` | sales_lead | 2026-06-03 | weekly review |
| `data/enterprise_sales/*.jsonl` | sales_lead | 2026-06-03 | append-only with evidence_level |
| `schemas/enterprise_account.schema.json` | sales_lead + engineer | 2026-06-03 | breaking change = RFC |
| `schemas/stakeholder.schema.json` | sales_lead | 2026-06-03 | — |
| `schemas/mutual_action_plan.schema.json` | sales_lead | 2026-06-03 | — |
| `schemas/enterprise_deal_risk.schema.json` | sales_lead | 2026-06-03 | — |
| `schemas/enterprise_questionnaire.schema.json` | sales_lead + legal | 2026-06-03 | — |
| `schemas/enterprise_risk.schema.json` | sales_lead | 2026-06-03 | — |
| `schemas/discovery_note.schema.json` | sales_lead | 2026-06-03 | — |
| `reports/enterprise_sales/*` | sales_lead | 2026-06-03 | weekly |

### 2.2 AI Governance (Agent 30) — owner: `ai_gov_lead`

| File | Owner | Last Review | Change Control |
|------|-------|-------------|----------------|
| `docs/ai_governance/AI_AGENT_GOVERNANCE_OS_AR.md` | ai_gov_lead + founder | 2026-06-03 | — |
| `docs/ai_governance/AGENT_AUTONOMY_LEVELS_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `docs/ai_governance/AGENT_ACCESS_RIGHTS_POLICY_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `docs/ai_governance/AGENT_PERMISSION_LIFECYCLE_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `docs/ai_governance/AGENT_ONBOARDING_OFFBOARDING_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `docs/ai_governance/AGENT_EVAL_CADENCE_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `docs/ai_governance/AGENT_RETIREMENT_POLICY_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `docs/ai_governance/HUMAN_APPROVAL_BOUNDARIES_AR.md` | ai_gov_lead + founder | 2026-06-03 | founder approves |
| `docs/ai_governance/AI_AGENT_INCIDENT_RESPONSE_AR.md` | ai_gov_lead | 2026-06-03 | — |
| `data/ai_governance/agent_registry.jsonl` | ai_gov_lead | 2026-06-03 | append-only |
| `data/ai_governance/agent_permissions.jsonl` | ai_gov_lead | 2026-06-03 | append-only |
| `data/ai_governance/agent_evals.jsonl` | ai_gov_lead | 2026-06-03 | weekly |
| `data/ai_governance/agent_incidents.jsonl` | ai_gov_lead | 2026-06-03 | append-only |
| `schemas/agent_*.schema.json` | ai_gov_lead + engineer | 2026-06-03 | — |
| `reports/ai_governance/*` | ai_gov_lead | 2026-06-03 | weekly |

### 2.3 Data Products (Agent 31) — owner: `data_lead`

| File | Owner | Last Review | Change Control |
|------|-------|-------------|----------------|
| `docs/data_products/DATA_PRODUCTS_OS_AR.md` | data_lead | 2026-06-03 | — |
| `docs/data_products/SECTOR_BENCHMARKS_AR.md` | data_lead | 2026-06-03 | refresh quarterly |
| `docs/data_products/MESSAGE_PERFORMANCE_LIBRARY_AR.md` | data_lead + marketing | 2026-06-03 | — |
| `docs/data_products/OBJECTION_INTELLIGENCE_AR.md` | data_lead + sales_lead | 2026-06-03 | — |
| `docs/data_products/OFFER_PERFORMANCE_MODEL_AR.md` | data_lead + marketing | 2026-06-03 | — |
| `docs/data_products/DELIVERY_PATTERN_LIBRARY_AR.md` | data_lead + csm | 2026-06-03 | — |
| `docs/data_products/RENEWAL_TRIGGER_LIBRARY_AR.md` | data_lead + csm | 2026-06-03 | — |
| `docs/data_products/PRICING_SENSITIVITY_LIBRARY_AR.md` | data_lead + sales_lead | 2026-06-03 | — |
| `data/data_products/*.jsonl` | data_lead | 2026-06-03 | PR with `data-change` tag |
| `schemas/{sector_benchmark,message_performance,objection_pattern,delivery_pattern,renewal_trigger,pricing_rule,offer_match,funnel_event,metric_event}.schema.json` | data_lead + engineer | 2026-06-03 | — |
| `reports/data_products/*` | data_lead | 2026-06-03 | — |

### 2.4 Offers (Agent 33) — owner: `marketing`

| File | Owner | Last Review | Change Control |
|------|-------|-------------|----------------|
| `docs/offers/OFFER_LANDING_PAGE_SYSTEM_AR.md` | marketing | 2026-06-03 | — |
| `docs/offers/REVENUE_LEAKAGE_DIAGNOSTIC_PAGE_AR.md` | marketing + sales_lead | 2026-06-03 | — |
| `docs/offers/FOLLOWUP_RECOVERY_WORKFLOW_PAGE_AR.md` | marketing + sales_lead | 2026-06-03 | — |
| `docs/offers/AI_REVENUE_OPS_STARTER_PAGE_AR.md` | marketing | 2026-06-03 | founder review (NEEDS_REVIEW) |
| `docs/offers/FULL_REVENUE_OS_PAGE_AR.md` | marketing + founder | 2026-06-03 | founder review (NEEDS_REVIEW) |
| `docs/offers/MONTHLY_OPTIMIZATION_PAGE_AR.md` | marketing + founder | 2026-06-03 | founder review (NEEDS_REVIEW) |
| `docs/offers/CUSTOM_COMPANY_OS_PAGE_AR.md` | marketing + sales_lead | 2026-06-03 | — |
| `docs/offers/OFFER_FAQ_LIBRARY_AR.md` | marketing + csm | 2026-06-03 | — |
| `docs/offers/OFFER_CTA_LIBRARY_AR.md` | marketing | 2026-06-03 | — |
| `schemas/product_offer.schema.json` | marketing + engineer | 2026-06-03 | — |
| `schemas/product_feature.schema.json` | marketing + engineer | 2026-06-03 | — |
| `reports/offers/*` | marketing | 2026-06-03 | — |

### 2.5 Integration Layer (Agent 35) — owner: `founder`

| File | Owner | Last Review | Change Control |
|------|-------|-------------|----------------|
| `docs/DEALIX_COMPANY_OS_INDEX_AR.md` | founder | 2026-06-03 | — |
| `docs/DEALIX_COMPANY_OS_MAP_AR.md` | founder | 2026-06-03 | — |
| `docs/FOUNDER_START_HERE_AR.md` | founder | 2026-06-03 | — |
| `docs/DAILY_OPERATING_GUIDE_AR.md` | founder | 2026-06-03 | — |
| `docs/WEEKLY_OPERATING_GUIDE_AR.md` | founder | 2026-06-03 | — |
| `docs/PRIORITY_ROADMAP_AR.md` | founder | 2026-06-03 | — |
| `docs/FILE_OWNERSHIP_MAP.md` | founder | 2026-06-03 | — |
| `docs/SYSTEM_BOUNDARIES.md` | founder | 2026-06-03 | — |
| `docs/ANTI_DUPLICATION_POLICY.md` | founder | 2026-06-03 | — |
| `reports/final/*` | founder | 2026-06-03 | — |

---

## 3) Legacy — Quick Reference

| Domain | Owner |
|--------|-------|
| `docs/commercial/` | sales_lead + founder |
| `docs/enterprise/` | sales_lead + csm |
| `docs/enterprise_rollout/` | csm + sales_lead |
| `docs/delivery/`, `docs/phase-e/` | csm |
| `docs/governance/`, `docs/responsible_ai/` | ai_gov_lead + founder |
| `docs/security/` | engineer + ai_gov_lead |
| `docs/data_governance/` | data_lead + engineer |
| `docs/finance/` | founder (CFO role) |
| `docs/legal/` | legal |
| `docs/partnerships/` | partnerships |
| `docs/product/` | engineer + founder |
| `docs/strategy/`, `docs/institutional/` | founder |
| `docs/ops/` (FOUNDER_*, RAILWAY_*, DEPLOY_*) | founder + engineer |
| `docs/ops/` (operational runbooks) | engineer |

---

## 4) Cross-Ownership Rules

- **Any file with `+` owner = 2 owners, both must approve PR.**
- **Any `enterprise_*` = sales_lead primary + relevant secondary.**
- **Any `data/*` = data_lead primary + engineer for schema changes.**
- **Any `ai_governance/*` = ai_gov_lead primary + founder for A0-A5 changes.**

---

## 5) Open Questions for Founder

1. هل تقرّ هذا الـ Roster، أم تريد إضافة `cto` كـ owner منفصل؟
2. متى تريد **last_review** تلقائياً (CI check)؟
3. هل تريد **renaming** للـ owners (مثلاً `ai_gov_lead` → `head_of_ai`)؟
