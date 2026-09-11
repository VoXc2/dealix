# Dealix Expanded Staff Registry — الهيكلية الكاملة لإدارة السوق كله

> Core 5 + Extended 8 = 13 — يحكمها 5 الأساسيون، الموسعون متخصصون مؤقتون/دائمون حسب الحاجة، كلهم تحت حوكمة واحدة

## الفلسفة
- 5 وكلاء أساسيون (pm, sales, delivery, engineer, content) يبقون النواة — `One Company, Five Core`
- 8 موسعون يغطون السوق كاملاً بشكل موسع — ليس 44 مشروع، بل 13 دورًا واضحًا
- كل موسع يتبع لأحد الأساسيين (owner_agent)، لا يصبح شركة منفصلة

## الهيكل الموسع (13)

| # | الوكيل | المالك الأساسي | المهمة |
|---|--------|----------------|--------|
| 6 | dealix-research | dealix-pm | رادار السوق، Etimad، ZATCA، MISA، منافسين |
| 7 | dealix-partner | dealix-sales | شراكات، تحالفات، توزيع، سوق |
| 8 | dealix-finance | dealix-pm | حقيقة مالية، تسعير، هامش، تحصيل |
| 9 | dealix-legal | dealix-pm | امتثال PDPL/NCA، عقود، مناقصات |
| 10 | dealix-support | dealix-delivery | دعم عملاء، نجاح، توسع |
| 11 | dealix-data | dealix-engineer | بيانات، جودة، تكامل، RAG |
| 12 | dealix-growth | dealix-content | نمو، SEO/AEO، محتوى، توزيع |
| 13 | dealix-hr | dealix-pm | توظيف، تدريب، عمليات موارد |

## الحوكمة
- كل موسع `L1` افتراضيًا، `L2` للكود عند الحاجة، `L5` للخارجي
- DeepWIP ≤3 لا يزال على المستوى الأساسي — الموسعون لا يستهلكون خانات DeepWIP مباشرة، بل عبر الأساسيين
- Audit: `python scripts/audit_agent_team.py` سيعد 13 الآن (5+8)، كان 5 — حدثنا الاختبار ليسمح ≥5
