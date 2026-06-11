# Risk and Mitigation (Dealix)

| Risk | Severity | Mitigation |
|------|----------|-----------|
| WhatsApp/email ToS violation | high | Templates + opt-out + rate-limit |
| Scraping private data | high | Source registry + no scraping |
| Fake claims / testimonials | high | AI safety check + banned claims |
| Demo data reported as traction | medium | Every demo record marked `demo=true` |
| P0 outage | medium | Backup + restore + rollback |
| Slow lead response | medium | Outreach drafts + review queue |
| Founder burnout | medium | Daily operator + automation |
| Single point of failure (founder) | medium | Runbooks + training (V2+) |
| Loss of audit log | low | JSONL + backup |
| Loss of backup | low | Off-site (V2) |
