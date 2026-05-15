# Dealix Commercial Wiring Map — خريطة الربط التجاري

> Version 1 — Wave 14J — Generated to match `auto_client_acquisition/service_catalog/registry.py` and `GET /api/v1/commercial-map`.

This document is the **single source of truth** showing how every commercial offer maps to a landing page, a backend endpoint, and a delivery surface. Every new engineer, partner, or founder-led handoff should start here.

هذه الوثيقة هي **المصدر الوحيد للحقيقة** التي تُظهر كيفية ربط كل عرض تجاري بصفحة هبوط، ونقطة نهاية خلفية، وسطح تسليم. يجب على كل مهندس أو شريك أو عملية تسليم يقودها المؤسس أن يبدأ من هنا.

---

## 1. The 7-offer canonical registry — السجل الرسمي للعروض السبعة

| `service_id` | Name (AR / EN) | Price (SAR) | Cadence | Customer Journey Stage |
|---|---|---|---|---|
| `free_mini_diagnostic` | التشخيص المجاني / Free Mini Diagnostic | 0 | one_time | discovery |
| `revenue_proof_sprint_499` | سبرنت إثبات الإيرادات / Revenue Proof Sprint | 499 | one_time | first_paid |
| `data_to_revenue_pack_1500` | حزمة من البيانات إلى الإيراد / Data-to-Revenue Pack | 1,500 | one_time | expansion |
| `growth_ops_monthly_2999` | عمليات النمو الشهرية / Growth Ops Monthly | 2,999 | per_month | monthly |
| `support_os_addon_1500` | إضافة دعم العمليات / Support OS Add-on | 1,500 | per_month | support_addon |
| `executive_command_center_7500` | غرفة قيادة الإدارة / Executive Command Center | 7,500 | per_month | executive |
| `agency_partner_os` | منصة شركاء الوكالات / Agency Partner OS | custom | — | channel |

The registry is authoritative — any disagreement with this table means **the code, not the table, is wrong**. Run `python -c "from auto_client_acquisition.service_catalog.registry import OFFERINGS; print([o.id for o in OFFERINGS])"` to verify.

السجل هو المرجع الرسمي — أي تعارض مع هذا الجدول يعني أن **الكود، وليس الجدول، هو الخطأ**.

---

## 2. Per-offer wiring — الربط لكل عرض

### 2.1 `free_mini_diagnostic` — التشخيص المجاني

- **Public landing:** `landing/diagnostic.html`
- **Intake endpoint:** `POST /api/v1/company-growth-beast/diagnostic` + `POST /api/v1/public/demo-request`
- **Checkout:** N/A (free / مجاني)
- **Delivery:** founder reviews via `GET /api/v1/founder/leads`
- **Proof / report:** bilingual brief emailed via `auto_client_acquisition/email/transactional.send_transactional(kind="diagnostic_intake_confirmation")`
- **Founder dashboard surface:** `landing/founder-leads.html` + `GET /api/v1/founder/dashboard`
- **Non-negotiables enforced:** `no_live_send`, `no_live_charge`, `no_cold_whatsapp`, `no_scraping`, `no_fake_proof`

### 2.2 `revenue_proof_sprint_499` — سبرنت إثبات الإيرادات

- **Public landing:** `landing/start.html` (with `landing/sprint-sample.html` for live preview)
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → `POST /api/v1/service-setup/proposal/{customer_id}`
- **Checkout:** `landing/checkout.html?tier=sprint` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `auto_client_acquisition/delivery_factory/delivery_sprint.run_sprint` + `POST /api/v1/sprint/run` (10 steps)
- **Proof / report:** `auto_client_acquisition/proof_os/proof_pack.assemble` → 14-section ProofPack
- **Founder dashboard surface:** `landing/founder-dashboard.html` + `GET /api/v1/founder/dashboard`
- **Non-negotiables enforced:** all 7 hard_gates from `registry.py`

### 2.3 `data_to_revenue_pack_1500` — حزمة من البيانات إلى الإيراد

- **Public landing:** `landing/data-pack.html` (NEW) + `landing/services.html` card
- **Intake endpoint:** CSV upload via `POST /api/v1/data-os/import-preview/upload` (live demo) → qualified via `POST /api/v1/service-setup/qualify`
- **Checkout:** `landing/checkout.html?tier=data_pack` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `auto_client_acquisition/data_os/` (SourcePassport + preview + compute_dq) plus the sprint orchestrator with a tighter scope
- **Proof / report:** Proof Pack + `POST /api/v1/data-os/import-preview` JSON output
- **Founder dashboard surface:** founder reviews CSV uploads and approves cleaned output
- **Non-negotiables enforced:** 6 hard_gates

### 2.4 `growth_ops_monthly_2999` — عمليات النمو الشهرية

- **Public landing:** `landing/pricing.html` (Growth card)
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → proposal
- **Checkout:** `landing/checkout.html?tier=growth` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `scripts/weekly_brief_runner.py --all-active` + `scripts/monthly_cadence_runner.py --all-active --schedule-renewals`
- **Proof / report:** `GET /api/v1/value/{handle}/report/monthly` + workspace
- **Founder dashboard surface:** `landing/customer-portal.html?handle={customer}` (Wave 14J wired)
- **Non-negotiables enforced:** 8 hard_gates

### 2.5 `support_os_addon_1500` — Support OS Add-on

- **Public landing:** `landing/services.html` (card 4)
- **Intake endpoint:** same qualification flow as Growth Ops
- **Checkout:** `landing/checkout.html?tier=support_addon`
- **Delivery:** `auto_client_acquisition/support_os/` (existing module)
- **Proof / report:** monthly value report
- **Non-negotiables enforced:** 5 hard_gates

### 2.6 `executive_command_center_7500` — غرفة قيادة الإدارة

- **Public landing:** `landing/executive-command-center.html`
- **Intake endpoint:** founder-led; `POST /api/v1/service-setup/requests`
- **Checkout:** founder-issued invoice (manual Moyasar link)
- **Delivery:** `auto_client_acquisition/executive_command_center/` (existing module)
- **Proof / report:** daily founder brief (WhatsApp) + monthly board pack
- **Non-negotiables enforced:** 8 hard_gates

### 2.7 `agency_partner_os` — Agency Partner OS

- **Public landing:** `landing/agency-partner.html`
- **Intake endpoint:** `POST /api/v1/public/partner-application`
- **Referral program:** `auto_client_acquisition/partnership_os/referral_store` (5,000 SAR per closed deal; persistence landed in Wave 14D.1)
- **Founder dashboard surface:** `landing/founder-leads.html` + referral dashboard
- **Non-negotiables enforced:** 8 hard_gates + the Partner Covenant (`docs/40_partners/PARTNER_COVENANT.md`)

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
