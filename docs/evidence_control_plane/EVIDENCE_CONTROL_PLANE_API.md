# Evidence Control Plane API (تصميم داخلي)

لا يُشترط بناء FastAPI لهذه المسارات الآن — ابدأ بـ **Python modules + عقود JSON**. صمّمها كأنها ستُبنى لاحقًا.

## مسارات مقترحة

| Method | Path | الغرض |
|--------|------|--------|
| POST | `/evidence/source` | تسجيل مصدر / جواز |
| POST | `/evidence/ai-run` | تسجيل AI run |
| POST | `/evidence/policy-check` | فحص سياسة |
| POST | `/evidence/review` | مراجعة بشرية |
| POST | `/evidence/approval` | موافقة |
| POST | `/evidence/output` | مخرج |
| POST | `/evidence/proof` | حدث proof |
| POST | `/evidence/value` | حدث قيمة |
| GET | `/evidence/graph/{project_id}` | رسم بياني للأدلة |
| GET | `/evidence/gaps/{client_id}` | فجوات الأدلة |

## الكود

`auto_client_acquisition/evidence_control_plane_os/evidence_api.py` — مواصفات المسارات كبيانات.
