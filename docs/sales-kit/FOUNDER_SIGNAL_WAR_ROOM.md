# Revenue War Room — غرفة عمليات الإيراد

> The one surface the founder opens every morning. Part tracking surface, part operating playbook.
> Part A is filled in daily. Part B is the reference you read from, not into.
> السطح الوحيد الذي يفتحه المؤسس كل صباح. جزء سطح تتبّع، وجزء دليل تشغيل.
> الجزء (أ) يُملأ يوميًا. الجزء (ب) مرجع تقرأ منه لا فيه.
>
> **Supersedes the v1 "Founder Signal War Room" tracking sheet — same file path, expanded scope.**
> **يحلّ محل نسخة "غرفة عمليات الإشارات" v1 — نفس المسار، نطاق موسّع.**
>
> Cross-link: [`WARM_LIST_WORKFLOW.md`](WARM_LIST_WORKFLOW.md) · [`MARKET_SIGNAL_CLASSIFICATION.md`](MARKET_SIGNAL_CLASSIFICATION.md) · [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md) · [`CONDITIONAL_BUILD_TRIGGERS.md`](CONDITIONAL_BUILD_TRIGGERS.md) · [`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) · [`../AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md) · [`../GTM_PLAYBOOK.md`](../GTM_PLAYBOOK.md) · [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)

---

## The governing sentence — الجملة الحاكمة

> You don't sell Dealix by explaining the whole product. You sell it by picking **one painful workflow**,
> proving where the leak is, offering a **small pilot**, delivering a Proof Pack, then opening a Sprint,
> a Retainer, or a Partner loop.
>
> تصريف Dealix لا يكون بشرح كل المنتج. يكون باختيار **workflow واحد مؤلم**، إثبات موضع الخلل،
> عرض **Pilot صغير**، تسليم Proof Pack، ثم فتح Sprint أو Retainer أو Partner loop.

> No approval = no external action. No proof = no upsell. No repeated demand = no new feature. No payment = no "Revenue Live".
> لا موافقة = لا إجراء خارجي · لا إثبات = لا ترقية · لا طلب متكرر = لا ميزة جديدة · لا دفع = لا "إيراد حيّ".

---

# Part A — Daily surface (fill these in) — الجزء (أ): السطح اليومي

## 1. Daily execution engine — محرّك التشغيل اليومي

The morning open is a fixed ritual, ≤ 45 minutes. The day has three checkpoints.
الافتتاحية طقس ثابت ≤ 45 دقيقة. اليوم له ثلاث نقاط تفتيش.

**Morning open — الافتتاحية:**
1. **Read the Signal log (§5).** Classify every reply from the last 24h before anything else. Reply SLA: within 24 hours, never sooner than 1 hour (`WARM_LIST_WORKFLOW.md` §4.1).
2. **Pick the top 10 targets** for today's approved touches (P0). Draft each message; nothing sends without your approval.
3. **Review the 5 follow-ups** due today from the War Room board (§2).
4. **Prepare a proof asset** for each warm lead (sample Proof Pack, Risk Score, Decision Passport example).
5. **Advance the Partner pipeline (§4).** One honest status per active partner. Run [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md) before promoting any stage.
6. **Review invoices and support escalations.**

**During the day — أثناء اليوم:** manual sends only · warm replies · demos · partner calls · scope pushes.

**End of day — إغلاق اليوم:** update the scorecard · note what worked / what failed · write the next 3 actions for tomorrow · record one no-build decision · write the daily wrap into [`../adoption/FRICTION_LOG.md`](../adoption/FRICTION_LOG.md).

> اقرأ سجل الإشارات وصنّفه · اختر أعلى 10 أهداف ووافق على رسائلها · راجع 5 متابعات · جهّز أصل إثبات لكل lead دافئ · حدّث خط الشركاء · راجع الفواتير والتصعيد · أغلق اليوم بسجل الاحتكاك.

### P0 — the one metric that cannot slip — المقياس الذي لا يسقط

**10 approved touches per day**, manual, human-approved. No automation, no second contact without a reply.
The named warm-list cadence (5 contacts/day from the 20-contact list, `WARM_LIST_WORKFLOW.md`) is a **sub-set** of the 10 — the remaining touches are partner outreach, follow-ups, and inbound replies.

**10 لمسات معتمدة يوميًا**، يدويّة وبموافقة بشرية. لا أتمتة، ولا تواصل ثانٍ بلا رد. إيقاع القائمة الدافئة (5/يوم) جزء من الـ10.

### Daily dashboard block — لوحة اليوم

```
Today / اليوم:
- 10 approved touches
- 5 follow-ups
- 1 founder post
- 1 partner conversation
- 1 scorecard update

Revenue / الإيراد:
- conversations · meetings · scopes · invoices sent · paid

Risks / المخاطر:
- no live send · no cold WhatsApp · no fake proof · no revenue claim before payment
```

---

## 2. The War Room board — لوحة غرفة العمليات

The master table. Every active target is one row. Seven columns, no more.
الجدول الرئيسي. كل هدف نشط = صف واحد. سبعة أعمدة فقط.

| # | Target / الهدف | Segment / الشريحة | Pain hypothesis / فرضية الألم | Offer / العرض | Proof asset / أصل الإثبات | Next action + date / الخطوة التالية + التاريخ | Status / الحالة |
|---|---|---|---|---|---|---|---|
| 1 | | agency / b2b_service / consulting | | | | | not_contacted |
| 2 | | | | | | | |
| 3 | | | | | | | |

> Add rows as targets enter the board. **No row may exist without a `Next action + date`.** Status uses the §3 vocabulary.
> أضف صفوفًا عند دخول الأهداف. **لا صف بلا خطوة تالية وتاريخ.** الحالة من قاموس §3.

---

## 3. Lifecycle states — حالات دورة الحياة

The 15 War Room states. This is a **standalone War Room board vocabulary** — it is *orthogonal to*
the CRM v10 `Lead`/`Deal` stage machine (`auto_client_acquisition/crm_v10/stage_machine.py`) and does
not replace it. The War Room board tracks founder-led motion; CRM v10 tracks system objects.

هذه 15 حالة للوحة غرفة العمليات — **قاموس مستقل** ومنفصل عن آلة مراحل CRM v10، ولا يحلّ محلّها.

```
not_contacted        → message_drafted     → approved_to_send   → sent_manual
→ replied            → proof_pack_sent     → meeting_booked     → scope_requested
→ invoice_sent       → paid                → delivery_started   → proof_pack_delivered
→ upsell_candidate   → referral_requested
closed_lost          (terminal — from any state)
```

| State | Meaning | Gate to leave it |
|---|---|---|
| `not_contacted` | On the board, no touch yet | Draft a message |
| `message_drafted` | Draft ready, not approved | Founder approves |
| `approved_to_send` | Approved, not yet sent | Manual send |
| `sent_manual` | Sent by hand, awaiting reply | A reply arrives |
| `replied` | Live conversation | Send proof / book meeting |
| `proof_pack_sent` | Sample proof shared | Lead engages |
| `meeting_booked` | Demo / call scheduled | Hold the meeting |
| `scope_requested` | Lead asked for scope | Draft scope (needs approval to send) |
| `invoice_sent` | Invoice issued | Payment clears |
| `paid` | Payment received — **now** "Revenue Live" is true | Start delivery |
| `delivery_started` | 7-day sprint running | Proof Pack assembled |
| `proof_pack_delivered` | Signed Proof Pack handed over | Confirm value |
| `upsell_candidate` | Value confirmed, next rung visible | Pitch Sprint / Retainer |
| `referral_requested` | Asked for a warm referral | Referral logged |
| `closed_lost` | No path forward — record reason | — |

> `paid` is the only state from which "Revenue Live" may be claimed. Estimated ≠ verified.
> `paid` هي الحالة الوحيدة التي يجوز فيها ادعاء "إيراد حيّ". التقديري ليس متحقَّقًا.

---

## 4. Pipelines — خطوط الأنابيب

### 4.1 Warm-list pipeline — خط القائمة الدافئة

20 named contacts, 5/day over 4 days. Stage vocabulary from `WARM_LIST_WORKFLOW.md`. Decision values: `ACCEPT` · `DIAGNOSTIC_ONLY` · `REFRAME` · `REJECT` · `REFER_OUT` · `—` (no reply yet).

| # | Contact label | Channel | Sent date | Reply? | Decision | Status (§3) | Next action + date |
|---|---|---|---|---|---|---|---|
| 1 | | wa / email | | y/n | | not_contacted | |
| 2 | | | | | | | |

> Stage `delivery_started` begins the sprint clock. Do not pitch the next rung without a recorded proof event.
> `delivery_started` يبدأ ساعة السبرنت. لا تقترح الدرجة التالية بلا حدث إثبات مُسجَّل.

### 4.2 Partner pipeline — خط الشركاء

Partners (agencies, intro sources) move on a separate engagement track. Stage values are *engagement-pipeline* labels — **not** the L0–L5 proof ladder. Never promote a stage without [`L4_TRUTH_CHECK.md`](L4_TRUTH_CHECK.md). Partner terms are governed by [`../AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md).

| Partner label | First touch date | Outreach stage | `founder_confirmed`? | Evidence (reply / thread / timestamp) | Next action + date |
|---|---|---|---|---|---|
| | | prepared_not_sent / first_touch_sent / replied / call_held / intro_made | y/n | | |

> `prepared_not_sent` is the honest default — a draft that was never sent is not "in progress".
> `prepared_not_sent` هو الوضع الصادق الافتراضي للمسودة غير المُرسلة.

### 4.3 Signal log — سجل الإشارات

Every incoming reply, classified the moment it is read. Signal names match [`MARKET_SIGNAL_CLASSIFICATION.md`](MARKET_SIGNAL_CLASSIFICATION.md).

| Date/time received | Source label | Raw message (short, anonymized) | Signal classification | Action taken + ledger entry |
|---|---|---|---|---|
| | | | replied_interested / meeting_booked / used_in_meeting / qualify_decision_returned / pilot_intro_requested / asks_for_pdf / asks_for_english / asks_for_scope / asks_for_pricing / asks_for_security / no_response_after_follow_up / low_intent / not_interested / invoice_sent / invoice_paid | |

> Reply within 24 hours (never sooner than 1 hour). `no_response_after_follow_up` = mark and move on; no chasing.
> الرد خلال 24 ساعة (وليس قبل ساعة). لا مطاردة بعد انتظار الرد.

---

## 5. Weekly distribution review — المراجعة الأسبوعية للتوزيع

Once a week, answer all 11. Then decide.
مرة كل أسبوع، أجب عن الـ11 كلها. ثم قرّر.

1. Best segment? — أفضل شريحة؟
2. Best message? — أفضل رسالة؟
3. Best channel? — أفضل قناة؟
4. Top objection? — أعلى اعتراض؟
5. Best partner source? — أفضل مصدر شريك؟
6. Highest lead-magnet conversion? — أعلى تحويل lead magnet؟
7. Where does the funnel stall? — أين يتوقف القمع؟
8. Is the price right? — هل السعر مناسب؟
9. Is the proof strong enough? — هل الإثبات قوي؟
10. What do we stop? — ماذا نوقف؟
11. What do we double down on? — ماذا نضاعف؟

**Weekly decision — one of:** scale a channel · fix a message · change the ICP · improve the Proof Pack · pause a weak affiliate · plan a webinar · **no-build**.
**القرار الأسبوعي — واحد من:** توسيع قناة · إصلاح رسالة · تغيير ICP · تحسين Proof Pack · إيقاف شريك ضعيف · تخطيط webinar · **لا بناء**.

---

# Part B — Playbook / reference — الجزء (ب): الدليل المرجعي

## 6. Channel playbooks — أدلّة القنوات

Each channel has one job. Do not run them all the same way.
لكل قناة وظيفة واحدة. لا تشغّلها كلها بنفس الأسلوب.

| Channel | Job | Allowed | Forbidden | Daily routine |
|---|---|---|---|---|
| **LinkedIn** | Trust + warm conversations | Founder posts; comments on target accounts; connection requests; manual DM **after** a request is accepted | Automation; scraping; mass DMs; inflated claims | 5 comments · 5 connection requests · 2 manual DMs (post-accept) · 1 founder post |
| **Email** | Structured outreach + partner proposals | Personalized, short, one clear CTA | False urgency; guaranteed ROI; purchased lists | Personalized sends to agencies / CRM consultants / B2B operators / founders with public emails |
| **WhatsApp** | Warm / opt-in / existing relationship **only** | Inbound leads; existing relationships; explicit consent; manual warm intros | Cold blast; unsolicited mass messages; outbound automation (`NO_COLD_WHATSAPP`) | Reply to inbound; warm intros only |
| **Partners** | Borrowed trust + distribution | Marketing agencies, CRM implementers, AI consultants, GRC advisors, communities, accelerators | Same forbidden list as above | 1 partner conversation/day |
| **Webinars** | Educate market + capture demand | Run **after** clear ICP + message + sample Proof Pack + Risk Score + a partner co-host exist | Launching with no ICP or no proof | Plan only when triggers met |
| **Paid ads** | Amplify a *proven* message | Start **after** 3–5 meetings + 2 recurring objections + 1 proof-pack request + 1 clear ICP | Starting before the message is proven | Off until triggers met |

> اللينكدإن للثقة، الإيميل للتواصل المنظّم، الواتساب للعلاقات الدافئة فقط، الشركاء للتوزيع، الويبينار والإعلانات بعد تحقّق الشروط.

---

## 7. The agency wedge — وتد الوكالات

Start with marketing agencies and marketing-service providers. One segment, four ways to win:
ابدأ بالوكالات ومزوّدي خدمات التسويق. شريحة واحدة، أربع طرق للفوز:

1. They **buy** Dealix — they live the follow-up pain.
2. They **refer** you to their clients.
3. They **resell** it as an added package.
4. They become an **implementation / partner channel**.

**The core message:** *You bring leads to your clients. Dealix helps you prove what happens after the lead — who was contacted, who replied, who needs follow-up, the best next action, and the evidence you hand the client.*

**رسالتك:** أنتم تجيبون الـleads لعملائكم. Dealix يثبت ماذا حدث بعد الـlead: من تواصل، من رد، من يحتاج متابعة، أفضل خطوة تالية، والدليل الذي تقدّمونه للعميل.

**The Agency Partner Pilot** — outputs: 1 client workflow · 10 opportunities · follow-up drafts · a lead status board · a Proof Pack · a co-selling / referral model.
**CTA:** *Let's try it on one client only.* / **الدعوة:** خلّونا نجرّب على عميل واحد فقط.

> Partner types, terms, and onboarding live in [`../AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md). "Start flexible, keep terms simple, push for one pilot or one referral."

---

## 8. Maturity-based packaging — التغليف حسب نضج العميل

Do not show the whole catalog. Match the rung to the lead's maturity. **Prices are the single source of
truth in `auto_client_acquisition/finance_os/pricing_catalog.py` and [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)** — quote from there, never invent numbers here.

لا تعرض كل الكتالوج. طابق الدرجة مع نضج العميل. **الأسعار مرجعها الوحيد كتالوج الأسعار** — اقتبس منه.

| Lead maturity | Offer (canonical tier) | Price (SAR) | Use when |
|---|---|---|---|
| Cold visitor | Free Risk Score / sample Proof Pack | — | Capture demand, qualify |
| Warm, exploring | **Free Growth Diagnostic** (`diagnostic`) | 0 | 30–60 min, pipeline assessment + 3 recommendations |
| Interested, price-sensitive | **Growth Starter Pilot** (`growth_starter_pilot`) | 499 | First proof fast; hesitant lead; agency trying one client |
| Has a messy list | **Data to Revenue** (`data_to_revenue`) | 1,500 | List cleanup + contactability score + segmented drafts |
| Validated, ongoing workflow | **Executive Growth OS** (`executive_growth_os`) | 2,999/mo | Recurring follow-ups, weekly brief, monthly Proof Pack |
| Partnership motion | **Partnership Growth** (`partnership_growth`) | 3,000+ project | Partner discovery, fit-score, co-branded Proof Pack |

### Conversion ladder — سلّم التحويل

```
Cold visitor        → Free Risk Score
Warm lead           → Sample Proof Pack
Interested lead     → Free Growth Diagnostic
Price-sensitive     → Growth Starter Pilot (499)
Has messy data      → Data to Revenue (1,500)
Validated, ongoing  → Executive Growth OS (2,999/mo)
Agency              → Agency Partner Pilot
Strong agency       → Co-selling partner
```

> Note: any price band beyond this table (e.g. larger custom diagnostics or sprints) is introduced **only** after the catalog and `OFFER_LADDER_AND_PRICING.md` are updated — the War Room never overrides the catalog.
> ملاحظة: أي شريحة سعرية خارج هذا الجدول تُضاف فقط بعد تحديث الكتالوج — غرفة العمليات لا تتجاوزه.

---

## 9. Message library — مكتبة الرسائل

All messages are **drafts** until founder-approved. All bilingual where the lead expects Arabic.
كل الرسائل **مسودّات** حتى موافقة المؤسس.

**Intro — agency (AR):**
> السلام عليكم [الاسم]، وصلت لكم لأن شغلكم قريب من التسويق وخدمة العملاء. Dealix نظام سعودي يساعد الوكالات على ترتيب متابعة العملاء من واتساب/الإيميل/نماذج الموقع، يصنّف الردود، يجهّز رسائل متابعة، ويربطها بحجز ديمو أو عرض سعر بدل ما تضيع الـleads بعد الحملة. الفكرة لكم كشريك أيضًا: نجرّبها على عميل واحد ونثبّت النتيجة بـProof Pack. يناسبكم ديمو 10 دقائق؟

**Follow-up — 24h (AR):**
> متابعة سريعة فقط. إذا عندكم leads تضيع بعد الإعلان أو بعد أول رسالة، أقدر أوريكم خلال 10 دقائق كيف Dealix يحوّلها إلى مسار متابعة وحجز.

**Follow-up — 72h, last (AR):**
> آخر متابعة مني هنا. إذا التوقيت غير مناسب أوقف الرسائل، وإذا فيه اهتمام أرسل لكم مثالًا عمليًا مخصصًا لنشاطكم قبل أي اجتماع.

**Partner intro (AR):**
> السلام عليكم [الاسم]، أبني Dealix كنظام سعودي يحوّل الـleads والمتابعة وworkflows الذكاء الاصطناعي إلى تشغيل محكوم: رسائل، متابعة، موافقات، Proof Pack، وقرارات واضحة. أرى زاوية شراكة مناسبة: أنتم تجيبون العلاقة، وDealix يشغّل التشخيص والـProof Pack. اقتراحي نبدأ بعميل واحد فقط بدون التزام كبير. يناسبك ديمو 10 دقائق هذا الأسبوع؟

**Post-demo (AR):**
> ممتاز. بناءً على ما شفناه، أفضل خطوة ليست اشتراكًا كبيرًا الآن. نبدأ بـDiagnostic/Pilot صغير على workflow واحد: 10 فرص أو leads، نرتّب المتابعة، نطلع Proof Pack، وبعدها نقرّر إذا يستاهل ترقية.

> English versions are produced on request (`asks_for_english` signal). Keep them short, one CTA, no guaranteed ROI.

---

## 10. Closing system — نظام الإغلاق

Don't close on features. Close on: one specific problem · one workflow · a Proof Pack · one clear decision · a small entry price.
لا تغلق بالميزات. اغلق بمشكلة محددة، workflow واحد، Proof Pack، قرار واحد، سعر دخول صغير.

**Close script (AR):**
> اللي أقترحه ما نبدأ كبير. نأخذ workflow واحد فقط — leads من حملة، أو رسائل واتساب/إيميل، أو متابعة المبيعات، أو قائمة عملاء. نطلع خلال 7 أيام: أين تضيع الفرص، من يحتاج متابعة، الرسائل المقترحة، المخاطر، وProof Pack. إذا شفتوا قيمة نكمل. إذا لا، نوقف عند التشخيص.

**Objection — price:** Instead of cutting price, cut risk — start a smaller pilot on one client/workflow; after the Proof Pack they decide on scale.
**اعتراض السعر:** بدل خفض السعر، خفّض المخاطرة — Pilot أصغر، وبعد Proof Pack يقرّرون التوسّع.

**Objection — "we have a CRM":** Dealix does not replace the CRM. It answers: *does the data in the CRM lead to follow-up, a decision, and value?* If the CRM exists but follow-up or proof is weak — that's the value.
**اعتراض "عندنا CRM":** Dealix لا يستبدل الـCRM، بل يجيب: هل بيانات الـCRM تؤدي إلى متابعة وقرار وقيمة؟

**Objection — "we have an agency":** Dealix can serve the agency itself — the agency brings the leads and campaigns; Dealix proves what happened after the lead.
**اعتراض "عندنا وكالة":** Dealix يخدم الوكالة نفسها — هي تجيب الـleads، وDealix يثبت ما حدث بعدها.

---

## 11. Proof-led selling — البيع المقوَّد بالإثبات

Every sale leans on proof.
كل بيع يستند إلى إثبات.

- **Before the sale:** sample Proof Pack · Risk Score · demo · Decision Passport example.
- **During the sale:** live workflow simulation · GTM first-10 · sales script · proof demo.
- **After the sale:** client Proof Pack · value confirmation · upsell path · referral ask.

**The rule:** never say "Dealix increases revenue." Say "Dealix proves where opportunities leak and what the next decision is."
**القاعدة:** لا تقل "Dealix يزيد الإيراد". قل "Dealix يثبت أين تضيع الفرص وما القرار التالي".

---

## 12. Partner & affiliate ops — تشغيل الشركاء والإحالة

A Google Sheet / Airtable is enough for now — no portal yet. Columns:
`partner_name · type · audience · fit_score · approved · referral_code · leads_submitted · qualified_leads · meetings · paid_deals · commission_due · compliance_status · next_action`.

| Partner type | Commission | Basis | Entry requirement |
|---|---|---|---|
| Referral Partner | **15%** | First payment only | Verbal/written agreement |
| Implementation Partner | **20–25%** | Every payment, life of relationship | ≥1 successful pilot as a customer first + signed agreement |
| Co-Selling Partner | **25–30%** | Every payment, life of relationship | ≥3 completed Proof Packs + signed agreement |
| White-label | — | — | **Only** after 3 completed Proof Packs |

> Commission bands are the canonical ones in [`../AGENCY_PARTNER_PROGRAM.md`](../AGENCY_PARTNER_PROGRAM.md) §2 — do not restate alternative numbers.

**Conditions:** no payout before `invoice_paid` · no misleading claims · disclosure required · approved messages only · no spam · no cold WhatsApp in Dealix's name. Start with ~5 trusted partners under manual review.
**الشروط:** لا دفع قبل سداد الفاتورة · لا ادعاءات مضللة · إفصاح مطلوب · رسائل معتمدة فقط · لا spam · لا واتساب بارد باسم Dealix.

---

## 13. Automation matrix — مصفوفة الأتمتة

Self-run as much as possible — but the boundary is fixed.
شغّل ذاتيًا قدر الإمكان — لكن الحدّ ثابت.

| Auto (no approval) — ذاتي | Needs approval — يحتاج موافقة | Forbidden now — ممنوع الآن |
|---|---|---|
| lead capture · lead scoring · routing | external message | LinkedIn automation |
| sample Proof Pack delivery **after consent** | invoice send | scraping |
| meeting-brief draft · scope draft · invoice draft | scope send | cold WhatsApp |
| follow-up reminders | discount · refund | live payment charge |
| support classification · KB search · low-risk support answers | case study | fake proof |
| evidence logging · scorecard update | security claim | guaranteed ROI |
| commission-calculation draft · weekly-report draft | affiliate payout · final diagnostic | guaranteed compliance |

> The founder approves every high-risk external action. This matrix mirrors the 11 non-negotiables — see [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) and the constitution.

---

## 14. Metrics — المقاييس

Do **not** measure "messages sent". Measure outcomes.
لا تقس "عدد الرسائل". قس النتائج.

- **Acquisition:** target accounts · manual touches · reply rate · proof-pack requests · risk-score completions.
- **Conversion:** qualified leads · meetings booked · scopes requested · invoices sent · invoices paid.
- **Distribution:** partner leads · affiliate leads · partner meetings · partner-sourced revenue · commission due.
- **Trust:** approval compliance · blocked risky actions · unsupported claims · evidence completeness.
- **Delivery:** Proof Packs delivered · delivery cycle time · value confirmed · upsell candidates.

---

## 15. 14-day activation sprint — سبرنت التفعيل (14 يومًا)

| Day | Actions |
|---|---|
| 1 | Set up the War Room · list 20 agencies · write 3 messages · send 10 manual touches · publish 1 founder post |
| 2 | 5 follow-ups · 10 new touches · prepare the sample Proof Pack · book the first demo |
| 3 | Start partner outreach · prepare the 499 Pilot · review objections · publish a proof snippet |
| 4 | Run the first demo · close on a Pilot/Diagnostic · prepare the scope |
| 5 | Follow up the demo · send the invoice / payment link · prepare onboarding |
| 6 | If paid/committed → start delivery. If not → follow up with one extra proof asset |
| 7 | Weekly review · pick the best segment · double the winning message · stop the weak one |
| **Week 2** | Repeat on 50 targets. Goal: **30 conversations · 5 meetings · 2 scopes · 1 payment/commitment.** |

---

## 16. Sales room per lead — غرفة بيع لكل lead

Every interested lead gets an internal "sales room":
`company · contact · source · pain hypothesis · lead score · conversation notes · proof asset sent · meeting brief · objections · scope status · invoice status · next action · evidence events`.

**No lead exists without:** `owner` · `next_action` · `next_action_date` · a clear `status` (§3) · `evidence`.
**لا lead بلا:** مالك · خطوة تالية · تاريخها · حالة واضحة · دليل.

> If sales is the problem, don't build a feature. If proof is the problem, improve the proof. If the ICP is the problem, change the segment. If price is the problem, offer a smaller pilot.
> إن كانت المشكلة في البيع فلا تبنِ ميزة. في الإثبات حسّن الإثبات. في الـICP غيّر الشريحة. في السعر اعرض pilot أصغر.

---

## 17. Ledgers and friction — السجلات والاحتكاك

The War Room points; the ledgers are the record of truth. Update the matching ledger the same day a state changes.
غرفة العمليات تشير؛ السجلات هي سجل الحقيقة. حدّث السجل المطابق يوم تغيّر الحالة.

| When this happens | Record it here |
|---|---|
| Qualify decision returned | [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) — event `qualify_decision` (canonical, `WARM_LIST_WORKFLOW.md` §5) |
| Proof event used in a meeting | [`../ledgers/PROOF_LEDGER.md`](../ledgers/PROOF_LEDGER.md) |
| Invoice paid / revenue confirmed | [`../ledgers/VALUE_LEDGER.md`](../ledgers/VALUE_LEDGER.md) |
| Capital asset deposited (sector pattern, reusable draft) | [`../ledgers/CAPITAL_LEDGER.md`](../ledgers/CAPITAL_LEDGER.md) |
| Governance decision / refusal | [`../ledgers/GOVERNANCE_LEDGER.md`](../ledgers/GOVERNANCE_LEDGER.md) |
| Objection, decline, confusion, daily wrap | [`../adoption/FRICTION_LOG.md`](../adoption/FRICTION_LOG.md) |
| Outbound referral made | `referral_ledger` — referral entries kept in [`../ledgers/CLIENT_LEDGER.md`](../ledgers/CLIENT_LEDGER.md) |

> A proof pack without a Value Ledger entry is incomplete. Source-less claims are not recorded.
> حزمة إثبات بلا قيد في سجل القيمة = ناقصة. لا تُسجَّل ادعاءات بلا مصدر.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
