# Quality Review Board

كل تسليم عميل يُراجع ضد:

## Business
- يجيب على المشكلة الفعلية؟ · next action؟ · مناسب للإدارة؟

## Data
- مصادر واضحة؟ · حقول ناقصة مذكورة؟ · PII؟

## AI
- دقة · عدم اليقين واضح · citations حيث لزم

## Arabic
- طبيعي واحترافي · نبرة أعمال سعودية مناسبة

## Governance
- forbidden actions؟ · ادعاءات بلا أدلة؟ · فجوات موافقة؟

## Decision
**Approved** / **Needs revision** / **Blocked** — سجّل الـscore من [`OUTPUT_QA_SCORECARD.md`](OUTPUT_QA_SCORECARD.md) أو الجدول أدناه.

## Delivery Quality Score (summary)

| Area | /max | Notes |
|------|-----:|-------|
| Business usefulness | 20 | |
| Data quality | 15 | |
| AI accuracy | 15 | |
| Arabic/English | 10 | |
| Compliance | 15 | |
| Actionability | 10 | |
| Report quality | 10 | |
| Upsell clarity | 5 | |
| **Total** | **100** | Pass ≥85 unless hard fail |

90–100 ممتاز · 85–89 تسليم · 70–84 مراجعة · أقل من 70 ممنوع · **Hard fail = ممنوع فوراً**
