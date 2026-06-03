# Dealix Operating Missions — مهام Dealix التشغيلية

> **الطبقة:** هذه الوثيقة تعرّف الطبقة الجديدة **Dealix Operating Missions** التي تجلس *تحت* الأعمدة الأربعة المواجهة للعميل، وليست تصنيفاً جديداً منفصلاً.
>
> **مصدر الحقيقة في الريبو (Source of truth):** هذه الوثيقة لا تخترع منتجاً جديداً، بل تعيد تغليف القدرات الموجودة فعلاً في:
> - `company_os/delivery/p1_delivery_sop.md` (مخرجات الـ Sprint)
> - `company_os/marketing/one_pagers/one_pager_arabic.md` و `company_os/marketing/pitch_deck/outline.md` (التموضع والأسعار)
> - `company_os/revenue/*` (outreach_queue / followups / proposals / objections / prospects)
> - `company_os/delivery/proof_pack_template.md` و `company_os/war_room/*` (الإثبات والتقارير)
> - `company_os/governance/agent_permissions.md` و `pdpl_checklist.md` (الحوكمة والخطوط الحمراء)
> - `src/pages/LandingPage.tsx` (الأسماء المواجهة للعميل حالياً)

---

## 0. الملخص في سطر واحد

```txt
Dealix لا يبدأ بكل شيء. Dealix يبدأ بأهم مهمة تشغيلية عندك الآن، ثم يحوّلها إلى نظام تشغيل إيرادات قابل للقياس.
```

العميل **لا** يرى 40 خدمة. يرى:
1. **براند واحد** — Dealix.
2. **4 أعمدة** — Radar, AI Team, Portal, Proof.
3. **مهمة واحدة يبدأ بها** — من قائمة الـ 8 مهام أدناه.

---

## 1. الهيكل الكامل (3 طبقات + عمود حوكمة)

```txt
البراند:   Dealix — نظام تشغيل الإيرادات للشركات السعودية (Saudi-first) · GCC-ready

الطبقة 1 — الأعمدة الأربعة (المنصّة التي يراها العميل):
   • Dealix Radar    → يرى أين تضيع الإيرادات وماذا يفعل
   • Dealix AI Team  → يجهّز العمل اليومي للإيراد (بحث، صياغة، متابعة، عروض)
   • Dealix Portal   → واجهة العميل والتسليم (workspace، onboarding، تقارير، موافقات)
   • Dealix Proof    → الدليل والنتائج والشفافية (Proof Pack، CEO Brief، case studies)

الطبقة 2 — Dealix Operating Missions (الطريقة التي نبيع بها): 8 مهام

الطبقة 3 — Services داخل كل Mission (الوحدات التشغيلية الفعلية)

العمود الحاكم (يخترق كل الطبقات): Governance Spine
   Observe → Advise → Draft → Act with Approval   (Autonomous = ممنوع الآن)
   PDPL/SDAIA · ai_action_ledger · بشري يوافق على كل إرسال/تسعير/تسليم
```

> الأسماء الداخلية الكثيرة في الريبو **لا تظهر للعميل**؛ تُربط دائماً تحت أحد الأعمدة الأربعة.

---

## 2. لماذا "Missions" وليس "قائمة خدمات"؟

| إذا قلنا للعميل…                         | شعوره            | النتيجة         |
| ---------------------------------------- | ----------------- | ---------------- |
| "نقدّم تسويق + مبيعات + واتساب + أتمتة…" | عرض عام ومبهم     | لا يشتري        |
| "نبدأ بمهمة تشغيلية واحدة، ثم نوسّعها"   | واضح وقابل للقياس | يبدأ ثم يتوسّع   |

هذا يسمح لنا أن نقدّم "كل شيء" دون أن نظهر مشتّتين: كل خدمة تُباع كـ **Mission** لها مخرج واضح ودليل قيمة سريع.

---

## 3. كتالوج الـ 8 مهام (Operating Missions)

> كل Mission تُغلّف تجارياً عبر منتجَي الريبو الحاليين:
> **P1 — Revenue Intelligence Sprint** (2,500–7,500 ر.س، 5 أيام) كمدخل تشخيصي، و**P2 — AI Sales Ops Retainer** (3,000–20,000 ر.س/شهر) كتشغيل مستمر.
> التفاصيل الكاملة للأسعار والترقية في `docs/commercial/MISSION_PACKAGING_MAP_AR.md`.

### M1 — Revenue Leakage Mission · مهمة كشف تسرّب الإيراد
- **لمن؟** شركة لا تعرف أين تضيع الفرص ولا حجم التسرّب.
- **الإشارة (Signal):** "founder blind to pipeline" / "weak CRM usage".
- **الألم المحتمل:** قرارات بلا رؤية، إنفاق إعلاني بلا قياس تحويل.
- **المخرج:** Revenue Leakage Map + أولويات التسرّب + تقدير الإيراد المعرّض للخطر.
- **العمود القائد:** Radar (يدعمه Proof).
- **التغليف:** P1 Sprint (مدخل).
- **المهمة التالية:** M2 Follow-up Recovery أو M8 Full Revenue OS.
- **زاوية الإثبات:** before/after لخريطة التسرّب + رقم الإيراد المُستردّ المتوقّع.
- **أمثلة من `prospects.csv`:** TechVenture Partners، Nexus IT Solutions، CloudShift Consulting.

### M2 — Follow-up Recovery Mission · مهمة استرداد المتابعات
- **لمن؟** شركة عندها leads تأتي لكن تضيع بلا متابعة منظمة.
- **الإشارة:** "no follow-up system" / "follow-up takes too long" / "leads from ads not followed up".
- **الألم المحتمل:** 37% من الفرص تضيع بعد أول رد (مرجع داخلي في `war_room/REVENUE_WAR_ROOM_TODAY.md`).
- **المخرج:** follow-up queue + drafts جاهزة + إيقاع متابعة (3/7/14 يوم — مطابق لـ `revenue/followups.json`).
- **العمود القائد:** AI Team (يدعمه Radar).
- **التغليف:** P1 Sprint → ترقية إلى P2.
- **المهمة التالية:** M3 Sales Draft Factory.
- **زاوية الإثبات:** عدد الفرص المُستردّة + تقرير أسبوعي بما حدث.
- **أمثلة:** Growth Labs SA، LearnFast Academy، BrandCraft Agency.

### M3 — Sales Draft Factory Mission · مهمة مصنع المسودات
- **لمن؟** شركة تحتاج رسائل ومتابعة بحجم كبير ومخصّصة.
- **الإشارة:** فريق مبيعات صغير + قاعدة prospects كبيرة.
- **الألم المحتمل:** الطاقة البشرية لا تكفي لتخصيص الرسائل.
- **المخرج:** حتى **400 draft/day** + approval queue + Top-100 مرتّبة للمراجعة. (التفاصيل في `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md`.)
- **العمود القائد:** AI Team.
- **التغليف:** P2 Retainer.
- **قاعدة حاكمة:** 400 **draft**/day مسموح. 400 **send**/day **ليس** مفعّلاً افتراضياً — يتطلب جاهزية تسليم ودومين وموافقة.
- **المهمة التالية:** M5 Proposal & Proof.
- **أمثلة:** Digital Rise Agency، MediaPulse Agency.

### M4 — WhatsApp Client OS Mission · مهمة تشغيل عملاء واتساب
- **لمن؟** شركة تتعامل بكثافة عبر واتساب (تدريب، عيادات، خدمات).
- **الإشارة:** "WhatsApp inquiries lost".
- **الألم المحتمل:** استفسارات واتساب لا تتحوّل لتسجيلات بسبب بطء الرد/غياب المتابعة.
- **المخرج:** action cards + scans لمحادثات العميل **المملوكة له** + handoff منظّم للبشر.
- **العمود القائد:** AI Team + Portal.
- **خط أحمر:** **لا أتمتة واتساب باردة (No cold WhatsApp automation).** نعمل فقط على محادثات العميل الواردة/المملوكة، والإرسال بشري. (راجع `docs/outreach/GCC_OUTREACH_POLICY_AR.md`.)
- **التغليف:** P1 تشخيص → P2 تشغيل.
- **المهمة التالية:** M2 ثم M6.
- **أمثلة:** TrainMe KSA، Elevate Training، NextGen Training.

### M5 — Proposal & Proof Mission · مهمة العروض والإثبات
- **لمن؟** شركة تحتاج عروضاً منظّمة ودليل قيمة.
- **الإشارة:** "proposals not tracked" / "deals stuck in proposal stage" / "no proof for clients".
- **الألم المحتمل:** عروض غير متّسقة، صفقات عالقة، لا دليل ROI.
- **المخرج:** proposal منظّم + Proof Pack (مبني على `delivery/proof_pack_template.md`).
- **العمود القائد:** AI Team + Proof.
- **التغليف:** P1 (مراجعة جودة العرض) → P2 (مصنع عروض + proof مستمر).
- **المهمة التالية:** M6 Customer Success.
- **أمثلة:** LegalEdge SA، Alpha Consulting Group، MediaPulse Agency.

### M6 — Customer Success Mission · مهمة نجاح العملاء والتجديد
- **لمن؟** شركة عندها عملاء وتريد تقليل churn ورفع التجديد.
- **الإشارة:** "client churn due to no ROI proof".
- **الألم المحتمل:** فقدان عملاء بلا إنذار مبكر ولا دليل قيمة دوري.
- **المخرج:** health score + renewal/upsell queue + تقرير قيمة دوري. (مبني على `delivery/client_success_plan.md`.)
- **العمود القائد:** Portal + Proof (يدعمه AI Team).
- **التغليف:** P2 Retainer.
- **المهمة التالية:** M8 Full Revenue OS.
- **أمثلة:** Saudi Marketing Pro.

### M7 — GTM Expansion Mission · مهمة التوسّع في السوق
- **لمن؟** شركة تريد دخول قطاع/مدينة/سوق جديد.
- **الإشارة:** نمو، توظيف Sales Ops، إطلاق منتج جديد.
- **الألم المحتمل:** توسّع بلا signals ولا قائمة prospects ولا محتوى ولا شراكات.
- **المخرج:** signals + prospects مؤهّلة + محتوى + شراكات/إحالات.
- **العمود القائد:** Radar + AI Team.
- **التغليف:** P2 Retainer (مسار نمو موازٍ).
- **المهمة التالية:** M8 Full Revenue OS.

### M8 — Full Revenue OS Mission · مهمة نظام الإيراد الكامل
- **لمن؟** شركة تريد نظام تشغيل إيرادات كامل.
- **المخرج:** الأعمدة الأربعة مفعّلة معاً: Radar + AI Team + Portal + Proof.
- **التغليف:** P2 Enterprise Retainer (أعلى tier في `finance/unit_economics.md`).
- **هذه هي الوجهة:** كل مهمة أصغر تقود إليها بالدليل والنتيجة، لا بالضغط البيعي.

---

## 4. منطق التتابع (Mission Ladder)

```txt
M1 Revenue Leakage  ─▶ M2 Follow-up Recovery ─▶ M3 Sales Draft Factory ─▶ M5 Proposal & Proof
                                                                              │
M4 WhatsApp Client OS ───────────────────────────────────────────────────────┤
                                                                              ▼
                                              M6 Customer Success ─▶ M8 Full Revenue OS
M7 GTM Expansion  ───────────────(مسار نمو موازٍ)──────────────────────────────▲
```

**القاعدة الذهبية:** كل Mission تنتهي بـ **Proof** و**Renewal**، وكل Mission تقود إلى Mission أكبر — بالدليل، لا بالوعود.

---

## 5. الخطوط الحمراء (مطابقة لـ `governance/agent_permissions.md`)

- لا إرسال خارجي بلا موافقة بشرية.
- لا معالجة PII خام في أدوات عامة.
- لا قرارات تسعير من AI.
- لا أتمتة واتساب باردة · لا أتمتة LinkedIn · لا قوائم مشتراة · لا Re/Fwd مزيّف.
- لا وعود/ضمانات نتائج (No guaranteed claims).
- 400 draft/day ✅ · 400 send/day ❌ افتراضياً (راجع سياسة الإرسال).

---

*Owner: Founder · Status: Proposed canonical architecture · يتطلب قرار مؤسس للتفعيل في `src/` (راجع التقرير النهائي).*
