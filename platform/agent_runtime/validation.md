# Runtime Validation

## Validation Layers

- schema validation
- policy validation
- source/citation validation
- business rule validation
- safety validation

## Required Decision Output

- `valid`: true/false
- `confidence`
- `blockers`
- `requires_approval`
- `recommended_next_step`

## Release Rule

أي workflow أو agent update لا يترقى للإنتاج قبل نجاح validation + eval gates.
