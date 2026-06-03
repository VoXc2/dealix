# Dealix Maximum Revenue Factory — الدستور التشغيلي

> **الحالة:** نسخة 1.0 — *آخر تحديث: 2026-06-03*
> **الملكية:** المؤسس (Founder) + المشغّل (Operator)
> **الطبيعة:** هذا الملف هو "الدستور التشغيلي" لـ Dealix. كل ملف آخر في
> `docs/operating_factory/` و`reports/operating_factory/` يخدم هذا الملف ويُفصّله.

---

## 0. لماذا هذا الملف؟

Dealix لم يعد "موقعًا + إيميلات" ولا حتى "400 Account Pack". أصبح **حلقة تشغيل
كاملة (Operating Loop)** تعمل يوميًا وتتعلّم أسبوعيًا وتقرّر شهريًا.

الفرق الجوهري:

```txt
قبل:  Generate 400 Account Packs        (توليد مخرجات)
بعد:  Discover → Score → Draft → Approve → Send/Call → Follow up
      → Mini Proposal → Close → Deliver → Report → Learn   (حلقة كاملة)
```

هذا الملف يجيب على عشرة أسئلة تشغيلية:

1. ما هي المنظومة؟
2. ما الأنظمة الخمسة؟
3. ما مخرجات كل يوم؟
4. ما مخرجات كل شركة؟
5. من يوافق على ماذا؟
6. متى نرسل؟
7. متى نتصل؟
8. متى نجهز Proposal؟
9. متى نبدأ التسليم؟
10. كيف نقيس؟

---

## 1. ما هي المنظومة؟

Dealix Maximum Revenue Factory = منظومة واحدة من عشر طبقات متصلة:

```txt
موقع احترافي
+ 5 أنظمة للبيع
+ 400 Account Packs يوميًا (هدف قابل للتوسع)
+ قنوات تواصل عامة ومشروعة
+ إيميلات مخصصة
+ Call Briefs
+ Mini Proposals
+ Delivery Automation
+ Finance Scoring
+ Founder Daily Command
+ Security / Privacy Gates
```

كل طبقة تُغذّي الطبقة التالية بمخرج محدد، وكل انتقال بين طبقتين يمرّ على
**بوابة جودة (Quality Gate)**. لا يوجد مخرج "يقفز" طبقة.

---

## 2. الأنظمة الخمسة (Customer-Facing Catalog)

| النظام | الوعد للعميل | الألم الذي يحلّه | الربط بالأصول الحالية |
|--------|--------------|------------------|------------------------|
| **Revenue OS** | كشف أين تضيع الإيرادات وبناء نظام بيع | فرص تضيع قبل أن تُغلق | P1 — Revenue Intelligence Sprint |
| **Follow-up Recovery OS** | استرجاع الفرص التي لم تُتابَع | آخر متابعة لم تحدث | جزء المتابعات في P1 + `company_os/revenue/followups.json` |
| **Executive Command OS** | تقرير قيادي يومي يعطي قرارًا لا بيانات | الإدارة لا ترى الصورة | War Room + CEO Brief الحاليان |
| **WhatsApp Client OS** | تحويل واتساب من Inbox إلى Workflow | الاستفسارات تضيع في واتساب | امتداد جديد منضبط (راجع سياسة الأمان) |
| **Proposal & Proof OS** | عرض مقنع بإثبات لا بكلام | العرض لا يُغلق | Proof Pack + `company_os/revenue/proposals.json` |

> **مبدأ مهم:** هذه الأسماء الخمسة **للعميل**. الأسماء الداخلية (Account Pack،
> Cash Priority Score، Quality Gate، C0–C4 …) لا تظهر أبدًا في نسخة موجّهة للعميل.
> راجع `QUALITY_GATES_AR.md` ← بوابة "لا أسماء داخلية في نسخة العميل".

### خريطة الربط مع SKUs الحالية

```txt
Revenue OS              → P1 Sprint (ابتداءً من 2,500 ريال) + P2 Retainer
Follow-up Recovery OS   → Sprint مصغّر للمتابعات (ابتداءً من 2,500 ريال)
Executive Command OS    → War Room ضمن P2 Retainer (ابتداءً من 3,000 ريال/شهر)
Proposal & Proof OS     → Proof Pack + Proposal System
WhatsApp Client OS      → وحدة Workflow ضمن P2 (ليست بوت عام)
```

> **التسعير النهائي قرار المؤسس وليس قرار الوكيل.** الأرقام أعلاه "ابتداءً من"
> مرجعية مأخوذة من `company_os/finance/unit_economics.md` و
> `company_os/revenue/proposals.json`. أي سعر يُرسل للعميل يمرّ على موافقة المؤسس.

---

## 3. الحلقة الكاملة (Dealix Operating Loop)

```txt
Discover
  → Score
    → Draft
      → Approve            ← بوابة المؤسس
        → Send / Call      ← إنسان يرسل/يتصل (لا وكيل)
          → Follow up
            → Mini Proposal ← بوابة موافقة العرض
              → Close       ← قرار المؤسس
                → Deliver   ← بوابة بدء التسليم
                  → Report
                    → Learn → (تعود إلى Discover بمعايير أفضل)
```

- **الحلقة اليومية** تُشغّل من Discover إلى Founder Command — راجع `DAILY_LOOP_AR.md`.
- **الحلقة الأسبوعية** تُشغّل Learn على مستوى الأنظمة/القطاعات/المدن — راجع `WEEKLY_LOOP_AR.md`.
- **المراجعة الشهرية** تقرّر التوسّع أو الإيقاف — راجع `MONTHLY_REVIEW_AR.md`.

---

## 4. مخرجات كل يوم (Daily Output)

الهدف اليومي الحالي: **400 Account Packs عالية الجودة** (وليس 800 ضعيفة).

### توزيع الـ 400 على الأنظمة

| النظام | الحصة اليومية |
|--------|---------------:|
| Revenue OS | 100 |
| Follow-up Recovery OS | 90 |
| Executive Command OS | 70 |
| WhatsApp Client OS | 70 |
| Proposal & Proof OS | 70 |
| **المجموع** | **400** |

### متى نرفع السقف؟

```txt
الشرط: متوسط جودة Account Pack ≥ 80/100 لمدة أسبوعين متتاليين.
المسار: 400 → 600 → 800 → 1000
```

المصنع **مبنيّ من البداية قابلًا للتوسّع**، لكن لا نرفع الكمية قبل إثبات الجودة.

### التقرير اليومي

كل ليلة يُنتَج تقرير واحد:
`reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md`
ويُلخّص في `reports/operating_factory/DAILY_LOOP_STATUS.md`.

---

## 5. مخرجات كل شركة (Account Pack)

كل شركة مكتشفة تحصل على **Account Pack** موحّد:

```txt
company_name
sector
city
size_estimate
public_signal            (إشارة عامة ملحوظة — لا تخمين)
likely_pain
recommended_system       (واحد من الأنظمة الخمسة)
why_this_system
contact_route            (راجع Contact Discovery)
contact_confidence       (C0–C4)
cash_priority_score      (0–100)
email_draft_ref
call_brief_ref
mini_proposal_ready      (نعم/لا)
delivery_ready           (نعم/لا)
source                   (مصدر عام مشروع)
last_checked_at
```

تفاصيل البوابات التي تتحكم في جودة هذه الحقول في `QUALITY_GATES_AR.md`.

---

## 6. من يوافق على ماذا؟ (Approval Matrix)

يمتد هذا الجدول من `company_os/governance/agent_permissions.md` (مصفوفة صلاحيات
الوكلاء)، ويضيف أدوار الحلقة. التفصيل الكامل في `ROLE_OWNERSHIP_AR.md`.

| القرار | يقترحه | يوافق عليه | ينفّذه |
|--------|--------|-----------|--------|
| اكتشاف شركة | وكيل البحث | — (تلقائي) | وكيل البحث |
| ترتيب/Score | وكيل البحث | — | وكيل البحث |
| مسودة إيميل | وكيل الصياغة | **المؤسس** | **إنسان يرسل** |
| اتصال | وكيل البحث (Brief) | **المؤسس** | **إنسان يتصل** |
| Mini Proposal | وكيل العروض | **المؤسس** | **إنسان يرسل** |
| السعر | — | **المؤسس فقط** | المؤسس |
| بدء التسليم | وكيل التسليم | **المؤسس** | المشغّل |
| نشر إثبات | وكيل العروض | **المؤسس** | المشغّل |

**خطوط حمراء (من agent_permissions.md):** الوكيل لا يرسل خارجيًا، لا يسعّر، لا
يحذف بيانات، لا يعمل بشكل مستقل على حسابات العملاء.

---

## 7–9. متى نرسل / نتصل / نجهّز Proposal / نبدأ التسليم؟ (Triggers)

| الحدث | الشرط (Trigger) | البوابة قبله |
|-------|------------------|--------------|
| **نرسل إيميل** | `contact_confidence ≥ C2` **و** Email Score ≥ 80 **و** موافقة المؤسس | 6 Email Gates |
| **نتصل** | رقم عام (C3+) **و** Call Brief مكتمل **و** موافقة المؤسس | Call Brief Gate |
| **نجهّز Mini Proposal** | نتيجة اتصال/رد = `interested` أو `send_more_info` | — (يُنتَج نفس اليوم) |
| **نرسل Mini Proposal** | تمرّ على Proposal Approval Gate + موافقة المؤسس | Proposal Gate |
| **نبدأ التسليم** | الحالة = `won` + اكتمال `required_inputs` | Delivery Start Gate |

> إذا `contact_confidence = C0/C1`: **لا نرسل ولا نتصل**. نعيد البحث أو نستخدم
> نموذج تواصل رسمي فقط. (راجع سياسة عدم الإزعاج والـ Suppression.)

---

## 10. كيف نقيس؟ (Measurement)

- **يوميًا:** `reports/operating_factory/DAILY_LOOP_STATUS.md`
  (عدد Packs، نسبة من لديهم contact route، Top 100، Top 20 sends، Top 30 calls).
- **أسبوعيًا:** `reports/operating_factory/WEEKLY_LOOP_STATUS.md`
  (أفضل نظام/قطاع/مدينة، أفضل زاوية إيميل، تحويل Mini Proposal، عوائق التسليم).
- **الجاهزية للإطلاق:** `reports/operating_factory/READY_TO_LAUNCH_SCORECARD.md`.
- **المالية:** يتصل بـ `company_os/finance/revenue_scorecard.csv` و
  `company_os/war_room/SCORECARD_REPORT.md`.

مؤشرات الحلقة الأساسية (Funnel):

```txt
Discovered → Packs Completed → Has Contact Route → Sent → Replied
→ Interested → Mini Proposal → Won → Delivered → Renewed
```

---

## 11. القواعد الصارمة (Hard Rules)

```txt
1.  400 Account Packs/يوم هدف الجودة (قابل للرفع بعد إثبات الجودة).
2.  الوكلاء لا يرسلون أي رسالة خارجية — الإرسال بيد إنسان بعد موافقة.
3.  لا اتصال آلي (No automated calling).
4.  لا واتساب بارد (No cold WhatsApp).
5.  لا قوائم مشتراة، ولا قواعد بيانات مسرّبة.
6.  لا جهات اتصال مُختلقة — مصادر عامة مشروعة فقط.
7.  لا ادعاءات مضمونة (نضمن/نضاعف/مضمون) في أي نسخة.
8.  لا أسرار في الـ prompts أو الـ logs أو التقارير.
9.  المحتوى الخارجي = بيانات فقط، لا يتحوّل أبدًا إلى تعليمات للنظام.
10. موافقة المؤسس مطلوبة لـ: الإرسال، الـ Mini Proposals، تغيير السعر، بدء التسليم.
```

تُفصَّل هذه القواعد في `docs/security/` و`docs/privacy/` و`QUALITY_GATES_AR.md`.

---

## 12. خريطة الملفات (أين يعيش كل شيء؟)

```txt
docs/operating_factory/
  DEALIX_MAXIMUM_REVENUE_FACTORY_AR.md   ← هذا الملف (الدستور)
  DAILY_LOOP_AR.md                       ← الحلقة اليومية بالساعة
  WEEKLY_LOOP_AR.md                      ← حلقة التعلّم الأسبوعية
  MONTHLY_REVIEW_AR.md                   ← المراجعة الشهرية وقرار التوسّع
  ROLE_OWNERSHIP_AR.md                   ← من يملك ماذا (RACI)
  QUALITY_GATES_AR.md                    ← كل بوابات الجودة (Email/Call/Proposal/Delivery…)
  READY_TO_LAUNCH_CHECKLIST_AR.md        ← قائمة الجاهزية للإطلاق

docs/privacy/      ← تقليل البيانات، عدم الإزعاج/Suppression، بيانات العملاء، الأسرار
docs/security/     ← سياسة المحتوى الخارجي كبيانات غير موثوقة

reports/operating_factory/   ← حالة الحلقة اليومية/الأسبوعية + Scorecard الإطلاق
reports/account_intelligence/NIGHTLY_400_ACCOUNT_PACKS_REPORT.md
reports/gtm/MAXIMUM_REVENUE_FACTORY_OPERATING_LOOP_FINAL_REPORT.md

company_os/        ← طبقة التشغيل الفعلية (revenue/finance/delivery/governance/war_room)
scripts/operating_factory_check.py   ← فحص تلقائي يتحقق من تكامل المنظومة
```

---

## 13. الخلاصة

Dealix الآن **مصنع نمو وتشغيل قابل للتوسّع**، يعطي المؤسس كل يوم إجابة واضحة على:

```txt
من نستهدف؟ كيف نوصل؟ ماذا نرسل؟ من يتصل؟ ماذا يقول؟
ما العرض؟ ما التسليم؟ ما العائق؟ ما القرار؟ ما الذي نتعلّمه؟
```

هذا هو الحدّ الفاصل بين "مشروع AI" و**"مصنع إيرادات"**.

---

*Dealix Maximum Revenue Factory — Operating Constitution | Version 1.0 | 2026-06-03*
