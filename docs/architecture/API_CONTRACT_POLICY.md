# Dealix API Contract Policy

This policy defines how Dealix treats API changes.

## Contract source

The FastAPI OpenAPI schema is the API contract source.

Export it with:

```bash
make openapi-export
```

The export utility is:

```bash
python scripts/export_openapi.py --output docs/architecture/openapi.json
```

## Breaking changes

The following are breaking changes for public or customer-facing endpoints:

- Removing an endpoint.
- Removing a response field used by clients.
- Renaming a field.
- Changing required request fields.
- Changing authentication requirements without a migration path.
- Changing status codes for successful flows.

## Non-breaking changes

The following are usually non-breaking:

- Adding optional request fields.
- Adding response fields.
- Adding new endpoints.
- Improving descriptions, examples, or tags.

## Required review

For any API change:

1. Run `make openapi-export`.
2. Mention changed routes in the PR.
3. Update client or frontend usage when needed.
4. Update docs and examples.
5. Add migration notes for breaking changes.

## Current automation

CI runs an OpenAPI export smoke check. A future improvement should compare the exported schema against a committed baseline and fail on unreviewed breaking changes.
