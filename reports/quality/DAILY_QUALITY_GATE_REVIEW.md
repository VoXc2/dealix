# Daily Quality Gate Review — مراجعة بوابة الجودة اليومية
*Date: 2026-06-03 | Batch: 18 drafts | Daily target: 400*

---

## 1. Score Model (out of 100)

| Criterion | Max |
|-----------|----:|
| Personalization | 25 |
| Pain clarity | 20 |
| System fit | 20 |
| CTA clarity | 15 |
| Risk safety | 10 |
| Tone quality | 10 |

Bands: `<65 rejected` · `65–74 needs_rewrite` · `75–84 approval_queue` · `85+ top_priority`

---

## 2. Batch Status

| Status | Count | % |
|--------|------:|--:|
| 🟢 top_priority (85+) | 4 | 22% |
| 🟡 approval_queue (75–84) | 3 | 17% |
| 🟠 needs_rewrite (65–74) | 1 | 6% |
| 🔴 rejected (<65 or gate fail) | 10 | 56% |

> 400 Draft status: scored **18** of a **400/day** target.

---

## 3. Top 100 Approval Queue (7)

Inclusion requires: score ≥ 75 · recommended_system · Client Need Card · risk ≠ high · evidence_level · CTA.

| # | Company | System | Score | Band | Evidence |
|--:|---------|--------|------:|------|----------|
| 1 | FleetCo Logistics | نظام تشغيل الإيرادات | 90 | top_priority | L4 |
| 2 | Digital Rise Agency | نظام تشغيل الإيرادات | 88 | top_priority | L2 |
| 3 | Growth Labs SA | نظام استرجاع المتابعات | 86 | top_priority | L3 |
| 4 | MediClinic Group | نظام عملاء واتساب | 85 | top_priority | L3 |
| 5 | EduPro Academy | نظام استرجاع المتابعات | 82 | approval_queue | L2 |
| 6 | TrainMe KSA | نظام عملاء واتساب | 80 | approval_queue | L2 |
| 7 | Vision Consulting | نظام القيادة التنفيذية | 78 | approval_queue | L2 |

---

## 4. Rejections by Reason

| Reason | Count |
|--------|------:|
| no_cta | 1 |
| guaranteed_claim | 1 |
| fake_re_fwd | 1 |
| no_need_card | 1 |
| no_recommended_system | 1 |
| internal_module_name_leaked | 1 |
| unverified_pain_as_fact | 1 |
| suppression_hit | 1 |
| prompt_injection_in_source | 1 |

---

## 5. Full Batch

| Draft | Company | System | Score | Status | Gate reasons |
|-------|---------|--------|------:|--------|--------------|
| DRAFT-0001 | Digital Rise Agency | نظام تشغيل الإيرادات | 88 | 🟢 top_priority | — |
| DRAFT-0002 | Growth Labs SA | نظام استرجاع المتابعات | 86 | 🟢 top_priority | — |
| DRAFT-0003 | TrainMe KSA | نظام عملاء واتساب | 80 | 🟡 approval_queue | — |
| DRAFT-0004 | Vision Consulting | نظام القيادة التنفيذية | 78 | 🟡 approval_queue | — |
| DRAFT-0005 | BuildRight Web | نظام العروض والإثبات | 72 | 🟠 needs_rewrite | — |
| DRAFT-0006 | Generic Co | نظام تشغيل الإيرادات | 58 | 🔴 rejected | — |
| DRAFT-0007 | NoCTA Trading | نظام استرجاع المتابعات | 71 | 🔴 rejected | no_cta |
| DRAFT-0008 | GuaranteeMax Agency | نظام تشغيل الإيرادات | 78 | 🔴 rejected | guaranteed_claim |
| DRAFT-0009 | ReplyChase Co | نظام استرجاع المتابعات | 80 | 🔴 rejected | fake_re_fwd |
| DRAFT-0010 | NoCard Ventures | نظام القيادة التنفيذية | 77 | 🔴 rejected | no_need_card |
| DRAFT-0011 | Unrouted LLC | — | 59 | 🔴 rejected | no_recommended_system |
| DRAFT-0012 | LeakName Agency | نظام استرجاع المتابعات | 81 | 🔴 rejected | internal_module_name_leaked |
| DRAFT-0013 | AssumePain Clinic | نظام عملاء واتساب | 75 | 🔴 rejected | unverified_pain_as_fact |
| DRAFT-0014 | Old Client Holding | نظام تشغيل الإيرادات | 81 | 🔴 rejected | suppression_hit |
| DRAFT-0015 | Injected Corp | نظام العروض والإثبات | 82 | 🔴 rejected | prompt_injection_in_source |
| DRAFT-0016 | FleetCo Logistics | نظام تشغيل الإيرادات | 90 | 🟢 top_priority | — |
| DRAFT-0017 | EduPro Academy | نظام استرجاع المتابعات | 82 | 🟡 approval_queue | — |
| DRAFT-0018 | MediClinic Group | نظام عملاء واتساب | 85 | 🟢 top_priority | — |

---

*Generated: 2026-06-03 | npm run commercial:quality*
