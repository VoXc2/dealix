# Ledger Architecture — الذاكرة الرسمية

كل حدث **مهم** يُسجَّل في **ledger** — الشركة تتعلم مؤسسيًا لا في رأس المؤسس فقط.

## Ledgers رئيسية

| Ledger | يخزّن |
|----------|--------|
| **AI Run** | agent · task · model · prompt version · redaction · schema · cost · risk · QA · governance status |
| **Audit** | who · what · when · why · approval · risk |
| **Proof** | قيمة مُنشأة · قياس · أدلة · قيود |
| **Capital** | أصل · reusable؟ · أين يُعاد الاستخدام؟ · أي وحدة تستفيد؟ |
| **Productization** | خطوة يدوية · تكرار · وقت · خطر · رابط إيراد · قرار |
| **Client Health** | توسع · تعاون · دفع · مخاطر |
| **Unit Performance** | إيراد وحدة · هامش · QA · proof · retainers · نضج |
| **Partner** | قنوات · شهادات · مخاطر شريك |
| **Venture Signal** | عوامل جاهزية venture |

**مراجع:** [`../product/AI_RUN_PROVENANCE.md`](../product/AI_RUN_PROVENANCE.md) · [`../governance/AUDIT_LOG_POLICY.md`](../governance/AUDIT_LOG_POLICY.md) · [`../product/PRODUCTIZATION_LEDGER.md`](../product/PRODUCTIZATION_LEDGER.md) · [`../ledgers/`](../ledgers/)

**أسماء مسجلة في الكود:** `intelligence_os/ledger_reader.py` (`LEDGER_NAMES`)

## مبدأ

الـ ledger ليس «سجل أنيق» فقط — هو **مدخل Metric Layer** و**Decision Layer**.
