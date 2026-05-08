# Dealix — نموذج التشغيل التجاري الأعظم (مرجع استراتيجي)

هذا المستند يثبت **كيف تفكر Dealix كشركة تشغيل نمو** وليس كمجموعة endpoints.  
المعادلة المرجعية:

```text
Dealix = ذكاء الإيرادات + تنفيذ تشغيلي + محرك إثبات + نجاح عميل + طبقة ثقة + حلقة تعلّم
```

## السلسلة الذهبية

```text
إشارة → Lead → Decision Passport → إجراء معتمد → تسليم → Proof → توسعة → تعلّم
```

**قاعدة المنتج:** بدون Decision Passport لا يُنفَّذ إجراء خارجي (الحوكمة في Trust Plane + Approval Center).

واجهات API ثابتة:

- `GET /api/v1/decision-passport/golden-chain`
- `GET /api/v1/decision-passport/evidence-levels`
- كل استجابة `POST /api/v1/leads` تتضمن الآن `decision_passport` و `customer_readiness` (تقدير أولي إلى حين ربط البوابة ودفتر الـ Proof).

## المستويات الثمانية (خرائط تقريبية للكود الحالي)

| المحرك | مسارات / وحدات في الريبو |
|--------|---------------------------|
| Market Radar | `search_radar`, `radar_events`, أجزاء `revenue_os`, `full_ops_radar` |
| Lead Intelligence | `leads`, `prospect`, `data`, Lead Machine |
| Decision Engine | **Decision Passport** (`auto_client_acquisition/decision_passport/`) + سياسات ICP/BANT |
| Action & Approval | `approval_center`, `tool_guardrail_gateway`, `channel_policy_gateway` |
| Delivery OS | `delivery_os`, `delivery_factory`, `service_sessions` |
| Customer Portal | `customer_company_portal`, `customer_loop`, واجهة Next.js |
| Proof & Expansion | `proof_ledger`, `proof_to_market`, `case_study_engine`, `customer_success*` |
| Learning Flywheel | `self_improvement_os`, تقارير المؤسس، (توسيع لاحق بأحداث فعلية) |

## مستويات أدلة الـ Proof (L0–L5)

مُعرَّفة في `auto_client_acquisition/proof_engine/evidence.py` وواجهة `GET .../evidence-levels`.

- L0/L1: لا تسويق خارجي  
- L2–L3: خاص / مبيعات  
- L4: نشر عام بموافقة  
- L5: توسعة إيراد بعد التزام  

الدالة `assert_public_proof_allowed` تمنع النشر دون L4 + موافقة صريحة.

## Customer Comfort & Expansion Readiness

`auto_client_acquisition/customer_readiness/scores.py` — درجات 0–100 مشتقة من إشارات تشغيلية (قابلة للربط لاحقًا بجداول Portal و Proof).

## مبدأ بناء المنتج

لا تُضاف ميزة إلا إذا تخدم السلسلة الذهبية أو تقياسًا تشغيليًا (تحويل، تسليم، إثبات، احتفاظ).

## مراجع داخلية

- `docs/v10/DEALIX_CAPABILITY_GAP_MAP.md` — فجوات قدرات
- `AGENTS.md` — تشغيل الوكلاء السحابيين
- `dealix/registers/no_overclaim.yaml` — سجل عدم المبالغة

---

*آخر تحديث: يتزامن مع إصدار Decision Passport في مسار الـ leads.*
