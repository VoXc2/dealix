# ماذا يحدث بعد الرد الإيجابي / الحجز / تعبئة النموذج؟
## WhatsApp Post-Consent Entry Flow

> **الغرض:** يوضّح هذه الوثيقة المسار الكامل من لحظة ثبوت أساس الموافقة (`consent_basis`) حتى الوصول إلى `welcome → readiness_scan → service_recommendation`. يؤكد أن المسار لا يذهب أبدًا مباشرةً إلى الدفع.

---

## 1. أساس الموافقة — الشروط المبدئية

لا تُفتح جلسة واتساب إلا إذا تحقّق أحد الأسس التالية:

| أساس الموافقة (`consent_basis`) | المصدر الشائع |
|---|---|
| `explicit_optin` | زر اشتراك صريح في نموذج أو صفحة هبوط |
| `positive_reply` | رد إيجابي على إيميل تسويقي أو تواصل سابق |
| `booking` | حجز اجتماع عبر Calendly أو مكالمة |
| `form_submission` | تعبئة نموذج اهتمام على الموقع |
| `existing_client` | عميل حالي في علاقة تعاقدية قائمة |

**ممنوع مطلقًا:** `none`, `cold`, `scraped` — أي منها يوقف الإجراء فورًا ويفشل في الاختبارات.  
مرجع: `AGENTS.md §5`, `schemas/whatsapp_session.schema.json` (حقل `consent.consent_basis`).

---

## 2. المسار الكامل (خطوة بخطوة)

```
[حدث خارجي: رد إيميل / حجز / نموذج]
           │
           ▼
    ثبوت consent_basis
    تسجيل consent_timestamp + consent_source
           │
           ▼
    إنشاء جلسة WAS-xxxx
    status: active | dry_run: true | send_enabled: false
           │
           ▼
  تدفق: welcome_after_consent
  ─────────────────────────────
  القالب: welcome_after_consent
  "أهلًا {first_name}، نساعد شركات B2B…"
  خيارات:
    [1] ابدأ فحص الجاهزية    → readiness_scan
    [2] عندي سؤال           → ask_question
    [3] ما أعرف — اقترح علي → dont_know_suggest
           │
           ▼ (إذا اختار العميل [1] أو [3])
  تدفق: readiness_scan
  ─────────────────────────────
  5 أسئلة (lead_flow / followup_maturity / crm_data_readiness / reporting_maturity / urgency)
  → خطوة compute → ينتج client_assessment (CAS-xxxx)
           │
           ▼
  تدفق: service_recommendation
  ─────────────────────────────
  القالب: service_recommendation
  "جاهزية الإيراد: {score}/100 — الخطوة المقترحة: {product_name}"
  (evidence_level مذكور صراحةً)
  خيارات:
    [1] ابغى التفاصيل     → proposal_review (البوابة)
    [2] رتّبوا مكالمة     → book_call → human_handoff
    [3] ما أعرف — اقترح علي → dont_know_suggest
```

---

## 3. ما الذي يحدث في `proposal_review`؟

- **إخطار واتساب:** رسالة قصيرة + رابط البوابة `{portal_link_placeholder}` (لا ملف، لا سعر نهائي).
- **البوابة الآمنة:** تحتوي على ملخص العرض المبدئي.
- **السعر النهائي:** لا يُذكر في واتساب — يعتمد بعد موافقة المؤسس.
- **الانتقال التالي:** `opened_portal` أو `support`.

**لا يوجد مسار مباشر من الرد الإيجابي إلى الدفع.** المسار دائمًا:  
`consent → welcome → readiness → recommendation → proposal (portal) → [موافقة المؤسس] → payment_handoff`

---

## 4. مسار "ما أعرف — اقترح علي" (dont_know_suggest)

```
dont_know_suggest
  ↓ القالب: "الأغلب في وضعك يبدأ بفحص الجاهزية (مجاني، دقيقتين)…"
  خيارات:
    [1] نعم ابدأ الفحص  → readiness_scan
    [2] كلّمني بشري     → human_handoff
```

هذا التدفق متاح دائمًا من أي نقطة في المحادثة (ثابت عالمي في `flows.yaml`).

---

## 5. قواعد الحماية في هذا المسار

| القاعدة | التفعيل |
|---|---|
| لا رسالة واتساب قبل consent | يفشل في الاختبارات إذا `consent_basis = cold/none` |
| لا سعر نهائي في واتساب | `proposal_review` يشير للبوابة فقط |
| كل إرسال `send_enabled=false` | حتى الموافقة الصريحة |
| opt_out يوقف كل الرسائل فورًا | `consent.opt_out = true` → `status: opted_out` |
| human_handoff متاح دائمًا | في كل تدفق، كل خطوة |

---

## 6. مثال عملي — Digital Rise Agency

```
consent_basis: positive_reply
consent_source: email_reply
→ WAS-0001 (active, dry_run=true)
→ welcome_after_consent
→ readiness_scan (current_step: q3)
→ [pending: service_recommendation]
```

السجل: `data/whatsapp/sessions.jsonl` (WAS-0001).

---

## مراجع

- `data/whatsapp/flows.yaml` (تدفقات: `welcome_after_consent`, `dont_know_suggest`, `readiness_scan`, `service_recommendation`)
- `data/whatsapp/templates.yaml`
- `schemas/whatsapp_session.schema.json`
- `docs/whatsapp/EMAIL_REPLY_TO_WHATSAPP_HANDOFF_AR.md` (جسر الإيميل → واتساب)

---

*مصدر الحقيقة: `AGENTS.md` — لا يُعاد كتابة أساس السوق في `company_os/`.*
