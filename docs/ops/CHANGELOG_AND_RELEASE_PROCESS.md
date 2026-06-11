# Changelog & Release Process (Dealix)

## Changelog
- See `CHANGELOG.md` at repo root
- One entry per release
- Format: ### V{major}.{minor} — {date}

## Release process
1. Open a release branch
2. Run all checks (`dealix_v10_run_all.sh`)
3. Generate release notes (`scripts/generate_release_notes.py`)
4. Tag the commit
5. Push the tag
6. PR to main

## Pre-release checklist
- [ ] All checks pass
- [ ] No secrets
- [ ] CHANGELOG updated
- [ ] Demo data still marked
- [ ] Documentation updated
