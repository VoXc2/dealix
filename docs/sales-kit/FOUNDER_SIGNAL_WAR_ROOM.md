# Founder Signal War Room — غرفة عمليات الإشارات للمؤسس

> The one surface the founder opens every morning during the Commercial Freeze.
> Not a strategy doc — a tracking surface. Fill the tables, follow the ritual, close the day.
> السطح الوحيد الذي يفتحه المؤسس كل صباح أثناء التجميد التجاري.
> ليست وثيقة استراتيجية — سطح تتبّع. املأ الجداول، اتبع الطقس اليومي، أغلق اليوم.
>
> Cross-link: [`WARM_LIST_WORKFLOW.md`](WARM_LIST_WORKFLOW.md) · [`MARKET_SIGNAL_CLASSIFICATION.md`](MARKET_SIGNAL_CLASSIFICATION.md) · [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md) · [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md) · [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md)

---

## 0. Daily ritual — الطقس اليومي

A fixed 4-step open. Total time ≤ 45 minutes. No new contacts beyond the cadence.
افتتاحية ثابتة من 4 خطوات. الوقت الإجمالي ≤ 45 دقيقة. لا تتجاوز إيقاع التواصل.

1. **Read the Signal log (Section 3).** Any reply received in the last 24h is classified before anything else. Reply SLA: same working day, during working hours — promptly but not instant (`WARM_LIST_WORKFLOW.md` §4.1).
2. **Send the day's 5 contacts.** Cadence is 5 warm contacts/day, one outreach each — no automation, no second contact without a reply. Log each at *send time* in the Warm-list pipeline (Section 1).
3. **Advance the Partner pipeline (Section 2).** One honest status per active partner. Before promoting any partner stage, run [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md).
4. **Write the daily wrap** into [`../adoption/FRICTION_LOG.md`](../adoption/FRICTION_LOG.md): messages sent, replies, biggest objection (verbatim, anonymized), one change for tomorrow or "no change + reason".

اقرأ سجل الإشارات أولاً وصنّف كل رد · أرسل دفعة الـ5 وسجّلها وقت الإرسال · حدّث خط الشركاء بحالة صادقة واحدة · اكتب إغلاق اليوم في سجل الاحتكاك.

> No approval = no external action. No proof = no upsell. No repeated demand = no new feature.
> لا موافقة = لا إجراء خارجي · لا إثبات = لا ترقية · لا طلب متكرر = لا ميزة جديدة.

---

## 1. Warm-list pipeline — خط القائمة الدافئة

20 named contacts, 5/day over 4 days. Stage vocabulary from `WARM_LIST_WORKFLOW.md`. Decision values: `ACCEPT` · `DIAGNOSTIC_ONLY` · `REFRAME` · `REJECT` · `REFER_OUT` · `—` (no reply yet).

| # | Contact label | Channel | Sent date | Reply? | Decision | Stage | Next action + date |
|---|---|---|---|---|---|---|---|
| 1 | | wa / email | | y/n | | sent / replied / qualified / diagnostic_in_progress / sprint / closed / friction | |
| 2 | | | | | | | |
| 3 | | | | | | | |
| 4 | | | | | | | |
| 5 | | | | | | | |

> Add rows as contacts are sent. Stage `diagnostic_in_progress` starts the 24-hour clock. `sprint` = 499 SAR Proof Sprint accepted. Do not pitch the next rung without a recorded proof event.
> أضف صفوفًا عند الإرسال. `diagnostic_in_progress` يبدأ ساعة الـ24. لا تقترح الدرجة التالية بلا حدث إثبات مُسجَّل.

---

## 2. Partner pipeline — خط الشركاء

Partners (agencies, intro sources) move on a separate engagement track from warm contacts. Stage values are *engagement-pipeline* labels — they are **not** the L0–L5 proof ladder. Never promote a stage without [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md).

| Partner label | First touch date | Outreach stage | `founder_confirmed`? | Evidence (reply / thread / timestamp) | Next action + date |
|---|---|---|---|---|---|
| | | prepared_not_sent / first_touch_sent / replied / call_held / intro_made | y/n | | |
| | | | | | |

> `prepared_not_sent` is an honest default. A draft that was never sent is `prepared_not_sent`, not "in progress". Promote only on real evidence.
> `prepared_not_sent` هو الوضع الصادق الافتراضي. المسودة غير المُرسلة ليست "قيد التقدم".

---

## 3. Signal log — سجل الإشارات

Every incoming reply, classified the moment it is read. Signal names match [`MARKET_SIGNAL_CLASSIFICATION.md`](MARKET_SIGNAL_CLASSIFICATION.md).

| Date/time received | Source label | Raw message (short, anonymized) | Signal classification | Action taken + ledger entry |
|---|---|---|---|---|
| | | | replied_interested / meeting_booked / asks_for_pdf / asks_for_pricing / asks_for_scope / asks_for_english / asks_for_security / pilot_intro_requested / no_response_after_follow_up / invoice_paid | |
| | | | | |

> Same-working-day reply applies to `replied_interested` and `meeting_booked`. `no_response_after_follow_up` = mark and move on; no chasing.
> الرد في نفس يوم العمل للمهتمين والاجتماعات. لا مطاردة بعد انتظار الرد.

---

## 4. Ledgers and friction — السجلات والاحتكاك

The war room points; the ledgers are the record of truth. Update the matching ledger the same day a state changes.

| When this happens | Record it here |
|---|---|
| Qualify decision returned | [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) — event `qualify_decision` (canonical, per `WARM_LIST_WORKFLOW.md` §5) |
| Proof event used in a meeting | [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) |
| Invoice paid / revenue confirmed | [`../ledgers/VALUE_LEDGER.md`](../ledgers/VALUE_LEDGER.md) |
| Capital asset deposited (sector pattern, reusable draft) | [`../ledgers/CAPITAL_LEDGER.md`](../ledgers/CAPITAL_LEDGER.md) |
| Governance decision / refusal | [`../ledgers/GOVERNANCE_LEDGER.md`](../ledgers/GOVERNANCE_LEDGER.md) |
| Objection, decline, confusion, daily wrap | [`../adoption/FRICTION_LOG.md`](../adoption/FRICTION_LOG.md) |
| Outbound referral made | `referral_ledger` — see [`../ledgers/CLIENT_LEDGER.md`](../ledgers/CLIENT_LEDGER.md) |

> A proof pack without a Value Ledger entry is incomplete. Source-less claims are not recorded.
> حزمة إثبات بلا قيد في سجل القيمة = ناقصة. لا تُسجَّل ادعاءات بلا مصدر.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
