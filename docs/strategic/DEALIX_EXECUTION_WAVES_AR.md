# موجات التنفيذ Dealix — من Commercial Trust إلى Enterprise

هذا الملف يربط **GitHub Milestones** بمسارات الكود والوثائق المولَّدة تحت `docs/0x_*` (طبقات التنفيذ).

## الموجة 1 — Commercial Trust MVP (تُباع الآن)

**الهدف:** Revenue Intelligence Sprint يثبت القيمة والحوكمة والإثبات.

| عنصر | كود / وثائق |
|------|-------------|
| Source Passport | `data_os/source_passport.py`, `docs/04_data_os/SOURCE_PASSPORT.md` |
| Import + جودة | `data_os/import_preview.py`, `data_os/data_quality_score.py`, `docs/04_data_os/` |
| تطبيع | `data_os/normalization.py` |
| Governance runtime | `governance_os/runtime_decision.py`, `governance_os/claim_safety.py`, `docs/05_governance_os/` |
| Scoring | `revenue_os/scoring.py`, `revenue_os/account_model.py` |
| Draft pack | `revenue_os/draft_pack.py`, `docs/03_commercial_mvp/DRAFT_PACK.md` |
| Proof | `proof_os/proof_pack.py`, `proof_os/proof_score.py`, `docs/07_proof_os/` |
| Value / Capital | `value_os/value_ledger.py`, `capital_os/capital_ledger.py` |
| Safety tests | `tests/test_no_*`, `tests/test_proof_pack_required.py`, … |

**مؤشر نجاح:** أي استيراد يمر بجواز المصدر؛ أي مسودة تحت `DRAFT_ONLY`؛ Proof Pack قابل للاكتمال.

## الموجة 2 — Retainer Engine

**الهدف:** تكرار شهري موضَّح القيمة.

- `adoption_os/adoption_score.py`, `adoption_os/retainer_readiness.py` (`wave2_retainer_eligibility`)
- `client_os/monthly_value_report.py`, `docs/13_workflow_os/MONTHLY_VALUE_REPORT.md`
- لوحات العميل: `client_os/capability_dashboard.py`, `client_os/workspace.py`

## الموجة 3 — Enterprise Trust

- `trust_os/trust_pack.py`, `docs/14_trust_os/`
- `auditability_os/` — أحداث تدقيق وسجل فحص سياسات
- `evidence_control_plane_os/` — سلسلة أدلة (موجودة في المستودع)

## الموجة 4 — Agent-Safe

- `agent_os/` — بطاقة وكيل، سجل، حدود أدوات MVP
- `secure_agent_runtime_os/` — حالات تشغيل، ذاكرة مخاطر، kill switch

## الموجة 5 — Standards + Ecosystem

- `docs/23_standards/`, `docs/24_ecosystem/` — بعد تراكم مشاريع وProof متكرر (لا تُطلق Academy مبكرًا).

## المراحل 6–14 — من التكرار إلى القوة السوقية (وثائق `docs/26`–`docs/44`)

| مرحلة | موضوع | مجلد وثائق | كود أساسي |
|-------|--------|------------|-----------|
| 6 Repeatability | كتالوج خدمات + playbooks + change requests | `docs/26_service_catalog/`, `docs/27_delivery_playbooks/`, `docs/28_change_requests/` | `delivery_os/change_request.py`, `scope_classifier.py`, `retainer_backlog.py` |
| 7 Sales & GTM | تأهيل + عروض + اعتراضات + تسعير | `docs/29_sales_os/`, `docs/30_pricing/` | `sales_os/` |
| 8 Operating Finance | هامش + تكلفة AI | `docs/31_operating_finance/` | `operating_finance_os/offer_unit_economics.py`, `cost_guard.py`, … |
| 9 Enterprise Readiness | أمن + Data Room | `docs/32_enterprise_readiness/` | يُكمل `trust_os/` و`auditability_os/` |
| 10 Rollout | Land → Expand | `docs/33_enterprise_rollout/` | `enterprise_rollout_os/` (موجود) |
| 11 AI Estate | جرد واستخدامات | `docs/34_ai_estate/` | لاحقًا `ai_estate_os/` |
| 12 Agent IAM | هوية وكيل | `docs/35_agent_iam/` | لاحقًا `agent_identity_access_os/` + `agent_os/` |
| 13 Runtime Security | أربع حدود | `docs/36_agent_runtime_security/` | توسيع `secure_agent_runtime_os/` |
| 14 Saudi Layer | تميز محلي | `docs/37_saudi_layer/` | لاحقًا `saudi_layer/` |
| Standards/Academy/Partners | معيار + شركاء | `docs/38_standards/` … `docs/40_partners/` | يكمّل `docs/23`–`24` عند النضج |
| Benchmarks & Market Power | مرجعية سوق | `docs/41_benchmarks/`, `docs/42_market_power/` | لاحقًا محركات تحليل |
| Business Units & Ventures | قابضة | `docs/43_business_units/`, `docs/44_ventures/` | يرتبط بـ`docs/25_ventures/` |

**توليد الوثائق:** `py -3 scripts/generate_scale_phase_docs.py`

**الدستور وغرفة الثقة (رؤية القابضة):** `py -3 scripts/generate_holding_vision_docs.py` → `docs/00_constitution/`، `docs/15_auditability/`، `docs/enterprise_trust/`، `docs/16_evidence_control_plane/`.

الجملة الاستراتيجية: **ابدأ بموجة 1 كمنتج موثوق، ثم اربط الموجات التالية بأدلة تشغيل لا بهندسة افتراضية.**
