# معايير الامتثال — هيئة الذكاء الاصطناعي السعودية (SDAIA)

## المखलص
Dealix تتبع معايير SDAIA في كل استخدام AI. هذا المستند يحدد ملف الـ compliance.

## 1. الحوكمة (Governance)
- [x] **Policy**: AI يوصي ويحلل، ولا يقرر بدلاً من الإنسان
- [x] **Approval Queue**: كل إخراج AI في رسائل marketing يتطلب manual approval
- [x] **Audit Trail**: كل قرار مرتبط بـ Owner + Date + Action
- [x] **No Auto-Send Gate**: `verify_no_auto_external_send.py` — يعمل تلقائياً

## 2. الشفافية (Transparency)
- [x] **AI Tag**: كل رسالة تولدها AI تحمل [AI] tag قبل الإرسال
- [x] **Explanation**: AI يوضح سبب الترشيح (prospect score + rationale)
- [x] **Documentation**: العميل يوضح كيف AI يعمل في الـ System Architecture

## 3. العدالة والحماية من التحيز (Fairness)
- [x] **Non-Discrimination**: Prospect scoring يعتمد على data — وليس جنسة/عرق/كيانات
- [x] **Equal Service**: كل prospects يُعطى access لنفس الأدوات
- [x] **Data Integrity**: Source URLs required + verification status tracked

## 4. الخصوصية وحماية البيانات (Privacy)
- [x] **PDPL Compliance**: متوافق مع نظام حماية البيانات السعودية
- [x] **Data Localization**: تُخزن في السعودية (Saudi-based hosting)
- [x] **No Third Party Sharing**: لا مشاركة بيانات العملاء مع أطراف ثالثة
- [x] **Anonymization**: PII (email, phone) مشفرة في DB + logs
- [x] **Client Consent**: Opt-in required (consent_email) before any outreach

## 5. الأمان والأمان (Security)
- [x] **Encrypted Storage**: AES-256 للـ DB + backups
- [x] **HTTPS/SSL**: كل communication مشفر (TLS 1.3)
- [x] **API Keys**: .env secret — لا secrets مكشوفة في الـ repo
- [x] **Rate Limiting**: API requests محددة لمنع abuse

## 6. الصلاحية والمسؤولية (Accountability)
- [x] **Founder Ownership**: كل send يتطلب موافقة founder
- [x] **Logging**: كل draft approved/sent يُسجل في Ledger
- [x] **Recall**: توقف outreach ممكن في أي لحظة
- [x] **Escalation**: كل خطأ خطير يرفع إلى founder مباشرة

## 7. إدارة المخاطر (Risk Management)
- [x] **Risk Register**: كل risk AI يُسجل ويُتابع
- [x] **Human-in-the-loop**: AI generates → Founder approves → System sends
- [x] **Kill Switch**: `EXTERNAL_SEND_ENABLED=false` يوقف كل الإرسال

## المستندات المرتبطة
- `docs/pdpl/PDPL_CHECKLIST.md` — تفاصيل SDAIA-PDPL mapping
- `scripts/verify_no_auto_external_send.py` — Safety gate
- `api/middleware.ts` — Manual approval enforcement
- `db/schema.ts` — Audit fields (`approved`, `sent`, `aiGenerated`)
