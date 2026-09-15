export const clientDeliveryControlSnapshot = {
  generated_at: "pending_exact_head_generation",
  company: "Dealix",
  control_name: "Client Delivery Control",
  delivery_method: "Qualify -> Authorize -> Baseline -> Execute -> Prove -> Decide",
  purpose:
    "turn an approved customer-specific Revenue Command Pilot into bounded delivery with one governed commercial-to-delivery handoff and customer-validated proof",
  verdict: "CLIENT_DELIVERY_RUNTIME_RECEIPT_REQUIRED",
  commercial_account_workspace: "customers/<slug>/",
  delivery_workspace: "clients/<slug>/",
  commercial_handoff: {
    source_of_truth: "customers/<slug>/",
    delivery_target: "clients/<slug>/",
    required_before_delivery_workspace: [
      "qualified_discovery_evidence_ref",
      "approved_scope_ref",
      "approved_named_customer_quote_ref",
      "customer_acceptance_ref",
      "payment_or_documented_start_condition_ref",
      "approved_data_boundary_ref"
    ],
    delivery_evidence_source: "clients/<slug>/05_proof/",
    customer_facing_proof_pack: "customers/<slug>/10_proof_pack.md"
  },
  agent_owners: {
    commercial_handoff: "dealix-sales + dealix-pm",
    delivery: "dealix-delivery",
    engineering_changes: "dealix-engineer",
    executive_command: "dealix-pm",
    permissioned_distribution: "dealix-content"
  },
  stages: [
    {
      name: "Commercial Handoff Gate",
      goal: "accept only a qualified, authorized customer scope with explicit start/data-boundary evidence"
    },
    {
      name: "Baseline & Readiness",
      goal: "capture stakeholders, current state, access, risks, baseline, instrumentation, and acceptance criteria"
    },
    {
      name: "Bounded Workflow Blueprint",
      goal: "design one in-scope workflow without expanding commercial authority"
    },
    {
      name: "Governed 30-Day Delivery",
      goal: "execute with deterministic controls, approval receipts, failure handling, and weekly evidence"
    },
    {
      name: "Weekly Proof & Command",
      goal: "reconcile activity, delivery, outcome, risk, approval, and evidence"
    },
    {
      name: "Final Proof Pack",
      goal: "separate delivery, payment, customer value, and publication permission"
    },
    {
      name: "Stop / Expand / Redesign",
      goal: "make the Day-30 decision from verified evidence; expansion requires a new bounded scope and customer-specific quote"
    }
  ],
  client_files_status: [],
  delivery_guardrails: [
    "no real client delivery workspace without commercial handoff/start evidence",
    "no scope expansion without new acceptance criteria and commercial authority",
    "no material external action without current action-bound authority and channel gates",
    "no delivery claim without delivery evidence",
    "no customer-value claim without customer confirmation",
    "no public reuse without publication permission",
    "no automatic renewal or upsell"
  ],
  next_delivery_actions: [
    "Complete the customers/<slug> commercial packet through approved scope/quote/acceptance/start evidence.",
    "Create clients/<slug> only from that governed handoff.",
    "Let dealix-delivery run the bounded 30-day workflow and capture receipts.",
    "Assemble final customer Proof from verified delivery evidence.",
    "Let dealix-pm choose Stop / Expand / Redesign from the final outcome review."
  ]
} as const;
