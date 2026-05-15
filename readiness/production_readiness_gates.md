# Production Readiness Gates

Release blocks unless all checks pass:

1. `python3 -m compileall api auto_client_acquisition`
2. `python3 -c "from api.main import app; print('api import ok')"`
3. `ruff check api auto_client_acquisition tests`
4. Targeted enterprise control-plane tests
5. `bash scripts/revenue_os_master_verify.sh`

If a gate fails, release is blocked until fixed or explicitly waived.
