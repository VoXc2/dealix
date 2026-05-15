# Workflow OS — العمليات والتسليم

## الهدف في المخطط

`workflow_os/` — في الريبو موزّع بين **تسليم الخدمة** وسجلات **سير عمل المنتج** والمشغل الشخصي.

## Workflow Object (مرجعي)

```json
{
  "workflow_id": "WF-001",
  "name": "Sales follow-up review",
  "owner": "Sales Manager",
  "inputs": ["ranked_accounts", "draft_pack"],
  "ai_assisted_steps": ["draft_email", "summarize_account"],
  "approval_required": true,
  "proof_metric": "follow_up_clarity",
  "cadence": "weekly"
}
```

## قواعد التشغيل

- لا سير عمل بلا **مالك**.
- لا retainer بلا **cadence**.
- لا cadence بلا **مقياس إثبات** (proof metric).

## التنفيذ في الريبو

- `auto_client_acquisition/delivery_os/` — إطار تسليم، تسليم يد، جاهزية، QA.
- `docs/product/WORKFLOW_REGISTRY.md`, `docs/product/WORKFLOW_RUNTIME_DESIGN.md`
- تشغيل المشغل: `auto_client_acquisition/personal_operator/`

## روابط

- [GOVERNANCE_OS.md](GOVERNANCE_OS.md) — [PROOF_OS.md](PROOF_OS.md)
