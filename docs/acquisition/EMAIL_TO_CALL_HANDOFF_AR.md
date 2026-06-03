# Email-to-Call Handoff — دليل التشغيل (AR)

> القاعدة الذهبية: **كل إيميل مُرسل يجب أن يُنتج `follow_up_due_date` + `call_brief` + `next_action` + `owner`.** لا تضيع الفرصة بين الإيميل والمكالمة.
> مرجع المصطلحات والحالات: `AGENTS.md §5`. التقرير المرجعي: `reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md`.

---

## 1. الغرض (Purpose)

أكبر تسريب في الاستحواذ ليس في كتابة الإيميل، بل في ما **بعد** إرساله: لا أحد يعرف من يتابع، ومتى، وبأي مادة. الـ handoff يحوّل كل إيميل مُرسل إلى مهمة متابعة واضحة المالك.

```txt
CANONICAL RULE (AGENTS.md §5):
كل إيميل مُرسل يجب أن يُنتج:
  follow_up_due_date  +  call_brief  +  next_action  +  owner
```

إذا أُرسل إيميل بلا هذه الأربعة، فالعملية ناقصة ويجب إكمالها قبل اعتبار الشركة "تمت متابعتها".

---

## 2. مفهوم Handoff Queue

الـ Handoff Queue هي القائمة التي تجمع كل الشركات التي وصلت حالتها إلى `sent` فأكثر، وتنتظر الخطوة التالية. كل سطر فيها يحمل: الشركة، الحالة، المالك، الخطوة التالية، وتاريخ المتابعة.

```txt
[ Email sent ] ──► follow_up_due_date محسوب ──► Call Brief يُجهَّز ──► Caller يتصل
                                                          │
                                            owner واضح لكل سطر في الـ queue
```

الـ queue تمنع سقوط الفرص: لا سطر بلا `owner`، ولا سطر بلا `next_action`. التقرير المولّد لهذا يعيش في `reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md`.

---

## 3. حالات CRM للشركة (Company Status) — الترتيب القانوني

```txt
researched → need_card_ready → draft_ready → approved_to_send → sent
→ follow_up_due → call_brief_ready → called → interested → mini_proposal_ready
→ proposal_sent → won → delivery_started → active → renewal_candidate
```

حالات نهائية: `lost`, `do_not_contact`.

---

## 4. جدول: الحالة → المالك → الخطوة التالية

| الحالة | المالك | الخطوة التالية |
|---|---|---|
| `researched` | Dealix AI Agents | توليد Client Need Card. |
| `need_card_ready` | Dealix AI Agents | كتابة email draft + draft quality score. |
| `draft_ready` | Outreach Operator | مراجعة + رفع للـ Top 100 إن `total ≥ 75`. |
| `approved_to_send` | Founder | الموافقة على الإرسال. |
| `sent` | Outreach Operator | احتساب `follow_up_due_date` + تجهيز `call_brief` + تعيين `owner`. |
| `follow_up_due` | Outreach Operator | تشغيل follow-up sequence (cadence [3,7,14]) + تسليم للـ Caller. |
| `call_brief_ready` | Caller / Sales Follow-up | الاتصال (متصل بشري) باستخدام الـ Call Brief. |
| `called` | Caller / Sales Follow-up | تسجيل الرد + تحديد الاهتمام. |
| `interested` | Caller / Founder | تجهيز Mini Proposal (يتطلب موافقة founder). |
| `mini_proposal_ready` | Founder | الموافقة على الـ Mini Proposal. |
| `proposal_sent` | Outreach Operator | متابعة الرد على العرض. |
| `won` | Founder | الانتقال إلى delivery (يتطلب required_inputs). |
| `delivery_started` | Delivery Operator | تشغيل Delivery Pack بعد استلام required_inputs. |
| `active` | Delivery Operator | تسليم first output + weekly value report. |
| `renewal_candidate` | Founder | تقييم التجديد/التوسّع. |
| `lost` / `do_not_contact` | — | حالة نهائية؛ تحترم suppression list. |

---

## 5. مثال عملي على سطر في الـ Queue

```txt
Company:            شركة تدريب في الرياض
Status:             follow_up_due
Email sent:         "آخر متابعة لم تحدث قد تكون أغلى فرصة" (followup_recovery_os)
follow_up_due_date: 2026-06-06   (بعد 3 أيام — أول خطوة في cadence [3,7,14])
call_brief:         CB-101 (ready)
next_action:        اتصال بشري عبر Call Brief CB-101 + بدء follow-up sequence FUS-101
owner:              Caller / Sales Follow-up
```

كل العناصر الأربعة المطلوبة موجودة: `follow_up_due_date` + `call_brief` (CB-101) + `next_action` + `owner`.

---

## 6. قواعد الأمان في الـ Handoff

```txt
- لا إرسال قبل approved_to_send (موافقة founder).
- كل sent يولّد فورًا: follow_up_due_date + call_brief + next_action + owner.
- الاتصال بشري فقط — لا اتصال آلي.
- Mini Proposal لا يُرسل قبل موافقة founder.
- delivery لا يبدأ قبل required_inputs.
- الشركات في do_not_contact / suppression list لا تدخل الـ queue.
```

> التقرير المرجعي: `reports/acquisition/EMAIL_TO_CALL_HANDOFF_QUEUE.md` (مولّد عبر `scripts/generate_acquisition_reports.py` / `npm run os:reports`).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
