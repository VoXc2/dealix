# Commercial Freeze | تجميد لصالح السوق

**Status:** ACTIVE
**Started:** 2026-05-16
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

## Frozen — do NOT do during the freeze | مُجمَّد

- ❌ No new feature PRs.
- ❌ No new product/architecture docs.
- ❌ No Board OS v2, no new `*_os` modules.
- ❌ No new API routers or endpoints.
- ❌ No frontend redesign or polish.
- ❌ No new dashboards.

## Allowed — the only work that ships | مسموح

- ✅ Founder-led selling: warm-list outreach, partner follow-ups, meetings.
- ✅ Market-motion artifacts (the founder's sales tools — see
  `docs/sales-kit/`).
- ✅ Delivery of a signed pilot + Proof Pack assembly.
- ✅ Production hotfixes and CI hygiene only (P0/P1 — broken build, broken gate,
  security).
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
