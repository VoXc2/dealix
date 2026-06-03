# PMF Score — درجة ملاءمة المنتج/السوق

## الصيغة (كل بُعد 0–100)

| البُعد | الوزن |
|--------|------|
| Repeated pain | 15% |
| Clear buyer | 10% |
| Willingness to pay | 15% |
| Delivery repeatability | 15% |
| Proof strength | 15% |
| Retainer conversion | 15% |
| Productization signal | 10% |
| Governance safety | 5% |

## النطاقات

| النتيجة | قرار |
|---------|------|
| 85–100 | Scale |
| 70–84 | Build |
| 55–69 | Pilot |
| below 55 | Hold or Kill |

**مثال:** Revenue Intelligence Sprint غالبًا يحصل على درجة عالية عند تكرار الألم ووضوح المشتري وقرب الإيراد ووجود مسار proof وretainer.

**الكود:** `auto_client_acquisition/investment_os/pmf_score.py` — `PmfScoreInputs` · `compute_pmf_score` · `pmf_band`

**صعود:** [`PMF_SIGNALS.md`](PMF_SIGNALS.md)
