# Capital Ledger — سجل الأصول الرأسمالية

> Purpose: define the asset taxonomy that turns every Dealix project into reusable capital, the constitutional rule that every project must deposit at least one asset, the weekly review cadence, and the Wave-1 contract that wires capital deposit into Proof Pack assembly.

Dealix sells projects, but Dealix is *not* a project-shop. The difference is the Capital Ledger. Every project, regardless of size or outcome, must deposit at least one reusable asset into the ledger. Over time, the ledger becomes the company's compounding moat — the reason a third sprint is faster, cheaper, and stronger than the first.

## Asset taxonomy — تصنيف الأصول

The ledger accepts exactly six asset types:

```
scoring_rule          — a ranking or scoring component proven on real data
draft_template        — a bilingual draft pattern proven to pass governance
governance_rule       — a runtime governance rule (new pattern, new redaction, new block)
proof_example         — a reusable evidence pattern (how to structure a section in the Proof Pack)
sector_insight        — a structured insight about a sector (signals, decision criteria, language)
productization_signal — evidence that a one-off step should become a productized capability
```

Asset record shape:

```json
{
  "asset_id": "cap_<ulid>",
  "asset_type": "scoring_rule | draft_template | governance_rule | proof_example | sector_insight | productization_signal",
  "title": "short human-readable name",
  "summary": "1-3 sentences",
  "origin_project_id": "proj_<ulid>",
  "origin_proof_pack_ref": "proof_<ulid>",
  "source_refs": ["src_<ulid>", "..."],
  "sector": "string | null",
  "language": "ar | en | bilingual",
  "reuse_count": 0,
  "created_at": "<iso8601>"
}
```

Each asset must carry at least one `source_ref` back to a Source Passport. See [SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md). Asset content that references client data must respect the passport's `external_use_allowed` flag.

## The "every project produces ≥ 1 asset" rule

This is a constitutional non-negotiable. See [NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md), rule 11.

A project that produces zero capital is not a project that "didn't have anything reusable to share". It is a productization failure: either the work was not abstracted, or the work was too similar to a previous project to deserve a new asset (in which case the prior asset's `reuse_count` should increment). Either way, the close path is the same: assemble cannot complete without an asset.

The rule is enforced at the assembly boundary:

- `proof_os.proof_pack.assemble()` calls `capital_os.capital_ledger.add_asset(...)` at least once.
- If the project produced no abstractable asset, the project owner must register a `productization_signal` describing why — for the weekly capital review to address.

## Capital review cadence — وتيرة المراجعة

The Capital Ledger is reviewed **weekly**. The review covers:

- New deposits since the last review (count by `asset_type`, sector breakdown).
- `reuse_count` deltas — which assets compounded.
- Productization signals — which one-off steps appeared more than once and should become productized.
- Stale assets — assets with `reuse_count = 0` over a long window. Either the asset is too narrow (retire), or the team is not retrieving it (improve discovery).

The review output feeds two places:

- The **company operating cadence** — what to build, what to retire, what to harden.
- The **service ladder** — which patterns are mature enough to become new productized offers. See [COMPANY_SERVICE_LADDER.md](../COMPANY_SERVICE_LADDER.md).

## The Wave-1 contract — العقد التقني للموجة الأولى

The Wave-1 contract wires Proof Pack assembly to Capital Ledger deposit. The contract is:

```python
# In proof_os.proof_pack.assemble()

def assemble(project_state) -> ProofPack:
    pack = render_sections(project_state)
    pack.score = compute_proof_score(pack)
    pack.tier  = classify_tier(pack.score)

    # Constitutional rule: at least one capital asset per project.
    assets = derive_assets(project_state)
    if not assets:
        raise CapitalAssetMissing(
            "No project may close without at least one capital asset."
        )

    for asset in assets:
        capital_os.capital_ledger.add_asset(asset)

    pack.section_13_capital_assets_created = [a.asset_id for a in assets]
    return pack
```

`capital_ledger.add_asset(...)` performs:

- Schema validation (the six allowed `asset_type` values, required fields).
- Source reference validation (at least one valid `source_ref`).
- Duplicate detection (near-identical assets increment `reuse_count` on the prior asset instead of creating a new record).
- Append-only write — the ledger is not retro-edited; corrections are new records that supersede old ones.

The contract is one-directional: Proof Pack assembly *calls* the ledger; the ledger does not call back into proof assembly. This keeps the dependency clean and avoids cycles.

## What does not belong in the ledger — ما لا يدخل

- Raw client data of any kind.
- One-off configuration values that are not abstractable.
- Marketing copy. Marketing copy may be *derived* from a `draft_template` asset, but the marketing copy itself is not the asset.
- Prompts copied verbatim from a single project. A prompt becomes a `draft_template` only after it has been generalized.

## Why the ledger is the moat — لماذا الأصول هي الميزة

A lead-gen agency restarts every month at zero. An AI consultant ships a deck and walks away. A SaaS vendor sells a generic feature set.

Dealix differs because every project leaves capital behind: a sharper scoring rule, a tested draft pattern, a new governance rule, a new sector insight. The third sprint in a sector is materially better than the first because it inherits the prior two sprints' assets. That compounding is what makes "Governed AI Operations" defensible as a category.

## Cross-references

- [Proof Pack Standard](../07_proof_os/PROOF_PACK_STANDARD.md) — section 13 lists assets created.
- [Non-Negotiables](../00_constitution/NON_NEGOTIABLES.md) — rule 11.
- [Source Passport](../04_data_os/SOURCE_PASSPORT.md) — every asset references at least one passport.
