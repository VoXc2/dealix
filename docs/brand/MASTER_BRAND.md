# Dealix Group — Master Brand

## Wordmark

`Dealix Group` (capital D, capital G; the word `Group` is non-optional
when referring to the holding parent).

## Tone

- Direct.
- Doctrinal.
- Verifiable.
- Not marketing-led.

We do not use:
- aspirational verbs without a tested control,
- guarantee language,
- "AI-first" / "AI-native" / similar buzzwords as primary frames.

We do use:
- "governed AI operations" (the category we operate in),
- "verifiable, not merely trusted" (the doctrine anchor),
- "cash now, proof always, governance by default" (the operating
  principles).

## Doctrine Anchor

Every Dealix Group public surface MUST display the doctrine version it
adopts. The endorsement line, exact form:

> Doctrine: Governed AI Operations Doctrine vX.Y.Z ·
> `https://dealix.example.com/api/v1/doctrine?version=vX.Y.Z`

## Logo & Color

Use the same color tokens defined in
`partner-kit/branding/COLORS.md`. The master mark is the wordmark in
`--dx-fg` on `--dx-bg`. No alternate logomarks until a Trust Services
or Labs BU is at SCALE and warrants a sub-mark request to the board.

## Forbidden

- The Dealix Group wordmark must not appear next to outcome claims
  unbacked by a Proof Pack.
- The Dealix Group wordmark must not appear on partner-led surfaces
  as a primary mark (only as secondary; see partner-kit logo usage).
- The Dealix Group wordmark may not be used to imply regulatory
  certification.

## Verification

- `tests/test_brand_architecture_doctrine_endorsement.py` ensures the
  endorsement line appears on every Dealix Group public surface.
- `tests/test_no_forbidden_features_in_diff.py` (PR4) blocks any
  product code that ships outcome-guarantee language.
