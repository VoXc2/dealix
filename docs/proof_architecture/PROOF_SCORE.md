# Proof Score — v2 (Enterprise)

كل Proof Pack يأخذ **0–100** حسب الأوزان:

| المكوّن | الوزن |
|---------|------:|
| Metric clarity | 15 |
| Source clarity | 15 |
| Evidence quality | 15 |
| Governance confidence | 15 |
| Business relevance | 15 |
| Before/after comparison | 10 |
| Retainer linkage | 10 |
| Limitations honesty | 5 |

## التفسير

- **85–100:** مرشح case  
- **70–84:** دعم مبيعات  
- **55–69:** تعلّم داخلي  
- **أقل من 55:** proof ضعيف — تحسين التسليم  

## قواعد Dealix

لا case study بدرجة أقل من **85**.  
لا استخدام في **sales** بدرجة أقل من **70**.  
لا دفع **Retainer** إذا **proof score** أقل من **80**.

**الكود:** `EnterpriseProofDimensions` · `enterprise_proof_score` · `proof_score_band` — `proof_architecture_os/proof_score.py` · **مستويات النشاط→التشغيل:** `PROOF_LEVELS` — `proof_architecture_os/proof_levels.py`

**صعود:** [`PROOF_PACK_V2.md`](PROOF_PACK_V2.md)
