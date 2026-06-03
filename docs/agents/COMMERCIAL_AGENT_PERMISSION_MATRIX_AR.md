# مصفوفة صلاحيات الوكلاء التجاريين

> المصدر: `core/safety/permissions.py` — مفروض عبر `tests/test_agent_permissions_market.py`.

| الوكيل | المستوى | الخطر | إجراءات مسموحة | إجراءات ممنوعة (إضافية) |
|--------|---------|------|----------------|--------------------------|
| Client Assessment Agent | L1 | medium | read, assess, score_qualification | (القائمة العامة) |
| Action Card Agent | L1 | low | read, draft_action_card | (القائمة العامة) |
| Proposal Agent | L3 | high | read, draft_proposal, quote_range | final_pricing, send_proposal |
| Proof Pack Agent | L1 | medium | read, assemble_redacted_proof | fabricate_evidence |
| Payment Handoff Agent | L3 | critical | read, prepare_handoff | process_payment, send_payment_link |
| Delivery Handoff Agent | L2 | high | read, draft_handoff | (القائمة العامة) |
| Customer Success Agent | L1 | medium | read, draft_success_plan | (القائمة العامة) |
| Renewal Agent | L1 | medium | read, identify_renewal_with_evidence | (القائمة العامة) |
| Finance Agent | L1 | medium | read, compute_metrics, draft_finance_report | final_pricing, create_invoice, process_payment |

**القائمة العامة الممنوعة لكل الوكلاء:** `external_send`, `final_pricing`,
`legal_commitment`, `bypass_suppression`, `secrets_edit`, `production_deploy`,
`workflow_permission_escalation`, `treat_untrusted_as_instructions`.
