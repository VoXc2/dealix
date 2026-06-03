# OpenAPI Baseline Policy

Dealix uses `scripts/export_openapi.py` and `scripts/check_openapi_contract.py` to keep the API contract reviewable.

## Current mode

CI exports the current FastAPI OpenAPI schema and checks it against `docs/architecture/openapi.json` when that baseline exists.

If `docs/architecture/openapi.json` does not exist, the contract checker still verifies that the schema exports successfully and asks maintainers to create the baseline.

## Creating or updating the baseline

Run:

```bash
make openapi-export
```

Then review the generated file before committing it.

## Review rule

Commit `docs/architecture/openapi.json` only when:

- The API is production-ready enough to freeze a baseline.
- Breaking changes are intentionally reviewed.
- Frontend/client usage has been updated.
- Release notes mention customer-visible API changes.

## Breaking changes to review

- Removed path.
- Removed method.
- Removed response field used by clients.
- Changed required request field.
- Changed authentication behavior.
- Changed success status code.

## Arabic summary

OpenAPI baseline يحول تغييرات الـ API من تعديل غير مرئي إلى عقد قابل للمراجعة. لا تثبت baseline إلا بعد التأكد أن الـ API جاهز كعقد إنتاجي.
