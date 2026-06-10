# Commercial Gap Audit — Phase 0
**Agent #3 — Commercial Expansion Agent**
**التاريخ:** 2026-06-03
**النطاق:** الطبقة التجارية الكاملة لـ Dealix

> هذا التقرير يفصل ما هو موجود فعلاً في المستودع اليوم، وما ينقص، وما يجب بناؤه — ثم يحدد ترتيب التنفيذ للـ 16 مرحلة التالية.

---

## 1. الموجود من الأصول التجارية (Existing Commercial Assets)

### 1.1 وثائق استراتيجية و GTM
- `docs/commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md` — خطة يومية 5 دقائق
- `docs/commercial/DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md` — Control Tower + 4 Motions + SOAEN + Offer Matrix
- `docs/commercial/DEALIX_UNIFIED_REVENUE_ATLAS_AR.md` — أطلس الإيراد الموحد
- `docs/commercial/DEALIX_SALES_GTM_SOVEREIGN_MASTER_AR.md` — عمق GTM
- `docs/commercial/COMMERCIAL_VALUE_MAP_AR.md` — خريطة القيمة المادية
- `docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md` — حزم RevOps
- `docs/commercial/FOUNDER_SALES_PLAYBOOK_AR.md` — Playbook المبيعات للمؤسس
- `docs/commercial/FULL_OPS_CLOSE_ENGINE_AR.md` — هندسة قرار الإغلاق
- `docs/commercial/COMMERCIAL_LAUNCH_CHECKLIST_AR.md` — قائمة الإطلاق
- `docs/commercial/PAID_LAUNCH_TRACKER_AR.md` + `PAID_LAUNCH_AFTER_SOFT_PASS_AR.md`
- `docs/commercial/LAUNCH_EXECUTION_NOW_AR.md`
- `docs/commercial/INFRA_HOSTING_REGION_RUBRIC_AR.md`
- `docs/commercial/FOUNDER_PDPL_COMPLIANCE_PASS_AR.md`
- `docs/commercial/MARKET_INTELLIGENCE_*` — 20+ ملف (category battlecard, cloud cross border, content GTM, customer success, demo script, email templates, EN executive summary, founder revops GTM, governed AI, implementation playbook, investor partner, master index, metrics credibility, objections PDPL, PDPL legal review, procurement FAQ, sales champion pack, Saudi SaaS market, trust security matrix, weekly review)

### 1.2 ملفات الإعدادات التجارية (Config)
- `dealix/config/pricing.yaml` — تسعير مرجعي SAR
  - diagnostic: 4,999 / 9,999 / 15,000 / 25,000
  - sprint: from 25,000
  - retainer: 4,999–35,000 monthly
- `dealix/config/offers.yaml` — السلم الرئيسي (7-day diagnostic → sprint → retainer)
- `dealix/config/icp_segments.yaml` — Motions B/C/D + weekly rotation
- `dealix/config/icp_primary.yaml` — ICP رئيسي + 6 شرائح + disqualifiers
- `dealix/config/icp_agency_wedge.yaml` — ICP الوكالة (الوتد)
- `dealix/config/lead_scoring.yaml` — A/B/Nurture scoring
- `dealix/config/stage_transitions.yaml` — State machine (16 مرحلة)
- `dealix/config/partner_rules.yaml` — referral 10-20% + implementation + co-sell + white-label
- `dealix/config/affiliate_rules.yaml`
- `dealix/config/approval_policy.yaml` — 9 فئات موافقة (external_message, scope_send, invoice_send, diagnostic_final, proof_pack_final, case_study_publish, security_claim, discount_request, refund_request, affiliate_payout, agent_tool_action)
- `dealix/config/agent_permissions.yaml` — 9 وكلاء + defaults (external_send=blocked, scrape=blocked, etc.)
- `dealix/config/claim_policy.yaml` — قواعد الادعاء (no ROI/guarantees)
- `dealix/config/outreach_templates.yaml`
- `dealix/config/support_intents.yaml`

### 1.3 سجلات (Registers) وسياسات
- `dealix/registers/no_overclaim.yaml`
- `dealix/registers/compliance_saudi.yaml`
- `dealix/registers/90_day_execution.yaml`
- `dealix/registers/technology_radar.yaml`
- `auto_client_acquisition/governance_os/rules/` — 9 قواعد (no_source_no_answer, no_scraping, no_pii_in_logs, no_linkedin_automation, no_guaranteed_claims, no_fake_proof, no_cold_whatsapp, external_action_requires_approval, etc.)

### 1.4 سكربتات (Scripts) تشغيلية
- `scripts/founder_strongest_plan_status.py`
- `scripts/run_founder_revenue_day.sh` + `run_founder_commercial_day.sh`
- `scripts/founder_one_command.sh` — أمر واحد يومي
- `scripts/run_dealix_daily_ops.py`
- `scripts/run_ceo_master_plan_status.py`
- `scripts/founder_daily_five_metrics.py`
- `scripts/verify_commercial_launch_ready.py`
- `scripts/verify_dealix_commercial_go_live.sh/.ps1`
- `scripts/render_diagnostic_proposal.py`
- `scripts/commercial_value_map_status.py`
- `scripts/gtm_conversation_log.py`
- `scripts/founder_weekly_ceo_retro.py`
- `scripts/apply_kpi_founder_commercial.py`
- `scripts/partner_distribution_radar.py`
- (المزيد في `scripts/`)

### 1.5 اختبارات موجودة
- `tests/test_commercial_doctrine.py`
- `tests/test_commercial_launch_os.py`
- `tests/test_commercial_map.py`
- `tests/test_commercial_objections.py`
- `tests/test_commercial_ops_digest.py`
- `tests/test_commercial_strategy_simulate.py`
- `tests/test_commercial_strategy_snapshot.py`
- `tests/test_commercial_value_map_status.py`
- `tests/test_commercial_engagements_lead_intelligence.py`
- `tests/test_commercial_engagements_support_desk.py`
- `tests/test_commercial_engagements_quick_win_ops.py`
- `tests/test_commercial_roadmap_mvp.py`
- `tests/test_sales_os_core.py`
- `tests/test_sales_os_v12.py`
- `tests/test_partnership_os_v12.py`
- `tests/test_partner_distribution_radar.py`
- `tests/test_icp_scorer.py`
- `tests/test_pricing_plans_endpoint.py`
- `tests/test_designops_proposal_pricing.py`
- `tests/test_run_commercial_expansion.py`
- `tests/test_expand_commercial_stack.py`
- `tests/test_expand_commercial_ops_all.py`
- `tests/test_gtm_commercial_stack.py`
- `tests/test_apply_kpi_founder_commercial.py`
- `tests/test_founder_commercial_day_evidence.py`
- `tests/test_founder_commercial_day_script.py`
- `tests/test_founder_commercial_digest.py`

### 1.6 نماذج محتوى (Templates)
- `data/templates/whatsapp_templates_collection.md`
- `data/templates/warm_intro_whatsapp_ar.md`
- `data/templates/proposal_499_sar_ar.md`
- `data/templates/proof_pack_ar.md`
- `data/templates/founder_daily_checklist.md`
- `data/workflows/` — diagnostic, outreach_draft, lead_radar, onboarding, proof_pack, support, expansion

### 1.7 واجهات (UI routes) تجارية
- `/[locale]/` — Commercial Launch Home
- `/[locale]/dealix-diagnostic`
- `/[locale]/risk-score`
- `/[locale]/proof-pack`
- `/[locale]/learn/[slug]`
- `/[locale]/partners`
- `/[locale]/business-now`
- `/[locale]/ops/founder` (90-min cockpit)
- `/[locale]/ops/war-room` · `/ops/marketing` · `/ops/sales` · `/ops/partners` · `/ops/evidence` · `/ops/approvals`

---

## 2. الموجود من العروض والمنتجات (Offers/Products)
- **تشخيص 7 أيام** (Governed Revenue & AI Ops) — primary surface offer
- **Sprint (Revenue Intelligence)** — from 25,000 SAR
- **Retainer (Governed Ops)** — 4,999–35,000 SAR/شهر
- **Agency Motion** (Audit → Proof Pack → Co-sell)
- **Executive Motion** (RevOps Diagnostic → OS → Retainer)
- **Five Service OS pages** — marketing_os, sales_os, operations_os, client_portal_os, trust_os

---

## 3. الموجود من التسعير (Pricing)
- 4 شرائح للتشخيص (starter→enterprise): 4,999 / 9,999 / 15,000 / 25,000
- Sprint: from 25,000
- Retainer: monthly 4,999–35,000
- Partner referral: 10–20% من first payment
- White-label: minimum 3 paid pilots
- **Missing:** guards صريحة لـ discount، payment terms، quote approval levels، margin floor

---

## 4. الموجود من ICP و Buyer Personas
- 6 شرائح ICP في `icp_primary.yaml`
- 3 Motions (B/C/D) في `icp_segments.yaml` (Agency Motion A موصود في MASTER_PLAN)
- Disqualifiers أساسية: student/job_seeker، vague AI curiosity، no_company_name، budget<5K
- Routing by score: A≥15, B≥10, Nurture≥6
- **Missing:** Buyer Personas مفصّلة (CTO, Head of Sales, Clinic Manager، إلخ)، Pain Matrix رسمي، ICP priority report، Market segmentation بصياغة كاملة

---

## 5. الموجود من Sales Workflow
- 16 stage transitions (new_lead → closed_lost) في `stage_transitions.yaml`
- 4 Motions (A=Agency, B=Direct, C=Consultant, D=Executive)
- Discovery template: `os/14_DISCOVERY_CALL_TEMPLATE.md`
- Proposal template: `os/15_PROPOSAL_TEMPLATE.md`
- Handover template: `os/18_HANDOVER_TEMPLATE.md`
- QA checklist: `os/17_QA_CHECKLIST.md`
- Project controls: `os/13_PROJECT_CONTROLS_AI_OS.md`
- **Missing:** qualification rules مفصّلة، next-step rules، pipeline review methodology، daily/weekly commercial rhythm مفصّل

---

## 6. الموجود من Proposal / Proof / Payment
- Approval policy صارمة (`approval_policy.yaml`)
- Proof pack template: `data/templates/proof_pack_ar.md`
- Proposal 499 SAR template: `data/templates/proposal_499_sar_ar.md`
- `api/routers/commercial.py` — 13 commercial chain endpoints
- `dealix/commercial/proof_builder.py`
- `dealix/commercial/case_study_generator.py`
- Sample proof: `docs/commercial/operations/sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md`
- **Missing:** proposal approval policy مفصّلة، proof pack commercial guide، case study policy، generic commercial_proposal schema، commercial_proof_pack schema

---

## 7. الموجود من Delivery / Renewal / Customer Success
- Onboarding template: `os/16_CLIENT_ONBOARDING_TEMPLATE.md`
- Handover template: `os/18_HANDOVER_TEMPLATE.md`
- Client success report: `os/19_CLIENT_SUCCESS_REPORT.md`
- Expansion playbook: `os/20_EXPANSION_PLAYBOOK.md`
- `dealix/commercial/pilot_delivery.py`
- `MARKET_INTELLIGENCE_CUSTOMER_SUCCESS_AR.md`
- **Missing:** first 30 days system، client health score، weekly value report template، renewal playbook مفصّل، expansion playbook مفصّل

---

## 8. الموجود من Partner / Channel
- `dealix/config/partner_rules.yaml` (4 نماذج)
- `docs/partners/PARTNER_PILOT_PIPELINE.yaml`
- `docs/commercial/operations/PARTNER_ONBOARDING_KIT_AR.md` (مرجود)
- `tests/test_partnership_os_v12.py`
- `tests/test_partner_distribution_radar.py`
- 4 GTM public surfaces
- Email channel، WhatsApp after-consent channel (سياسات موجودة)
- **Missing:** channel strategy مفصّلة، partner pricing/margin، partner qualification، partner enablement kit، channel ROI model

---

## 9. الموجود من Finance / Unit Economics
- `dealix/transformation/kpi_founder_commercial_registry.yaml`
- `dealix/transformation/kpi_founder_commercial_import.example.yaml`
- `scripts/apply_kpi_founder_commercial.py`
- **Missing:** unit economics، offer margin model، CAC/payback model، channel ROI، sales capacity model، retainer revenue model

---

## 10. الموجود من Dashboards / Reports
- `/[locale]/ops/founder` — cockpit 90 دقيقة
- `/[locale]/ops/war-room` — أعلى 10
- `/[locale]/ops/marketing` — today + factory
- `/[locale]/ops/sales` · `/partners` · `/evidence` · `/approvals`
- APIs: `/api/v1/ops-autopilot/war-room/today-pack` · `.../marketing/queue-approval` · `.../marketing/social-today`
- `reports/company_os/control/latest_tick.json` · `doctor.json`
- `reports/revenue/dealix_revenue_asset_index.md`
- **Missing:** commercial control room spec موحّد، daily command، weekly review methodology

---

## 11. الناقص من الأنظمة التجارية (Missing Commercial Systems)

### 11.1 Gap Analysis — أولوية عالية
1. **Pricing Guardrails رسمية** — لا توجد قواعد discount/quote approval صريحة (يوجد approval policy عام فقط)
2. **Buyer Personas مفصّلة** — غير موجودة كملف مستقل
3. **Pain-to-Offer Matrix** — غير موجود كملف رسمي
4. **Customer Health Score** — غير موجود
5. **First 30 Days System** — غير موثّق
6. **Walk-Away Rules / Bad-Fit Client Policy** — غير موجود
7. **Unit Economics / Offer Margin Model** — غير موجود
8. **Channel ROI Model** — غير موجود
9. **ICP Priority Report** — لا يوجد تقرير مفصّل بالأولويات
10. **Commercial Tests** — موجودة كثيرة لكن لا يوجد تغطية لـ:
    - test_pricing_requires_approval
    - test_no_guaranteed_revenue_claims
    - test_payment_handoff_requires_approval
    - test_walk_away_rules
    - test_partner_model_margin_rules

### 11.2 Gap Analysis — أولوية متوسطة
1. **Objection Bank** مفصّل (موجود في MARKET_INTELLIGENCE_OBJECTIONS_PDPL_AR.md لكن غير مهيكَل)
2. **Competitor Positioning Matrix** — غير موجود كملف مستقل
3. **ROI Conversation Guide** — غير موجود
4. **Risk Reversal Policy** — غير موجود
5. **Content Channel Strategy** — مدمج لكن غير منفصل
6. **Press Channel Strategy** — غير منفصل
7. **Referral Channel** — موجود لكن غير مهيكل
8. **Customer Success Agents** permission matrix
9. **Renewal Agent** كوحدة مستقلة
10. **Commercial Risk Register** مفصّل
11. **Scope Creep Policy** — غير موجود
12. **Commercial Agent Roles** — لا يوجد ملف موحّد

### 11.3 Gap Analysis — أولوية منخفضة (تحسين)
1. **Bad-Fit Client Policy** — موجود ضمنياً في disqualifiers
2. **Disqualification Rules** — موجودة جزئياً في `icp_primary.yaml`
3. **Price Anchoring Guide** — غير منفصل
4. **Quote Approval Policy** — موجودة جزئياً في approval_policy
5. **Discount Policy** — غير منفصل
6. **Payment Terms** — موجودة ضمنياً (MANUAL_PAYMENT_SOP)

---

## 12. التعارضات والتكرارات (Conflicts/Duplicates)

### 12.1 لا تعارضات حرجة
- الـ existing configs و docs تستخدم YAML في الغالب و AR markdown للوثائق
- Approval policy صارمة ومتسقة عبر الملفات
- No-overclaim register و claim_policy متطابقتان

### 12.2 تكرارات يمكن توحيدها
- `icp_segments.yaml` و `icp_primary.yaml` و `icp_agency_wedge.yaml` — يمكن توحيدها في ICP matrix شامل (لكن **لا نلمس** الملفات الموجودة، نضيف ملفات جديدة تكاملية)
- `partner_rules.yaml` و `docs/partners/PARTNER_PILOT_PIPELINE.yaml` و `operations/PARTNER_ONBOARDING_KIT_AR.md` — منفصلان لكن متكاملان
- `claim_policy.yaml` و `no_overclaim.yaml` — متطابقان فعلياً (لا نلمسهما)
- `approval_policy.yaml` و `agent_permissions.yaml` — متكاملان (لا نلمسهما)

**القاعدة:** Agent #3 **لا يحذف ولا يعدل** الموجود، فقط يضيف ملفات تكاملية في:
- `docs/commercial/` (إضافة وثائق)
- `reports/commercial/` (إنشاء مجلد جديد)
- `data/commercial/` (إنشاء مجلد جديد)
- `data/customer_success/` (إنشاء مجلد جديد)
- `data/partners/` (تأكيد وجود)
- `data/evals/commercial_safety_cases.jsonl`
- `schemas/` (إضافة schemas جديدة)
- `tests/` (إضافة tests جديدة بـ prefix `test_commercial_`)
- `docs/agents/` (إنشاء مجلد جديد)

---

## 13. أعلى المخاطر التجارية (Highest-Risk Commercial Gaps)

| # | الفجوة | المخاطرة | الأثر المالي |
|---|--------|----------|--------------|
| 1 | لا يوجد pricing guardrails صريحة | Discount عشوائي، تآكل الهامش | عالٍ |
| 2 | لا يوجد walk-away rules | قبول عملاء سيئين، إهدار delivery | عالٍ |
| 3 | لا يوجد client health score | churn غير مرئي، فقدان تجديد | عالٍ |
| 4 | لا يوجد first 30 days system | فشل التسليم، استرداد | عالٍ |
| 5 | لا يوجد offer margin model | بيع بخسارة | عالٍ |
| 6 | لا يوجد channel ROI | استمرار قنوات مكلفة | متوسط |
| 7 | لا يوجد buyer personas مفصّلة | رسائل غير موجهة، ضعف التحويل | متوسط |
| 8 | لا يوجد pain-to-offer matrix | اقتراح خاطئ، وقت ضائع | متوسط |
| 9 | لا يوجد payment handoff approval test | تسعير خاطئ، فوضى فواتير | متوسط |
| 10 | لا يوجد scope creep policy | توسيع غير محكوم | متوسط |

---

## 14. ترتيب التنفيذ الموصى به (Recommended Implementation Order)

> الترتيب يتبع منطق: **Audit → Foundation → Systems → Operations → Safety**

### 14.1 Foundation (PHASE 1)
- بناء Commercial Operating System لأنه القاعدة التي ترتبط بها كل المراحل
- تحديد Decisional Rules واضحة

### 14.2 Foundation Data (PHASES 2-5)
- ICP matrix → Buyer personas → Pain matrix → Offer ladder → Pricing guardrails
- هذا التسلسل منطقي: مَن → مَن فيهم → ما المشكلة → ما الحل → بكم

### 14.3 Sales Operations (PHASES 6-8)
- Sales process → Proposal/proof → Objection handling
- هذا التسلسل منطقي: كيف نبيع → كيف نقنع بالعرض → كيف نتعامل مع الاعتراضات

### 14.4 Channels & Partnerships (PHASES 9-10)
- القنوات → الشراكات (الشراكات قناة مدمجة)

### 14.5 Post-Sale (PHASE 11)
- Customer success (بعد إتمام الصفقة، لكن يجب أن يكون النظام جاهز قبل البيع)

### 14.6 Finance & Risk (PHASES 12-13)
- Finance metrics → Risk register (مترابطان)

### 14.7 Control Room & Tests (PHASES 14-15)
- Control Room (واجهة) → Tests (حماية)

### 14.8 Agent Roles (PHASE 16)
- تعريف الوكلاء التجاريين (يعتمد على كل ما سبق)

### 14.9 Final Report
- ربط كل شيء في تقرير نهائي

---

## 15. المخرجات الإجمالية المتوقعة

- ~50 وثيقة جديدة (AR markdown)
- ~10 schemas جديدة (JSON)
- ~10 ملفات data (YAML/JSONL/CSV)
- ~8 tests جديدة
- ~3 ملفات evals
- 1 تقرير نهائي شامل

**كل الملفات الجديدة** تكاملية — لا تحذف ولا تعدل الموجود.

---

## 16. قواعد غير قابلة للتفاوض (Non-Negotiable Rules) — مذكّرة

- ❌ لا تفعيل إرسال خارجي
- ❌ لا إرسال بريد
- ❌ لا إرسال WhatsApp
- ❌ لا LinkedIn automation
- ❌ لا scraping
- ❌ لا spam workflows
- ❌ لا ادعاءات مضمونة
- ❌ لا دراسات حالة ملفقة
- ❌ لا تسعير نهائي بدون موافقة
- ❌ لا التزامات قانونية
- ✅ كل شيء external → dry_run + approval_required

---

## 17. جاهز للبدء

ننتقل إلى PHASE 1 — Commercial Operating System.
