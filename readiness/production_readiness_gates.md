# Production Readiness Gates

## Mandatory gates
1. `python3 -m compileall api auto_client_acquisition`
2. `python3 -c "from api.main import app; print('api import ok')"`
3. `ruff check api auto_client_acquisition tests`
4. Targeted enterprise control-plane test bundle.
5. `bash scripts/revenue_os_master_verify.sh`

## Gate policy
- Any failed gate blocks release.
- PARTIAL verdict is not release-ready.
- High-risk endpoints must remain approval-gated.
