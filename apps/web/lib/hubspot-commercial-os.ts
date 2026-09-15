export const hubspotTargetGroups = [
  {
    name: "Clinics and Healthcare Operations Targets",
    industry: "HOSPITAL_HEALTH_CARE",
    sector: "clinics",
    offer: "Follow-up Recovery OS",
    pain: "missed booking and patient follow-up discipline",
  },
  {
    name: "Saudi Real Estate Automation Targets",
    industry: "REAL_ESTATE",
    sector: "real_estate",
    offer: "Revenue Command Room OS",
    pain: "lead leakage and proposal follow-up",
  },
  {
    name: "Logistics and Delivery Operations Targets",
    industry: "LOGISTICS_AND_SUPPLY_CHAIN",
    sector: "logistics",
    offer: "Revenue Command Room OS",
    pain: "B2B proposal tracking and account ownership",
  },
  {
    name: "Training Centers Automation Targets",
    industry: "PROFESSIONAL_TRAINING_COACHING",
    sector: "training_centers",
    offer: "Follow-up Recovery OS",
    pain: "registration follow-up and cohort pipeline visibility",
  },
  {
    name: "B2B Services and Agencies Targets",
    industry: "MANAGEMENT_CONSULTING",
    sector: "b2b_services",
    offer: "Revenue Command Room OS",
    pain: "pipeline visibility and daily commercial next action",
  },
  {
    name: "Retail and Ecommerce Automation Targets",
    industry: "RETAIL",
    sector: "retail_ecommerce",
    offer: "Customer Follow-up and Recovery OS",
    pain: "abandoned cart, support queue, and repeat purchase follow-up",
  },
  {
    name: "Construction and PMO Targets",
    industry: "CONSTRUCTION",
    sector: "construction_pmo",
    offer: "Client Delivery OS",
    pain: "project visibility, approvals, and proof of work",
  },
  {
    name: "Government Contractor Operations Targets",
    industry: "GOVERNMENT_RELATIONS",
    sector: "government_contractors",
    offer: "AI Trust and Governance OS",
    pain: "controlled documentation, proposal discipline, and approvals",
  },
];

export const hubspotLaunchTasks = [
  "Build HubSpot CRM OS delivery checklist",
  "Prepare Private Company Brain proof bundle",
  "Build Revenue Operations OS proposal",
  "Package Dealix Lead Engine offer",
  "Review weekly revenue dashboard",
];

export const hubspotServiceCatalog = [
  ["Revenue Command Room Sprint", "Customer-specific quote", "scope/terms after qualified discovery"],
  ["Company Brain Sprint", "Customer-specific quote", "scope/terms after qualified discovery"],
  ["Follow-up Recovery Sprint", "Customer-specific quote", "scope/terms after qualified discovery"],
  ["AI Sales Agent Setup", "Customer-specific quote", "scope/terms after qualified discovery"],
  ["AI Trust and Governance OS", "Customer-specific quote", "scope/terms after qualified discovery"],
  ["Client Delivery OS", "Customer-specific quote", "scope/terms after qualified discovery"],
];

export const hubspotCommercialPayload = {
  mode: "read_only_proposal",
  crmRole: "source_of_truth",
  dealixRole: "intelligence_scoring_drafting_negotiation_command_center",
  targetGroups: hubspotTargetGroups,
  launchTasks: hubspotLaunchTasks,
  serviceCatalog: hubspotServiceCatalog,
  writeBackStages: [
    "read_only_intelligence",
    "proposed_write_back",
    "confirmed_tasks_and_notes",
    "confirmed_deals_and_pipeline",
    "controlled_communication_queue",
  ],
};
