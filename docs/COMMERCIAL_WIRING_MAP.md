# Dealix Commercial Wiring Map — خريطة الربط التجاري

> Version 2 — 2026-Q2 reframe — Generated to match `auto_client_acquisition/service_catalog/registry.py` and `GET /api/v1/commercial-map`.

This document is the **single source of truth** showing how every commercial offer maps to a landing page, a backend endpoint, and a delivery surface. Every new engineer, partner, or founder-led handoff should start here.

هذه الوثيقة هي **المصدر الوحيد للحقيقة** التي تُظهر كيفية ربط كل عرض تجاري بصفحة هبوط، ونقطة نهاية خلفية، وسطح تسليم. يجب على كل مهندس أو شريك أو عملية تسليم يقودها المؤسس أن يبدأ من هنا.

---

## 1. The 3-offer canonical registry (2026-Q2) — السجل الرسمي للعروض الثلاثة

| `service_id` | Name (AR / EN) | Price (SAR) | Cadence | Customer Journey Stage |
|---|---|---|---|---|
| `strategic_diagnostic` | التشخيص الاستراتيجي / Strategic Diagnostic | 0 | one_time | discovery |
| `governed_ops_retainer_4999` | ريتينر العمليات المحوكمة / Governed Ops Retainer | 4,999 | per_month | monthly |
| `revenue_intelligence_sprint_25k` | سبرنت ذكاء الإيرادات الرئيسي / Revenue Intelligence Sprint | 25,000 | one_time | flagship |

The 2025 seven-offer ladder (499 Sprint, 1,500 Data Pack, 2,999 Growth Ops, 1,500 Support Add-on, 7,500 Executive Command Center, Agency Partner OS) is **archived** from the customer-facing ladder. Legacy IDs still resolve via `_LEGACY_ID_ALIASES` in `service_catalog/registry.py` to their closest 2026 successor — see `docs/sales-kit/PRICING_REFRAME_2026Q2.md` for the rationale.

The registry is authoritative — any disagreement with this table means **the code, not the table, is wrong**. Run `python -c "from auto_client_acquisition.service_catalog.registry import OFFERINGS; print([o.id for o in OFFERINGS])"` to verify.

السجل هو المرجع الرسمي — أي تعارض مع هذا الجدول يعني أن **الكود، وليس الجدول، هو الخطأ**.

---

## 2. Per-offer wiring — الربط لكل عرض

### 2.1 `strategic_diagnostic` — التشخيص الاستراتيجي

- **Public landing:** `landing/diagnostic.html`
- **Intake endpoint:** `POST /api/v1/company-growth-beast/diagnostic` + `POST /api/v1/public/demo-request`
- **Checkout:** N/A (free / مجاني)
- **Delivery:** founder reviews via `GET /api/v1/founder/leads` (target: < 1 working day)
- **Proof / report:** bilingual brief emailed via `auto_client_acquisition/email/transactional.send_transactional(kind="diagnostic_intake_confirmation")`
- **Founder dashboard surface:** `landing/founder-leads.html` + `GET /api/v1/founder/dashboard`
- **Beachhead anchor:** Saudi B2B services (50–500 employees) PDPL + NDMO posture audit
- **Next offer:** `governed_ops_retainer_4999` (the diagnostic to retainer conversion is the primary funnel)
- **Non-negotiables enforced:** `no_live_send`, `no_live_charge`, `no_cold_whatsapp`, `no_scraping`, `no_fake_proof`

### 2.2 `governed_ops_retainer_4999` — ريتينر العمليات المحوكمة

- **Public landing:** `landing/pricing.html#retainer` (highlighted card on index.html `#pricing`)
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → `POST /api/v1/service-setup/proposal/{customer_id}`
- **Checkout:** `landing/checkout.html?tier=retainer` → `POST /api/v1/payment-ops/invoice-intent` (3-month minimum commitment)
- **Delivery:** `scripts/weekly_brief_runner.py --all-active` + `scripts/monthly_cadence_runner.py --all-active --schedule-renewals`
- **Proof / report:** `GET /api/v1/value/{handle}/report/monthly` + Adoption Score endpoint + workspace
- **Renewal:** `auto_client_acquisition/payment_ops/renewal_scheduler` (auto-charge intent emitted after 3 confirmed cycles)
- **Founder dashboard surface:** `landing/customer-portal.html?handle={customer}`
- **Next offer:** `revenue_intelligence_sprint_25k` (retainer customers are the natural pool for the flagship)
- **Non-negotiables enforced:** 8 hard_gates (no_live_send, no_live_charge, no_cold_whatsapp, no_linkedin_auto, no_scraping, no_fake_proof, no_fake_revenue, no_blast)

### 2.3 `revenue_intelligence_sprint_25k` — سبرنت ذكاء الإيرادات الرئيسي

- **Public landing:** `landing/start.html` (with `landing/sprint-sample.html` for live preview)
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → `POST /api/v1/service-setup/proposal/{customer_id}`
- **Checkout:** `landing/checkout.html?tier=sprint` → `POST /api/v1/payment-ops/invoice-intent` (50% on acceptance, 50% on Proof Pack)
- **Delivery:** `auto_client_acquisition/delivery_factory/delivery_sprint.run_sprint` + `POST /api/v1/sprint/run` (orchestrated 30-day plan)
- **Sample preview:** `GET /api/v1/sprint/sample`
- **Proof / report:** `auto_client_acquisition/proof_os/proof_pack.assemble` → 14-section ProofPack + `GET /api/v1/proof-to-market/case-safe/{engagement_id}` + Trust Pack PDF (`GET /api/v1/value/trust-pack/{handle}/pdf`)
- **Capital Asset:** every Sprint MUST register at least one asset via `capital_os.add_asset`
- **Founder dashboard surface:** `landing/founder-dashboard.html` + `GET /api/v1/founder/dashboard`
- **Next offer:** `governed_ops_retainer_4999` (every Sprint is sold with a Retainer renewal option)
- **Non-negotiables enforced:** all 8 hard_gates including `no_blast` and `no_fake_revenue`

### 2.4 Partnership channel (out-of-ladder)

Agency / referral partnerships are no longer a customer-facing offer.
They are served exclusively through `auto_client_acquisition/partnership_os/referral_store` under the Partner Covenant (`docs/40_partners/PARTNER_COVENANT.md`). The 5,000 SAR / closed deal credit policy remains; partners do not appear on the public ladder.

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
GET /api/v1/commercial-map           → JSON list of 7 offers + URLs + endpoints
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
