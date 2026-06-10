# Customer #1 Go-Live Runbook | دليل تشغيل العميل الأول
<!-- Owner: Founder | Date: 2026-05-16 | Arabic primary — العربية أولاً -->

> هذا الدليل خطوة-بخطوة لتسليم **أول عميل مدفوع** عبر Sprint الـ499 ريال —
> من تأكيد الدفع إلى تسليم Proof Pack مُنسَّق. كل خطوة يدوية وبموافقة المؤسس.
> A step-by-step runbook to deliver the **first paid customer** through the
> 499 SAR Sprint — from payment confirmation to a rendered Proof Pack. Every
> step is manual and founder-approved.

---

## 0. قبل البدء | Before you start

- [ ] الـbackend منشور على Railway ويعمل (`/health` يرد 200).
- [ ] العميل وافق على عرض Sprint الـ499 ريال (مسودة العرض مُعتمدة).
- [ ] لديك بيانات العميل: قائمة العملاء المحتملين / pipeline بصيغة CSV.
- [ ] Source Passport جاهز (من أين أتت البيانات + أساس الموافقة).

---

## 1. تحصيل الدفعة | Collect payment

الوضع الافتراضي **يدوي / تحويل بنكي** — لا شحن مباشر تلقائي
(`NO_LIVE_CHARGE`). خطوات اختيارية لتفعيل Moyasar المباشر في القسم 6.

1. أنشئ نية الفاتورة:
   `POST /api/v1/payment-ops/invoice-intent`
   `{"customer_handle": "<اسم>", "amount_sar": 499, "method": "bank_transfer"}`
   → احفظ `payment_id`.
2. أرسل تفاصيل التحويل البنكي للعميل يدوياً، وانتظر السداد.
3. عند استلام إيصال التحويل، ارفع الإثبات:
   `POST /api/v1/payment-ops/manual-evidence`
   `{"payment_id": "<id>", "evidence_reference": "<مرجع الإيصال>"}`
4. أكِّد الدفعة (إجراء المؤسس):
   `POST /api/v1/payment-ops/confirm`
   `{"payment_id": "<id>", "confirmed_by": "<اسمك>"}`
   → الحالة تصبح `payment_confirmed`.

## 2. بدء التسليم | Kick off delivery

5. شغّل بدء التسليم:
   `POST /api/v1/payment-ops/{payment_id}/kickoff-delivery`
   → الحالة تصبح `delivery_kickoff` ويُصدَر `delivery_kickoff_id`.
   الردّ يتضمّن `next_action` يخبرك بالخطوة التالية. احفظ `delivery_kickoff_id`
   — هو **رابط التدقيق** بين الدفعة والتسليم، وستستخدمه كـ`engagement_id`.

> ملاحظة: `kickoff-delivery` لا يشغّل الـSprint تلقائياً — لأن بيانات العميل
> (الـCSV) لم تُرفع بعد. الخطوة التالية يدوية ومقصودة.

## 3. تشغيل الـSprint | Run the Sprint

6. شغّل المُنسِّق ذا الـ10 خطوات ببيانات العميل الحقيقية:
   `POST /api/v1/sprint/run`
   ```json
   {
     "engagement_id": "<delivery_kickoff_id من الخطوة 5>",
     "customer_id": "<customer_handle>",
     "source_passport": { ... },
     "raw_csv": "<CSV العميل>",
     "accounts": [ ... ],
     "problem_summary": "<وصف مشكلة العميل>",
     "workflow_owner_present": true
   }
   ```
   → الردّ هو سجل التشغيل الكامل؛ منه خُذ الحقل `proof_pack`. شغّل الـSprint
   **مرة واحدة فقط** — التشغيل يكتب في السجلّات ويُسجّل أصولاً.

## 4. تسليم Proof Pack مُنسَّق | Render the deliverable

> مسارات `/render/*` تُنسِّق فقط — تأخذ `proof_pack` من ردّ الخطوة 6 ولا
> تُعيد تشغيل الـSprint.

7. ولّد الـProof Pack بصيغة PDF (أو Markdown احتياطياً):
   `POST /api/v1/sprint/render/pdf`
   `{"customer_handle": "<الاسم>", "proof_pack": <كائن proof_pack من الخطوة 6>}`
   → ملف PDF. إن لم يتوفّر مُحرِّك PDF يرجع Markdown مع ترويسة
   `X-PDF-Renderer: unavailable`. (يمكن بدلاً من `proof_pack` تمرير ردّ
   الخطوة 6 كاملاً في الحقل `run`.)
8. ولّد نص بريد جاهز للإرسال:
   `POST /api/v1/sprint/render/email-body` بنفس الـbody → رسالة غلاف ثنائية
   اللغة.
9. **راجع الملف بنفسك** — تأكد أن قسم "Limitations" واضح ولا توجد ادعاءات
   مضمونة. ثم أرسله للعميل **من بريدك الشخصي**. لا إرسال تلقائي
   (`NO_LIVE_SEND` — موافقة أولاً).

> للتشخيص المجاني (الدرجة 0) استخدم بدلاً من ذلك:
> `POST /api/v1/diagnostic/report/pdf` و `/report/markdown` (تأخذ نفس body
> الـ`POST /api/v1/diagnostic/generate`).

## 5. التسجيل في السجلّات | Record to the ledgers

10. سجّل التسليم والإثبات في:
    - `docs/ledgers/DELIVERY_LEDGER.md` — التسليم تم.
    - `docs/ledgers/PROOF_LEDGER.md` — درجة Proof Pack والمستوى.
    - `docs/ledgers/CAPITAL_LEDGER.md` — الأصول القابلة لإعادة الاستخدام.
11. إذا اعتمد العميل الـProof Pack عند مستوى L3+ → **شرط الخروج من
    التجميد التجاري قد تحقّق** (`docs/ops/COMMERCIAL_FREEZE.md`).

---

## 6. (اختياري) تفعيل Moyasar المباشر | Optional: Moyasar live cutover

هذه **خطوة المؤسس فقط** — تتطلب مفتاح `sk_live_...` السرّي الحقيقي ولا يمكن
لأي مساعد آلي تنفيذها.

1. شغّل المساعد التفاعلي: `python scripts/moyasar_live_cutover.py`
   — يتحقّق من شكل المفتاح، يطبع ما تلصقه في Railway، ولا يخزّن المفتاح على
   القرص.
2. على Railway: أضِف `DEALIX_MOYASAR_MODE=live` ومتغيرات المفتاح كما يطبعها
   المساعد. راجع `docs/sales-kit/RAILWAY_MOYASAR_STEP_BY_STEP.md`.
3. اقلب رابط الـwebhook في لوحة Moyasar.
4. اختبر بـ1 ريال (sandbox) قبل أي شحن حقيقي.

> بدون `DEALIX_MOYASAR_MODE=live` بشكل صريح، النظام يرفض `moyasar_live`
> (بوابة `NO_LIVE_CHARGE`). الوضع الافتراضي يبقى التحويل البنكي اليدوي.

---

## بوابات لا تُكسَر | Hard gates that never break

- `NO_LIVE_CHARGE` — لا شحن مباشر دون تفعيل صريح من المؤسس.
- `NO_LIVE_SEND` — كل مُخرَج يُرسله المؤسس يدوياً بعد المراجعة.
- موافقة أولاً — لا إجراء خارجي دون موافقة.
- لا إثبات زائف — Proof Pack فارغ يُعرض كـ"لم يُولَّد بعد"، لا يُختلق؛
  والتشغيل بلا بيانات يُسجَّل كـ`weak_proof`.

*Estimated outcomes are not guaranteed outcomes /
النتائج التقديرية ليست نتائج مضمونة.*
