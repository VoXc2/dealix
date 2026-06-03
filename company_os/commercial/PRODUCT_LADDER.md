# Product Ladder

A climb from low-friction proof to recurring revenue. Every rung maps to a pain in
`ICP_MATRIX.md` and to the `offer` enum in `schemas/proposal.schema.json`. **All
prices are ranges and every quote requires founder approval** (see
`PRICING_GUARDRAILS.md`). No guaranteed-result language anywhere.

---

| # | Offer (`id`) | Price range (SAR) | Duration | Goal |
|---|--------------|-------------------|----------|------|
| 1 | Readiness Scan (`readiness_scan`) | Free / low-friction | minutes | Convert confused prospects |
| 2 | Revenue Leakage Diagnostic (`revenue_leakage_diagnostic`) | 1,500–5,000 | 3–5 days | Paid entry, find the leak |
| 3 | Follow-up Recovery Workflow (`follow_up_recovery_workflow`) | 8,000–18,000 | 7–14 days | First proof of value |
| 4 | AI Revenue Ops Starter (`ai_revenue_ops_starter`) | 18,000–35,000 | 14–30 days | Core implementation |
| 5 | Full Revenue OS (`full_revenue_os`) | 35,000–90,000 | 30–60 days | Broad implementation |
| 6 | Monthly Optimization Retainer (`monthly_optimization_retainer`) | 3,000–15,000 / mo | ongoing | Recurring revenue |
| 7 | Custom Company OS (`custom_company_os`) | 90,000+ | scoped | Enterprise / premium |

> The current go-to-market entry point is the **Revenue Intelligence Sprint** (5
> days, ~5,000 SAR) — a packaged Diagnostic. It is the proof-first wedge referenced
> in `revenue/` and the war-room reports.

---

## Each offer must define

promise · buyer · pain · deliverables · timeline · price range · scope · **out of
scope** · requirements · proof needed · success metric · risks · delivery handoff ·
renewal path.

---

## Upsell path

```
Readiness Scan → Revenue Leakage Diagnostic → Follow-up Recovery
   → AI Revenue Ops Starter → Full Revenue OS → Monthly Optimization
   → Custom Company OS → multi-department rollout
```

Each step up cites **delivered value** (evidence ≥ L3), suggests one next step,
avoids pressure, and requires approval. See `../customer_success/RENEWAL_PLAYBOOK.md`.

---

*Version 1.0 | 2026-06-03*
