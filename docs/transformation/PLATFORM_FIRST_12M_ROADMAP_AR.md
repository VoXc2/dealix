# خارطة Platform-First — مراحل بوابات (12 شهر تشغيلي)

> التقدم **بوابات إثبات** وليس تواريخ ثابتة. كل مرحلة تُغلق بتحقق آلية.

## المرحلة A — Spine (موجة 0)

- North Star manifest + registry 100 مبادرة
- إيقاع تنفيذي 2.0 + operating calendar
- **بوابة:** `--check-initiatives` PASS

## المرحلة B — حوكمة وقراءة جاهزية (موجة 1)

- Policy-as-Code، lanes، unified readiness API
- **بوابة:** `pytest tests/test_unified_readiness.py` + governance tests

## المرحلة C — منصة (موجة 2)

- API domain ownership، SLO by domain، script inventory
- **بوابة:** `reliability_drills_scorecard` + domain doc

## المرحلة D — إيراد (موجة 3)

- Deal Desk، attribution، productized offers، GTM سعودي
- **بوابة:** `revenue_os_master_verify.sh`

## المرحلة E — منتج وأدلة (موجات 4–5)

- PERB أسبوعي، capability map، trust dashboard، DQ OS
- **بوابة:** weekly proof pack يحتوي PERB + initiative rollup

## المرحلة F — تجربة عميل (موجة 6)

- أول 14 يوم، QBR، blueprints
- **بوابة:** delivery + adoption tests

## المرحلة G — مؤسسة (موجات 8–10)

- portfolio bets، institution mode، academy، board pack
- **بوابة:** `generate_board_ready_pack.py` + ownership review

## مراجعة ربع سنوية

حدّث حالة المبادرات في `strategic_initiatives_registry.yaml` (`proposed` → `active` → `done`).
