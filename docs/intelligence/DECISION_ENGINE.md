# Strategy Office — Decision Engine

**طبقتان ماليتان في الكود المحض:**

1. **Capital priority** (`capital_allocator.py`) — تخصيص الموارد عبر أوزان إيراد/إثبات/منتج…  
2. **Strategy decision score** (`strategy_decision.py`) — قرار استراتيجي أوسع يشمل **margin**، **governance_safety**، **signals** للتوسع/الإيقاف.

## Decision types (تصنيف تشغيلي)

`SCALE` · `BUILD` · `PILOT` · `HOLD` · `KILL` — عبر `StrategyDecisionBand` بعد حساب النقاط.

**إجراءات ثانوية مقترحة يدويًا من القيادة:** `RAISE_PRICE` · `PRODUCTIZE` · `RETENTION_PUSH` · `PARTNER_PUSH` · `VENTURE_CANDIDATE` (تُضاف في لوحة القرار عندما يدعمها المؤشر — **لا أتمتة بلا موافقة بشرية**).

## الصيغة

```text
Decision Score =
  revenue_signal * 0.20
+ margin_signal * 0.15
+ proof_signal * 0.15
+ repeatability_signal * 0.15
+ governance_safety * 0.15
+ productization_signal * 0.10
+ strategic_moat * 0.10
```

## القواعد

| نقاط | نطاق |
|------|------|
| **85–100** | SCALE |
| **70–84** | BUILD |
| **55–69** | PILOT |
| **40–54** | HOLD |
| **<40** | KILL |

## أمثلة

**Lead Intelligence Sprint** بإشارات عالية → **SCALE** + مراجعة **RAISE_PRICE** + **PRODUCTIZE** (انظر [`OPERATING_ALGORITHMS.md`](OPERATING_ALGORITHMS.md)).

**Random custom chatbot** إشارات ضعيف وحوكمة شبهة → **KILL** أو إعادة إطار **Company Brain Sprint**.

**الكود:** `compute_strategy_decision_score` · `strategy_decision_band` في `auto_client_acquisition/intelligence_os/strategy_decision.py`

**قرارات أدق (تصنيف):** `IntelligenceDecision` في `decision_engine.py`
