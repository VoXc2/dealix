# Dependency Risk Map

| اعتماد | خطر | ضبط |
|--------|-----|-----|
| Single LLM provider | صدمة سعر/جودة/سياسة | LLM Gateway + model router |
| Founder delivery | اختناق | delivery OS + قوائم |
| مشاريع مخصصة فقط | فخ وكالة | عروض مُنتَجة |
| بيانات ضعيفة | مخرجات سيئة | Source Passport |
| أتمتة غير آمنة | فقدان ثقة | Governance Runtime |
| قناة مبيعات واحدة | هشاشة نمو | شركاء + محتوى + academy |
| شريحة عملاء واحدة | هشاشة سوق | portfolio |
| لا proof | احتفاظ ضعيف | Proof Pack |
| لا التقاط رأس مال معرفي | لا مركب | Capital Ledger |

**القاعدة:** كل dependency لها **fallback أو control**.

**الكود:** `DEPENDENCY_REQUIRED_CONTROLS` · `dependency_mitigated` — `sovereignty_os/dependency_risk.py`

**صعود:** [`OPERATING_SOVEREIGNTY.md`](OPERATING_SOVEREIGNTY.md)
