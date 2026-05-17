# Revenue Operating Machine — Gap Analysis & Roadmap

> تحليل استراتيجية "ماكينة الإيراد" (25 قسم / 12 ماكينة) مقابل الكود الفعلي في المستودع.
> **التاريخ:** 2026-05-17 · **الفرع:** `claude/dealix-revenue-machine-dhiov`

---

## 0. الحكم التنفيذي (Executive Verdict)

**أنت لم تَعُد تبني ماكينة الإيراد. أنت بنيتها بالفعل.**

المستودع فيه **183 وحدة** تحت `auto_client_acquisition/`. عند مطابقة الـ12 ماكينة في استراتيجيتك مع الكود الفعلي:

- **9 من 12 ماكينة موجودة وكاملة** (مربوطة بـ API + مغطاة باختبارات).
- **3 ماكينات بها فجوات حقيقية** (Webinar غير موجودة، Retargeting/UTM شبه فارغة، Partner Portal UI واجهة فقط).
- طبقة الحوكمة (Approval Center + Evidence Ledger + Doctrine + الـ11 non-negotiables) **كاملة ومُختبَرة** — هذه أصعب طبقة وهي جاهزة.

**الخطر الحقيقي ليس نقص ماكينات. الخطر هو بناء المزيد من الماكينات بينما العائق الفعلي في مكان آخر** (راجع القسم 4).

---

## 1. مطابقة الـ12 ماكينة مع الكود (Machine → Repo Map)

| # | الماكينة | الحالة | الوحدة في المستودع | ملاحظة |
|---|----------|--------|---------------------|--------|
| 1 | **Sales Machine** | ✅ كاملة | `agents/intake.py`, `crm_v10/`, `icp_scorer.py`, `agents/outreach.py`, `email/reply_classifier.py`, `api/routers/{leads,outreach,crm_v10,automation}.py` | القمع كامل من الـlead حتى الـCRM؛ مربوط + مُختبَر. |
| 2 | **Support Machine** | ✅ كاملة | `support_os/` (classifier, knowledge_answer, escalation), `knowledge_v10/`, `customer_inbox_v10/` | تصنيف القاعدة + KB + RAG + تصعيد؛ draft-only. |
| 3 | **Marketing / Content** | 🟡 جزئية | `growth_beast/content_engine.py`, `gtm_os/content_calendar.py` | توليد تقويم محتوى + أفكار؛ لا نشر آلي. |
| 4 | **Media / Authority** | ✅ كاملة | `command_os/market_authority_score.py`, `category_os/`, `founder_v10/daily_brief.py` | تسجيل سلطة السوق + إشارات الفئة. |
| 5 | **Affiliate Machine** | 🟡 جزئية | `partnership_os/`, `ecosystem_os/partner_score.py`, `api/routers/referral_program.py` | التتبع والتسجيل موجود؛ منطق الـclawback ولوحة الشريك ناقصة. |
| 6 | **Partner Distribution** | ✅ كاملة | `partnership_os/{partner_profile,partner_motion,referral_tracker}.py`, `public.py` (`/partner-application`) | الملف + التقييم + بوابة الـ7 معايير جاهزة. |
| 7 | **Webinar Machine** | ❌ غير موجودة | — | لا توجد أي وحدة تسجيل/إدارة webinar. |
| 8 | **Newsletter / Email** | ✅ كاملة | `email/` (transactional, daily_targeting, gmail_send), `api/routers/email_send.py` | إرسال Gmail OAuth + بوابات امتثال PDPL + استيعاب الردود. |
| 9 | **SEO Machine** | 🟡 جزئية | `self_growth_os/` (seo_technical_auditor, internal_linking_planner, proof_snippet_engine) | تدقيق SEO + روابط داخلية؛ لا نشر صفحات حي. |
| 10 | **Referral Machine** | ✅ كاملة | `partnership_os/{referral_tracker,referral_store}.py`, `api/routers/referral_program.py` | 5 حالات إحالة + JSONL + جدول `referral_payouts`. |
| 11 | **Upsell Machine** | ✅ كاملة | `growth_beast/offer_intelligence.py`, `finance_os/pricing_catalog.py` | سلّم الـ5 درجات مُرمَّز؛ مطابقة قطاع/إشارة → عرض. |
| 12 | **Governance Machine** | ✅ كاملة | `approval_center/`, `evidence_control_plane_os/`, `safe_send_gateway/doctrine.py`, `governance_os/draft_gate.py` | 7 فحوص doctrine + 11 non-negotiable + سجل أدلة بـ11 نوع. |

**الخلاصة:** 9 ✅ كاملة · 3 🟡 جزئية · 1 ❌ مفقودة (Webinar).

---

## 2. الفجوات الحقيقية (Real Gaps — Buildable Work)

هذه فقط الأشياء التي تستحق كتابة كود لها. كل ما عداها موجود.

| الفجوة | الحالة الحالية | الجهد | الأولوية | السبب |
|--------|----------------|-------|----------|-------|
| **Commission clawback-on-refund** | ثوابت ساكنة في `referral_program.py`؛ لا منطق استرداد ديناميكي | صغير (~يوم) | **عالية متى وُجد شركاء** | بدونه خطر مالي: تدفع عمولة على صفقة تُسترَد لاحقاً. |
| **Partner Portal API + dashboard** | `ecosystem_os/partner_portal.py` مجرّد scorer؛ لا API ولا UI | متوسط (~2-3 أيام) | متوسطة | يلزم فقط بعد تجنيد أول 5 شركاء فعليين. |
| **Approved-assets library + disclosure** | `governance_os/draft_gate.py` يدقق النص؛ لا مكتبة أصول ولا أتمتة إفصاح | صغير-متوسط | متوسطة | مطلوب قبل إطلاق برنامج العمولة علناً (مخاطر تنظيمية/PDPL). |
| **Webinar Machine** | غير موجودة | متوسط (~3 أيام) | **منخفضة** | رافعة متأخّرة؛ لا قيمة قبل أول 3-5 عملاء مدفوعين. |
| **Retargeting / UTM event tracking** | `daily_targeting.py` فقط؛ لا UTM ولا pixel | متوسط | **منخفضة** | لا معنى للـretargeting قبل وجود ترافيك مدفوع. |
| **Meeting Brief + Scope Builder كـ endpoints** | المنطق موجود (`personal_operator/llm_brief.py`, `sales_os/scope_renderer.py`) لكنه غير معروض كـ API | صغير | منخفضة | المنطق جاهز؛ مجرد تغليف router. |

---

## 3. ما لا يجب بناؤه (Do NOT Build)

استراتيجيتك تطلب 25 قسماً. المستودع يغطي ~22 منها. بناء الباقي **لن يُنتج إيراداً** — سيؤخّره.

- ❌ لا تُعِد بناء `partnership_os` — موجود وكامل.
- ❌ لا تُعِد بناء Approval Center / Evidence Ledger / Doctrine — أصعب طبقة، جاهزة ومُختبَرة.
- ❌ لا تبنِ Webinar/Retargeting الآن — رافعات متأخّرة بلا جمهور.
- ❌ لا تبنِ "Growth Orchestrator" جديد — التنسيق موجود في `core.agents` + routers.

**المبدأ:** المستودع مُفرَط في البناء (over-built) وليس ناقصاً. إضافة ماكينات لا تحرّك الإيراد.

---

## 4. العائق الحقيقي (The Actual Bottleneck)

ماكينة الإيراد جاهزة تقنياً. ما يمنع الإيراد **ليس كوداً**:

1. **تفعيل حساب Moyasar** — `account_inactive_error`. لا يمكن تحصيل ريال واحد حتى يكمل سامي الـKYC في لوحة Moyasar. (راجع `DEALIX_COMPANY_OPERATIONAL_STATE.md`).
2. **أول رسالة تواصل (Outreach)** — الـ5 leads الأولى + الرسائل المخصّصة جاهزة في `docs/ops/launch_content_queue.md`. تنتظر فقط ضغطة "إرسال" من سامي (إجراء هوية، لا أتمتة).
3. **أول 3-5 عملاء مدفوعين** — لا يوجد affiliate ولا partner ولا webinar له قيمة قبل إثبات أن العرض يُغلَق يدوياً.

> **القاعدة:** لا تبنِ Affiliate/Partner/Webinar قبل إثبات البيع اليدوي. وإلا فأنت تؤتمت قمعاً غير مُثبَت.

---

## 5. التسلسل الموصى به (Recommended Sequence)

```
الآن        →  فكّ عائق Moyasar (سامي) + إرسال أول DM (سامي)   ← لا كود
أول 3-5 عملاء  →  بيع يدوي عبر القمع الموجود (Sales Machine جاهزة)
ثم          →  Commission clawback-on-refund  ← أول كود يستحق الكتابة
ثم          →  Approved-assets library + disclosure
ثم          →  Partner Portal API + dashboard  ← عند وجود 5 شركاء
لاحقاً      →  Webinar + Retargeting  ← عند وجود جمهور مدفوع
```

**أول مهمة هندسية حقيقية متى أردت كتابة كود:** `Commission clawback-on-refund` —
يربط webhook الاسترداد من Moyasar (`payment_refunded`) بحالة الإحالة في
`partnership_os/referral_store.py`، فيُلغي/يستردّ العمولة داخل نافذة الـ30 يوماً.
صغير، محدّد، ويغلق خطراً مالياً حقيقياً قبل أن يصبح خطراً.

---

## 6. الخلاصة بجملة واحدة

> ماكينة الإيراد مبنيّة. القرار ليس "ماذا نبني" — القرار هو "فكّ Moyasar، أرسل أول DM، أغلق أول 5 عملاء يدوياً" — ثم نضيف الـclawback كأول كود يستحق الكتابة.
