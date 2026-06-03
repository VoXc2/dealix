# Metrics Engine — كيف تعرف أنك على الطريق؟

لكل **عائلة ledger** مؤشرات تشغيلية (تُجمع أسبوعيًا/شهريًا).

## AI Run Metrics

AI cost / project · AI cost / workflow · QA pass rate · schema failure rate · model fallback rate · high-risk run count

## Governance Metrics

blocked actions · approval delays · PII flags · source attribution coverage · audit coverage · policy violations

## Proof Metrics

proof packs / project · proof events / project · فئات قيمة مغطاة · proof معتمد من العميل · **proof-to-retainer conversion**

## Capital Metrics

assets / project · نسبة الأصول القابلة لإعادة الاستخدام · تحديثات playbook · feature candidates · رؤى آمنة للسوق

## Product Metrics

ساعات يدوية موفرة · feature reuse · استخدام أدوات داخلية · module adoption · انخفاض وقت التسليم

## Business Unit Metrics

إيراد الوحدة · هامش · QA · proof count · retainers · نضج المنتج · نضج الـ playbook

**عائلات الأحداث:** `intelligence_os/metrics_engine.py` · **من event → عائلة:** `intelligence_os/events_to_metrics.py`

**لوحات:** [`../institutional/EXECUTIVE_DASHBOARDS.md`](../institutional/EXECUTIVE_DASHBOARDS.md)
