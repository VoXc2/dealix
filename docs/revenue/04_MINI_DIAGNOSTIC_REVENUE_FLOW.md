# تدفق Mini Diagnostic (تحويل)

1. **موافقة:** سؤال صريح أن الإجابات للتشخيص الداخلي فقط حتى توافق على إرسال خارجي.
2. **توليد:** `python scripts/dealix_diagnostic.py --company "..." --sector b2b_services --region riyadh --pipeline-state "..."`  
   أو `--json` لملخص آمن.
3. **مراجعة يدوية** ثم تسليم صفحة واحدة للعميل.
4. **عرض Pilot 499** باستخدام `scripts/dealix_pilot_499_close_pack.py`.

Workflow API إن لزم: [`api/routers/diagnostic_workflow.py`](../api/routers/diagnostic_workflow.py).
