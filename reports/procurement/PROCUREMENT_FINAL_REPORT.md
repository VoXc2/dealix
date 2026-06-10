# Agent #17 — Procurement Final Report

**Date:** 2026-06-03
**Agent:** Agent #17 — Vendor, Procurement, Cost Optimization

---

## 1. ملخص تنفيذي

لا يوجد procurement OS في الـ repo. Agent #17 بنى **catalog كامل
لـ 25 vendor** (مستخرج من `.env.example`)، schema، و 5 policies
(Vendor Management، API Cost، Tool Selection، Build vs Buy، Vendor
Risk، Subscription Review).

## 2. ما أُنشئ

| المسار | الملف |
| --- | --- |
| `docs/agent_definitions/agent_17_procurement.md` | تعريف |
| `reports/procurement/VENDOR_REVIEW.md` | Gap audit |
| `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md` | نظام إدارة الموردين |
| `data/procurement/vendors.jsonl` | catalog (25 vendors) |
| `schemas/vendor.schema.json` | schema |
| `docs/procurement/API_COST_CONTROL_AR.md` | التحكم في تكلفة API |
| `docs/procurement/TOOL_SELECTION_POLICY_AR.md` | سياسة اختيار الأداة |
| `docs/procurement/BUILD_VS_BUY_POLICY_AR.md` | Build vs Buy |
| `docs/procurement/VENDOR_RISK_POLICY_AR.md` | مخاطر الموردين |
| `docs/procurement/SUBSCRIPTION_REVIEW_AR.md` | مراجعة الاشتراكات |

## 3. الـ 25 Vendors (في `vendors.jsonl`)

### Critical (8)
- v_moyasar (payments)
- v_whatsapp_multi (multi-provider chain)
- v_anthropic (LLM primary)
- v_railway (hosting)
- v_aws_s3 (backups)
- v_1password (secrets)
- v_hubspot (CRM) — high but listed
- v_MiniMax (LLM daily)

### High (5)
- v_hubspot
- v_gmail_oauth
- v_whatsapp_multi (also critical)

### Medium (8)
- v_calendly, v_posthog, v_sentry, v_sendgrid, v_openai, v_groq, v_uptimerobot, v_hunter

### Low (7)
- v_google_cse, v_tavily, v_firecrawl, v_abstract, v_wappalyzer, v_google_maps, v_serpapi, v_apify

(إجمالي ≈ 25 vendor.)

## 4. Schema Fields (15 field)

`vendor_id`, `name`, `purpose`, `owner`, `monthly_cost_sar_estimate`,
`monthly_cost_sar_actual`, `usage_metric`, `data_risk`,
`data_risk_reason`, `secrets_required`, `replacement_option`,
`replacement_effort`, `cancellation_difficulty`,
`business_criticality`, `review_date`, `contract_end`,
`pdpl_compliant`, `soc2_certified`, `data_residency`.

## 5. Risk Tiers (R0–R4)

- R4: critical risk (concentration + critical business + critical data).
  حالياً: Moyasar, Railway, 1Password, AWS S3, WhatsApp Meta.
- R3: high risk.
- R2: medium risk.
- R1: low risk.
- R0: لا تأثير.

## 6. R4 Mitigations

- Daily monitoring (Sentry + PostHog + UptimeRobot).
- Manual fallback runbook.
- Backup vendor or replacement option.
- Quarterly drill.
- Secret rotation quarterly.
- Data export ability (30-day exit).

## 7. LLM Spend Budget (من `API_COST_CONTROL_AR.md`)

- Daily cap $10.
- Per-agent HERMES_COST_BUDGET_USD=$5.
- Token cap 10K output.
- Cache TTL 1h.
- Rate limits per API.

## 8. Tool Selection (7 أسئلة)

1. هل هناك أداة حالية تغطي؟
2. critical أم nice-to-have؟
3. data risk؟
4. ضمن budget؟
5. monthly cancellable؟
6. Saudi data residency؟
7. SaaS أم self-hosted؟

## 9. Build vs Buy Decisions (current)

### Buy
- PostHog, Sentry, SendGrid, Calendly, Railway, AWS S3, 1Password,
  Moyasar

### Build
- Revenue OS, Governance engine, Proof ledger, WhatsApp decision
  layer, Personal Operator, Saudi Lead Machine

### Hybrid
- WhatsApp integration, CRM sync, LLM routing

## 10. Monthly Subscription Review

- 4-step process (checklist).
- Auto-cancel rules (60-day unused, tier change, certification loss).
- 5 steps logged in `SUBSCRIPTION_REVIEW.md`.

## 11. Remaining Gaps

1. **`api_costs.jsonl`** populated (currently empty).
2. **`subscriptions.jsonl`** populated (currently empty).
3. **`subscription.schema.json`** created.
4. **`api_cost.schema.json`** created.
5. **Real cost values** extracted from invoices/faturas.
6. **CI test** for vendor schema validity.
7. **Cancellation procedures** documented per vendor.
8. **Auto-cancel script** (with founder approval gate).

## 12. Founder Next Actions

1. ✅ اعتماد `VENDOR_MANAGEMENT_OS_AR.md`.
2. ✅ اعتماد `vendors.jsonl` (25 vendor).
3. ✅ اعتماد `vendor.schema.json`.
4. ⏳ Populate `api_costs.jsonl` و `subscriptions.jsonl`.
5. ⏳ Extract real cost from invoices.
6. ⏳ CI test: `tests/test_vendor_schema_valid.py`.
7. ⏳ Cancellation procedures per R4 vendor.
8. ⏳ Build a procurement dashboard.

## 13. Cross-Agent

- **Agent #12 (Infra):** vendor hosting = Railway + AWS S3 backup.
- **Agent #13 (Legal):** vendor PDPL = legal review trigger.
- **Agent #15 (Services):** API cost per service = pricing basis.
- **Agent #16 (Data Room):** vendor list = due diligence section.

## 14. المراجع

- `docs/agent_definitions/agent_17_procurement.md`
- `reports/procurement/VENDOR_REVIEW.md`
- `docs/procurement/VENDOR_MANAGEMENT_OS_AR.md`
- `data/procurement/vendors.jsonl`
- `schemas/vendor.schema.json`
- `docs/procurement/API_COST_CONTROL_AR.md`
- `docs/procurement/TOOL_SELECTION_POLICY_AR.md`
- `docs/procurement/BUILD_VS_BUY_POLICY_AR.md`
- `docs/procurement/VENDOR_RISK_POLICY_AR.md`
- `docs/procurement/SUBSCRIPTION_REVIEW_AR.md`
- `docs/SUPPLIER_MASTER_LIST.md` (existing)
- `docs/COST_OPTIMIZATION.md` (existing)
- `docs/V7_COST_CONTROL_POLICY.md` (existing)
- `docs/SLO.md` (existing, Tier 3 cost)
- `docs/finance/FOUNDER_UNIT_ECONOMICS_MODEL_AR.md` (existing)
