# Dealix Cloud — خارطة الواجهة والـ API

يربط [DEALIX_CLOUD_VISION.md](DEALIX_CLOUD_VISION.md) بمسارات Phase 2 في [PHASE_COMPLETION_TRACKER.md](../PHASE_COMPLETION_TRACKER.md).

## مركز التنقل

| Surface | مسار |
| --- | --- |
| **Business HQ (الآن)** | `/[locale]/business-now` — لقطة تشغيل + `GET /api/v1/business-now/commercial-strategy` (قرارات واستراتيجية؛ يكمّل Cloud) |
| **Operator signals** | نفس الصفحة عند `NEXT_PUBLIC_DEALIX_ADMIN_API_KEY` — `GET /api/v1/business-now/operator-signals` |

| وحدة Cloud | مسار UI | API / مرجع |
| --- | --- | --- |
| Client Workspace | `/[locale]/clients` | إدارة العملاء |
| Reporting Dashboard | `/[locale]/dashboard` | KPI + charts |
| Capability Scorecards | `/[locale]/analytics` | تحليلات |
| Data OS | `/[locale]/cloud` (بطاقة Data OS) | `GET /api/v1/revenue-os/catalog` |
| Revenue OS | `/[locale]/cloud` + `/[locale]/pipeline` | catalog، leads، decision passport |
| Governance OS | `/[locale]/approvals` | Approval center |
| Workflow OS | `/[locale]/agents` | نشاط الوكلاء |
| Proof Ledger | `/[locale]/trust-check` | anti-waste + evidence levels |
| AI Control Tower | `/[locale]/agents` + `/[locale]/approvals` | حوكمة الوكلاء |
| Knowledge OS | `/[locale]/cloud` (قريبًا embeddings) | [EMBEDDINGS_PIPELINE.md](../EMBEDDINGS_PIPELINE.md) |
| Compliance / Trust | `/[locale]/trust-check` | PDPL + L0–L5 |
| Customer portal | `/[locale]/customer-portal` | Phase 2 beta |

## Revenue OS (من مركز Cloud)

| Endpoint | استخدام UI |
| --- | --- |
| `GET /api/v1/revenue-os/catalog` | مصادر، waterfall، action catalog |
| `GET /api/v1/decision-passport/evidence-levels` | مستويات L0–L5 |
| `GET /api/v1/decision-passport/golden-chain` | السلسلة الذهبية |
| `POST /api/v1/revenue-os/anti-waste/check` | فحص الهدر (لا إرسال خارجي تلقائي) |

متغير الواجهة: `NEXT_PUBLIC_API_URL` (افتراضي `http://localhost:8000`).

## Phase alignment

| Phase | Cloud modules المستهدفة |
| --- | --- |
| 2 Private beta | Workspace، Dashboard، Governance، Proof، Cloud hub |
| 3 Paid | Moyasar + DPA (خارج UI؛ بوابات في scripts) |
| 4 Public | كل الوحدات + PUBLIC_LAUNCH_CHECKLIST |
