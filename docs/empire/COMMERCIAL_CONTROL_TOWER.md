# Commercial Control Tower — The Cockpit / برج القيادة التجاري

> The Control Tower is the cockpit that runs the whole commercial motion. It is
> not a report — it is the instrument panel the founder reads to decide what to
> do next. It works in three cadences: daily, weekly, monthly.
>
> برج القيادة هو قمرة القيادة التي تدير الحركة التجارية بأكملها. ليس تقريراً —
> بل لوحة الأدوات التي يقرأها المؤسس ليقرر الخطوة التالية. يعمل بثلاث وتائر:
> يومية، أسبوعية، شهرية.

**Date opened / تاريخ الفتح:** 2026-05-17
**Owner / المالك:** Founder
**Status / الحالة:** Strategic narrative — not a binding spec.

---

## 1. The daily cadence / الوتيرة اليومية

The daily view answers one question: did today move the motion forward?

العرض اليومي يجيب على سؤال واحد: هل دفع اليوم الحركة إلى الأمام؟

| Daily metric / مؤشر يومي | Read / القراءة |
|---|---|
| Messages sent / رسائل مُرسلة | Outreach volume to opted-in targets. |
| Follow-ups / متابعات | Follow-ups completed on open threads. |
| Replies / ردود | Genuine replies received. |
| Demos / عروض | Demos scheduled or run. |
| Scopes / نطاقات | Scopes drafted or sent. |
| Invoices / فواتير | Invoices issued. |
| Paid / commitments / مدفوع / التزامات | Payments and verbal commitments. |
| Proof Packs delivered / حِزم أدلة مُسلّمة | Proof Packs handed to customers. |
| Partner conversations / محادثات شركاء | Partner conversations held. |
| Affiliate leads / عملاء من المُحيلين | Leads arriving via affiliates. |
| Blocked risks / مخاطر معطّلة | Anything blocking progress. |
| Best message / أفضل رسالة | The message that worked best today. |
| Worst channel / أسوأ قناة | The channel that wasted effort. |
| Tomorrow's priority / أولوية الغد | The single most important next action. |

---

## 2. The weekly cadence / الوتيرة الأسبوعية

The weekly view answers: what is working, and what should stop?

العرض الأسبوعي يجيب: ما الذي ينجح، وما الذي يجب إيقافه؟

- Best segment / أفضل شريحة
- Best message / أفضل رسالة
- Best offer / أفضل عرض
- Best channel / أفضل قناة
- Where the funnel stopped / أين توقف القمع
- Which objection recurred / أي اعتراض تكرر
- Which partner brought quality / أي شريك جلب جودة
- Which affiliate brought noise / أي مُحيل جلب ضجيجاً
- What to double down on / ما الذي نضاعف التركيز عليه
- What to stop / ما الذي نوقفه
- What NOT to build / ما الذي لا نبنيه

---

## 3. The monthly cadence / الوتيرة الشهرية

The monthly view answers: is the company compounding?

العرض الشهري يجيب: هل تتراكم الشركة؟

| Monthly area / مجال شهري | Question / السؤال |
|---|---|
| Revenue / الإيراد | What was earned this month? |
| Pipeline / خط الأنابيب | What is realistically in motion? |
| Delivery / التسليم | What was delivered and at what quality? |
| Support / الدعم | What support load appeared? |
| Partners / الشركاء | How did the partner channel perform? |
| Governance / الحوكمة | Were the non-negotiables held everywhere? |
| Learning / التعلّم | What did the month teach? |
| Next strategic bet / الرهان الاستراتيجي التالي | What is the single next bet? |

---

## 4. The 90-day priority windows / نوافذ أولويات الـ90 يوماً

The Control Tower keeps the founder inside the right window. Each window has a
focus; numbers below are activity counts, not revenue commitments.

برج القيادة يبقي المؤسس داخل النافذة الصحيحة. لكل نافذة تركيز؛ والأرقام أدناه
عدّادات نشاط، لا التزامات إيراد.

| Window / النافذة | Focus / التركيز |
|---|---|
| Now (7 days) | Sample Proof Pack, Agency Proof Pilot one-pager, the Control Tower itself, 10 targets/day, 5 follow-ups/day, 1 partner conversation/day, **no feature building**. |
| 30 days | 1 paid pilot, 1 Proof Pack, 1 partner loop, 3 case-style insights, a clear winning message and ICP. |
| 60 days | 3 paid pilots, 1 Sprint proposal, 1 retainer candidate, 5 partners, a Proof Pack library, an objection engine. |
| 90 days | 5–8 paid pilots, 2 diagnostics, 1 Sprint, 1 retainer candidate, 10 partners, a mini benchmark report, a repeatable sales script. |

---

## 5. Where it lives in the system / أين يعيش في النظام

The Control Tower relates to the repo routers
`api/routers/command_center.py` and `api/routers/founder_dashboard.py`. Those
surface the daily and founder views. This doc defines the *intent* behind those
surfaces; the routers are the implementation.

برج القيادة يرتبط براوترات المستودع `api/routers/command_center.py` و
`api/routers/founder_dashboard.py`. هما يعرضان العرضين اليومي والمؤسس. هذه
الوثيقة تحدد *النية* خلف تلك الواجهات؛ والراوترات هي التنفيذ.

---

## Doctrine alignment / المواءمة مع الدستور

- The Control Tower carries no firm SAR targets; revenue is observed, not
  promised. / لا يحمل برج القيادة أهداف ريال ثابتة؛ الإيراد يُرصد لا يُوعَد به.
- "What NOT to build" is a deliberate guard against feature creep during the
  90-day windows.
- Outreach counts apply to opted-in targets only — no cold WhatsApp, no
  scraping, no bulk automation.

## Related docs / مراجع ذات صلة

- [`README.md`](README.md) — the Empire set and its 90-day priorities
- [`OFFER_LADDER.md`](OFFER_LADDER.md) — the offers the Tower tracks
- [`CUSTOMER_SUCCESS_EXPANSION.md`](CUSTOMER_SUCCESS_EXPANSION.md) — the expansion loop
- [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md) — canonical pricing
- [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) — hard limits
