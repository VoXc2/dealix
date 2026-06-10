# دليل التشغيل الأسبوعي — WEEKLY_OPERATING_GUIDE_AR

> **الإيقاع الأسبوعي** — كل يوم أحد 9 صباحاً: مراجعة pipeline + deal risk + governance eval + data product refresh + founder escalation. checklist بمالك لكل بند.
>
> **آخر تحديث:** 2026-06-03 — المالك: Founder — الإصدار: v1.0

---

## 1) الوقت والمدة

- **الموعد:** Sunday 9:00 AM (Asia/Riyadh)
- **المدة:** 60 دقيقة
- **الحضور:** Founder + Sales Lead + Data Lead + AI Governance Lead (30 دقيقة founder solo + 30 minute standup)

---

## 2) الأمر الموحّد (Sunday gates)

```bash
bash scripts/founder_weekly_loop.sh
# يطبع: DEALIX_WEEKLY_VERDICT=PASS|FAIL + قائمة البنود
```

---

## 3) البنود (Checklist) — كل بند له مالك

| # | البند | المالك | الوقت | الـ Output |
|---|-------|--------|-------|-----------|
| 1 | **Pipeline Review** | Sales Lead | 10 min | `ENTERPRISE_PIPELINE_REVIEW.md` |
| 2 | **Deal Risk Review** | Sales Lead | 10 min | `ENTERPRISE_DEAL_RISK_REVIEW.md` |
| 3 | **Account Plan Review** | Sales Lead | 5 min | `ACCOUNT_PLAN_REVIEW.md` |
| 4 | **Agent Governance Eval** | AI Governance Lead | 10 min | `AGENT_GOVERNANCE_REVIEW.md` |
| 5 | **Permission Review** | AI Governance Lead | 5 min | `AGENT_PERMISSION_REVIEW.md` |
| 6 | **Incident Review** | AI Governance Lead | 5 min | `AGENT_INCIDENT_REVIEW.md` |
| 7 | **Data Product Refresh** | Data Lead | 5 min | `LEARNING_LOOP_REVIEW.md` |
| 8 | **Data Quality Check** | Data Lead | 5 min | `DATA_QUALITY_REVIEW.md` (legacy) |
| 9 | **Founder Escalation** | Founder | 5 min | `FOUNDER_DECISION_QUEUE.md` |
| **الإجمالي** | — | — | **60 min** | — |

---

## 4) تفاصيل كل بند

### 4.1 Pipeline Review (Sales Lead — 10 min)

```bash
cat reports/enterprise_sales/ENTERPRISE_PIPELINE_REVIEW.md
```

- 3 Tier-1 accounts status?
- New stakeholders added? (`stakeholders.jsonl`)
- MAP milestones on track?
- Conversion: lead → SQL → opportunity → closed-won

### 4.2 Deal Risk Review (Sales Lead — 10 min)

```bash
cat reports/enterprise_sales/ENTERPRISE_DEAL_RISK_REVIEW.md
cat data/enterprise_sales/deal_risks.jsonl
```

- 9 risk categories (champion, economic_buyer, technical, ...)
- Severity: HIGH vs MEDIUM vs LOW
- Mitigation: who/when

### 4.3 Account Plan Review (Sales Lead — 5 min)

```bash
cat reports/enterprise_sales/ACCOUNT_PLAN_REVIEW.md
```

- TAP completeness (14 fields per account)
- Tier distribution (Tier-1/2/3)

### 4.4 Agent Governance Eval (AI Governance Lead — 10 min)

```bash
cat reports/ai_governance/AGENT_GOVERNANCE_REVIEW.md
cat data/ai_governance/agent_evals.jsonl
```

- All active agents evaluated this week?
- New agents registered? (must be `evidence_level=validated`)
- Any A5 attempts? (must be 0)

### 4.5 Permission Review (AI Governance Lead — 5 min)

```bash
cat reports/ai_governance/AGENT_PERMISSION_REVIEW.md
```

- Any scope drift? (agents writing outside `allowed_file_areas`)
- Permission lifecycle: onboarded / retired / modified

### 4.6 Incident Review (AI Governance Lead — 5 min)

```bash
cat reports/ai_governance/AGENT_INCIDENT_REVIEW.md
cat data/ai_governance/agent_incidents.jsonl
```

- Open P0/P1 incidents?
- Time to resolution
- Recurring patterns

### 4.7 Data Product Refresh (Data Lead — 5 min)

```bash
cat reports/data_products/LEARNING_LOOP_REVIEW.md
```

- New rows in `data/data_products/*.jsonl`?
- Any `assumption` upgraded to `observed`/`validated`?
- Sector benchmarks refresh needed?

### 4.8 Data Quality Check (Data Lead — 5 min)

```bash
cat reports/data_governance/DATA_QUALITY_REVIEW.md
cat data/data_governance/data_quality_issues.jsonl
```

- PII leaks? (must be 0)
- Schema validation failures?
- Retention compliance?

### 4.9 Founder Escalation (Founder — 5 min)

```bash
cat reports/analytics/FOUNDER_DECISION_QUEUE.md
```

- Decisions pending founder?
- Approvals queue (top 3)?
- Strategic opportunities (1)?

---

## 5) Output كل أسبوع

- **1 weekly report** → `reports/weekly_operating_<YYYY-WW>.md`
- **1 weekly retrospective** → `docs/ops/FOUNDER_WEEKLY_METRICS_AR.md` (تحديث)
- **3-5 decisions** → `data/analytics/founder_decisions.jsonl`
- **1 weekly meeting notes** → `docs/meetings/WEEKLY_OPERATING_REVIEW.md`

---

## 6) KPIs مراقبة أسبوعية

| KPI | Healthy | Watch | Action |
|-----|---------|-------|--------|
| Conversion lead → SQL | ≥ 10% | 7-10% | < 7% review message library |
| Deal Risk HIGH | 0 | 1-2 | ≥ 3 immediate escalation |
| Open P0/P1 incidents | 0 | 1 | ≥ 2 stop all external actions |
| New agents (validated) | 0-1/week | 2-3 | ≥ 4 sprawl alert |
| Sector benchmarks upgraded | ≥ 1/quarter | — | — |
| Approvals backlog | < 5 | 5-10 | ≥ 10 founder intervention |

---

## 7) See Also

- [`DAILY_OPERATING_GUIDE_AR.md`](DAILY_OPERATING_GUIDE_AR.md)
- [`FOUNDER_START_HERE_AR.md`](FOUNDER_START_HERE_AR.md)
- [`PRIORITY_ROADMAP_AR.md`](PRIORITY_ROADMAP_AR.md)
- [`FILE_OWNERSHIP_MAP.md`](FILE_OWNERSHIP_MAP.md)
- [`DEALIX_COMPANY_OS_INDEX_AR.md`](DEALIX_COMPANY_OS_INDEX_AR.md)

---

## Open Questions for Founder

1. هل 60 دقيقة/اسبوع معقولة، أم تحتاج تخفيض إلى 30 min (دمج البنود)؟
2. هل تريد **automated Slack digest** في 8:55 AM كل أحد يلخّص البنود قبل الاجتماع؟
3. هل تفضّل **asynchronous** weekly review (كل lead يسلّم PR مع review) بدلاً من meeting حي؟
