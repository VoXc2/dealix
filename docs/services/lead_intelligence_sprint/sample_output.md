# تقرير تنفيذي — Lead Intelligence Sprint
## Sample Executive Report — Lead Intelligence Sprint

**العميل (مجهول الهوية) / Customer codename:** BFSI-A1
**القطاع / Vertical:** الخدمات المصرفية والتمويل / Banking, Financial Services & Insurance (Mid-market)
**المنطقة / Region:** الرياض + الشرقية / Riyadh + Eastern Province
**نافذة المشروع / Sprint window:** Day 1 → Day 10 (10 أيام عمل / 10 business days)
**تاريخ التسليم / Delivery date:** Day 10
**المعدّل بواسطة / Prepared by:** Dealix RevOps · `engagement_id: LIS-2026-014`

> **Sample/Synthetic disclaimer:** This is a synthesized executive report illustrating Lead Intelligence Sprint output quality. All names, codenames, and numbers are fictional but internally consistent and reflect realistic Saudi B2B baselines.

---

## 1. الملخص التنفيذي / Executive Summary

**AR:** حوّلنا 5,000 سجلًا من بيانات BFSI-A1 إلى **50 حسابًا مرتّبًا** يمثل قيمة قابلة للاستهداف قدرها **6.4 مليون ريال** خلال الربع الأول. تم تنظيف 84% من السجلات، وإزالة 320 تكرار، وتطبيق توقيع PDPL على كل مسودة. أعلى 10 إجراءات فورية جاهزة للإرسال بعد موافقة مدير المبيعات، وتمت كتابة كل رسالة بنسختين عربية وإنجليزية مع تذييل المادة 13.

**EN:** We transformed 5,000 BFSI-A1 records into **50 ranked Saudi accounts** representing **SAR 6.4M in addressable Q1 pipeline**. 84% of records were validated, 320 duplicates removed, and PDPL-compliant footers applied to every draft. The top 10 immediate actions are queued for sales-manager approval, with bilingual outreach drafts ready to deploy.

**رقم واحد لرئيس المجلس / One number for the board:**
> "From 5,000 messy records to SAR 6.4M ranked pipeline in 10 days — with zero forbidden claims and 100% PDPL coverage."

**الإجراء التالي المقترح / Recommended next step:** اشتراك RevOps الشهري بقيمة **18,000 ريال/شهريًا** للحفاظ على نظافة البيانات + تشغيل دورات outreach شهرية + توسيع قاعدة الحسابات إلى 200 شركة. التفاصيل في القسم 9.

---

## 2. نتائج جودة البيانات / Data Quality Findings

### 2.1 ملخص الجودة / Quality summary

| المقياس / KPI | القيمة / Value | النسبة / % | الطريقة / Method |
|---|---|---|---|
| السجلات المستلمة / Rows received | 5,000 | 100% | intake CSV + CRM export |
| السجلات الصالحة / Valid rows | 4,200 | 84.0% | `data_quality_score.score_batch` |
| التكرارات المُدمَجة / Duplicate groups merged | 320 | 6.4% | dedupe report (CR + phone + domain) |
| سجلات بدون مصدر / Missing source field | 480 | 9.6% | provenance audit (quarantined) |
| كشف PII / PII findings auto-redacted | 27 | 0.5% | `dealix/trust/pii_detector.py` |
| Saudi entity normalization applied | 4,200 | 100% of valid | CR + VAT + AR/EN name normalization |

### 2.2 تفصيل أسباب الإقصاء / Why rows were quarantined

| السبب / Reason | العدد / Count | التوصية / Recommendation |
|---|---|---|
| مصدر غير موثّق / Source field missing | 480 | إعادة التحقق مع فريق المبيعات / re-verify with sales |
| سجل تجاري غير صالح / Invalid CR number | 165 | استعلام عبر منصة المركز السعودي للأعمال |
| دومين شخصي (gmail/hotmail) / Personal email domain | 122 | تحديد جهة الاتصال داخل الشركة |
| تكرار كامل / Exact duplicates | 320 | تم الدمج تلقائيًا |
| لا يوجد رقم اتصال / No phone | 38 | إثراء يدوي (out of sprint scope) |

**ملاحظة:** 480 سجلًا بلا مصدر تم وضعها في الحجر (quarantine) ولم تُستخدم في التصنيف، احترامًا لقاعدة "no source = no use" المنصوص عليها في `compliance_perimeter.md`.

### 2.3 درجة الجودة قبل/بعد / Data Quality Score

| المقياس | قبل / Before | بعد / After | الفرق / Δ |
|---|---|---|---|
| Quality Score (0–100) | 52 | 91 | **+39** |
| Source coverage % | 60% | 96% | +36% |
| Duplicate rate % | 12% | 0% | -12% |

---

## 3. التصنيف حسب القطاع والمنطقة والشريحة / Opportunity Segmentation

### 3.1 توزيع الحسابات النشطة (4,200 سجلًا) / Active account distribution

| القطاع الفرعي / Sub-vertical | الرياض | الشرقية | جدة | المجموع | % |
|---|---|---|---|---|---|
| البنوك التجارية / Retail Banks | 28 | 19 | 12 | 59 | 1.4% |
| التأمين العام / General Insurance | 41 | 22 | 14 | 77 | 1.8% |
| الوساطة المالية / Financial Brokerage | 18 | 7 | 6 | 31 | 0.7% |
| التمويل المؤسسي / Corporate Lending Clients | 612 | 384 | 201 | 1,197 | 28.5% |
| الشركات الصغيرة والمتوسطة (SME) | 1,180 | 740 | 612 | 2,532 | 60.3% |
| أخرى / Other | 184 | 78 | 42 | 304 | 7.2% |
| **المجموع / Total** | **2,063** | **1,250** | **887** | **4,200** | **100%** |

### 3.2 توزيع التصنيف A/B/C/D / Score banding

| الشريحة / Band | العدد / Count | المتوسط / Median score | الإجراء / Action |
|---|---|---|---|
| **A** (priority outreach) | 187 | 84 | تواصل خلال 7 أيام |
| **B** (nurture cadence) | 612 | 71 | تواصل خلال 30 يومًا |
| **C** (qualify first) | 1,902 | 54 | تحقق إضافي قبل الإرسال |
| **D** (hold / re-verify) | 1,499 | 33 | إعادة تحقق من المصدر |
| **المجموع / Total** | **4,200** | — | — |

> **ملاحظة:** أعلى 50 حسابًا تم اختيارها حصرًا من الشريحة A بالتقاطع مع ICP المعتمد (BFSI mid-market, 50–500 موظف، نشاط رقمي مرئي خلال 60 يومًا).

---

## 4. أفضل 50 حسابًا مرتّبًا / Top 50 Ranked Accounts

**عرض أول 10 حسابات (الـ 40 المتبقية في الملف المرفق `top50_accounts_BFSI-A1.csv`):**

| # | اسم الشركة (مستعار) / Codename | القطاع | المنطقة | الموظفون | درجة ICP | الشريحة | لماذا الآن؟ / Why now |
|---|---|---|---|---|---|---|---|
| 1 | شركة الميسرة المالية / Maysarah Finance Co. | Corporate Lending | الرياض | 240 | 92 | A | إعلان توسّع شرق + مدير مبيعات جديد (LinkedIn, 18 يومًا) |
| 2 | تأمين السلامة العالمية / Salamah Global Insurance | General Insurance | الرياض | 180 | 90 | A | تحديث منصة المطالبات + RFP منشور للأتمتة |
| 3 | شركة الأمان للتمويل / Aman Financing PJSC | Corporate Lending | الشرقية | 320 | 89 | A | فتح فرع ينبع — حاجة لتوسيع CRM (إشارة عامة) |
| 4 | بنك الإقليم للأعمال / Iqleem Business Bank | Retail Banking | الرياض | 410 | 88 | A | تعيين CDO جديد (تاريخ التعيين قبل 31 يومًا) |
| 5 | الوساطة الذكية المالية / SmartBroker Capital | Financial Brokerage | الرياض | 95 | 87 | A | جولة تمويل أُعلنت 9 أيام مضت |
| 6 | تأمين الخليج الموحّد / Khaleej Unified Insurance | General Insurance | الشرقية | 220 | 86 | A | تجديد عقد CRM ينتهي خلال 60 يومًا |
| 7 | شركة النخلة للتمويل الإسلامي / Nakhlah Islamic Finance | Corporate Lending | جدة | 165 | 85 | A | إطلاق منتج SME جديد — حاجة لـ lead routing |
| 8 | مدفوعات سعد / Saad Payments Tech | Fintech | الرياض | 130 | 84 | A | شراكة مع مزود BNPL — إعلان رسمي 22 يومًا |
| 9 | شركة الواحة للتمويل العقاري / Wahah Real Estate Finance | Corporate Lending | الرياض | 280 | 83 | A | تعيين رئيس مبيعات تجزئة جديد |
| 10 | بنك الأهلية للاستثمار / Ahleyah Investment Bank | Investment Banking | الرياض | 510 | 82 | A | إعادة هيكلة قطاع المتوسطين (إعلان داخلي مُسرّب عبر job posting) |

**الـ 40 حسابًا المتبقية:** انظر `top50_accounts_BFSI-A1.csv` (مرفق مع التسليم). الأعمدة: codename, vertical, region, employees, ICP_score, band, owner_recommended, next_action, evidence_url, evidence_date.

**القيمة الإجمالية المرتبطة / Total addressable pipeline value (Q1):** SAR 6,400,000 (متوسط حجم صفقة 128,000 ريال × 50 حساب).

**القيمة المتوقعة عند معدل التأهيل القطاعي 22% / Expected value at sector qualification 22%:** SAR 1,408,000

---

## 5. أفضل 10 إجراءات فورية / Top 10 Immediate Actions

| # | الإجراء / Action | الحساب المستهدف | المالك المقترح | الموعد | الأثر المتوقع (SAR) |
|---|---|---|---|---|---|
| 1 | إرسال مسودة A1 إلى Maysarah Finance | #1 | مدير مبيعات BFSI | يوم 1–3 | 180,000 |
| 2 | طلب اجتماع مع Salamah Global Insurance | #2 | مدير حسابات رئيسي | يوم 1–4 | 240,000 |
| 3 | اقتراح تحليل مجاني لـ Iqleem Business Bank | #4 | الشريك الإداري | يوم 2–6 | 320,000 |
| 4 | إرسال مسودة A2 إلى Nakhlah Islamic Finance | #7 | مدير مبيعات BFSI | يوم 2–5 | 145,000 |
| 5 | تنسيق عرض demo لـ SmartBroker Capital | #5 | مهندس حلول | يوم 3–7 | 95,000 |
| 6 | دعوة Aman Financing لجلسة استكشاف | #3 | مدير حسابات | يوم 3–8 | 200,000 |
| 7 | إرسال study case إلى Wahah Real Estate Finance | #9 | مدير تسويق | يوم 4–9 | 175,000 |
| 8 | عرض RFP-ready proposal لـ Khaleej Unified Insurance | #6 | الشريك الإداري | يوم 5–10 | 220,000 |
| 9 | جلسة LinkedIn discovery مع CDO الجديد في Iqleem | #4 | الشريك الإداري | يوم 5–11 | 90,000 |
| 10 | متابعة Saad Payments Tech بعد BNPL announcement | #8 | مدير حسابات BFSI | يوم 6–10 | 110,000 |
| **المجموع المتوقع / Expected total** | | | | | **1,775,000** |

---

## 6. حزمة المراسلات الجاهزة / Outreach Draft Pack

كل مسودة مرّت بـ `forbidden_claims.py` ✓ و`pii_detector.py` ✓ وتذييل المادة 13 موجود.

### Draft 1 — Maysarah Finance Co. (Account #1, Email)

**Subject (AR):** فكرة سريعة لفريقكم الجديد في الرياض
**Subject (EN):** A quick idea for your new Riyadh sales team

**Body (AR):**
> الأستاذ {{first_name}}،
>
> لاحظنا إعلان شركة الميسرة المالية حول التوسع شرقًا قبل ثلاثة أسابيع، ووجود فريق مبيعات جديد. عادةً ما يكون التحدي الأول في هذه المرحلة ليس Leads، بل **ترتيب الـ Leads** الموجودة فعلًا في CRM، حسب احتمال الإغلاق.
>
> ساعدنا بنوكًا متوسطة في الرياض على تحويل بيانات مبعثرة إلى 50 حسابًا مرتّبًا في 10 أيام. هل تتيح لنا 25 دقيقة الأسبوع القادم لنشرح كيف يمكن أن ينطبق على Maysarah؟
>
> شكرًا،
> {{sender_name}} · Dealix
>
> *إذا لا ترغب في التواصل، رد بكلمة "إلغاء" أو راسلنا على dpo@dealix.me. تتم المعالجة وفقًا لنظام حماية البيانات الشخصية في المملكة العربية السعودية (المادة 13).*

**Body (EN):** (parallel — same structure, same PDPL footer)

---

### Draft 2 — Salamah Global Insurance (Account #2, Email + WhatsApp)

**Subject (AR):** عن RFP الأتمتة المنشور — اقتراح فكرة

**Body (AR — مختصر):**
> الأستاذة {{first_name}}،
>
> لفت انتباهنا الـ RFP المتعلق بأتمتة منصة المطالبات. لا نقدم منصة مطالبات، لكن قبل أن نُهدر وقت فريقك في موردين كثيرين، نقترح جلسة 30 دقيقة لنتأكد أن المتطلبات نظيفة قبل تقييم العروض. هذا غالبًا يُقصّر دورة الاختيار من 5 أشهر إلى شهرين.
>
> هل يناسبك {{day_1}} أو {{day_2}}؟
>
> *تذييل PDPL المعتمد*

### Draft 3 — Iqleem Business Bank (Account #4, LinkedIn DM لـ CDO الجديد)

**AR (≤ 280 char):**
> الأستاذ {{first_name}}، تهانينا على دور CDO في بنك الإقليم. أرى أنك جئت بخبرة تحويل رقمي في القطاع. عندنا تجربة محددة في مشاريع البنوك المتوسطة — هل لديك 20 دقيقة الأسبوع القادم لنتعرف أكثر؟

**EN (parallel):** Welcome to Iqleem, {{first_name}}. Brief intro: we helped 3 Saudi mid-market BFSI players turn raw CRM data into ranked pipeline. Curious whether the timing makes sense to share notes? 20 min next week?

---

## 7. المخاطر / Risks & Compliance Notes

| المخاطرة / Risk | الشدة | الحالة | التخفيف / Mitigation |
|---|---|---|---|
| 480 سجلًا بلا مصدر موثّق | متوسطة | محجوزة | إعادة تحقق مع فريق العميل خلال 14 يومًا |
| 12 سجلًا فيها PII حساس (هوية وطنية) | عالية | تم إزالتها قبل المعالجة | logged في `event_store` ✓ |
| تذييل المادة 13 على كل مسودة | منخفضة | تم تطبيقه على 100% من المسودات | مراجعة DPO قبل الإرسال |
| ادعاءات غير قابلة للتحقق في 7 مسودات أولية | منخفضة | تم رفضها وإعادة كتابتها | `forbidden_claims.py` |
| ركود قاعدة البيانات (data drift) | متوسطة | متوقع خلال 90 يومًا | تجديد ربع سنوي مع RevOps Retainer |

**ملاحظة PDPL Art. 27:** لا توجد بيانات حساسة (صحية، دينية، إلخ) ضمن الجمهور المستهدف. النطاق ضمن المادة 13 (إعلام صريح) والمادة 14 (الموافقة الضمنية في B2B).

---

## 8. خريطة التفعيل لمدة 30 يومًا / 30-Day Activation Plan

| الأسبوع | المهمة | المالك | المخرَج |
|---|---|---|---|
| **W1** | تنفيذ Top 10 actions + إرسال أول 30 مسودة | مدير مبيعات BFSI | 30 رسالة مُرسَلة + ردود مسجّلة |
| **W2** | اجتماعات اكتشاف لـ 7–10 حسابات A | الشريك الإداري + SE | محاضر + مقترحات أولية |
| **W3** | تعميق ICP بناء على الردود الفعلية | RevOps (Dealix) | ICP v2 + إعادة تصنيف Top 50 |
| **W4** | dashboards أسبوعية في Mini CRM + تقرير | Sales Ops | KPI scorecard |

---

## 9. الإجراء التالي المقترح / Next Step Proposal

### **العرض: اشتراك RevOps الشهري / Monthly RevOps Retainer**

| البند | التفاصيل |
|---|---|
| **السعر / Price** | **SAR 18,000 / شهريًا** (ضريبة قيمة مضافة 15% خارج السعر) |
| **المدة / Term** | 3 أشهر (auto-renew) |
| **التسليمات الشهرية** | تحديث 2,000 سجل + إعادة تصنيف Top 100 + 20 مسودة بيلينغوال + تقرير شهري |
| **اجتماعات** | لقاء أسبوعي 45 دقيقة + ورشة شهرية مع QBR |
| **SLA** | استجابة 4 ساعات عمل، تسليم خلال 3 أيام عمل |

### قيمة الأنابيب المتوقعة / Projected pipeline value

| الفترة | حسابات A جديدة | قيمة قابلة للاستهداف | قيمة متوقعة @ 22% |
|---|---|---|---|
| الربع الأول | 50 (الحالي) | SAR 6.4M | SAR 1.41M |
| الربع الثاني | 70 | SAR 8.9M | SAR 1.96M |
| الربع الثالث | 90 | SAR 11.5M | SAR 2.53M |
| **المجموع 9 أشهر** | **210** | **SAR 26.8M** | **SAR 5.9M** |

**ROI خام:** SAR 5.9M متوقعة / SAR 162,000 رسوم 9 أشهر = **36× return** (قبل ضريبة القيمة المضافة وتكاليف فريق العميل الداخلي).

**عرض بديل / Alternative offer:** Lead Intelligence Sprint v2 (top-100 expansion, SAR 14,000 one-shot).

> **للقبول، رد على هذا التقرير برسالة واحدة: "نعم، RevOps Retainer" أو "نعم، Sprint v2"، وسنرسل SOW جاهز للتوقيع خلال 24 ساعة.**

---

## 10. ملخص حزمة الإثبات / Proof Pack Summary

| المقياس / KPI | قبل / Before | بعد / After | الفرق / Δ |
|---|---|---|---|
| Data Quality Score | 52 | 91 | +39 |
| Hours to first prioritized list | 38h | 0h (delivered) | -38h |
| Active accounts in CRM (deduped) | 5,000 | 4,200 | -800 (cleanup) |
| Ranked accounts available | 0 | 50 | +50 |
| Bilingual drafts approved | 0 | 10 | +10 |
| Pipeline value created (addressable, SAR) | 0 | 6,400,000 | +6.4M |
| PDPL Art. 13 coverage | 0% | 100% | +100% |
| Forbidden-claim violations in drafts | n/a | 0 | — |

**الإثبات الكامل:** `docs/services/lead_intelligence_sprint/proof_pack_template.md` يوضح هيكل تقرير الإثبات Stage-7. تم تجميع جميع الأدلة في `engagement_id: LIS-2026-014`.

**شهادة العميل (مسودة، بانتظار التوقيع):**
> "في 10 أيام، خرجنا من فوضى Excel إلى قائمة 50 حسابًا مرتّبة وقابلة للتنفيذ. الرسائل العربية كانت بمستوى يفوق ما كنا نكتبه داخليًا." — VP Sales, BFSI-A1 *(لتوثيقها بعد إذن خطّي عبر `customer_consent.md`)*

---

**مرفقات / Attachments delivered with this report:**
- `top50_accounts_BFSI-A1.csv`
- `outreach_drafts_BFSI-A1_v1.docx` (10 مسودات بيلينغوال)
- `data_quality_appendix_BFSI-A1.pdf`
- `proof_pack_BFSI-A1_v1.pdf`
- `mini_crm_export_BFSI-A1.json`

**تواصل / Contact:** sales@dealix.me · `engagement_id: LIS-2026-014`

*هذا تقرير اصطناعي (Sample) من Dealix RevOps. يوضّح جودة الإخراج، لا يمثّل عميلًا حقيقيًا.*
