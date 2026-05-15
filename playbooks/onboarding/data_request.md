# العربية

# طلب البيانات — Layer 10 / مرحلة التهيئة

**المالك:** قائد التسليم (Delivery Lead)
**الجمهور:** عضو الفريق الذي يجمع بيانات العميل لبدء التسليم
**المراجع:** `clients/_TEMPLATE/02_data_request.md` · `docs/PILOT_DELIVERY_SOP.md` · `playbooks/onboarding/kickoff.md` · `playbooks/onboarding/access_request.md`

> الغرض: طلب موحّد لأقل قدر من البيانات اللازم للتسليم — بحماية كاملة لبيانات العميل ووفق نظام حماية البيانات (PDPL).

## 1. متى يُستخدم هذا الدليل

بعد اجتماع الانطلاق مباشرة وقبل اليوم 1 من التسليم. لا يبدأ التسليم قبل استلام البيانات الأساسية.

## 2. مبدأ الحد الأدنى من البيانات

اطلب فقط ما يلزم للمخرَج الحالي. كل حقل إضافي يجب أن يكون له سبب تسليمي واضح. البيانات الزائدة عبء لا قيمة.

## 3. البيانات الأساسية المطلوبة

| البند | الصيغة | السبب |
|---|---|---|
| تصدير خط الأنابيب | CSV / Excel | تقييم الحسابات وترتيب الفرص |
| وصف العميل المثالي | نص | تركيز الاستهداف |
| 3 صفقات حالية | نص أو صفوف | فهم المراحل والتحديات |
| صوت العلامة (أمثلة رسائل) | نص | صياغة مسودات تشبه العميل |

## 4. خطوات الطلب (خطوة بخطوة)

1. أرسل نموذج طلب البيانات من `clients/_TEMPLATE/02_data_request.md`.
2. وضّح صيغة كل ملف والقناة الآمنة لرفعه.
3. اطلب من العميل إخفاء البيانات الشخصية الحساسة قبل الإرسال إن أمكن.
4. أكّد الاستلام كتابياً وافحص اكتمال الملفات.
5. خزّن البيانات في مجلد العميل المقيّد الوصول.
6. سجّل حدث الاستلام في سجل حوكمة العميل.

## 5. القواعد الحاكمة (Non-negotiables)

- لا كشط ولا جمع بيانات من مصادر خارجية — العميل وحده مصدر البيانات.
- لا تطلب أرقام تواصل أو هويات وطنية دون سبب تسليمي موثق.
- البيانات تُستخدم لهذا الارتباط فقط ولا تُشارَك خارجياً.
- تُحذف أو تُعاد البيانات عند الإنهاء وفق PDPL.
- لا أسماء عملاء حقيقية تُنقَل إلى ملفات المستودع العامة.

## 6. معايير القبول (قائمة الجاهزية)

- [ ] كل البنود الأساسية الأربعة مُستلمة ومكتملة.
- [ ] الملفات بصيغة قابلة للقراءة وخالية من التلف.
- [ ] DPA موقّعة قبل أي نقل بيانات.
- [ ] حدث الاستلام مسجَّل في `governance_events.md`.
- [ ] الوصول مقيّد على فريق التسليم فقط.

## 7. المقاييس

- زمن استلام البيانات: من الطلب إلى الاكتمال (الهدف ≤ 24 ساعة).
- اكتمال البيانات من المحاولة الأولى.
- نسبة الارتباطات التي بدأت بكامل البيانات الأساسية.

## 8. خطافات المراقبة (Observability)

- سجّل حالة البيانات: `requested` / `received` / `validated`.
- علّم أي ملف ناقص وتاريخ المتابعة.
- مراجعة أسبوعية لزمن استلام البيانات.

## 9. إجراء التراجع (Rollback)

إذا وصلت بيانات ناقصة أو تالفة:
1. تواصل مع العميل خلال 4 ساعات بطلب محدد وواضح.
2. لا تبدأ اليوم 1 من التسليم ببيانات ناقصة.
3. إذا اكتُشف نقل غير ضروري لبيانات شخصية، احذفها فوراً وسجّل الحادثة.

# English

# Data Request — Layer 10 / Onboarding Stage

**Owner:** Delivery Lead
**Audience:** Team member collecting client data to start delivery
**References:** `clients/_TEMPLATE/02_data_request.md` · `docs/PILOT_DELIVERY_SOP.md` · `playbooks/onboarding/kickoff.md` · `playbooks/onboarding/access_request.md`

> Purpose: a standard request for the minimum data needed to deliver — with full protection of client data and compliance with the PDPL.

## 1. When to use this playbook

Immediately after the Kick-off meeting and before Day 1 of delivery. Delivery does not start before core data is received.

## 2. Minimum-data principle

Request only what the current deliverable needs. Every extra field must have a clear delivery reason. Excess data is a liability, not value.

## 3. Core data required

| Item | Format | Reason |
|---|---|---|
| Pipeline export | CSV / Excel | Account scoring and opportunity ranking |
| Ideal client description | Text | Targeting focus |
| 3 current deals | Text or rows | Understand stages and challenges |
| Brand voice (sample messages) | Text | Draft messages that sound like the client |

## 4. Request steps (step by step)

1. Send the data request form from `clients/_TEMPLATE/02_data_request.md`.
2. Specify each file format and the secure channel for upload.
3. Ask the client to redact sensitive PII before sending where possible.
4. Confirm receipt in writing and check files for completeness.
5. Store the data in the access-restricted client folder.
6. Log the receipt event in the client governance log.

## 5. Governance rules (non-negotiables)

- No scraping and no data collected from external sources — the client is the only data source.
- Do not request phone numbers or national IDs without a documented delivery reason.
- Data is used for this engagement only and is never shared externally.
- Data is deleted or returned on offboarding per the PDPL.
- No real client names carried into public repository files.

## 6. Acceptance criteria (readiness checklist)

- [ ] All four core items received and complete.
- [ ] Files in a readable, non-corrupt format.
- [ ] DPA signed before any data transfer.
- [ ] Receipt event logged in `governance_events.md`.
- [ ] Access restricted to the delivery team only.

## 7. Metrics

- Data receipt time: request to completion (target ≤ 24 hours).
- First-pass data completeness.
- Share of engagements that started with full core data.

## 8. Observability hooks

- Log data state: `requested` / `received` / `validated`.
- Flag any missing file and the follow-up date.
- Weekly review of data receipt time.

## 9. Rollback procedure

If incomplete or corrupt data arrives:
1. Contact the client within 4 hours with a specific, clear request.
2. Do not start Day 1 of delivery with incomplete data.
3. If unnecessary PII transfer is found, delete it immediately and log the incident.
