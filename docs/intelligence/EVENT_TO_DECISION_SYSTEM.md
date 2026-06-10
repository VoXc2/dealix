# Event → Decision System

## 1. Event Layer — كل شيء يبدأ بحدث

لا تجعل Dealix **مجرد سجلات CRUD** فقط — اجعلها **event-driven**.

### أحداث أساسية

`project_created` · `client_intake_completed` · `data_source_registered` · `dataset_uploaded` · `data_quality_scored` · `pii_detected` · `governance_checked` · `ai_run_completed` · `account_scored` · `draft_generated` · `approval_required` · `approval_granted` · `proof_event_created` · `report_delivered` · `capital_asset_created` · `feature_candidate_created` · `retainer_recommended` · `retainer_won` · `playbook_updated` · `partner_lead_created` · `venture_signal_detected`

**الفائدة:** audit trail · proof trail · client timeline · AI analytics · governance monitoring · telemetry · capital tracking · لوحة CEO.

### مثال

```json
{
  "event_type": "proof_event_created",
  "project_id": "PRJ-001",
  "client_id": "CL-001",
  "proof_type": "Revenue Value",
  "metric": "accounts_scored",
  "value": 50,
  "source": "Revenue Intelligence Report",
  "created_at": "2026-05-13T12:00:00Z"
}
```

**ربط event → عائلة مؤشرات (كود):** `intelligence_os/events_to_metrics.py`

---

## 2. Decision Layer — أنواع القرارات

| نوع قرار | معنى |
|-----------|------|
| Sell More | مضاعفة عرض فائز |
| Raise Price | جودة إثبات تسمح برفع سعر |
| Stop Selling | كلفة/مخاطر عالية |
| Productize | تكرار + رابط إيراد |
| Create Playbook | نمط قطاعي ناضج |
| Offer Retainer | proof + صحة عميل + cadence |
| Create Partner Offer | توزيع تحت حوكمة |
| Promote to Business Unit | وحدة ناضجة |
| Promote to Venture Candidate | venture score مرتفع |
| Kill Experiment | لا إثبات ولا هامش |

### مثال Lead Intelligence (مختصر)

**إذا:** win rate عالٍ · proof عالٍ · تكرار scoring يدوي · **2+ retainers**  
**قرار:** Scale Dealix Revenue · تعزيز Revenue OS · رفع سعر ~15% · B2B playbook

**إذا:** Support Desk طلب منخفض · QA معقّد · لا retainer  
**قرار:** Hold / Pilot only — لا Support OS كامل بعد

**تصنيف القرارات (كود):** `intelligence_os/decision_engine.py` (`IntelligenceDecision`)

---

## 3. التسلسل الكامل

```text
Events → Ledgers → Metrics → Decisions → Capital Allocation
→ Productization / BU / Venture → Strategic Memory
```

انظر [`LEDGER_ARCHITECTURE.md`](LEDGER_ARCHITECTURE.md) · [`METRICS_ENGINE.md`](METRICS_ENGINE.md) · [`CAPITAL_ALLOCATION_SCORE.md`](CAPITAL_ALLOCATION_SCORE.md)
