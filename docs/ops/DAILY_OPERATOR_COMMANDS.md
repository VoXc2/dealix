# Daily Operator Commands (Dealix)

## الأهم: مشغّل يومي واحد
```bash
python3 scripts/dealix_daily_operator.py --mode demo
```

## يولّد
- scored_leads.json
- outreach_review_queue.json
- prospect pack
- follow-up queue
- proposal
- CEO brief
- pipeline report

## ملفات المخرجات
- `business/_data/`
- `business/crm/exports/`
- `business/proposals/generated/`
- `business/reports/exports/`

## الأوامر اليدوية

### اعتماد مسوّدة
```bash
python3 scripts/approve_outreach_draft.py --draft-id <id> --reviewer Sami
```

### رفض مسوّدة
```bash
python3 scripts/reject_outreach_draft.py --draft-id <id> --reviewer Sami --reason "..."
```

### توليد عرض
```bash
python3 scripts/generate_proposal.py --account-id <id> --offer "Revenue OS" --lang both --timeline "21 days"
```

### فحص الإنتاج
```bash
python3 scripts/production_readiness_check.py
```

### حارس الدفع
```bash
python3 scripts/pre_push_guard.py
```
