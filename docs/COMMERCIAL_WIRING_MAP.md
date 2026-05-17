# Dealix Commercial Wiring Map — خريطة الربط التجاري

> Version 1 — Wave 14J — Generated to match `auto_client_acquisition/service_catalog/registry.py` and `GET /api/v1/commercial-map`.

This document is the **single source of truth** showing how every commercial offer maps to a landing page, a backend endpoint, and a delivery surface. Every new engineer, partner, or founder-led handoff should start here.

هذه الوثيقة هي **المصدر الوحيد للحقيقة** التي تُظهر كيفية ربط كل عرض تجاري بصفحة هبوط، ونقطة نهاية خلفية، وسطح تسليم. يجب على كل مهندس أو شريك أو عملية تسليم يقودها المؤسس أن يبدأ من هنا.

---

## 1. The canonical registry — السجل الرسمي للعروض

The Revenue Autopilot sells one front-door offer — the 7-Day Governed Revenue & AI Ops Diagnostic, at three price tiers — with two evidence-led follow-ons. Doctrine: `docs/REVENUE_AUTOPILOT.md`.

| `service_id` | Name (AR / EN) | Price (SAR) | Cadence | Customer Journey Stage |
|---|---|---|---|---|
| `diagnostic_starter_4999` | تشخيص الإيراد والذكاء الاصطناعي المحكوم ٧ أيام — المبدئية / 7-Day Governed Revenue & AI Ops Diagnostic — Starter | 4,999 | one_time | diagnostic |
| `diagnostic_standard_9999` | …القياسية / …Standard | 9,999 | one_time | diagnostic |
| `diagnostic_executive_15000` | …التنفيذية / …Executive | 15,000 | one_time | diagnostic |
| `revenue_intelligence_sprint` | سبرنت ذكاء الإيراد / Revenue Intelligence Sprint | per scope | custom | sprint |
| `governed_ops_retainer` | اشتراك العمليات المحكومة / Governed Ops Retainer | per scope | custom | retainer |

The registry is authoritative — any disagreement with this table means **the code, not the table, is wrong**. Run `python -c "from auto_client_acquisition.service_catalog.registry import OFFERINGS; print([o.id for o in OFFERINGS])"` to verify.

السجل هو المرجع الرسمي — أي تعارض مع هذا الجدول يعني أن **الكود، وليس الجدول، هو الخطأ**.

---

## 2. Per-offer wiring — الربط لكل عرض

### 2.1–2.3 `diagnostic_starter_4999` / `diagnostic_standard_9999` / `diagnostic_executive_15000` — التشخيص المحكوم ٧ أيام

- **Public landing:** `landing/dealix-diagnostic.html`
- **Intake endpoint:** `POST /api/v1/revenue-autopilot/lead` (Revenue Autopilot, automation 1)
- **Checkout:** `landing/checkout.html?tier=diagnostic_starter|diagnostic_standard|diagnostic_executive` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `auto_client_acquisition/diagnostic_engine/` + `auto_client_acquisition/revenue_autopilot/` (automations 6–9) via `POST /api/v1/revenue-autopilot/engagements/{id}/automations/{automation_name}`
- **Proof / report:** `auto_client_acquisition/proof_os/proof_pack.assemble` → 14-section Proof Pack
- **Founder dashboard surface:** `landing/founder-dashboard.html` + approval queue
- **Non-negotiables enforced:** all 8 hard_gates from `registry.py`

### 2.4 `revenue_intelligence_sprint` — سبرنت ذكاء الإيراد

- **Public landing:** `landing/dealix-diagnostic.html#sprint`
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → `POST /api/v1/service-setup/proposal/{customer_id}`
- **Checkout:** founder-issued invoice (scoped from the diagnostic findings)
- **Delivery:** `auto_client_acquisition/revenue_autopilot/orchestrator` (automation 10 drafts the proposal)
- **Proof / report:** `auto_client_acquisition/proof_os/proof_pack.assemble`
- **Non-negotiables enforced:** all 8 hard_gates

### 2.5 `governed_ops_retainer` — اشتراك العمليات المحكومة

- **Public landing:** `landing/dealix-diagnostic.html#retainer`
- **Intake endpoint:** `POST /api/v1/service-setup/qualify`
- **Checkout:** founder-issued monthly invoice (price scoped per engagement)
- **Delivery:** `scripts/monthly_cadence_runner.py` + `auto_client_acquisition/revenue_autopilot/`
- **Proof / report:** `GET /api/v1/value/{handle}/report/monthly`
- **Founder dashboard surface:** `landing/customer-portal.html?handle={customer}`
- **Non-negotiables enforced:** all 8 hard_gates

---

## 3. The 11 non-negotiables — enforced in code

Refer to `docs/00_constitution/NON_NEGOTIABLES.md` for the canonical wording. Each rule is enforced by a passing test under `tests/test_no_*.py` or `tests/governance/`:

1. `no_live_send` — `tests/test_no_live_send.py`
2. `no_live_charge` — `tests/test_no_live_charge.py`
3. `no_cold_whatsapp` — `tests/test_no_cold_whatsapp.py`
4. `no_scraping` — `tests/test_no_scraping.py`
5. `no_fake_proof` — `tests/test_no_fake_proof.py`
6. `no_unconsented_data` — `tests/test_no_unconsented_data.py`
7. `no_unverified_outcomes` — `tests/test_no_unverified_outcomes.py`
8. `no_hidden_pricing` — `tests/test_no_hidden_pricing.py`
9. `no_silent_failures` — `tests/test_no_silent_failures.py`
10. `no_unbounded_agents` — `tests/governance/test_agent_boundaries.py`
11. `no_unaudited_changes` — `tests/governance/test_audit_chain.py`

If CI ever fails on one of these guards, **do not merge**. Investigate, fix the root cause, re-run CI.

إذا فشل أي من هذه الاختبارات في CI، **لا تدمج**. حقّق في السبب الجذري، أصلحه، ثم أعد التشغيل.

---

## 4. Cross-cutting infrastructure — البنية التحتية المشتركة

The following modules are reused across multiple offers:

- `auto_client_acquisition/lead_inbox.py` — JSONL lead persistence
- `auto_client_acquisition/email/transactional.py` — 9 whitelisted email kinds
- `auto_client_acquisition/sales_os/qualification.py` — 8-question scorer
- `auto_client_acquisition/sales_os/proposal_renderer.py` — bilingual proposal renderer
- `auto_client_acquisition/payment_ops/renewal_scheduler.py` — JSONL retainer scheduler
- `auto_client_acquisition/proof_os/proof_pack.py` — 14-section assembler
- `auto_client_acquisition/trust_os/trust_pack.py` — 11-section enterprise pack
- `auto_client_acquisition/auditability_os/` — audit event store + evidence chain
- `auto_client_acquisition/evidence_control_plane_os/` — graph + gaps + compliance index
- `auto_client_acquisition/agent_os/` + `secure_agent_runtime_os/` — agent registry + 4 boundaries + kill switch
- `auto_client_acquisition/benchmark_os/` — k-anonymity report generator
- `auto_client_acquisition/proof_to_market/pdf_renderer.py` — weasyprint/pandoc PDF
- `auto_client_acquisition/partnership_os/referral_store.py` — referral program

Each of these modules has its own bilingual README under `auto_client_acquisition/<module>/README.md`. Do **not** duplicate logic across offers — extend the shared module instead.

لا تكرّر المنطق عبر العروض — وسّع الوحدة المشتركة بدلًا من ذلك.

---

## 5. The commercial-map endpoint — نقطة نهاية خريطة الربط

```
GET /api/v1/commercial-map           → JSON list of all offers + URLs + endpoints
GET /api/v1/commercial-map/markdown  → this document (always in sync with the registry)
```

The markdown variant is rendered directly from `service_catalog/registry.py`. If you change the registry, this document changes automatically — there is no second source of truth to drift.

النسخة Markdown تُولَّد مباشرة من `service_catalog/registry.py`. عند تغيير السجل، تتغير هذه الوثيقة تلقائيًا.

---

## 6. Verification — التحقق

Run all three to be sure the wiring is consistent:

1. Pull the live JSON:
   ```bash
   curl https://<prod>/api/v1/commercial-map | jq .
   ```
2. Compare with the registry:
   ```bash
   python -c "from auto_client_acquisition.service_catalog.registry import OFFERINGS; print([o.id for o in OFFERINGS])"
   ```
3. Run the contract test:
   ```bash
   pytest tests/test_commercial_map.py
   ```

If any of the three disagree, the deploy is broken. Roll back per `docs/RAILWAY_DEPLOY_CHECKLIST.md` section 6.

إذا تعارض أيٌّ من الثلاثة، فإن النشر معطل. تراجع إلى الإصدار السابق وفقًا للقسم 6 من قائمة التحقق.

---

## Footer

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
