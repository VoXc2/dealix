export const serviceOsSnapshot = {
  summary: {
    rcmax_ready: true,
    auto14_ready: true,
    client_ops_ready: true,
    conversation_ready: true,
    strategy_ready: true,
    service_os_ready: true,
    live_sends: 0,
    final_commitments: 0,
    daily_delivery_items: 7,
    approval_gates: 6,
    weekly_review: 1,
    proof_report: 1,
    renewal_plan: 1
  },
  offers: [
    {
      name: 'Revenue Command Room OS',
      scopeAuthority: 'Customer-specific scope after the Free Diagnostic and qualified discovery.',
      commercialAuthority: 'Timeline, price, and acceptance criteria are customer-specific and require an approved quote.',
      outcome: 'Daily revenue actions, follow-up queue, proposal queue, and proof report.'
    },
    {
      name: 'Client Service OS',
      scopeAuthority: 'Customer-specific scope after the Free Diagnostic and qualified discovery.',
      commercialAuthority: 'Timeline, price, and acceptance criteria are customer-specific and require an approved quote.',
      outcome: 'Client intake, workflow diagnosis, owner map, daily delivery, weekly proof, and renewal path.'
    },
    {
      name: 'AI Trust & Safety OS',
      scopeAuthority: 'Customer-specific scope after the Free Diagnostic and qualified discovery.',
      commercialAuthority: 'Timeline, price, and acceptance criteria are customer-specific and require an approved quote.',
      outcome: 'Approval gates, safe AI policy, no fake claims, and external action review.'
    }
  ],
  clientGets: [
    'clear view of missed opportunities',
    'owner map',
    'action queue',
    'follow-up drafts',
    'proof report',
    'weekly review',
    'next action plan'
  ],
  approvalGates: [
    'external sharing',
    'final quote',
    'contracts',
    'terms',
    'result claims',
    'live outbound'
  ],
  operatingFlow: ['intake', 'diagnosis', 'queue', 'drafts', 'proof', 'weekly review', 'renewal'],
  mode: 'approval_first'
} as const;
