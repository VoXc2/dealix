# Dealix — Affiliate Governance
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> هذه الوثيقة **حوكمة لبرنامج الإحالة القائم** — وليست طبقة تجارية جديدة.
> برنامج الإحالة موجود بالفعل في `../sales-kit/dealix_referral_program.md`
> وفي وحدة `auto_client_acquisition/partnership_os/referral_store.py`.
> This governs the EXISTING referral program — it is not a new layer.

---

## النطاق — Scope

البرنامج القائم يدفع **5,000 SAR لكل صفقة مُغلقة** (ثابت `REFERRER_CREDIT_SAR`
في `referral_store.py`). هذه الوثيقة تضيف **قواعد التشغيل الآمن** فوقه:
من يُسمح له، كيف يُروّج، ومتى يُدفع.

---

## قواعد الحوكمة — Governance rules

| القاعدة | التفصيل |
|---------|---------|
| **عدد محدود** | ابدأ بـ 5–10 مُحيلين موثوقين فقط — لا فتح عام |
| **موافقة يدوية** | كل مُحيل يُعتمد يدوياً من المؤسس قبل التفعيل |
| **سكربتات معتمدة** | الترويج بالسكربتات المعتمدة فقط — لا صياغة حرة |
| **إفصاح إلزامي** | كل ترويج يحمل إفصاحاً واضحاً عن العلاقة |
| **الدفع بعد `invoice_paid`** | العمولة تُصرف فقط بعد حالة `invoice_paid` |

حالة `invoice_paid` هي حالة صريحة في `ReferralStatus` داخل
`referral_store.py`. لا دفع عند `pending` أو `redeemed`.

---

## محظورات — Banned, no exceptions

- ❌ ادعاءات ROI مضمون أو امتثال مضمون.
- ❌ إيحاء بأن Dealix يرسل رسائل تلقائياً نيابة عن أحد.
- ❌ Spam أو رسائل بالجملة غير مرغوبة.
- ❌ Cold WhatsApp إلى جهات لا تعرف المُحيل.
- ❌ إثبات مزيّف أو أمثلة عملاء غير حقيقية.
- ❌ ترويج بدون إفصاح.
- ❌ أي ادعاء غير معتمد عن الميزات أو الأسعار.

المخالفة: تحذير → تعليق العمولات → إنهاء + استرداد المدفوع. (متوافق مع
قسم الامتثال في `../sales-kit/dealix_referral_program.md`.)

---

## مقتطف الإفصاح الجاهز — Bilingual disclosure snippet

ينسخه المُحيل كما هو في أي منشور أو رسالة ترويجية:

> **عربي:** "أنا شريك إحالة لدى Dealix. إذا اشتركت عبر رابطي قد أحصل على
> عمولة. هذا لا يغيّر السعر عليك، وكل النتائج تقديرية وليست مضمونة."
>
> **English:** "I am a Dealix referral partner. If you sign up through my
> link I may earn a commission. This does not change your price, and all
> outcomes are estimated, not guaranteed."

---

## ما لا يفعله المُحيل — Out of bounds

- لا يتحدث باسم Dealix أو ينتحل صفة الفريق.
- لا يعد بأسعار خارج `../OFFER_LADDER_AND_PRICING.md`.
- لا يجمع بيانات leads بدون موافقتها.
- لا يستخدم scraping ولا أتمتة LinkedIn.

---

## التتبّع — Tracking

الإسناد والحالات تُدار في `partnership_os/referral_store.py`
(`ReferralCode` / `Referral` / `ReferralPayout`). أي عمولة تُصرف يدوياً
بعد تأكيد `invoice_paid`، مع تسجيل audit. لا صرف صامت، لا تجاوز بشري.

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
