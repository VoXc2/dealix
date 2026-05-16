# OUTREACH DRAFTS — QUEUED FOR FOUNDER APPROVAL — NOT SENT

> **STATUS: DRAFTS ONLY.** Nothing in this document has been sent. Nothing in this document
> may be sent by any automated process. Every draft below requires the founder to:
> 1. Read and edit the draft before sending.
> 2. Confirm the recipient is a genuine warm / known contact — a person met at least once
>    in person or by named introduction. No purchased lists. No scraped lists.
>    No "found you on LinkedIn" first contact.
> 3. Send manually, on the channel the existing relationship already uses, one human
>    message per contact. No automation, no bulk send.
>
> **Doctrine reference:** `docs/institutional/DEALIX_CONSTITUTION.md` (non-negotiables) and
> `docs/sales-kit/WARM_LIST_WORKFLOW.md` (cadence, channels, reply model).
>
> **Constitutional non-negotiables honored here:** no cold WhatsApp automation, no scraping,
> no LinkedIn automation, no guaranteed-outcome claims, no external send without explicit
> founder approval.
>
> _Session note: the once-per-session launch-status check returned no output in this
> environment (PROD endpoint unreachable / not configured). These are draft-only outputs and
> carry no send or invoice risk. Before any real proposal or transactional email is sent, the
> founder must verify Moyasar mode and Gmail OAuth status per the Wave 15 checklist._

---

## Part A — Warm-list outreach drafts / مسوّدات التواصل مع القائمة الدافئة

### A.0 — Scope reminder / تذكير بالنطاق

These drafts are for the founder's **20 named personal contacts** only. The offer entry point
is a **Free AI Ops Diagnostic**, followed optionally by a **499 SAR 7-Day Revenue Proof
Sprint**. No revenue outcome is promised at any point. Pick the language variant that matches
the language the relationship already uses.

### A.1 — The one-line ask (canonical) / السطر الواحد

This is consistent with `WARM_LIST_WORKFLOW.md` Section 2 — use it as the default. One
question only. No deck, no pricing breakdown beyond the 499 SAR figure, no calendar link in
the first message.

**العربية:**

> أبني MVP لخدمة Revenue Intelligence لشركات B2B سعودية — أبحث عن 2–3 شركات يجربون تشخيصاً مجانياً + Sprint مدفوع 499 ريال. هل تعرف من يفيدك هذا؟

**English:**

> Building an MVP for a Revenue Intelligence service for Saudi B2B companies. Looking for 2 to 3 companies to run a free diagnostic and a paid 7-day 499 SAR sprint. Do you know anyone this would be useful for?

### A.2 — Light personalization variants / صيغ مخصّصة خفيفة

Each variant is still **a single human message**, sent on the **existing relationship
channel**, with **no automation**. The personalization is one clause — it does not change the
ask. Use only with a contact where the opening line is genuinely true.

#### Variant 1 — Peer founder / مؤسس نظير

**العربية:**

> بصفتك مؤسس وتعرف معاناة أول سوق — أبني MVP لخدمة Revenue Intelligence لشركات B2B سعودية. أبحث عن 2–3 شركات تجرّب تشخيصاً مجانياً + Sprint مدفوع 499 ريال. هل تعرف من يفيده؟

**English:**

> As a fellow founder who knows the first-market grind — I'm building an MVP for a Revenue Intelligence service for Saudi B2B companies. Looking for 2 to 3 companies to try a free diagnostic and a paid 7-day 499 SAR sprint. Anyone come to mind?

#### Variant 2 — Contact with B2B clients / جهة لديها عملاء B2B

**العربية:**

> بحكم تعاملك مع شركات B2B — أبني MVP لخدمة Revenue Intelligence. أبحث عن 2–3 شركات تجرّب تشخيصاً مجانياً للعمليات + Sprint مدفوع 499 ريال. هل أحد من عملائك قد يستفيد؟

**English:**

> Given the B2B companies you work with — I'm building an MVP for a Revenue Intelligence service. Looking for 2 to 3 companies to try a free ops diagnostic and a paid 7-day 499 SAR sprint. Would any of your clients find this useful?

#### Variant 3 — Contact in a regulated sector / جهة في قطاع منظَّم

**العربية:**

> بما أنك في قطاع منظَّم وتعرف أهمية الحوكمة — أبني MVP لخدمة Revenue Intelligence مبنية على مصدر واضح واعتماد بشري وسجل أدلة. أبحث عن 2–3 شركات تجرّب تشخيصاً مجانياً + Sprint مدفوع 499 ريال. هل تعرف من يفيده؟

**English:**

> Since you're in a regulated sector and know why governance matters — I'm building an MVP for a Revenue Intelligence service built on clear sourcing, human approval, and an evidence trail. Looking for 2 to 3 companies to try a free diagnostic and a paid 7-day 499 SAR sprint. Anyone come to mind?

#### Variant 4 — Reconnecting contact / جهة لم نتواصل منذ فترة

**العربية:**

> طال الوقت — أتمنى أمورك طيبة. أبني هذه الفترة MVP لخدمة Revenue Intelligence لشركات B2B سعودية. أبحث عن 2–3 شركات تجرّب تشخيصاً مجانياً + Sprint مدفوع 499 ريال. هل تعرف من قد يفيده؟

**English:**

> It's been a while — hope you're well. I'm currently building an MVP for a Revenue Intelligence service for Saudi B2B companies. Looking for 2 to 3 companies to try a free diagnostic and a paid 7-day 499 SAR sprint. Know anyone this would suit?

### A.3 — Cadence and reply model / الإيقاع ونموذج الرد

**Cadence / الإيقاع:** 5 contacts per day for 4 days = 20 contacts total. One outreach per
contact. No automated follow-up. A second message only when the contact replies, or when an
explicit follow-up window was agreed. Log each contact at send time in `engagement_ledger`
with `channel`, `language`, `timestamp`, and `relationship_basis` (the consent record). If
there is no reply within 7 days, the contact is left alone.

**Five-decision reply model / نموذج الرد بخمسة قرارات:** every reply that crosses into "tell
me more" triggers a 20-minute qualification call and a structured intake, then the founder
runs the qualify endpoint. The endpoint returns exactly one of five decisions — the founder
does not invent a sixth:

| Decision | Meaning | Next step |
|---|---|---|
| `ACCEPT` | Fits the productized offer; data ownership clear; decision-maker on the call. | Send Free Diagnostic intake link; 24-hour clock starts on submission. |
| `DIAGNOSTIC_ONLY` | Fits at the diagnostic tier only; do not pitch the sprint yet. | Run the Free Diagnostic; recommendation field decides on a sprint invite. |
| `REFRAME` | Genuine intent, wrong frame (asking for a service we don't offer, but the underlying need fits one we do). | Send a 3-line reframe note; re-run qualify with the new framing. |
| `REJECT` | Outside scope (cold-outreach automation, LinkedIn automation, guaranteed sales, scraped-list enrichment). | Polite refusal citing the constitutional clause; `friction_log` entry; no follow-up. |
| `REFER_OUT` | Legitimate need, better served by a partner. | Make the intro; record in `referral_ledger` (entries kept in `../ledgers/CLIENT_LEDGER.md`). |

---

## Part B — Partner follow-up email drafts / مسوّدات بريد متابعة الشركاء

> **Both emails below are drafts requiring founder review before sending.** The founder must
> confirm the recipient is a genuine warm / known contact before any send. These are NOT an
> AI-automation resale motion — they position a governed AI operations diagnostic. No revenue
> outcome is promised. Use the `[Name]` / `[الاسم]` placeholder and the signature `Sami`.

### B.1 — Email Draft 1: "One client segment" (warm follow-up) / متابعة دافئة

**Subject / الموضوع:** A governed lens on the AI questions your clients are already asking
— عدسة محوكمة لأسئلة الذكاء الاصطناعي التي يطرحها عملاؤك

**English:**

> Hi [Name],
>
> Following up on our earlier conversation. I want to be precise about what I'm building,
> because it is easy to mishear it as an AI-automation resale offer — it isn't.
>
> Dealix is a governed AI operations diagnostic. It is for clients who are already
> experimenting with AI but are missing the operational layer underneath it: source clarity
> (where each answer comes from), approval boundaries (what an AI step may and may not do
> without a human), evidence trails (a record of every decision), proof of value (whether
> the experiment actually moved anything), and agent-identity controls (knowing which agent
> acted, under whose authority).
>
> The reason I'm writing: would it be useful to compare this against one client segment you
> already see asking about AI governance or AI-driven revenue operations? Not a referral ask
> and not a resale conversation — just one segment, so we can see whether the governed
> diagnostic maps cleanly onto a real pattern you're seeing.
>
> Happy to keep it to a short call whenever it suits you.
>
> Best,
> Sami

**العربية:**

> مرحباً [الاسم]،
>
> متابعةً لحديثنا السابق. أريد أن أكون دقيقاً في وصف ما أبنيه، لأنه قد يُفهَم خطأً على أنه عرض إعادة بيع لأتمتة الذكاء الاصطناعي — وهو ليس كذلك.
>
> Dealix هو تشخيص محوكَم لعمليات الذكاء الاصطناعي. موجَّه للعملاء الذين يجرّبون الذكاء الاصطناعي فعلاً لكن تنقصهم الطبقة التشغيلية تحته: وضوح المصدر (من أين تأتي كل إجابة)، حدود الاعتماد (ما الذي يجوز لخطوة آلية فعله دون إنسان وما لا يجوز)، سجلات الأدلة (توثيق كل قرار)، إثبات القيمة (هل حرّكت التجربة شيئاً فعلاً)، وضوابط هوية الوكيل (معرفة أي وكيل تصرّف وتحت صلاحية من).
>
> سبب رسالتي: هل سيكون من المفيد مقارنة هذا مع شريحة عملاء واحدة ترى بالفعل أنها تسأل عن حوكمة الذكاء الاصطناعي أو عمليات الإيرادات المدفوعة بالذكاء الاصطناعي؟ ليست طلب إحالة ولا حديث إعادة بيع — فقط شريحة واحدة، لنرى هل ينطبق التشخيص المحوكَم بوضوح على نمط حقيقي تلاحظه.
>
> يسعدني مكالمة قصيرة في الوقت الذي يناسبك.
>
> تحياتي،
> Sami

### B.2 — Email Draft 2: "Regulated workflows" — clean re-introduction / إعادة تعريف

> **Use only when** re-contact is legitimate under `WARM_LIST_WORKFLOW.md` §1:
> a follow-up window was explicitly agreed, **or** enough time has passed
> (≥ ~3 months) that this is a genuine fresh introduction on a new basis —
> **never** as an unsolicited chase of a recent unanswered note.
> يُستخدَم فقط عند اتّفاق صريح على متابعة، أو بعد انقضاء مدة كافية (≈3 أشهر)
> بحيث يكون تعريفًا جديدًا فعليًّا — لا كمطاردة لرسالة حديثة بلا رد.

**Subject / الموضوع:** Governed AI operations for regulated workflows — a re-introduction
— عمليات ذكاء اصطناعي محوكَمة للأعمال المنظَّمة: إعادة تعريف

**English:**

> Hi [Name],
>
> It has been a while — I'd rather re-introduce this cleanly than assume the
> earlier timing was right. No reply to the earlier note is expected.
>
> I'm building Dealix, a governed AI operations company starting in Saudi Arabia. It is most
> relevant for regulated workflows — settings where AI experimentation is already happening,
> but source clarity, human approval, evidence trails, and proof of value are not yet
> operationalized. This is not generic AI automation; the governance layer is the product.
>
> The first motion is deliberately small: a controlled diagnostic or a Revenue Intelligence
> Sprint that produces a Proof Pack (the evidence of what was found and changed), a Value
> Ledger (a record of value, estimated separately from value verified), and a governed
> decision trail. It is bounded, it is reviewable, and it does not require the client to
> commit to a platform up front.
>
> My one question: would it be useful to compare this against one regulated client segment
> you already see exploring AI? One segment is enough to tell whether the governed approach
> fits a real pattern in your book — and if it doesn't, that's a useful answer too.
>
> Glad to keep this to a short call at your convenience.
>
> Best,
> Sami

**العربية:**

> مرحباً [الاسم]،
>
> مرّت فترة — أفضّل إعادة تعريف الأمر بوضوح بدل افتراض أن التوقيت السابق كان مناسباً. لا يُنتظَر ردّ على الرسالة السابقة.
>
> أبني Dealix، شركة عمليات ذكاء اصطناعي محوكَمة تنطلق من السعودية. هي الأكثر صلة بالأعمال المنظَّمة — البيئات التي يجري فيها تجريب الذكاء الاصطناعي فعلاً، لكن وضوح المصدر والاعتماد البشري وسجلات الأدلة وإثبات القيمة لم تُفعَّل تشغيلياً بعد. هذه ليست أتمتة ذكاء اصطناعي عامة؛ طبقة الحوكمة هي المنتج.
>
> الحركة الأولى صغيرة عمداً: تشخيص مضبوط أو Revenue Intelligence Sprint ينتج حزمة إثبات (Proof Pack توثّق ما اكتُشف وما تغيّر)، وسجل قيمة (Value Ledger يفرّق بين القيمة التقديرية والقيمة المُتحقَّقة)، وسجل قرارات محوكَم. عمل محدود النطاق، قابل للمراجعة، ولا يتطلب من العميل الالتزام بمنصّة مسبقاً.
>
> سؤالي الوحيد: هل سيكون من المفيد مقارنة هذا مع شريحة عملاء واحدة في قطاع منظَّم ترى بالفعل أنها تستكشف الذكاء الاصطناعي؟ شريحة واحدة تكفي لمعرفة هل يناسب النهج المحوكَم نمطاً حقيقياً لديك — وإن لم يناسب، فهذا جواب مفيد أيضاً.
>
> يسعدني مكالمة قصيرة في الوقت الذي يناسبك.
>
> تحياتي،
> Sami

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
