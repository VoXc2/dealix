# Dealix Client Maturity Engine

محرك داخلي يحدد **مستوى العميل** على السلم (0–7)، والعرض المناسب، وما يُمنع أو يُؤجّل، وسببًا قصيرًا يشرح القرار.

> الملف البرمجي: `maturity_engine.py` (نفس دور «client maturity engine» في المستودع).

## المخرجات (مرجع JSON)

```json
{
  "client_id": "CL-001",
  "maturity_level": 3,
  "current_state": "AI-Assisted Workflow",
  "recommended_next_offer": "Governance Runtime Setup + Proof Pack System + Monthly Operating Cadence",
  "blocked_offers": ["Enterprise AI Control Plane", "Autonomous Agents", "Monthly Retainer"],
  "reason": "Workflow exists but audit and governance coverage are incomplete."
}
```

## المدخلات (للمحرك)

| حقل | المعنى |
|-----|--------|
| **Leadership alignment** | جزء من `ClientMaturityDimensions` (0–100) |
| **Data readiness** | جاهزية بيانات |
| **Workflow ownership** | وضوح الملكية على السير |
| **Governance maturity** | `governance_coverage` في الأبعاد |
| **Proof discipline** | انضباط الإثبات في الأبعاد |
| **Proof score** | جودة/اكتمال proof (عتبة retainer ≥ 80) |
| **Adoption score** | اعتماد فعلي (عتبة retainer ≥ 70) |
| **Monthly cadence** | `monthly_cadence_active` |
| **Audit need** | `requires_audit` (بوابة L7) |
| **Workflow count** | عدد سير العمل النشطة |
| **Executive sponsor / Governance owner** | بوابات L7 |
| **Clear budget** | بوابة L7 |
| **Shadow AI uncontrolled** | كبح السلم عند ضعف الحوكمة |

## اللوحة التشغيلية

انظر [MATURITY_DASHBOARD.md](MATURITY_DASHBOARD.md) — `build_maturity_dashboard()` يضيف: `proof_score`، `adoption_score`، `governance_score`، `readiness_blockers`، وإشارات سحب المنصة.

## الكود

- `auto_client_acquisition/client_maturity_os/maturity_engine.py`  
- `maturity_score.py` — درجة 0–100 والنطاقات  
- `offer_matrix.py` — عروض، ممنوعات، `level1_first_track`، شروط retainer وL7  

## روابط

- [MATURITY_TO_OFFER_MATRIX.md](MATURITY_TO_OFFER_MATRIX.md)  
- [MATURITY_DASHBOARD.md](MATURITY_DASHBOARD.md)
