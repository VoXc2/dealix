# Market Intelligence — ذكاء السوق

## الأسئلة التشغيلية

- من يشتري؟ لماذا يشتري؟  
- ما الألم المتكرر؟ ما اللغة التي يفهمها؟  
- ما الاعتراض المتكرر؟ ما القطاع الأسرع نموًا في الطلب؟

## مصادر إشارات (taxonomy)

مثال في المنتج: `sales_call`, `inbound_form`, `partner_referral`, … — راجع `market_intelligence.py`.

## قواعد تشغيلية (مثال)

- **ألم أو اعتراض يتكرر ≥3 مرات** → صفحة عرض / رد اعتراض جاهز.  
- **قطاع يتكرر ≥5 مرات** → vertical playbook.

## حدود الأمان

لا تُخزَّن تسجيلات مكالمات خام كـ «ذكاء» في طبقة عامة؛ التجميع **ملخّص ومجهّل** حيث يلزم.

## مراجع سياقية (خارجية)

- [IT Pro — AI adoption vs clear ROI strategy](https://www.itpro.com/business/business-strategy/ai-adoption-projects-keep-failing-but-enterprise-fomo-means-investment-is-still-rising)

## روابط

- [INTELLIGENCE_FLYWHEEL.md](INTELLIGENCE_FLYWHEEL.md) · [DECISION_ENGINE.md](DECISION_ENGINE.md) · [INTELLIGENCE_TO_BENCHMARK_SYSTEM.md](INTELLIGENCE_TO_BENCHMARK_SYSTEM.md)
