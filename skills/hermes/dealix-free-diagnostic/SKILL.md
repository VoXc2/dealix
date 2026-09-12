---
name: dealix-free-diagnostic
description: Run the Dealix universal free diagnostic (D0-D2 free, Arabic-first, ESTIMATED-only numbers) for one commercial surface and return evidence-bound next steps. Internal and read-only: never sends, never charges, never publishes.
---

# Dealix Free Diagnostic (D0-D2 free)

## Scope

- D0 signal scan, D1 rapid and D2 functional are genuinely free: no card, no urgency, no fake ROI.
- Every number is `PATTERN`, `ESTIMATED` or `UNKNOWN`. `ESTIMATED` always carries a basis; otherwise it stays `UNKNOWN`.
- Never send, charge, publish or create a binding commitment from this skill.

## Commands

```bash
REPO="${DEALIX_REPO:-/opt/dealix/workspace/dealix}"
PY="$REPO/.venv/bin/python"; [ -x "$PY" ] || PY=python3

"$PY" "$REPO/scripts/verify_universal_diagnostic_acceptance.py"
```

One commercial surface (example: clinics):

```bash
"$PY" -c "import sys; sys.path.insert(0,'$REPO'); from dealix.commercial.universal_diagnostic_factory import UniversalDiagnosticFactory, DiagnosticDepth as D; f=UniversalDiagnosticFactory(); s,fams=f.compose_for_surface('clinics', buyer_role='coo', problem='support_backlog', depth=D.D1_RAPID); q=f.generate_questions(fams[0], locale='ar'); print('sector=', s.canonical_sector if s else 'UNKNOWN'); print('families=', [x.family_id for x in fams]); print('q1=', q[0]['question_text'])"
```

Surface coverage check (31 surfaces):

```bash
"$PY" -c "import sys; sys.path.insert(0,'$REPO'); from dealix.commercial.universal_diagnostic_factory import SECTOR_SURFACES; print(len(SECTOR_SURFACES), sorted(s.surface_id for s in SECTOR_SURFACES))"
```

## Output contract

- Language: Arabic first, English parity.
- Numbers: `truth_class` in `{PATTERN, ESTIMATED, UNKNOWN}`; `is_measured_fact` is `false` for estimates.
- Next step: `discovery` only when evidence exists; otherwise `signal_scan`.
- Pricing: `price_sar=0` and `pricing_basis=free_d0_d2` for D0-D2. Deeper work is `quote_required_after_qualified_discovery` and is never invented here.

## Forbidden

- External send, charging, publishing, production mutation, or presenting estimates as measured facts.
