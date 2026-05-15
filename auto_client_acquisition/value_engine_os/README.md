# value_engine_os — System 34: Business Value Engine

## English

Measures the business value of workflow runs — revenue impact, time saved,
execution speed, efficiency gain — and computes ROI per workflow.

Tier discipline (mirrors `value_os`): a `measured` metric must carry a
verifiable `source_ref`; otherwise it is rejected with `ValueDisciplineError`
(`no_unverified_outcomes` / `no_fake_proof`). The engine measures only — it
never charges anything (`no_live_charge`).

Distinct from the customer-facing `value_os` (Monthly Value Reports); this is
the internal workflow-ROI engine.

## العربية

تقيس القيمة التجارية لتشغيلات سير العمل — أثر الإيراد والوقت الموفّر وسرعة
التنفيذ ومكاسب الكفاءة — وتحسب العائد على الاستثمار لكل سير عمل. أي مقياس
"مُقاس" يجب أن يحمل مرجع مصدر موثّقًا وإلا رُفض. المحرّك يقيس فقط ولا يحصّل أي مبالغ.

## API

`/api/v1/value-engine` — `POST /metrics`, `GET /workflows/{id}/roi`,
`GET /optimization-candidates`.
