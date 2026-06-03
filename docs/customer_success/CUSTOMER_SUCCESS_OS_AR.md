# نظام نجاح العملاء — Customer Success OS

> **المستوى:** L2 Advise / L3 Draft | **الإيقاع:** أسبوعي | **الموافقة:** مطلوبة لأي مسودة تجديد أو ترقية

---

## 1. المهمة

نظام نجاح العملاء في Dealix يضمن أن كل عميل B2B يصل إلى **قيمة مُسلَّمة وقابلة للقياس** خلال أول 30 يومًا، ويبقى فيها طوال العلاقة. المهمة ليست إدارة الحساب فقط — بل **تحويل التسليم إلى دليل مُعاش يمكن الاستشهاد به**.

**مبدأ رئيسي:** لا تجديد ولا ترقية إلا بعد قيمة مُسلَّمة فعلية. `evidence_level` يجب أن يكون `client_data` أو `measured` أو `verified`. أي درجة أضعف = لا تجديد.

---

## 2. الإشارات الأساسية (Health Signals)

مستمدة من `schemas/client_health.schema.json`:

| الإشارة | النوع | المعنى |
|---|---|---|
| `onboarding_complete` | boolean | اكتمل Intake والـ Access في الأسبوع الأول |
| `access_complete` | boolean | الفريق يملك الصلاحيات اللازمة للتسليم |
| `first_workflow_delivered` | boolean | أُسلِّم أول workflow فعلي للعميل |
| `weekly_report_delivered` | boolean | تقرير القيمة الأسبوعي أُرسل (بموافقة) |
| `client_engagement` | 0–5 | مستوى استجابة وتفاعل العميل |
| `value_proof` | boolean | يكون `true` فقط إذا وجدت قيمة `measured` أو `verified` |
| `unresolved_risks` | integer | عدد المخاطر غير المعالجة في سجل المخاطر |

**قاعدة الإشارة الحمراء:** إذا كانت `value_proof = false` في اليوم 21+ — يُعلَن حالة تدخّل فوري وتُبلَّغ لمدير نجاح العملاء.

---

## 3. نطاقات الصحة والتجديد

| health_score | health_band | renewal_fit | الحالة |
|---|---|---|---|
| 80–100 | green | strong | العميل يحقق قيمة، جاهز للتجديد |
| 60–79 | amber | possible | تقدّم جيد لكن يحتاج متابعة ودليل إضافي |
| 40–59 | amber | not_yet | قيمة جزئية، لا يُقترح تجديد حتى يرتفع الدليل |
| 0–39 | red | at_risk | علاقة في خطر، خطة إنقاذ فورية، لا تجديد |

**مثال حقيقي:** Digital Rise Agency — `CHS-1001` → `health_score: 82`, `health_band: green`, `renewal_fit: strong`, `evidence_level: measured`.

---

## 4. الإيقاع الأسبوعي لنجاح العملاء

| اليوم | الفعالية | المخرَج |
|---|---|---|
| الأحد | مراجعة إشارات الصحة لكل العملاء | قائمة العملاء الأمبر/الأحمر |
| الثلاثاء | تسليم تقرير القيمة الأسبوعي | WVR بعد موافقة المؤسس |
| الخميس | مراجعة المخاطر وتحديث سجل المخاطر | risk_log مُحدَّث |
| الخميس | تقييم شروط التجديد (هل تستوفي القيمة؟) | مسودة REN إذا اكتملت الشروط |

---

## 5. الحدود (What We Don't Do)

- **لا نرسل مسودة تجديد** دون `evidence_level ∈ {client_data, measured, verified}`.
- **لا نقدّم أرقام ROI مضمونة** — نقدّم الأرقام المقاسة فقط.
- **لا نستخدم أساليب ضغط** — خطوة واحدة، بلا إلحاح، بلا ضغط.
- **لا نرسل أي شيء للعميل** دون موافقة المؤسس (L4 أو L5).
- **لا نتجاوز حدود النطاق** المتفق عليه في عقد التسليم — التوسعة تمر بسلّم الترقية.

---

## 6. علاقة نجاح العملاء بباقي المنظومة

```
company_os/delivery/client_success_plan.md   ← قالب خطة النجاح (مصدر الحقيقة لخطط العملاء الفردية)
docs/delivery/WEEKLY_VALUE_REPORT_AR.md      ← تقرير القيمة الأسبوعي (التسليم)
docs/customer_success/FIRST_30_DAYS_AR.md    ← إيقاع أول 30 يوم
docs/customer_success/CLIENT_HEALTH_SCORE_AR.md ← حساب درجة الصحة
docs/customer_success/RENEWAL_PLAYBOOK_AR.md ← متى وكيف نقترح التجديد
docs/customer_success/EXPANSION_PLAYBOOK_AR.md ← التوسعة عبر الإدارات
docs/renewal/RENEWAL_ENGINE_AR.md            ← محرك التجديد التقني
data/customer_success/client_health.jsonl    ← سجل صحة العملاء (CHS-*)
```

**مرجع ثابت:** [خطة نجاح العميل](../../company_os/delivery/client_success_plan.md) — قالب KPIs والتسليمات والمخاطر والتجديد والإحالة. لا يُعاد كتابته هنا.

---

## 7. أدوار ومسؤوليات

| الدور | المسؤولية |
|---|---|
| مدير نجاح العملاء (CSM) | تتبع الإشارات، الإيقاع الأسبوعي، كتابة WVR |
| المؤسس | الموافقة على كل تجديد/ترقية/رسالة خارجية |
| الذكاء الاصطناعي (Agent #2) | دعم L1/L2/L3 — تحليل، توصيات، مسودات فقط |

---

## 8. الفحص والالتزام

سكربت الفحص: `python3 scripts/client_revenue_delivery_check.py`

يتحقق من:
- `evidence_level` لكل مسودة تجديد/ترقية
- `cites_delivered_value` غير فارغ
- كل `product_id` يوجد في `data/catalog/product_catalog.json`
- `approval_required = true` لكل إجراء L4/L5

---

*آخر تحديث: 2026-06-03 | مرجع: [AGENTS.md](../../AGENTS.md) | الطبقة: Customer Success / Renewal — Agent #2*
