# L4 Truth Check — فحص الصدق قبل التصرّف على مرحلة تواصل

> A checklist and decision tree that forces honesty about *claimed* outreach stages
> before the founder acts on them. Use it whenever you are about to release a
> follow-up that assumes an earlier message was already sent.
> قائمة فحص وشجرة قرار تفرض الصدق بشأن مراحل التواصل *المُدّعاة* قبل التصرّف عليها.
>
> Cross-link: [`WARM_LIST_WORKFLOW.md`](WARM_LIST_WORKFLOW.md) · [`FOUNDER_SIGNAL_WAR_ROOM.md`](FOUNDER_SIGNAL_WAR_ROOM.md) · [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) · [`../institutional/DEALIX_CONSTITUTION.md`](../institutional/DEALIX_CONSTITUTION.md)

---

## 0. Two different "L" things — لا تخلط بين مفهومين

This document exists to stop one specific mistake: treating an outreach stage as if it were a proof level.

- **The L0–L5 ladder is the *proof-publication* ladder.** It governs when a piece of evidence can be reused: L0 planned, L1 internal draft, L2 customer-reviewed/private, L3 customer-approved/private sales proof, L4 public-publish approved (case study), L5 revenue/expansion evidence. Source of truth: `auto_client_acquisition/proof_engine/evidence.py`. There is no L6 or L7.
- **An "outreach stage" is a separate engagement-pipeline concept.** When the founder says "this partner is at L4", that is *shorthand*, not the proof ladder. It means "I believe this conversation reached an advanced stage." This doc verifies whether that belief is true.

> Never write an outreach stage into the proof ladder, and never publish a proof level off the back of an outreach belief.
> لا تُسجِّل مرحلة تواصل في سلّم الإثبات، ولا تنشر مستوى إثبات بناءً على انطباع تواصل.

سلّم L0–L5 هو سلّم *نشر الإثبات* فقط (لا يوجد L6/L7). "مرحلة التواصل" مفهوم منفصل في خط التفاعل. هذه الوثيقة تتحقق هل الانطباع حقيقي.

---

## 1. The truth checklist — قائمة الصدق

Run all five before promoting any partner or contact stage. Any "no" or "unknown" fails the check.

| # | Question | Pass condition | السؤال بالعربية |
|---|---|---|---|
| 1 | Was a message **actually sent**? | A real send exists — not a draft, not a plan, not "I meant to". | هل أُرسلت رسالة فعليًا؟ |
| 2 | Is `founder_confirmed = true` for that send? | The founder personally confirms the send in the engagement record. | هل `founder_confirmed = true`؟ |
| 3 | Is there a **timestamp**? | A real send time is recorded (channel log, sent folder, message header). | هل يوجد ختم زمني للإرسال؟ |
| 4 | Is there **evidence of receipt or reply**? | A reply, a read marker, or a thread the other side touched. | هل يوجد دليل استلام أو رد؟ |
| 5 | Is the stage consistent with the ledgers? | The claimed stage matches what `FOUNDER_SIGNAL_WAR_ROOM.md` and the ledgers show. | هل المرحلة متّسقة مع السجلات؟ |

> Checks 1–3 prove the message left the founder. Check 4 proves the other side engaged. Check 5 proves the record is not drifting from reality.
> الفحوص 1–3 تثبت أن الرسالة غادرت. الفحص 4 يثبت تفاعل الطرف الآخر. الفحص 5 يثبت أن السجل لم ينحرف.

---

## 2. Decision tree — شجرة القرار

```
Claimed advanced outreach stage
        |
        v
Checks 1, 2, 3 ALL pass?  (sent + founder_confirmed + timestamp)
        |
   no --+--> NOT REAL: the message was never genuinely sent.
        |        - Correct the record to outreach stage = prepared_not_sent.
        |        - Send the GENUINE first-touch now (warm-list one-line ask
        |          or partner first-touch), per WARM_LIST_WORKFLOW.md.
        |        - Log the corrected state in FOUNDER_SIGNAL_WAR_ROOM.md.
        |        - STOP. Do not release any follow-up.
        |
  yes --+--> Check 4 passes? (evidence of receipt or reply)
                 |
            no --+--> SENT BUT SILENT: message is real, no engagement yet.
                 |        - Stage = first_touch_sent (not "in progress").
                 |        - No unsolicited follow-up. A second message goes
                 |          out only if a follow-up window was explicitly
                 |          agreed (WARM_LIST_WORKFLOW §1). Otherwise wait
                 |          7 days, then no_response_after_follow_up. No
                 |          chasing.
                 |
           yes --+--> Check 5 passes? (consistent with ledgers)
                          |
                     no --+--> RECORD DRIFT: reconcile first.
                          |        - Fix the war room / ledger to match
                          |          the evidence, THEN re-run this tree.
                          |
                    yes --+--> REAL: the stage is verified.
                                   - Release the prepared follow-up.
                                   - Classify any reply via
                                     MARKET_SIGNAL_CLASSIFICATION.md.
```

---

## 3. Outcomes — المخرجات

| Outcome | What it means | The honest action |
|---|---|---|
| **REAL** | Sent, confirmed, timestamped, engaged, consistent. | Release the prepared follow-up. Then classify the reply. |
| **SENT BUT SILENT** | Real send, no reply yet. | Hold at `first_touch_sent`. No unsolicited follow-up — a second message only if a window was agreed (`WARM_LIST_WORKFLOW.md` §1); otherwise wait 7 days, then stop. |
| **RECORD DRIFT** | Send is real but the recorded stage is wrong. | Reconcile the record, re-run the tree. |
| **NOT REAL** | No genuine send behind the claim. | Set `prepared_not_sent`, send the real first-touch, log the correction. |

> The most expensive mistake is sending a "thanks for the great call" follow-up when the first message was never delivered. This check costs two minutes and prevents it.
> أغلى خطأ هو إرسال متابعة "شكرًا على المكالمة" بينما الرسالة الأولى لم تصل أصلًا. هذا الفحص يكلّف دقيقتين ويمنع ذلك.

> No fake proof. No source-less claim. A belief is not evidence until checks 1–5 pass.
> لا إثبات زائف. لا ادعاء بلا مصدر. الانطباع ليس دليلًا حتى تنجح الفحوص الخمسة.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
