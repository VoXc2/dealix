# Clients directory — onboarding + delivery “portal” (Markdown-first)

Per client, create a folder:

```text
clients/<client_slug>/
  00_scope.md
  01_intake.md
  02_data_request.md
  03_delivery_checklist.md
  04_qa_review.md
  05_report.md
  06_proof_pack.md
  07_next_steps.md
  DELIVERY_COMMAND.md
  governance_events.md
  delivery_approval.md
  EXPANSION_MAP.md
  CAPABILITY_ROADMAP.md
  CAPABILITY_BACKLOG.md
  CAPABILITY_SCORECARD.md
  OPERATING_CADENCE.md
  VALUE_DASHBOARD.md
  AI_OPERATING_MODEL.md
```

## Bootstrap

Copy everything from `_TEMPLATE/` and rename nothing (numbers keep sorting stable).

## Per-project workbench (each sprint / engagement)

For **closed-loop execution** and auditability, also use:

```text
clients/<client_slug>/<project_slug>/
```

Templates: [`_PROJECT_WORKBENCH/README.md`](_PROJECT_WORKBENCH/README.md).

## Governance

Highly sensitive client data may stay on Drive/Notion — keep **stubs + links** here if this repo is shared.
