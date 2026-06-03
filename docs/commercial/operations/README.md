# Commercial Operations — حزمة التنفيذ

مرتبطة بـ [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../MASTER_COMMERCIAL_OPERATING_PLAN_AR.md).

**مراجعة شاملة (36 قسمًا):** [COMMERCIAL_OPS_QUICK_REFERENCE_AR.md](../COMMERCIAL_OPS_QUICK_REFERENCE_AR.md) — CI/CD · Railway · checkout · approvals · North Star · CODE_MAP

| ملف | الغرض |
|-----|--------|
| [../GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md](../GTM_SAUDI_WEB_RESEARCH_PLAYBOOK_AR.md) | **فهرس GTM (بحث ويب):** ABM · لوب مؤسس · Proof Stack · مساران A/B |
| [GTM_DUAL_TRACK_CLARIFICATION_AR.md](GTM_DUAL_TRACK_CLARIFICATION_AR.md) | ترويج للعملاء vs ops داخلي — شجرة قرار |
| [FOUNDER_SALES_LOOP_AR.md](FOUNDER_SALES_LOOP_AR.md) | لوب مكالمة + TTV + مراجعة أسبوعية |
| [PROOF_STACK_ORDER_AR.md](PROOF_STACK_ORDER_AR.md) | ترتيب أدلة 1–5 (امتثال → pilot → case) |
| [founder_meeting_debrief_template.yaml](founder_meeting_debrief_template.yaml) | قالب بعد كل discovery/demo |
| [FOUNDER_GTM_CODIFICATION_AR.md](FOUNDER_GTM_CODIFICATION_AR.md) | ترميز أول 10 صفقات + [founder_gtm_codification_registry.yaml](founder_gtm_codification_registry.yaml) |
| [founder_pdpl_compliance_pass.yaml](founder_pdpl_compliance_pass.yaml) | قائمة PDPL للمؤسس — [FOUNDER_PDPL_COMPLIANCE_PASS_AR.md](../FOUNDER_PDPL_COMPLIANCE_PASS_AR.md) |
| [founder_weekly_decision_template.yaml](founder_weekly_decision_template.yaml) | قرار أسبوعي واحد — [FOUNDER_WEEKLY_ONE_DECISION_AR.md](../../ops/FOUNDER_WEEKLY_ONE_DECISION_AR.md) |
| [targeting/ABM_WAVE1_ICP_AR.md](targeting/ABM_WAVE1_ICP_AR.md) | موجة 1: 30–50 حساب warm + معايير ICP |
| [GTM_CHANNELS_PLAYBOOK_AR.md](GTM_CHANNELS_PLAYBOOK_AR.md) | قنوات warm · تسلسل لمسة · بوابة إعلان |
| [GTM_OBJECTION_MATRIX_AR.md](GTM_OBJECTION_MATRIX_AR.md) | ردود حية ↔ objection registry |
| [GTM_ROI_ONEPAGER_TEMPLATE_AR.md](GTM_ROI_ONEPAGER_TEMPLATE_AR.md) | قالب ROI للمشتريات |
| [GTM_WEEKLY_REVIEW_CHECKLIST_AR.md](GTM_WEEKLY_REVIEW_CHECKLIST_AR.md) | مراجعة GTM أسبوعية (جمعة) |
| [../FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md](../FULL_AUTONOMOUS_COMMERCIAL_OPS_AR.md) | أتمتة كاملة بحوكمة + مقارنة سوق 2026 |
| [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](EVIDENCE_EVENTS_CLOSE_PATH_AR.md) | مسار lead→proof + أحداث أدلة |
| [evidence_events_tracker.csv](evidence_events_tracker.csv) | تتبع يومي (انسخ صفوفاً) |
| [FIRST_PAID_DIAGNOSTIC_DOD_AR.md](FIRST_PAID_DIAGNOSTIC_DOD_AR.md) | DoD أول إيراد مدفوع |
| [motion_a_agency/](motion_a_agency/) | قوالب Motion A (نطاق، Proof، توسع) |
| [PARTNER_ONBOARDING_KIT_AR.md](PARTNER_ONBOARDING_KIT_AR.md) | حزمة شراكة |
| [AEO_CONTENT_CALENDAR_AR.md](AEO_CONTENT_CALENDAR_AR.md) | جدول صفحات إجابة |
| [objection_engine_registry.yaml](objection_engine_registry.yaml) | اعتراض → أصل |
| [COMMERCIAL_WEEKLY_SCORECARD_AR.md](COMMERCIAL_WEEKLY_SCORECARD_AR.md) | Pilots + Proof أسبوعياً |
| [COMMERCIAL_GOVERNANCE_GATES_AR.md](COMMERCIAL_GOVERNANCE_GATES_AR.md) | بوابات امتثال وقنوات |
| [sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md](sample_proof_pack/SAMPLE_PROOF_PACK_AGENCY_AR.md) | عيّنة Proof للوكالات |
| [FOUNDER_GTM_BENCHMARKS_AR.md](FOUNDER_GTM_BENCHMARKS_AR.md) | مقارنة GTM خارجية |
| `drafts/` (gitignored) | مخرجات `generate_commercial_content_pack.py` |
| [targeting/agency_accounts_seed.csv](targeting/agency_accounts_seed.csv) | قائمة أهداف Motion A (وكالات) |
| [targeting/gtm_revenue_machine_import.json](targeting/gtm_revenue_machine_import.json) | بذرة Data OS لـ revenue-machine |
| [GATED_AUTO_SEND_RFC_AR.md](GATED_AUTO_SEND_RFC_AR.md) | استكشاع إرسال تلقائي (معطّل افتراضياً) |
| [aeo_drafts/](aeo_drafts/) | مسودات صفحات AEO (نشر لاحقاً) |

**سكربتات:** `run_founder_commercial_day.sh` (canonical) · `founder_cadence.sh` / `.ps1` (صباح/مساء/أسبوع) · `run_founder_revenue_day.sh` (wrapper + Business NOW) · **`founder_comprehensive_plan_status.py`** · **`founder_weekly_decision_init.py`** · `verify_dealix_commercial_go_live.sh` · `commercial_war_room_sync.py` (P0 + outreach drafts) · `rotate_agency_targets.py` · `queue_content_drafts_for_approval.py` · **`founder_gtm_status.py`** · **`founder_meeting_debrief_init.py`** · **`verify_gtm_stack.py`**

**محتوى / سوشال — أي سكربت؟**

| سكربت | متى | مخرج |
|--------|-----|------|
| `social_queue_today.py` | يومي (ضمن revenue/commercial day) | منشور LinkedIn اليوم |
| `generate_commercial_content_pack.py` | جمعة (`founder_content_weekly.yml`) | `operations/drafts/` |
| `generate_weekly_content_drafts.py` | عند الحاجة | `var/content_drafts/YYYY-Www.json` |

**GitHub Actions secrets (إنتاج):**

| Secret | مطلوب لـ |
|--------|---------|
| `DEALIX_API_BASE` | [daily-revenue-machine.yml](../../.github/workflows/daily-revenue-machine.yml) |
| `DEALIX_API_KEY` | revenue-machine/run |
| `DEALIX_ADMIN_API_KEY` | evidence sync (اختياري) |
| `DEALIX_SYNC_EVIDENCE` | `1` لمزامنة CSV |

**محلي:** `bash scripts/run_founder_commercial_day.sh` → `data/founder_briefs/DAILY_PACK_YYYY-MM-DD.md`
