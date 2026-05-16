# Commercial Freeze | تجميد لصالح السوق

**Status:** ACTIVE
**Started:** 2026-05-16
**Scope (amended 2026-05-16):** the freeze applies to **rungs 3–5** of the offer
ladder (Managed Ops, Command Center, Partner OS). The rung 0–1 *delivery finish*
is explicitly permitted — see "Allowed" below.
**Exit condition:** first paid pilot delivered + customer-approved Proof Pack (L3+).

---

## Why | لماذا

The platform is shipped and verified. The constraint on revenue is no longer
code — it is **founder-led selling**. Every hour spent building instead of
selling now has negative expected value. This freeze redirects all effort from
*building* to *operating and selling*, until the first paid pilot proves the
motion.

المنصة جاهزة ومُتحقَّق منها. القيد على الإيراد لم يَعُد الكود — بل **البيع
بقيادة المؤسس**. هذا التجميد يحوّل كل الجهد من *البناء* إلى *التشغيل والبيع*،
حتى يُثبت أول Pilot مدفوع أن الحركة تعمل.

## Scope of the freeze | نطاق التجميد

The freeze covers **rungs 2–5** of the offer ladder. Rungs 3–5 (Managed Ops,
Command Center, Partner OS) are *marketed* but today delivered as
founder-assisted tooling, not fully managed services. Rung 2 (the 1,500 SAR
Data-to-Revenue Pack) is also frozen — it received **no** delivery-finish
exception, so no new build for it ships during the freeze. No new automation
for rungs 2–5 ships until real pilot demand unlocks it
(`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`).

The freeze does **not** cover the **rung 0–1 delivery finish**: the minimum work
needed for the Free Diagnostic (rung 0) and the 499 SAR 7-Day Revenue Proof
Sprint (rung 1) to ship a real, customer-facing rendered deliverable. That work
is in service of *delivering the first paid pilot* — which is the freeze's own
exit condition — so it is permitted and scoped tightly (no rung 3–5 capability).

## Frozen — do NOT do during the freeze | مُجمَّد

- ❌ No new feature PRs for **rungs 2–5**.
- ❌ No new product/architecture docs.
- ❌ No Board OS v2, no new `*_os` modules unrelated to rung 0–1 delivery.
- ❌ No new API routers or endpoints for **rungs 2–5**.
- ❌ No frontend redesign or polish.
- ❌ No new dashboards.

## Allowed — the only work that ships | مسموح

- ✅ Founder-led selling: warm-list outreach, partner follow-ups, meetings.
- ✅ Market-motion artifacts (the founder's sales tools — see
  `docs/sales-kit/`).
- ✅ **Rung 0–1 delivery finish**: customer-facing rendered (HTML/PDF) Proof Pack
  and Diagnostic report, the payment→delivery audit link, and the doctrine
  hotfixes that support them. Minimum scope only — no rung 3–5 capability.
- ✅ Delivery of a signed pilot + Proof Pack assembly.
- ✅ Production hotfixes and CI hygiene only (P0/P1 — broken build, broken gate,
  security/doctrine).
- ✅ Recording to the ledgers (`docs/ledgers/`).

## Build-on-demand exception | استثناء البناء عند الطلب

A new asset is built **only** when a real market signal asks for it — governed
by [`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md).
No signal → no build.

## Exit | الخروج من التجميد

The freeze ends when **one paid pilot is delivered and its Proof Pack is
customer-approved (evidence level L3 or above)**. At that point the warm-list
motion has been proven, and the next 90-day plan
([`docs/90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md))
governs what unlocks.
