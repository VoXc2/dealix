# حزم مهام الوكلاء اليومية

> للمؤسس + Cursor subagents · مسودات خارجية فقط

**قالب المهام (SoT):** [`dealix/config/founder_agent_task_queue.yaml`](../../dealix/config/founder_agent_task_queue.yaml) · **حالة اليوم:** `data/founder_agent/queue_today.json` · **أمر:** `py -3 scripts/founder_agent_queue_status.py --seed-today`

**كتاب التشغيل:** [`FOUNDER_AGENT_PLAYBOOK_AR.md`](FOUNDER_AGENT_PLAYBOOK_AR.md)

**إيقاع أسطول (أمر واحد):** `bash scripts/run_founder_agent_fleet_rhythm.sh` · `--weekly` · Windows: `run_founder_agent_fleet_rhythm.ps1`

---

## هرم التشغيل (3 مستويات)

```text
أنت + dealix-pm (أوركستريتور)
  → dealix-sales | dealix-delivery | dealix-engineer | dealix-content
    → مهمة جزئية واحدة = حزمة عمل واحدة
```

---

## حزم يومية

| الحزمة | الوكيل | مخرج | تحقق |
|--------|--------|------|--------|
| `pm_morning_orchestrator` | dealix-pm | `data/founder_briefs/daily_decisions_{date}.md` | `founder_comprehensive_plan_status.py` |
| `sales_war_room_drafts` | dealix-sales | `data/outreach_drafts/` | `commercial_war_room_sync.py --dry-run` |
| `delivery_proof_checklist` | dealix-delivery | `data/proof_packs/` | Proof standard |
| `engineer_gate_smoke` | dealix-engineer | `last_engineer_gate.json` | `verify_railway_production_config.py` |
| `content_aeo_draft` | dealix-content | `data/content_drafts/` | `queue_content_drafts_for_approval.py` |

## حزمة أسبوعية

| الحزمة | الوكيل | مخرج | تحقق |
|--------|--------|------|--------|
| `weekly_metrics_bundle` | dealix-pm | `data/founder_weekly/metrics_{week}.yaml` | `founder_weekly_metrics_bundle.py` |

---

## ذاكرة مشتركة (لا تخترع)

| طبقة | مسار |
|------|------|
| قرارات المؤسس | `founder_integration_truth.yaml` |
| أرقام CRM | `kpi_founder_commercial_import.yaml` فقط |
| أحداث إثبات | `evidence_events_tracker.csv` |
| أولويات | `business_now_cache.yaml` |

---

## Prompt قالب

```text
نفّذ حزمة {packet_id} من data/agent_work_packets/daily_packets.yaml.
اقرأ المدخلات، اكتب المخرجات في المسار المحدد، شغّل verify_commands.
لا إرسال خارجي. لا أرقام مخترعة.
```
