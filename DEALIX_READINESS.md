# Dealix Readiness Control Center

**لا تثق بالإحساس. ثق بنظام التحقق.**
**نظام التشغيل اليومي:** [`docs/company/DEALIX_OPERATING_KERNEL.md`](docs/company/DEALIX_OPERATING_KERNEL.md) — [`docs/company/DECISION_RULES.md`](docs/company/DECISION_RULES.md) — مراجعة أسبوعية [`docs/company/WEEKLY_OPERATING_REVIEW.md`](docs/company/WEEKLY_OPERATING_REVIEW.md) — [`docs/company/SERVICE_REGISTRY.md`](docs/company/SERVICE_REGISTRY.md).
سياق السوق: [McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/) — [Gartner — AI-ready data](https://www.gartner.com/en/newsroom/press-releases/2025-02-26-lack-of-ai-ready-data-puts-ai-projects-at-risk).

المرجع: [`docs/company/DEALIX_STAGE_GATES_AR.md`](docs/company/DEALIX_STAGE_GATES_AR.md).

التحقق الآلي:

```bash
python scripts/verify_dealix_ready.py
python scripts/verify_dealix_ready.py --skip-tests
```

**آخر تحقق آلي:** 2026-05-14 — Wave 19 recovery sprint — `DEALIX_READY_FOR_SALES=true`.

---

## Company Status

| Field | Value |
|-------|--------|
| **Current Stage** | Gate 8 Pass — جاهز للبيع للخدمات الستة الأولى |
| **Officially Sellable Services** | lead_intelligence_sprint, ai_quick_win_sprint, company_brain_sprint, ai_support_desk_sprint, ai_governance_program, client_ai_policy_pack |
| **Services in Beta** | (لا يوجد — كل الخدمات الرسمية ≥ 90) |
| **Services Not Ready** | (لا يوجد ضمن المعتمد) |

---

## Gate Scores (آلي: راجع `scripts/verify_dealix_ready.py`)

| Gate | الاسم | قرار | Score / مصدر |
|------|--------|------|---------------|
| 0 | Founder Clarity | **PASS** | verifier |
| 1 | Offer Readiness | **PASS** | 3/3 starter offers ≥ 85 (all 100) |
| 2 | Delivery Readiness | **PASS** | verifier |
| 3 | Product Readiness | **PASS** | verifier |
| 4 | Governance Readiness | **PASS** | verifier |
| 5 | Demo Readiness | **PASS** | verifier |
| 6 | Sales Readiness | **PASS** | verifier |
| 7 | Client Delivery Readiness | **PASS** | verifier |
| 8 | Retainer Readiness | **PASS** | verifier |
| 9 | Scale Readiness | — | not yet evaluated |
| 10 | World-Class Readiness | — | معيار طموح ([WORLD_CLASS_READINESS_AR.md](docs/company/WORLD_CLASS_READINESS_AR.md)) |

**Decision:** `SELL_READY_STACK`. PASS → انتقل ; FIX → أصلح ثم أعد التقييم ; BLOCKED → لا بيع ولا توسع حتى تُزال المعرقلات.

---

## Official Services (Score 100)

1. Lead Intelligence Sprint — `docs/services/lead_intelligence_sprint/`
2. AI Quick Win Sprint — `docs/services/ai_quick_win_sprint/`
3. Company Brain Sprint — `docs/services/company_brain_sprint/`
4. AI Support Desk Sprint — score 90
5. AI Governance Program — score 100
6. Client AI Policy Pack — score 100

## Do Not Sell Yet

- لا يوجد ضمن stack الـ6 المعتمدة.

## Critical Gaps (Tracked, Not Blocking Sales)

1. **Maturity-roadmap OS layers** (adoption_os, agent_os, auditability_os, capital_os.case_study, evidence_control_plane_os, market_power_os, operating_empire_os, sales_os.qualification, secure_agent_runtime_os, trust_os.trust_pack) — modules scaffolded with partial API surface. Aspirational tests in `tests/test_*` flag missing functions. Not on the sales path; tracked for follow-up sprint.
2. **GitHub MCP auth** — re-authentication required before merge of PR #236; ping founder when ready.

## Next Build Decisions

1. Fill the 10 maturity-roadmap modules to test parity (follow-up sprint, post-merge).
2. Wire `scripts/export_outreach_ready.py` to a deployed API endpoint and run a dry-export against the warm list.
3. Add Gate 9 (Scale Readiness) automated checks to `verify_dealix_ready.py`.

---

## Wave 19 Recovery Sprint — restoration log

Commit ranges restored from `fe334e5` baseline (regressions caused by the maturity-roadmap collapse in `4687755`):

| Module | Action | Lines restored |
|--------|--------|----------------|
| `auto_client_acquisition/value_os/value_ledger.py` | Full operational API (ValueEvent, add_event, list_events, summarize, clear_for_test, ValueDisciplineError) restored alongside canonical re-exports | ~200 |
| `auto_client_acquisition/value_os/__init__.py` | Export both surfaces | ~30 |
| `auto_client_acquisition/data_os/data_quality_score.py` | DQScore + compute_dq restored alongside lightweight helpers | ~170 |
| `auto_client_acquisition/data_os/import_preview.py` | ImportPreview + preview() restored alongside import_preview_csv | ~115 |
| `auto_client_acquisition/data_os/source_passport.py` | validate / ValidationResult / requires_approval + enum constants restored alongside sovereignty bridge | ~140 |
| `auto_client_acquisition/governance_os/runtime_decision.py` | decide() + DecisionResult restored alongside policy-check mappers | ~190 |
| `auto_client_acquisition/data_os/__init__.py` | Re-export new helpers | ~5 |

**Tests after recovery:** 87/87 PASS in governance + proof + readiness + value_os + layered_os scope.

---

## قاعدة البيع (تلخيص)

- **بع رسمياً** فقط ما عبر: Gate 0, 1, 2, 4, 5, 6 + Gate 3 كـMVP. راجع `DEALIX_READY_FOR_SALES` من السكربت.
- **Beta** إذا كان score العرض/التسليم بين **70 و 84** وبلا hard fail.
- **ممنوع** إذا كان أقل من 70 أو لا QA / لا scope / لا حوكمة / وعود مبيعات مضمونة / إرسال أو scraping غير محكوم.

## حزم الـDemo

[`demos/lead_intelligence_demo/`](demos/lead_intelligence_demo/) · [`demos/ai_quick_win_demo/`](demos/ai_quick_win_demo/) · [`demos/company_brain_demo/`](demos/company_brain_demo/)
