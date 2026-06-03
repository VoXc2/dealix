# Dealix Revenue War Room — غرفة التصريف والإيراد اليومية

**الغرض:** تحويل التوزيع من «خطة تسويق» إلى **نظام نمو بموافقة بشرية**: target → personalize → send → track → convert، مع حدود امتثال غير قابلة للمساومة.

**مرساة اليوم (3 مراجع):** [FOUNDER_DAILY_ANCHOR_AR.md](FOUNDER_DAILY_ANCHOR_AR.md) — مع [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) و [FOUNDER_OPERATING_SYSTEM_AR.md](FOUNDER_OPERATING_SYSTEM_AR.md).

**عداد 30 يوم:** [`REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml`](REVENUE_WAR_ROOM_30_DAY_TRACKER.yaml) · **تشغيل يومي:** `bash scripts/run_revenue_war_room_daily.sh` (Windows: `scripts/run_revenue_war_room_daily.ps1`) · **واجهة:** `/[locale]/ops/founder`

**محاذاة مع المستودع**

| موضوع | مرجع |
|--------|--------|
| سلم العروض والأسعار المعتمدة للعقد | [docs/commercial/DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [docs/COMMERCIAL_WIRING_MAP.md](../COMMERCIAL_WIRING_MAP.md) |
| قواعد المؤسس (ممنوعات، سلم بيع) | [`.cursor/rules/dealix-founder-sales.mdc`](../../.cursor/rules/dealix-founder-sales.mdc) |
| حركة البيع والـ go-live | [FOUNDER_SELL_MOTION_AR.md](FOUNDER_SELL_MOTION_AR.md) · [FOUNDER_GO_LIVE_DAY0_AR.md](FOUNDER_GO_LIVE_DAY0_AR.md) |
| لوحة «الآن» واستراتيجية تجارية | [docs/business/DEALIX_BUSINESS_NOW_AR.md](../business/DEALIX_BUSINESS_NOW_AR.md) — واجهة `/[locale]/business-now` |
| حلقة يومية خفيفة | [DAILY_COMMERCIAL_LOOP_AR.md](DAILY_COMMERCIAL_LOOP_AR.md) |
| خطة تصريف شاملة + أحداث أدلة | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](../commercial/MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) · [EVIDENCE_EVENTS_CLOSE_PATH_AR.md](../commercial/operations/EVIDENCE_EVENTS_CLOSE_PATH_AR.md) · [evidence_events_tracker.csv](../commercial/operations/evidence_events_tracker.csv) |
| Revenue OS (مصدر، مسودات، anti-waste) | [AGENTS.md](../../AGENTS.md) — مسارات `/api/v1/revenue-os/*` |

**نموذج المنتج:** حقل `war_room_status` على كل lead في [dealix/revenue_ops_autopilot/schemas.py](../../dealix/revenue_ops_autopilot/schemas.py) — جدول التحويل مع `LeadStage`: [WAR_ROOM_STATUS_MAPPING_AR.md](WAR_ROOM_STATUS_MAPPING_AR.md) · API: `GET/PATCH/POST /api/v1/ops-autopilot/war-room` · واجهة: `/[locale]/ops/war-room` (جدول 7 أعمدة) · Cloud: `/[locale]/cloud`

**قواعد سلامة (ملخص)**

- لا واتساب بارد، لا إرسال جماعي غير مرغوب، لا أتمتة LinkedIn خارج السياسة، ولا scraping إنتاجي.
- لا ادعاء «إيراد مفعّل / Revenue Live» قبل **دفع/التزام مثبت**.
- أي رسالة خارجية = **مسودة + موافقة** ما لم تكن رداً على inbound صريح أو علاقة قائمة.

---

## 1. Revenue War Room — الجدول المركزي (7 أعمدة فقط)

| # | عمود | معنى مختصر |
|---|------|------------|
| 1 | **Target** | حساب/جهة اتصال محددة |
| 2 | **Segment** | شريحة ICP (مثلاً وكالة، SaaS، مُنفّذ CRM) |
| 3 | **Pain Hypothesis** | فرضية ألم واحدة قابلة للاختبار |
| 4 | **Offer** | العرض الحالي (Diagnostic / Pilot / Sprint …) |
| 5 | **Proof Asset** | ما أُرسل أو يُجهَّز: Sample Proof، Risk Score، Decision Passport، إلخ |
| 6 | **Next Action** | خطوة واحدة واضحة + تاريخ |
| 7 | **Status** | مرحلة في المسار (القائمة أدناه) |

### حالات Status (مسار واحد)

`not_contacted` → `message_drafted` → `approved_to_send` → `sent_manual` → `replied` → `proof_pack_sent` → `meeting_booked` → `scope_requested` → `invoice_sent` → `paid` → `delivery_started` → `proof_pack_delivered` → `upsell_candidate` → `referral_requested` · أو `closed_lost`

### أسئلة كل صباح

- من **أعلى 10 targets** اليوم؟
- من يحتاج **follow-up**؟ من طلب **proof**؟ من جاهز **لاجتماع**؟
- من يحتاج **scope**؟ **invoice**؟ **delivery**؟ **upsell**؟

---

## 2. Dashboard اليومي (Today / Revenue / Risks)

**Today (مثال حد أدنى تشغيلي)**

- 10 لمسات موافَق عليها (يدوياً)
- 5 متابعات
- 1 منشور مؤسس (LinkedIn)
- 1 محادثة شريك
- 1 تحديث للـ scorecard

**Revenue**

- محادثات · اجتماعات · طلبات نطاق · فواتير · مدفوع

**Risks (مراقبة)**

- لا إرسال «live» خارج السياسة · لا واتساب بارد · لا دليل مزيف · لا ادعاء إيراد قبل الدفع

---

## 3. Channel Playbooks — وظيفة كل قناة

### LinkedIn

- **الوظيفة:** ثقة + محادثات دافئة.
- **تستخدم لـ:** منشورات مؤسس، تعليقات على حسابات مستهدفة، طلبات اتصال، DM يدوي بعد القبول، اكتشاف شراكات.
- **ممنوع:** أتمتة إرسال، scraping، رسائل جماعية، مبالغة في المطالبات.
- **روتين إرشادي:** 5 تعليقات/يوم · 5 طلبات اتصال/يوم · 2 DM يدوي بعد القبول · 1 منشور مؤسس/يوم.

### Email

- **الوظيفة:** تواصل منظم + عروض شراكة.
- **الأفضل:** وكالات، مستشارو CRM، مُشغّلون B2B، مؤسسون ببريد علني.
- **قواعد:** تخصيص، قصر، CTA واحد، بلا إلحاح مزيف، بلا ROI مضمون.

### WhatsApp

- **الوظيفة:** دافئ / opt-in / علاقة قائمة فقط.
- **ممنوع:** إطلاق بارد، رسائل غير مرغوبة، أتمتة صادرة.
- **يُستخدم إذا:** inbound، علاقة قائمة، موافقة صريحة، إحالة دافئة يدوياً.

### Partners

- **الوظيفة:** ثقة مقترضة + توزيع.
- **تستهدف:** وكالات تسويق، منفّذي CRM، استشاريي AI، مستشارو GRC، مجتمعات أعمال، مسرّعات.

### Webinars

- **الوظيفة:** تثقيف السوق وجمع الطلب.
- **بعد توفر:** ICP واضح، رسالة واضحة، عيّنة Proof Pack، تقييم مخاطر، شريك مضيف.

### Paid Ads

- **الوظيفة:** تضخيم رسالة مُثبتة.
- **لا تبدأ قبل:** عدة اجتماعات، اعتراضات متكررة، طلب Proof Pack، ICP واضح.

---

## 4. الوتد الحالي: الوكالات ومزودو التسويق

**لماذا هذه الشريحة أولاً**

1. قد يشترون Dealix (ألم متابعة).
2. قد يحيلون لعملائهم.
3. قد يبيعونه كباقة إضافية.
4. قد يصبحون قناة تنفيذ/شراكة.

**الرسالة الأساسية**

أنتم تجلبون الـ leads لعملائكم — Dealix يثبت **ماذا يحدث بعد الـlead**: من تواصل؟ من رد؟ من يحتاج متابعة؟ ما أفضل **next action**؟ ما **الدليل** الذي تقدمونه للعميل؟

**عرض: Agency Partner Pilot (مخرجات مقترحة)**

- Workflow لعميل واحد · 10 فرص · مسودات متابعة · لوحة حالة leads · Proof Pack · نموذج **co-selling** أو إحالة.

**CTA:** تجربة على **عميل واحد فقط**.

**شراكات (مرن البداية، بسيط الشروط)**  
الأفضل: pilot واحد أو إحالة واحدة قبل توسيع الشروط — أنماط: Referral، Implementation، تبادل خدمة، Co-selling Pilot؛ الـ white-label لاحقاً بعد الإثبات.

---

## 5. Packaging — تسلسل حسب نضج العميل

استخدم **عرضاً واحداً** مناسباً لمرحلة المحادثة؛ الأرقام التعاقدية المعتمدة في الريبو مذكورة في [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md).

| مرحلة تفكير العميل | اتجاه العرض |
|---------------------|-------------|
| **Entry** | Risk Score مجاني · عيّنة Proof Pack · مراجعة تشخيصية ~20 دقيقة — التقاط طلب وتصفية |
| **First payment / تردد** | Pilot منخفض المخاطر (مثل 499 SAR حيث ينطبق السلم) |
| **Starter** | Diagnostic أصغر نطاقاً (نطاق سعري مرن للشركات الصغيرة) |
| **Standard** | Diagnostic أعمق عندما القرار والمزانية جاهزة |
| **Sprint** | بعد Proof Pack عندما الألم والـworkflow والقيمة مؤكدة |
| **Retainer** | تشغيل شهري حكوم، متابعة متكررة، مراجعة مستمرة |

---

## 6. Message Library — مسودات (تُرسل بعد الموافقة)

### وكالة — لمسة أولى

السلام عليكم [Name]، وصلت لكم لأن شغلكم قريب من التسويق وخدمات العملاء.

عندي Dealix: نظام سعودي يساعد الوكالات ترتب متابعة العملاء من واتساب/إيميل/نماذج الموقع، يصنّف الردود، يجهّز رسائل متابعة، ويربطها بحجز ديمو أو عرض سعر بدل ما تضيع الـleads بعد الحملة.

الفكرة لكم مو بس كعميل؛ كشريك: تقدرون تبيعونه كخدمة لعملائكم أو نجرب Pilot على عميل واحد ونثبت النتيجة بـProof Pack.

يناسبكم ديمو 10 دقائق؟

### متابعة 24 ساعة

متابعة سريعة — الفكرة ليست حملة بيع طويلة. إذا عندكم leads تضيع بعد الإعلان أو بعد أول رسالة، أقدر أوريكم خلال 10 دقائق كيف Dealix يحوّلها لمسار متابعة وحجز واضح.

### متابعة 72 ساعة

آخر متابعة مني هنا. إذا التوقيت غير مناسب أوقف الرسائل، وإذا فيه اهتمام أرسل لكم مثال عملي مخصص لنشاطكم قبل أي اجتماع.

### Partner — إرسال

السلام عليكم [Name]،

أبني Dealix كنظام سعودي يساعد الشركات والوكالات على تحويل الـleads والمتابعة ومسارات الـAI إلى تشغيل محكوم: رسائل، متابعة، موافقات، Proof Pack، وقرارات واضحة.

أشوف فيه زاوية شراكة: أنتم تجيبون العلاقة/العميل، وDealix يشغّل التشخيص والـProof Pack، ثم نقرر pilot أو تسليم تنفيذ.

اقتراحي نبدأ بعميل واحد فقط بدون التزام كبير.

يناسبك ديمو 10 دقائق هذا الأسبوع؟

سامي

### بعد الديمو

بناءً على ما شفناه، أفضل خطوة ليست اشتراك كبير الآن. نبدأ بـDiagnostic/Pilot صغير على workflow واحد: 10 فرص أو leads، نرتب المتابعة، نطلع Proof Pack، وبعدها نقرر Sprint أو Retainer.

---

## 7. Sales Room لكل lead (حقول داخلية إلزامية)

لا lead بدون **next action**.

| حقل | |
|-----|--|
| company · contact · source | تعريف وتتبع |
| pain hypothesis · lead score | تركيز وترتيب |
| conversation notes · objections | سياق |
| proof asset sent · evidence events | أثر وإثبات |
| meeting brief | إذا وُجد اجتماع |
| scope status · invoice status | تنفيذ وتسعير |
| next_action · next_action_date · stage · owner | ملكية ووضوح |

---

## 8. Closing System — الإغلاق بالمشكلة لا بالميزات

**اغلق بـ:** مشكلة محددة · workflow واحد · Proof Pack · قرار واحد · **دخول بسعر مخاطرة منخفضة**.

**Close script (هيكل)**

- نأخذ workflow واحداً: leads من حملة؛ واتساب/إيميل؛ متابعة مبيعات؛ أو قائمة عملاء.
- خلال ~7 أيام: أين تضيع الفرص؛ من يحتاج متابعة؛ رسائل مقترحة؛ مخاطر؛ Proof Pack.
- إن ظهرت قيمة → Sprint/Retainer؛ وإلا نتوقف عند التشخيص.

**اعتراض السعر:** نخفض **المخاطرة** لا القيمة — Pilot على عميل/workflow واحد ثم قرار بعد Proof.

**اعتراض «عندنا CRM»:** Dealix لا يستبدل CRM؛ السؤال: هل بيانات CRM تُترجم إلى follow-up وقرار وقيمة؟

**اعتراض «عندنا وكالة»:** الوكالة تجلب الحملات؛ Dealix يثبت ماذا بعد الـlead: متابعة، ردود، next action، Proof للعميل.

---

## 9. Proof-Led Selling

| مرحلة | أدوات |
|--------|--------|
| قبل البيع | Sample Proof Pack · Risk Score · Demo · مثال Decision Passport |
| أثناء | محاكاة workflow · أول 10 في GTM · سكربت مبيعات · demo إثبات |
| بعد | Proof Pack عميل · تأكيد قيمة · مسار upsell · طلب إحالة |

**صياغة:** لا تقل «يزيد الإيراد» كوعد عام — قل «يُثبت أين تضيع الفرص وما القرار التالي».

---

## 10. Affiliate & Partner Ops (حتى لوحة بسيطة)

أعمدة مقترحة: `partner_name` · `type` · `audience` · `fit_score` · `approved` · `referral_code` · `leads_submitted` · `qualified_leads` · `meetings` · `paid_deals` · `commission_due` · `compliance_status` · `next_action`

**أنواع:** Referral · Implementation · Service Exchange · Co-selling Pilot · White-label (لاحقاً).

**عمولات إرشادية (تُثبت عقدياً):** Referral 10–20% أول دفع · Affiliate 5–10% أول diagnostic مدفوع · Strategic 15–20% · Implementation: يحتفظ الشريك بتنفيذ؛ Dealix بطبقة التشخيص/الإثبات.

**شروط:** لا صرف قبل `invoice_paid` · لا ادعاءات مضللة · إفصاح · رسائل معتمدة فقط · لا spam · لا واتساب بارد باسم Dealix.

---

## 11. Customer Conversion Ladder

Cold visitor → Risk Score مجاني → Warm → Sample Proof Pack → مهتم → Diagnostic Review → حساس للسعر → Pilot → جاد → Standard Diagnostic → lead مُتحقَّق من القيمة → Sprint → workflow مستمر → Retainer · وكالة → Partner Pilot → وكالة قوية → Co-selling.

---

## 12. Daily Execution Engine

**صباحاً:** Founder Command Center → اختيار 10 targets → مراجعة 5 متابعات → موافقة مسودات → تجهيز proof للـleads الدافئة → فواتير → تصعيد دعم.

**نهاراً:** إرسال يدوي · ردود دافئة · ديمو · مكالمات شراكة · دفع النطاق.

**مساءً:** scorecard · ما نجح/فشل · 3 خطوات غداً · قرار no-build صريح.

---

## 13. Weekly Distribution Review

1. أفضل شريحة · 2. أفضل رسالة · 3. أفضل قناة · 4. أعلى اعتراض · 5. أفضل مصدر شريك · 6. أفضل تحويل lead magnet · 7. انسداد الـfunnel · 8. ملاءمة السعر · 9. قوة الـproof · 10. ما نوقف · 11. ما نضاعف.

**قرار أسبوعي محتمل:** توسيع قناة · إصلاح رسالة · تعديل ICP · تحسين Proof Pack · إيقاف affiliate ضعيف · webinar · no-build.

---

## 14. Metrics

**Acquisition:** target accounts · لمسات يدوية · معدل رد · طلبات proof · إكمال Risk Score.

**Conversion:** leads مؤهلة · اجتماعات · طلبات نطاق · فواتير · مدفوع.

**Distribution:** leads شركاء · لقاءات شركاء · إيراد من شركاء · عمولات مستحقة.

**Trust:** امتثال موافقات · إجراءات عالية الخطورة المحظورة · اكتمال أدلة.

**Delivery:** Proof Pack مسلّم · زمن دورة · تأكيد قيمة · مرشحو upsell.

---

## 15. أتمتة كاملة قدر الإمكان — وحدود الموافقة

**يُؤتمت بأمان:** استقبال lead · scoring · توجيه · تسليم عيّنة proof بعد موافقة · مسودة briefing اجتماع · مسودة نطاق/فاتورة · تذكير متابعات · تصنيف دعم · بحث KB · إجابات دعم منخفضة المخاطر · تسجيل أدلة · تحديث scorecard · مسودة عمولة · مسودة تقرير أسبوعي.

**يحتاج موافقة:** رسالة خارجية · إرسال فاتورة/نطاق · خصم · استرداد · دراسة حالة · ادعاء أمني · صرف عمولة · تشخيص نهائي للعميل.

**ممنوع الآن:** أتمتة LinkedIn للإرسال · scraping · واتساب بارد · شحن دفع live بدون مسار موافق · proof مزيف · ROI مضمون · امتثال مضمون كَلِفّة.

---

## 16. أقوى 14 يوماً لتصريف المنتج (هيكل)

**اليوم 1:** War Room جاهز · 20 وكالة قائمة · 3 رسائل · 10 لمسات يدوية · منشور مؤسس.

**اليوم 2:** 5 متابعات · 10 لمسات جديدة · Sample Proof Pack · أول ديمو مُجدول.

**اليوم 3:** شراكات · Pilot جاهز للعرض · مراجعة اعتراضات · snippet إثبات.

**اليوم 4:** أول ديمو · إغلاق باتجاه Pilot/Diagnostic · مسودة نطاق.

**اليوم 5:** متابعة ديمو · رابط دفع/فاتورة · تهيئة onboarding.

**اليوم 6:** عند الدفع — بدء تسليم؛ وإلا متابعة بدليل إثبات إضافي.

**اليوم 7:** مراجعة أسبوعية — أفضل segment، مضاعفة الرسالة الرابحة، إيقاف الضعيف.

**الأسبوع الثاني:** توسيع قائمة الأهداف؛ هدف تشغيلي: محادثات واجتماعات ونطاقات ودفع واقعي — **القياس على ردود واجتماعات ونطاق ومدفوع، لا على عدد الرسائل فقط**.

---

## 17. خط الدفاع ضد الفشل

- إن كانت المشكلة في **المبيعات** لا تُضف features.
- إن كانت في **الإثبات** حسّن Proof Pack.
- إن كانت في **ICP** غيّر الشريحة.
- إن كانت في **السعر** قلّل المخاطرة بحزمة أصغر.

**Affiliate:** لا برنامج مفتوح — ابدأ بشركاء محدودين، رسائل معتمدة، مراجعة يدوية.

---

*آخر تحديث وصفي: 2026-05-17 — وثيقة تشغيلية للمؤسس؛ يراجع سلم الأسعار عند كل تغيير عقدي.*
