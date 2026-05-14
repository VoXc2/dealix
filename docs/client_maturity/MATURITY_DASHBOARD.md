# Maturity Dashboard

لوحة لكل عميل تجمع **الحقيقة التشغيلية**: مستوى السلم، الدرجة، العوائق، العرض التالي، الممنوعات، وإشارات **سحب المنصة** (Platform pull).

## الحقول (تطابق `MaturityDashboardView`)

| الحقل | المصدر |
|--------|--------|
| `current_level` / `target_level` | محرك النضج + اختيار يدوي للهدف |
| `maturity_score` / `maturity_band` | `client_maturity_score` + `client_maturity_band` |
| `proof_score` / `adoption_score` | مدخلات العميل (عتبات retainer) |
| `governance_score` | `dimensions.governance_coverage` |
| `readiness_blockers` | `derive_readiness_blockers` — أبعاد تحت عتبة + shadow + owner |
| `recommended_next_offer` / `blocked_offers` / `reason` | `maturity_engine_result` |
| `platform_pull_signals` | يُمرَّر من التشغيل (أو CRM) — مرجع slugs أدناه |

## إشارات سحب المنصة (مرجعية)

الثوابت البرمجية: `PLATFORM_PULL_SIGNALS` في `maturity_dashboard.py`:

- `multiple_users_need_access`  
- `approvals_repeat`  
- `proof_reports_repeat`  
- `executive_dashboard_request`  
- `audit_requested`  

## مثال قرار (مرجعي)

```json
{
  "client": "Client A",
  "current_level": 4,
  "target_level": 5,
  "maturity_score": 78,
  "maturity_band": "retainer_workspace_ready",
  "proof_score": 82,
  "adoption_score": 72,
  "governance_score": 80,
  "readiness_blockers": [],
  "next_offer": "Client Workspace + Proof Timeline + Value Dashboard + Approval Center",
  "blocked": ["AI Control Plane"],
  "platform_pull_signals": ["approvals_repeat", "proof_reports_repeat"],
  "reason": "Governed workflow in place; scale with monthly operating cadence and proof discipline."
}
```

## الكود

`auto_client_acquisition/client_maturity_os/maturity_dashboard.py`
