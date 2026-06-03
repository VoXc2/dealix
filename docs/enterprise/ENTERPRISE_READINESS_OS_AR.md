# نظام الجاهزية المؤسسية (Enterprise Readiness OS)

دليل جاهزية Dealix للبيع للمؤسسات والمراجعات الأمنية. **لا تُختلق جاهزية** —
المجهول يُعلَّم `TBD`، وتُستخدم مستويات الأدلة.

## أعمدة الجاهزية
| العمود | الحالة | المرجع |
|--------|--------|--------|
| وضع أمني موثّق | 🟢 | `SECURITY_POSTURE_SUMMARY_AR.md`, `docs/security/*` |
| خصوصية/PDPL | 🟢 سياسات / 🟡 تسجيل عند الإيراد | `docs/privacy/*` |
| حوكمة وكلاء | 🟢 | `docs/agents/*` (مفروضة باختبارات) |
| اختبارات/CI | 🟢 134 اختبار + 9 بوابات | `tests/`, `.github/workflows` |
| إدارة أسرار | 🟢 سياسة / 🟡 مدير أسرار إنتاج | `docs/infra/SECRETS_MANAGEMENT_POLICY_AR.md` |
| موثوقية/SLO | 🟡 مسودة | `docs/infra/SLO_SLA_POLICY_AR.md` |
| نماذج DPA مع المورّدين | 🟡 TBD | `data/procurement/vendors.jsonl` |
| Traction موثّق | 🟡 TBD (يملؤه المؤسس) | `docs/data_room/TRACTION_TEMPLATE_AR.md` |

## مستويات الأدلة
`none / assumption / anecdote / internal_data / verified / third_party_verified`.

## ما الذي نقوله للمؤسسة بصدق اليوم
- نظام إيرادات B2B سعودي، **موافقة-أولاً، dry-run افتراضياً**، مع طبقة سلامة
  قابلة للاختبار وحوكمة وكلاء وبوابات CI أقل صلاحية.
- **لا** إرسال آلي، **لا** نشر إنتاج، **لا** ادعاءات نتائج مضمونة.
- بنود مفتوحة صريحة (TBD) بدل المبالغة.
