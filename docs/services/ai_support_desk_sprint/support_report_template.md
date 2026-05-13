# AI Support Desk Sprint — Weekly Support Report Template / تقرير الدعم الأسبوعي

Bilingual PDF (4–6 pages). Generated every Monday for the prior week's conversations. Owner: customer's support manager; HoCS reviews the first 4 reports during the 14-day retuning window. **No autosend appears anywhere; every dispatch in this report was human-clicked.**

## 1. Period & Scope / الفترة والنطاق
- Week of `<YYYY-MM-DD>` to `<YYYY-MM-DD>`.
- Channels in scope: `<email | whatsapp | web>`.
- Agent roster + shift coverage hours.
- Customer codename + vertical.

## 2. Volume Summary / ملخص الحجم
| KPI | Value | WoW delta | Method |
|---|---|---|---|
| Inbound messages | n | +/- n% | inbox count |
| Distinct customers | n | +/- n | hashed customer_id |
| AR / EN / mixed split | % / % / % | — | language tag |
| Repeat customers | n | +/- n | second-touch within 7d |

Visual: daily volume bar chart, language-split donut.

## 3. Response & Resolution / الاستجابة والحل
| KPI | Value | Target | Method |
|---|---|---|---|
| Median first response time | n min | < 2h business | timestamp delta |
| 90th-percentile first response | n min | < 8h business | percentile |
| Median resolution time | n h | n h | last-message timestamp |
| Reopen rate within 7 days | n% | — | reopen flag |

Visual: response-time histogram, resolution heatmap by category.

## 4. Suggestion Engine Performance / أداء محرك الردود
| KPI | Value | Notes |
|---|---|---|
| Suggestions generated | n | one per inbound |
| Suggestions used as-is | n (%) | agent clicked unchanged |
| Suggestions edited then dispatched | n (%) | human edit |
| Suggestions discarded | n (%) | agent wrote own reply |
| Mean confidence (used drafts) | n | classifier output |
| Forbidden-claim blocks | n | `dealix/trust/forbidden_claims.py` |

Visual: stacked bar (used / edited / discarded), confidence histogram.

## 5. Top Intents / أهم النوايا
| Rank | Intent | Volume | Avg confidence | Notes |
|---|---|---|---|---|
| 1 | `<intent>` | n | n | — |
| ... | ... | ... | ... | ... |

Visual: pareto chart of top 10 intents.

## 6. Escalations / التصعيدات
| Tier | Count | Reason mix | SLA met % |
|---|---|---|---|
| 1 | n | low-conf / repeat | n% |
| 2 | n | refund / complaint | n% |
| 3 | n | regulator / VIP | n% |
| 4 | n | executive | n% |

Visual: stacked bar by tier, SLA-met sparkline.

## 7. Compliance Snapshot / الامتثال
- PDPL Art. 13/14 footer applied: 100% of external dispatches.
- PII surfacing in drafts: 0 (must remain zero).
- Audit-log coverage: 100%.
- Right-to-erasure requests this week: n; resolution time: < 72 hours.
- Autosend events: 0 (must remain zero — MVP rule).

## 8. Insights & Next Actions / رؤى وإجراءات
- Top 3 wins this week.
- Top 3 friction points (suggest a doc/FAQ update or retraining).
- Recommended FAQ additions (link to drafts).
- Suggested classifier tuning (if accuracy < floor).

## 9. Roadmap / خارطة الطريق
- 30-day improvements queue.
- Renewal-pathway preview (see `upsell.md`).

## Recommended Visuals
- Daily volume line + AR/EN split.
- Response-time histogram.
- Suggestion-use stacked bar.
- Pareto of top intents.
- Escalation funnel.

## Cross-links / روابط ذات صلة
- Offer: `docs/services/ai_support_desk_sprint/offer.md`
- Escalation rules: `docs/services/ai_support_desk_sprint/escalation_rules.md`
- Upsell: `docs/services/ai_support_desk_sprint/upsell.md`
- Reply suggestion: `auto_client_acquisition/customer_inbox_v10/reply_suggestion.py`
- Reporting module: `auto_client_acquisition/executive_reporting/`
- Trust pack: `docs/TRUST_AND_COMPLIANCE_BUSINESS_PACK.md`
- CS framework: `docs/customer-success/cs_framework.md`
