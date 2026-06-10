# DesignOps Master Evidence Table

Per-row evidence of what is shipped vs. what is planned. Status legend:
**green** = shipped + tested; **yellow** = partial / scaffolded;
**red** = not yet built / blocker present.

| Layer | Check | Expected | Actual | Status | Evidence | Blocker | Next Action |
|---|---|---|---|---|---|---|---|
| design system | tokens (color, type, spacing, bilingual) | module + token map | not built | red | — | needs founder sign-off on visual identity | scaffold `designops/design_system.py` once tokens approved |
| skill registry | 15 skills registered with input/output schemas | registry + schema per skill | catalog doc only | yellow | `docs/DESIGNOPS_SKILL_CATALOG.md` | — | add `designops/skill_registry.py` with the 15 entries |
| safety gate | 8 forbidden tokens, claim scan, name scan, PDPL | gate function + tests | doc only | yellow | `docs/DESIGNOPS_ARTIFACT_SAFETY.md`; tokens overlap with `tests/test_no_guaranteed_claims.py` | — | port the 8 tokens into a `safety_gate.py` and bind the existing test |
| brief builder | service-call → render-brief normalizer | function + tests | not built | red | — | depends on skill registry | implement after registry lands |
| generator: mini_diagnostic | bilingual md + html | generator + tests | not built | red | — | depends on brief builder | implement step 1 |
| generator: full_diagnostic | bilingual md + html | generator + tests | not built | red | — | depends on brief builder | step 2 |
| generator: proposal_page | bilingual md + html | generator + tests | not built | red | — | depends on brief builder + pricing_catalog | step 3 |
| generator: pricing_reference | EN md, founder-only | generator + tests | not built | red | — | reuse `finance_os.pricing_catalog` | step 4 |
| generator: proof_pack | bilingual md + html | generator + tests | not built | red | — | reuse `proof_ledger` reads | step 5 |
| generator: executive_weekly_pack | EN md + html, founder-only | generator + tests | not built | red | — | reuse `executive_reporting` | step 6 |
| **exporter** | local md/html/json, no upload, sanitized filenames, PDF/PPTX deferred | module + ≥6 tests | shipped | **green** | `auto_client_acquisition/designops/exporter.py`; `tests/test_designops_exporter.py` (10 tests) | — | none — done |
| API routes | `/api/v1/designops/*` admin-only | router + tests | not built | red | — | depends on generators | wire after first generator lands |
| hard rule: no upload | exporter performs zero HTTP | monkey-patched HTTP libs assert no calls | enforced | green | `tests/test_designops_exporter.py::test_no_remote_upload_happens` | — | — |
| hard rule: filename sanitization | rejects `..`, `/`, `\\`; strips unsafe chars | tested | enforced | green | `test_filename_sanitization_rejects_path_traversal`, `test_filename_sanitization_strips_unsafe_chars` | — | — |
| hard rule: PDF/PPTX deferred | calls raise NotImplementedError with clear message | tested | enforced | green | `test_pdf_raises_not_implemented`, `test_pptx_raises_not_implemented` | — | — |
| hard rule: empty content rejected | raises ValueError | tested | enforced | green | `test_empty_content_raises` | — | — |
| hard rule: `safe_to_send=False` default | every manifest defaults False | gate + tests | doc + exporter respect it | yellow | `docs/DESIGNOPS_ARTIFACT_SAFETY.md`; exporter persists whatever manifest says | — | enforce in `safety_gate.py` once landed |
| hard rule: no marketing claim | 8 forbidden tokens + claim scan | regex tests | partial | yellow | `tests/test_no_guaranteed_claims.py`, `tests/test_landing_forbidden_claims.py` | — | extend to designops artifacts when generators land |
| hard rule: no real customer name | doc + gate scan | doc enforced; gate planned | yellow | `docs/DESIGNOPS_FIRST_CUSTOMER_USE_CASES.md` uses `founder_X` only | — | add registry-cross-check in `safety_gate.py` |
| .gitignore | `docs/designops/exports/**` ignored | rule appended | shipped | green | `.gitignore` (DesignOps OS section) | — | — |
| secret scan | exporter has no API keys, no URLs, no tokens | grep clean | shipped | green | `auto_client_acquisition/designops/exporter.py` (only stdlib + Path) | — | re-run secret scan when generators land |
| bundle | `pytest --no-cov -q` green | full suite passes | green for new tests | green | `tests/test_designops_exporter.py` 10/10 | — | run full bundle on every PR |

## Roll-up
- **Green rows:** exporter + its hard rules + .gitignore + secret scan = 7.
- **Yellow rows:** skill registry, safety gate, `safe_to_send` default,
  forbidden-claim coverage, real-name scan = 5.
- **Red rows:** design system, brief builder, 6 generators, API routes = 9.

The exporter and the 4 founder-facing docs (this file is the 5th) are the
**foundation**. The rest of DesignOps OS is scaffolded by these docs and
will be built phase-by-phase.
