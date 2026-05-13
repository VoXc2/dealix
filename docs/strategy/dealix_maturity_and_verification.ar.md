---
title: نموذج نضج Dealix ونظام التحقق
doc_id: W6.T37.maturity-verification.ar
owner: CEO
status: approved
last_reviewed: 2026-05-13
audience: [internal]
language: ar
ar_companion: docs/strategy/dealix_maturity_and_verification.md
related: [W6.T32, W6.T33, W6.T34, W6.T35, W6.T36]
---

# نموذج نضج Dealix ونظام التحقق

## 1. الفكرة

الرؤية لا تكون حقيقية إلا إذا قابلة للتحقق تشغيليًا. هذه الوثيقة تجيب على
سؤال: **"كيف أعرف أن Dealix وصلت؟"** عبر نموذج نضج بخمسة مستويات،
سبعة اختبارات وصول، أربع بوّابات جاهزية، ولوحة تشغيل أسبوعية.

## 2. نموذج النضج (5 مستويات)

| المستوى | الاسم | المطلوب |
|---|---|---|
| **0** | فكرة | رؤية وكتالوج بالكلام — ليست شركة بعد |
| **1** | خدمات مُنتجة | 3 عروض افتتاحية بسعر/قالب/تقرير/Demo |
| **2** | تسليم متكرر | 3–5 عملاء مدفوعون، نفس الخدمة بجودة ثابتة، Quality ≥ 80 |
| **3** | Platform-Assisted | المنصة نفسها تساعد في التسليم (import / scoring / reports / drafts / approvals / audit / proof) |
| **4** | Retainer Machine | MRR ثابت، عملية تجديد، Health Score، Usage Metrics |
| **5** | Enterprise AI OS | Multi-tenant، RBAC، Integrations، SLA، Audit Exports، Enterprise Onboarding |

**قاعدة الترقية:** يُعترف بالمستوى فقط عند توفّر الدليل (لا التطلّع).

## 3. سبعة اختبارات الوصول

1. **السوق**: ≥ 3 عملاء مدفوعون، ≥ 1 Retainer، تحويل Sprint→Retainer ≥ 20%، هامش ≥ 50%، Case Study واحدة على الأقل. **العلامة:** العميل يدفع مرة ثانية بدون ما تشرح كثير.
2. **المنتج**: كل خدمة عندها صفحة + Intake + Scope + Delivery checklist + QA checklist + Report + Demo + Pricing + Upsell + Module داعم.
3. **التكرار**: نفس الخدمة تتسلّم لعميلَين بنفس الجودة في نفس الوقت المعروف.
4. **الأثر**: كل مشروع يثبت ساعات/بيانات/أخطاء/سرعة/Pipeline/فرص/تقارير/معرفة/مخاطر.
5. **الحوكمة**: كل مشروع فيه source attribution + lawful basis + PII redaction + approval + audit + لا أتمتة غير آمنة.
6. **البيانات**: Data Readiness Gate يمنع البدء قبل جاهزية البيانات.
7. **الفريق**: كل عملية = Template + Checklist + Tool + QA + Report + Playbook. لا اعتماد على شخص واحد.

## 4. بوّابات الجاهزية الأربع

### 4.1 Service Readiness Score (0–100)
- يُباع فقط عند ≥ 80.
- المعايير: Offer/Price (10), Intake (10), Scope (10), Module (15), Report (10), QA (15), Demo (10), Compliance (10), Upsell (10).

### 4.2 Delivery Readiness Gate
- المدخلات/المخرجات/خارج النطاق/الجدول الزمني/التقرير/QA/الأثر/العرض التالي = كلها "نعم".

### 4.3 AI Readiness Gate
- البيانات/المصدر/الصحة/PII/الاستخدام المسموح/الموافقة البشرية/المقياس = كلها مغطّاة.
- إذا لا، ابدأ بـ Data Readiness أو Cleanup قبل بناء AI.

### 4.4 Production Readiness Gate
- Tests + Logging + Errors + Audit + No PII leak + Output schema + Fallback + Cost guard + Docs.

## 5. لوحة تشغيل Dealix الأسبوعية

تُراجَع أسبوعيًا في إيقاع التشغيل (W5.T30):

- **الإيراد**: MRR، إيراد جديد، هامش، تحويل Sprint→Retainer، Expansion.
- **التسليم**: التسليم في الوقت، QA Score، Rework Rate، Satisfaction، Proof Packs.
- **المنتج**: خدمات يدعمها المنتج، خطوات يدوية مؤتمتة، قوالب قابلة لإعادة الاستخدام.
- **جودة AI**: Hallucinations، Citation Coverage، Eval Pass Rate، Cost/Project.
- **الحوكمة**: PII Incidents (هدف 0)، Approvals، Audit Coverage، Forbidden Blocks، Source Attribution.

## 6. قاعدة "ابنِ بعد التكرار"

لا تُبنى ميزة إلا بعد تكرار الحاجة ≥ 2 في تسليم حقيقي. هذا يمنع الإفراط في
الهندسة ويضمن أن كل ميزة مدفوع ثمنها في وقت تسليم فعلي قبل تحمل تكلفة بنائها.

## 7. حلقة القرار الأسبوعية للـ CEO

كل يوم اثنين، أجِب 10 أسئلة:
1. أي خدمة جلبت فلوس؟
2. أي عملية تكررت؟
3. أكبر سبب تأخير؟
4. أكثر طلب من العملاء؟
5. أكثر شيء أخذ وقت؟
6. أكبر مخاطرة مفتوحة؟
7. أي ميزة تخفض زمن التسليم؟
8. أي خدمة تستحق Retainer؟
9. أي قطاع كان الأكثر استجابة؟
10. أي دليل قابل للتحويل إلى Case Study؟

ثلاث قرارات فقط: ميزة لتُبنى، عملية لتُقولَب، تجربة لتُجرى.

## 8. الروابط

- النسخة الإنجليزية: `docs/strategy/dealix_maturity_and_verification.md`
- التموضع: `docs/strategy/dealix_operating_partner_positioning.ar.md`
- الخدمات الافتتاحية: `docs/strategy/three_starting_offers.ar.md`
- معيار التسليم + الجودة: `docs/strategy/dealix_delivery_standard_and_quality_system.ar.md`
