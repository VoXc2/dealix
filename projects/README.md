# Projects directory

Store **per-engagement** artifacts that are not only client-facing portal files.

Suggested layout:

```text
projects/<client_slug>/<project_slug>/
  POST_PROJECT_REVIEW.md
```

## Rules

- **Copy** `_TEMPLATE/POST_PROJECT_REVIEW.md` at kickoff and **finish** it before internal closure.
- Slug names: lowercase, ASCII, hyphens (e.g. `acme-corp`, `lead-intel-sprint-2026-q2`).

## Relation to `clients/`

- `clients/` = day-to-day operating folder for one client.
- `projects/` = learning + retrospective home for a specific engagement (can nest multiple projects per client over time).

## Privacy

If repo is shared, keep identifiable data **out of git**; use Drive/Notion with links here instead.
