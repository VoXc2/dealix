# Dealix — Distribution OS — نظام التوزيع
<!-- PHASE 13 | Owner: Founder | Date: 2026-05-17 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** المنتج جاهز. المعركة الآن في التوزيع، الإثبات،
> الإغلاق، والاحتفاظ. لا قيمة لميزة لا تصل إلى عميل يدفع.
>
> **Golden rule:** The product is mature. The battle is now distribution,
> proof, closing, retention. A feature that never reaches a paying
> customer has no value.

> **إفصاح — Disclosure.** هذا المستند يوحّد أصولاً متفرقة في نظام تشغيل
> واحد. لا يُنشئ تسعيراً جديداً ولا قنوات جديدة — كل رقم هنا مصدره
> [`docs/OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md)
> وكل مرحلة قمعٍ مصدرها `auto_client_acquisition/sales_os/funnel.py`.

---

## 1. السياق — لماذا يوجد هذا المستند / Context

### عربي

المنتج اجتاز مرحلة "هل يعمل؟". المشكلة لم تعد تقنية. المشكلة الآن:
عدد المحادثات الحقيقية أسبوعياً، عدد Proof Packs المُسلَّمة، عدد
الصفقات المُغلقة، ونسبة العملاء الباقين. Distribution OS يجمع
السكربتات والقوالب ولوحات المتابعة المتناثرة في نظام تشغيل واحد
يُدار يومياً.

### English

The product passed the "does it work?" stage. The problem is no longer
technical. It is now: real conversations per week, Proof Packs
delivered, deals closed, and customers retained. The Distribution OS
consolidates scattered scripts, templates, and dashboards into one
operating system run daily.

---

## 2. قمع التوزيع — 12 مرحلة / The 12-Stage Distribution Funnel

> هذا الجدول يطابق `STAGE_PROPERTIES` في
> `auto_client_acquisition/sales_os/funnel.py` حرفياً. القمع
> "مسنّن أمامي" — تقدّم مرحلة واحدة فقط، أو سقوط إلى `lost` /
> `refer_out`. لا قفز ولا رجوع.

| # | المرحلة / Stage | Owner | Status | Next action | Evidence | Approval rule | KPI | Failure mode |
|---|---|---|---|---|---|---|---|---|
| 1 | target | founder | open | Add the account to the War Room table with city, segment, decision maker. | target.added event with account + segment recorded | auto — internal record, no external action | targets_added_per_day | vague target with no decision maker identified |
| 2 | pain_hypothesis | founder | open | Write one concrete pain hypothesis for this account. | pain.hypothesized event with the hypothesis text | auto — internal record | pain_hypotheses_written | generic pain that fits every account (not specific) |
| 3 | proof_asset | founder | open | Attach the proof asset that closes a conversation (sample Proof Pack / one-pager). | proof asset reference linked to the target | auto — reuse existing approved assets only | targets_with_proof_asset_ready | building 20 pages instead of one closing asset |
| 4 | manual_outreach | founder | in_progress | Draft the personalized message; queue for founder approval before sending. | message.drafted then message.approved then message.sent events | human (risk=medium); draft-only — no live send | messages_sent_per_day | sending before approval / cold WhatsApp / LinkedIn automation |
| 5 | conversation | founder | in_progress | Classify the reply and prepare the next follow-up. | reply.received and reply.classified events | human — each follow-up draft approved before send | reply_rate | no follow-up owner; replies decay unanswered |
| 6 | demo_12min | founder | in_progress | Run the 12-minute closing demo; end with the pilot ask. | meeting.booked then meeting.held events | auto — founder-led live call | demo_rate | full product tour instead of a close-focused demo |
| 7 | pilot_diagnostic | founder | in_progress | Send the scope for a single workflow / 10 opportunities. | scope.sent event with the scoped deliverable | human — scope reviewed before it is sent | pilot_offer_rate | scope too large; offer risk kills the close |
| 8 | payment_commitment | founder | in_progress | Send the invoice; record the payment or written commitment. | invoice.sent then invoice.paid or commitment.recorded events | human — no live charge; invoice sent manually after approval | payment_or_commitment_rate | discounting instead of reducing scope |
| 9 | delivery | founder | in_progress | Deliver the first artifact within 24-48 hours. | delivery artifacts logged against the engagement | human — external sends in delivery stay draft-only | time_to_first_delivery_hours | waiting weeks; momentum lost after payment |
| 10 | proof_pack | founder | in_progress | Assemble and deliver the Proof Pack documenting what happened. | proof.pack_requested then proof.pack_delivered events | human — final Proof Pack approved before it is shared | proof_pack_delivery_time | fake or unevidenced proof; claims without a source |
| 11 | sprint_retainer | founder | open | Offer the next rung (Sprint / Retainer) on the back of delivered proof. | deal.proposal_sent event referencing the Proof Pack | human — proposal approved before it is sent | upsell_candidate_rate | upsell pitched before proof exists |
| 12 | referral_partner_loop | founder | open | Ask for a referral and open one partner conversation. | referral.requested and partner.conversation_logged events | human — partner terms approved individually | referral_rate | no loop closed; proof never converted into distribution |

> **ملاحظة:** كل مرحلة بدون خصائصها السبع ليست "Full Ops" — هي نشاط
> غير مُعرَّف. لا تُعلِن مرحلةً لم تصل إليها فعلياً.

---

## 3. War Room + لوحة النتائج اليومية / Daily Scorecard

### عربي

تُحدَّث لوحة النتائج نهاية كل يوم عمل (17:00 بتوقيت السعودية).
المولّد `scripts/war_room_scorecard.py` يقرأ تيار الأحداث
(`message.sent`، `reply.received`، `meeting.held`،
`proof.pack_delivered` …) ويملأ الأرقام تلقائياً — الأرقام مصدرها
الأحداث، لا الذاكرة. القالب الكامل في
[`docs/ops/daily_scorecard.md`](ops/daily_scorecard.md).

| الرقم اليومي / Daily number | المصدر / Event source |
|---|---|
| Messages sent | message.sent |
| Follow-ups sent | reply.classified → follow-up message.sent |
| Replies received | reply.received |
| Proof-pack requests | proof.pack_requested |
| Demos booked | meeting.booked |
| Demos held | meeting.held |
| Scopes sent | scope.sent |
| Invoices sent | invoice.sent |
| Paid / commitment | invoice.paid / commitment.recorded |
| Proof Packs delivered | proof.pack_delivered |
| Partner conversations | partner.conversation_logged |
| Risks blocked | risk_blocked |
| Tomorrow's #1 priority | founder-set, one line |

> **قاعدة:** رقمٌ بلا حدثٍ يدعمه = `insufficient_data`. لا يُكتب رقم
> تقديري في خانة فعلية. A number with no backing event is
> `insufficient_data`, never written into an actual column.

---

## 4. سلّم الإغلاق / The Close Ladder

سلّم الإغلاق يُسقَط مباشرةً على سلّم العروض في
[`docs/OFFER_LADDER_AND_PRICING.md`](OFFER_LADDER_AND_PRICING.md):

| Rung | العرض / Offer | السعر / Price | شرط الفتح / Unlock |
|---|---|---|---|
| 0 | Free AI Ops Diagnostic | مجاني | باب الدخول |
| 1 | 7-Day Revenue Proof Sprint | 499 SAR | Pilot Gate |
| 2 | Data-to-Revenue Pack | 1,500 SAR | بعد Sprint |
| 3 | Managed Revenue Ops | 2,999–4,999 SAR/شهر | بعد pilot ناجح |
| 4 | Executive Command Center | 7,500–15,000 SAR/شهر | بعد ≥ 3 pilots |
| 5 | Agency Partner OS | مخصص + 15–30% rev-share | بعد ≥ 3 Proof Packs |

### القاعدة الأهم — قلّل النطاق قبل أن تخفض السعر

> **Reduce scope before you reduce price.** السعر إشارة قيمة؛ خفضه
> يكسر السلّم كله. النطاق مرن.

أمثلة على تقليل النطاق بدل الخصم:

- **بدل سير عمل كامل → 10 فرص فقط.** نراجع 10 فرص ونصنّفها، لا
  الـ pipeline بأكمله.
- **بدل كل العملاء → عميل واحد.** نطبّق على عميل واحد من عملاء
  الوكالة، لا على محفظتها كلها.
- **بدل Sprint كامل → Proof Pack واحد.** مخرَج واحد موثَّق يثبت
  النمط، ثم يُقرَّر التوسّع.

الخصم يُخفي مشكلة قيمة؛ تقليل النطاق يكشفها بأمانة ويُبقي السعر
المرجعي سليماً.

---

## 5. مصفوفة الأتمتة / Full-Ops Automation Matrix

| مؤتمت بالكامل / Fully automatable | يحتاج موافقة / Needs approval | ممنوع الآن / Forbidden now |
|---|---|---|
| تسجيل أحداث القمع داخلياً (target.added، pain.hypothesized) | صياغة رسائل التواصل (draft → موافقة) | الإرسال الخارجي المباشر دون موافقة |
| توليد لوحة النتائج من تيار الأحداث | إرسال النطاق والفاتورة | السحب الآلي للرسوم (auto-charge) |
| تجميع مسودات Proof Pack من القوالب | مشاركة Proof Pack النهائي | cold WhatsApp / أتمتة LinkedIn |
| حساب المقاييس واتجاهاتها | عرض الترقية للدرجة التالية | scraping / قوائم مشتراة |
| تذكيرات المتابعة الداخلية | شروط الشركاء (كلٌّ على حدة) | white-label قبل 3 Proof Packs |
| كشف المخاطر ووضع علامة `risk_blocked` | صرف عمولة شريك | صرف عمولة قبل دفع الفاتورة |

> كل فعل خارجي = draft-only / approval-gated. الأتمتة تُسرّع العمل
> الداخلي فقط. Every external action is draft-only and approval-gated.

---

## 6. مقاييس القرار / Decision Metrics

| المقياس / Metric | يقرأ / Reads |
|---|---|
| Reply rate | هل الرسالة تستحق رداً؟ |
| Demo rate | هل المحادثة تتحوّل إلى اجتماع؟ |
| Pilot-offer rate | هل الديمو يصل إلى عرض نطاق؟ |
| Payment / commitment rate | هل النطاق يُغلَق؟ |
| Proof-Pack delivery time | هل نُسلّم بسرعة بعد الدفع؟ |
| Upsell-candidate rate | هل الإثبات يفتح الدرجة التالية؟ |
| Referral rate | هل العميل الراضي يفتح باباً جديداً؟ |
| Partner-sourced lead rate | هل قناة الشركاء تُنتج فرصاً؟ |
| Blocked-risk count | كم خطراً أوقفناه قبل وقوعه؟ |

### تشخيص — إذا تعطّل القمع / Funnel diagnostic

- **السوق لا يردّ (reply rate منخفض):** المشكلة في الاستهداف أو
  فرضية الألم أو أصل الإثبات — راجع المراحل 1–3. لا تزد حجم الإرسال.
- **السوق يردّ لكن لا يدفع (payment rate منخفض):** المشكلة في
  الديمو أو حجم النطاق — راجع المراحل 6–8. قلّل النطاق، لا السعر.
- **يدفع لكن لا يبقى (لا upsell):** المشكلة في سرعة التسليم أو
  Proof Pack — راجع المراحل 9–11.

> كل رقم غير مُثبت يُكتب كـ **estimate**. لا نسبة تحويل تُعرَض
> كحقيقة. Every unproven number is marked an estimate; no conversion
> rate is presented as fact.

---

## 7. الأصول الفرعية / Sub-Assets

| المستند / Document | الغرض / Purpose |
|---|---|
| [`distribution-os/14_DAY_SPRINT.md`](distribution-os/14_DAY_SPRINT.md) | سبرنت التوزيع 14 يوماً |
| [`distribution-os/AGENCY_WEDGE_ONEPAGER.md`](distribution-os/AGENCY_WEDGE_ONEPAGER.md) | إسفين شراكة الوكالات |
| [`distribution-os/DEMO_12MIN_SCRIPT.md`](distribution-os/DEMO_12MIN_SCRIPT.md) | سكربت ديمو الإغلاق 12 دقيقة |
| [`distribution-os/AFFILIATE_GOVERNANCE_SPEC.md`](distribution-os/AFFILIATE_GOVERNANCE_SPEC.md) | مواصفة حوكمة المسوّقين بالعمولة |
| [`distribution-os/CONTENT_FLYWHEEL.md`](distribution-os/CONTENT_FLYWHEEL.md) | دولاب المحتوى إلى الإغلاق |

### روابط ذات صلة / Related docs

- [`docs/ops/daily_scorecard.md`](ops/daily_scorecard.md)
- [`docs/templates/PROOF_PACK_TEMPLATE.md`](templates/PROOF_PACK_TEMPLATE.md)
- [`docs/partners/PARTNER_PACKAGES.md`](partners/PARTNER_PACKAGES.md)
- [`docs/AGENCY_PARTNER_PITCH.md`](AGENCY_PARTNER_PITCH.md)
- [`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`](90_DAY_BUSINESS_EXECUTION_PLAN.md)
- [`docs/FIRST_3_DIAGNOSTIC_SCRIPT.md`](FIRST_3_DIAGNOSTIC_SCRIPT.md)
- [`docs/FIRST_10_WARM_MESSAGES_AR_EN.md`](FIRST_10_WARM_MESSAGES_AR_EN.md)

---

*Distribution OS v1.0 · 2026-05-17 · Dealix · القيمة التقديرية ليست
قيمة مُتحقَّقة — Estimated value is not Verified value.*
