# Doctrine Versions

Append-only changelog. Every public Dealix claim should reference a
specific version. The companion JSON
(`open-doctrine/doctrine_versions.json`) is the machine-readable mirror.

| Version    | Commit SHA  | Date         | Summary                                                                                  | Signed by  |
|-----------:|:-----------:|:-------------|:-----------------------------------------------------------------------------------------|:-----------|
| `v1.0.0`   | *initial*   | 2026-05-14   | Initial open doctrine: 11 non-negotiables + control mapping + README.                    | Founder    |

Bumping rules:
- **patch** (`vX.Y.Z+1`): wording fixes that don't change a commitment.
- **minor** (`vX.Y+1.0`): added clarifying commitment or new control.
- **major** (`vX+1.0.0`): removed or modified an existing commitment.

A major bump requires explicit founder approval and is documented in
the corresponding commit message (`feat(doctrine): vN.0.0 — ...`).

Endpoints:

```
GET /api/v1/doctrine/versions          → list every published version
GET /api/v1/doctrine?version=v1.0.0    → pinned snapshot at that version
GET /api/v1/doctrine                   → current HEAD snapshot
```
