# Capital Allocation Score

| البُعد | الوزن |
|--------|------:|
| Revenue impact | 20 |
| Repeatability | 15 |
| Margin improvement | 15 |
| Governance value | 15 |
| Proof strength | 10 |
| Productization potential | 10 |
| Strategic moat | 10 |
| Speed to learn | 5 |

## القرار

- **85–100:** Invest now  
- **70–84:** Build small MVP  
- **55–69:** Test manually  
- **‏‏<55:** Hold / reject  

كل بُعد يُدخل كقيمة **0–100** (قوة البوابة)، ثم يُحسب المجموع المرجّح: `sum(dimension × weight) // 100` بحد أقصى 100.

## مثال — Proof Pack Generator (≈88 → Invest now)

مدخلات تقريبية (تطابق مساهمات تشغيلية قوية):  
`CapitalAllocationDimensions(75, 100, 100, 67, 100, 100, 80, 100)` → **88** → `invest_now`.

## مثال عكسي — Academy Portal مبكرًا (≈49 → Hold)

عندما Method غير مستقر وأصول proof ناقصة، تبقى الأبعاد منخفضة، مثل:  
`CapitalAllocationDimensions(45, 40, 40, 70, 50, 50, 50, 50)` → **49** → `hold_or_reject`.  
**الشرط التالي:** مثلًا 10 مشاريع + 3 أصول proof قوية قبل إعادة التقييم.

**الكود:** `CapitalAllocationDimensions` · `capital_allocation_score` · `capital_allocation_band` — `operating_finance_os/capital_allocation_score.py`

**صعود:** [`CAPITAL_ALLOCATION_DASHBOARD.md`](CAPITAL_ALLOCATION_DASHBOARD.md)
