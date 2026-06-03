# Client Need Card System — نظام بطاقة احتياج العميل

> **المبدأ:** لا تُكتب أي رسالة (draft) قبل أن يحصل الـ prospect على **Client Need Card**. البطاقة تُجيب على سؤال "هذا العميل بالضبط وش يحتاج؟" قبل البيع.
>
> **مبني على:** حقول `company_os/revenue/prospects.csv` (company, segment, decision_maker, pain, score) وبنية المسودات في `company_os/revenue/outreach_queue.json`. البطاقة تربط الإشارة بالمهمة المناسبة من `docs/commercial/DEALIX_OPERATING_MISSIONS_AR.md`.

---

## 1. مخطط البطاقة (Need Card Schema)

```txt
Company:              اسم الشركة
Country:              الدولة (Saudi-first)
City:                 المدينة
Sector:               القطاع
Signal:               الإشارة الملحوظة (سبب التواصل)
Likely pain:          الألم المحتمل
Recommended mission:  المهمة المقترحة (M1..M8)
Why this mission:     لماذا هذه المهمة الآن
Proof angle:          زاوية الإثبات (كيف نُثبت القيمة)
Risk:                 المخاطر/الحساسيات
First email angle:    زاوية أول رسالة
CTA:                  الخطوة التالية الصغيرة
```

> **خصوصية:** نخزّن الدور الوظيفي لا اسم الشخص؛ لا PII خام (مطابق لـ `governance/data_handling_checklist.md`).

---

## 2. الـ Need Router (الإشارة → المهمة)

يأخذ الراوتر مدخلات عامة (بيانات عامة فقط — `agent_permissions.md`: Observe/Public data only):

```txt
المدخلات: sector · city · website · job signals · services listed ·
          contact channels · forms · WhatsApp presence · content activity · size hint
المخرجات: most likely pain · best mission · best offer · email angle · risk · first CTA
```

### جدول التوجيه (Signal → Mission)

| الإشارة                          | الاحتياج المرجّح        | المهمة                     |
| -------------------------------- | ----------------------- | -------------------------- |
| واتساب فقط كقناة                 | متابعة غير منظّمة       | M4 WhatsApp Client OS      |
| خدمات/نماذج كثيرة                | عروض غير منظّمة         | M5 Proposal & Proof        |
| يوظّف Sales Ops                  | pipeline يحتاج نظاماً   | M8 Full Revenue OS (Starter) |
| دورات/حملات موسمية كثيرة         | enrollment follow-up    | M2 Follow-up Recovery      |
| وكالة إعلانات                    | تسرّب leads الحملات     | M3 Sales Draft Factory     |
| عملاء متكرّرون                   | retention/renewal       | M6 Customer Success        |
| "founder blind to pipeline"      | غياب رؤية               | M1 Revenue Leakage         |
| دخول قطاع/سوق جديد               | توسّع منظّم             | M7 GTM Expansion           |

> الراوتر **يقترح** فقط (مستوى Advise/Draft). اختيار المهمة وإرسال الرسالة قرار بشري.

---

## 3. مثال مطبّق (من `revenue/prospects.csv`)

```txt
Company:              BrandCraft Agency
Country:              Saudi Arabia
City:                 Riyadh
Sector:               Marketing Agency
Signal:               leads from ads not followed up (score 9)
Likely pain:          إنفاق إعلاني يضيع لأن المتابعة غير مرتبطة بأولوية
Recommended mission:  M2 Follow-up Recovery (ثم M3 Sales Draft Factory)
Why this mission:     كل حملة بلا follow-up منظّم تقلّل قيمة الإنفاق الإعلاني
Proof angle:          before/after لطابور المتابعة + تقرير أسبوعي بالفرص المُستردّة
Risk:                 low — بيانات عامة، لا PII
First email angle:    "مو كل lead يحتاج رسالة؛ يحتاج next step واضح"
CTA:                  أرسل لك تشخيص مختصر يوضّح أول workflow مناسب؟
```

---

## 4. كيف تتغذّى المسودات من البطاقة؟

```txt
Need Card ─▶ يملأ حقول الـ Draft Schema تلقائياً:
   recommended_mission ← Recommended mission
   signal              ← Signal
   pain_hypothesis     ← Likely pain
   draft_subject/body  ← First email angle (+ Proof angle)
   cta                 ← CTA
   risk_level          ← Risk
```

بهذا تكون كل مسودة مبنية على احتياج مُشخّص، لا على قالب عام.

---

## 5. قاعدة "أول إيميل"

لا نبيع كل الخدمات في أول رسالة. نُظهر أننا فهمنا مشكلة محتملة ونقترح **Mission واحدة صغيرة**:

```txt
نقول: "أعتقد أن هذا أول شيء يناسبكم."
لا نقول: "نحن نقدّم كل شيء."
```

(قالب الرسالة الكامل في `docs/outreach/GCC_OUTREACH_POLICY_AR.md`.)

---

## 6. الربط

- بطاقات حقيقية للـ prospects الحاليين: `reports/outreach/CLIENT_NEED_CARDS.md`
- المصنع اليومي: `docs/outreach/DAILY_400_DRAFT_FACTORY_AR.md`
- كتالوج المهام: `docs/commercial/DEALIX_OPERATING_MISSIONS_AR.md`
