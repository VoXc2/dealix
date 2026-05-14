# Sub-Brand Rules — Dealix Group

Each operating BU is a sub-brand. The Charter (PR10) is the brand's
foundation; this document is the brand contract every sub-brand must
honor.

## The Four Sub-Brand Commitments

1. **Doctrine pinning.** The BU charter records the doctrine version it
   adopts. The BU's public surfaces show that version explicitly.

2. **Trust Pack publication.** Before any external claim or invoice,
   the BU publishes a Trust Pack from
   `partner-kit/TRUST_PACK_TEMPLATE.md`, with the BU's name + charter
   filled in.

3. **Group endorsement line.** Every BU public page includes the
   single line: "Operating BU of Dealix Group · Doctrine vX.Y.Z" with
   a link to `/api/v1/doctrine?version=vX.Y.Z`.

4. **No carve-outs.** A BU cannot adopt a weaker version of any
   non-negotiable. The BU may add stricter rules; never weaker.

## Sub-Brand Lifecycle States (mirrors `UnitPortfolioDecision`)

| State    | Public visibility                                    |
|----------|------------------------------------------------------|
| `BUILD`  | Internal-facing; can appear on Group landing.        |
| `PILOT`  | Can publish a draft Trust Pack; no public claims.    |
| `SCALE`  | Full public surface; eligible for case studies.      |
| `HOLD`   | Removed from Group landing; no new claims published. |
| `KILL`   | Removed from Group landing; archive page only.       |
| `SPINOUT`| Brand transitions out of Dealix Group ownership.     |

## Naming Pattern

`Dealix <Function>` — exactly. Examples:

- `Dealix Core OS` (operating spine).
- `Dealix Sprint Delivery` (productized delivery).
- `Dealix Trust Services` (audit / evidence).
- `Dealix Labs` (research / ventures).
- `Dealix Academy` (training / certification).

Forbidden patterns:
- Fanciful one-word names (e.g., "Dealix Spark").
- Geographic suffixes ("Dealix KSA"). The doctrine is country-aware
  but the sub-brand identity is not.
- Year suffixes ("Dealix 2026"). The doctrine version anchor handles
  time.

## Approval Workflow

1. Founder drafts the BU charter (`docs/holding/units/<slug>.md`).
2. `python scripts/register_business_unit.py --really-this-is-a-bu …`.
3. Validate via `python scripts/validate_business_units.py`.
4. Update `landing/group.html` to surface the new sub-brand (the
   listing test in PR13 will block CI if you forget).

## Suspension

Same rules as the partner suspension policy
(`docs/40_partners/PARTNER_SUSPENSION_POLICY.md`):
- A non-negotiable violation suspends the sub-brand.
- A suspended sub-brand is hidden from `landing/group.html`.
- Reinstatement requires a board memo.
