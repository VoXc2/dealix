# أول 10 warm intros

1. اختر 10 علاقات دافئة فقط (لا قوائم مشتراة).
2. شغّل `python scripts/dealix_first10_warm_intros.py` لتوليد لوحة خانات في `docs/revenue/live/` (لا تُرفع لـ git).
3. لكل خانة: اقرأ آخر 3 منشورات، املأ `pain_hypothesis` خارج الريبو.
4. ولّد مسودة: `POST /api/v1/sales/script` مع `locale=ar` و`script_type=opener`.
5. راجع الموافقات: `GET /api/v1/approvals/pending` ثم أرسل **يدوياً**.
