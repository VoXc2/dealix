# Launch Risk Register (سجل المخاطر)

سجل المخاطر التي قد تُفشل الإطلاق، ومستواها، والتخفيف المعتمد. يُراجَع قبل كل
انتقال بين أوضاع الإطلاق.

---

| # | الخطر | المستوى | التخفيف |
|---|-------|--------:|---------|
| R1 | Email domain reputation | High | إرسال يدوي + SPF/DKIM/DMARC + حجم منخفض + warm-up |
| R2 | Invented contacts | High | اشتراط مصدر عام + درجة ثقة + فحص آلي في checker |
| R3 | Weak delivery | High | Delivery Gate + inputs إلزامية + acceptance criteria |
| R4 | Prompt injection / tool poisoning | High | External content = untrusted data + least-privilege CI |
| R5 | Too many systems publicly | Medium | الموقع العام = الأنظمة الأساسية فقط |
| R6 | Founder overload | Medium | Daily Super Command يلخّص القرار الواحد المهم |
| R7 | Bad-fit prospects | Medium | Account score نهائي + suppression للمستبعَدين |
| R8 | Scope creep | Medium | Proposal Gate + بند out-of-scope صريح |
| R9 | Secrets leakage في logs/prompts | High | لا secrets في prompts/logs/reports + مراجعة |
| R10 | Spam complaints / no unsubscribe | High | one-click unsubscribe + مراقبة spam rate |

---

## قواعد التخفيف الثابتة

- **R1/R10 (سمعة البريد):** البريد البارد بدون قواعد deliverability يضر الدومين بسرعة.
  Google تطلب SPF/DKIM، و DMARC للمرسلين الكبار، و one-click unsubscribe للرسائل
  التسويقية من bulk senders، وتوصي بمراقبة spam rate. لذلك يجب gates قبل الإرسال،
  لا مجرد توليد مسودّات.
- **R4/R9 (الأمن):** الأدوات المعتمدة على AI و MCP عرضة لـ prompt injection و
  tool poisoning. القاعدة: المحتوى الخارجي بيانات لا أوامر، و GitHub Actions بأقل
  صلاحية ممكنة.

التفاصيل التنفيذية في `reports/launch/LAUNCH_RISK_REGISTER.md` و
`reports/launch/SECURITY_GO_NO_GO.md`.
