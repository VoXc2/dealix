# Lead Intelligence Sprint — اختبار قبول (Acceptance)

الخدمة **PASS** على مجموعة العرض إذا نُفِّذ التالي على **بيانات عرض / عميل** (بدون إرسال خارجي):

1. استيراد ≥100 صف (أو ما يعادلها في النطاق المتفق).  
2. فرز valid / invalid rows.  
3. كشف duplicates.  
4. حساب **data quality score**.  
5. **source attribution** مسجّل للحقول الحرجة.  
6. **scoring** مع شرح مختصر للدرجة.  
7. **Top 50** (أو حد النطاق) حسابات مرتبة.  
8. **Top 10 actions** واضحة.  
9. ≥10 **outreach drafts** (مسودات فقط).  
10. **منع** cold WhatsApp / إرسال تلقائي من المسار.  
11. **Executive report** منسّق.  
12. **Proof pack** يغطي مدخلات / معالجة / مخرجات / أثر / الخطوة التالية.

أي بند يفشل = الخدمة **غير جاهزة** للتوسيع في التسويق حتى يُصلح.

المشغّل المرجعي: [`lead_intelligence_sprint.py`](../../../auto_client_acquisition/commercial_engagements/lead_intelligence_sprint.py).
