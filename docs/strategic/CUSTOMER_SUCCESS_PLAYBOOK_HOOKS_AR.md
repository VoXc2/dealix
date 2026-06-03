# ربط نجاح العملاء بـ customer_readiness والبوابة (Playbook Hooks)

**الغرض:** تحويل محفزات CS الكلاسيكية إلى **مدخلات قابلة للقياس** تتوافق مع `compute_comfort_and_expansion` إلى أن تُربَط البوابة بالكامل بالبيانات الفعلية.

## المرجع البرمجي

- الدالة: `compute_comfort_and_expansion` في [auto_client_acquisition/customer_readiness/scores.py](../../auto_client_acquisition/customer_readiness/scores.py)
- استخدام تمهيدي من جواز القرار: `from_passport_meta` في نفس الملف
- استجابة الليد: حقل `customer_readiness` في `POST /api/v1/leads` (انظر [api/routers/leads.py](../../api/routers/leads.py))
- **Wave 13 — تجميع ذكاء CS:** [api/routers/customer_success_scores.py](../../api/routers/customer_success_scores.py) يجمع خمس درجات (`health`, `comfort`, `expansion_readiness`, `churn_risk`, `proof_maturity`) مع `is_estimate=True` لكل مكوّن — استخدمه كطبقة قراءة موحّدة فوق الجدول أدناه عند التكامل.
- وحدات مساعدة: [auto_client_acquisition/customer_success/churn_risk.py](../../auto_client_acquisition/customer_success/churn_risk.py), [auto_client_acquisition/customer_success/proof_maturity.py](../../auto_client_acquisition/customer_success/proof_maturity.py)

## جدول المحفزات → المدخلات → الحركة المقترحة

| محفز CS | أعراض | حقول `compute_comfort_and_expansion` المتأثرة | حركة تشغيل |
|---------|-------|-----------------------------------------------|-------------|
| **تبني ضعيف** | لا timeline حالة، لا next action | `has_status_timeline`, `has_next_action` | جلسة تمكين + تحديث بوابة الحالة |
| **ازدحام موافقات** | طلبات معلقة كثيرة | `pending_approvals` | تبسيط مسار الموافقة أو تفويض مؤقت |
| **دعم متأخر** | تذاكر مفتوحة، SLA مكسور | `open_support_tickets`, `avg_response_hours` | تصعيد تشغيلي + مراجعة قنوات |
| **قلة الإثبات** | لا Proof مسجّل | `proof_events_count`, `max_proof_level` | جدولة جلسة تسليم وProofEvent |
| **جاهزية توسعة** | عميل دافع + تسليم نشط | `payment_ok`, `delivery_sessions_active` | مراجعة `anti-waste` ثم عرض توسعة |
| **نافذة تجديد** | اقتراب نهاية العقد | (مستقبلاً: حقل صريح في Portal) | تشغيل playbook تجديد مرتبط بـ `expansion_readiness_score` |

## مؤشرات مركبة مقترحة

- **صحة الحساب (Heuristic):** `customer_comfort_score` — يزداد مع timeline، next action، Proof، واستجابة ≤24h؛ ينخفض مع الموافقات المعلقة والتذاكر.
- **جاهزية التوسعة:** `expansion_readiness_score` — يرتبط بـ Proof والدفع والجلسات النشطة؛ **لا تُستخدم وحدها** لعرض سعر (انظر `compute_pricing_power_score` والملاحظات في الكود).

## البوابة (Portal) — عند الجاهزية

1. عرض `comfort` و `expansion` مع `breakdown` للشفافية.
2. مصدر الحقيقة لـ `proof_events_count` و `max_proof_level` من `proof_ledger` (وليس تقديراً يدوياً).
3. ربط `avg_response_hours` بقنوات الدعم الفعلية (انظر فجوة Inbox في [DEALIX_CAPABILITY_GAP_MAP.md](../v10/DEALIX_CAPABILITY_GAP_MAP.md) §4).

## مراجع

- [ENTERPRISE_PILOT_TEMPLATE_AR.md](ENTERPRISE_PILOT_TEMPLATE_AR.md)
- [ENTERPRISE_OFFER_POSITIONING_AR.md](ENTERPRISE_OFFER_POSITIONING_AR.md)
