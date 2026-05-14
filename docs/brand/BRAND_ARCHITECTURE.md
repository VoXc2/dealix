# Dealix Group — Brand Architecture

> Pinned to doctrine version: `v1.0.0`.
> Machine-readable: every active / piloted / building BU must appear in
> `data/business_units.json` (PR10) and in `landing/group.html`.

## Hierarchy

```
Dealix Group  (holding parent — never sold to)
├── Dealix Core OS              ← BU: active product (status: BUILD)
├── Dealix Sprint Delivery      ← BU: planned (not registered yet)
├── Dealix Trust Services       ← BU: planned
├── Dealix Labs                 ← BU: planned (gated on first SCALE BU)
└── Dealix Academy              ← BU: planned (gated on ≥ 2 sector pilots)
```

The parent brand is **Dealix Group**. The operating BUs use the
`Dealix <Function>` pattern. A BU's brand authority is its **charter**
registered under `data/business_units.json`.

## Naming Rules

1. Every BU name starts with `Dealix`.
2. The second word is the **function** (Core OS, Sprint Delivery,
   Trust Services, Labs, Academy). No fanciful names.
3. No BU is publicly used before its registry entry exists with a
   `BUILD`, `PILOT`, `SCALE`, or `SPINOUT` status.
4. A BU whose status is `HOLD` or `KILL` does NOT appear on the
   public Group landing.
5. The `Dealix Group` mark may never appear without a doctrine version
   anchor (see Logo Usage rules in `partner-kit/branding/LOGO_USAGE.md`).

## Color Tokens

The same tokens used for the partner kit and the Founder Command
Center: `--dx-fg`, `--dx-bg`, `--dx-pass`, `--dx-warn`, `--dx-fail`,
`--dx-accent`, `--dx-card`, `--dx-border`. See
`partner-kit/branding/COLORS.md` for the canonical values.

## Sub-Brand Contract

Every sub-brand (operating BU) commits to:

1. **Doctrine pinning.** The BU charter records the doctrine version
   the BU adopts. Bumps follow `open-doctrine/VERSIONS.md`.
2. **Trust Pack publication.** Before any external claim, the BU
   publishes its Trust Pack from
   `partner-kit/TRUST_PACK_TEMPLATE.md`.
3. **Group endorsement line.** Every public surface (page, deck,
   proposal, slide) includes one explicit line linking back to
   `Dealix Group` and the published doctrine version.
4. **No carve-outs.** A sub-brand cannot adopt a weaker version of any
   non-negotiable.

## Verification

- `tests/test_brand_architecture_lists_all_active_units.py` — every
  BU in `data/business_units.json` with status in
  `{BUILD, PILOT, SCALE, SPINOUT}` is listed in `landing/group.html`.
- `tests/test_brand_architecture_doctrine_endorsement.py` — every
  Dealix Group public surface page includes the doctrine endorsement
  line (links to `/api/v1/doctrine?version=`).

## Branding for External Co-Sell

Partner-level branding (third parties co-selling under Dealix)
continues to follow `partner-kit/branding/LOGO_USAGE.md`. This
document concerns **internal** sub-brands (BUs we operate), not
external partners.
