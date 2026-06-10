# Dealix Moat Score

مقياس داخلي مركب لـ**قوة الخندق التشغيلي** (ليست شعبية منتج).

---

## الأبعاد والأوزان

| البُعد | الوزن |
|--------|------|
| Governance depth | 20 |
| Proof strength | 20 |
| Product reuse | 15 |
| Saudi/Arabic differentiation | 15 |
| Capital assets created | 10 |
| Partner / Academy distribution | 10 |
| Market language adoption | 10 |

كل بُعد يُقيَّم **0–100**؛ الدرجة المركبة = مجموع (بُعد × وزن) / 100.

---

## التفسير

| النطاق | التسمية |
|--------|---------|
| 85–100 | strong moat |
| 70–84 | emerging moat |
| 50–69 | weak moat |
| < 50 | commodity risk |

---

## مثال تشغيلي

**Revenue Intelligence Sprint** يرفع الدرجة لأنه يجمع: قيمة مالية واضحة، proof قوي، تكرار، حوكمة outreach، لغة أعمال سعودية، إمكان ترسية.

---

## الكود

- `MoatScoreDimensions` · `weighted_moat_score` · `moat_tier` · `moat_compound_index` — `auto_client_acquisition/moat_os/moat_score.py`
- تبني لغة السوق: `moat_market_language_adoption_score` — `moat_os/market_language_score.py`

**صعود:** [`STRATEGIC_OPERATING_MOAT.md`](STRATEGIC_OPERATING_MOAT.md)
