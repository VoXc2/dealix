# Deployment Architecture

## Environment Model

- development
- staging
- production

## Deployment Requirements

- immutable release versioning
- gated promotion by readiness and eval thresholds
- observability verification post-deploy
- rollback path validated before production promotion

## Gate IDs

- `G-DPL-001`: release gates pass
- `G-DPL-002`: observability checks pass
- `G-DPL-003`: rollback readiness verified
