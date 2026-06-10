# Agent #17 — Procurement Gap Audit

**Date:** 2026-06-03
**Auditor:** Agent #17 (Vendor, Procurement, Cost Optimization)

---

## 1. Executive Summary

There is **no procurement operating system** in the repo. Vendor
information is scattered across `.env.example`, AGENTS.md, and various
docs (`SUPPLIER_MASTER_LIST.md`, integrations/, etc.). Agent #17 builds
the **centralized vendor + cost + subscription tracking** that prevents
secret sprawl, duplicate tools, and unused paid tools.

## 2. Existing Inventory

| Item | Status | Note |
| --- | --- | --- |
| `docs/SUPPLIER_MASTER_LIST.md` | ✅ exists | Reference list |
| `docs/COST_OPTIMIZATION.md` | ✅ exists | Cost rules |
| `docs/V7_COST_CONTROL_POLICY.md` | ✅ exists | V7 policy |
| `.env.example` (175 lines) | ✅ | All API keys documented |
| `docs/SLO.md` (Tier 3 cost) | ✅ | LLM spend targets |
| `docs/finance/FOUNDER_UNIT_ECONOMICS_MODEL_AR.md` | ✅ | Unit economics |
| `docs/finance/` | ✅ | Various |
| `auto_client_acquisition/finance_os/` | ✅ | Code |

## 3. Missing

| File | Priority |
| --- | --- |
| `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md` | **Critical** |
| `docs/procurement/API_COST_CONTROL_AR.md` | High |
| `docs/procurement/TOOL_SELECTION_POLICY_AR.md` | High |
| `docs/procurement/BUILD_VS_BUY_POLICY_AR.md` | High |
| `docs/procurement/VENDOR_RISK_POLICY_AR.md` | High |
| `docs/procurement/SUBSCRIPTION_REVIEW_AR.md` | Medium |
| `schemas/vendor.schema.json` | High |
| `schemas/api_cost.schema.json` | High |
| `schemas/subscription.schema.json` | High |
| `data/procurement/vendors.jsonl` | Critical (catalog) |
| `data/procurement/api_costs.jsonl` | High |
| `data/procurement/subscriptions.jsonl` | High |
| `reports/procurement/VENDOR_REVIEW.md` | Medium |
| `reports/procurement/API_COST_REVIEW.md` | Medium |
| `reports/procurement/SUBSCRIPTION_REVIEW.md` | Medium |
| `reports/procurement/PROCUREMENT_FINAL_REPORT.md` | Final |

## 4. Vendor Inventory (Extracted from `.env.example`)

| Vendor | Purpose | Monthly Cost (est) | Criticality | Owner |
| --- | --- | --- | --- | --- |
| Moyasar | Payments | TBD (transactional) | Critical | Founder |
| HubSpot | CRM | TBD (free → starter) | High | Founder |
| WhatsApp (Meta / Green API / Ultramsg / Fonnte) | WhatsApp Business | TBD | High | Founder |
| Calendly | Scheduling | TBD | Medium | Founder |
| PostHog | Analytics | TBD | Medium | Founder |
| Sentry | Error monitoring | TBD | Medium | Founder |
| SendGrid | Email | TBD | Medium | Founder |
| Anthropic (Claude) | LLM primary | TBD | Critical | Founder |
| MiniMax | LLM bilingual daily | TBD | High | Founder |
| Groq | LLM fallback | TBD | Medium | Founder |
| OpenAI | LLM fallback | TBD | Medium | Founder |
| Hermes (Anthropic-native) | Multi-agent | TBD | High | Founder |
| Google CSE | Search | TBD | Low | Founder |
| Tavily | Search fallback | TBD | Low | Founder |
| Google Maps | Local discovery | TBD | Low | Founder |
| SerpAPI | Local discovery | TBD | Low | Founder |
| Apify | Local discovery | TBD | Low | Founder |
| Firecrawl | Crawler | TBD | Low | Founder |
| Hunter.io | Email intelligence | TBD | Low | Founder |
| Abstract API | Email intelligence | TBD | Low | Founder |
| Wappalyzer | Tech detection | TBD | Low | Founder |
| Gmail OAuth | Daily email | $0 (OAuth) | High | Founder |
| Railway | Hosting | TBD | Critical | Founder |
| AWS S3 (me-south-1) | Backups | TBD | Critical | Founder |
| 1Password | Secrets vault | TBD | Critical | Founder |
| UptimeRobot | Health monitoring | TBD (free → pro) | Medium | Founder |

> **Note:** كل "TBD" يحتاج فعلي استخراج من الفواتير. هذا هو عمل
> `data/procurement/vendors.jsonl` و `subscriptions.jsonl`.

## 5. Risks

1. **No single source-of-truth** for vendor cost.
2. **No rotation policy** for vendor credentials.
3. **No replacement plan** for single-vendor dependencies.
4. **No cancellation difficulty** tracked (e.g., Sentry annual contract).
5. **No data risk** classification per vendor.

## 6. Recommendations

1. **Phase 1 priority:** `VENDOR_MANAGEMENT_OS_AR.md` +
   `data/procurement/vendors.jsonl` + `schemas/vendor.schema.json`.
2. **Phase 2 priority:** `API_COST_CONTROL_AR.md` +
   `data/procurement/api_costs.jsonl`.
3. **Phase 3 priority:** `TOOL_SELECTION_POLICY_AR.md` +
   `BUILD_VS_BUY_POLICY_AR.md` + `VENDOR_RISK_POLICY_AR.md`.
4. **Phase 4 priority:** `SUBSCRIPTION_REVIEW_AR.md` +
   `data/procurement/subscriptions.jsonl` + reports + final.
