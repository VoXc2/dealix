# خريطة الكود — أنظمة Dealix التشغيلية ↔ الحزم في الريبو

هذا الملف يربط **أسماء الأنظمة/خطوط الخدمة** في الوثائق التجارية بالمسارات الفعلية في المستودع. التسليم الافتراضي للعملاء يبقى **مسودات + تقارير** مع **موافقة بشرية** قبل أي إجراء خارجي (PDPL، anti-waste، بوابات المسودات).

| الاسم في الوثائق (OS / خط خدمة) | حزم Python رئيسية | أهم مسارات API (FastAPI) | سكربتات / تقارير | ملاحظات حوكمة |
|----------------------------------|-------------------|----------------------------|-------------------|----------------|
| **Strategy OS** | [`auto_client_acquisition/strategy_os/`](../../auto_client_acquisition/strategy_os/) | — (منطق مكتبة؛ ربط لاحق بالـ API حسب المنتج) | — | قراءات حتمية؛ لا إرسال خارجي. |
| **Revenue OS** | [`auto_client_acquisition/revenue_os/`](../../auto_client_acquisition/revenue_os/) | [`api/routers/leads.py`](../../api/routers/leads.py)، [`api/routers/revenue_os.py`](../../api/routers/revenue_os.py)، [`api/routers/revenue_os_catalog.py`](../../api/routers/revenue_os_catalog.py) | [`scripts/revenue_os_master_verify.sh`](../../scripts/revenue_os_master_verify.sh) | مسودات pipeline؛ anti-waste؛ لا cold WhatsApp تلقائي. |
| **Customer OS (دعم)** | [`auto_client_acquisition/support_os/`](../../auto_client_acquisition/support_os/) | — (يُستدعى من مشغّلات Sprint أو راوترات لاحقة) | — | تصنيف + مسودات رد؛ **لا إرسال** من هذه الطبقة. |
| **Marketing OS** | [`auto_client_acquisition/gtm_os/`](../../auto_client_acquisition/gtm_os/)، [`auto_client_acquisition/self_growth_os/`](../../auto_client_acquisition/self_growth_os/) | حسب الراوترات المرتبطة بالنمو | — | محتوى/حملات مربوطة بالعرض؛ بدون scraping إنتاجي افتراضياً. |
| **Operations OS** | [`api/routers/delivery_factory.py`](../../api/routers/delivery_factory.py)، [`api/routers/bottleneck_radar.py`](../../api/routers/bottleneck_radar.py) | نفس الملفات | [`scripts/`](../../scripts/) (`dealix_*`) | قراءات/تقارير؛ تغييرات حساسة خلف موافقة. |
| **Governance OS** | [`auto_client_acquisition/governance_os/`](../../auto_client_acquisition/governance_os/)، [`auto_client_acquisition/compliance_os/`](../../auto_client_acquisition/compliance_os/) | [`api/routers/pdpl.py`](../../api/routers/pdpl.py) (وما شابه) | — | `draft_gate`، انتهاكات intake؛ مسودات فقط. |
| **Data OS** | [`auto_client_acquisition/data_os/`](../../auto_client_acquisition/data_os/) | — | — | جودة جداول، اكتمال؛ حتمي. |
| **Delivery OS** | [`auto_client_acquisition/delivery_os/`](../../auto_client_acquisition/delivery_os/)، [`auto_client_acquisition/service_sessions/`](../../auto_client_acquisition/service_sessions/) | [`api/routers/service_sessions.py`](../../api/routers/service_sessions.py) | — | مراحل تسليم + قوائم تحقق افتراضية. |
| **Reporting OS** | [`auto_client_acquisition/reporting_os/`](../../auto_client_acquisition/reporting_os/)، [`executive_reporting/`](../../auto_client_acquisition/executive_reporting/) | — | — | غلاف تقارير + proof pack منطقي. |
| **Knowledge OS** | [`auto_client_acquisition/knowledge_os/`](../../auto_client_acquisition/knowledge_os/)، [`support_os/knowledge_answer.py`](../../auto_client_acquisition/support_os/knowledge_answer.py)، [`company_brain_mvp/`](../../auto_client_acquisition/company_brain_mvp/) | `POST /api/v1/company-brain/query` | — | اقتباسات؛ حدود «لا مصدر لا إجابة» عبر الـ API. |
| **Dealix Master System (8 أنظمة)** | — | [`docs/company/DEALIX_MASTER_SYSTEM_AR.md`](../company/DEALIX_MASTER_SYSTEM_AR.md) | [`scripts/verify_full_mvp_ready.py`](../../scripts/verify_full_mvp_ready.py) | يربط السوق → النمو بوثائق + تحقق. |
| **Agentic Enterprise (Systems 16–25)** | [`auto_client_acquisition/agentic_enterprise_os/`](../../auto_client_acquisition/agentic_enterprise_os/) | — (حالياً عقود قدرات + مؤشرات جاهزية) | [`platform/system_16_25_registry.json`](../../platform/system_16_25_registry.json) | تخطيط قدرة تشغيلية (Capability-first)؛ بلا تنفيذ خارجي تلقائي. |
| **Service docs ↔ service_id** | — | [`docs/company/SERVICE_ID_MAP.yaml`](../company/SERVICE_ID_MAP.yaml)، [`docs/services/`](../services/) | [`scripts/verify_service_files.py`](../../scripts/verify_service_files.py) | مثال: `ai_support_desk_sprint` ↔ `support_desk_sprint`. |

| **قاعدة الاحتراف** | — | [`docs/company/COMPANY_PROFESSIONALISM_AR.md`](../company/COMPANY_PROFESSIONALISM_AR.md) | — | لا ارتجال؛ كل خدمة نظام + QA + proof + توسع. |
| **Dealix Method** | — | [`docs/company/DEALIX_METHOD_AR.md`](../company/DEALIX_METHOD_AR.md) | — | Diagnose → Expand؛ تكرار تسليم عالي الجودة. |
| **محركات التسليم (نية)** | — | [`docs/product/DELIVERY_ENGINES_INTENT_AR.md`](../product/DELIVERY_ENGINES_INTENT_AR.md) | — | ربط المراحل بجودة/حوكمة/إثبات/playbooks/تعلّم + Growth. |
| **رؤية AI OS (24 شهراً)** | — | [`docs/company/DEALIX_AI_OS_LONG_TERM_AR.md`](../company/DEALIX_AI_OS_LONG_TERM_AR.md)، [`docs/strategy/ROADMAP_24_MONTH_AR.md`](../strategy/ROADMAP_24_MONTH_AR.md) | — | مستويات 1–5، BUs، Enterprise gates. |

## مشغّلات Sprint (تشغيل موحّد JSON)

| المشغّل | الوحدة | الغرض |
|---------|--------|--------|
| Lead Intelligence Sprint | [`auto_client_acquisition/commercial_engagements/lead_intelligence_sprint.py`](../../auto_client_acquisition/commercial_engagements/lead_intelligence_sprint.py) | جودة بيانات + dedupe + ترتيب + مسودات + فحص مسودة (`audit_draft_text`). |
| Support Desk Sprint | [`support_desk_sprint.py`](../../auto_client_acquisition/commercial_engagements/support_desk_sprint.py) | تصنيف + مسودة رد + SLA (بدون إرسال). |
| Quick Win Ops | [`quick_win_ops.py`](../../auto_client_acquisition/commercial_engagements/quick_win_ops.py) | تلخيص أسبوعي + قوائم تحقق مراحل BUILD/VALIDATE. |

### تشغيل عبر API (محلي)

المسارات تتطلب رأس **`X-API-Key`** عند تعيين متغير البيئة **`API_KEYS`** (قائمة مفاتيح مفصولة بفواصل). في التطوير بدون مفاتيح، الـ middleware يمرّر الطلبات (انظر [`api/security/api_key.py`](../../api/security/api_key.py)).

```bash
# Lead Intelligence Sprint — جسم JSON: { "accounts": [ { "company_name": "...", "sector": "...", "city": "..." } ] }
curl -sS -X POST "http://localhost:8000/api/v1/commercial/engagements/lead-intelligence-sprint" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d "{\"accounts\":[{\"company_name\":\"مثال\",\"sector\":\"تقنية\",\"city\":\"الرياض\"}]}"

# Support Desk Sprint — جسم: { "messages": [ "نص الرسالة 1", "نص الرسالة 2" ] }
curl -sS -X POST "http://localhost:8000/api/v1/commercial/engagements/support-desk-sprint" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d "{\"messages\":[\"أريد استرداد المبلغ\",\"سؤال عن الاشتراك\"]}"

# Quick Win Ops — جسم: { "weekly_rows": [ { "channel": "email", "count": 3 } ], "group_by": "channel" }
curl -sS -X POST "http://localhost:8000/api/v1/commercial/engagements/quick-win-ops" \
  -H "Content-Type: application/json" \
  -H "X-API-Key: YOUR_KEY" \
  -d "{\"weekly_rows\":[{\"channel\":\"email\",\"count\":3}],\"group_by\":\"channel\"}"
```

## جاهزية استراتيجية (Strategy OS)

- [`auto_client_acquisition/strategy_os/ai_readiness.py`](../../auto_client_acquisition/strategy_os/ai_readiness.py) — درجات 0–1 لمحاور + `readiness_score` + `recommended_next_service` (حتمي، بدون LLM).

## مسارات إضافية (خطة AI Operations — MVP)

| الغرض | مسار API | الوحدة |
|--------|-----------|--------|
| كتالوج التسليم + ربط الوثائق | `GET /api/v1/commercial/engagements/delivery-catalog` | [`commercial_engagements/delivery_catalog.py`](../../auto_client_acquisition/commercial_engagements/delivery_catalog.py) |
| معاينة CSV للحسابات | `POST /api/v1/revenue-data/csv-preview` | [`revenue_data_intake/csv_preview.py`](../../auto_client_acquisition/revenue_data_intake/csv_preview.py) |
| لوحة CRM تجريبية | `GET/POST /api/v1/revenue-data/crm-board` | [`revenue_data_intake/crm_board_mvp.py`](../../auto_client_acquisition/revenue_data_intake/crm_board_mvp.py) |
| حملة تسويقية حتمية + فحص مسودة | `POST /api/v1/commercial/engagements/campaign-intelligence-sprint` | [`campaign_intelligence_sprint.py`](../../auto_client_acquisition/commercial_engagements/campaign_intelligence_sprint.py) |
| Company Brain MVP (ذاكرة داخل العملية) | `POST /api/v1/company-brain/ingest`، `POST /api/v1/company-brain/query` | [`company_brain_mvp/`](../../auto_client_acquisition/company_brain_mvp/) |
| لوحة مخاطر للمؤسس | `GET /api/v1/governance/risk-dashboard` | [`governance_risk_dashboard.py`](../../api/routers/governance_risk_dashboard.py) + [`policy_registry.py`](../../auto_client_acquisition/governance_os/policy_registry.py) |
| طابور تقارير Sprint (ARQ) | `POST /jobs` مع `job_type: commercial_sprint_report` | [`core/queue/tasks.py`](../../core/queue/tasks.py) |
| واجهة تجريبية للخدمات | `NEXT_PUBLIC_SHOW_OPERATIONAL_TOOLS` | [`frontend/src/components/services/SprintToolsPanel.tsx`](../../frontend/src/components/services/SprintToolsPanel.tsx) |
| مقاييس North Star | وثيقة | [`NORTH_STAR_METRICS_AR.md`](NORTH_STAR_METRICS_AR.md) |
| تحقق قدرة التشغيل (اختبارات السوق + النضج) | وثيقة | [`docs/company/CAPABILITY_VERIFICATION_AR.md`](../company/CAPABILITY_VERIFICATION_AR.md) |
| درجة جاهزية الخدمة (0–100) | `GET/POST /api/v1/commercial/service-readiness/{service_id}` | [`delivery_os/service_readiness.py`](../../auto_client_acquisition/delivery_os/service_readiness.py) + [`service_readiness_defaults.yaml`](../../auto_client_acquisition/governance_os/policies/service_readiness_defaults.yaml) |
| بوابات التسليم / AI / الإنتاج | `POST /api/v1/commercial/readiness-gates/check` | [`delivery_os/readiness_gates.py`](../../auto_client_acquisition/delivery_os/readiness_gates.py) |
| لوحة تشغيل المؤسس | `GET /api/v1/founder/operating-scorecard` | [`api/routers/founder.py`](../../api/routers/founder.py) |
| سكربت CI للقدرة | `bash scripts/dealix_capability_verify.sh` | [`scripts/dealix_capability_verify.sh`](../../scripts/dealix_capability_verify.sh) |
