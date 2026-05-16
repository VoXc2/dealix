# Commercial Evidence State Machine (CEL)

> Canonical spec for how a commercial engagement progresses, and the evidence
> required at each step. This is the single source of truth for the backend
> module `auto_client_acquisition/commercial_os/` and the Ops Console UI.

## Why this exists

Dealix is a **Governed Revenue & AI Operations Company**. Every commercial claim
must be backed by evidence: a clear source, an explicit approval, a documented
artifact, and a measurable outcome. The Commercial Evidence State Machine makes
that auditable — a deal cannot *claim* a stage it has not *earned*.

## CEL vs. proof/autonomy L0–L5 — two separate axes

The repo already uses **L0–L5** for an unrelated axis: proof / autonomy levels
(see `/api/v1/decision-passport/evidence-levels`). That axis answers *"how much
autonomy may an agent take, and how strong is the proof artifact?"*

**Commercial Evidence Level (CEL)** is a **different, orthogonal axis**. It
answers *"how far has this commercial engagement progressed, and what evidence
proves it?"* The two never substitute for each other. To avoid collision, the
commercial axis is always written with the `CEL` prefix.

| Axis | Prefix | Question it answers |
|------|--------|---------------------|
| Proof / autonomy | `L0`–`L5` | How strong is the proof artifact / how much autonomy is allowed? |
| Commercial evidence | `CEL2`–`CEL7` | How far has the commercial engagement progressed? |

## States and levels

| State | CEL | Meaning |
|-------|-----|---------|
| `prepared_not_sent` | `CEL2` | Outreach drafted and staged. Nothing sent. |
| `sent` | `CEL4` | Founder-approved message actually sent. |
| `replied_interested` | `CEL4` | Recipient replied with interest. |
| `meeting_booked` | `CEL4` | A meeting is scheduled. |
| `used_in_meeting` | `CEL5` | A Dealix artifact was used in a real meeting. |
| `scope_requested` | `CEL6` | Prospect asked for a scope / proposal. |
| `pilot_intro_requested` | `CEL6` | Prospect asked for a pilot or an intro. |
| `invoice_sent` | `CEL7_candidate` | An invoice has been issued. |
| `invoice_paid` | `CEL7_confirmed` | Payment received and reconciled. |

There is deliberately no `CEL1` or `CEL3`. The numbering mirrors the founder's
operating language and leaves room without implying intermediate states that
carry no evidence.

## Transition table

```
(start)              -> prepared_not_sent        CEL2
prepared_not_sent     -> sent                      CEL4   [requires founder_confirmed]
sent                  -> replied_interested        CEL4
sent                  -> (silent / not_interested) CEL4   [classified, terminal-ish]
replied_interested    -> meeting_booked            CEL4
meeting_booked        -> used_in_meeting           CEL5
used_in_meeting       -> scope_requested           CEL6
used_in_meeting       -> pilot_intro_requested     CEL6
scope_requested       -> invoice_sent              CEL7_candidate
pilot_intro_requested -> invoice_sent              CEL7_candidate
invoice_sent          -> invoice_paid              CEL7_confirmed
```

A reply classification (`interested` / `silent` / `not_interested`) is always
recorded, including silence — an unclassified send is incomplete evidence.

## The five hard rules

These are enforced by `commercial_os/transitions.py::validate_transition` and by
the `POST /api/v1/evidence/events` endpoint (illegal transitions return `422`).

1. **No `sent` without `founder_confirmed=true`.** A draft never leaves the
   building without an explicit founder approval recorded.
2. **No `CEL5` without `used_in_meeting`.** A meeting being *booked* is not a
   meeting where a Dealix artifact was *used*.
3. **No `CEL6` without a scope or intro request.** Pull must come from the
   prospect; interest alone is not pull.
4. **No `CEL7_confirmed` without payment.** `invoice_sent` is only a candidate.
5. **No revenue recognized before `invoice_paid`.** Reporting, the North Star
   count, and the value ledger all read `CEL7_confirmed`, never `CEL7_candidate`.

## Relationship to the 11 non-negotiables

This state machine *is* the enforcement surface for several non-negotiables:
rule 1 implements "no external action without approval"; rule 5 implements "no
fake / un-sourced claims" and "no guaranteed sales outcomes" by refusing to
recognize revenue that has not been paid.

## بالعربية — موجز

**آلة الحالة للأدلة التجارية (CEL)** تجعل تقدّم أي صفقة قابلاً للتدقيق: لا
مرحلة تُدّعى دون دليل. المحور `CEL2`–`CEL7` منفصل تماماً عن محور البرهان/الاستقلالية
`L0`–`L5` الموجود في المستودع. القواعد الخمس الصارمة: لا إرسال دون موافقة المؤسس،
لا `CEL5` دون استخدام فعلي في اجتماع، لا `CEL6` دون طلب نطاق/تعريف من العميل،
لا `CEL7_confirmed` دون دفع، ولا اعتراف بإيراد قبل `invoice_paid`.
