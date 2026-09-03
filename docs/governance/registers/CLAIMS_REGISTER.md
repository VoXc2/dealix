# Claims Register / سجل الادّعاءات

**Purpose:** A single, auditable list of external-facing claims Dealix may use,
with the evidence that backs each claim. If a claim is not here with current
verified evidence, it may **not** be used in sales, marketing, the website, or
customer Proof Packs.

**Related:** [`../../37_saudi_layer/FORBIDDEN_ARABIC_CLAIMS.md`](../../37_saudi_layer/FORBIDDEN_ARABIC_CLAIMS.md) ·
[`../APPROVAL_POLICY.md`](../APPROVAL_POLICY.md) ·
[`../../03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md`](../../03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md)

## Rules / القواعد
- **No source → no claim.** Every row needs checkable current evidence.
- A product/process capability claim is not a customer outcome claim.
- No guaranteed-revenue or guaranteed-outcome wording.
- No customer name, result, quote, logo, or case-study reuse without the matching written publication permission.
- No future/unbuilt module described as live.
- Payment, delivery, customer value, and publication permission remain separate truth states.
- Status `verified` is required before a claim is eligible for external use; the exact external action still follows current authority/policy gates.

## Register / السجل
| # | Claim / الادّعاء | Type | Evidence / الدليل | Status | Owner | Last reviewed |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | Dealix defines a governed **30-Day Revenue Command Pilot** with one bounded workflow, baseline, approval path, weekly Proof cadence, final Proof Pack, and Stop/Expand/Redesign review. This is a capability/process claim — not proof of a customer result. | capability | `dealix/config/first_launch_offer_gate.yaml`, `customers/_template/`, `scripts/run_dealix_e2e_dry_run.py` | verified | `dealix-pm` + `dealix-delivery` | 2026-09-03 |
| 2 | Material external actions remain approval/authority-gated and are distinct from internal analysis/drafting. | governance | `docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md`, `data/commercial/governed_channel_runtime_v1.json`, `customers/_template/06_approval_register.md` | verified | `dealix-pm` / Governance OS | 2026-09-03 |
| 3 | Research/public contact data does not itself establish a relationship or consent for outreach. | governance | `data/commercial/governed_channel_runtime_v1.json`, `scripts/verify_governed_channel_runtime_v1.py` | verified | Governance OS | 2026-09-03 |

## Forbidden phrasing / صياغات ممنوعة
- "Guaranteed", "نضمن", "مضمون" tied to revenue or outcomes.
- "Used by <named customer>" or any customer-result statement without current evidence and reuse permission.
- "Live now" for anything not actually deployed and verified on the current production identity.
- Any retired 7-day/fixed-price/automatic-upsell motion as current launch authority.
