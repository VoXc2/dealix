# نظام واتساب للعميل — نظرة شاملة (بعد الموافقة)
## WhatsApp Client OS — Overview (Post-Consent)

> **الغرض:** هذا المستند هو نقطة دخول WhatsApp Client OS في Dealix. يغطي المبادئ الحاكمة، قنوات التفاعل، ملخص الـ13 تدفقًا المعرّفة في `data/whatsapp/flows.yaml`، والحدود بين قناة واتساب والبوابة الآمنة.
> **ملاحظة:** واتساب يعمل **بعد الموافقة فقط**. لا رسائل باردة أبدًا. انظر `AGENTS.md §5`.

---

## 1. المبادئ الأساسية

| المبدأ | التطبيق العملي |
|---|---|
| **الموافقة أولًا** | `consent_basis` يجب أن يكون أحد: `explicit_optin`, `positive_reply`, `booking`, `form_submission`, `existing_client` |
| **لا أسرار في واتساب** | مفاتيح API، كلمات مرور، روابط موقّعة — حصرًا عبر البوابة الآمنة (`portal://...`) |
| **لا سعر نهائي** | السعر النهائي يعتمد فقط بعد موافقة المؤسس + تسليم بشري (L5) |
| **لا رابط دفع تلقائي** | كل دفع يمر بموافقة المؤسس قبل الإرسال اليدوي |
| **إلزامية "ما أعرف — اقترح علي"** | هذا الخيار يظهر في كل بطاقة توصية/تقييم |
| **التسليم البشري دائمًا متاح** | زر واحد يوصل لبشري في أي لحظة |
| **dry_run=true افتراضيًا** | كل إجراء خارجي يبقى في وضع المحاكاة حتى الموافقة الصريحة |

---

## 2. قنوات التفاعل

```
المصدر الخارجي (إيميل، نموذج، حجز)
        │
        ▼ [consent_basis موثّق]
  واتساب (بعد الموافقة)
        │
        ├─→ بطاقات الإجراء (Action Cards)      ← تفاعل هيكلي قصير
        ├─→ الإخطارات                           ← تنبيه + رابط البوابة
        └─→ التسليم البشري                      ← في أي وقت، لأي سبب

  البوابة الآمنة (portal://)
        │
        ├─→ الأسرار/الصلاحيات
        ├─→ ملفات العروض/Proof Pack
        └─→ الدفع (بعد الموافقة)
```

**قاعدة الحدود:** أي شيء يتضمن ملفات، أسرار، أسعار نهائية، أو دفع = البوابة لا واتساب.

---

## 3. ملخص الـ13 تدفقًا (flows.yaml)

| # | معرّف التدفق (`id`) | المدخل | البوابة | الوصف المختصر |
|---|---|---|---|---|
| 1 | `welcome_after_consent` | نقطة الدخول (`entry: true`) | — | رسالة ترحيب + 3 خيارات أولية |
| 2 | `dont_know_suggest` | من أي تدفق | — | يقترح فحص الجاهزية لمن يتردد |
| 3 | `readiness_scan` | من welcome أو dont_know | — | 5 أسئلة تنتج `client_assessment` |
| 4 | `service_recommendation` | من readiness_scan | — | عرض المنتج المناسب + `evidence_level` |
| 5 | `proposal_review` | من service_recommendation | `portal` | إخطار بالعرض المبدئي (السعر في البوابة) |
| 6 | `proof_pack_review` | بعد الاتفاق المبدئي | `portal` | إخطار بـProof Pack (كل رقم له مستوى دليل) |
| 7 | `permission_request` | قبل التشخيص | `portal` | طلب صلاحية قراءة فقط (لا مفاتيح في واتساب) |
| 8 | `secure_portal_link` | متى احتاج رابطًا | `approval` | إصدار رابط بوابة منتهي الصلاحية + MFA |
| 9 | `payment_handoff` | بعد قبول العرض | `human_handoff` | إشعار بخطوة الدفع (لا إرسال تلقائي) |
| 10 | `onboarding_checklist` | بعد إتمام الصفقة | `portal` | checklist أول 14 يوم في البوابة |
| 11 | `weekly_report` | أسبوعيًا للعملاء | `portal` | إخطار بتقرير القيمة الأسبوعي |
| 12 | `support_escalation` | في أي وقت | `human_handoff` | تحويل لبشري + إنشاء `support_ticket` |
| 13 | `renewal_upsell` | عند استحقاق التجديد | `approval` | اقتراح التجديد/التوسعة (بدليل فعلي) |

**الثوابت العالمية لكل التدفقات:**
- `dry_run: true`
- `send_enabled: false`
- `dont_know_suggest` + `human_handoff` + `opt_out` متاحة دائمًا

---

## 4. دورة حياة الجلسة (Session Lifecycle)

```
consent_basis موثّق
      │
      ▼
  WAS-xxxx [status: active]
      │
      ├─ تقدّم في تدفق   → status: active
      ├─ انتظار موافقة   → status: awaiting_approval
      ├─ تسليم بشري      → status: handoff
      ├─ الانسحاب        → status: opted_out (إيقاف فوري لكل الرسائل)
      └─ انتهاء          → status: closed
```

حقول السكيمة الرئيسية: `id` (نمط `WAS-*`)، `consent.consent_basis`، `consent.opt_out`، `current_flow`، `current_step`، `status`، `dry_run`، `send_enabled`.  
مرجع: `schemas/whatsapp_session.schema.json`.

---

## 5. الحدود مع البوابة الآمنة

| يحدث في واتساب | يحدث في البوابة فقط |
|---|---|
| أسئلة الفحص (نص قصير) | رفع الملفات |
| الخيارات المرقّمة | الأسرار وكلمات المرور |
| الإخطارات والتنبيهات | تفاصيل العرض النهائي والسعر |
| طلب التسليم البشري | روابط الدفع (بعد موافقة المؤسس) |
| خيار opt_out | منح الصلاحيات (read_only فقط) |

---

## 6. الحالات الشاهدة (أمثلة حقيقية)

**TrainMe KSA** — `form_submission` ← `WAS-0002` ← تقييم `CAS-0002` ← عرض `PROP-1001` (ينتظر موافقة)  
**Digital Rise Agency** — `positive_reply` ← `WAS-0001` ← عرض مُعتمد `PROP-1002` ← Proof Pack `PRF-1001` ← تسليم دفع `PAY-1001`

---

## 7. مراجع

- سكيمة الجلسة: `schemas/whatsapp_session.schema.json`
- التدفقات: `data/whatsapp/flows.yaml`
- القوالب: `data/whatsapp/templates.yaml`
- عقد الحوكمة: `AGENTS.md`
- صلاحيات الوكلاء: `company_os/governance/agent_permissions.md`

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
