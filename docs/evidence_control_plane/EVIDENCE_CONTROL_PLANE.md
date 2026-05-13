# Dealix Enterprise Evidence Control Plane

> Dealix is the operating layer that **records, governs, links, and explains** every meaningful AI-assisted action across data, agents, workflows, approvals, proof, and value.

Layer 28 consolidated doctrine. Typed surfaces in `auto_client_acquisition/evidence_control_plane_os/`.

## 1. The seven questions every action must answer

What data? Who used it? Which policy was checked? What decision? Who reviewed/approved? What output? What proof of value or blocked risk?

## 2. Evidence layers (10)

Source, Input, Policy, AI Run, Human Review, Approval, Output, Proof, Value, Risk, Decision.

## 3. Evidence Graph

Nodes: Client, Project, Source, Dataset, Agent, AI Run, Policy Check, Governance Decision, Human Review, Approval, Output, Proof Event, Value Event, Risk Event, Decision.

Edges connect them so the system can reconstruct the entire chain from source to value.

## 4. Evidence Object — canonical shape

See `evidence_control_plane_os.evidence_object.EvidenceObject`. ID, type, client/project, actor (type + id), human owner, source IDs, linked artifacts, summary, confidence, timestamp.

## 5. Maturity Levels (0–5)

- L0 No Evidence — forbidden for Dealix.
- L1 Basic Logs — internal MVP.
- L2 Governance Evidence — real MVP.
- L3 Approval + Proof Evidence — retainers.
- L4 Enterprise Evidence Control Plane — enterprise.
- L5 Continuous Trust OS — future state.

## 6. Evidence Dashboard

Evidence Coverage, Source Passport Coverage, AI Run Ledger Coverage, Policy Check Coverage, Human Review Coverage, Approval Linkage, Proof Linkage, Value Linkage, Risk Events, Open Evidence Gaps.

Thresholds: <70% fragile, 70–84 internal-only, 85–94 client-ready, 95–100 enterprise-ready.

## 7. Evidence Gap Rules

Source gap → block AI use. Policy gap → block client delivery. Approval gap → incident. Proof gap → remove claim. Value gap → no retainer push. Agent gap → no production use.

## 8. Evidence-to-Sales

> We do not ask you to trust black-box AI. Dealix shows the evidence: source, policy decision, approval, audit trail, proof, and value.

## 9. Evidence-to-Proof Pack

Proof Pack v3 sections: Executive Summary, Problem, Source Evidence, AI Run Evidence, Governance Evidence, Human Review Evidence, Output Evidence, Value Evidence, Blocked Risk Evidence, Limitations, Recommended Next Action.

## 10. Evidence-to-Accountability

Output fields: generated_by, reviewed_by, approved_by, governance_owner, final_accountability. Rule: no owner = no execution; no approval owner = no external action.

## 11. Evidence-to-Risk

Every gap is a risk signal at low/medium/high/critical severity, each with a defined response.

## 12. Evidence-to-Productization

Repeated source-passport flows → Source Passport Panel. Repeated governance decisions → Governance Runtime UI. Repeated approvals → Approval Center. Repeated proof events → Proof Timeline. Repeated value events → Value Dashboard. Repeated risk events → Risk Dashboard.

## 13. Internal API

```
POST /evidence/source
POST /evidence/ai-run
POST /evidence/policy-check
POST /evidence/review
POST /evidence/approval
POST /evidence/output
POST /evidence/proof
POST /evidence/value
GET  /evidence/graph/{project_id}
GET  /evidence/gaps/{client_id}
```

Design it now; build it when Dealix needs it.

## 14. Human-Amplified Evidence

> AI contributed. Human reviewed. Human approved. System logged. Proof validated.

## 15. Saudi Evidence Layer

Arabic executive evidence summaries; explicit "no external sending by Dealix"; bilingual audit reports; PDPL-aware framing.

## 16. The closing sentence

> Dealix wins when it becomes the **Evidence Control Plane** — selling not AI outputs but the ability to see, understand, review, prove, and hold accountable every AI action inside a company.
