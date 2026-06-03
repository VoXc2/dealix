# Client Need Card — دليل التشغيل (AR)

> بطاقة الحاجة هي **طبقة القرار المقطّرة**: تأخذ كل ما في الـ Company Intelligence Pack وتختصره إلى خط واحد واضح يربط الإشارة بالنظام بالزاوية بالـ CTA.
> مرجع الحقول الحرفي: `schemas/client_need_card.schema.json`. مرجع المصطلحات: `AGENTS.md`.

---

## 1. الغرض (Purpose)

البطاقة تجيب على سؤال واحد: **"ما الذي تحتاجه هذه الشركة، وما هي خطوتنا التالية المنطقية؟"**

```txt
signal  →  likely_pain  →  recommended_system  →  email_angle  →  CTA
```

بينما الـ pack يحمل كل التفاصيل (23 حقلًا)، الـ Need Card يحمل **13 حقلًا فقط** — وهي القرار الجوهري. هذا يجعلها سريعة المراجعة من founder ومن Outreach Operator قبل أي إرسال.

البطاقة هي **gate**: لا يصبح أي إيميل send-ready إذا غاب `recommended_system` أو غاب `client_need_card` أو غاب `CTA` (راجع Draft Quality Score في `AGENTS.md`).

---

## 2. الحقول الـ 13 (The 13 Fields)

| # | الحقل | الشرح بسطر واحد |
|---|---|---|
| 1 | `company` | اسم الشركة. |
| 2 | `website` | الموقع الرسمي العام. |
| 3 | `sector` | القطاع. |
| 4 | `signal` | الإشارة العامة الملاحظة. |
| 5 | `likely_pain` | الألم المحتمل (يُصاغ كاحتمال عند L0/L1). |
| 6 | `recommended_system` | أحد الأنظمة الخمسة. |
| 7 | `why_this_system` | لماذا هذا النظام لهذه الشركة. |
| 8 | `first_mission` | أول مهمة عملية صغيرة. |
| 9 | `proof_angle` | زاوية الإثبات / أول مخرج ملموس. |
| 10 | `email_angle` | زاوية الإيميل (عادة angle النظام من `AGENTS.md`). |
| 11 | `CTA` | الدعوة للإجراء الواضحة (سؤال/خطوة واحدة). |
| 12 | `risk_level` | `low` / `medium` / `high`. |
| 13 | `evidence_level` | `L0`–`L4`. |

> الـ `id` نمطه `CNC-###`.

---

## 3. العلاقة بالـ Intelligence Pack

البطاقة **مشتقّة** من الـ pack — ليست بديلًا عنه:

| الطبقة | المحتوى | الجمهور | الحجم |
|---|---|---|---|
| Company Intelligence Pack | كل شيء: بحث + مسودة إيميل + مواد اتصال + زاوية عرض (23 حقلًا) | Operator + Caller | كامل |
| **Client Need Card** | القرار المقطّر: الإشارة → النظام → الزاوية → CTA (13 حقلًا) | Founder للمراجعة السريعة | مختصر |

ستة حقول تنتقل كما هي من الـ pack: `company`, `website`, `sector`, `signal`, `likely_pain`, `recommended_system`, `why_this_system`, `first_mission`, `proof_angle`. والبطاقة تضيف بوضوح حقلين تشغيليين: `email_angle` و`CTA`.

---

## 4. مثال عملي لكل نظام (One Worked Example per System)

> كل البطاقات أدناه تستخدم أسماء شركات **تركيبية**، وتصوغ `likely_pain` كاحتمال لأن المصدر عام.

### 4.1 `revenue_os`

```txt
id:                 CNC-201
company:            Digital Rise Agency
website:            https://example-digitalrise.sa
sector:             Marketing Agency
signal:             حجم leads ظاهر من إعلانات + لا يظهر مسار متابعة موحّد
likely_pain:        غالبًا تصل فرص لكن بلا next action واضح لكل lead
recommended_system: revenue_os
why_this_system:    يضيف طبقة next action + تقرير أسبوعي للفرص فوق ما هو موجود
first_mission:      بناء lead status model + next action لكل فرصة مفتوحة
proof_angle:        تقرير أسبوعي يوضح الفرص بلا خطوة تالية
email_angle:        أين تضيع الفرص؟ من يحتاج متابعة؟ ما الخطوة التالية؟
CTA:                هل يناسب مكالمة 20 دقيقة نوضح فيها أين قد تتعطل الفرص عندكم؟
risk_level:         low
evidence_level:     L1
```

### 4.2 `executive_command_os`

```txt
id:                 CNC-202
company:            TrainMe KSA
website:            https://example-trainme.sa
sector:             Training
signal:             نشاط تشغيلي كثير + تقارير متعددة على الموقع/الحسابات العامة
likely_pain:        قد تكون التقارير كثيرة لكن القرار اليومي للإدارة غير واضح
recommended_system: executive_command_os
why_this_system:    يحوّل التقارير إلى قرار يومي واضح بدل لوحات متفرقة
first_mission:      تعريف أهم تقرير يومي + ربطه بقرار تالٍ صريح
proof_angle:        Daily Command view يوضح القرار اليوم لا الأرقام فقط
email_angle:        التقارير كثيرة، لكن القرار اليومي غير واضح
CTA:                هل يناسب نعرض لكم شكل Daily Command في مكالمة قصيرة؟
risk_level:         low
evidence_level:     L1
```

### 4.3 `followup_recovery_os`

```txt
id:                 CNC-203
company:            شركة تدريب في الرياض
website:            https://example-training.sa
sector:             Training
signal:             برامج متعددة + واتساب ظاهر للتسجيل
likely_pain:        استفسارات التسجيل غالبًا تضيع أو لا تُتابع بنفس الجودة
recommended_system: followup_recovery_os
why_this_system:    أسرع قيمة في ترتيب المتابعة وتجهيز رسائل التسجيل
first_mission:      بناء follow-up queue + رسائل متابعة حسب حالة المسجّل
proof_angle:        Weekly Recovery Report يوضح المتابعات المعاد تفعيلها
email_angle:        آخر متابعة لم تحدث قد تكون أغلى فرصة
CTA:                هل يناسب أرسل لكم نموذجًا مختصرًا من صفحة واحدة؟
risk_level:         low
evidence_level:     L1
```

### 4.4 `whatsapp_client_os`

```txt
id:                 CNC-204
company:            عيادة في جدة
website:            https://example-clinic.sa
sector:             Clinics
signal:             واتساب قناة رئيسية للحجوزات + استفسارات كثيرة ظاهرة
likely_pain:        قد تكون الطلبات داخل واتساب غير مصنّفة وبلا handoff واضح
recommended_system: whatsapp_client_os
why_this_system:    واتساب يحتاج flows + action cards + handoff آمن لإنسان
first_mission:      تصنيف أنواع الطلبات + تعريف متى يتم التصعيد لإنسان
proof_angle:        نموذج flow + action cards لأكثر طلب متكرر
email_angle:        واتساب ليس فقط محادثات؛ يحتاج flows وaction cards وhandoff آمن
CTA:                هل يناسب مكالمة قصيرة نوضح فيها شكل الـ flow المقترح؟
risk_level:         medium
evidence_level:     L2
```

### 4.5 `proposal_proof_os`

```txt
id:                 CNC-205
company:            شركة استشارات في الدمام
website:            https://example-consulting.sa
sector:             Consulting
signal:             خدمات B2B متعددة + صفحة أعمال سابقة بلا proof واضح في العروض
likely_pain:        غالبًا العروض تأخذ وقتًا ولا تحتوي scope وproof كافيين
recommended_system: proposal_proof_os
why_this_system:    العرض المقنع يحتاج Proof وليس كلامًا أكثر
first_mission:      بناء قالب عرض فيه scope + proof + سعر افتتاحي
proof_angle:        نموذج عرض من صفحة واحدة لخدمة واحدة كـ proof
email_angle:        العرض المقنع يحتاج Proof وليس كلامًا أكثر
CTA:                هل يناسب أرسل لكم نموذج عرض من صفحة واحدة؟
risk_level:         low
evidence_level:     L2
```

---

## 5. أين تعيش البيانات والتحقق

- البيانات: `data/acquisition/*.jsonl` (عيّنات تركيبية).
- التحقق: `schemas/client_need_card.schema.json`.
- الفاحص: `scripts/acquisition_delivery_check.py` (`npm run os:check`).

> قاعدة `best_contact_role`: عند اشتقاق Contact Target من البطاقة، يجب أن يكون الدور ضمن أدوار النظام المسموحة — راجع `CONTACT_TARGETING_RULES_AR.md`.

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
