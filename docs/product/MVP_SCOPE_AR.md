# Dealix — نطاق MVP

## تعريف MVP

**MVP = Minimum Viable Product** = الحد الأدنى من المنتج القابل للتسويق

هدف MVP:
- يثبت القيمة الأساسية
- آمن وقابل للحوكمة
- قابل للتكرار
- يُنتج بيانات حقيقية

---

## مكونات MVP الإلزامية

### 1. docs/specs (مواصفات)
- [ ] API specs للـ endpoints الأساسية
- [ ] Data models للـ entities
- [ ] User flows للـ core journeys

### 2. schemas (مخططات)
- [ ] opportunity.schema.json
- [ ] product_feature.schema.json
- [ ] product_feedback.schema.json
- [ ] roadmap_item.schema.json

### 3. reports (تقارير)
- [ ] Weekly Value Report template
- [ ] Delivery Handoff Report
- [ ] ROI Proof template

### 4. dry-run scripts (سكربتات تجريبية)
- [ ] Lead scoring dry-run
- [ ] Content draft dry-run
- [ ] Approval queue simulation

### 5. approval queues (طوابير الموافقة)
- [ ] Outreach approval queue
- [ ] Proof generation approval
- [ ] Report sending approval

### 6. safety gates (بوابات الأمان)
- [ ] Pre-send validation gate
- [ ] Data privacy gate
- [ ] Compliance gate

### 7. minimal UI specs (مواصفات UI دنيا)
- [ ] Founder Control Room wireframe
- [ ] Approval queue interface
- [ ] Basic dashboard layout

### 8. NO uncontrolled external actions
- ❌ لا إرسال بريد بدون موافقة
- ❌ لا واتساب بدون consent
- ❌ لا scraping بدون authorization

---

## Features ضمن MVP

| Feature | Priority | Effort | Status |
|---------|----------|--------|--------|
| Lead intake + scoring | P0 | High | Required |
| GTM Draft Factory | P0 | High | Required |
| Approval Queue | P0 | Medium | Required |
| Founder Control Room | P0 | High | Required |
| Proposal template | P1 | Medium | Required |
| Basic dashboard | P1 | Medium | Required |
| Reply handling (basic) | P1 | Medium | Required |

---

## Features مؤجلة لـ v1.1+

| Feature | Priority | Reason |
|---------|----------|--------|
| WhatsApp integration | P2 | Requires consent flow |
| CRM sync | P2 | Post-MVP |
| Advanced analytics | P2 | Post-MVP |
| Partner portal | P3 | Post-MVP |

---

## Features التي لن تُبنى أبداً في MVP

- ❌ Cold WhatsApp automation
- ❌ LinkedIn automation
- ❌ Broad scraping
- ❌ General AI chatbot
- ❌ Production deploy automation بدون approval

---

## Release Criteria

### لاطلاق MVP:
1. ✅ جميع P0 features مكتملة
2. ✅ Approval queues تعمل
3. ✅ Safety gates مفعلة
4. ✅ CI tests تمر
5. ✅ Founder review تم
6. ✅ Security audit passed

### للنجاح:
1. ✅ أول 3 عملاء يوقعون
2. ✅ أول 3 مقترحات تُرسل
3. ✅ أول proof pack يُولد
4. ✅ أول weekly report يُرسل

---

## _links

- Strategy: `PRODUCT_STRATEGY_AR.md`
- Principles: `PRODUCT_PRINCIPLES_AR.md`
- Roadmap: `ROADMAP_AR.md`
- What Not to Build: `WHAT_NOT_TO_BUILD_AR.md`
