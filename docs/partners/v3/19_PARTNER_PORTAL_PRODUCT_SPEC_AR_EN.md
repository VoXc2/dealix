# Dealix Partner Portal V3 — Product Spec AR/EN

## Product promise
A mobile-first Arabic/English partner workspace that shows exactly what the partner may do, what Dealix has accepted, what opportunity is attributed, what commission state exists, and what remains blocked.

## Primary navigation
1. Home / الرئيسية
2. Application & Eligibility / الطلب والأهلية
3. Learn & Certify / التدريب والاعتماد
4. Register a Deal / تسجيل فرصة
5. My Pipeline / فرصي
6. Commissions / العمولات
7. Assets / المواد المعتمدة
8. Disputes / الاعتراضات
9. Policies & Receipts / السياسات والإيصالات
10. Support / الدعم

## Home state cards
- Legal classification status.
- Terms policy version accepted.
- Certification state.
- Active/hold state with reason.
- Accepted deal registrations.
- NCCR/commission truth state.
- Clearing days remaining.
- Disputes requiring action.
- Compliance notices.

## Commission truth UI
Use explicit states only:
`REGISTERED → ACCEPTED_ATTRIBUTION → QUALIFIED → WON_NOT_PAID → COLLECTED → COMMISSION_ELIGIBLE → CLEARED → APPROVED_FOR_PAYMENT → STAGED_NOT_PAID → PAID_VERIFIED`.

The portal must visually separate projected, eligible, clearing, staged and paid amounts. `STAGED_NOT_PAID` must never render as “Paid”.

## Deal registration UX
Required: company, sector, relationship evidence, problem signal, consent state, government/tender flag, source, contributor roles and idempotency key.
Result: immutable registration receipt with accepted/rejected/duplicate/hold status, attribution window and policy version.

## Rights & disputes
Partner can open a dispute against attribution, NCCR, commission calculation or payout status. Every dispute records evidence, owner, SLA, resolution and immutable resolution receipt. Policy changes apply prospectively unless explicitly agreed otherwise.

## Mobile/RTL/accessibility
- Arabic RTL first-class, English LTR parity.
- WCAG 2.2 AA target.
- 44px minimum touch targets.
- No meaning conveyed by color alone.
- Full keyboard navigation for desktop.
- Optimistic UI prohibited for economic truth mutations.
- Every mutation returns an auditable receipt ID.

## Authority boundaries
Portal may submit applications, evidence, deal registrations, content drafts and disputes. It may display commission calculations and payout state. It cannot sign contracts for Dealix, set customer pricing, execute a payout, mark bank settlement true, publish content or bypass B2G/legal holds.

## Analytics
North Star: `VERIFIED_PARTNER_SOURCED_ECONOMIC_MOVEMENT`.
Supporting metrics: activation rate, time-to-first-accepted-deal, time-to-first-collected-cash, NCCR, conversion by sector/source, compliance incident rate, dispute rate, retention/expansion contribution and founder minutes per verified movement.

Clicks, impressions, signups and raw referrals remain diagnostic funnel metrics only.