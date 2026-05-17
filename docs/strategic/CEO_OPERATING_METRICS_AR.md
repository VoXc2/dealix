# مؤشرات تشغيل الرئيس التنفيذي (داخلية)

**الاستخدام:** قرارات أسبوعية — **لا تُعلَن خارجياً** حتى تُربَط بمصادر بيانات موثوقة و`no_overclaim`.

## 1. Time-to-first-proof

- **التعريف:** من أول `lead`/`signal` مسجّل إلى أول `ProofEvent` (أو ما يعادله في `proof_ledger`).
- **المصدر المستهدف:** أحداث التسليم + سجل الإثبات (ربط تدريجي).

## 2. Approval cycle time

- **التعريف:** من توصية وكيل/نظام إلى قرار بشري مسجّل في Approval Center.
- **المصدر المستهدف:** طبقة الثقة + سجلات المراجعة.

## 3. معدل التحويل على سلّم الخدمات

- **التعريف:** نسبة الانتقال على سلّم الإيراد المُحوكَم وعمليات الذكاء الاصطناعي: Risk Score المجاني → 7-Day Governed Revenue & AI Ops Diagnostic → Revenue Intelligence Sprint → Governed Ops Retainer.
- **المصدر المستهدف:** CRM/فواتير/تكامل دفع — عند توفرها.
- **مرجع السلم:** [docs/OFFER_LADDER_AND_PRICING.md](../OFFER_LADDER_AND_PRICING.md).

## 4. Degraded portal rate

- **التعريف:** نسبة جلسات البوابة LIVE التي تُظهر `insufficient_data` في أقسام Full-Ops أو Proof.
- **المصدر المستهدف:** [landing/customer-portal.html](../../landing/customer-portal.html) + API البوابة.

## 5. صحة طبقة v10

- تشغيل دوري: `pytest tests/test_*_v10.py -q --no-cov` كجزء من جودة الإصدار.

## مراجع

- [docs/ops/PHASE0_CEO_RELEASE_GATE_AR.md](../ops/PHASE0_CEO_RELEASE_GATE_AR.md)
- [ENTERPRISE_P0_GAP_BACKLOG_AR.md](ENTERPRISE_P0_GAP_BACKLOG_AR.md)
