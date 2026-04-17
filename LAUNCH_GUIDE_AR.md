# 🚀 Dealix — دليل التدشين الكامل

**آخر تحديث:** 17 أبريل 2026  
**المالك:** Sami Mohammed Assiri — sami.assiri11@gmail.com

---

## ✅ ما تم إنجازه (جاهز للاستخدام)

### 1. المستودع
- **GitHub:** https://github.com/VoXc2/dealix (private)
- **الفرع الرئيسي:** `main` (محمي منطقياً)
- **Commits:** 12+ commit منظّمة
- **Workflows:** 3 (Build ✅، Repo Hygiene ✅، Dependabot)
- **حجم المستودع:** 932 ملف
- **الحالة:** نظيف، بدون ZIPs، بدون secrets، CI أخضر

### 2. الصفحة الترويجية (Landing Page)
- **URL مباشر:** https://www.perplexity.ai/computer/a/dealix-TySM5EfESEW_3m4J5E3RZA
- **RTL كامل + عربي first**
- **Responsive + Dark mode**
- **11 قسم:** nav, hero, value props, 8 agents, كيف يعمل, testimonials, تسعير, امتثال, FAQ, CTA, footer
- **~72KB total**

### 3. التوثيق الاحترافي (الكل عربي)
| الملف | الأسطر | الهدف |
|------|--------|-------|
| `README.md` | 449 | نظرة عامة + stack + agents |
| `ARCHITECTURE.md` | 376 | البنية المعمارية + ADRs |
| `docs/API.md` | 522 | REST API spec كاملة |
| `docs/DEPLOYMENT.md` | 503 | دليل النشر (dev/staging/prod) |
| `docs/QUICKSTART.md` | 316 | بدء سريع للمطورين |
| `docs/registry/TRUTH.yaml` | 135 | 12 claim بدليل |
| `docs/registry/CLAIMS.md` | 60 | قائمة المصطلحات الممنوعة |
| `DAILY_EXECUTION_SCHEDULE_AR.md` | 1,136 | **90 يوم × 451 مهمة** |
| `LAUNCH_CHECKLIST_AR.md` | 161 | قائمة تحقق التدشين |
| `backend/README.md` | 145 | دليل Backend |
| `frontend/README.md` | 151 | دليل Frontend |
| `frontend/RTL_GUIDE.md` | 242 | دليل RTL |

### 4. الجودة والأمان
- **Backend:** Ruff + Black + mypy + Bandit + pytest
- **Frontend:** ESLint + Prettier + TypeScript strict
- **Truth Registry validator** — يعمل في CI
- **Repo Hygiene** — يرصد secrets حقيقية فقط
- **GitHub templates** — Bug, Feature, PR
- **Branch protection** — يحتاج GitHub Pro (راجع الخطوات التالية)

### 5. البنية التحتية
- **docker-compose.yml** محدّث (PostgreSQL 16, Redis 7, Backend, Worker, Beat, Frontend)
- **Root Makefile** — `make install`, `make up`, `make test`, `make validate`
- **`.env.example`** كامل (root + backend + frontend)

### 6. الأتمتة
- **بريف Dealix اليومي** — يرسل إشعار كل صباح 8 ص بتوقيت الرياض
- **4 crons إضافية** (بانتظار موافقتك)

---

## 📋 ما تحتاج تعمله بنفسك (يتطلب بياناتك الشخصية)

### 1. النطاق (Domain) — أولوية عالية 🔴

**الموصى به:** `dealix.sa` أو `dealix.ai` أو `dealix.app`

**خطوات التسجيل:**
1. افتح [Namecheap](https://www.namecheap.com) أو [GoDaddy](https://www.godaddy.com) أو [SaudiNIC](https://nic.sa) (للـ .sa)
2. ابحث عن `dealix` + الامتداد المطلوب
3. اشتره (السعر: 10-50$ للسنة، أو 150-400 ريال لـ .sa)
4. فعّل Privacy Protection
5. **بعد الشراء:** أرسل لي اسم النطاق لأضبط الـ DNS والـ SSL

**DNS configuration بعد الشراء:**
```
A     @           → IP الخادم
CNAME www         → dealix.sa
TXT   @           → (SPF سجل للإيميل)
CNAME mail        → (ربط Zoho/Google Workspace)
```

### 2. الحساب البنكي وبوابة الدفع — أولوية عالية 🔴

#### أ) السجل التجاري (إن لم يكن موجوداً)
- [منصة المركز السعودي للأعمال](https://business.sa)
- رسوم: ~1,200 ريال/سنة
- نوع النشاط: "خدمات تقنية المعلومات" أو "الأنشطة المتعلقة ببرامج الحاسب"

#### ب) الحساب البنكي التجاري
**بنوك موصى بها للـ SaaS:**
- **الراجحي** (الأوسع تغطية)
- **الأهلي التجاري** (خدمات رقمية جيدة)
- **البنك العربي** (للتحويلات الدولية)
- **STC Pay** (للمدفوعات الرقمية الصغيرة)

**المتطلبات:**
- السجل التجاري
- الهوية الوطنية
- عقد إيجار/ملكية المقر
- خطاب طلب فتح حساب

#### ج) بوابة الدفع (للاشتراكات الشهرية)
**الخيارات الرئيسية للسوق السعودي:**

| البوابة | العمولة | الميزات |
|---------|---------|---------|
| **[Moyasar](https://moyasar.com)** ⭐ | 2.75% + 1 ريال | سعودية، متوافق ZATCA، دعم سعودي |
| **[Tap Payments](https://tap.company)** | 2.85% + 1 ريال | خليجية، سريعة الإعداد |
| **[HyperPay](https://hyperpay.com)** | مفاوض | enterprise، تكامل بنوك محلية |
| **Stripe** | 2.9% + 1.2 ريال | عالمية، لكن محدودة للسعودية |

**الموصى به:** Moyasar (للبدء)

**ما تحتاجه:**
- سجل تجاري
- حساب بنكي
- هوية وطنية
- رقم جوال ساري
- عقد استضافة/خدمة (يمكن رفع نموذج من Dealix)

### 3. إيميل العمل (Business Email)

**الخيارات:**
- **Google Workspace** — 25 ريال/شهر (موصى به)
- **Microsoft 365** — 30 ريال/شهر
- **Zoho Mail** — مجاني لـ 5 مستخدمين (موفّر)

**الإعداد:**
1. اختر المزود
2. اربطه بالنطاق `contact@dealix.sa`, `support@dealix.sa`, `billing@dealix.sa`
3. فعّل 2FA
4. أرسل لي الإعدادات لأحدّث الـ landing page

### 4. التسجيلات الحكومية

#### ZATCA (للفوترة الإلكترونية)
- **متطلب:** أي شركة SaaS
- [منصة فاتورة](https://zatca.gov.sa/ar/E-Invoicing/Pages/default.aspx)
- تسجل الشركة + تحصل على رقم مزود
- **المرحلة 2** مطلوبة لكل الشركات الجديدة
- Dealix تكامل متوفر في الكود (`backend/app/integrations/zatca/`)

#### PDPL (حماية البيانات)
- سجّل الشركة كـ "Data Controller" في [SDAIA](https://sdaia.gov.sa)
- عيّن "Data Protection Officer" (يمكن يكون أنت في البداية)
- نشر Privacy Policy عربي (موجود في `docs/legal/PRIVACY_POLICY_AR.md` — بانتظار مراجعة قانونية)

#### هيئة الاتصالات (CST) — اختياري
- إذا ستقدّم خدمات اتصالات (WhatsApp مرسل رسائل تسويقية) قد تحتاج ترخيصاً

### 5. الاستضافة (Hosting)

**التوصيات حسب المرحلة:**

| المرحلة | الخيار | التكلفة/شهر |
|---------|-------|------------|
| **MVP (1-10 عملاء)** | [Hetzner](https://hetzner.com) VPS | ~$20 (75 ريال) |
| **Staging** | [Railway](https://railway.app) / [Render](https://render.com) | ~$30-50 |
| **Production (50+ عميل)** | [AWS](https://aws.amazon.com) me-south-1 (البحرين) | $200-500+ |
| **Enterprise** | [STC Cloud](https://cloud.stc.com.sa) | مفاوض |

**الموصى به للبدء:** Hetzner VPS + Cloudflare CDN

**ما تحتاجه:**
1. افتح حساب Hetzner (يتطلب بطاقة ائتمان)
2. أنشئ Cloud Server (CX21 — 4GB RAM)
3. أرسل لي IP الخادم + SSH key

### 6. المكاتب والتواصل

- **رقم هاتف العمل:** من STC Business (150 ريال/شهر)
- **WhatsApp Business API:** عبر [Twilio](https://twilio.com) أو [360dialog](https://360dialog.com) أو Meta مباشرة
- **عنوان بريدي:** صندوق بريد أو مكتب افتراضي ([Regus](https://regus.com) ~500 ريال/شهر)

---

## 🎯 الخطوات التالية بترتيب الأولوية

### الأسبوع القادم (18-24 أبريل)
1. ☐ **احجز نطاق dealix.sa أو dealix.ai** (ساعة واحدة)
2. ☐ **افتح حساب بنكي تجاري** (2-3 أيام)
3. ☐ **سجل في Moyasar** (يوم واحد)
4. ☐ **أنشئ Google Workspace** (ساعة)
5. ☐ **أنشئ Hetzner VPS** (نصف ساعة)
6. ☐ **أرسل لي كل المعلومات** لأربطها بالمشروع

### الأسبوعان التاليان (25 أبريل - 8 مايو)
7. ☐ تسجيل ZATCA
8. ☐ نشر Privacy Policy + Terms of Service (سأجهزهما)
9. ☐ نشر الـ landing page على النطاق الرسمي
10. ☐ اختبار docker-compose محلياً

### الشهر القادم (9 مايو - 8 يونيو)
11. ☐ اكتمال Backend hardening (راجع جدول 90 يوم — أسابيع 3-5)
12. ☐ تكامل LLM router + 8 agents
13. ☐ أول pilot customer

---

## 📞 طريقة العمل معي

أرسل لي أي من هذه، وأنا أتصرّف فوراً:
- "النطاق جاهز: dealix.sa" → أضبط DNS + SSL + landing
- "حساب Moyasar API Key: xxx" → أتكامل في الـ backend
- "VPS IP: x.x.x.x" → أنشر الـ stack
- "Google Workspace جاهز" → أضبط إيميلات + DMARC
- "أريد مراجعة [شيء]" → أفحص وأحسّن

**البريف اليومي** يوصلك كل صباح 8 ص على تقدم المشروع.

---

## 🔗 روابط سريعة

- **المستودع:** https://github.com/VoXc2/dealix
- **Landing Live:** https://www.perplexity.ai/computer/a/dealix-TySM5EfESEW_3m4J5E3RZA
- **جدول 90 يوم:** [DAILY_EXECUTION_SCHEDULE_AR.md](./DAILY_EXECUTION_SCHEDULE_AR.md)
- **Launch Checklist:** [LAUNCH_CHECKLIST_AR.md](./LAUNCH_CHECKLIST_AR.md)
- **Architecture:** [ARCHITECTURE.md](./ARCHITECTURE.md)
- **API:** [docs/API.md](./docs/API.md)
- **Deployment:** [docs/DEPLOYMENT.md](./docs/DEPLOYMENT.md)

---

© 2026 Dealix — جميع الحقوق محفوظة.
