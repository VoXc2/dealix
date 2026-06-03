# Business Need Intelligence — فهرس الطبقة

طبقة ذكاء احتياج الأعمال في Dealix: تكتشف احتياج كل قطاع، تربطه بنظام عام جاهز،
تخصّصه، وتجهّز الإيميل/الاتصال/العرض/التسليم — مع إبقاء الموقع العام بسيطًا
(5 أنظمة + صفحات قطاعات + تشخيص).

## المستندات

| الملف | الغرض |
|-------|-------|
| [BUSINESS_NEED_INTELLIGENCE_ENGINE_AR.md](./BUSINESS_NEED_INTELLIGENCE_ENGINE_AR.md) | المحرك والمبادئ والـ pipeline |
| [NEED_TO_SYSTEM_ROUTER_AR.md](./NEED_TO_SYSTEM_ROUTER_AR.md) | الاحتياج → النظام العام/المتخصص |
| [SECTOR_NEED_MAP_AR.md](./SECTOR_NEED_MAP_AR.md) | القطاع → أقوى احتياجاته |
| [SECTOR_SIGNAL_LIBRARY_AR.md](./SECTOR_SIGNAL_LIBRARY_AR.md) | الإشارات العلنية لكل قطاع |
| [SPECIALIZED_SPRINT_LIBRARY_AR.md](./SPECIALIZED_SPRINT_LIBRARY_AR.md) | 20 سبرنتًا متخصصًا |
| [BUYER_ROLE_BY_NEED_AR.md](./BUYER_ROLE_BY_NEED_AR.md) | المشتري حسب الاحتياج |
| [DELIVERY_VARIANT_BY_SECTOR_AR.md](./DELIVERY_VARIANT_BY_SECTOR_AR.md) | عقد التسليم لكل قطاع |

## البيانات (مصدر الحقيقة)

`data/business_need_intelligence/*.yaml` — يقرؤها ويتحقق منها
`scripts/business_need_validate.py`.

## المخططات (Schemas)

`schemas/business_need.schema.json` · `schemas/specialized_sprint.schema.json` ·
`schemas/need_to_system_route.schema.json` · `schemas/account_pack_need_intelligence.schema.json`

## التقارير

`reports/business_need_intelligence/` — كشف يومي، أعلى الاحتياجات حسب القطاع،
مراجعة التوجيه، والتقرير النهائي للتوسعة.

## الموقع العام

الواجهة العامة تبقى بسيطة. هندسة المعلومات ومصدر بيانات الصفحات في
[`../site/SOLUTIONS_PAGE_IA_AR.md`](../site/SOLUTIONS_PAGE_IA_AR.md) و
`data/business_need_intelligence/sector_solutions.yaml`.

## التحقق

```bash
python3 scripts/business_need_validate.py   # أو: npm run bni:validate
```
