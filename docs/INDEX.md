# Dealix Docs · فهرس التوثيق

> 428+ مجلد/ملف في `docs/`. هذا الفهرس يجمعهم في 12 موضوع. لو ضعت → ابدأ من القسم المناسب لسؤالك.
>
> **مبدأ:** كل قسم له ملف "بداية واحد" → اقرأه أولاً، ثم تعمّق.

---

## 🚀 ابدأ من هنا (Start here)

| السؤال | الملف |
|--------|------|
| أول مرة أشغّل الريبو؟ | `docs/playbooks/QUICK_START.md` + `make first-setup` |
| ماذا أفعل اليوم/الأسبوع؟ | `docs/playbooks/FOUNDER_NEXT_STEPS.md` |
| ما هي doctrine الـ 11؟ | `/AGENTS.md` (sections "non-negotiables") |
| كيف أنشر للإنتاج؟ | `docs/contributing/DEPLOYMENT.md` + `docs/DEPLOY_CHECKLIST.md` |
| ما الـ stubs / NotImplementedError؟ | `docs/reference/KNOWN_LIMITATIONS.md` |

---

## 1) Foundation / الدستور

ابدأ بـ `docs/00_constitution/` و `docs/00_foundation/`. تحدد:
- Mission, vision, ICP
- 11 non-negotiables (doctrine)
- Constitutional articles (Articles 4, 8, 11)

ملفات مرتبطة: `DEALIX_OPERATING_CONSTITUTION.md`, `DEALIX_CONSTITUTION_TRUTH_AUDIT.md`.

## 2) Category / Positioning

`docs/01_category/`, `docs/01_category_creation/`, `docs/02_saudi_positioning/`, `docs/03_saudi_positioning/`.
ملفات: `COMPETITIVE_POSITIONING.md`, `BRAND_PRESS_KIT.md`.

## 3) Commercial / Product

`docs/03_commercial_mvp/`, `docs/04_product_strategy/`, `docs/26_service_catalog/`, `docs/30_pricing/`.
ملفات: `BUSINESS_MODEL.md`, `COMPANY_SERVICE_LADDER.md`, `DEALIX_PRODUCT_SIMPLIFICATION_MAP.md`.

## 4) Data OS

`docs/04_data_os/`, `docs/06_data_os/`. ملف: `DATA_MAP.md`.

## 5) Client / Customer OS

`docs/05_client_os/`, `docs/11_client_os/`. ملفات: `CUSTOMER_JOURNEYS.md`, `CUSTOMER_SUCCESS_PLAYBOOK.md`, `CUSTOMER_SUCCESS_SOP.md`.

## 6) Governance & Compliance

`docs/05_governance_os/`, `docs/07_governance/`, `docs/25_compliance_trust/`. ملفات: `DATA_RETENTION_POLICY.md`, `CROSS_BORDER_TRANSFER_ADDENDUM.md`.

## 7) LLM Gateway & Agents

`docs/06_llm_gateway/`, `docs/09_llm_gateway/`, `docs/10_agents/`, `docs/16_agents/`. ملفات: `AI_MODEL_ROUTING_STRATEGY.md`, `AI_OBSERVABILITY_AND_EVALS.md`, `AI_STACK_DECISIONS.md`.

## 8) Proof / Value / Trust

`docs/07_proof_os/`, `docs/08_value_os/`, `docs/14_proof/`, `docs/14_trust_os/`, `docs/15_value/`. ملف بداية: `BUSINESS_READINESS_EVIDENCE_TABLE.md`.

## 9) Capital & Finance

`docs/09_capital_os/`, `docs/16_capital/`, `docs/21_operating_finance/`, `docs/28_operating_finance/`, `docs/31_operating_finance/`. ملفات: `UNIT_ECONOMICS_AND_MARGIN.md`, `COST_OPTIMIZATION.md`, `BILLING_MOYASAR_RUNBOOK.md`.

## 10) Sales & Operating Rhythm

`docs/20_sales_os/`, `docs/29_sales_os/`, `docs/21_operating_rhythm/`. ملفات: `SALES_OPS_SOP.md`, `DAILY_LEAD_PREP_SETUP_GUIDE.md`, `DAY_1_LAUNCH_KIT.md`, `COMMERCIAL_LAUNCH_MASTER_PLAN.md`.

## 11) Architecture / Operations / Runbooks

`docs/36_architecture/`, `docs/ops/`. ملفات: `ARCHITECTURE_LAYER_MAP.md`, `BEAST_LEVEL_ARCHITECTURE.md`, `BACKEND_RELIABILITY_HARDENING_PLAN.md`, `BILLING_RUNBOOK.md`, جميع `docs/ops/*.md`.

## 12) Compliance Saudi / PDPL / Risk

`docs/24_risk_resilience/`, ملفات: `CROSS_BORDER_TRANSFER_ADDENDUM.md`, `DATA_RETENTION_POLICY.md`. Saudi-specific: `docs/37_saudi_layer/`.

---

## 📋 Top-20 ملفات يقرأها الفاوندر مرة واحدة

(مرتبة حسب الأولوية)

1. `/AGENTS.md` — doctrine + module layout
2. `docs/playbooks/FOUNDER_NEXT_STEPS.md` — ماذا تفعل الآن
3. `docs/reference/KNOWN_LIMITATIONS.md` — stubs catalog
4. `docs/operations/DEALIX_COMPANY_OPERATIONAL_STATE.md` — current state
5. `docs/COMMERCIAL_LAUNCH_MASTER_PLAN.md`
6. `docs/BUSINESS_MODEL.md`
7. `docs/COMPANY_SERVICE_LADDER.md` — 5-rung offer ladder
8. `docs/UNIT_ECONOMICS_AND_MARGIN.md`
9. `docs/SALES_OPS_SOP.md`
10. `docs/CUSTOMER_SUCCESS_SOP.md`
11. `docs/BILLING_MOYASAR_RUNBOOK.md`
12. `docs/AI_MODEL_ROUTING_STRATEGY.md`
13. `docs/ARCHITECTURE_LAYER_MAP.md`
14. `docs/ops/FOUNDER_DAILY_OPERATING_RHYTHM.md`
15. `docs/COMPETITIVE_POSITIONING.md`
16. `docs/DATA_RETENTION_POLICY.md`
17. `docs/DEALIX_OPERATING_CONSTITUTION.md`
18. `docs/DEPLOY_CHECKLIST.md`
19. `docs/DAY_1_LAUNCH_KIT.md`
20. `docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md`

## 📂 منظومة docs/ الجديدة (After cleanup)

```
docs/
├── INDEX.md                    ← هذا الملف
├── architecture/               ← AI_CONVENTIONS, PROMPTS
├── contributing/               ← CONTRIBUTING, CODE_OF_CONDUCT, DEPLOYMENT
├── operations/                 ← DEALIX_BUILD_TASK, COMPANY_OPERATIONAL_STATE, READINESS
├── playbooks/                  ← FOUNDER_NEXT_STEPS, QUICK_START
├── reference/                  ← KNOWN_LIMITATIONS
├── archive/                    ← DEALIX_PHASE2_CHEAP_TASK
└── 00_*, 01_*, ...             ← Constitution layers (428 subdirs)
```

---

## ⚠️ ملاحظات على ترتيب docs/

- **ترقيم متضارب** (01_category vs 01_category_creation, 16_agents vs 16_capital): مقصود — كل فرع موضوعي رقمه الخاص ضمن باب أكبر. التفاصيل في `DEALIX_MASTER_LAYERS_MAP.md`.
- **428 مجلد** = طبقة "Constitution" غنية. عادة الفاوندر يعمل مع 6-12 ملف فقط (انظر top-20 فوق).
- **لا تنقل ملفات** بدون تحديث `DEALIX_MASTER_EXECUTION_MATRIX.md`.
- **Frontend canonical:** `frontend/` (customer UI) + `apps/web/` (enterprise admin) كلاهما رسمي. لا تخلط.

---

## 🔍 البحث السريع

```bash
# ابحث في docs/ عن كلمة:
grep -rl "moyasar" docs/

# اعرض شجرة عمق 1:
ls docs/ | head -50

# 10 ملفات الأكبر (يحتمل تكون مهمة):
find docs/ -type f -name "*.md" -exec wc -l {} + | sort -rn | head -10
```
