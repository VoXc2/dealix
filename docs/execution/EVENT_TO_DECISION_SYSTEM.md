# Dealix Event-to-Decision System (Execution Layer)

**الهدف:** كل حدث مهم ينتج **قرارًا محتملًا** — Dealix «تفكر» من بياناتها التشغيلية.

---

## أمثلة أحداث

`dataset_uploaded` · `data_quality_scored` · `pii_detected` · `governance_checked` · `proof_event_created` · `capital_asset_created` · `feature_candidate_created` · `retainer_recommended` · `partner_lead_created` · `venture_signal_detected`

**نموذج أحداث الريبو:** [`../architecture/EVENT_MODEL.md`](../architecture/EVENT_MODEL.md)

---

## قواعد قرار (مختصرة)

| إشارة | قرار مقترح |
|--------|-------------|
| `data_quality_score < 60` | Data Readiness قبل workflow AI |
| `proof_strength > 85` و `client_health > 70` | توصية retainer |
| خطوة يدوية تُكرر **3+** | مرشح ترسية (productization) |
| إجراء مُحظر يتكرر | تشديد حوكمة + رد objection مبيعات |
| `paid_clients ≥ 5` و `retainers ≥ 2` | مراجعة venture candidate |

**الكود:** `auto_client_acquisition/execution_os/event_to_decision.py` — `recommend_decisions`.

---

## مرجع طبقة الاستخبارات

التفصيل الاستراتيجي الأوسع: [`../intelligence/EVENT_TO_DECISION_SYSTEM.md`](../intelligence/EVENT_TO_DECISION_SYSTEM.md) — هذا المستند يخص **تنفيذ Dealix الأسبوعي/المشروع** ومزامنته مع الـ ledgers.

**صعود:** [`EXECUTION_SUPREMACY_SYSTEM.md`](EXECUTION_SUPREMACY_SYSTEM.md)
