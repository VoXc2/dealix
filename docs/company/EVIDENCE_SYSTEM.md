# Dealix Evidence System

Dealix لا تعتبر أي خدمة أو مخرجاً «جاهزاً» بدون **أدلة** قابلة للمراجعة في الريبو أو في التشغيل.

**السياق:** سوق واسع في السعودية ([Saudi Gazette](https://www.saudigazette.com.sa/article/658036))؛ لكن الفرصة التنافسية في **تحويل الطلب إلى تشغيل قابل للقياس** لا في «استخدام AI» وحده ([McKinsey — The State of AI](https://www.mckinsey.com/capabilities/quantumblack/our-insights/the-state-of-ai/)).

---

## أنواع الأدلة

| النوع | ماذا يثبت؟ | أين يُوجد عادةً؟ |
|--------|------------|------------------|
| **1. Strategic Evidence** | التموضع، ICP، North Star، المبادئ | `docs/company/POSITIONING.md`، `ICP.md`، `NORTH_STAR_METRICS.md`، `MISSION_VISION.md` |
| **2. Offer Evidence** | وعد، سعر، مدة، مخرجات، استثناءات، KPI | `docs/services/<service>/offer.md` + `scope.md` |
| **3. Delivery Evidence** | تسليم بدون ارتجال | `docs/delivery/*`، `delivery_checklist.md` لكل خدمة |
| **4. Product Evidence** | الكود يدعم التسليم | `auto_client_acquisition/*_os/`، اختبارات `tests/` |
| **5. Governance Evidence** | أمان وثقة وPDPL | `docs/governance/*`، [`verify_governance_rules.py`](../../scripts/verify_governance_rules.py) |
| **6. Demo Evidence** | إقناع قبل الشراء | [`demos/`](../../demos/)، [`DEMO_READINESS.md`](../delivery/DEMO_READINESS.md) |
| **7. Sales Evidence** | إغلاق واعتراضات | `docs/sales/*` |
| **8. Proof Evidence** | أثر بعد التنفيذ | `proof_pack_template.md`، [`templates/proof_pack.md`](../templates/proof_pack.md)، `reporting_os` |

---

## قاعدة الجاهزية (Official)

خدمة **رسمية (Sellable)** فقط إذا اجتمعت:

- **Service Readiness Score ≥ 85** (من [`service_readiness`](../../auto_client_acquisition/delivery_os/service_readiness.py) + مجلد كامل يمرّ [`verify_service_files.py`](../../scripts/verify_service_files.py)).
- **Governance:** وثائق إلزامية تمرّ التحقق؛ معيار يدوي مستهدف **≥ 90** — انظر [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md).
- **Demo:** حزمة demo للخدمات الثلاث الأولى ضمن [`demos/`](../../demos/) عند Gate 5.
- **Proof pack template** + **QA checklist** لكل خدمة في `docs/services/<service>/`.
- **Sales assets** لـ Gate 6.
- **Product module** يدعم التسليم (Gate 3 MVP في [`verify_dealix_ready.py`](../../scripts/verify_dealix_ready.py)).

ما لا يستوفِ الأدلة = **Beta** أو **Not Ready** — انظر [`SELLABILITY_POLICY.md`](SELLABILITY_POLICY.md) و[`SERVICE_READINESS_MATRIX.md`](SERVICE_READINESS_MATRIX.md).

---

## روابط

- بوابات المراحل: [`DEALIX_STAGE_GATES_AR.md`](DEALIX_STAGE_GATES_AR.md)
- نواة التشغيل: [`DEALIX_OPERATING_KERNEL.md`](DEALIX_OPERATING_KERNEL.md) · [`DECISION_RULES.md`](DECISION_RULES.md)
- التراكم بعد كل مشروع: [`COMPOUNDING_SYSTEM.md`](COMPOUNDING_SYSTEM.md) · [`PROJECT_SUCCESS_SCORECARD.md`](PROJECT_SUCCESS_SCORECARD.md) · [`../templates/LEARNING_LOOP.md`](../templates/LEARNING_LOOP.md)
- المعيار الثماني: [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md) · تعريف الإنجاز: [`DEFINITION_OF_DONE.md`](DEFINITION_OF_DONE.md)
- نظام القرار: [`DECISION_OPERATING_SYSTEM.md`](DECISION_OPERATING_SYSTEM.md) · [`DECISION_RULES.md`](DECISION_RULES.md) · ما لا تُباع بعد: [`DO_NOT_SELL_YET.md`](DO_NOT_SELL_YET.md)
- سجل التشغيل: [`OPERATING_LEDGER.md`](OPERATING_LEDGER.md) · [`CONTROL_PLANE.md`](CONTROL_PLANE.md) · [`STOP_DOING.md`](STOP_DOING.md)
- التنفيذ المغلق الحلقة: [`CLOSED_LOOP_EXECUTION.md`](CLOSED_LOOP_EXECUTION.md) · [`../operations/REQUEST_INTAKE_SYSTEM.md`](../operations/REQUEST_INTAKE_SYSTEM.md)
- نموذج رأس المال التراكمي: [`DEALIX_CAPITAL_MODEL.md`](DEALIX_CAPITAL_MODEL.md) · [`../ledgers/CAPITAL_LEDGER.md`](../ledgers/CAPITAL_LEDGER.md)
- نموذج القدرات التشغيلية: [`CAPABILITY_OPERATING_MODEL.md`](CAPABILITY_OPERATING_MODEL.md) · [`CAPABILITY_MATURITY_MODEL.md`](CAPABILITY_MATURITY_MODEL.md)
- لوحة القيادة اليدوية: [`../../DEALIX_READINESS.md`](../../DEALIX_READINESS.md)
- التحقق الآلي: [`../../scripts/verify_dealix_ready.py`](../../scripts/verify_dealix_ready.py)
