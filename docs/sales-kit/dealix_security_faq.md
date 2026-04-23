# Dealix — Security FAQ

## 20 سؤال الأكثر تكراراً من فرق IT وأجوبة جاهزة

**الاستخدام:** أرسلها قبل demo للـ Scale tier أو بعد أول اعتراض أمني.

---

## القسم 1: البيانات والتشفير

### 1. وين تُخزّن بياناتنا؟
**الجواب:** في Saudi Tier III+ data centers (STC Cloud — الرياض). البيانات لا تخرج المملكة.

### 2. كيف تُشفّر البيانات؟
- **At rest:** AES-256-GCM
- **In transit:** TLS 1.3 (بدون fallback لـ 1.2)
- **Backups:** AES-256 بمفاتيح مختلفة عن production
- **Keys:** AWS KMS / STC Cloud HSM — rotation كل 90 يوم تلقائياً

### 3. من يقدر يشوف بياناتنا داخل Dealix؟
- **Customer Success Manager:** للدعم فقط، ضمن NDA
- **On-call engineer:** عند حوادث P0/P1 فقط
- **لا يوجد:** استعلام روتيني على بيانات العملاء
- **كل وصول:** مسجّل في audit log قابل للتدقيق

### 4. كيف أضمن أنكم ما تبيعون بياناتنا؟
**الجواب:** مكتوب صراحة في `terms_of_service_ar.md` البند 7. نحن SaaS مدفوع — نموذج الأعمال يعتمد على رسوم الاشتراك، لا على بيع البيانات. انتهاك هذا البند يعطيك حق فسخ فوري + استرداد كامل.

### 5. إذا ألغينا، كيف نستعيد بياناتنا؟
- **تصدير فوري:** CSV / JSON / Excel عبر dashboard
- **API export:** endpoint `/api/v1/export` لأي نطاق زمني
- **بعد الإلغاء:** 30 يوم retention، ثم حذف نهائي
- **تأكيد الحذف:** شهادة موقّعة بالـ SHA-256 hash للبيانات المحذوفة

---

## القسم 2: الامتثال والشهادات

### 6. هل أنتم ملتزمون بنظام حماية البيانات الشخصية (PDPL)؟
**نعم.** كامل. مدققون ذاتياً مع مراجعة قانونية خارجية ربع سنوية. راجع `privacy_policy_ar.md`.

### 7. وضعكم من GDPR؟
ملتزمون بـ GDPR كـ processor. نوقّع DPA (Data Processing Agreement) مع أي عميل يطلبه.

### 8. أي شهادات أمنية عندكم؟
| الشهادة | الحالة | الموعد المتوقع |
|--------|-------|----------------|
| ISO 27001 | قيد التدقيق | نوفمبر 2026 |
| SOC 2 Type I | مخطط | Q2 2027 |
| PCI DSS | ❌ غير ضروري (الدفع عبر Moyasar PCI-compliant) |

### 9. هل تشاركون البيانات مع أطراف ثالثة؟
**Subprocessors الوحيدين:**
- STC Cloud (استضافة — السعودية)
- Moyasar (معالجة الدفع — السعودية)
- PostHog EU (analytics — ألمانيا، مشفّر + anonymized)
- Sentry (error tracking — الولايات المتحدة، scrubbed من PII)

قائمة كاملة + DPAs: في `privacy_policy_ar.md` الملحق أ.

### 10. هل تستخدمون AI يتدرّب على بياناتنا؟
**لا.** نماذج AI (LLMs للتلخيص + الاقتراحات) تستخدم APIs احترافية مع `zero-retention` mode. البيانات لا تُستخدم للتدريب.

---

## القسم 3: المصادقة والوصول

### 11. هل SSO مدعوم؟
نعم — Google Workspace، Microsoft 365، Okta، Azure AD، أي SAML 2.0 provider. (متضمن في Scale tier)

### 12. هل MFA إلزامي؟
- **للمستخدمين العاديين:** قابل للتفعيل
- **للـ admins:** إلزامي — لا يمكن تعطيله
- **الخيارات:** TOTP (Google Authenticator)، WebAuthn، SMS (مُثبّط)

### 13. كيف تُدار الصلاحيات؟
RBAC (Role-Based Access Control) مع 6 أدوار مُعرّفة:
- Super Admin / Admin / Manager / Sales Rep / Viewer / Integration

Custom roles: متاح في Scale tier.

### 14. هل يوجد IP whitelisting؟
نعم، في Scale tier. تحدد ranges (CIDR) في dashboard → Security → Network.

---

## القسم 4: التوفّر والموثوقية

### 15. ما هو SLA الخاص بكم؟
| Tier | Uptime SLA | Credit لو خُرق |
|------|-----------|-----------------|
| Starter | 99.5% | 5% |
| Growth | 99.9% | 10% |
| Scale | 99.95% | 25% |

**المقاس:** uptimerobot.com/r/m12345 (public status page)

### 16. كيف تتعاملون مع الكوارث (DR)؟
- **RPO** (Recovery Point Objective): **15 دقيقة**
- **RTO** (Recovery Time Objective): **4 ساعات**
- **Backups:** كل ساعة، كامل يومي، أسبوعي للأرشيف
- **Geo-replication:** بين الرياض وجدة
- **DR tests:** ربع سنوية مع تقرير للعملاء

### 17. إذا تأكد اختراق، متى تخبرونا؟
- **الكشف داخلياً:** < 1 ساعة (automated alerts)
- **إشعار العميل المتأثر:** < 24 ساعة
- **إشعار الهيئة السعودية للبيانات:** حسب PDPL — 72 ساعة
- **تقرير كامل:** خلال 7 أيام

---

## القسم 5: التكامل والأمان على مستوى API

### 18. كيف تُدار API keys؟
- مرتبطة بمستخدم محدد + صلاحياته
- Rotation تلقائي كل 12 شهر (تحذير قبل 30 يوم)
- Scoped: قابلة للحصر بـ read-only، specific endpoints، IP ranges
- Audit log: كل استدعاء يُسجّل

### 19. هل يوجد rate limiting؟
- **Per user:** 1,000 req/min
- **Per API key:** 10,000 req/min
- **Webhook retries:** exponential backoff، حتى 24 ساعة
- **DDoS protection:** Cloudflare Enterprise

### 20. هل عندكم bug bounty أو security disclosure program؟
نعم — security@dealix.sa
- **PGP key:** منشور على dealix.sa/security
- **Response SLA:** < 48 ساعة
- **المكافآت:** من 500 إلى 20,000 ريال حسب الشدة
- **Hall of fame:** dealix.sa/security/hof

---

## أسئلة إضافية شائعة

### هل يمكن self-hosting؟
**Scale tier فقط** — نشر على on-prem / private cloud عميلك. يحتاج +50% على السعر (متطلب infra + دعم خاص).

### هل تدعمون Saudi NCA Essential Cybersecurity Controls (ECC)?
نعم. Mapping كامل متاح عند الطلب (security@dealix.sa).

### ماذا يحدث لو شركتكم أُفلست؟
- **Data escrow:** نسخ محصّنة عند طرف ثالث (Iron Mountain KSA)
- **Source code escrow:** Scale tier فقط، عبر اتفاقية منفصلة
- **90 يوم wind-down guarantee:** تُعطى للعميل للانتقال

---

## جهة الاتصال الأمنية

**مسؤول الأمن:** سامي العسيري (مؤقتاً — CISO معيّن Q3 2026)
**البريد:** security@dealix.sa
**PGP:** متاح على dealix.sa/security
**Response SLA:** < 24 ساعة

---

*آخر تحديث: 2026-04-23 | مراجعة تالية: 2026-07-23*
