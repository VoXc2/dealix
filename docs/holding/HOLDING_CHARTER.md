# Dealix Group — Holding Charter

> Pinned to doctrine version: see `/api/v1/doctrine`.
> Snapshot rendered at: `landing/assets/data/holding-portfolio.json`.

## What Dealix Group Is

**Dealix Group** is the holding parent of `Dealix Core OS` and any
future operating business units. Its sole job is to **compose, govern,
and verify** the operating units below it.

It is **not**:

- a separate brand competing with its own BUs,
- a SaaS marketplace,
- a venture studio that ships before proof,
- a multi-jurisdiction shell.

## Four Operating Principles

1. **Cash now.** Every BU has a path to invoice within 90 days of
   registration. No "burn first, monetize later".
2. **Proof always.** Every BU publishes a Proof Pack before any
   commercial claim and a Trust Pack before its first invoice.
3. **Governance by default.** Every BU adopts the same eleven
   non-negotiables (`open-doctrine/11_NON_NEGOTIABLES.md`). No
   BU-specific carve-outs.
4. **Productize repetition.** What the founder does three times is a
   playbook. What the playbook does three times is a product. What the
   product does in three sectors is a BU.

## The Four Holding-Level Non-Negotiables

1. **Zero unverifiable units.** A BU that is not registered in
   `data/business_units.json` with a charter, owner, and status from
   the published enum does not exist for capital-allocation purposes.
2. **Doctrine version pinning.** Every BU pins to a published doctrine
   version. Doctrine bumps are coordinated at the group level (see
   `open-doctrine/VERSIONS.md`).
3. **Every BU publishes a Trust Pack** from the partner-kit template
   before any external claim is made on its behalf.
4. **No BU is killed quietly.** A KILL decision requires a board memo
   stored under `data/_state/bu_memos/` and a final Capital Asset entry
   summarizing what is salvaged for the rest of the group.

## Operating Sequence

The 13-step holding sequence
(`auto_client_acquisition/dominance_os/holding_sequence.py`) governs
maturity. Wave 22 ships the registry, surfaces, and lifecycle artifacts
that let the sequence be measured end-to-end.

## Charter Authority

This charter is doctrine, not legal text. Any legal entity formation,
shareholder agreement, or jurisdictional structure is downstream of
this charter and must adopt its principles or refuse to operate under
the Dealix Group name.

## How To Add A BU

1. Draft the charter.
2. Run `python scripts/register_business_unit.py --really-this-is-a-bu \
        --slug <slug> --name <name> --owner <handle> --status <enum> \
        --kpi <kpi>`
3. Run `python scripts/validate_business_units.py` — exit 0 required.
4. Publish the BU's Trust Pack from `partner-kit/TRUST_PACK_TEMPLATE.md`.
5. Cross-link the BU into `docs/holding/BUSINESS_UNIT_REGISTRY.md`.

## How To Kill A BU

1. Draft a decision memo with
   `python scripts/draft_bu_decision_memo.py --unit <slug>` (PR14).
2. Board reviews the memo.
3. Update the BU status to `KILL` via the same `register_business_unit.py`
   CLI (with `--reason <one-line>`).
4. Register a final Capital Asset summarizing salvageable assets.

## Charter Version

`v1.0.0` — initial. Future revisions bumped per the same semver rules
as `open-doctrine/VERSIONS.md`.
