# Capital Ledger v2 — درجة الأصل

الـ ledger لا يسجل الأصل فقط — يسجل **جودة الأصل** كدرجة 0–100.

## العوامل

| العامل | نقاط |
|--------|------|
| Reusable | 25 |
| Tied to revenue | 20 |
| Reduces delivery time | 20 |
| Improves trust | 15 |
| Supports productization | 10 |
| Supports market authority | 10 |

## النطاقات

| النتيجة | التصنيف |
|---------|---------|
| 80+ | strategic asset |
| 60–79 | useful asset |
| 40–59 | internal note |
| &lt; 40 | archive |

## مثال JSON

```json
{
  "asset": "B2B Revenue Intelligence Playbook",
  "type": "Knowledge",
  "score": 88,
  "reuse": "all B2B service clients",
  "revenue_link": "Lead Intelligence Sprint",
  "market_use": "content + sales enablement"
}
```

**الكود:** `auto_client_acquisition/enterprise_os/capital_asset_score.py`

**صعود:** [`SOVEREIGN_ENTERPRISE_ARCHITECTURE.md`](SOVEREIGN_ENTERPRISE_ARCHITECTURE.md) · [`STRATEGIC_ASSET_CLASSES.md`](STRATEGIC_ASSET_CLASSES.md)
