# Market Signal Classification — تصنيف إشارات السوق

> A response-to-action matrix. For every incoming signal there is one exact next
> action — nothing left to mood or memory. Classify the signal the moment the
> reply is read, take the listed action, record it in the listed ledger.
> مصفوفة من الإشارة إلى الإجراء. لكل إشارة واردة إجراء تالٍ واحد محدّد.
> صنّف الإشارة لحظة قراءة الرد، نفّذ الإجراء، سجّله في السجل المذكور.
>
> Cross-link: [`WARM_LIST_WORKFLOW.md`](WARM_LIST_WORKFLOW.md) · [`FOUNDER_SIGNAL_WAR_ROOM.md`](FOUNDER_SIGNAL_WAR_ROOM.md) · [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md) · [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md) · [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) · [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md)

---

## 0. How to use this — كيفية الاستخدام

When a reply lands, do three things in order:

1. **Classify** — pick the single closest signal name from the table below.
2. **Act** — execute the exact next action for that signal. No improvisation.
3. **Record** — write the signal and the action into the Signal log in
   [`FOUNDER_SIGNAL_WAR_ROOM.md`](FOUNDER_SIGNAL_WAR_ROOM.md) §3 and the listed ledger.

Two standing rules govern every row:

- **No offer-laddering ahead of proof.** A signal of interest is not permission to
  pitch the next rung of [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).
  The next rung opens only after a recorded proof event from the current one.
- **No new build from a signal here.** A request for an asset is routed to
  [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md), which decides
  whether a small sales asset is built. A signal never triggers a feature.

عند وصول رد: صنّف الإشارة بدقّة، نفّذ الإجراء المحدّد، سجّله. لا ترقية قبل إثبات.
الطلبات على أصول تُوجَّه إلى سجل البناء المشروط — الإشارة لا تُنتج ميزة أبدًا.

---

## 1. Signal-to-action matrix — مصفوفة الإشارة إلى الإجراء

| Signal | الإشارة | Exact next action | الإجراء التالي | Record in |
|---|---|---|---|---|
| `replied_interested` | رد بالاهتمام | Reply the same working day, during working hours — promptly but not instant (`WARM_LIST_WORKFLOW.md` §4.1). Request a 20-min qualification call. | رد في نفس يوم العمل وخلال ساعات العمل — بسرعة دون أن يبدو آليًّا (§4.1). اطلب مكالمة تأهيل 20 دقيقة. | War Room §3 |
| `meeting_booked` | حُجز اجتماع | Prepare a tight agenda only. Do **not** pre-build an offer or pitch a rung ahead of proof. Ask them to nominate one real customer to discuss. | جهّز أجندة فقط — لا عرض مسبق ولا ترقية قبل الإثبات. | War Room §3 |
| `used_in_meeting` | استُخدم في اجتماع | After the meeting, record a proof event in [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) — what was shown, the type, the outcome. | سجّل حدث إثبات في سجل الإثبات بعد الاجتماع. | PROOF_LEDGER |
| `qualify_decision_returned` | عاد قرار التأهيل | Log the five-decision outcome (`ACCEPT` / `DIAGNOSTIC_ONLY` / `REFRAME` / `REJECT` / `REFER_OUT`) as `event=qualify_decision`, exactly as `WARM_LIST_WORKFLOW.md` §5 specifies. | سجّل قرار التأهيل كـ`event=qualify_decision` وفق §5. | PROOF_LEDGER |
| `pilot_intro_requested` | طُلب تمهيد Pilot | Send the **Diagnostic Scope template** (Offer Ladder rung 0). No commitment language; the diagnostic is the door. | أرسل قالب نطاق التشخيص — لا لغة التزام. | War Room §3 |
| `asks_for_pdf` | يطلب ملف PDF | Send the small asset only. Route the build (if not yet built) via [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md). One file, never a deck. | أرسل الأصل الصغير فقط — وجّه البناء عبر سجل البناء المشروط. | War Room §3 |
| `asks_for_english` | يطلب نسخة إنجليزية | Send the English one-pager variant. Route via [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md). | أرسل النسخة الإنجليزية — وجّه البناء عبر سجل البناء المشروط. | War Room §3 |
| `asks_for_scope` | يطلب النطاق | Send the **Diagnostic Scope template**. Route via [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md). | أرسل قالب نطاق التشخيص — وجّه البناء عبر سجل البناء المشروط. | War Room §3 |
| `asks_for_pricing` | يطلب الأسعار | Send the **Offer/Pricing one-pager** (figures from [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)). No negotiation in chat below the Managed Ops tier. | أرسل ورقة العرض والأسعار — لا تفاوض في المحادثة دون درجة الإدارة. | War Room §3 |
| `asks_for_security` | يطلب الأمان/الحوكمة | Send **Trust Pack Lite**. Route via [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md). | أرسل حزمة الثقة المختصرة — وجّه البناء عبر سجل البناء المشروط. | War Room §3 |
| `no_response_after_follow_up` | لا رد | If no reply within 7 days, mark it and move on — no chasing. No unsolicited follow-up; a second message goes out only when a follow-up window was explicitly agreed (`WARM_LIST_WORKFLOW.md` §1). Re-engage only on a natural occasion. | إن لم يصل رد خلال 7 أيام، علّمها وانتقل — لا مطاردة. لا متابعة غير مطلوبة؛ رسالة ثانية فقط عند اتّفاق صريح على نافذة متابعة. | War Room §3 + FRICTION_LOG |
| `low_intent` | اهتمام ضعيف | A third back-and-forth with no progress to a call or an intake form (`WARM_LIST_WORKFLOW.md` §4). Log it and leave the door open — no push, no pitch. | تبادل ثالث دون تقدّم لمكالمة أو نموذج إدخال. سجّلها واترك الباب مفتوحاً — لا دفع ولا عرض. | War Room §3 + FRICTION_LOG |
| `not_interested` | غير مهتم | Thank them, log the decline reason anonymized, never push. The relationship is the asset. | اشكرهم، سجّل سبب الاعتذار مجهّلًا، لا إلحاح. | FRICTION_LOG |
| `invoice_sent` | أُرسلت الفاتورة | Record the pending invoice. Revenue is not confirmed yet — do not log value until paid. | سجّل الفاتورة المعلّقة — لا تُسجَّل القيمة قبل الدفع. | War Room §3 |
| `invoice_paid` | دُفعت الفاتورة | Revenue confirmed. Record the value event in [`../ledgers/VALUE_LEDGER.md`](../ledgers/VALUE_LEDGER.md) with evidence. Trigger Proof Pack assembly. | الإيراد مؤكّد — سجّل حدث القيمة في سجل القيمة مع دليل. | VALUE_LEDGER |

---

## 2. Notes that keep the matrix honest — ملاحظات تحفظ صدق المصفوفة

- **`meeting_booked` is not `meeting_held`.** A booked meeting can still slip. Promote
  the stage only on real evidence — see [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md).
- **`used_in_meeting` before `invoice_paid`.** A proof event recorded in the
  Proof Ledger is private sales proof (L3 at most until the customer approves
  public use). It is not a public case study and not a revenue claim.
- **`invoice_sent` ≠ revenue.** Only `invoice_paid` writes to the Value Ledger.
  An estimate is never logged as a verified result.
- **Asset requests are bounded.** Every `asks_for_*` signal routes through
  [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md). If the asset
  already exists, send it; if not, build only within the size cap there. No
  signal ever justifies a new feature, module, or API during the freeze.
- **REJECT signals are still recorded.** Out-of-scope requests (scraping, cold
  WhatsApp automation, LinkedIn automation, guaranteed sales) get a polite refusal
  and a friction-log entry — never a workaround.

الاجتماع المحجوز ليس اجتماعًا منعقدًا · حدث الإثبات ليس دراسة حالة عامة ·
الفاتورة المُرسلة ليست إيرادًا · طلبات الأصول محدودة بسقف · طلبات خارج النطاق تُرفض وتُسجَّل.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
