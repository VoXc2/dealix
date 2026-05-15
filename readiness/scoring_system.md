# Readiness Scoring System — نظام تسجيل الجاهزية

**EN.** Every layer is scored 0–100 across the eight components from
[`enterprise_readiness_model.md`](enterprise_readiness_model.md). The score
produces one of three decisions, reusing the repo's existing convention:
`PASS / FIX / BLOCKED`.

**AR.** تُسجَّل كل طبقة من 0 إلى 100 عبر المكوّنات الثمانية. تُنتج النتيجة قرارًا
من ثلاثة، باستخدام اصطلاح المستودع القائم: `PASS / FIX / BLOCKED`.

---

## 1. The eight components — المكوّنات الثمانية

Each component is worth **12.5 points**. Sum = 100.

| # | Component | 0 (absent) | 6 (partial) | 12.5 (real) |
|---|-----------|-----------|-------------|-------------|
| 1 | Code | No working impl, or only a stub / unused `_v*` fork. | Works but fragile, undocumented, or duplicated. | Single canonical impl, used in production paths. |
| 2 | Tests | No tests. | Some tests; breakage not caught. | Tests fail when behaviour breaks; cover the golden path + edges. |
| 3 | Evals | No eval pack. | Eval pack exists, no threshold or not run. | Eval pack with threshold, run on change. |
| 4 | Observability | No traces/metrics/logs. | Logs only, no `trace_id`. | `trace_id` on every action; metrics + logs queryable. |
| 5 | Governance | No policy/approval/audit. | Policy OR audit, not both. | Risk → policy → approval → audit on every action. |
| 6 | Rollback | No rollback path. | Documented, never drilled. | Documented **and** drilled within 90 days. |
| 7 | Metrics | No operational numbers. | Numbers exist, not monitored. | Live, monitored, with alert thresholds. |
| 8 | Business Impact | No measured outcome. | Anecdotal / projected only. | Measured outcome a customer pays for. |

Partial scores between 0, 6, and 12.5 are allowed (e.g. 9) when the evidence
sits between two columns. **Always cite the evidence** (file path, test name,
eval file) next to the score — a score without evidence is invalid.

---

## 2. The decision — القرار الثلاثي

| Score | Decision | Meaning |
|-------|----------|---------|
| **≥ 85** | `PASS` | The layer is real. Build on it. Sell it. |
| **70–84** | `FIX` | Close the named gaps, then re-score. Beta only — no full sale. |
| **< 70** | `BLOCKED` | Do not sell, do not build on top. Remove the blockers first. |

This mirrors `docs/readiness/` Gate decisions and the `DEALIX_READY_FOR_SALES`
output of `scripts/verify_dealix_ready.py`.

---

## 3. Hard fails — الإخفاقات القاطعة

Some gaps cap the score regardless of the other components. If any hard fail is
true, the layer is **`BLOCKED`** even if the arithmetic says otherwise:

- Any cross-tenant data leak path (Layer 2).
- Any high-risk action that can execute without approval (Layer 7).
- Any retrieval that ignores user permission or tenant scope (Layer 6).
- Any release path with no rollback (Layer 5 / `rollback.md`).
- Any of the 11 non-negotiables (`docs/00_foundation/NON_NEGOTIABLES.md`)
  reachable in code — scraping, cold WhatsApp, fake proof, PII in logs,
  external action without approval.

A hard fail is a **`BLOCKED`** verdict and a same-week fix item — not a "FIX".

---

## 4. How to score a layer — كيفية تسجيل طبقة

1. Open the layer in [`gap_analysis.md`](gap_analysis.md).
2. For each of the 8 components, find the **evidence** (code path, test, eval).
3. Assign 0 / 6 / 12.5 (or an in-between value) and write the evidence beside it.
4. Sum to 0–100.
5. Apply the hard-fail check (§3). If any is true → `BLOCKED`.
6. Otherwise map the score to `PASS / FIX / BLOCKED` (§2).
7. List the **residual gaps** — the specific, named work to raise the score.

Re-score whenever the layer changes, and at every release gate.

---

## 5. Layer roll-up — تجميع الطبقات

A release passes only when **every layer it depends on** is `PASS`. One `FIX`
layer makes the release a `FIX` (beta); one `BLOCKED` layer makes the release
`BLOCKED`. The weakest layer sets the ceiling — readiness does not average away
a blocker.

---

## ملخص بالعربية

كل طبقة تُسجَّل من 100 عبر ثمانية مكوّنات (12.5 لكل منها). النتيجة ≥ 85 = PASS،
و70–84 = FIX، وأقل من 70 = BLOCKED. هناك إخفاقات قاطعة (تسريب بيانات، إجراء
عالي الخطورة بلا موافقة، استرجاع يتجاوز الصلاحيات، مسار إصدار بلا تراجع، أي
انتهاك لغير القابلة للتفاوض) تجعل الطبقة BLOCKED مهما كان المجموع. الإصدار لا
ينجح إلا إذا كانت كل طبقاته PASS — أضعف طبقة تحدّد السقف.
