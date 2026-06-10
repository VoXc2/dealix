# Evidence-to-Risk

كل **Evidence Gap** = إشارة مخاطر.

## أمثلة

| Gap | نوع الخطر |
|-----|------------|
| Missing Source Passport | Data Risk |
| Missing Approval | Channel Risk |
| Missing Proof | Claim Risk |
| Missing Review | QA Risk |
| Missing Agent Card | Autonomy Risk |
| Missing Value Event | Retainer Risk |

## تصعيد

- Low: إصلاح قبل التقرير التالي  
- Medium: حظر تسليم حتى الإصلاح  
- High: مراجعة حادثة  
- Critical: إيقاف مؤقت للـ workflow  

## الكود

`evidence_gap_detector.py` — ربط gap بـ severity.
