# Founder Command Center

The single screen the founder/CEO opens every morning. Tells you exactly
what matters today, what's at risk, and what to decide.

> Markdown form is the MVP. Wire it to live event-store data in Phase 2
> (Founder Command Center UI in `frontend/src/app/[locale]/`).

## Today (refresh each morning)

### Money
- Active proposals (count + total SAR): __
- Verbal yes pending payment: __
- Cash collected this week: __
- Cash collected MTD: __

### Active projects
- Total active sprints: __
- In Discover / Diagnose: __
- In Build / Validate: __
- In Deliver / Prove / Expand: __

### Quality
- QA reviews pending: __
- Quality Score (last 5 projects, avg): __
- Hard-fails this month: __ (target 0)

### Governance
- Pending approvals: __
- PII incidents this month: __ (target 0)
- Forbidden-action blocks this week: __

### AI cost
- LLM spend MTD: SAR __
- Cost per active project: SAR __
- Budget utilization: __%

### Sales pipeline
- New leads this week: __
- Discovery calls scheduled: __
- Proposals sent: __
- Retainer conversations active: __

### Risks / blockers
1. __
2. __
3. __

### Upsell opportunities
1. __
2. __
3. __

### Compounding assets created this week
- New templates: __
- New playbook updates: __
- New feature candidates: __
- New anonymized sales assets: __

## Today's 3 decisions

The founder closes the day having made exactly 3 decisions, no more.

1. __
2. __
3. __

## How to refresh

```bash
python scripts/verify_dealix_ready.py   # gate status
python scripts/verify_full_mvp_ready.py # full scorecard
git log --since="1 week ago" --oneline  # what shipped
```

Then manually update the numbers above. Phase 2 wires this to live data via
`api/routers/reports.py` weekly endpoint.

## Cross-links

- `docs/company/DEALIX_OPERATING_KERNEL.md`
- `docs/company/WEEKLY_OPERATING_REVIEW.md`
- `docs/analytics/executive_kpi_spec.md` (W4.T13 — canonical KPI definitions)
- `docs/operations/executive_operating_cadence.md` (W5.T30 — weekly/monthly/quarterly rituals)
