# Client Maturity Score

درجة موحّدة **0–100** تجمع أبعاد النضج التشغيلي.

## الأبعاد والأوزان

| البعد | الوزن |
|--------|-------|
| Leadership alignment | 15 |
| Data readiness | 15 |
| Workflow ownership | 15 |
| Governance coverage | 20 |
| Proof discipline | 15 |
| Adoption | 10 |
| Operating cadence | 10 |

## القرار

| النطاق | المعنى |
|--------|--------|
| 85–100 | جاهز لتوسع مؤسسي (L6–L7 مع شروط) |
| 70–84 | retainer / workspace جاهز (L4–L5) |
| 55–69 | sprint + enablement (L2–L3) |
| 35–54 | diagnostic + readiness (L0–L1) |
| <35 | لا تنشر سير عمل AI حتى إصلاح الأساسيات |

## الكود

`auto_client_acquisition/client_maturity_os/maturity_score.py`
