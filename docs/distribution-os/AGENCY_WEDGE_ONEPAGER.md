# Dealix — Agency Partner Pilot Wedge — إسفين الشراكة مع الوكالات
<!-- PHASE 13 | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** الوكالة ليست عميلاً فقط — هي **قناة توزيع**. كل
> عميل لها هو باب. الإسفين هو أصغر التزام يُثبت ذلك بأمان.
>
> **Golden rule:** an agency is not just a customer — it is a
> distribution channel. Each of its clients is a door. The wedge is the
> smallest commitment that proves this safely.

> **العلاقة — Relationship.** هذه الورقة الواحدة **تكمّل ولا تكرّر**
> [`docs/AGENCY_PARTNER_PITCH.md`](../AGENCY_PARTNER_PITCH.md). العرض
> الكامل (العمولة، الرابريك، آلية الدفع) هناك. هنا فقط **عرض الـ Pilot
> الافتتاحي** — نقطة الدخول منخفضة المخاطر. لا تُعرض شراكة كاملة قبل
> إتمام 3 Proof Packs.

---

## الإسفين / The wedge

### عربي

الوكالة لا تشتري منصة، ولا تغيّر نظامها، ولا توقّع عقداً طويلاً. نأخذ
**عميلاً واحداً** من عملائها كحالة اختبار، ونُنتج Proof Pack موثَّقاً.
بعدها — وبعدها فقط — نقرّر معاً: Pilot، أو Sprint، أو إحالة. إذا لم
يقتنعوا، لا شيء تغيّر في أعمالهم.

### English

The agency buys no platform, changes no system, signs no long contract.
We take **one of their clients** as a test case and produce a documented
Proof Pack. Then — and only then — we decide together: Pilot, Sprint, or
referral. If they are not convinced, nothing changed in their business.

---

## العرض / The offer

نطاق الإسفين الواحد، بسعر الدرجة 1 من سلّم العروض
([`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)):

| العنصر / Item | التفاصيل / Detail |
|---|---|
| العميل | عميل واحد من محفظة الوكالة (لا المحفظة كلها) |
| المراجعة | 10 فرص / leads تُراجَع وتُصنَّف |
| الردود | تصنيف الردود الواردة (مهتم / لاحقاً / غير مناسب) |
| المسوّدات | متابعات مكتوبة جاهزة — **مسوّدة فقط، الوكالة ترسلها** |
| المخرَج | Proof Pack ثنائي اللغة موثَّق وموقَّع |
| القرار | بعد التسليم: Pilot 499 SAR / Sprint / إحالة |
| السعر | 7-Day Revenue Proof Sprint — **499 SAR** |

---

## لماذا منخفض المخاطر / Why it is low-risk

- **لا تغيير نظام.** لا تكامل CRM، لا تركيب أدوات، لا تدريب فريق.
- **لا شراء منصة.** الإسفين خدمة منجَزة، ليس اشتراك برنامج.
- **عميل واحد فقط.** التعرّض محصور؛ سمعة الوكالة محميّة.
- **لا فعل خارجي بلا موافقة.** كل مسوّدة تُراجَع وتُرسَل بيد الوكالة
  أو العميل — Dealix لا يرسل نيابةً عن أحد.
- **لا واتساب بارد، لا scraping، لا قوائم مشتراة، لا ادّعاء أرقام
  مضمونة.** التزام بالعمل وبالـ Proof Pack فقط.

---

## لماذا هي قناة توزيع / Why it is a distribution channel

كل وكالة تخدم عشرات عملاء B2B. عميل اختبار واحد ناجح يفتح:

1. عملاء آخرين للوكالة نفسها (نمط `referral_partner_loop`).
2. تحوّل الوكالة من عميل إلى شريك مُحيل.
3. أصلاً مرجعياً co-branded يُستخدم في محادثات وكالات أخرى.

> الإسفين يُثبت النمط على عميل واحد؛ القناة تتسع عبر الإثبات لا عبر
> الوعود. The wedge proves the pattern on one client; the channel
> widens through proof, not promises.

---

## بعد الإسفين / After the wedge

| المسار / Path | الشرط / Condition | الوجهة / Destination |
|---|---|---|
| Pilot ثانٍ | العميل الأول مقتنع | عميل ثانٍ للوكالة |
| Sprint موسّع | الوكالة تريد عمقاً | درجة أعلى في سلّم العروض |
| إحالة | الوكالة تفضّل البقاء مُحيلاً | `referral_partner_loop` |
| شراكة كاملة | **بعد 3 Proof Packs مكتملة** | راجع [`AGENCY_PARTNER_PITCH.md`](../AGENCY_PARTNER_PITCH.md) و [`partners/PARTNER_PACKAGES.md`](../partners/PARTNER_PACKAGES.md) |

> الـ white-label وحصص العمولة الكاملة لا تُفتح قبل 3 Proof Packs —
> حدّ صارم يفرضه `commission_eligible()` في
> `auto_client_acquisition/sales_os/partner_engine.py`. تفاصيل
> الحوكمة في [`AFFILIATE_GOVERNANCE_SPEC.md`](AFFILIATE_GOVERNANCE_SPEC.md).

---

*Agency Wedge One-Pager v1.0 · 2026-05-17 · Dealix.*

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
