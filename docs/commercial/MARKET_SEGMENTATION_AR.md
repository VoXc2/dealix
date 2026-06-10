# Market Segmentation — تقسيم السوق
**Dealix — Agent #3**

> **الغرض:** تقسيم منهجي للسوق السعودي B2B المستهدف من Dealix، بحيث يربط بين القطاع، حجم الشركة، نضج المبيعات، والإيرادات المتوقعة.

---

## 1. Segmentation Dimensions (أبعاد التقسيم)

نستخدم **4 أبعاد** لتقسيم السوق:

| البُعد | الوصف | الفئات |
|--------|-------|--------|
| **Industry (القطاع)** | ما القطاع؟ | agency, training, clinic, real_estate, recruitment, professional_services, local_saas, education, logistics, restaurant |
| **Size (الحجم)** | كم عدد الموظفين؟ | micro (1-5), small (6-20), medium (21-100), large (100+) |
| **Lead Flow Maturity** | هل عندهم leads متكررة؟ | none, sporadic, recurring, growing |
| **Sales Process Maturity** | هل عندهم sales process منظم؟ | none, ad-hoc, documented, optimized |

---

## 2. Total Addressable Market (TAM) — التقدير

**سوق B2B السعودي للشركات متوسطة الحجم (SMEs):**
- عدد SMEs في السعودية ≈ 1.1M (تقرير مُقدر)
- النسبة في قطاعاتنا الـ 10 ≈ 30% (تقدير) = 330K شركة
- ICP fit (top 10 segments) ≈ 5% = 16,500 شركة
- SAM (التي يمكننا الوصول إليها بسوقنا الحالي) ≈ 5% من ICP fit = 825 شركة
- SOM (Year 1 realistic) = 25-50 شركة

**Source:** تقدير مبني على `MARKET_INTELLIGENCE_SAUDI_SAAS_MARKET_AR.md`. كل رقم تقديري يجب أن يُوسم `is_estimate`.

---

## 3. Segment Cards (بطاقات الشرائح)

### 3.1 Marketing Agencies
- **Volume:** 5,000+ agency in KSA (تقدير)
- **Avg deal size:** 9,999-25,000 SAR (Diagnostic) + 4,999-15,000/mo (Retainer)
- **Cycle time:** 7-21 يوم
- **Decision maker:** Agency Owner
- **Trigger:** campaigns active + leakage
- **Source signals:** leads, campaigns, hashtag, content

### 3.2 Training Companies
- **Volume:** 2,000+ (تقدير)
- **Avg deal:** 8,000-18,000 SAR
- **Cycle:** 14-30 يوم
- **DM:** Owner / Training Manager
- **Trigger:** enrollment season approaching
- **Source signals:** enrollment, registration, course

### 3.3 Clinics
- **Volume:** 8,000+ clinics (تقدير)
- **Avg deal:** 12,000-25,000 SAR
- **Cycle:** 14-30 يوم
- **DM:** Clinic Manager
- **Trigger:** appointments being lost
- **Source signals:** appointment, no-show, follow-up

### 3.4 Real Estate
- **Volume:** 3,000+ brokerages (تقدير)
- **Avg deal:** 9,999-25,000 SAR
- **Cycle:** 14-21 يوم
- **DM:** Office Manager / Owner
- **Trigger:** leads cooling fast
- **Source signals:** viewing, property, listing

### 3.5 Recruitment
- **Volume:** 1,500+ (تقدير)
- **Avg deal:** 12,000-25,000 SAR
- **Cycle:** 14-30 يوم
- **DM:** Agency Owner
- **Trigger:** placements lost
- **Source signals:** candidate, client, placement

### 3.6 Professional Services
- **Volume:** 6,000+ firms (تقدير)
- **Avg deal:** 9,999-25,000 SAR
- **Cycle:** 21-45 يوم
- **DM:** Partner
- **Trigger:** inquiry to proposal gap
- **Source signals:** consultation, advisory, RFP

### 3.7 Local SaaS
- **Volume:** 1,000+ (تقدير)
- **Avg deal:** 18,000-35,000 SAR
- **Cycle:** 21-45 يوم
- **DM:** Founder / Head of Sales
- **Trigger:** ARR pressure
- **Source signals:** demo, trial, ARR

### 3.8 Education
- **Volume:** 2,000+ providers (تقدير)
- **Avg deal:** 15,000-35,000 SAR
- **Cycle:** 30-60 يوم
- **DM:** Admissions Manager
- **Trigger:** admissions season
- **Source signals:** admission, registration, enrollment

### 3.9 Logistics / Service Ops
- **Volume:** 4,000+ companies (تقدير)
- **Avg deal:** 15,000-25,000 SAR
- **Cycle:** 21-30 يوم
- **DM:** Ops Manager
- **Trigger:** quote chaos
- **Source signals:** quote, shipment, delivery

### 3.10 Restaurant Groups
- **Volume:** 2,500+ groups (تقدير)
- **Avg deal:** 9,999-18,000 SAR
- **Cycle:** 14-30 يوم
- **DM:** Group Owner
- **Trigger:** campaign inquiries lost
- **Source signals:** reservation, order, customer

---

## 4. Size Distribution (التوزيع الحجمي)

لكل شريحة، توزيع تقريبي:

| Segment | Micro | Small | Medium | Large |
|---------|-------|-------|--------|-------|
| Agency | 40% | 45% | 12% | 3% |
| Training | 50% | 35% | 12% | 3% |
| Clinic | 70% | 25% | 4% | 1% |
| Real Estate | 60% | 30% | 8% | 2% |
| Recruitment | 55% | 35% | 8% | 2% |
| Prof Services | 65% | 25% | 8% | 2% |
| Local SaaS | 30% | 50% | 18% | 2% |
| Education | 50% | 35% | 12% | 3% |
| Logistics | 55% | 35% | 8% | 2% |
| Restaurant | 70% | 25% | 4% | 1% |

**Focus:** small + medium = priority (decision speed + budget fit + delivery complexity)

---

## 5. Lead Flow Maturity Distribution

| Segment | None | Sporadic | Recurring | Growing |
|---------|------|----------|-----------|---------|
| Agency | 10% | 20% | 40% | 30% |
| Training | 25% | 30% | 30% | 15% |
| Clinic | 15% | 35% | 35% | 15% |
| Real Estate | 10% | 30% | 40% | 20% |
| Recruitment | 20% | 30% | 35% | 15% |
| Prof Services | 35% | 35% | 20% | 10% |
| Local SaaS | 10% | 20% | 40% | 30% |
| Education | 20% | 30% | 35% | 15% |
| Logistics | 30% | 35% | 25% | 10% |
| Restaurant | 35% | 35% | 25% | 5% |

**Best leads:** Recurring + Growing (الـ 70%+)

---

## 6. Sales Process Maturity Distribution

| Segment | None | Ad-hoc | Documented | Optimized |
|---------|------|--------|------------|-----------|
| Agency | 25% | 40% | 25% | 10% |
| Training | 50% | 30% | 15% | 5% |
| Clinic | 55% | 30% | 10% | 5% |
| Real Estate | 45% | 35% | 15% | 5% |
| Recruitment | 40% | 35% | 20% | 5% |
| Prof Services | 35% | 40% | 20% | 5% |
| Local SaaS | 20% | 35% | 30% | 15% |
| Education | 40% | 35% | 20% | 5% |
| Logistics | 45% | 35% | 15% | 5% |
| Restaurant | 60% | 30% | 8% | 2% |

**Best fit:** Documented + Optimized (الـ 25-30%+)

---

## 7. Sub-Segments Worth Noting

### 7.1 Saudi Government Tenders (GOV)
- Volume low but avg deal size high
- **Decision cycle:** 6-18 شهر
- **Risk:** high (procurement, compliance)
- **Recommendation:** not focus now

### 7.2 Holding Companies (multi-vertical)
- Volume low but avg deal size very high
- **Decision cycle:** 3-6 months
- **Risk:** medium (multi-stakeholder)
- **Recommendation:** Year 2+

### 7.3 Multi-Brand Retail (e.g., fashion, F&B chains)
- Volume medium, avg deal high
- **Decision cycle:** 30-60 يوم
- **Risk:** medium
- **Recommendation:** Restaurant groups overlap

### 7.4 EdTech / HealthTech Startups
- Volume low, deal size medium
- **Decision cycle:** 21-45 يوم
- **Risk:** low (digital native)
- **Recommendation:** Year 2 (Local SaaS adjacency)

---

## 8. Geographic Segmentation

| المنطقة | الحجم | density | focus |
|--------|------|---------|-------|
| Riyadh | high | highest | P1 |
| Jeddah | high | high | P1 |
| Dammam / Eastern | medium | medium | P2 |
| Makkah / Madinah | low | low | P3 |
| Other cities | low | low | P3 (year 2) |

**التفصيل:** `MARKET_INTELLIGENCE_SAUDI_SAAS_MARKET_AR.md`

---

## 9. Arabic vs English Speaking

| نوع العميل | اللغة | التقدير |
|------------|-------|---------|
| Saudi B2B SMEs | Arabic | 80% |
| International B2B in KSA | English | 15% |
| Saudi enterprise | Arabic + English | 5% |

**Default:** Arabic first content; English for international.

---

## 10. Companion Files

- ICP: `ICP_MATRIX_AR.md` + `data/commercial/icp_segments.yaml`
- Personas: `BUYER_PERSONAS_AR.md`
- Disqualifiers: `DISQUALIFICATION_RULES_AR.md`
- Priority: `reports/commercial/ICP_PRIORITY_REPORT.md`

---

**كل رقم في هذا الملف `is_estimate` ما لم يأت من مصدر موثّق. لا ادعاء بـ TAM/SAM/SOM بدون labelled source.**
