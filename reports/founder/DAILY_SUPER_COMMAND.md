# أمر المؤسس اليومي — Daily Super Command
*التاريخ: 2026-06-03 · المنطقة: Asia/Riyadh · الحالة: تشغيل تجريبي (send_enabled=false)*

> شاشة واحدة. قرار حرج واحد. كل الإجراءات الخارجية مُعطّلة حتى موافقتك. لا أسرار هنا.

---

## ⭐ القرار الحرج اليوم
**اعتماد سعر عرض TrainMe KSA (PROP-1001) — تشخيص تسرّب الإيراد.**
- النطاق السعري المقترح: 2,500–5,000 ريال (غير نهائي). | المخاطرة: medium | الدليل: client_reported.
- التوصية: اعتماد 2,500 ريال (كعميل أول بالقطاع) → تحويل لتسليم الدفع لاحقًا.
- الإجراء: `approve price` / `edit` / `reject`.

---

## 1. حالة إنتاج المسودات
| النوع | جاهزة للمراجعة | المصدر |
|---|---|---|
| عروض | 1 (PROP-1001) | `reports/revenue_execution/PROPOSAL_QUEUE.md` |
| Proof Packs | 1 (PRF-1001) | `reports/revenue_execution/PROOF_PACK_QUEUE.md` |
| تسليم دفع | 1 (PAY-1001) | `reports/revenue_execution/PAYMENT_HANDOFF_QUEUE.md` |
| بطاقات واتساب | 3 (WAC-0001/0002/0003) | `reports/whatsapp/WHATSAPP_ACTION_QUEUE.md` |

## 2. أهم إجراءات الموافقة (أعلى 5)
| # | العنصر | الشركة | النوع | المخاطرة | الإجراء |
|---|---|---|---|---|---|
| 1 | PROP-1001 | TrainMe KSA | اعتماد سعر | medium | approve/edit |
| 2 | PAY-1001 | Digital Rise | تسليم دفع (1,250 ريال) | high | approve/mark-sent |
| 3 | WAC-0002 | TrainMe KSA | بطاقة صلاحية (بوابة) | medium | approve |
| 4 | HHO-0001 | TrainMe KSA | تسليم بشري (سعر نهائي) | medium | assign/resolve |
| 5 | RAC-1003 | Digital Rise | توليد Proof Pack | low | approve |

## 3. الردود الإيجابية
- Digital Rise Agency (positive_reply) → جلسة واتساب WAS-0001 (فحص جاهزية).
- TrainMe KSA (form_submission) → WAS-0002 (بانتظار موافقة بدء التدفق).

## 4. بطاقات واتساب
WAC-0001 توصية · WAC-0002 صلاحية · WAC-0003 تسليم دفع — كلها `dry_run=true`, `send_enabled=false`.

## 5. طابور العروض / تسليمات الدفع
- العروض: PROP-1001 (pending) · PROP-1002 (معتمد).
- الدفع: PAY-1001 (pending_approval, لا إرسال تلقائي).

## 6. تسليمات (Sales→Delivery) / التجديد
- التسليم: DHO-1001 (Digital Rise) قيد التسليم؛ ONB-1001 (يوم 0/1 مكتمل).
- التجديد/الترقية: REN-1001 / UPS-1001 (مبنيّان على WVR-1001 — قيمة `measured`).

## 7. تنبيهات الخصوصية / الأمن
- 🔒 انتهاكات أسرار/أمن: **0** (آخر فحص: `scripts/client_revenue_delivery_check.py` ✓).
- ⚠️ UPL-1001 يحمل `pii_flag=true` → يجب إخفاء الهوية قبل التحليل.

## 8. لقطة النقد / الـpipeline
- pipeline: محتملون 15 · عرض معتمد 1 (2,500 ريال) · دفعة قيد الاعتماد 1,250 ريال.
- (ربط: `company_os/war_room/REVENUE_WAR_ROOM_TODAY.md`.)

---
*المرجع الحاكم: `AGENTS.md` · يتجدد يوميًا 09:00 — لا إرسال خارجي في v1.*
