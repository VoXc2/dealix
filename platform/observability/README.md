# Observability

## الحد الأدنى الإلزامي
- traces
- logs
- workflow metrics

## مخرجات v1
- `trace_id` لكل تشغيل
- structured logs على مستوى الخطوات
- counters للخطوات/retries/blocking + زمن التنفيذ

## نقطة ربط
- `ObservabilityRuntime` في `auto_client_acquisition/foundation_core/enterprise_loop.py`
