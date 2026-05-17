# Dealix Growth System — نظام النمو في Dealix — Canonical Playbook

## 1. الغرض — Purpose

**AR —** هذه الوثيقة هي المرجع الرسمي (canonical) لاستراتيجية "نظام النمو في Dealix": شبكة من 12 ماكينة تحوّل كل إشارة سوق إلى عميل، وكل عميل إلى دليل، وكل دليل إلى محتوى ومبيعات إضافية. الوثيقة تجمع الاستراتيجية الكاملة التي وضعها المؤسس، ثم تربط كل ماكينة بملفات حقيقية في المستودع مع حالة صريحة: مُنجز / جزئي / مفقود (DONE / PARTIAL / MISSING)، إضافةً إلى خارطة طريق مرتّبة بالأولوية تحترم العقيدة.

**EN —** This document is the canonical reference for the Dealix Growth System strategy: a 12-machine network that turns every market signal into a lead, every lead into evidence, and every evidence into content and upsell. It captures the founder's full strategy and honestly maps each machine to real repository files with an explicit status: DONE / PARTIAL / MISSING, plus a doctrine-safe prioritized roadmap.

> **ملاحظة حاكمة — Canonical, not a completion claim.** هذه الوثيقة تصف *الاستراتيجية* وتوثّق *الحالة الفعلية*. وجود ماكينة في القائمة لا يعني أنها مبنية. لا تُقدَّم أي ميزة طموحة كأنها جاهزة. اعتمد دائماً على عمود الحالة (Status) والمسارات في الجداول أدناه.

> **Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

---

## 2. الفلسفة وحلقة النمو — Philosophy & the Growth Loop

**AR —** نظام النمو في Dealix ليس قناة تسويق واحدة، بل اندماج سبع طبقات:

> Sales Autopilot + Support Autopilot + Marketing Factory + Media Authority Engine + Affiliate & Partner Network + Governance/Approval Layer + Evidence Ledger.

كل قناة تُنتج عميلاً محتملاً (lead). كل عميل يدخل التسجيل (scoring). كل نتيجة تسجيل تُنتج إجراءً تالياً. كل إجراء عالي المخاطرة يحتاج موافقة المؤسس. كل نتيجة تُسجَّل كدليل (evidence). كل دليل يصبح محتوى أو بيعاً إضافياً أو playbook.

**حلقة النمو — The loop:**

```
Signal → Lead → Proof → Meeting → Scope → Invoice → Delivery → Upsell → Referral → Content → More Leads
```

**القاعدة الذهبية — Golden rule:** *الوكيل يُسوِّد. المؤسس يوافق. النظام يُسجِّل. — Agent drafts. Founder approves. System logs.*

### العقيدة — The 11 non-negotiables

كل وصف ماكينة في هذه الوثيقة يجب أن يعكس: **مُسوّدة فقط + موافقة مطلوبة + دليل مُسجَّل** (draft-only + approval-required + evidence-logged).

| # | غير قابل للتفاوض — Non-negotiable | يُفرَض عبر — Enforced by |
|---|---|---|
| 1 | لا إرسال حيّ — no live send | `tests/test_live_gates_default_false.py` |
| 2 | لا تحصيل حيّ — no live charge | `tests/test_live_gates_default_false.py` |
| 3 | لا واتساب بارد — no cold WhatsApp | `tests/test_no_cold_whatsapp.py`, `whatsapp_safe_send.py` |
| 4 | لا أتمتة LinkedIn — no LinkedIn automation | `tests/test_no_linkedin_automation.py`, `tests/test_no_linkedin_scraper_string_anywhere.py` |
| 5 | لا كشط بيانات — no scraping | `tests/test_no_scraping_engine.py` |
| 6 | لا أدلة مزيّفة — no fake proof | `tests/test_no_source_no_answer.py`, `test_no_source_passport_no_ai.py` |
| 7 | لا إيرادات مزيّفة — no fake revenue | `db/models_revenue_events.py` (ProofEvent gated) |
| 8 | لا إرسال جماعي — no blast | `auto_client_acquisition/safe_send_gateway/` |
| 9 | لا ادعاءات مضمونة — no guaranteed claims | `tests/test_no_guaranteed_claims.py`, `test_landing_forbidden_claims.py` |
| 10 | لا تسجيل PII — no PII logging | `tests/test_no_pii_in_logs.py` |
| 11 | لا أعلام تفعيل جديدة — no new allow-flags | `tests/test_live_gates_default_false.py` |

---

## 3. الماكينات الـ 12 — The 12 Machines

> الحالة: **DONE** = مبني وموثّق. **PARTIAL** = مكوّن أساسي موجود مع فجوة واضحة. **MISSING** = غير مبني.

### الماكينة 1 — Sales Autopilot

**AR —** خط أنابيب مبيعات كامل: التقاط العميل، استخراج الألم، مطابقة ICP، التسجيل، التوجيه، تسويد الرسائل (مسوّدة فقط)، حجز الاجتماعات، بناء النطاق، تسويد الفوترة. مراحل: `new_lead → qualified_A/B → nurture → partner_candidate → meeting_booked/done → scope_requested/sent → invoice_sent/paid → delivery_started → proof_pack_sent → sprint/retainer_candidate → closed_lost`. تسجيل العميل: +4 رئيس تنفيذي/مؤسس، +3 B2B، +3 لديه CRM، +3 يستخدم/يخطط لـ AI، +2 خليجي، +2 عاجل <30 يوم، +2 ميزانية 5k+ ريال، +2 شريك محتمل؛ سالب لمن لا شركة له/طالب/غامض. النطاقات: 15+ مؤهَّل A، 10–14 B، 6–9 توعية/شريك، <6 أرشفة.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Lead & pipeline model (LeadRecord, DealRecord) | `db/models.py` | DONE | DealRecord يحمل amount/stage فقط |
| Lead intake pipeline (Signal→…→Learning) | `auto_client_acquisition/pipeline.py` | DONE | — |
| LeadCapture agent | `auto_client_acquisition/agents/intake.py` | DONE | — |
| Pain extraction | `auto_client_acquisition/agents/pain_extractor.py` | DONE | — |
| ICPScoring agent | `auto_client_acquisition/agents/icp_matcher.py`, `qualification.py` | DONE | — |
| Routing | `auto_client_acquisition/agents/rules_router.py` | DONE | — |
| Positioning / Prospecting | `auto_client_acquisition/agents/prospector.py` | DONE | — |
| OutreachDraft agent (draft-only email) | `auto_client_acquisition/agents/outreach.py` | DONE | مسوّدة فقط — لا إرسال حيّ |
| Follow-up | `auto_client_acquisition/agents/followup.py` | DONE | — |
| MeetingBrief / Booking (Calendly) | `auto_client_acquisition/agents/booking.py` | DONE | — |
| ScopeBuilder / Proposal | `auto_client_acquisition/agents/proposal.py` | DONE | — |
| CRM sync (optional HubSpot) | `auto_client_acquisition/agents/crm.py` | DONE | اختياري |
| WhatsApp draft-only | `auto_client_acquisition/whatsapp_safe_send.py` | DONE | NO_COLD_WHATSAPP مفروض |
| ReplyClassifier agent | — | PARTIAL | منطق التصنيف في support_os؛ غير مفصول لقناة المبيعات |
| BillingDraft / Invoice state machine | `db/models.py` (DealRecord.amount فقط) | MISSING | لا جدول Invoice بحالات draft/sent/paid؛ Moyasar محجوب على تفعيل الحساب |
| Sales routers | `api/routers/sales.py`, `sales_os.py`, `commercial_engagements.py`, `outreach.py`, `prospect.py`, `pricing.py`, `payment_ops.py` | DONE | — |
| Sales docs | `docs/sales/SALES_PLAYBOOK.md`, `docs/SALES_OPS_SOP.md`, `docs/sales/QUALIFICATION_ENGINE.md`, `docs/sales/QUALIFICATION_SCORE.md`, `docs/growth/LEAD_SCORING_RULES.md`, `docs/growth/CRM_PIPELINE_SCHEMA.md` | DONE | — |

**خلاصة الماكينة 1 ≈ 85% DONE** — الفجوة الوحيدة الجوهرية: آلة حالة الفاتورة.

---

### الماكينة 2 — Support Autopilot

**AR —** التدفق: سؤال → تصنيف النية → بحث في قاعدة المعرفة → تسويد إجابة → تقييم المخاطر → ردّ تلقائي إن كان آمناً / تصعيد إن كان محفوفاً → تسجيل → رصد فجوة معرفية. الردّ التلقائي فقط إذا: موجود في KB، منخفض المخاطر، بلا ادعاء أمني، بلا وعد مالي، بلا تشخيص خاص بعميل، بلا شكوى. التصعيد: أمن/امتثال، استرداد، خصم، نطاق مخصّص، تشخيص عميل، شكوى، إذن دراسة حالة، حذف/تصدير بيانات.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Intent classifier | `auto_client_acquisition/support_os/classifier.py` | DONE | — |
| Ticket handling | `auto_client_acquisition/support_os/ticket.py` | DONE | — |
| Answer responder (draft-only) | `auto_client_acquisition/support_os/responder.py` | DONE | KB غير موصولة بالـ responder المنشور |
| Escalation rules | `auto_client_acquisition/support_os/escalation.py` | DONE | — |
| SLA | `auto_client_acquisition/support_os/sla.py`, `support_inbox/sla_monitor.py` | DONE | — |
| Knowledge answer | `auto_client_acquisition/support_os/knowledge_answer.py`, `knowledge_os/`, `knowledge_v10/` | PARTIAL | لا `/api/v1/knowledge/search` endpoint |
| Inbox state | `auto_client_acquisition/support_inbox/state_store.py` | DONE | — |
| Support routers | `api/routers/support_os.py`, `support_inbox.py`, `support_journey.py`, `customer_success_os.py` | DONE | تكرار موجِّهات (انظر الفجوات العرضية) |
| Ticket storage (ConversationRecord) | `db/models.py` | PARTIAL | مخزّن كـ ConversationRecord — لا جدول support_tickets مخصّص |
| knowledge_articles / knowledge_gaps tables | — | MISSING | لا جداول DB مخصّصة |
| Per-answer risk_score field | — | MISSING | حقل risk_score لكل إجابة غير موجود |

**خلاصة الماكينة 2 ≈ 60% DONE** — التدفق والتصعيد جاهزان؛ طبقة بيانات KB والـ risk_score مفقودة.

---

### الماكينة 3 — Marketing Factory

**AR —** ركائز المحتوى: إخفاقات حوكمة AI، جاهزية CRM/البيانات، تسرّب الإيراد، حدود الموافقة، مسارات الأدلة، جوازات القرار، البناء العلني، عمليات AI/الإيراد الخليجية، تشريح سير عمل مُجهَّل، أمثلة proof pack. أسبوعياً: منشورا LinkedIn، فيديو قصير، carousel، نشرة، لقطة دليل، منشور شريك، منشور اعتراض. **كل تفاعل → محتوى.**

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Marketing & content system doc | `docs/MARKETING_AND_CONTENT_SYSTEM.md` | DONE | — |
| Content calendar | `docs/growth/CONTENT_CALENDAR_MONTH_1.md`, `docs/GEO_CONTENT_CALENDAR.md` | DONE | — |
| Landing pages (24 live) | `docs/growth/WEBSITE_STRUCTURE.md`, `WEBSITE_MVP.md`, `WEBSITE_FIRST_COPY.md` | DONE | — |
| SEO audit (read-only) | `scripts/seo_audit.py`, `auto_client_acquisition/self_growth_os/seo_technical_auditor.py` | DONE | تدقيق فقط — لا نشر |
| Self-growth router | `api/routers/self_growth.py` (`GET /api/v1/self-growth/seo/audit`) | DONE | — |
| Safe publishing QA gate | `auto_client_acquisition/self_growth_os/safe_publishing_gate.py` | PARTIAL | ~70% من بوّابة الجودة |
| Forbidden-claims test | `tests/test_landing_forbidden_claims.py` | DONE | — |
| Case study engine | `auto_client_acquisition/case_study_engine/`, `api/routers/case_study_engine.py` | DONE | — |
| Growth research agents | `autonomous_growth/agents/` (market_research, sector_intel, competitor, content, enrichment, distribution) | DONE | content.py مُسوّد فقط |
| Proof snippet engine | `auto_client_acquisition/self_growth_os/proof_snippet_engine.py` | DONE | — |
| Newsletter | — | MISSING | غير مُحدَّد النطاق |
| Webinars | — | MISSING | غير مُحدَّد النطاق |
| Lead magnets | — | MISSING | غير مُحدَّد النطاق |
| Content brief generator | `docs/SELF_GROWTH_OS_SCOPE.md` §7-8 | MISSING | مؤجَّل عمداً |
| Content draft engine | `docs/SELF_GROWTH_OS_SCOPE.md` §8 | MISSING | مؤجَّل عمداً |
| UTM scheme | — | MISSING | غير مُشكَّل في الكود |

**خلاصة الماكينة 3 ≈ 55% DONE** — التدقيق والمعايرة جاهزان؛ مولّدات المحتوى مؤجَّلة عمداً.

---

### الماكينة 4 — Media Authority Engine

**AR —** امتلاك فئة خليجية: "Governed Revenue & AI Ops". الأصول: قائمة فحص مخاطر AI والإيراد الخليجية، قالب Proof Pack، قالب Decision Passport، مقياس نضج سير عمل الإيراد، قالب سياسة موافقة AI، قائمة جاهزية CRM. حملة شهرية: "GCC AI & Revenue Ops Risk Review".

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Market power / authority docs | `docs/market_power/`, `docs/42_market_power/MARKET_POWER_OS.md` | DONE | — |
| Authority system docs | `docs/growth/AUTHORITY_SYSTEM.md`, `PUBLIC_AUTHORITY_ENGINE.md`, `TRUST_MARKETING_CORE.md` | DONE | — |
| Decision Passport | `api/routers/decision_passport.py` | DONE | — |
| Proof Pack template | `api/routers/proof_pack_governed.py`, `proof_ledger.py` | PARTIAL | القالب موجود؛ مكتبة الأمثلة غير منشورة |
| Risk Checklist / Maturity Score / AI Policy / CRM Readiness assets | — | MISSING | أصول lead-magnet لم تُنتَج بعد |
| Monthly Risk Review campaign | — | MISSING | غير مجدول |

**خلاصة الماكينة 4 ≈ 45% DONE** — البنية الفكرية موجودة؛ الأصول القابلة للتنزيل مفقودة.

---

### الماكينة 5 — Affiliate Machine

**AR —** أربع فئات (الاستراتيجية): T1 مُحيل تابع (5% من أول Diagnostic مدفوع)، T2 إحالة مؤهَّلة (10% من أول صفقة مدفوعة)، T3 شريك استراتيجي (15–20%)، T4 شريك تنفيذ (رسوم تسليم / مشاركة إيراد). العمولة فقط بعد `invoice_paid`؛ استرجاع إن حدث استرداد خلال 30 يوماً؛ لا إحالة ذاتية، لا مزايدة على العلامة، لا spam، لا واتساب بارد باسم Dealix، الإفصاح إلزامي.

> **ملاحظة مواءمة:** المستودع حالياً يطبّق برنامج **شركاء** بثلاث فئات (`docs/AGENCY_PARTNER_PROGRAM.md`: Referral 15%، Implementation 20–25%، Co-Selling 25–30%). الاستراتيجية تطلب برنامج **تابعين (affiliate)** منفصلاً بأربع فئات ونسب أقل. هذا تمييز مفقود — انظر خارطة الطريق.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Partner program doc (3 tiers) | `docs/AGENCY_PARTNER_PROGRAM.md` | DONE | فئات شريك ≠ فئات تابع الـ4 |
| Partner legal agreement | `docs/PARTNER_LEGAL_AGREEMENT.md` | DONE | — |
| Referral tracking | `auto_client_acquisition/partnership_os/referral_tracker.py`, `referral_store.py` | DONE | حقول partner_id/referral_code موجودة |
| PartnerRecord (commission_terms, mrr_share_pct) | `db/models.py` | PARTIAL | لا حقل invoice_paid/commission_status منفصل |
| Referral program router | `api/routers/referral_program.py` | DONE | — |
| Separate affiliate tier model | — | MISSING | غير مميَّز عن الشريك |
| commissions / payouts DB tables | — | MISSING | غير موصولة بالكامل |
| Commission payout (live) | — | MISSING | مُسوّد — بانتظار تفعيل Moyasar |

**خلاصة الماكينة 5 ≈ 40% DONE** — تتبّع الإحالة جاهز؛ نموذج التابع والعمولات الحيّة مفقودان.

---

### الماكينة 6 — Affiliate/Partner Recruiting

**AR —** نموذج تقديم + تسجيل شريك: +4 جمهور B2B، +3 خليجي، +3 مستشار/مشغّل، +2 إحالات سابقة، +2 جودة محتوى؛ سالب لـ spam/جمهور مزيّف/لا إفصاح. تسلسل تأهيل اليوم 0–14.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Partner profile | `auto_client_acquisition/partnership_os/partner_profile.py` | DONE | — |
| Partner fit score | `auto_client_acquisition/partnership_os/fit_score.py` | DONE | — |
| Partner motion / onboarding | `auto_client_acquisition/partnership_os/partner_motion.py` | PARTIAL | تسلسل اليوم 0–14 غير مؤتمت |
| Partner enablement kit | `docs/40_partners/PARTNER_ENABLEMENT_KIT.md` | DONE | — |
| Partner covenant / suspension | `docs/40_partners/PARTNER_COVENANT.md`, `PARTNER_SUSPENSION_POLICY.md` | DONE | — |
| `POST /partner-apply` public endpoint | — | MISSING | نموذج التقديم العام غير منشور |

**خلاصة الماكينة 6 ≈ 65% DONE** — التسجيل والوثائق جاهزة؛ نموذج التقديم العام والتأهيل المؤتمت مفقودان.

---

### الماكينة 7 — Partner Distribution

**AR —** Dealix تُشخّص، الشريك يُنفّذ. النماذج: إحالة، تنفيذ، Diagnostic بعلامة بيضاء، محفظة، شريك ورشة عمل. ورشة شهرية مشتركة.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Partner ecosystem doc | `docs/40_partners/PARTNER_ECOSYSTEM.md`, `docs/growth/PARTNER_NETWORK.md` | DONE | — |
| Partner strategy | `docs/growth/PARTNER_STRATEGY.md`, `docs/growth/AGENCY_RESELLER_PLAYBOOK.md` | DONE | — |
| Partner outreach plan | `docs/growth/PARTNER_OUTREACH_PLAN.md` | DONE | — |
| Partnership router | `api/routers/partnership_os.py` | DONE | — |
| White-label Diagnostic flow | — | MISSING | غير مُحدَّد النطاق |
| Monthly co-hosted workshop | — | MISSING | مرتبط بماكينة 10 (webinars) |

**خلاصة الماكينة 7 ≈ 60% DONE** — النماذج موثّقة؛ التنفيذ بعلامة بيضاء والورش مفقودة.

---

### الماكينة 8 — Paid Ads

**AR —** **لا تبدأ** الإعلانات حتى تتحقق: 3–5 اجتماعات + اعتراضان متكرران + طلب proof-pack واحد + ICP واضح. بِع الـ lead magnet (Risk Score) لا الـ Diagnostic. القنوات: LinkedIn Ads، Google Search، retargeting.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Paid ads | — | MISSING | **مؤجَّل عمداً** — لا تبدأ قبل رسالة مُثبتة |

**خلاصة الماكينة 8 — 0% (مؤجَّل عمداً، صحيح بحسب العقيدة).**

---

### الماكينة 9 — Email / Newsletter

**AR —** "GCC AI & Revenue Ops Notes" — نشرة أسبوعية بخمس كتل: رؤية، خطأ، إطار، لقطة دليل، CTA. تسلسل ما بعد lead-magnet اليوم 0–14. شرائح: مؤسسون، مشغّلون، مستشارون، شركاء، عملاء دافئون، عملاء، تابعون.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Email send infra (gated) | `api/routers/email_send.py` | PARTIAL | بنية الإرسال موجودة؛ مُغلَقة على no-live-send |
| Newsletter content/sequences | — | MISSING | غير مُحدَّد النطاق |
| Audience segments | — | MISSING | لا جدول audiences |

**خلاصة الماكينة 9 ≈ 20% DONE** — بنية الإرسال موجودة ومُغلَقة؛ النشرة نفسها غير مُحدَّدة.

---

### الماكينة 10 — Webinars

**AR —** شهرياً: "Before AI Agents: Govern Your Revenue Workflows" — أجندة 7 نقاط، تسلسل تسجيل → تذكير → إعادة → risk-score → diagnostic.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Webinars | — | MISSING | غير مُحدَّد النطاق |

**خلاصة الماكينة 10 — 0% MISSING.**

---

### الماكينة 11 — SEO

**AR —** كلمات مفتاحية: AI governance Saudi Arabia، RevOps GCC، CRM readiness for AI، AI automation approval policy، decision passport، proof pack template. أنواع الصفحات: أدلة، قوالب، قوائم فحص، مقارنات، أمثلة بأسلوب دراسة حالة، مسرد.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| SEO technical audit (read-only) | `auto_client_acquisition/self_growth_os/seo_technical_auditor.py`, `scripts/seo_audit.py` | DONE | — |
| GEO/AIO radar | `auto_client_acquisition/self_growth_os/geo_aio_radar.py`, `search_radar.py` | DONE | — |
| Internal linking planner | `auto_client_acquisition/self_growth_os/internal_linking_planner.py` | DONE | — |
| GEO content calendar | `docs/GEO_CONTENT_CALENDAR.md` | DONE | — |
| Keyword-targeted page production | — | MISSING | تابع لمولّد المحتوى المؤجَّل |

**خلاصة الماكينة 11 ≈ 65% DONE** — التدقيق والتخطيط جاهزان؛ إنتاج الصفحات تابع لمولّد المحتوى.

---

### الماكينة 12 — Retargeting

**AR —** كل من زار / طلب proof pack / فتح بريداً / حضر webinar / تفاعل على LinkedIn يدخل retargeting برسائل مطابقة للمرحلة.

| Component | Repo path | Status | Gap / Next step |
|---|---|---|---|
| Retargeting | — | MISSING | تابع لـ UTM scheme + Paid Ads (مؤجَّل) |

**خلاصة الماكينة 12 — 0% MISSING (تابع بشكل صحيح للإعلانات المؤجَّلة).**

> الماكينات الإضافية في الاستراتيجية — **Customer Referral Machine** (سؤال الإحالة بعد تأكيد القيمة) و**Upsell Machine** (Diagnostic → Revenue Intelligence Sprint → Governed Ops Retainer → Trust Pack Lite → CRM/Data Readiness → Board Decision Memo) — مغطّاة بـ `docs/growth/EXPANSION_OFFER_SYSTEM.md` و`docs/growth/PROOF_TO_UPSELL_MAP.md` و`docs/growth/PROOF_TO_RETAINER_SYSTEM.md` و`docs/growth/RETAINER_OPERATING_MODEL.md` — **DONE كوثائق، PARTIAL كأتمتة** (لا محرّك upsell موصول بمراحل الـ pipeline).

---

## 4. الجداول الخلفية وواجهات API — Backend Tables & APIs

### 4.1 جداول قاعدة البيانات — DB tables

| Playbook table | الحالة — Status | المقابل في المستودع — Repo equivalent |
|---|---|---|
| `leads`, `accounts`, `contacts`, `opportunities` | exists | LeadRecord, DealRecord في `db/models.py` |
| `messages`, `meetings`, `scopes` | partial | منطق موجود؛ لا جداول مخصّصة منفصلة |
| `invoices` | missing | لا آلة حالة فاتورة — DealRecord.amount فقط |
| `support_tickets` | partial | يُخزَّن كـ ConversationRecord في `db/models.py` |
| `knowledge_articles`, `knowledge_gaps`, `support_answers` | missing | لا جداول DB مخصّصة |
| `approvals` | exists | `migrations/versions/20260515_103_approval_tickets.py` |
| `evidence_events` | partial | ProofEvent في `db/models_revenue_events.py` موجود لكن غير مُعبّأ؛ `evidence_collector.py` داخل العملية فقط |
| `policies`, `agent_run_logs`, `claim_reviews` | partial | AgentRunRecord موجود؛ claim_reviews متناثر |
| `campaigns`, `content_assets`, `lead_magnets`, `utm_events`, `marketing_events`, `email_sequences`, `webinars`, `audiences` | missing | لم تُحدَّد |
| `partners`, `partner_links`, `referrals` | exists/partial | PartnerRecord + referral_store |
| `commissions`, `payouts`, `approved_assets`, `partner_compliance_events` | missing | غير موصولة |

### 4.2 واجهات API — APIs

| Playbook endpoint | الحالة — Status | المقابل في المستودع — Repo equivalent |
|---|---|---|
| `POST /risk-score` (public) | missing | lead magnet غير منشور |
| `POST /proof-pack-request` (public) | partial | `api/routers/proof_pack_governed.py` |
| `POST /partner-apply` (public) | missing | لا نموذج تقديم عام |
| `POST /support` (public inbound) | exists | `POST /api/v1/support-inbox/inbound` |
| Ops dashboards founder/sales/marketing/partners/support | exists/partial | `founder_dashboard.py`, `sales_os.py`, `partnership_os.py`, `support_os.py` |
| Lead scoring + draft-message | exists | عبر `auto_client_acquisition/agents/` + `api/routers/outreach.py` |
| Reply classify | partial | منطق في `support_os/classifier.py` — غير مكشوف لقناة المبيعات |
| Approvals approve/reject | exists | `api/routers/approval_center.py` |
| Evidence events | partial | `api/routers/proof_ledger.py` + `evidence_control_plane_os/evidence_api.py` — داخل العملية |
| Partner referrals | exists | `api/routers/referral_program.py` |
| Commissions calculate / payouts mark-paid | missing | غير موصول — بانتظار Moyasar |
| `/api/v1/knowledge/search` | missing | KB غير مكشوفة كـ endpoint |

### 4.3 ملاحظة الواجهة الأمامية — Frontend note

الصفحات العامة (`/dealix-diagnostic`, `/proof-pack`, `/partners`) منشورة ضمن الـ 24 صفحة هبوط (`docs/growth/WEBSITE_STRUCTURE.md`). صفحات `/risk-score`, `/affiliate`, `/templates`, `/webinars` و**بوّابة الشريك** (`/partner`) ولوحات الـ ops الداخلية = **MISSING UI**.

---

## 5. حوكمة المبيعات والتسويق والتابعين — Governance Rules

**AR —** هذه القواعد **مفروضة مسبقاً** عبر `tests/test_no_*` و`test_landing_forbidden_claims.py` و`test_live_gates_default_false.py`. وكيل الحوكمة (Governance Agent) يراجع: ادعاءات التابعين، نسخ الإعلانات، نسخ صفحات الهبوط، نسخ البريد، إجابات الدعم، نصوص المبيعات، مسوّدات دراسات الحالة.

**ممنوع على التابعين والشركاء — Forbidden:**

- ادعاءات ROI/امتثال مضمونة — guaranteed ROI/compliance claims.
- "Dealix ترسل بالذكاء الاصطناعي ذاتياً" — "Dealix sends AI autonomously".
- واتساب بارد جماعي — cold WhatsApp mass.
- spam، استخدام شعار غير مصرّح، تسعير غير مُعلَن، دراسات حالة غير مصرّح بها.

**مسموح — Allowed:**

- الرسائل المعتمدة فقط، الـ Risk Score، عيّنة Proof Pack، دعوات webinar، الإحالات المؤهَّلة، مع الإفصاح.

| طبقة الحوكمة — Layer | Repo path | Status |
|---|---|---|
| ApprovalGate (Redis, CRITICAL_ACTIONS, 24h TTL, auto-approve risk<0.7) | `dealix/governance/approvals.py` | DONE |
| approval_tickets migration | `migrations/versions/20260515_103_approval_tickets.py` | DONE |
| Approval router | `api/routers/approval_center.py` | DONE |
| Agent run logs (AgentRunRecord) | `db/models.py`, `api/routers/agent_os.py`, `agents.py` | DONE |
| Audit log (PDPL Art. 18) | AuditLogRecord في `db/models.py` | DONE |
| Safe-send / channel policy gateway | `auto_client_acquisition/safe_send_gateway/`, `channel_policy_gateway.py` | DONE |
| Evidence control plane (9 modules) | `auto_client_acquisition/evidence_control_plane_os/` | PARTIAL — داخل العملية فقط |
| 11 non-negotiables tests | `tests/test_no_*.py`, `test_landing_forbidden_claims.py`, `test_live_gates_default_false.py` | DONE |

---

## 6. خارطة الطريق — Roadmap (ما المتبقي — What's Left)

**AR —** مرتّبة وفق ترتيب التنفيذ في القسم 21 من الاستراتيجية، ومُعاد صياغتها كـ"ما تبقى". الجهد: S (≤أسبوع) / M (1–2 أسبوع) / L (>2 أسبوع).

| # | البند — Item | الجهد | الحارس العقدي — Doctrine guardrail |
|---|---|---|---|
| 1 | **آلة حالة الفاتورة** — جدول `invoices` بحالات draft/sent/paid + استرجاع 30 يوماً | M | no live charge — مسوّدة فقط حتى تفعيل Moyasar |
| 2 | **تعزيز فرض الموافقة** — ربط CRITICAL_ACTIONS كحجوزات إلزامية على كل إجراء حيّ (حالياً اختياري) | M | no new allow-flags — لا تُفعِّل إجراءً تجاوزاً للبوّابة |
| 3 | **سجل الأدلة الدائم** — تعبئة جدول ProofEvent بدل المخزن داخل العملية | M | no fake proof / no fake revenue — لا أحداث مُصنَّعة |
| 4 | **جداول دعم/معرفة مخصّصة** — `support_tickets`, `knowledge_articles`, `knowledge_gaps` + حقل risk_score لكل إجابة + `/api/v1/knowledge/search` | M | no money promise / no security claim في الردّ التلقائي |
| 5 | **نموذج التابع المنفصل** — تمييز affiliate (4 فئات) عن partner (3 فئات) + جداول `commissions`/`payouts` | M | no spam, no cold WhatsApp باسم Dealix، الإفصاح إلزامي |
| 6 | **نموذج `POST /partner-apply` العام** + تأهيل اليوم 0–14 المؤتمت | S | المسوّدات فقط — كل تواصل خارجي يحتاج موافقة |
| 7 | **توحيد الموجِّهات** — دمج `growth_os/growth_v10/growth_beast` و`support_os/support_journey` | M | لا فرق سلوكي — إعادة هيكلة فقط |
| 8 | **مخطط UTM رسمي** + جدول `utm_events` | S | no PII logging في أحداث UTM |
| 9 | **نطاق النشرة** — `email_sequences`, `audiences` + بنية الكتل الخمس | M | no live send — تسلسل مُسوّد فقط |
| 10 | **نطاق الـ webinars** — جدول `webinars` + تسلسل التسجيل/الإعادة | M | no blast — دعوات مُستهدفة معتمدة فقط |
| 11 | **محرّك الـ lead magnets** — `POST /risk-score` + أصول الماكينة 4 القابلة للتنزيل | L | no guaranteed claims في الـ Risk Score |
| 12 | **محرّك upsell موصول** — ربط مسارات الـ upsell بمراحل الـ pipeline | M | الوكيل يُسوِّد العرض؛ المؤسس يوافق |
| 13 | **بوّابة الشريك UI** (`/partner`) ولوحات ops الداخلية | L | **لا تُبنى قبل عميل مدفوع** (انظر القسم 8) |
| 14 | **Paid Ads + Retargeting** | L | **لا تبدأ قبل رسالة مُثبتة** (انظر القسم 8) |

**قواعد التسلسل — Sequencing rules (إلزامية):**

1. لا برنامج تابعين قبل **رسائل معتمدة** (البنود 1–4 قبل 5–6).
2. لا إعلانات قبل **رسالة مُثبتة** (3–5 اجتماعات + اعتراضان + طلب proof-pack).
3. لا بوّابة عملاء قبل **عميل مدفوع واحد**.
4. لا SaaS قبل **سير عمل متكرر مُثبَت**.

**الفجوات العرضية (مُدرجة في خارطة الطريق):** فرض الموافقة (#2)، سجل الأدلة (#3)، آلة الفاتورة (#1)، تكرار الموجِّهات (#7)، جداول الدعم/المعرفة (#4)، نطاق النشرة/الـwebinar/الـlead-magnet (#9–11)، بوّابة الشريك (#13)، عمولات حيّة (#5).

---

## 7. أهداف 30 و90 يوماً — 30-Day & 90-Day Targets

### خطة 30 يوماً — 30-day plan

| الأسبوع | التركيز — Focus | الحالة الراهنة — Current state |
|---|---|---|
| W1 | نواة المبيعات — Sales core | ≈85% جاهز — يتبقّى آلة الفاتورة |
| W2 | المبيعات + الدعم — Sales + Support | الدعم ≈60% — يتبقّى جداول KB |
| W3 | ماكينة التسويق — Marketing machine | ≈55% — مولّدات المحتوى مؤجَّلة |
| W4 | ماكينة التابعين/الشركاء — Affiliate/Partner | ≈40–65% — يتبقّى نموذج التابع + العمولات |

### أهداف 90 يوماً — 90-day targets (مقابل الحالة الراهنة)

| الهدف — Target | الحالة — State |
|---|---|
| 3–5 diagnostics مدفوعة | محجوب على تفعيل Moyasar — التسويد جاهز |
| 1 Revenue Sprint, 1 retainer candidate | الوثائق جاهزة (`EXPANSION_OFFER_SYSTEM.md`) — الأتمتة جزئية |
| 20 تابعاً/شريكاً نشطاً، 5 شركاء إحالة أقوياء | التتبّع جاهز — نموذج التقديم العام مفقود |
| 1 webinar شهري، 1 نشرة نشطة | MISSING — يحتاج تحديد نطاق (البنود 9–10) |
| 1 KB دعم، 1 مكتبة proof pack | KB جزئية، مكتبة proof pack مفقودة |
| CAC واضح حسب القناة، أفضل ICP واضح | يحتاج مخطط UTM (البند 8) — ICP scoring جاهز |

---

## 8. ما الذي لا يُبنى الآن ولماذا — What NOT to Build Yet

**AR —**

1. **Paid Ads + Retargeting** — لا تبدأ قبل تحقّق رسالة مُثبتة (3–5 اجتماعات، اعتراضان متكرران، طلب proof-pack، ICP واضح). الإنفاق على رسالة غير مُثبتة يحرق رأس المال ويُخفي إشارة الـ ICP.
2. **بوّابة الشريك / بوّابة العميل (UI)** — لا تُبنى قبل عميل مدفوع واحد. البوّابة قبل العميل = صيانة بلا إيراد.
3. **منتج SaaS** — لا يُبنى قبل سير عمل متكرر مُثبَت عبر عدة عملاء. التحويل المبكّر إلى منتج يجمّد افتراضات غير مُختبَرة.
4. **مولّد مسوّدات المحتوى** — مؤجَّل عمداً (`docs/SELF_GROWTH_OS_SCOPE.md` §7-8). التدقيق والمعايرة آمنان للأتمتة؛ توليد النشر يحمل مخاطر no-fake-proof / no-guaranteed-claims ويحتاج بوّابة جودة 100% (حالياً ~70%).
5. **برنامج التابعين** — لا يُطلَق قبل اكتمال الرسائل المعتمدة وجداول العمولات؛ تابعون بلا أصول معتمدة = خطر ادعاءات.

**EN —** Defer paid ads and retargeting until the message is proven; defer partner/customer portals until a paid customer exists; defer SaaS until a workflow repeats; keep the content draft generator deferred until the QA gate reaches 100%; do not launch the affiliate program before approved messaging and commission tables exist. Every deferral protects a non-negotiable.

---

## 9. روابط ذات صلة — Related Docs

- `docs/growth/EXPANSION_OFFER_SYSTEM.md` — Upsell ladder
- `docs/growth/PROOF_TO_UPSELL_MAP.md`, `docs/growth/PROOF_TO_RETAINER_SYSTEM.md`
- `docs/growth/LEAD_SCORING_RULES.md`, `docs/growth/CRM_PIPELINE_SCHEMA.md`
- `docs/sales/SALES_PLAYBOOK.md`, `docs/SALES_OPS_SOP.md`
- `docs/MARKETING_AND_CONTENT_SYSTEM.md`, `docs/GEO_CONTENT_CALENDAR.md`
- `docs/AGENCY_PARTNER_PROGRAM.md`, `docs/40_partners/PARTNER_ECOSYSTEM.md`
- `docs/42_market_power/MARKET_POWER_OS.md`
- `docs/SELF_GROWTH_OS_SCOPE.md` — deferred-scope rationale

> **روابط لم تُحَل (للمؤسس):** لا توجد وثيقة نطاق منفصلة للنشرة/الـwebinar/الـlead-magnet بعد — البنود 9–11 من خارطة الطريق تحتاج وثائق نطاق مستقبلية ترتبط هنا.

---

> **Disclosure / إفصاح:** Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
