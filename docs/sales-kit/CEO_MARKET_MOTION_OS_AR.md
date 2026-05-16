# Dealix CEO Market Motion OS (AR/EN)

هذا الدليل يحوّل الجاهزية الداخلية إلى أحداث سوقية موثقة.

**المبدأ الحاكم:** لا تبنِ أكثر قبل أول إشارات حقيقية.  
**سلسلة الإثبات:** أول 5 رسائل حقيقية → أول رد/صمت موثق → أول اجتماع → أول scope → أول فاتورة.

---

## 1) Market Motion OS — نظام الإرسال

- ابدأ بـ 5 جهات فقط من warm list.
- رسالة قصيرة + سطر شخصي واحد + سؤال واحد.
- لا Deck، لا PDF، لا روابط كثيرة.
- لا تسجّل `sent` قبل حدوث الإرسال فعليًا.

تحضير المسودات:

`python3 scripts/dealix_market_motion.py prepare-first5 --csv data/warm_list.csv --out data/outreach/warm_list_first5_personalized.md`

---

## 2) Evidence OS — مستويات الإثبات

داخل النظام التشغيلي:

- `L4` = `sent` (external exposure)
- `L5` = `used_in_meeting` فقط
- `L6` = `asks_for_scope` أو `pilot_intro_requested`
- `L7` = `invoice_sent` / `invoice_paid`

قواعد عدم التضليل:

- `sent` ليس traction.
- `reply` ليس validation.
- `meeting_booked` ليس L5.
- `invoice_sent` ليس revenue.
- `invoice_paid` هو revenue confirmed.

---

## 3) Response Classification OS — نظام تصنيف الردود

الأحداث المعتمدة:

- `replied_interested`
- `send_more_info`
- `asks_for_case_study`
- `asks_for_pdf`
- `asks_for_english`
- `asks_for_scope`
- `meeting_booked`
- `used_in_meeting`
- `pilot_intro_requested`
- `no_response_after_follow_up`
- `invoice_sent`
- `invoice_paid`

كل حدث يجب أن يحمل `source_ref` (رابط/مرجع/مذكرة).

---

## 4) Meeting Conversion OS — تحويل الاجتماع

هدف الاجتماع:

- شريحة عميل واحدة **أو**
- طلب pilot intro **أو**
- طلب scope واضح.

لا تعتبر الاجتماع إثبات L5 إلا عند استخدام الأصل في الاجتماع (`used_in_meeting`).

---

## 5) Offer Ladder OS — سلم العرض

الترتيب التشغيلي:

1. Governed AI Operations Diagnostic
2. Revenue Intelligence Sprint
3. Governed Ops Retainer

ابدأ بخدمة قابلة للإثبات قبل أي توسع SaaS.

---

## 6) Diagnostic Scope OS — نظام السكوب

لا تسجّل `invoice_sent` إلا بعد `asks_for_scope`.

قاعدة النظام الحالية:

- `invoice_sent` مرفوض دون `asks_for_scope`.
- `invoice_paid` مرفوض دون `invoice_sent`.

---

## 7) Revenue Proof OS — نظام إثبات الإيراد

السلسلة التشغيلية:

`asks_for_scope -> invoice_sent -> invoice_paid`

بعد الدفع: proof pack + capital asset + template reuse.

---

## 8) Capital Allocation OS — رأس المال

- الأصل الذي يتحرك إلى `L6/L7` هو الذي يستحق الاستثمار.
- الأصل الذي يتوقف عند `L4` يذهب للمراجعة/التعلم، لا للتوسع.

---

## 9) Board Decision OS — قارئ قرار عملي

المدخلات:

- sent_count
- reply_count
- meeting_count
- no_response_count
- asks_for_scope_count
- asks_for_pdf_count

المخرجات:

- `continue`
- `revise_message`
- `test_batch_2`
- `build_pdf`
- `prepare_scope`

عرض الحالة:

`python3 scripts/dealix_market_motion.py status --ledger docs/ops/live/market_motion_events.jsonl`

---

## 10) Saudi/GCC Positioning OS

التموضع:

**Governed AI Operations** (ليس generic automation resale).

لغة السوق:

- AR/EN proof-ready language
- PDPL-aware wording بدون ادعاءات شهادة رسمية
- Human-in-the-loop + trust gates

---

## 11) Risk Control OS — نظام المخاطر

ممنوعات التشغيل:

- no cold WhatsApp
- no LinkedIn automation
- no scraping
- no unsupported revenue claims
- no external autonomous actions without approval

---

## 12) Strategic Restraint OS — نظام “لا تفعل”

قبل أول إشارات:

- لا Batch كبير.
- لا توسعة Product.
- لا Board OS v2.
- لا Dashboard جديد.
- لا Case Study عامة بدون proof وموافقة.

---

## التشغيل اليومي (Quick Loop)

1) حضّر أول 5:

`python3 scripts/dealix_market_motion.py prepare-first5`

2) بعد كل إرسال حقيقي، سجّل الحدث:

`python3 scripts/dealix_market_motion.py log-event --contact-id <id> --event sent --source-ref "whatsapp:2026-05-16T09:00Z"`

3) سجّل الردود/الصمت بنفس الطريقة:

`python3 scripts/dealix_market_motion.py log-event --contact-id <id> --event asks_for_scope --source-ref "email-thread-42"`

4) راقب 7 أرقام + قرار واحد:

`python3 scripts/dealix_market_motion.py status`

---

الجملة الحاكمة:

**لا تضف استعدادًا الآن. اصنع دليلًا.**
