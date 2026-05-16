# Dealix Commercial Wiring Map — خريطة الربط التجاري

> Version 1 — Wave 14J — Generated to match `auto_client_acquisition/service_catalog/registry.py` and `GET /api/v1/commercial-map`.

This document is the **single source of truth** showing how every commercial offer maps to a landing page, a backend endpoint, and a delivery surface. Every new engineer, partner, or founder-led handoff should start here.

هذه الوثيقة هي **المصدر الوحيد للحقيقة** التي تُظهر كيفية ربط كل عرض تجاري بصفحة هبوط، ونقطة نهاية خلفية، وسطح تسليم. يجب على كل مهندس أو شريك أو عملية تسليم يقودها المؤسس أن يبدأ من هنا.

---

## 1. The 5-rung canonical ladder — سُلَّم العروض الرسمي بدرجاته الخمس

The canonical reference for what Dealix sells is
[`docs/COMPANY_SERVICE_LADDER.md`](COMPANY_SERVICE_LADDER.md). This wiring map
must align to it. There are **5 active rungs**, not 7 offers.

المرجع الرسمي لما تبيعه Dealix هو
[`docs/COMPANY_SERVICE_LADDER.md`](COMPANY_SERVICE_LADDER.md). يجب أن تتوافق هذه
الخريطة معه. توجد **5 درجات فعّالة** لا 7 عروض.

| Rung | `service_id` | Name (AR / EN) | Price (SAR) | Cadence | Journey Stage |
|---|---|---|---|---|---|
| 0 | `free_ai_ops_diagnostic` | تشخيص العمليات المجاني / Free AI Ops Diagnostic | 0 | one_time | discovery |
| 1 | `revenue_intelligence_sprint_499` | سبرنت ذكاء الإيرادات / 7-Day Revenue Intelligence Sprint | 499 | one_time | first_paid |
| 2 | `data_to_revenue_pack_1500` | حزمة من البيانات إلى الإيراد / Data-to-Revenue Pack | 1,500 | one_time | expansion |
| 3 | `managed_revenue_ops` | إدارة عمليات الإيرادات / Managed Revenue Ops | 2,999–4,999 | per_month | monthly |
| 4 | `custom_ai_service_setup` | إعداد خدمة ذكاء اصطناعي مخصصة / Custom AI Service Setup | 5,000–25,000 | scoped | custom |

### Locked / future — not active offers — مغلقة / مستقبلية — ليست عروضاً فعّالة

The following appeared in earlier registries. They are **not active offers**
and must not be sold or quoted. They may become components of Rung 3 or Rung 4
in the future, but only after the rung's unlock trigger is met.

- `support_os_addon` — a possible Rung 3 component, not a standalone offer.
- `executive_command_center` — a possible Rung 3/4 surface, not a standalone offer.
- `agency_partner_os` — partner/channel motion. Locked until 3 pilots delivered + signed permission; not a customer-facing rung.

العناصر التالية ظهرت في سجلات سابقة. **ليست عروضاً فعّالة** ولا تُباع ولا تُسعَّر.
قد تصبح مكوّنات للدرجة 3 أو 4 مستقبلاً بعد استيفاء شرط الفتح فقط.

If the code registry (`service_catalog/registry.py`) still lists 7 offers, the
**registry is stale** and must be reconciled to this 5-rung ladder. The
service ladder doc — not the code — is the source of truth for the offer set.

إذا كان سجل الكود لا يزال يُدرج 7 عروض، فإن **السجل قديم** ويجب توفيقه مع هذا
السُّلَّم بدرجاته الخمس.

---

## 2. Per-offer wiring — الربط لكل عرض

### 2.1 Rung 0 — `free_ai_ops_diagnostic` — تشخيص العمليات المجاني

- **Public landing:** `landing/diagnostic.html`
- **Intake endpoint:** `POST /api/v1/company-growth-beast/diagnostic` + `POST /api/v1/public/demo-request`
- **Checkout:** N/A (free / مجاني)
- **Delivery:** founder reviews via `GET /api/v1/founder/leads`
- **Proof / report:** bilingual brief emailed via `auto_client_acquisition/email/transactional.send_transactional(kind="diagnostic_intake_confirmation")`
- **Founder dashboard surface:** `landing/founder-leads.html` + `GET /api/v1/founder/dashboard`
- **Non-negotiables enforced:** `no_live_send`, `no_live_charge`, `no_cold_whatsapp`, `no_scraping`, `no_fake_proof`

### 2.2 Rung 1 — `revenue_intelligence_sprint_499` — سبرنت ذكاء الإيرادات

- **Public landing:** `landing/start.html` (with `landing/sprint-sample.html` for live preview)
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → `POST /api/v1/service-setup/proposal/{customer_id}`
- **Checkout:** `landing/checkout.html?tier=sprint` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `auto_client_acquisition/delivery_factory/delivery_sprint.run_sprint` + `POST /api/v1/sprint/run` (10 steps)
- **Proof / report:** `auto_client_acquisition/proof_os/proof_pack.assemble` → 14-section ProofPack
- **Founder dashboard surface:** `landing/founder-dashboard.html` + `GET /api/v1/founder/dashboard`
- **Non-negotiables enforced:** all 7 hard_gates from `registry.py`

### 2.3 Rung 2 — `data_to_revenue_pack_1500` — حزمة من البيانات إلى الإيراد

- **Public landing:** `landing/data-pack.html` (NEW) + `landing/services.html` card
- **Intake endpoint:** CSV upload via `POST /api/v1/data-os/import-preview/upload` (live demo) → qualified via `POST /api/v1/service-setup/qualify`
- **Checkout:** `landing/checkout.html?tier=data_pack` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `auto_client_acquisition/data_os/` (SourcePassport + preview + compute_dq) plus the sprint orchestrator with a tighter scope
- **Proof / report:** Proof Pack + `POST /api/v1/data-os/import-preview` JSON output
- **Founder dashboard surface:** founder reviews CSV uploads and approves cleaned output
- **Non-negotiables enforced:** 6 hard_gates

### 2.4 Rung 3 — `managed_revenue_ops` — إدارة عمليات الإيرادات

- **Public landing:** `landing/pricing.html` (Managed Revenue Ops card)
- **Price:** 2,999–4,999 SAR / month, confirmed per engagement.
- **Intake endpoint:** `POST /api/v1/service-setup/qualify` → proposal
- **Checkout:** `landing/checkout.html?tier=managed_revenue_ops` → `POST /api/v1/payment-ops/invoice-intent`
- **Delivery:** `scripts/weekly_brief_runner.py --all-active` + `scripts/monthly_cadence_runner.py --all-active --schedule-renewals`
- **Proof / report:** `GET /api/v1/value/{handle}/report/monthly` + workspace
- **Founder dashboard surface:** `landing/customer-portal.html?handle={customer}`
- **Unlock rule:** requires a Rung 1 pilot delivered for the same customer.
- **Non-negotiables enforced:** 8 hard_gates

### 2.5 Rung 4 — `custom_ai_service_setup` — إعداد خدمة ذكاء اصطناعي مخصصة

- **Public landing:** founder-led; no self-serve page.
- **Price:** 5,000–25,000 SAR, scoped per engagement.
- **Intake endpoint:** founder-led; `POST /api/v1/service-setup/requests`
- **Checkout:** founder-issued invoice (manual Moyasar link).
- **Delivery:** scoped build on top of an existing retainer relationship.
- **Unlock rule:** 3 pilots delivered + a signed publish permission from the customer.
- **Non-negotiables enforced:** 8 hard_gates; no Custom Enterprise tier without 6+ months retainer history.

### 2.6 Locked / future surfaces — أسطح مغلقة / مستقبلية

The surfaces below exist in the repo but are **not active offers**. They must
not be quoted or sold as standalone products. They may later be folded into
Rung 3 or Rung 4 once that rung's unlock trigger is met.

- `support_os_addon` — `auto_client_acquisition/support_os/` module. Possible Rung 3 component. Locked.
- `executive_command_center` — `auto_client_acquisition/executive_command_center/` module + `landing/executive-command-center.html`. Possible Rung 3/4 surface. Locked.
- `agency_partner_os` — `landing/agency-partner.html` + `auto_client_acquisition/partnership_os/`. Partner/channel motion, not a customer-facing rung. Locked until 3 pilots delivered + signed permission, per the Partner Covenant (`docs/40_partners/PARTNER_COVENANT.md`).

الأسطح أعلاه موجودة في الريبو لكنها **ليست عروضاً فعّالة**. لا تُسعَّر ولا تُباع
كمنتجات مستقلة.

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
GET /api/v1/commercial-map           → JSON list of the 5 active rungs + URLs + endpoints
GET /api/v1/commercial-map/markdown  → this document
```

This document and `docs/COMPANY_SERVICE_LADDER.md` define the 5-rung offer set.
If `service_catalog/registry.py` still emits 7 offers, the registry is stale
and must be reconciled — the service ladder doc is the source of truth.

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

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
