# خطة الجلسة الواحدة — رؤية CEO استراتيجية (Dealix)

## لماذا هذه الوثيقة؟

الريبو يحتوي اليوم على **مسار تشغيل + مسار هندسة + بوابات تحقق**. ما يبقى لإغلاق «الجاهزية التجارية» ليس أيام تقويمية بل **ثلاث طبقات حقيقة**: إثبات سوق، أرقام مصدرية، وقطع تقني بإشارة. هذه الخطة تجمع كل ذلك في **أمر واحد** قدر الإمكان، مع مقارنة سوقية قبل أي قرار توسع.

---

## مقارنة سوقية (بحث 2025–2026) — ماذا يفعل الآخرون وكيف يختلف Dealix

| بعد | منصات Revenue Intelligence (Clari / Gong / نمط السوق) | Dealix (هذا الريبو) |
| --- | --- | --- |
| **القيمة** | لوحات + توقع + تنبيهات انزلاق صفقات | **Revenue Memory** + Decision Passport + قيمة بمرجع مصدر (`source_ref`) وليس أرقامًا وهمية |
| **الحوكمة** | RBAC + تدقيق CRM؛ كثير من الشركات بلا إطار حوكمة AI كامل | **approval-first**، لا إرسال بارد، مسارات `workflow_control_registry`، عقود observability |
| **البيانات** | تكامل CRM مركزي؛ 46%+ بلا بنية GTM موحدة | كتالوج JSONL→Postgres، قطع بـ `dual`، سياسة `engineering_cutover_policy` |
| **الترحيل** | عادة SaaS مُدار | **expand–contract**: JSONL مرجع + Postgres + مرآة `operational_event_streams` |
| **الامتثال** | SOC2/GDPR عند البائع | حزمة enterprise + PDPL/contactability + Trust pack قابلة للتخصيص |
| **الوكلاء** | Gen-4: orchestration (2026) | Agent runtime ببوابات؛ لا autonomy خارج approval |

**استنتاج CEO:** لا تنافس «لوحة أخرى». تنافس **شركة محكومة بالأدلة** — كل رقم مرتبط بمرجع، كل إجراء خارجي بموافقة، كل قطع تقني بإشارة عقد/بايلوت.

---

## أمر الجلسة الواحدة (تنفيذ في الريبو)

```bash
bash scripts/run_ceo_one_session_readiness.sh
```

### ماذا يفعل (بالترتيب)

| مرحلة | ماذا | مخرج |
| --- | --- | --- |
| A | `run_executive_weekly_checklist.sh` | proof pack مؤرّخ + سجل `weekly_ops_checklist.log` + مزامنة `last_checklist_run_iso` |
| B | `populate_kpi_baselines_platform_signals.py` | يملأ إشارات **منصة** (موثوقية، هامش نموذجي، حواجز صفرية) مع `source_ref` صريح — **لا يختلق CRM** |
| C | `run_pre_scale_gate_bundle.sh` | بوابات التوسع القطاعي |
| D | `verify_global_ai_transformation.sh` | تحقق برنامج التحول + control plane |
| E | `check_alembic_single_head.py` | رأس ترحيل واحد |
| F | `reliability_drills_scorecard.py` | بطاقة تدريبات |
| G | تقرير جلسة | `docs/transformation/evidence/session_report_YYYY-MM-DD.md` |

---

## بوابات الإنجاز (بدون أيام — فقط «تم / لم يتم»)

### بوابة 1 — تشغيل وإثبات (مؤسس / RevOps)

- [ ] تشغيل `run_ceo_one_session_readiness.sh` بنجاح
- [ ] تعبئة كل `snapshots.*` التي ما زالت `null` من CRM/المالية/التسليم في [`kpi_baselines.yaml`](../dealix/transformation/kpi_baselines.yaml)
- [ ] `updated_period_iso` و`source_ref` غير فارغ لكل قيمة غير null
- [ ] مراجعة [`ownership_matrix.yaml`](../dealix/transformation/ownership_matrix.yaml) وتحديث `executive_review.last_ownership_matrix_review_iso`
- [ ] بايلوت واحد موثّق عبر [`enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md`](enterprise_package/PILOT_EXECUTION_RUNBOOK_AR.md)

### بوابة 2 — جاهزية تقنية (منصة)

- [ ] `GLOBAL AI TRANSFORMATION: PASS` و`ENTERPRISE CONTROL PLANE: PASS`
- [ ] Alembic head واحد (`012` أو أحدث حسب `alembic heads`)
- [ ] كل صفوف [`02_gap_closure_matrix.md`](02_gap_closure_matrix.md) لها ملف [`evidence/gap_closure_*.md`](evidence/) + أرقام KPI حيث ينطبق

### بوابة 3 — قطع إنتاج (فقط بإشارة خارجية)

راجع [`ENGINEERING_CUTOVER_RUNBOOK_AR.md`](ENGINEERING_CUTOVER_RUNBOOK_AR.md):

1. `PROOF_LEDGER_BACKEND=dual` → مراقبة → `postgres`
2. `VALUE_LEDGER_BACKEND=dual` → مراقبة → `postgres`
3. `DEALIX_OPERATIONAL_STREAM_BACKEND=dual` عند الحاجة لـ audit
4. `OTEL_CONTRACT_TRACE_EXPORT=true` عند طلب عميل/امتثال

كل PR يحتوي: `external_signal:` و`contract_or_pilot_ref:`

### بوابة 4 — توسع فئة / إقليم

- [ ] `bash scripts/run_pre_scale_gate_bundle.sh` أخضر
- [ ] أدلة توسع في [`category_expansion_gates.yaml`](../dealix/transformation/category_expansion_gates.yaml)

### بوابة 5 — إيرادات و GTM (عند تغيير المسار التجاري)

```bash
bash scripts/verify_ceo_signal_readiness.sh revenue_os
```

---

## ماذا يُعبَّأ تلقائياً vs يدوياً

| مفتاح KPI | مصدر الجلسة الواحدة | مصدر المؤسس (إلزامي للحقيقة التجارية) |
| --- | --- | --- |
| `reliability_posture_score` | من `weekly_cross_os_snapshot` | مراجعة drills فعلية + SLO |
| `gross_margin_by_offer` | هامش من مدخلات اقتصاد **نموذجية** (موسومة في source_ref) | دفاتر مالية فعلية |
| حواجز العدّ (3 مفاتيح) | 0 بعد PASS التحقق (موسوم platform) | مراجعة حوادث إن وُجدت |
| `measured_customer_value_sar` | يبقى null | CRM + value ledger |
| `conversion_discovery_to_pilot` | يبقى null | CRM + بايلوت |
| `approval_cycle_time_hours` | يبقى null | approval_tickets |
| `governance_integrity_rate` | يبقى null | تقارير تحكم فعلية |

---

## ترتيب ذكي عند ضيق الوقت (داخل جلسة واحدة)

1. **أمر الجلسة الكامل** أعلاه (15–25 دقيقة حسب الجهاز).
2. إن فشل شيء: `bash scripts/verify_ceo_signal_readiness.sh transformation` فقط، ثم أصلح، ثم أعد الجلسة.
3. لا تفعّل cutover إنتاجي في نفس الجلسة إلا إذا كانت **الإشارة الخارجية** موجودة مسبقاً.

---

## وثائق مرتبطة

- تشغيل أسبوعي: [`EXECUTIVE_OPERATING_CHECKLIST_AR.md`](EXECUTIVE_OPERATING_CHECKLIST_AR.md)
- قطع تقني: [`ENGINEERING_CUTOVER_RUNBOOK_AR.md`](ENGINEERING_CUTOVER_RUNBOOK_AR.md)
- فهرس البرنامج: [`README.md`](README.md)
- سياسة الإشارة: [`engineering_cutover_policy.yaml`](../dealix/transformation/engineering_cutover_policy.yaml)

---

## تعريف «كل شيء جاهز»

- **تشغيلياً:** بايلوت موثّق، baselines بأرقام حقيقية للـ CRM/finance، weekly proof packs منتجة، ملاك محدثون.
- **تقنياً:** جميع بوابات التحقق خضراء، كتالوج JSONL إما Postgres أو مؤجّل بإشارة مسجّلة، gap evidence مكتملة.
- **تجارياً:** حزمة enterprise مخصّصة لعميل، لا تسويق عام تحت L4، لا upsell بلا proof.

هذا هو الفارق بين «ريبو مكتمل» و«شركة جاهزة للتوسع».
