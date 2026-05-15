# Definition of Done (Dealix)

Three gates: **service**, **project**, **feature**. All must be checkable — not “felt.”

See also: [`DEALIX_STANDARD.md`](DEALIX_STANDARD.md), [`docs/audit/AUDIT_STANDARD.md`](../audit/AUDIT_STANDARD.md).

---

## Service Definition of Done

A service is **done** (sellable / ready for repeatable delivery) when:

- **Offer** exists (`docs/services/<service>/offer.md` or equivalent)
- **Scope** exists and matches registry (`SERVICE_REGISTRY.md`)
- **Intake** exists (template or service-specific)
- **Delivery checklist** exists
- **QA** checklist exists and is used
- **Demo** exists where required by stage gates (`demos/` or `docs/assets/demos/`)
- **Proof pack** template exists for the service (`verify_proof_pack.py` must pass)
- **Sales** narrative / objection notes aligned (`docs/sales/`)
- **Governance** checks documented (forbidden actions, approval matrix)
- **Acceptance** / verification: `scripts/verify_service_files.py` + readiness score per policy

---

## Project Definition of Done

A **client project** is **done** when:

- Client **deliverables** are delivered and acknowledged
- **QA** passed (`clients/<client>/delivery_approval.md` + score threshold per policy)
- **Governance** passed (no unresolved high-risk items without sign-off)
- **Proof pack** delivered (`06_proof_pack.md` + any annexes)
- **Review call** completed; feedback captured
- **Next step** proposed (`07_next_steps.md`)
- **Post-project review** completed (`projects/<client>/<project>/POST_PROJECT_REVIEW.md`)
- **Internal assets** updated where applicable (`docs/assets/`, `docs/playbooks/`, `FEATURE_CANDIDATE_LOG.md`)

---

## Feature Definition of Done

A **product feature** is **done** when:

- **Implemented** behind the right module boundary
- **Tested** (unit or integration per risk)
- **Documented** (README, operator note, or API doc as appropriate)
- **Error handling** for known failure modes
- **Audit logging** if the feature touches approvals, PII, or external channels
- **Supports at least one** service path in `SERVICE_REGISTRY` / capability matrix
- **Reduces delivery time or risk** (or documents why it is strategic infrastructure)

---

## Operational note

If DoD is met but **Dealix Standard** item is missing, treat as **needs improvement** in audit — see `docs/audit/CLIENT_PROJECT_AUDIT.md`.
