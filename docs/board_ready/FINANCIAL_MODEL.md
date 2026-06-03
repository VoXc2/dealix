# Financial Model — Board

نموذج مالي مبسّط على **5 خطوط دخل**.

## Revenue lines

1. Diagnostics  
2. Sprints  
3. Retainers  
4. Platform / Workspace (لاحقًا)  
5. Academy / Partners (لاحقًا)  

## Unit economics (لكل عرض)

price · delivery hours · AI cost · gross margin · proof strength · retainer conversion · reuse assets created.

## مثال هيكلي

```text
Revenue Intelligence Sprint:
Price: X
Delivery hours: Y
AI cost: Z
Gross margin: target 65%+
Proof output: Revenue Proof Pack
Retainer path: Monthly RevOps OS
Product signal: account_scoring + proof_pack_generator
```

## قاعدة المجلس

```text
لا توسع عرضًا gross margin فيه ضعيف، proof ضعيف، أو scope creep عالي.
```

**الكود:** `revenue_line_ok_for_scale` — `board_ready_os/financial_model.py`

**صعود:** [`PRICING_POWER_SYSTEM.md`](PRICING_POWER_SYSTEM.md) · [`BOARD_DASHBOARD.md`](BOARD_DASHBOARD.md)
