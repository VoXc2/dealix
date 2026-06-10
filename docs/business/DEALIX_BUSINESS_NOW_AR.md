# Dealix — مركز الأعمال (الآن)

**نقطة دخول واحدة للمؤسس:** تجاري، تسليم، منتج، امتثال، مالية، GTM، فريق، منصة.

- **واجهة:** `/ar/business-now`
- **أمر لقطة:** `bash scripts/run_business_now.sh` (Windows: `scripts/run_business_now.ps1`)
- **API:** `GET /api/v1/business-now/snapshot` · `GET /api/v1/business-now/commercial-strategy` · `GET /api/v1/business-now/operator-signals` (مفتاح admin)
- **Cache أحكام التحقق:** `dealix/transformation/business_now_cache.yaml`
- **الاستراتيجية التجارية:** [DEALIX_COMMERCIAL_STRATEGY_AR.md](DEALIX_COMMERCIAL_STRATEGY_AR.md)
- **حزمة Ops (Runbook + Deck):** [ops_client_pack/](../commercial/ops_client_pack/) — يظهر في `/ar/business-now#strategy` عبر `ops_client_pack` في API
- **بيع + ربط + وكلاء (مؤسس):** [FOUNDER_GO_LIVE_DAY0_AR.md](../ops/FOUNDER_GO_LIVE_DAY0_AR.md) · `bash scripts/founder_go_live_verify.sh`

### المرحلة 2

- **8 محاور** بما فيها GTM منفصل
- **KPI panel** من `GET /api/v1/transformation/kpi-snapshot`
- **امتثال حي:** ملخص من `/api/v1/compliance/status` (بدون ادّعاء PASS وهمي)
- **Enterprise Control Plane** في cache + `verify_enterprise_control_plane.sh`
- **إشارات المؤسس:** operator-signals عند مفتاح admin

---

## 1) تجاري — العروض والإيراد

| طبقة | مرجع |
| --- | --- |
| سلم القيمة | [VALUE_CAPTURE_LADDER.md](../value_capture/VALUE_CAPTURE_LADDER.md) |
| حزم RevOps | [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) |
| خريطة ربط | `GET /api/v1/commercial-map` |

**اليوم:** اختر عرضاً واحداً للتركيز (عادة Sprint 499 أو Diagnostic) — لا تفتح كل القنوات دفعة واحدة.

---

## 2) GTM ومبيعات

- ليدز: [SAUDI_LEAD_MACHINE_AR.md](../ops/SAUDI_LEAD_MACHINE_AR.md) · `POST /api/v1/leads`
- Playbook: [GTM_PLAYBOOK.md](../GTM_PLAYBOOK.md)
- قبل أي حملة: `POST /api/v1/revenue-os/anti-waste/check` أو [/trust-check](/trust-check)

**اليوم:** مسودة تواصل دافئ فقط — لا واتساب بارد، لا LinkedIn تلقائي.

---

## 3) تسليم وبايلوت

- Runbook: [PILOT_EXECUTION_RUNBOOK_AR.md](../transformation/enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md)
- متتبع 3 sprints: [pilot_sprint_tracker.yaml](../transformation/evidence/pilot_sprint_tracker.yaml)

---

## 4) منتج

- Dealix Cloud: `/ar/cloud`
- Private beta checklist: [PHASE2_PRIVATE_BETA_CHECKLIST.md](../PHASE2_PRIVATE_BETA_CHECKLIST.md)
- حالة YAML: [phase2_checklist_status.yaml](../../dealix/transformation/phase2_checklist_status.yaml)

---

## 5) امتثال وثقة

- PDPL: [SECURITY_PDPL_CHECKLIST.md](../SECURITY_PDPL_CHECKLIST.md)
- DPA: [DPA_PILOT_TEMPLATE.md](../DPA_PILOT_TEMPLATE.md)
- واتساب: [WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md)
- بوابة: `bash scripts/run_compliance_gtm_gate_bundle.sh`

---

## 6) مالية

- هامش منصة في `kpi_baselines.yaml` (ليس دفاتر CRM حتى التعبئة)
- Moyasar live: [CTO_MOYSASAR_PHASE3_GATE_AR.md](../transformation/CTO_MOYSASAR_PHASE3_GATE_AR.md)

---

## 7) فريق وملكية

- [ownership_matrix.yaml](../../dealix/transformation/ownership_matrix.yaml)
- [hiring_slots.yaml](../../dealix/transformation/hiring_slots.yaml)

---

## 8) منصة وتحقق

```bash
bash scripts/run_cto_weekly_anchor.sh
bash scripts/run_business_now.sh
python3 scripts/verify_global_ai_transformation.py
```

---

## معلّق على المؤسس (حقيقة تجارية)

الـ **6 KPIs** التجارية تبقى `pending` حتى تصدير CRM حقيقي:

1. انسخ `dealix/transformation/kpi_founder_commercial_import.example.yaml` → `kpi_founder_commercial_import.yaml`
2. عبّئ `value_numeric` + `source_ref` من HubSpot/المالية
3. `python3 scripts/apply_kpi_founder_commercial.py`

**لا تُخترع أرقاماً في الأتمتة.**

---

<!-- AUTO_GENERATED_START -->
# Business NOW snapshot — 2026-05-16

## Platform
- transformation_verdict: PASS
- governed_domains: 16

## Commercial KPIs
- pending: 6
- ready: 0

## Pilot sprints
- sprint_001: template_ready
- sprint_002: template_ready
- sprint_003: template_ready

## Today actions
- P1: عبّئ KPIs التجارية من CRM في kpi_founder_commercial_import.yaml ثم apply
- P2: ابدأ بايلوت sprint_001 — نفّذ PILOT_EXECUTION_RUNBOOK
- P3: راجع موافقات اليوم — لا إرسال خارجي بدون جواز
- P4: شغّل anti-waste قبل أي حملة أو رسالة خارجية

## Offers (summary)
- free_mini_diagnostic: 0.0 SAR — التشخيص المجاني المختصر
- revenue_proof_sprint_499: 499.0 SAR — سبرنت إثبات الإيرادات (٤٩٩ ر.س)
- data_to_revenue_pack_1500: 1500.0 SAR — حزمة من البيانات إلى الإيراد (١٥٠٠ ر.س)
- growth_ops_monthly_2999: 2999.0 SAR — عمليات النمو الشهرية (٢٩٩٩ ر.س / شهر)
- support_os_addon_1500: 1500.0 SAR — دعم Support OS (١٥٠٠ ر.س / شهر)
- executive_command_center_7500: 7500.0 SAR — غرفة قيادة الإدارة (٧٥٠٠ ر.س / شهر)
- agency_partner_os: 0.0 SAR — نظام الشريك الوكالة

<!-- AUTO_GENERATED_END -->
