# Dealix — تصميم الفئة والمنظومة التشغيلية القصوى

هذا المستند **مرافق** لـ [SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md): الرادارات تركز على **كيف نشغّل الشركة أسبوعياً مع أدلة**؛ هذا الملف يجيب: **لماذا نفوز في الفئة، أي معمارية نبني نحوها، وما خارطة 12 شهراً.**
ولنسخة "خريطة السيطرة" المخصصة لفئة **Governed Revenue & AI Ops** راجع: [GCC_GOVERNED_REVENUE_AI_OPS_CONTROL_MAP_AR.md](GCC_GOVERNED_REVENUE_AI_OPS_CONTROL_MAP_AR.md).

**تنبيه للمراجعات الخارجية:** الروابط أدناه إلى مواقع جهات خارجية قد تتغير. راجع المصدر الرسمي قبل أي نشر أو عقد.

---

## 0) الفكرة الأم: لا تبنِ شركة أدوات، ابنِ شركة تشغيل دخل

المنافسون يبيعون عادة **جزءاً واحداً:** CRM يخزن · أداة واتساب ترسل · كاتب AI ينص · وكالة تنفذ يدوياً · أداة leads تعطي قوائم · مستشار يعطي رأياً.

Dealix يربطها في **سلسلة واحدة:**

```text
Signal → Context → Service Recommendation → Risk Check → Draft → Approval
→ Execution → Outcome → Proof → Learning → Upgrade
```

**التموضع النهائي**

```text
Dealix = Saudi Revenue Operating System
للشركات والوكالات التي تريد فرصاً، رسائل، اجتماعات، متابعة، وProof
بدون حرق القنوات.
```

عربياً يمكن صياغته: **نظام تشغيل النمو والمبيعات للشركات السعودية.**

ارتباط داخلي: [DEALIX_V3_AUTONOMOUS_REVENUE_OS.md](../DEALIX_V3_AUTONOMOUS_REVENUE_OS.md) · [BUSINESS_MODEL.md](../BUSINESS_MODEL.md)

---

## 1) Market Intelligence System — رادار السوق

### رادار القطاعات

لكل قطاع: `pain` · `buyer` · `trigger` · `best channel` · `opening angle` · `offer` · `risk` · `proof metric`

| القطاع | الألم (مختصر) | عرض قوي |
|--------|----------------|---------|
| الوكالات | leads تضيع بعد الحملات | Agency Partner Pilot |
| العقار | تأهيل ميزانية/منطقة/نوع عقار | Lead qualification + follow-up |
| التدريب | استفسارات كثيرة وتحويل ضعيف | Meeting Sprint |
| المتاجر | عملاء سابقون وقوائم غير مستغلة | Reactivation |
| خدمات B2B | لا يعرفون من يستهدفون | Growth Starter |

### رادار الإشارات (أمثلة)

فرع جديد · حملات منشورة · توظيف Sales/Marketing · إطلاق منتج · نموذج leads بلا متابعة · إعلانات قوية · موقع فيه واتساب فقط بلا CRM · تكرار «نستقبل طلبات».

### رادار المناطق والاستهداف

ابدأ بـ **قطاع × مدينة × قناة × عرض** لا «السعودية» ككتلة واحدة.

**بيانات السوق (حسب ما نُشر):** وكالة الأنباء السعودية نقلت عن منشآت أرقاماً تشير إلى نمو في السجلات التجارية في Q4 2024 وإجمالي يُذكر في التقارير بحدود **1.6 مليون** سجل تجاري، مع تركز جغرافي يُذكر للرياض ومكة والشرقية — استخدم ذلك كـ **خريطة أولية** للتركيز (الرياض أولاً، ثم جدة/مكة، ثم الشرقية) مع التحقق من أحدث بيانات المنشأة. [SPA — Monshaat commercial registrations Q4 2024](https://www.spa.gov.sa/en/N2273553)

---

## 2) Category Design — بناء الفئة

إذا قلت «CRM بالذكاء الاصطناعي» تُقارن بـ HubSpot وSalesforce. إذا قلت «بوت واتساب» تُقارن بأدوات إرسال. إذا قلت «نجيب leads» تُقارن بفريلانسر.

**الفئة الصحيحة:** `Revenue Execution OS` — تنفيذ إيرادات مربوط بسياق سعودي، موافقة، وProof.

| الفئة | ماذا تقدم | أين Dealix يتفوق |
|-------|-----------|------------------|
| CRM | تخزين pipeline | `next_step` يومي وتشغيل |
| أتمتة واتساب | إرسال | قرار: هل الإرسال **آمن** أصلاً |
| AI writer | نصوص | النص مربوط بفرصة وقناة وProof |
| قاعدة leads | بيانات | تحويل إلى Pilot وتسليم |
| وكالة | تنفيذ بشري | playbook قابل للتكرار والقياس |
| مستشار | رأي | workflow + scorecard |
| Salesforce / HubSpot | منصات مؤسسات + agents | Dealix: **Saudi SMB-first** · عربي · واتساب-aware · service-first · Proof Pack |

مرجع تنافسي موسّع: [COMPETITIVE_POSITIONING.md](../COMPETITIVE_POSITIONING.md)

---

## 3) Product Architecture — المعمارية (7 طبقات)

### الطبقة 1 — Intake Layer

حقول أساسية: الشركة · القطاع · المدينة · العرض · العميل المثالي · القنوات الحالية · قوائم موجودة؟ · الموافقة.  
**الهدف:** فهم تجاري لا جمع بيانات زائد.

### الطبقة 2 — Knowledge Layer

لكل عميل: FAQ · عروض · أسعار · اعتراضات · لغة · سياسات · قطاعات مستهدفة · قوائم/فرص.

### الطبقة 3 — Lead Graph

ليس «قائمة شركات» فقط: `Account` · `Contact` · `Source` · `Signal` · `Score` · `Risk` · `Channel` · `Next action` · `Outcome`.  
ارتباط تشغيلي: [DATA_MAP.md](../DATA_MAP.md) · [DATA_LAKE_PLAYBOOK.md](../ops/DATA_LAKE_PLAYBOOK.md)

### الطبقة 4 — Policy Engine

حكم لكل فعل: `Auto` · `Approval required` · `Blocked`.

| القناة / الفعل | حكم مقترح |
|----------------|-----------|
| رد على نموذج موقع | Auto أو assisted |
| واتساب inbound | مسموح ضمن نافذة الخدمة والسياسة |
| واتساب بارد | Blocked |
| LinkedIn DM | **يدوي** + موافقة (لا أتمتة مخالفة لسياسة المنصة) |
| دفع / فاتورة | موافقة بشرية في المراحل المبكرة |
| بيانات حساسة | Escalate |

LinkedIn يحدّ من البرمجيات والامتدادات التي تؤتمت النشاط أو تسحب البيانات بطرق محظورة — راجع المساعدة الرسمية: [Prohibited software and extensions — LinkedIn Help](https://www.linkedin.com/help/linkedin/answer/a1341387)

### الطبقة 5 — Card Layer

كل شيء يصير كرت: Lead جديد · بيانات ناقصة · Diagnostic جاهز · Follow-up · Pilot محتمل · Invoice · Proof Pack · Upgrade.  
المحتوى: ماذا حدث · لماذا الآن · الإجراء المقترح · المخاطر · أثر Proof · أزرار موافقة/تعديل/تخطي.

### الطبقة 6 — Execution Layer

رسائل · إيميلات (مسودات) · ردود واتساب inbound · متابعات · ملاحظات اجتماع · تعليمات فاتورة · Proof Pack.

### الطبقة 7 — Learning Layer

بعد كل دورة: أي قناة؟ أي رسالة؟ نتيجة؟ اعتراض؟ دفع؟ تجديد؟ الدرس؟ — هنا يتكون الـ moat.

---

## 4) GTM Strategy — استراتيجية الدخول

**Wedge 1 — الوكالات:** تفهم leads · لديها عملاء · تحتاج Proof لعملائها · قد تشترى أو تحيل.

**Wedge 2 — B2B services:** استشارات · تدريب · محاسبة · تقنية · HR · مقاولات خفيفة.

**Wedge 3 — قطاعات عالية leads:** عقار · فنادق · قاعات · مطاعم · نقل · مقاولات — قناة بداية مختلفة لكل قطاع.

ارتباط: [GTM_PLAYBOOK.md](../GTM_PLAYBOOK.md) · [docs/playbooks/](../playbooks/) · [docs/partners/](../partners/)

---

## 5) Offer Ladder — سلم العروض

تسلسل مقترح:

```text
Free Diagnostic → Managed Pilot (مثلاً 499 SAR / 7 أيام) → Starter شهري (999–3K SAR مبدئياً)
→ Growth OS Pro → Agency Partner → Enterprise
```

**Free Diagnostic:** 3 فرص · رسالة واحدة · قناة · مخاطرة · توصية.

**Pilot:** نطاق زمني وعدد leads/فرص ورسائل وفق العرض؛ **بدون** وعود ضمان إيراد أو spam أو أتمتة لقنوات محظورة.

السلم المفصل في الريبو: [OFFER_LADDER.md](../OFFER_LADDER.md) — راجعه مع هذا القسم للاتساق.

---

## 6) Sales System — نظام البيع

**Pipeline (مثال)**

```text
New → Qualified → Diagnostic Requested → Diagnostic Sent → Meeting Requested
→ Pilot Offered → Invoice Sent → Paid/Committed → Delivery Started
→ Proof Delivered → Upgrade Offered → Closed / Nurture
```

**لكل صف:** owner · next_step · deadline · channel · last_touch · risk · expected value

### قواعد

```text
لا lead بدون next_step.
لا Diagnostic بدون follow-up.
لا اهتمام بدون Pilot offer (حيث ينطبق).
لا قبول بدون invoice (عند الالتزام المدفوع).
لا Delivery بدون Proof.
```

---

## 7) Delivery System — نظام التسليم

**Delivery Pack (Pilot)** يتضمن على الأقل: Client brief · Target segment · 10 opportunities · لكل فرصة: why-fit · why-now · decision maker role · recommended channel · first message · follow-up 1 و2 · risk note · next step.

**معيار الجودة:** إذا قال العميل «طيب وش أسوي؟» فشل الملف. إذا قال «واضح، أقدر أرسل هذا اليوم» فاز.

---

## 8) Proof System — نظام الإثبات

Proof Pack أصل استراتيجي: What was created · What was protected · What needs approval · Revenue impact estimate · Next recommended action.

**مقاييس مثال:** opportunities_created · drafts_created · followups_planned · risks_blocked · messages_approved · meetings_suggested · conversion_stage.

يحوّل البيع من «صدقني» إلى «شاهد ماذا أنجزنا.»

---

## 9) Compliance & Trust System — الثقة والامتثال

**PDPL (إطار عمل):** البيانات الشخصية قد تشمل ما يعرّف الفرد بما فيه وسائل التواصل؛ التسويق المباشر يتطلب أسساً قانونية وموافقة/انسحاب وسجلات حسب النظام — راجع مركز المعرفة: [SDAIA Data Governance Platform — PDPL](https://dgp.sdaia.gov.sa/wps/portal/pdp/knowledgecenter)

**WhatsApp:** نافذة خدمة العميل (رسائل الجلسة) تختلف عن الرسائل خارجها؛ التوسع يتطلب قوالب وسياسات Meta — راجع الوثائق الرسمية: [WhatsApp Business Platform — Overview](https://developers.facebook.com/docs/whatsapp/overview)

**ممنوعات ثابتة:** cold WhatsApp · scraping جماعي لـ LinkedIn · إرسال جماعي بلا opt-out · دفع live بلا سياسة · تسرّب أسرار · وعود ضمان إيراد.

حقول تسجيل مقترحة: consent_source · time_of_consent · channel_allowed · opt_out · last_touch_at · message_type · risk_note.

ارتباط: [PRIVACY_PDPL_READINESS.md](../PRIVACY_PDPL_READINESS.md) · [WHATSAPP_OPERATOR_FLOW.md](../WHATSAPP_OPERATOR_FLOW.md)

---

## 10) Data System — نظام البيانات

**كائنات أساسية:** Company · Contact · Lead · Source · Consent · Signal · Message · Action · Outcome · Proof · Customer · Partner · Invoice.

**كل lead:** source · consent_source · sector · city · goal · recommended_service · score · risk · next_step · status · outcome.

**كل رسالة:** channel · template · reason · approval_status · sent_by · sent_at · reply_status · opt_out_status.

---

## 11) AI System — الذكاء الاصطناعي

**AI يفيد في:** بحث · تلخيص · score · recommend · draft · risk-check · ضبط نبرة · اقتراح Proof · اقتراح next_step.

**AI لا يفعل وحده:** إرسال واتساب حي · سحب LinkedIn آلي · «ضمان مبيعات» · قرار قانوني · عرض enterprise بدون مراجعة.

**فلترة جودة (7):** نبرة سعودية · دقة · تخصيص · أمان القناة · لا مبالغة في الوعود · next action واضح · ربط بـ Proof.

---

## 12) Competitive Intelligence — مقارنة المنصات العالمية

- **Salesforce Agentforce:** اتجاه المنصات نحو وكلاء AI مع **رؤية وسيطرة** وتشغيل مؤسسي — درس: أي agent قوي يحتاج observability/control لا مجرد تنفيذ. [Salesforce investor news — Agentforce](https://investor.salesforce.com/news/news-details/2025/Salesforce-Launches-Agentforce-3-to-Solve-the-Biggest-Blockers-to-Scaling-AI-Agents-Visibility-and-Control/default.aspx)

- **HubSpot Breeze (AI prospecting):** إشارات شراء وبحث وصياغة outreach — السوق يتجه لـ agents تراقب وتتصرف عند التوقيت. [HubSpot — Breeze Prospecting Agent](https://www.hubspot.com/products/sales/ai-prospecting-agent)

**موقع Dealix:** ليس أقوى CRM ولا أكبر قاعدة بيانات — بل **طبقة تنفيذ إيرادات سعودية SMB** بين هذه الأدوات: عربي · موافقة أولاً · Proof Pack · يدوي حيث تفرض المنصة أو القانون.

---

## 13) Brand System — العلامة

**المظهر:** سعودي · عملي · احترافي · آمن · مباشر · لا أوهام.

**وعود مقترحة:** «من الفوضى إلى next step واضح.» أو «نحوّل الاستفسارات والفرص إلى متابعة وProof.»

**تجنب:** نضمن · نضاعف · أوتوماتيك كامل · بدون مجهود · نرسل للجميع.

**استخدم:** نرتب · نقترح · نجهز · نراجع · نثبت · نقيس · نحمي القناة.

---

## 14) Partnership System — الشراكات

أنواع: Referral · Implementation · Service exchange · Co-selling pilot · white-label **لاحقاً** فقط بعد Proof.

**قواعد مبكرة:** لا exclusivity في البداية · لا white-label قبل proof · لا revenue share بلا تتبع · لا custom build قبل دفع · ابدأ بعميل واحد.

**أفضل طلب:** «أعطني عميلاً واحداً leads تضيع بعد الحملة، وأطلع له audit/pilot.»

---

## 15) Finance & Unit Economics — المالية

لكل Pilot: Revenue · ساعات التسليم · تكلفة الساعة · هامش إجمالي · وقت التسليم · احتمال التحويل شهرياً.

**تتبع:** Cash collected · Invoices sent/paid · Pilot→Monthly · ساعات التسليم لكل pilot · إيراد حسب القطاع · إيراد من شركاء.

**رفع السعر:** بعد 3–5 pilots مدفوعة · Proof packs · تسليم أقل من ~5 ساعات/ pilot · طلب استمرار من العميل — لا بالحدس فقط.

---

## 16) Operating System — النظام اليومي

16 loop موثقة في [SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md) — يجب أن تكون **نظام الشركة** لا وثيقة فقط.

**إيقاع يومي (مثال):** صحة النظام → أهداف اليوم → outreach → diagnostics → متابعات → Pilot/مبيعات → Scorecard.

**نهاية اليوم:** leads جديدة · diagnostics مرسلة · pilots معروضة · دفعات/التزامات · Proof · مخاطر محجوبة · أولوية الغد.

ارتباط: [DAILY_OPERATING_LOOP.md](../ops/DAILY_OPERATING_LOOP.md) · [full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md](../ops/full_ops_pack/DAILY_SCORECARD_TEMPLATE_AR.md)

---

## 17) Governance System — الحوكمة

**دستور مقترح**

```text
لا ميزة بدون revenue loop.
لا قناة بدون consent.
لا وعد بدون proof.
لا pilot بدون delivery.
لا delivery بدون proof.
لا lead بدون next_step.
لا أسبوع بدون learning.
```

**أي PR/تغيير تقني:** هل يحسن conversion؟ أو يسرّع delivery؟ أو يقلل risk؟ أو يحسن proof؟ أو يفتح revenue؟ وإلا فـ backlog.

---

## 18) Technical Platform — المنصة التقنية (مراحل)

**الآن (Level 1):** GitHub Pages / frontend · Railway API · DNS · Google Form + Sheet + Apps Script · Moyasar يدوي · wa.me inbound.

**بعد الإثبات:** ربط API بالـ Form · Command Center مربوط بالوحة · Proof generator · WhatsApp Cloud inbound فقط · إيميل بمراجعة.

**بعد ~10 عملاء:** CRM sync · dashboards حسب الأدوار · partner dashboard · billing أتمتة تدريجية · policy أقوى · observability.

لا تقفز المراحل قبل milestones.

ارتباط: [scripts/launch_readiness_check.py](../../scripts/launch_readiness_check.py) · [RAILWAY_DEPLOY_GUIDE_AR.md](../RAILWAY_DEPLOY_GUIDE_AR.md)

---

## 19) Enterprise Readiness — جاهزية المؤسسات (وثيقة فقط)

Checklist مستقبلي: SLA · Access control · Audit logs · Data retention · Consent records · Role-based approvals · تقارير قابلة للتصدير · مراجعة أمنية · onboarding/offboarding.

**لا تُبنى كلها الآن** — تُوثَّق كطبقة Enterprise.

---

## 20) Moat Building — الخندق

أسبوعياً تضيف أصلاً صعب النسخ: مكتبة اعتراضات سعودية · مكتبة رسائل · playbooks قطاعية · شبكة شركاء · Proof Packs · benchmarks مصادر وقنوات.

**بعد 90 يوماً (هدف):** أفضل 5 رسائل · 5 قطاعات · 5 اعتراضات · 5 عروض · 5 أنواع شركاء · أول case studies.

---

## 21) خريطة 12 شهراً — Ambition Map

| الفترة | تركيز |
|--------|--------|
| 0–30 يوم | Level 1 ops · 5 diagnostics · 1–2 paid pilots · 1 proof · محادثة وكالة |
| 31–60 | 5 pilots مدفوعة · 2 تحويلات شهرية · partner pilot · تحسين service mapping |
| 61–90 | 10 عملاء مدفوعين · 3 retainers · شريك وكالة · WA Cloud inbound · Command Center استخدام حقيقي |
| 3–6 أشهر | Growth OS منتَج · playbooks عمودية · محرك إحالات شركاء · MRR · case studies |
| 6–12 شهر | Hybrid منصة+خدمة · moat بيانات تنفيذية · حزم عمودية · enterprise readiness · قناة شركاء |

---

## 22) ماذا يعني «الأفضل في كل شيء» عملياً؟

**الأفضل في التكامل:** أسرع time-to-value · أوضح next step · أقوى نبرة سعودية · أقل مخاطرة قناة · أفضل Proof Pack · أفضل agency wedge · أفضل human-in-loop · أفضل مسار من يدوي إلى أتمتة · أفضل learning loop.

**فخ:** أكبر CRM · أضخم database · أكثر automation · أرخص sender · أكثر dashboards.

---

## 23) CEO Operating Dashboard — لوحة أسبوعية

| المحور | السؤال |
|--------|--------|
| Market | أي قطاع رد أكثر؟ |
| Product | أي كرت أفاد أكثر؟ |
| Sales | أين يتعطل التحويل؟ |
| Delivery | كم ساعة يأخذ pilot؟ |
| Finance | هل الهامش مقبول؟ |
| Trust | هل توجد قنوات خطرة؟ |
| Proof | هل لدينا evidence؟ |
| Partner | من يوزعنا؟ |
| Learning | ماذا تعلمنا هذا الأسبوع؟ |
| Focus | ما الشيء الوحيد القادم؟ |

---

## 24) أقوى مسار تنفيذ الآن

```text
1. ثبّت الموقع والـ API.
2. شغّل Full Ops Board.
3. اختر الوكالات كشريحة أولى.
4. أرسل 10 رسائل يدوية.
5. اجلب 2 diagnostics.
6. اعرض Pilot 499.
7. سلّم Proof Pack.
8. استخرج learning.
9. كرر.
```

تفاصيل Level 1: [full_ops_pack/DEALIX_FULL_OPS_SETUP.md](../ops/full_ops_pack/DEALIX_FULL_OPS_SETUP.md) · [EXECUTE_NOW_AR.md](../ops/EXECUTE_NOW_AR.md)

---

## 25) الخلاصة — 9 قوى والقاعدة الذهبية

**Dealix يفوز إذا جمع:**

```text
1. Market clarity
2. Saudi-specific GTM
3. Consent-first channels
4. Revenue cards
5. Productized service
6. Proof Pack
7. Partner wedge
8. Data learning loop
9. Founder discipline
```

**القاعدة الذهبية**

```text
لا تبنِ لتبدو كبيراً.
ابنِ لتثبت قيمة، ثم حوّل القيمة إلى نظام، ثم حوّل النظام إلى منصة.
```

**الهدف النهائي:** Dealix **نظام تشغيل نمو** يعرف السوق ويفهم العميل ويختار القناة ويصيغ الرسالة ويمنع الخطر ويقود المتابعة ويثبت القيمة ويتعلم — **فئة** لا مجرد أداة.

---

## فهرس وثائق الريبو

| الموضوع | الملف |
|---------|--------|
| الرادارات الـ25 + loops | [SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md) |
| ملخص تنفيذي إنجليزي | [DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md](DEALIX_CATEGORY_EXECUTIVE_SUMMARY_EN.md) |
| v3 طبقات المنتج | [DEALIX_V3_AUTONOMOUS_REVENUE_OS.md](../DEALIX_V3_AUTONOMOUS_REVENUE_OS.md) |
| ما بعد الإطلاق | [POST_LAUNCH_BACKLOG.md](../ops/POST_LAUNCH_BACKLOG.md) |
