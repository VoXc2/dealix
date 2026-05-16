# Conditional Build Triggers — مُحفِّزات البناء المشروط

> The build-on-demand registry the Commercial Freeze points to. During the
> freeze nothing new is built unless a real market signal asks for it.
> This document is the gate: a signal in, a small sales asset out, capped in size.
> سجلّ البناء عند الطلب الذي يشير إليه التجميد التجاري. أثناء التجميد لا يُبنى
> شيء جديد ما لم تطلبه إشارة سوق حقيقية. هذه الوثيقة هي البوّابة.
>
> Cross-link: [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) · [`MARKET_SIGNAL_CLASSIFICATION.md`](MARKET_SIGNAL_CLASSIFICATION.md) · [`FOUNDER_SIGNAL_WAR_ROOM.md`](FOUNDER_SIGNAL_WAR_ROOM.md) · [`WARM_LIST_WORKFLOW.md`](WARM_LIST_WORKFLOW.md) · [`../institutional/DEALIX_CONSTITUTION.md`](../institutional/DEALIX_CONSTITUTION.md)

---

## 0. The rule — القاعدة

**No signal → no build.** A build is justified only by a recorded incoming
signal from a real, named contact (see the Signal log in
[`FOUNDER_SIGNAL_WAR_ROOM.md`](FOUNDER_SIGNAL_WAR_ROOM.md) §3). No anticipation,
no "they will probably ask", no building because there is spare time.

Every build still respects the Commercial Freeze. What may be built is **a sales
asset only** — a document a customer reads. What may **never** be built under any
signal:

- ❌ A new product feature, module, or `*_os`.
- ❌ A new API router or endpoint.
- ❌ A dashboard, a frontend redesign, a new architecture doc.

If a signal seems to ask for a feature, that is not a build trigger — it is a
demand signal to record. Per the Constitution: *no repeated demand, no product
feature*. A single request never becomes a feature; it is logged and watched.

لا إشارة = لا بناء. الإشارة المسجّلة من جهة حقيقية مُسمّاة هي المبرّر الوحيد.
كل بناء يحترم التجميد: أصل بيع فقط، لا ميزة ولا API ولا لوحة. الطلب المتكرّر يُسجَّل ولا يصبح ميزة من طلب واحد.

---

## 1. Trigger registry — سجلّ المحفِّزات

| Signal | الإشارة | Asset to build | الأصل المراد بناؤه | Size cap |
|---|---|---|---|---|
| `asks_for_pdf` | يطلب ملف PDF | Partner Motion Pack — PDF export of an existing sales-kit page. No new content; export only. | تصدير PDF لصفحة موجودة من حزمة البيع. | 1 file, existing content only |
| `asks_for_english` | يطلب نسخة إنجليزية | English partner one-pager — English-side variant of an existing AR one-pager. | ورقة شريك إنجليزية — صيغة من ورقة عربية موجودة. | ≤ 1 page |
| `asks_for_scope` | يطلب النطاق | Diagnostic Scope template — bounded scope, inclusions, exclusions, inputs for the Free AI Ops Diagnostic (Offer rung 0). | قالب نطاق التشخيص — نطاق محدود، شموليات، استثناءات، مدخلات. | ≤ 1 page |
| `asks_for_pricing` | يطلب الأسعار | Offer/Pricing one-pager — figures lifted unchanged from [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md). | ورقة العرض والأسعار — أرقام منقولة كما هي من سلم العروض. | ≤ 1 page |
| `asks_for_security` | يطلب الأمان/الحوكمة | Trust Pack Lite — short summary of governance posture: sourcing, approval gates, evidence trail, PII handling. | حزمة الثقة المختصرة — ملخّص الحوكمة: المصدر، بوّابات الاعتماد، سجل الأدلة، التعامل مع البيانات الشخصية. | ≤ 2 pages |
| `repeated_pilot_demand` | طلب Pilot متكرّر | Small Partner Sales Kit — only after the *same* pilot ask appears from two or more separate contacts. Bundles the assets above; no new content. | حزمة بيع للشركاء صغيرة — فقط بعد تكرّر طلب الـPilot من جهتين منفصلتين فأكثر. | ≤ 4 pages, bundle only |

> Note on "repeated pilot demand": the founder's shorthand sometimes calls an
> advanced partner conversation an "L6-style" demand. There is no L6 — the
> proof ladder is L0–L5 (see `L4_TRUTH_CHECK.md` §0). What matters here is
> simply *repetition from independent contacts*, verified, before a kit is built.

ملاحظة: لا يوجد L6. ما يهم هو تكرار الطلب من جهات مستقلّة، مُتحقَّق منه، قبل بناء أي حزمة.

---

## 2. Build procedure — إجراء البناء

Before building any asset in Section 1:

1. **Confirm the signal is real.** A recorded incoming reply from a named contact
   exists in [`FOUNDER_SIGNAL_WAR_ROOM.md`](FOUNDER_SIGNAL_WAR_ROOM.md) §3. If the
   "signal" is only a belief, run [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md) first.
2. **Confirm it is a sales asset, not a feature.** If it fails this test, do not
   build — record the demand and stop.
3. **Build within the size cap.** Exceeding the cap requires a separate explicit
   founder decision logged in [`../ledgers/DECISION_LEDGER.md`](../ledgers/DECISION_LEDGER.md).
4. **Reuse before writing.** If an existing `docs/sales-kit/` file already covers
   the topic, extend it — do not duplicate.
5. **Log the build.** Record asset built, the signal that triggered it, and the
   contact label, in [`../ledgers/DECISION_LEDGER.md`](../ledgers/DECISION_LEDGER.md).

قبل أي بناء: تأكّد أن الإشارة حقيقية ومسجّلة · تأكّد أنه أصل بيع لا ميزة · ابقَ ضمن السقف · أعد الاستخدام قبل الكتابة · سجّل البناء.

---

## 3. What ends the freeze — ما الذي ينهي التجميد

This registry operates only during the Commercial Freeze. The freeze ends when
**one paid pilot is delivered and its Proof Pack is customer-approved (evidence
level L3 or above)**, per [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md).
Until then, every build passes through this gate — and most signals need no
build at all, only the matched action in
[`MARKET_SIGNAL_CLASSIFICATION.md`](MARKET_SIGNAL_CLASSIFICATION.md).

ينتهي التجميد بتسليم Pilot مدفوع واحد واعتماد العميل لحزمة الإثبات (L3 فأعلى).
حتى ذلك الحين، كل بناء يمرّ بهذه البوّابة — ومعظم الإشارات لا تحتاج بناءً أصلًا.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
