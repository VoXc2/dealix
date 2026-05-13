# AI Quick Win Sprint — Executive Report Skeleton / هيكل التقرير التنفيذي

Bilingual PDF, <= 10 slides. Compiled on Day 6, finalized on Day 7. Delivered to process owner + COO/CFO sponsor.

## 1. Headline / العنوان
- One-line outcome AR + EN (e.g., "Weekly CEO report now runs in 4 minutes instead of 6 hours, with 100% audit-log coverage.").
- Use case label (one of the curated 5).
- Sprint window + customer codename.

## 2. Executive Summary / الملخص التنفيذي
- The painful manual process before the sprint.
- What automation now does + what still requires human approval.
- One number for the CEO (hours saved / errors avoided / cycle-time delta).

## 3. The Automation / الأتمتة
- Input -> processing -> output flow diagram.
- Approval gates highlighted (per `dealix/trust/approval_matrix.py`).
- Trigger: cron / event / manual.
- Owners: process owner, backup, escalation.

## 4. ROI Baseline / قياس العائد
KPI rows (before vs after, last 30 runs):
| KPI | Before | After | Delta | Method |
|---|---|---|---|---|
| Time per run (min) | n | n | n | timesheet / log |
| Runs per week | n | n | — | calendar |
| Errors per week | n | n | -n | post-review log |
| Hours saved per week | — | n | +n | (before - after) * runs/week |
| Approval-gate fires | n/a | n | — | `event_store` query |
| Audit-log coverage | 0% | 100% | — | event store |
| Annualized SAR saved | — | n | +n | hours/wk * 50 wks * SAR/hr |

## 5. Quality & Compliance / الجودة والامتثال
- Output schema validation (Pydantic) pass rate.
- Forbidden-claims auto-check: 0 violations.
- PII findings auto-redacted: n.
- PDPL Art. 13/14 notices attached where outputs touch external parties.
- Edge cases verified: empty / malformed / missing-field / multilingual.

## 6. Runbook Highlights / أبرز ما في الدليل
- How to run.
- What to monitor (3 alarms).
- Common failure modes + fixes.
- Escalation path.

## 7. 30-Day Adoption Plan / خطة التبني
- Week 1: shadow mode (human reviews every output).
- Week 2-3: spot-check mode (sample 20%).
- Week 4: steady state + KPI review.
- Upsell decision point at Day 30 (see `upsell.md`).

## 8. Risks & Open Items / المخاطر والبنود المفتوحة
- Out-of-scope requests deferred to upsell pathway.
- Any model dependency or vendor risk noted.
- Suggested guardrail upgrades for Phase 2.

## Recommended Visuals
- Before/after bar chart (time per run).
- Pipeline diagram with approval gates.
- Weekly hours-saved trendline (projected).
- Audit-log heatmap (runs x days).

## Cross-links
- Proof pack: `docs/services/ai_quick_win_sprint/proof_pack_template.md`
- Handoff agenda: `docs/services/ai_quick_win_sprint/handoff.md`
- Renewal pathways: `docs/services/ai_quick_win_sprint/upsell.md`
- Approval matrix: `dealix/trust/approval_matrix.py`
- Forbidden claims: `dealix/trust/forbidden_claims.py`
- Operations module: `auto_client_acquisition/business_ops/`
