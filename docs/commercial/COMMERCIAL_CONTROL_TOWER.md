<!-- Owner: Founder | Date: 2026-05-17 | Commercial Scale System -->

# برج التحكم التجاري — Commercial Control Tower

> **قاعدة ذهبية:** كل يوم تجاري ينتهي بـ **Commercial Evidence Event** واحد على الأقل. لا تقدّم في pipeline بدون دليل مُتحقَّق.

## النطاق / Scope

- **هذا الملف:** حلقة تشغيل تجارية يومية تربط السوق بالشريك بالمحتوى، مع خطتي 60 و90 يوماً.
- **ليس هذا الملف:** قائمة أسعار، ولا خطة منتج هندسية، ولا بديل عن `../ops/DAILY_COMMERCIAL_LOOP_AR.md` (هذا الأخير هو الإجراء اليومي التفصيلي).

## المصدر القانوني / Canonical source

- الأسعار والنطاق المعتمد: [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
- الحلقة التجارية اليومية التفصيلية (canonical): [`../ops/DAILY_COMMERCIAL_LOOP_AR.md`](../ops/DAILY_COMMERCIAL_LOOP_AR.md)
- حوكمة الوحدات والقرارات: [`../control_tower/README.md`](../control_tower/README.md) · [`../control_tower/CEO_DECISIONS.md`](../control_tower/CEO_DECISIONS.md)

## سلسلة التشغيل اليومية — The daily chain

البرج يمرّ كل يوم على 12 محطة بالترتيب. كل محطة تُنتج إدخالاً واحداً قابلاً للقياس.

| # | المحطة | السؤال الذي يطرحه البرج |
|---|--------|--------------------------|
| 1 | Market | أي قطاع يعطي أوضح إشارة طلب اليوم؟ |
| 2 | Audience | ما أفضل شريحة (ICP) للتركيز عليها الآن؟ |
| 3 | Channel | أي قناة تهدر جهداً، وأيها تعطي ردوداً حقيقية؟ |
| 4 | Offer | ما العرض المناسب لهذه الشريحة من سلم الخدمات؟ |
| 5 | Proof | ما أفضل Proof asset نعرضه لهذا القطاع؟ |
| 6 | Sales Room | أين توقف العميل في المحادثة، وما أعلى objection؟ |
| 7 | Invoice | هل صدرت فاتورة، وهل وصل أول دفع؟ |
| 8 | Delivery | هل التسليم يسير وفق معيار Source→Owner→Approval→Evidence→Next؟ |
| 9 | Expansion | هل أنتج التسليم upsell أو حالة قابلة للترقية؟ |
| 10 | Partner | أي شريك جلب lead بجودة جيدة، وأيهم جلب ضوضاء؟ |
| 11 | Content | ما الحالة المجهّلة (anonymized) الجاهزة للنشر اليوم؟ |
| 12 | Benchmark | ما الذي **يجب ألا** نبنيه بعد، وما الذي يستحق التتبع؟ |

### الأسئلة اليومية الثابتة

- أفضل شريحة اليوم؟ أفضل رسالة؟ أفضل Proof asset؟
- أعلى objection تكرر؟ أين توقف العميل بالضبط؟
- أي شريك جلب جودة؟ أي قناة تهدر الجهد؟
- ما الذي يجب **ألا** نبنيه (حتى لا نهرب من البيع إلى الهندسة)؟

## الهدف من البرج — Goal

برج التحكم التجاري ينجح عندما يُنتج بشكل متكرر:

1. **Paid Pilot** — تجربة مدفوعة عبر rung [1] 7-Day Revenue Proof Sprint (499 SAR).
2. **First Proof Pack** — أول حزمة إثبات مُتحقَّقة وقابلة للعرض.
3. **Repeatable workflow** — تسلسل تشغيل يتكرر بنفس الخطوات دون ارتجال.
4. **Partner loop** — حلقة شركاء تجلب leads بجودة قابلة للقياس.

## Commercial Evidence Event — حدث الإثبات التجاري

كل يوم يجب أن ينتهي بحدث واحد على الأقل من القائمة. لا يُسجَّل أي حدث بدون مصدر ومالك.

| الحدث | المعنى |
|-------|--------|
| `message_sent_manual` | رسالة أُرسلت يدوياً بعد موافقة بشرية (لا live send آلي) |
| `reply_received` | ردّ حقيقي من جهة خارجية |
| `demo_booked` | حجز عرض (12 دقيقة) |
| `scope_requested` | العميل طلب تحديد نطاق |
| `invoice_sent` | فاتورة صدرت |
| `payment_received` | دفع وصل (لا live charge آلي — تأكيد يدوي) |
| `proof_pack_delivered` | Proof Pack سُلِّم بعد QA |
| `partner_intro_created` | تعريف شريك أُنشئ |
| `referral_requested` | طلب إحالة سُجِّل |

**ممنوع منعاً قاطعاً داخل البرج:** scraping، cold WhatsApp / LinkedIn automation، fake proof، وعود ROI أو نتائج مضمونة، PII في السجلات، إجابة بلا مصدر، مخرج AI للعميل بلا QA، live send، live charge، أي إجراء خارجي بلا موافقة بشرية، وأي تقدّم مرحلة بلا دليل مُتحقَّق.

## خطة الأيام 31–60 — Days 31–60 plan

المرحلة الأولى (تثبيت): قفل أفضل عرض، تجهيز partner kit، نشر 3 منشورات بأسلوب الحالة (case-style)، تشغيل mini workshop، بدء retargeting بسيط، وتحويل أول Proof إلى مقترح Sprint.

المرحلة الثانية (توسيع مبكر): إغلاق 2–3 pilots إضافية، بدء retainer خفيف واحد، تفعيل 5 شركاء، بدء benchmark tracking، وبناء أول customer-success loop.

**هدف الـ60 يوماً:**

| المؤشر | الهدف |
|--------|-------|
| Paid pilots | 3 |
| Sprint proposals | 1 |
| Retainer candidate | 1 |
| شركاء مفعّلون | 5 |
| رؤى مجهّلة (anonymized insights) | 3 |
| ICP أوضح | محدّد بوضوح |

## نموذج الـ90 يوماً التجاري — 90-day commercial model

| المؤشر | الهدف 90 يوماً |
|--------|-----------------|
| Paid pilots | 5–8 |
| Data-to-Revenue Packs (rung [2]) | 2 |
| Deep-implementation sprint | 1 |
| Retainer candidate | 1 |
| شركاء نشطون | 10 |
| Mini benchmark report | 1 |
| Proof-pack library | مبنية |
| Objection library | مبنية |
| Repeatable sales script | جاهز |

أي مبلغ خارج السلم المعتمد (مثل عرض «تشخيص مخصص») لا يُنشر كسعر ثابت؛ يُعاد تأطيره كـ "custom — quoted per scope" ويُوجَّه إلى الدرجة المناسبة في [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

## روابط ذات صلة / Related

- [مسارات البيع الأربعة](SALES_MOTIONS.md)
- [مصفوفة العروض](OFFER_MATRIX.md)
- [معيار Dealix](DEALIX_STANDARD.md)
- [منهجية Dealix](DEALIX_METHOD.md)
