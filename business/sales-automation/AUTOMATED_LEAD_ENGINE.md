# Automated Lead Engine (Dealix)

## المبدأ
ليدز صحية تجي من:
1. **إشارات عامة** مرئية (موقع، إعلانات، تقييمات، محتوى)
2. **مصادر رسمية** فقط (data.gov.sa، APIs معتمدة، ملفات يقدمها المؤسس)
3. **بحث يدوي** يقوم به المؤسس ويسجل ملاحظة مهيكلة

ليدز غير صحية:
- تجريف لبيانات خاصة
- شراء قوائم
- scraping لشبكات اجتماعية
- بيانات بدون مصدر

## دورة حياة الليد
1. **Source** — مصدر موثّق (URL أو note)
2. **Score** — نقاط ICP + BANT + ضعف
3. **Draft** — مسوّدة عربي/إنجليزي
4. **Review** — مراجعة بشرية (approved / rejected)
5. **Send** — إرسال يدوي فقط
6. **Track** — متابعة + notes + stage update
7. **Archive** — أرشفة دورية بدون حذف بيانات

## المصادر المعتمدة
| Source | Auto-Send | Note |
|--------|-----------|------|
| Open Data SA | No | public aggregate only |
| CSV (founder) | No | source required |
| Manual research | No | URL/quote required |
| Website signal (local file) | No | no crawling |
| Google Places (official) | No | rate-limit aware |
| HubSpot (official) | No | OAuth read-only |
| WhatsApp Business (official) | No | templates only |
| Referral | No | written consent |

## المخرجات
- `business/_data/leads.json` — كل الليدز
- `business/_data/scored_leads.json` — الليدز المسجّلة
- `business/_data/outreach_review_queue.json` — طابور المراجعة

## السكربتات
- `scripts/import_leads_csv.py`
- `scripts/score_leads.py`
- `scripts/generate_outreach_drafts.py`
- `scripts/approve_outreach_draft.py`
- `scripts/reject_outreach_draft.py`
- `scripts/generate_followup_queue.py`
