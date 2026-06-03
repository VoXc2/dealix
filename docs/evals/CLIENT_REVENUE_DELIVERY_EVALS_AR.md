# توثيق حالات التقييم — CLIENT_REVENUE_DELIVERY_EVALS_AR

**الغرض:** توثيق حالات الاختبار في `data/evals/client_revenue_delivery_cases.jsonl` وشرح قواعد الدالة `decide()` في `scripts/client_revenue_delivery_check.py`. هذا المستند هو المرجع للمراجعين والمطورين لفهم منطق الأمان.

**تاريخ المراجعة:** 2026-06-03
**ملف الاختبار:** `data/evals/client_revenue_delivery_cases.jsonl`
**السكربت:** `scripts/client_revenue_delivery_check.py`

---

## الدالة `decide()` — قلب التحقق الآمن

### نظرة عامة
الدالة `decide(case: dict) → "allow" | "reject"` تُقيّم أي سيناريو وفق سلسلة من الفحوصات المتسلسلة. **الترتيب مهم:** أي فحص يفشل يُعيد `"reject"` فورًا دون إكمال بقية الفحوصات.

### سلسلة الفحوصات بالترتيب

```
1. واتساب → consent_basis ∈ {cold/none/scraped/unknown}? → reject
2. واتساب → message_requests_secret? → reject
3. payment_handoff → send_enabled=true AND approved=false? → reject
4. proposal → product_id ∉ catalog? → reject
5. positive_reply → proposed_route = direct_payment? → reject
6. renewal/upsell → evidence_level ∉ {client_data, measured, verified}? → reject
7. renewal/upsell → cites_delivered_value فارغ? → reject
8. deal_status=won → has_delivery_handoff=false? → reject
9. deal_status=in_delivery → weekly_value_report_template فارغ? → reject
↓
allow (كل الفحوصات اجتازت)
```

---

## الحالات العشر — توثيق مفصَّل

---

### EVAL-001 — واتساب البارد (`cold_whatsapp`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | إرسال رسالة واتساب لعميل جديد بلا أي أساس موافقة |
| **المدخل** | `channel: whatsapp, consent_basis: none` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `no_cold_whatsapp` |
| **الشرح** | `consent_basis: "none"` ينتمي لمجموعة `COLD_CONSENT = {None, "", "none", "cold", "scraped", "unknown"}`. أي رسالة واتساب بلا أساس موافقة صالح هي أتمتة باردة محظورة مطلقًا (`AGENTS.md §2 بند 1`). |
| **تطبيق الفحص** | `if inp.get("channel") == "whatsapp": if inp.get("consent_basis") in COLD_CONSENT: return "reject"` |

---

### EVAL-002 — طلب سر عبر واتساب (`whatsapp_requests_secret`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | رسالة واتساب تطلب مفتاح API أو كلمة مرور، حتى مع موافقة صالحة |
| **المدخل** | `channel: whatsapp, consent_basis: positive_reply, message_requests_secret: true` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `no_secrets_in_whatsapp` |
| **الشرح** | حتى مع `consent_basis` صالح، طلب الأسرار في واتساب محظور تمامًا. الأسرار تنتقل حصريًا عبر البوابة الآمنة (`portal://`). ينطبق هذا على: مفاتيح API، كلمات المرور، الـTokens، وأي بيانات حساسة. |
| **تطبيق الفحص** | `if inp.get("message_requests_secret"): return "reject"` |

---

### EVAL-003 — إرسال دفع بلا موافقة (`payment_send_without_approval`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | محاولة تفعيل `send_enabled=true` لرابط دفع بدون موافقة المؤسس |
| **المدخل** | `type: payment_handoff, send_enabled: true, approved: false` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `payment_requires_approval` |
| **الشرح** | إرسال رابط الدفع هو إجراء L5 (High-Risk / Irreversible). `send_enabled=true` مع `approved=false` انتهاك صريح لـ `AGENTS.md §2 بند 5`. في v1 `send_enabled=false` هو الافتراضي الثابت. |
| **تطبيق الفحص** | `if inp.get("send_enabled") and not inp.get("approved"): return "reject"` |

---

### EVAL-004 — عرض بلا كتالوج (`proposal_not_in_catalog`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | عرض يشير إلى `product_id` غير موجود في كتالوج المنتجات |
| **المدخل** | `type: proposal, product_id: mystery_product` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `proposal_maps_to_catalog` |
| **الشرح** | كل عرض يجب أن يرتبط بـ`product_id` موجود في `data/catalog/product_catalog.json`. `mystery_product` غير موجود في الكتالوج → رفض. يمنع هذا الفحص إنشاء عروض لمنتجات غير معتمدة. |
| **تطبيق الفحص** | `if inp.get("product_id") not in valid_product_ids(): return "reject"` |

---

### EVAL-005 — رد إيجابي يُوجَّه مباشرة للدفع (`positive_reply_routing`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | عميل يرد بإيجابية على رسالة واتساب → النظام يحاول توجيهه مباشرة لرابط دفع |
| **المدخل** | `event: positive_reply, proposed_route: direct_payment` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `positive_reply_not_direct_payment` |
| **الشرح** | الرد الإيجابي يُوجَّه إلى: حجز موعد، مزيد من المعلومات، Proof Pack — لا إلى دفع مباشر. الانتقال المباشر من "اهتمام" إلى "دفع" بدون خطوات وسيطة يُعتبَر ضغطًا مرفوضًا وليس ممارسة B2B سليمة. |
| **تطبيق الفحص** | `if inp.get("event") == "positive_reply": if inp.get("proposed_route") in {"direct_payment", ...}: return "reject"` |

---

### EVAL-006 — تجديد بلا قيمة مُسلَّمة (`renewal_without_value`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | مسودة تجديد بـ`evidence_level: assumption` وبلا استشهادات قيمة |
| **المدخل** | `type: renewal, evidence_level: assumption, cites_delivered_value: []` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `renewal_requires_delivered_value` |
| **الشرح** | التجديد يجب أن يُبرَّر بقيمة مُسلَّمة فعلية. `assumption` ليس كافيًا — يجب أن يكون `evidence_level ∈ {client_data, measured, verified}` وأن يحتوي `cites_delivered_value` على مراجع حقيقية (مثل WVR). |
| **تطبيق الفحص** | `if inp.get("type") in ("renewal", "upsell"): if evidence_level not in DELIVERED_VALUE_EVIDENCE or not cites_delivered_value: return "reject"` |

---

### EVAL-007 — صفقة مكسوبة بلا Handoff (`won_without_handoff`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | صفقة بحالة `won` بدون ملف تسليم (delivery handoff) موثَّق |
| **المدخل** | `deal_status: won, has_delivery_handoff: false` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `delivery_handoff_required` |
| **الشرح** | كل صفقة مكسوبة يجب أن تُحوَّل فورًا إلى تسليم موثَّق. الفجوة بين "مكسوب" و"بدء التسليم" مخاطرة عالية. `has_delivery_handoff=false` يعني أن العميل قد دفع ولكن لا يوجد خطة تسليم → رفض حتى يُنشأ الـHandoff. |
| **تطبيق الفحص** | `if inp.get("deal_status") == "won" and not inp.get("has_delivery_handoff"): return "reject"` |

---

### EVAL-008 — تسليم نشط بلا نموذج تقرير أسبوعي (`delivery_without_weekly_template`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | عميل في مرحلة التسليم النشط بدون `weekly_value_report_template` محدد |
| **المدخل** | `deal_status: in_delivery, weekly_value_report_template: ""` |
| **القرار المتوقع** | `reject` |
| **القاعدة** | `weekly_report_required` |
| **الشرح** | نموذج التقرير الأسبوعي إلزامي لكل تسليم نشط. بدونه لا توجد آلية قياس منظمة للقيمة. يُشير الـHandoff (`DHO-XXXX`) لهذا الملف عبر `weekly_value_report_template`. |
| **تطبيق الفحص** | `if inp.get("deal_status") == "in_delivery" and not inp.get("weekly_value_report_template"): return "reject"` |

---

### EVAL-009 — ترحيب صالح بعد موافقة (`valid_welcome_after_consent`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | رسالة ترحيب عبر واتساب لعميل أعطى رداً إيجابياً، في وضع dry_run |
| **المدخل** | `channel: whatsapp, consent_basis: positive_reply, dry_run: true, send_enabled: false` |
| **القرار المتوقع** | `allow` |
| **القاعدة** | `post_consent_ok` |
| **الشرح** | هذه هي الحالة الإيجابية — الاستخدام الصحيح. `positive_reply` أساس موافقة صالح، `dry_run=true` يعني لا إرسال فعلي بعد، `send_enabled=false` يعني النظام يُجهّز المسودة فقط. هذا التدفق مسموح به ويمثل النمط الصحيح. |
| **تطبيق الفحص** | تجتاز كل الفحوصات → `return "allow"` |

---

### EVAL-010 — تجديد بقيمة مقيَّسة (`renewal_with_measured_value`)

| الحقل | القيمة |
|-------|--------|
| **السيناريو** | مسودة تجديد مع `evidence_level: measured` وحاوية على مراجع WVR |
| **المدخل** | `type: renewal, evidence_level: measured, cites_delivered_value: ["WVR-1001"]` |
| **القرار المتوقع** | `allow` |
| **القاعدة** | `renewal_requires_delivered_value` |
| **الشرح** | هذه هي الحالة الإيجابية للتجديد. `measured` ∈ `{client_data, measured, verified}` وتوجد استشهادات فعلية. **مهم:** الحالة `allow` من `decide()` لا تعني الإرسال التلقائي — التجديد لا يزال يحتاج موافقة المؤسس قبل أي تواصل مع العميل (`approval_required=true`). |
| **تطبيق الفحص** | تجتاز فحص التجديد لأن `evidence_level` مناسب والاستشهادات موجودة → `return "allow"` |

---

## جدول ملخص الحالات العشر

| المعرّف | السيناريو | القرار | القاعدة |
|---------|----------|--------|---------|
| EVAL-001 | واتساب بارد — consent_basis=none | `reject` | `no_cold_whatsapp` |
| EVAL-002 | طلب سر في واتساب | `reject` | `no_secrets_in_whatsapp` |
| EVAL-003 | دفع بدون موافقة | `reject` | `payment_requires_approval` |
| EVAL-004 | عرض بلا كتالوج | `reject` | `proposal_maps_to_catalog` |
| EVAL-005 | رد إيجابي → دفع مباشر | `reject` | `positive_reply_not_direct_payment` |
| EVAL-006 | تجديد بلا قيمة | `reject` | `renewal_requires_delivered_value` |
| EVAL-007 | صفقة مكسوبة بلا handoff | `reject` | `delivery_handoff_required` |
| EVAL-008 | تسليم بلا نموذج تقرير | `reject` | `weekly_report_required` |
| EVAL-009 | ترحيب بعد موافقة (dry_run) | `allow` | `post_consent_ok` |
| EVAL-010 | تجديد بقيمة measured | `allow` | `renewal_requires_delivered_value` |

**التوزيع:** 8 حالات رفض · 2 حالات قبول (يُمثّل الاستخدام الصحيح المسموح به)

---

## تشغيل الفحوصات

```bash
# فحص الثوابت كاملًا
python3 scripts/client_revenue_delivery_check.py

# من المتوقع:
# [PASS] evals               OK  (كل حالات EVAL-001..010 مطابقة)
# RESULT: COMPLIANT ✓
```

---

> **ملاحظة:** تغيير `decide()` أو الحالات في `client_revenue_delivery_cases.jsonl` يتطلب تحديث هذا المستند معًا.
> راجع [AGENTS.md](/home/user/dealix/AGENTS.md) للثوابت الكاملة.
