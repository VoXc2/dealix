# اقتصاديات الوحدة والهامش — Unit Economics & Margin

> القاعدة: لا تجعل Dealix يبيع شيئاً يخسر وقتك.
> هذه الوثيقة تكمّل النموذج المالي القائم في `company_os/finance/unit_economics.md`،
> والمراجعة العملية في [UNIT_ECONOMICS_REVIEW](../../reports/success/UNIT_ECONOMICS_REVIEW.md).

---

## 1. ما يجب حسابه لكل Sprint

```txt
starter_price
estimated_hours
gross_margin
founder_involvement
delivery_complexity
revision_risk
upsell_potential
```

أي Sprint لا نملك له هذه الأرقام = **لا نعرف إن كان يربح وقتنا**.

---

## 2. نموذج اقتصاديات الـ Sprint

| الحقل | الوصف | قاعدة |
|-------|-------|-------|
| starter_price | السعر الافتتاحي | يمرّ عبر موافقة المؤسس |
| estimated_hours | ساعات التسليم المقدّرة | تشمل التحضير والمراجعة |
| gross_margin | (السعر − تكلفة الوقت) ÷ السعر | يجب ألا يقل عن 60% |
| founder_involvement | نسبة وقت المؤسس | كلما قلّ، تحسّنت قابلية التوسّع |
| delivery_complexity | بسيط / متوسط / مرتفع | المرتفع يُؤجَّل حتى تثبيت Pack |
| revision_risk | احتمال جولات مراجعة إضافية | scope مغلق يخفّضه |
| upsell_potential | احتمال التوسّع لـ Retainer | يرفع LTV |

```txt
Gross Margin = (starter_price − (estimated_hours × hourly_rate)) ÷ starter_price
```

---

## 3. القاعدة الذهبية للبداية

ابدأ بما يحقّق الخمسة معاً:

```txt
ألم واضح
بيع سريع
تسليم سريع
هامش جيد
توسّع لاحق
```

أفضل البداية غالباً (من زاوية الاقتصاد + سهولة التسليم):

```txt
1. Proposal & Proof OS
2. Follow-up Recovery OS
3. Executive Command OS
4. Lead Qualification OS
5. Client Onboarding OS
```

---

## 4. قواعد الهامش الصارمة

مستمدة ومتّسقة مع `company_os/finance/unit_economics.md`:

```txt
1. الهامش الإجمالي يبقى فوق 60% — إن انخفض: ارفع السعر أو قلّل وقت التسليم.
2. حصّل دفعة مقدّمة — 50% على الأقل قبل بدء أي ارتباط.
3. تتبّع CAC بدقة — إذا تجاوز 20% من LTV، أصلح القمع.
4. فحص نقدي أسبوعي — اعرف بالضبط كم نقداً حُصّل مقابل ما فُوتر.
```

---

## 5. علاقة السعر بالتحويل والتسليم

```txt
سعر منخفض جداً  → هامش ضعيف + جذب عملاء صعبي التسليم
سعر مرتفع جداً  → قتل التحويل في البداية
السعر الصحيح    → أعلى سعر لا يقتل التحويل ويُبقي الهامش > 60%
```

حلقة التعلّم الأسبوعية تكتشف **أي سعر لا يقتل التحويل** لكل Sprint.

---

## 6. أعلام اقتصادية تستدعي التوقّف

| العلم | المعنى | الإجراء |
|------|--------|---------|
| 🔴 الهامش < 60% | الـ Sprint يخسر وقتك | ارفع السعر أو بسّط التسليم |
| 🔴 founder_involvement مرتفع دائماً | لا يتوسّع | أتمت الخطوات المتكررة |
| 🟠 revision_risk مرتفع | scope مفتوح | أغلق النطاق في العرض |
| 🟠 upsell_potential منخفض | LTV ضعيف | أعد تصميم مسار التوسّع |

---

## 7. الربط بباقي البنية

- الأسعار الافتتاحية للـ Sprints: [OFFER_STRATEGY_AR](./OFFER_STRATEGY_AR.md).
- أثر سعة التسليم على الساعات: [DELIVERY_BEFORE_SALES_POLICY_AR](./DELIVERY_BEFORE_SALES_POLICY_AR.md).
- المراجعة العملية للأرقام: [UNIT_ECONOMICS_REVIEW](../../reports/success/UNIT_ECONOMICS_REVIEW.md).

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder | Status: Active*
