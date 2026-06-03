# كشف الانحراف (Drift Detection)

كشف الفجوة بين الحالة المقصودة والفعلية (كود/بيانات/حوكمة).

## أنواع الانحراف ومراقبته
| النوع | كيف يُكشف |
|------|-----------|
| انحراف وثائق الوكلاء عن السجل | `agentic-security-gate.yml` يشغّل المولّد ويفشل عند الفرق |
| انحراف المخططات عن البيانات | `tests/test_schemas_and_data.py` |
| انحراف بوابات CI | `scripts/check_workflow_security.py` |
| أسرار مُرتكبة | `scripts/scan_secrets.py` + secret-scanning |
| ادعاءات في المحتوى الصادر | `tests/test_no_claims_in_docs.py` |
| تكرار/تعارض (مثل `company_os/company_os/`) | مراجعة + تقرير تعارض |

## قاعدة
أي انحراف يكسر CI أو يُرفع للمؤسس — لا يُتجاوز بإضعاف الفحص.
