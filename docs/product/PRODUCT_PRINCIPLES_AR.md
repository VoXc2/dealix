# Dealix — مبادئ المنتج

## المبادئ التوجيهية

### 1. الإيراد قبل الزينة
> لا نبنى ميزات لا تُحقق إيراد أو توفر وقت جوهري.

كل feature يجب أن تُجيب على سؤال: **كيف تزيد الإيراد أو تقلل التكلفة أو تحميDealix?**

### 2. الثقة قبل الأتمتة
> لا أتمتة بدون حوكمة. لا إرسال بدون موافقة.

- كل إجراء خارجي يمر عبر Approval Queue
- Safety Gates إلزامية
- Audit log لكل إجراء

### 3. أدلة قبل الادعاءات
> Proof قبل Proposal.

- لا نقدم ادعاءات بدون evidence
- كل تقرير عميل يتضمن بيانات حقيقية
- Case studies من مشاريع حقيقية

### 4. CI وHealth قبل الإطلاق
> لا إطلاق بدون اختبارات وبنية صحية.

- اختبارات CI مرتبطة بكل PR
- Health checks للـ APIs
- Rollback plan لكل feature

### 5. العميل يحكم
> كل قرار منتج يجب أن يمر عبر العميل.

مصادر القرار:
- Discovery calls
- Proposal objections
- Delivery blockers
- Renewal reasons
- Churn risks

### 6. التكرار أولاً
> نُركز على what's repeatable قبل what's novel.

- بناء playbooks قابلة للتكرار
- توثيق what's working
- أتمتة what's repeatable

### 7. البساطة قوة
> Less is more. كل feature جديدة يجب أن تُثبت قيمتها.

- MVP أولاً
- Iterate بناءً على feedback
- Remove ما لا يعمل

### 8. البيانات تُقنع
> الأرقام تتحدث. القرارات تتبع البيانات.

- Metric قبل initiative
- Measure everything
- Trust the data not the opinion

---

## Anti-Patterns (لا نفعل)

| Anti-Pattern | البديل |
|--------------|--------|
| Building features nobody asked for | Wait for customer signal |
| Automating without approval gates | Always require human approval |
| Making claims without proof | Lead with evidence |
| Complex solutions for simple problems | KISS principle |
| Launching without testing | CI + health first |

---

## Decision Framework

### لبدء بناء Feature:
1. ✅ Customer pain identified?
2. ✅ Revenue impact quantified?
3. ✅ Risk assessed?
4. ✅ MVP scope defined?
5. ✅ Approval gates defined?
6. ✅ CI tests planned?

### لعدم بناء Feature:
1. ❌ No customer signal?
2. ❌ Risk > Value?
3. ❌ Complicates core flow?
4. ❌ Not repeatable?

---

## _links

- Strategy: `PRODUCT_STRATEGY_AR.md`
- MVP Scope: `MVP_SCOPE_AR.md`
- Roadmap: `ROADMAP_AR.md`
- What Not to Build: `WHAT_NOT_TO_BUILD_AR.md`
