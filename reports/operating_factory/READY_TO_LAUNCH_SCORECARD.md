# Dealix Ready-to-Launch Scorecard

> *Generated: 2026-06-03* · Checklist spec: `docs/operating_factory/READY_TO_LAUNCH_CHECKLIST_AR.md`
> Scoring bands: 90–100 Launch Ready · 75–89 Soft Launch Ready · 60–74 Internal Dry Run · <60 Not Ready

**What this measures:** whether each of the 11 capability areas is *defined, governed,
and executable today* (even if manually). It does **not** claim the volume pipeline is
automated or that every website page is built — see the caveat below.

---

## Scorecard (11 capabilities)

Legend: ✅ Complete (1.0) · 🟡 Partial (0.5) · 🔴 Missing (0.0)

| # | Capability | Docs / Structure | Live / Operational | Score |
|---|-----------|:---------------:|:-----------------:|:-----:|
| 1 | **Website** | ✅ documented | 🟡 landing+pricing+CTAs live; 5 system pages + diagnostic page **not built** | 🟡 0.5 |
| 2 | **Account Intelligence** | ✅ 400-pack structure + Top 100 | 🟡 manual/semi-auto today; full 400/day automation pending | ✅ 1.0 |
| 3 | **Contacts** | ✅ C0–C4 + missing handling + no-invented rule | ✅ enforceable now | ✅ 1.0 |
| 4 | **Emails** | ✅ 6 gates + Quality Score | ✅ draft generator exists; human send | ✅ 1.0 |
| 5 | **Calls** | ✅ Call Brief + outcomes → next action | ✅ enforceable now | ✅ 1.0 |
| 6 | **Mini Proposals** | ✅ Approval Gate | ✅ templates in proposals.json | ✅ 1.0 |
| 7 | **Delivery** | ✅ 5 delivery packs + acceptance/start gates | ✅ P1 delivery SOP exists | ✅ 1.0 |
| 8 | **Finance** | ✅ Cash Priority Score | ✅ unit economics + scorecard exist | ✅ 1.0 |
| 9 | **Founder Command** | ✅ daily command (19:00) | ✅ war_room reports exist | ✅ 1.0 |
| 10 | **Security** | ✅ untrusted-data policy | ✅ governance_check enforces secrets | ✅ 1.0 |
| 11 | **Privacy** | ✅ minimization + suppression/DNC | ✅ do_not_contact.csv live | ✅ 1.0 |

**Raw score:** (10 × 1.0 + 1 × 0.5) / 11 × 100 = **95 / 100** → computed band: **Launch Ready**.

---

## ⚠️ Honest verdict (override): **Soft Launch Ready**

The computed score is 95, but two facts must not be hidden:

1. **Website is only partial.** A public launch needs the 5 per-system pages and a
   diagnostic page; only the landing page, pricing, and CTAs exist today.
2. **Volume/automation is not live.** The 400-packs/day pipeline is *designed and
   governed*, not yet *automated*. Today the loop runs at founder/manual volume.

Because Website is a hard market-facing prerequisite, the **recommended operational
verdict is `Soft Launch Ready` (75–89)**:

```txt
✅ Start now: governed, founder-led, manual-volume outreach using the full loop,
   gates, governance, privacy and security policies — all of which ARE in place.
⏳ Hold full public launch until: (a) 5 system pages + diagnostic page ship,
   and (b) discovery→draft pipeline is automated and quality ≥ 80/100 for 2 weeks.
```

---

## Gaps blocking full "Launch Ready"

| Gap | Owner | Blocks |
|-----|-------|--------|
| Build 5 system pages (`src/pages/`) | Founder + web | Website |
| Build diagnostic page + booking CTA | Founder + web | Website |
| Automate discovery → 400 packs/day | Operator | Account Intelligence (scale) |
| First 2 weeks of live quality data (≥ 80) | Operator | Scale decision (400 → 600) |

---

## What IS ready today

```txt
✅ Full operating loop (daily/weekly/monthly) documented and owned (RACI)
✅ All quality gates (contact/email/call/proposal/delivery/finance)
✅ Governance: human-in-the-loop, no agent sends, no automated calling
✅ Privacy: data minimization, suppression/do-not-contact, client data handling, secrets
✅ Security: external content treated as untrusted data
✅ Finance scoring + existing unit economics
```

---

*Dealix Ready-to-Launch Scorecard | 2026-06-03 | Computed 95 · Verdict: Soft Launch Ready*
