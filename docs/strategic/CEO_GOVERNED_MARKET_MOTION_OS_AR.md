# Dealix — CEO Governed Market Motion OS

هذا الدليل يحوّل الجاهزية الحالية إلى **أحداث سوقية موثّقة** بدل البناء الإضافي.

المبدأ الحاكم:

> لا نبيع "AI Automation". نبيع تشغيل AI محكوم: مصدر واضح، حدود موافقات، أدلة أثر، وقرار قابل للتدقيق.

---

## الهدف التنفيذي الآن

السلسلة التنفيذية المطلوبة:

1. أول 5 رسائل حقيقية.
2. أول رد أو صمت موثق.
3. أول اجتماع.
4. أول scope.
5. أول فاتورة.
6. أول proof.

---

## أنظمة التشغيل الـ12 (نسخة تنفيذية)

## 1) Market Motion OS (الإرسال)

- دفعة أولى = 5 جهات فقط من warm list.
- رسالة شخصية قصيرة + سؤال واحد.
- بدون deck / PDF / روابط كثيرة / شرح كامل للمنتج.
- تسجيل `sent` بعد الإرسال فقط.

## 2) Evidence OS (سُلّم الدليل)

- `L4`: sent / external exposure.
- `L5`: used in meeting.
- `L6`: market pull (intro أو scope).
- `L7 candidate`: invoice sent.
- `L7 confirmed`: invoice paid.

قواعد منع التضخيم:

- `sent` ليس traction.
- `reply` ليس validation.
- لا كلمة traction قبل L5.
- لا كلمة revenue قبل invoice paid.

## 3) Response Classification OS

التصنيفات القياسية:

- `replied_interested` → ask meeting.
- `send_more_info` → 30-minute framing.
- `asks_for_case_study` → proof-stage response.
- `asks_for_pdf` → PDF صغير فقط.
- `asks_for_english` → English one-pager فقط.
- `asks_for_scope` → draft diagnostic scope.
- `meeting_booked` → prepare agenda.
- `used_in_meeting` → log L5.
- `pilot_intro_requested` → log L6.
- `no_response_after_follow_up` → move to Batch 2.
- `invoice_sent` → L7 candidate.
- `invoice_paid` → revenue confirmed.

## 4) Meeting Conversion OS

هدف الاجتماع: مخرج واحد فقط (segment أو pilot intro أو scope).

Agenda 30 دقيقة:

1. Dealix ليست automation resale.
2. أين يستخدم العميل AI الآن.
3. أين يضعف source clarity / governance.
4. ما الدليل الذي يبرر diagnostic.
5. trust gates والحدود.
6. قرار واحد نهائي.

## 5) Offer Ladder OS

التدرج التجاري:

1. Governed AI Operations Diagnostic.
2. Revenue Intelligence Sprint.
3. Governed Ops Retainer.

## 6) Diagnostic Scope OS

scope من صفحة واحدة فقط:

- Objective
- Inputs
- Outputs
- Exclusions
- Timeline
- Price
- Next step

## 7) Revenue Proof OS

التدفق:

`scope_requested -> scope_sent -> invoice_sent -> invoice_paid -> proof_pack -> retainer_offer`

## 8) Capital Allocation OS

القرار على كل أصل:

- Invest
- Activate
- Maintain
- Prune
- Kill

القاعدة: لا بناء بدون signal.

## 9) Board Decision OS

يدخل للـ Board بعد أول batch:

- sent_count
- reply_count
- meeting_count
- no_response_count
- asks_for_scope_count
- asks_for_pdf_count

المخرجات المسموحة:

- `continue`
- `revise_message`
- `test_batch_2`
- `build_pdf`
- `prepare_scope`

## 10) Saudi/GCC Positioning OS

التموضع:

**Saudi/GCC Governed AI Operations**

المتطلبات:

- Arabic/English proof packs.
- لغة PDPL-aware دون ادعاء قانوني.
- Human-in-the-loop.
- No cold WhatsApp.

## 11) Risk Control OS

أهم المخاطر:

- fake traction
- overclaim
- scope creep
- agent external actions بلا approval
- data trust gap

القاعدة: `source_ref` لكل رقم.

## 12) Strategic Restraint OS (لا تفعل)

- لا إرسال 20 دفعة واحدة.
- لا PR منتجي جديد قبل signal.
- لا PDF قبل طلب PDF.
- لا English قبل طلب English.
- لا SaaS قبل paid proof.
- لا dashboard قبل workflow حقيقي.

---

## التنفيذ الفوري (جلسات)

## جلسة 1: أول 5

1. اختيار 5 من warm list.
2. مراجعة سريعة.
3. إرسال يدوي.
4. تسجيل `sent`.

## جلسة 2: أول نتيجة

- الرد المهتم → اجتماع.
- طلب تفاصيل → 30 دقيقة framing.
- طلب PDF/English → artifact صغير فقط.
- لا رد → follow-up واحد ثم Batch 2.

## جلسة 3: الاجتماع

- اختبار fit على governance + proof + segment.
- خروج بمخرج واحد (intro أو scope).

## جلسة 4: scope → invoice

1. صفحة scope واحدة.
2. قبول السعر.
3. invoice.
4. بعد الدفع: proof pack + capital asset.

---

## 7 أرقام فقط

1. `sent_count`
2. `reply_rate`
3. `meeting_rate`
4. `l5_count`
5. `l6_count`
6. `invoice_sent_count`
7. `invoice_paid_count`

---

## أدوات مرتبطة داخل الكود

- منطق التصنيف + L4→L7 + قرار Board: `auto_client_acquisition/sales_os/market_motion.py`
- مولد رسائل أول 5 (رسالة حاكمة قصيرة): `scripts/warm_list_outreach.py`

