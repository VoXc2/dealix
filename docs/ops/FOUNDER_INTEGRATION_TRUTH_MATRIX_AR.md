# مصفوفة حقيقة الربط — للمؤسس

> **المصدر الآلي:** [`dealix/transformation/founder_integration_truth.yaml`](../../dealix/transformation/founder_integration_truth.yaml)  
> **تحديث الحالة:** عدّل `status: green|yellow|red` في YAML ثم شغّل `bash scripts/founder_go_live_verify.sh`  
> **API:** `GET /api/v1/business-now/commercial-strategy` → `integration_truth_summary`

## معنى الألوان

| status | للمؤسس | للعميل |
| --- | --- | --- |
| **green** | جاهز محلياً / pytest | يمكن عرضه live في الديمو |
| **yellow** | يدوي أو sandbox أو يحتاج tenant | «نفعّل بعد التوقيع / بيئة اختبار» |
| **red** | غير مفعّل — لا تعد | «خارج النطاق حتى الموافقة والإعداد» |

---

## سلم العروض (Diagnostic → Retainer)

| العرض | السعر | Endpoint | اختبار | status |
| --- | --- | --- | --- | --- |
| Governed Revenue Ops Diagnostic | 4,999–15,000 | `POST /api/v1/service-setup/qualify` | qualify + proposal يدوي | yellow |
| تشخيص مجاني | 0 | `POST /api/v1/company-growth-beast/diagnostic` | intake | green |
| سبرنت 499 | 499 | `POST /api/v1/sprint/run` | golden chain smoke | green |
| حزمة بيانات 1500 | 1,500 | `POST /api/v1/data-os/import-preview/upload` | data_os tests | green |
| نمو شهرية 2999 | 2,999/شهر | `GET /api/v1/value/{handle}/report/monthly` | tenant يدوي | yellow |
| دعم 1500 | 1,500/شهر | support_os | capability verify | yellow |
| ECC 7500 | 7,500/شهر | founder command center | demo runbook | yellow |

---

## تكاملات خارجية

| التكامل | status | ماذا تقول |
| --- | --- | --- |
| Postgres + Redis | green | أساس التشغيل المحلي |
| Moyasar live | red | فاتورة يدوية أو KYC |
| Moyasar sandbox | yellow | اختبار تقني بـ sk_test |
| WhatsApp Business | red | مسودات + موافقة فقط |
| HubSpot | yellow | CRM يدوي + YAML KPI |
| Gmail خارجي | red | لا إرسال بدون موافقة |

---

## فحوصات المنصة

| فحص | سكربت |
| --- | --- |
| Golden chain | `pytest tests/test_revenue_os_golden_chain_smoke.py` |
| Business NOW | `scripts/run_business_now.sh` |
| Revenue OS | `scripts/revenue_os_master_verify.sh` |
| Capability | `scripts/dealix_capability_verify.sh` |

---

## Moyasar sandbox (P0)

1. أنشئ `sk_test_...` من لوحة Moyasar
2. ضعه في `.env` كـ `MOYASAR_SECRET_KEY`
3. `POST /api/v1/payment-ops/invoice-intent` (عميل اختبار)
4. حدّث `moyasar_sandbox` → `green` في YAML بعد نجاح الاختبار

مرجع: [INTEGRATIONS_NEEDED.md](INTEGRATIONS_NEEDED.md)
