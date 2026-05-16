# Production Readiness Gates

1. `python -m compileall api auto_client_acquisition`
2. `python -c "from api.main import app; print('api import ok')"`
3. `ruff check api auto_client_acquisition tests`
4. Enterprise control-plane tests pass (10 targeted files)
5. Revenue OS master verify passes
6. Script prints `ENTERPRISE CONTROL PLANE: PASS`

If any gate fails, release is blocked.
