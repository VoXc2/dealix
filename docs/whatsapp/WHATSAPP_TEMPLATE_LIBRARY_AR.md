# مكتبة القوالب (Template Library)
## توثيق templates.yaml وشروط الاستخدام

> **الغرض:** يوثّق هذا المستند كامل مكتبة قوالب واتساب المعرّفة في `data/whatsapp/templates.yaml` — أسماء القوالب، متغيراتها، خياراتها، والقواعد التي تحكم استخدامها.  
> **تذكير:** خيار "ما أعرف — اقترح علي" **إلزامي** في كل بطاقة توصية/تقييم.

---

## 1. ثوابت المكتبة (من templates.yaml)

```yaml
version: 1
locale_default: ar
forbidden:
  - cold_outreach            # لا قالب بارد أبدًا
  - request_api_key          # لا طلب مفاتيح في واتساب
  - send_payment_link_auto   # لا إرسال تلقائي لروابط الدفع
mandatory_option:
  label: "ما أعرف — اقترح علي"
  value: "dont_know_suggest"
```

**يُمنع استخدام أي قالب لا يوجد في هذا الملف.** القوالب المخصَّصة تُضاف بعد مراجعة الحوكمة.

---

## 2. القوالب الـ12 — جدول مرجعي

| اسم القالب | يُستخدم في تدفق | متغيرات الجسم | خيارات |
|---|---|---|---|
| `welcome_after_consent` | `welcome_after_consent` | `{first_name}` | ابدأ فحص / سؤال / ما أعرف |
| `dont_know_suggest` | `dont_know_suggest` | — | ابدأ الفحص / كلّمني بشري |
| `readiness_intro` | `readiness_scan` | — | يلا نبدأ |
| `service_recommendation` | `service_recommendation` | `{revenue_readiness}`, `{followup_maturity}`, `{recommended_product_name}`, `{reason}`, `{evidence_level}` | تفاصيل / مكالمة / ما أعرف |
| `proposal_review_notice` | `proposal_review` | `{portal_link_placeholder}` | فتحت البوابة / أحتاج مساعدة |
| `proof_pack_notice` | `proof_pack_review` | `{portal_link_placeholder}` | اطّلعت / عندي سؤال |
| `permission_request_notice` | `permission_request` | `{portal_link_placeholder}` | أعطيت الصلاحية / ليش؟ / ما أعرف |
| `payment_handoff_notice` | `payment_handoff` | — | تمام / كلّمني بشري |
| `onboarding_checklist_notice` | `onboarding_checklist` | — | ببدأ الآن / أحتاج مساعدة |
| `weekly_report_notice` | `weekly_report` | `{week_of}`, `{headline}`, `{portal_link_placeholder}` | اطّلعت / ناقشني |
| `support_escalation` | `support_escalation` | — | كتبت المطلوب |
| `renewal_notice` | `renewal_upsell` | `{delivered_value}` | اشرح لي / ليس الآن |
| `opt_out_ack` | أي تدفق | `{first_name}` | (لا خيارات) |

---

## 3. وصف تفصيلي للقوالب الرئيسية

### welcome_after_consent — نقطة الدخول

```
أهلًا {first_name} 👋 معك Dealix.
شكرًا إنك تواصلت معنا. نساعد شركات B2B بالسعودية
توقف تسرب الإيراد وتنظّم المتابعة.
تحب نبدأ بفحص جاهزية سريع (٥ أسئلة)
أو عندك سؤال محدد؟
─────────────────────
[1] ابدأ فحص الجاهزية
[2] عندي سؤال
[3] ما أعرف — اقترح علي  ✅ إلزامي
```

**ملاحظة:** كل رسالة ترحيب تفترض وجود `consent_basis` موثّق.

---

### service_recommendation — عرض النتائج

```
بناءً على ردودك:
• جاهزية الإيراد: {revenue_readiness}/100
• نضج المتابعة: {followup_maturity}/100
الخطوة المقترحة: {recommended_product_name}.
السبب: {reason}. (مستوى الدليل: {evidence_level})
تحب التفاصيل أو نرتّب لك مكالمة؟
─────────────────────
[1] ابغى التفاصيل
[2] رتّبوا مكالمة
[3] ما أعرف — اقترح علي  ✅ إلزامي
```

**مهم:** لا يُذكر سعر في هذا القالب. السعر في البوابة فقط.

---

### renewal_notice — التجديد/الترقية

```
مرّ شهر تقريبًا 👏
بناءً على القيمة اللي تحققت ({delivered_value})
نقترح خطوة وحدة بسيطة للاستمرار/التوسعة.
نشرح لك؟ (بدون أي ضغط)
─────────────────────
[1] اشرح لي
[2] ليس الآن
```

**قيد الحوكمة:** `{delivered_value}` يجب أن يستند إلى `evidence_level ∈ {client_data, measured, verified}`. لا تجديد بدون قيمة مُسلَّمة فعلية.

---

## 4. قواعد استخدام القوالب

| القاعدة | التطبيق |
|---|---|
| كل القوالب `requires_consent: true` | لا إرسال قبل `consent_basis` موثّق |
| "ما أعرف — اقترح علي" إلزامي في كل توصية | في `service_recommendation`, `permission_request`, `proposal_review_notice`, `proof_pack_notice` |
| لا متغيرات بها أسرار | `{portal_link_placeholder}` ليس رابطًا حقيقيًا في القالب — يُبدَّل وقت الإرسال |
| كل إرسال `send_enabled=false` افتراضيًا | لا إرسال تلقائي حتى الموافقة |
| `opt_out_ack` لا يحمل خيارات | بعد الانسحاب لا تفاعل إضافي |

---

## 5. إضافة قالب جديد

لإضافة قالب إلى المكتبة:
1. تعريف القالب في `data/whatsapp/templates.yaml`
2. ربطه بتدفق في `data/whatsapp/flows.yaml`
3. التأكد من وجود `is_dont_know: true` في الخيارات (إذا كان قالب توصية)
4. اجتياز فحص `scripts/client_revenue_delivery_check.py`

---

## مراجع

- `data/whatsapp/templates.yaml` (مصدر الحقيقة)
- `data/whatsapp/flows.yaml`
- `AGENTS.md §3` (الثوابت: "ما أعرف دائمًا متاح")
- `docs/whatsapp/WHATSAPP_UX_POLICY_AR.md` (سياسة UX)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
