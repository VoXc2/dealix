# Project workbench (per engagement)

Copy this folder to:

```text
clients/<client_slug>/<project_slug>/
```

Then fill in order `00` → `09`. **Governance log** and **QA** are mandatory for internal closure ([`../../docs/company/CLOSED_LOOP_EXECUTION.md`](../../docs/company/CLOSED_LOOP_EXECUTION.md)).

| File | Purpose |
|------|---------|
| `00_intake.md` | Request + classification |
| `01_scope.md` | Binding scope ([`SCOPE_ENGINE`](../../docs/delivery/SCOPE_ENGINE.md)) |
| `02_data_files/` | Symlinks / README only in git; binaries elsewhere |
| `03_delivery_checklist.md` | Execution gates |
| `04_governance_log.md` | Decisions + risk |
| `05_outputs/` | Deliverables index; large files off-repo |
| `06_qa_review.md` | Scored QA |
| `07_proof_pack.md` | Proof Pack 2.0 body |
| `08_client_handoff.md` | Review outcomes + client decision |
| `09_post_project_review.md` | Learning + assets ([`../../projects/_TEMPLATE/POST_PROJECT_REVIEW.md`](../../projects/_TEMPLATE/POST_PROJECT_REVIEW.md)) |

Client-level portal (`clients/<client>/00_scope.md` …) can stay for **account** rhythm; **project** workbench is for each sprint.
