# Master Code Map (Dealix OS)

Logical layout under `auto_client_acquisition/` and API routers.

```text
auto_client_acquisition/
  data_os/
    schema.py
    import_preview.py
    validators.py
    data_quality_score.py
    dedupe.py
    pii_detection.py
  governance_os/
    policy_check.py
    forbidden_actions.py
    approval_matrix.py
    audit_log.py
    redaction.py
    lawful_basis.py
    rules/
  revenue_os/
    icp_builder.py
    scoring.py
    outreach_drafts.py
    pipeline.py
    revenue_report.py
  customer_os/
    message_classifier.py
    suggested_replies.py
    escalation_rules.py
    support_report.py
  operations_os/
    workflow_builder.py
    approval_flow.py
    sop_builder.py
    ops_dashboard.py
  knowledge_os/
    document_ingestion.py
    retrieval.py
    answer_with_citations.py
    knowledge_eval.py
  reporting_os/
    executive_report.py
    proof_pack.py
    weekly_summary.py
  delivery_os/
    intake.py
    checklist.py
    qa_review.py
    renewal_recommendation.py
  llm_gateway/
    model_catalog.py
    routing_policy.py
    cost_guard.py
    prompt_registry.py
    run_log.py
  ai_workforce/
    agents.py
    orchestrator.py
    compliance_guard.py

api/routers/
  (data / governance / revenue / reporting / delivery / founder — as implemented)
```

The repo may use consolidated modules; this map is the **target decomposition** for scaling the spine.
