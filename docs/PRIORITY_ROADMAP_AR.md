# خارطة الأولويات — PRIORITY_ROADMAP_AR

> **أول 90 يوماً** بعد الموجة 29-33. مجمّعة في 4 buckets: NOW (week 1)، NEXT (week 2-4)، LATER (month 2-3)، DEFERRED (Q2+). كل بند له مالك + success criteria + blocker.
>
> **آخر تحديث:** 2026-06-03 — المالك: Founder — الإصدار: v1.0

---

## 1) NOW — Week 1 (Days 1-7)

> **7 launch blockers حرجة.** كلها قرارات بشرية.

| # | البند | المالك | Success Criteria | Blocker |
|---|-------|--------|------------------|---------|
| N1 | تأكيد 6 pricing bands | Founder | PR في `OFFER_*_PAGE_AR.md` و `OFFER_LADDER_AR.md` | Founder availability |
| N2 | Tier-1 actual list (3 شركات) | Founder + Sales Lead | 3 rows real في `data/enterprise_sales/accounts.jsonl` | Sales Lead input |
| N3 | Calendly URL + WhatsApp | Founder | PR في `OFFER_CTA_LIBRARY_AR.md` | Founder phone number |
| N4 | اقرأ FOUNDER_START_HERE + INDEX | Founder | checkbox | time |
| N5 | شغّل company_ready_verify | Founder | `VERDICT=PASS` | nothing |
| N6 | Approval routing (نائب) | Founder | PR في `AGENT_PERMISSION_LIFECYCLE_AR.md` | Sales Lead agreement |
| N7 | A5 policy clarification | Founder | PR في `AI_AGENT_GOVERNANCE_OS_AR.md` | — |

---

## 2) NEXT — Week 2-4 (Days 8-30)

| # | البند | المالك | Success Criteria | Blocker |
|---|-------|--------|------------------|---------|
| X1 | أول outreach لـ 3 Tier-1 | Sales Lead | ≥ 3 stakeholders حقيقيين | N2 |
| X2 | أول pilot proposal | Sales Lead | signed MAP في `mutual_action_plans.jsonl` | N1 |
| X3 | Founder review لـ FULL_REVENUE_OS | Founder | status → READY | N1 |
| X4 | Founder review لـ MONTHLY_OPTIMIZATION | Founder | status → READY | N1 |
| X5 | أول Agent Eval weekly (7 وكلاء) | AI Governance Lead | rows in `agent_evals.jsonl` | N6 |
| X6 | أول incident logged (إن حصل) | AI Governance Lead | row in `agent_incidents.jsonl` | — |
| X7 | أول proof pack | Delivery Lead | `proofs/dealix_v1_proof_pack.json` exists | X2 |
| X8 | تحديث `sector_benchmarks.jsonl` مع observed | Data Lead | ≥ 1 new row | X2 |
| X9 | أول Monday weekly meeting | Founder | minutes في `docs/meetings/` | N4 |
| X10 | إصلاح 2 broken links | Agent 35 follow-up | 1 PR | — |

---

## 3) LATER — Month 2-3 (Days 31-90)

| # | البند | المالك | Success Criteria | Blocker |
|---|-------|--------|------------------|---------|
| L1 | ترقية 3 KPIs من `observed` → `measured` | Data Lead | rows in `sector_benchmarks.jsonl` بـ `evidence_level=measured` | أول pilot delivered |
| L2 | تحويل ABM list إلى 10 Tier-1 + 20 Tier-2 | Sales Lead | 30 rows in `accounts.jsonl` | N2 |
| L3 | أول expansion path closed (multi-dept) | Sales Lead | rows in `mutual_action_plans.jsonl` stage 2+ | X2 |
| L4 | إضافة 2 agents جدد (after-validation) | AI Governance Lead | rows in `agent_registry.jsonl` بـ `evidence_level=validated` | N6 |
| L5 | أول quarterly review | Founder | board memo في `reports/company_os/board_memo_<Q>.md` | month 3 |
| L6 | أول MRR > 50K SAR | Founder | accounting close | N1 + N2 + X2 |
| L7 | تحسين `OFFER_FAQ_LIBRARY_AR.md` مع real data | Marketing | ≥ 30% rows updated | X7 |
| L8 | Saudi-specific sector benchmarks | Data Lead | ≥ 5 sectors with KSA data | X2 |
| L9 | Schema v2 design (breaking change opt-in) | Engineer | RFC in `docs/transformation/rfcs/` | — |
| L10 | CI check لـ broken links | Engineer | GitHub Action created | — |

---

## 4) DEFERRED — Q2+ (After Day 90)

| # | البند | المالك | السبب | متى نعيد التقييم |
|---|-------|--------|-------|----------------|
| D1 | Multi-region expansion (UAE, Egypt) | Founder | After MRR > 200K SAR | Q2 end |
| D2 | Custom industry LLM fine-tuning | Engineer | After ≥ 10K observations | Q3 |
| D3 | Multi-tenant theming | Engineer | After ≥ 5 accounts | Q2 |
| D4 | Partner portal self-serve | Partnerships Lead | After ≥ 3 active partners | Q3 |
| D5 | Marketplace (third-party offers) | Founder | After retention > 90% | Q4 |
| D6 | Public API for Dealix OS | Engineer | After documentation stable | Q3 |
| D7 | Arabic NLP-specific features | Engineer | After observed Arabic data > 50K rows | Q3 |
| D8 | M&A / venture factory | Founder | After $1M+ ARR | Q4+ |

---

## 5) Success Criteria الإجمالية (90 يوماً)

| المؤشر | Goal |
|--------|------|
| Tier-1 accounts with stakeholders | ≥ 10 |
| Active pipelines (signed MAP) | ≥ 3 |
| Agents registered & evaluated | ≥ 10 |
| Incidents closed in 24h | 100% of P0/P1 |
| Sector benchmarks `measured` | ≥ 3 |
| Proof packs published | ≥ 5 |
| Pricing bands confirmed | 6/6 |
| Launch blockers cleared | 7/7 |

---

## 6) Risk-adjusted Plan

| Scenario | Trigger | Pivot |
|---------|---------|-------|
| **Best case** | N1-N7 all cleared by Day 7 | Execute NEXT on schedule |
| **Realistic** | 5/7 cleared by Day 7 | Delay NEXT by 1 week |
| **Worst case** | < 5/7 cleared by Day 14 | Pivot to "manual sales" mode, no ABM |

---

## 7) See Also

- [`FOUNDER_START_HERE_AR.md`](FOUNDER_START_HERE_AR.md)
- [`DAILY_OPERATING_GUIDE_AR.md`](DAILY_OPERATING_GUIDE_AR.md)
- [`WEEKLY_OPERATING_GUIDE_AR.md`](WEEKLY_OPERATING_GUIDE_AR.md)
- [`DEALIX_COMPANY_OS_INDEX_AR.md`](DEALIX_COMPANY_OS_INDEX_AR.md)
- [`FILE_OWNERSHIP_MAP.md`](FILE_OWNERSHIP_MAP.md)
- `reports/final/FOUNDER_FINAL_READINESS_REPORT.md`

---

## Open Questions for Founder

1. هل 90 يوماً هو الـ horizon الصحيح، أم تريد 60 أو 120 يوماً؟
2. أي من بنود DEFERRED تستحق **إعادة تقييم مبكرة** (Q1+)؟
3. هل توافق على **Realistic scenario** كـ baseline (5/7 launch blockers cleared)؟
