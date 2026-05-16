# Enterprise Nervous System — Dealix

هذا المجلد يترجم رؤية Dealix من "شركة AI" إلى "بنية تشغيل مؤسسية" قابلة للقياس.

## Contents

- `OPERATING_BLUEPRINT_V1_AR.md` — المخطط التشغيلي لنظام الأعصاب المؤسسي.
- `CAPABILITY_ROADMAP_V1_AR.md` — خارطة الطريق المرحلية (Control → Intelligence → Execution).
- `EXECUTIVE_SCORECARD_V1_AR.md` — بطاقة القيادة التنفيذية لقياس الأثر.
- `LAYER_STACK_AND_HANDOFFS_V1_AR.md` — عقود الطبقات والتسليم بين الأنظمة.
- `FULL_IMPLEMENTATION_CHECKLIST_V1_AR.md` — قائمة تنفيذ شاملة عبر التقنية والتشغيل والحوكمة.

## Product Hook

واجهات برمجية مرتبطة بهذه الوثائق:

- `GET /api/v1/enterprise-nervous-system/blueprint`
- `GET /api/v1/enterprise-nervous-system/roadmap`
- `GET /api/v1/enterprise-nervous-system/scorecard`
- `GET /api/v1/enterprise-nervous-system/layers/contracts`
- `GET /api/v1/enterprise-nervous-system/layers/dependencies`
- `POST /api/v1/enterprise-nervous-system/layers/validate`
- `GET /api/v1/enterprise-nervous-system/health/defaults`
- `POST /api/v1/enterprise-nervous-system/health/cross-plane`
- `POST /api/v1/enterprise-nervous-system/assess`
- `POST /api/v1/enterprise-nervous-system/assess/full`
