# فهرس التشغيل الرئيسي — CTO / المؤسس (24 شهرًا)

**ابدأ من «الآن»:** [DEALIX_BUSINESS_NOW_AR.md](../business/DEALIX_BUSINESS_NOW_AR.md) · `/ar/business-now` · `bash scripts/run_business_now.sh`

نقطة دخول واحدة لبرنامج Dealix الموسّع. لا يكرّر محتوى الوثائق — يربطها بمحاور وبوابات زمنية.

## المحور 0 — حوكمة البرنامج والقياس

| إيقاع | أمر |
| --- | --- |
| أسبوعي CTO | `bash scripts/run_cto_weekly_anchor.sh` |
| أسبوعي تنفيذي | `bash scripts/run_executive_weekly_checklist.sh` |
| شهري | `bash scripts/run_ceo_one_session_readiness.sh` |
| قبل توسع | `bash scripts/run_pre_scale_gate_bundle.sh` |
| أعمدة تحقق | `bash scripts/run_cto_pillar_verify_bundle.sh` · `bash scripts/run_compliance_gtm_gate_bundle.sh` |

**وثائق:** [CTO_EXECUTIVE_CADENCE_AR.md](CTO_EXECUTIVE_CADENCE_AR.md) · [EXECUTIVE_OPERATING_CHECKLIST_AR.md](EXECUTIVE_OPERATING_CHECKLIST_AR.md) · [CEO_ONE_SESSION_MASTER_PLAN_AR.md](CEO_ONE_SESSION_MASTER_PLAN_AR.md)

**سجلات YAML:** [`dealix/transformation/`](../../dealix/transformation/) — `kpi_baselines`, `ownership_matrix`, `risk_register`, `todo_registry`, `ceo_signal_os`

**API قراءة KPI:** `GET /api/v1/transformation/kpi-snapshot`

---

## المحور 1 — تجاري وإيرادات

| موضوع | مرجع |
| --- | --- |
| سلم القيمة | [docs/value_capture/VALUE_CAPTURE_LADDER.md](../value_capture/VALUE_CAPTURE_LADDER.md) |
| تسعير وعروض | [OFFER_PRICING_MODEL.md](../value_capture/OFFER_PRICING_MODEL.md) · [commercial/DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) |
| GTM | [08_gtm_system_playbook.md](08_gtm_system_playbook.md) · [docs/GTM_PLAYBOOK.md](../GTM_PLAYBOOK.md) |
| ليدز سعودية | [docs/ops/SAUDI_LEAD_MACHINE_AR.md](../ops/SAUDI_LEAD_MACHINE_AR.md) |
| KPI تجاري (مؤسس) | [`kpi_founder_commercial_registry.yaml`](../../dealix/transformation/kpi_founder_commercial_registry.yaml) + `apply_kpi_founder_commercial.py` |
| توسع فئة | [12_category_dominance.md](12_category_dominance.md) · [`category_expansion_gates.yaml`](../../dealix/transformation/category_expansion_gates.yaml) |
| إطلاق تجاري | [COMMERCIAL_LAUNCH_MASTER_PLAN.md](../COMMERCIAL_LAUNCH_MASTER_PLAN.md) |

---

## المحور 2 — تسليم ونجاح عميل

| موضوع | مرجع |
| --- | --- |
| موجات تنفيذ | [DEALIX_EXECUTION_WAVES_AR.md](../strategic/DEALIX_EXECUTION_WAVES_AR.md) |
| بايلوت / sprint | [enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md](enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md) |
| تتبع 3 sprints | [evidence/pilot_sprint_tracker.yaml](evidence/pilot_sprint_tracker.yaml) |
| برج تسليم | [10_delivery_control_tower.md](10_delivery_control_tower.md) |
| نطاق | [SCOPE_CONTROL_SYSTEM.md](../value_capture/SCOPE_CONTROL_SYSTEM.md) |

---

## المحور 3 — منتج و Dealix Cloud

| موضوع | مرجع |
| --- | --- |
| رؤية | [DEALIX_CLOUD_VISION.md](../product/DEALIX_CLOUD_VISION.md) |
| خارطة UI | [DEALIX_CLOUD_UI_MAP.md](../product/DEALIX_CLOUD_UI_MAP.md) |
| واجهة | `/[locale]/cloud` |
| Revenue OS API | [AGENTS.md](../../AGENTS.md) (Decision Passport · catalog · anti-waste) |
| Phase 2 beta | [PHASE2_PRIVATE_BETA_CHECKLIST.md](../PHASE2_PRIVATE_BETA_CHECKLIST.md) · [PHASE1_2_CTO_STATUS.md](PHASE1_2_CTO_STATUS.md) |

---

## المحور 4 — هندسة ومنصة

| موضوع | مرجع |
| --- | --- |
| 12 مبادرة | [CTO_12_PILLAR_BACKLOG.md](CTO_12_PILLAR_BACKLOG.md) · [GLOBAL_AI_TRANSFORMATION_EXECUTION_INDEX_AR.md](GLOBAL_AI_TRANSFORMATION_EXECUTION_INDEX_AR.md) |
| فجوات MVP | [02_gap_closure_matrix.md](02_gap_closure_matrix.md) · `evidence/gap_closure_*.md` |
| حوكمة موسّعة | [04_governance_expansion.md](04_governance_expansion.md) · `governance_workflow_inventory.yaml` |
| قطع إنتاج | [ENGINEERING_CUTOVER_RUNBOOK_AR.md](ENGINEERING_CUTOVER_RUNBOOK_AR.md) · [CUTOVER_PR_CHECKLIST_AR.md](CUTOVER_PR_CHECKLIST_AR.md) |
| Knowledge / embeddings | [EMBEDDINGS_PIPELINE.md](../EMBEDDINGS_PIPELINE.md) · `scripts/check_embeddings_readiness.py` |
| نشر | [DEPLOYMENT.md](../../DEPLOYMENT.md) |

---

## المحور 5 — امتثال وثقة

| موضوع | مرجع |
| --- | --- |
| PDPL | [SECURITY_PDPL_CHECKLIST.md](../SECURITY_PDPL_CHECKLIST.md) |
| DPA | [DPA_PILOT_TEMPLATE.md](../DPA_PILOT_TEMPLATE.md) |
| Trust Pack | [ENTERPRISE_TRUST_PACK.md](../trust/ENTERPRISE_TRUST_PACK.md) |
| Moyasar Phase 3 | [CTO_MOYSASAR_PHASE3_GATE_AR.md](CTO_MOYSASAR_PHASE3_GATE_AR.md) |

---

## المحور 6 — تنظيم وفريق

| موضوع | مرجع |
| --- | --- |
| نظام تشغيل | [11_org_operating_system.md](11_org_operating_system.md) |
| ملاك | [`ownership_matrix.yaml`](../../dealix/transformation/ownership_matrix.yaml) |
| توظيف | [`hiring_slots.yaml`](../../dealix/transformation/hiring_slots.yaml) |
| تدريب | [docs/training/](../training/) |

---

## المحور 7 — شركاء / أكاديمية / ventures (سنة 2+)

| موضوع | مرجع |
| --- | --- |
| شركاء | [PARTNER_MONETIZATION.md](../value_capture/PARTNER_MONETIZATION.md) |
| أكاديمية | [ACADEMY_MONETIZATION.md](../value_capture/ACADEMY_MONETIZATION.md) |
| ventures | [VENTURE_GRADUATION_GATE.md](../ventures/VENTURE_GRADUATION_GATE.md) |

---

## المحور 8 — ذكاء تشغيلي

| موضوع | مرجع |
| --- | --- |
| Operating brain | [OPERATING_BRAIN.md](../intelligence/OPERATING_BRAIN.md) |
| تقرير تعلّم | `GET /api/v1/revenue-os/learning/weekly-template` |

---

## خارطة زمنية (بوابات — لا أيام)

### 0–90 يوم

- [ ] `run_cto_weekly_anchor` مستمر
- [ ] 6 KPIs تجارية من CRM (`kpi_founder_commercial_import.yaml` + apply)
- [ ] بايلوت #1 في [pilot_sprint_tracker.yaml](evidence/pilot_sprint_tracker.yaml)
- [ ] Phase 1 staging + Phase 2 checklist ([PHASE1_2_CTO_STATUS.md](PHASE1_2_CTO_STATUS.md))

### 90–180 يوم

- [ ] 3 sprints موثّقة L4+ في tracker
- [ ] أول retainer ببوابة adoption
- [ ] Moyasar test → [CTO_MOYSASAR_PHASE3_GATE_AR.md](CTO_MOYSASAR_PHASE3_GATE_AR.md)

### 180–365 يوم

- [ ] Dealix Cloud لعميل خارجي
- [ ] قطاع واحد: `saudi_fintech_b2b` في category gates
- [ ] أول hire: [`hiring_slots.yaml`](../../dealix/transformation/hiring_slots.yaml)

### 12–24 شهر

- [ ] Enterprise متكرر · partner pilot · academy مسودة · venture gate واحد

---

## أوامر سريعة

```bash
bash scripts/run_cto_weekly_anchor.sh
python3 scripts/apply_kpi_founder_commercial.py --status
python3 scripts/check_embeddings_readiness.py
bash scripts/verify_ceo_signal_readiness.sh revenue_os
```
