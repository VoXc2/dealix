# Dealix Commercial Scale System — من Pilot إلى تصريف مستمر، شركاء، معيار سوقي، ثم منصة

**الموقف الاستراتيجي (لا يغيّر اتجاه المنتج):** Dealix لا يحتاج أن «يثبت أنه AI». يحتاج أن يثبت أنه **يحوّل الفوضى بعد الـ lead إلى قرار موثّق قابل للبيع**.  
**القرار الداخلي:** Sales Kit جاهز لفتح محادثة (تموضع، دليل، ديمو، عرض مدفوع، خطة Ops). **لا نبني أكثر الآن؛ نستخدم ما بُني لإغلاق أول Diagnostic مدفوع.**  
**النمو المعتمد يدوياً (موافقات):** نظام `target → personalize → send (draft/approval) → track → convert` — والوتد الأساسي **الوكالات ومزودو التسويق** لأنهم يشترون، يحيلون، يعيدون البيع، أو يربطون الخدمة بعرضهم.

**روابط داخلية:**

| الموضوع | المرجع |
|--------|--------|
| **تنفيذ يومي (ابدأ هنا)** | [MASTER_COMMERCIAL_OPERATING_PLAN_AR.md](MASTER_COMMERCIAL_OPERATING_PLAN_AR.md) · [operations/](operations/) |
| محرك إغلاق Full Ops، زوايا الشراء | [FULL_OPS_CLOSE_ENGINE_AR.md](FULL_OPS_CLOSE_ENGINE_AR.md) |
| غرفة تصريف يومية | [../ops/DEALIX_REVENUE_WAR_ROOM_AR.md](../ops/DEALIX_REVENUE_WAR_ROOM_AR.md) |
| حزم وأسعار | [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) |
| Sales Kit | [../sales-kit/README.md](../sales-kit/README.md) |
| قالب Proof Pack | [../delivery/PROOF_PACK_TEMPLATE.md](../delivery/PROOF_PACK_TEMPLATE.md) |
| الهوية التشغيلية التاسعة | [DEALIX_AI_OPERATING_COMPANY_AR.md](DEALIX_AI_OPERATING_COMPANY_AR.md) |

---

## 1) Commercial Control Tower — الطبقة الناقصة

**المشكلة:** War Room وحده لا يكفي. تحتاج **Commercial Control Tower** يربط السلسلة كاملةً:

```text
Market → Audience → Channel → Offer → Proof → Sales Room → Invoice → Delivery → Expansion → Partner → Content → Benchmark
```

**أسئلة يومية (قرار، لا «نشاط»):**

- ما أفضل شريحة؟  
- ما أفضل رسالة؟  
- ما أفضل أصل Proof؟  
- ما أعلى اعتراض؟  
- أين توقف العميل؟  
- أي شريك جلب *quality*؟  
- أي قناة فيها *waste*؟  
- ما الذي يجب **ألا** نبنيه؟  

**الهدف التشغيلي:**

- Paid Pilot  
- First Proof Pack  
- Repeatable workflow  
- Partner loop  

**Commercial Evidence Event — يجب أن ينتهي اليوم بواحد أو أكثر (تتبع يدوي/نظام):**

| الحدث | معنى |
|--------|------|
| `message_sent_manual` | مسودة/إرسال بموافقة حسب السياسة |
| `reply_received` | رد مسجّل |
| `demo_booked` | ديمو محجوز |
| `scope_requested` | طلب نطاق/تشخيص |
| `invoice_sent` | فاتورة |
| `payment_received` | دفع |
| `proof_pack_delivered` | Proof Pack مسلّم |
| `partner_intro_created` | مقدّمة شريك/مسار شراكة |
| `referral_requested` | طلب إحالة صريح |

---

## 2) أربعة Motions للبيع — وليس قمعاً واحداً

### Motion A — Agency Wedge (المسار الأساسي)

**المسار:** Agency → 10-Lead Audit → Agency Proof Pack → Co-selling Pilot → Partner Program  

**يناسب:** وكالة تسويق/إعلان/محتوى/عقار، أو شركة تدير حملات لعملاء.  

**الرسالة:** «أنتم تجيبون الاهتمام. Dealix يثبت ماذا حدث **بعد** الاهتمام.»

### Motion B — Direct Company

**المسار:** Company → Free Risk Score → 10-Lead Audit → Diagnostic → Sprint → Retainer  

**يناسب:** عيادات، عقار، تعليم، خدمات B2B، فرق لديها متابعة مبيعات.  

**الرسالة:** «لا تحتاجون أدوات أكثر. تحتاجون معرفة من يحتاج متابعة الآن، وما الرسالة التالية، وأين الدليل.»

### Motion C — Consultant / CRM Partner

**المسار:** Consultant → Diagnostic Layer → Implementation Handoff → Recurring Proof Layer  

**يناسب:** مستشارو CRM، منفّذو Zoho/HubSpot، أتمتة، AI ops.  

**الرسالة:** «Dealix يعطي طبقة diagnostic/proof **قبل** التنفيذ، فتدخل العميل بتنفيذ أوضح وأقوى.»

### Motion D — Executive / Governance

**المسار:** CEO / Board → AI & Revenue Ops Diagnostic → Executive Growth OS → Control Tower Retainer  

**يناسب:** مؤسس، CEO، COO، مدير مبيعات، صانع قرار على مستوى مجلس/حوكمة.  

**الرسالة:** «Dealix يحوّل AI والإيراد من تجارب متفرقة إلى **قرارات أسبوعية موثّقة**.»  

**تعليق:** Motion D ليس «enterprise مبكراً» فقط — إنه زاوية **ثقة، سياسات، مساءلة، control plane** مناسبة لمن يوسّع وكلاء/أتمتة في الإنتاج (موافقات، أدلة، تدقيق).

---

## 3) Offer Matrix حسب ألم العميل (توجيه داخلي)

**لا تُعرض كل الصفوف في شاشة واحدة.** استخدمها كـ **routing matrix** حسب الألم.

| الألم | العرض | السعر (مؤشر) | الهدف |
|--------|--------|---------------|--------|
| Leads تضيع بعد الحملة | 10-Lead Audit | 499 SAR | أول دفع سريع |
| الوكالة تحتاج proof للعميل | Agency Proof Pack | 990 SAR | دخول وكالة |
| CRM مليان لكن غير مفيد | Data to Revenue Snapshot | 1,500 SAR | ترقية للـ Diagnostic |
| CEO يريد تشغيل أسبوعي | Executive Growth OS | 2,999 SAR/شهر | Retainer خفيف |
| شريك يريد تجربة | Partner Sprint | 3,000–7,500 SAR | قناة توزيع |
| Workflow واضح وجاهز للتشخيص | Governed Revenue Diagnostic | 4,999–15,000 SAR | العرض الأساسي |
| بعد proof واضح | Revenue Intelligence Sprint | 25,000 SAR+ | تنفيذ عميق |
| Workflow يتكرر شهرياً | Control Tower Retainer | 4,999–35,000 SAR/شهر | توسع |

**مصدر الأسعار والنطاق التفصيلي:** [DEALIX_REVOPS_PACKAGES_AR.md](DEALIX_REVOPS_PACKAGES_AR.md) و`dealix/config/offers.yaml` حيث ينطبق.

---

## 4) معيار البيع: Dealix SOAEN Standard

**تعريف:** أي workflow في Dealix يمرّ بخمس شروط:

```text
Source → Owner → Approval → Evidence → Next Action
```

**بالعربي:** مصدر، مالك، موافقة، دليل، خطوة تالية.

**قواعد سريعة:**

- Lead بلا **owner** ليس pipeline.  
- Follow-up بلا **evidence** ليس تشغيلاً موثّقاً.  
- إجراء AI بلا **approval** خطر (حسب سياسة المنتج).  
- لوحة بلا **next action** هي تقرير فقط.

هذا يحوّل Dealix من «أداة» إلى **منهج**.

---

## 5) الصفحة الرئيسية تقود القرار (إرشاد محتوى)

**Above the fold**

- العنوان: Dealix يثبت ماذا يحدث بعد الـ lead.  
- الوعد: تحويل المتابعة الفوضوية إلى **قرارات إيراد موثّقة**.  

**CTA (ثلاثة فقط في الأعلى):**

- احصل على Risk Score  
- شاهد Sample Proof Pack  
- احجز ديمو 10 دقائق  

**Section 2 — المشكلة**

- الإعلانات تجيب leads. لكن أين تضيع؟  
- لا owner / لا follow-up موثّق / لا approval / لا proof / لا next action  

**Section 3 — كيف يعمل**

1. نأخذ 10 leads أو workflow واحد.  
2. نصنّف الحالة والمتابعة.  
3. نجهّز الرسائل والقرارات.  
4. نسلّم Proof Pack.  
5. نقرر Sprint أم Retainer.  

**Section 4 — العروض (ثلاثة فقط على السطح)**

- 10-Lead Audit  
- Agency Proof Pack  
- Governed Revenue Diagnostic  

**Section 5 — Trust (تُباع كقيمة)**

- No cold WhatsApp.  
- No scraping.  
- No fake proof.  
- No guaranteed revenue claims.  
- Human approval for external actions.  

---

## 6) Proof Pack Sample — مغناطيس قوي

**ليس PDF عاماً.** أفضل lead magnet: **Sample Proof Pack** يوضح الشكل النهائي.

**محتوى مقترح:**

- Client type: Agency / Clinic / Real Estate  
- Problem: leads disappear after first contact  
- Inputs: 10 sample leads (وهمية/مُنزّهة)  
- Findings: missing owner؛ follow-up بطيء؛ next action غير واضح؛ لا proof للعميل  
- Recommendations: سكربتات متابعة؛ قائمة أولويات؛ حدود موافقة؛ خطوة تالية  

**CTA داخلي:** «هل تريد نسخة على 10 leads عندكم؟»

---

## 7) Discovery Script — قبل الديمو

**القاعدة:** لا تبدأ الديمو قبل discovery.

**الأسئلة السبعة:**

1. من أين تأتي الـ leads حالياً؟  
2. كم lead يدخل تقريباً أسبوعياً؟  
3. من يرد أولاً؟  
4. كيف تعرفون أن lead يحتاج متابعة؟  
5. أين تسجّلون الردود؟  
6. هل تقدرون تثبتون للعميل ماذا حدث بعد الحملة؟  
7. إذا أصلحنا workflow واحداً، أي workflow تختارون؟  

**إن لم يكن للعميل إجابة:** هذه **قيمة Dealix** — قل: «هذا بالضبط ما نكشفه في أول Proof Pack.»

---

## 8) Enterprise — لغة جاهزة، بيع لاحق

**لا تبيع «10 leads» للكبار.** استخدم:

**AI & Revenue Operations Control Tower**

مكوّنات للحديث فقط عند المناسب:

- AI action register  
- Approval matrix  
- Evidence ledger  
- Workflow risk map  
- Monthly executive report  
- Agent governance dashboard  

**جملة مقفّاة:**

> قبل أن توسّعوا AI agents في الإيراد، تحتاجون معرفة: من يملك الـ action؟ ما الـ source؟ ما الـ approval؟ ما الـ evidence؟ وما الـ rollback؟

---

## 9) AEO / Answer Engine Optimization — ظهور داخل إجابات AI والبحث

**أنشئ صفحات إجابة واضحة (تعريف + متى تحتاجه + خطوات + قالب/CTA).**

أمثلة عناوين (مسارات URL مقترحة تحت `/en/learn` أو `/ar/learn` عند التنفيذ):

| الصفحة | غرض الإجابة |
|--------|-------------|
| What is Post-Lead Revenue Ops? | تعريف الفئة |
| What is a Proof Pack? | تسليم الأدلة |
| How to audit lead follow-up? | إجراء عملي |
| AI approval policy for sales teams | حوكمة |
| Saudi agency lead follow-up checklist | وتم قطاعي |
| No cold WhatsApp growth policy | ثقة + تمييز |
| CRM vs Revenue Ops: what is the difference? | مقارنة تعليمية |

**كل صفحة:** تعريف → متى تحتاجه → خطوات → قالب/رابط مجاني → CTA إلى **Risk Score** أو **Sample Proof Pack**.

---

## 10) Objection Engine — من اعتراض إلى أصل

**سير العمل:**

```text
objection_received → classify → response_draft → sales_asset → content_asset → FAQ_update
```

**أمثلة:**

| الاعتراض | أصل مقترح |
|----------|-----------|
| عندنا CRM | مقال/بوست: «CRM يخزّن، لكن من يحرّك follow-up؟» |
| عندنا وكالة | «الوكالة تجيب الاهتمام، Dealix يثبت ما بعد الاهتمام» |
| السعر عالي | one-pager: «لماذا نبدأ بـ10 leads فقط؟» |
| عندنا AI داخلي | دليل: «كيف تحكم AI actions قبل التوسع؟» |

---

## 11) Partner Onboarding Kit — حزمة جاهزة للشراكة

**الهدف:** تمكين شريك (وكالة/مستشار) من **بيع مشترك** بدون إعادة اختراع القصة كل أسبوع.

**محتويات الحزمة (Minimum viable):**

| عنصر | الوصف |
|------|--------|
| **Partner one-pager (AR + EN)** | من نحن في جملة واحدة؛ Motion المناسب؛ SOAEN؛ ما نفعله بعد الـ lead |
| **Co-sell call outline** | Discovery السبعة + جدولة Proof أو Audit |
| **Demo 10 دقائق** | لقطة شاشة/تدفق: من lead إلى evidence إلى next action (بدون مبالغة بالـ AI) |
| **Pricing & routing card** | جدول Offer Matrix (داخلي للشريك) — ماذا يُقترح لأي ألم |
| **Referral & rev-share draft** | مسودة شروط (للمراجعة القانونية) — نسبة/حد أدنى/فترة اعتماد |
| **Delivery boundary** | ما يسلّمه Dealix vs ما يسلّمه الشريك (تنفيذ CRM/حملات) |
| **Proof expectations** | شكل Proof Pack، SLA تشخيصي معقول، ممنوعات (لا أرقام وهمية) |
| **Support path** | قناة تواصل للشريك، وقت الاستجابة المستهدف للأسئلة قبل الصفقة |
| **Objection cheat sheet** | 5 اعتراضات شائعة + ربط بأصول Objection Engine |

**ربط العمليات:** بعد أول صفقة شريك ناجحة — حدث `partner_intro_created` + تحديث Control Tower (جودة الإحالة، معدل الإغلاق، waste بالقناة).

---

## ملحق: ترقيٌ المنتج (لاحقاً)

**منظومة → معيار سوقي → منصة:**  
هذا المستند يثبّت **المنهج والأدلة والشراكة**. عند تكرار الأدلة وتوسيع الـ API/UI، تُترجم Benchmark وContent تلقائياً من نفس سلسلة Evidence Events — دون قلب اتجاه المنتج نحو «ميزات إضافية قبل إغلاق أول Diagnostic مدفوع».
