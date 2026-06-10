# Arabic Executive QA — تقييم الجودة التنفيذي العربي

## 12 QA Dimensions

The Arabic QA system evaluates content across 12 weighted dimensions:

| # | Dimension (EN) | Dimension (AR) | Weight | Minimum Pass |
|---|---------------|----------------|--------|-------------|
| 1 | Clarity | الوضوح | 15% | 60 |
| 2 | Executive Tone | النبرة التنفيذية | 12% | 60 |
| 3 | Saudi Business Fit | ملاءمة السوق السعودي | 10% | 60 |
| 4 | No Exaggeration | عدم المبالغة | 12% | 70 |
| 5 | Claim Safety | أمان الادعاءات | 12% | 70 |
| 6 | Actionability | قابلية التنفيذ | 8% | 50 |
| 7 | Grammar Correctness | الصحة النحوية | 7% | 60 |
| 8 | Cultural Appropriateness | الملاءمة الثقافية | 8% | 60 |
| 9 | Formatting Quality | جودة التنسيق | 4% | 50 |
| 10 | Honorific Usage | استخدام الألقاب | 4% | 50 |
| 11 | PDPL Compliance | الامتثال لخصوصية البيانات | 5% | 70 |
| 12 | Vision 2030 Alignment | التوافق مع رؤية ٢٠٣٠ | 3% | 30 |

## Scoring Levels

| Score Range | Level | Meaning |
|-------------|-------|---------|
| 90-100 | ممتاز (Excellent) | Ready for executive presentation |
| 75-89 | جيد (Good) | Minor improvements needed |
| 60-74 | مقبول (Acceptable) | Several improvements needed |
| 0-59 | ضعيف (Weak) | Requires significant revision |

## Dimension Descriptions with Examples

### 1. Clarity — الوضوح
- **Good**: "نقدم حلولاً متكاملة لتحسين إنتاجية فريقك بنسبة تصل إلى ٣٠٪"
- **Bad**: "من خلال استراتيجياتنا المتطورة والمنهجيات الحديثة نحقق قيمة مضافة لعملائنا عبر تمكينهم وتحسين كفاءتهم التشغيلية"
- **Rules**: Short sentences (25 words max), one idea per sentence, use bullet points for lists

### 2. Executive Tone — النبرة التنفيذية
- **Good**: "يقود هذا المشروع نحو تحقيق أهداف التحول الرقمي وفق رؤية المملكة ٢٠٣٠"
- **Bad**: "يعجبني هذا المشروع لأنه مفيد ورائع جداً"
- **Rules**: Professional, decisive, confident; avoid emotional language; use business terminology

### 3. Saudi Business Fit — ملاءمة السوق السعودي
- **Good**: "متوافق مع نظام حماية البيانات الشخصية الصادر بالمرسوم الملكي م/١٤٨"
- **Bad**: "نحن نستخدم أفضل الممارسات العالمية" (too generic)
- **Rules**: Reference Saudi regulations, Vision 2030, local examples; use Saudi business terminology

### 4. No Exaggeration — عدم المبالغة
- **Good**: "من الشركات الرائدة في مجال التقنية في المملكة"
- **Bad**: "الشركة الأولى والأفضل على مستوى المملكة بل والعالم"
- **Rules**: Avoid superlatives without proof; use "من الـ" constructions; qualify claims

### 5. Claim Safety — أمان الادعاءات
- **Good**: "تساعد حلولنا في تحسين كفاءة العمليات بناءً على نتائج قياسية"
- **Bad**: "نضمن زيادة أرباحك بنسبة ١٠٠٪"
- **Rules**: Match claims to evidence level; no guarantees; use proof-safe language

### 6. Actionability — قابلية التنفيذ
- **Good**: "في الأسبوع الأول: نقيّم وضعك الحالي، ثم نقدم خطة عمل مع جدول زمني"
- **Bad**: "سنحقق نقلة نوعية في أدائك" (unclear how)
- **Rules**: Clear next steps, specific timelines, concrete deliverables

### 7. Grammar Correctness — الصحة النحوية
- **Common Issues**: إعراب خاطئ, همزة القطع والوصل, التاء المربوطة والمفتوحة
- **Rules**: Use formal فصحى (not dialect), check إعراب, verify spelling of همزات

### 8. Cultural Appropriateness — الملاءمة الثقافية
- **Good**: Uses appropriate Islamic expressions, respects Saudi traditions
- **Bad**: Uses Levantine/Egyptian dialect terms
- **Rules**: No جدعان, باشا, افندي; Use السلام عليكم; Respect religious sensitivities

### 9. Formatting Quality — جودة التنسيق
- **Good**: Right-aligned, proper Arabic punctuation (؛ ، ؟), Arabic-Indic numbers
- **Bad**: Left-aligned Arabic, English punctuation in Arabic text, mixed fonts
- **Rules**: Right-to-left alignment, Arabic punctuation marks, consistent fonts

### 10. Honorific Usage — استخدام الألقاب
- **Examples**: الأستاذ, الدكتور, المهندس, سعادة
- **Rules**: Use appropriate honorifics based on known titles; when unknown, use الأستاذ

### 11. PDPL Compliance — الامتثال لخصوصية البيانات
- **Required Elements**: الغرض, أساس المعالجة, مدة الاحتفاظ, حقوق صاحب البيانات
- **Rules**: Include PDPL disclosure; mention data retention period; specify data subject rights

### 12. Vision 2030 Alignment — التوافق مع رؤية ٢٠٣٠
- **Good**: "يتماشى هذا المشروع مع أهداف برنامج التحول الوطني ورؤية المملكة ٢٠٣٠"
- **Bad**: No mention of national context when relevant
- **Rules**: Reference specific Vision 2030 programs when appropriate; don't over-reference

## Scoring Formula

```
Weighted Score = Σ(dimension_score × weight) / Σ(weights)
Final Score = round(Weighted Score)
```

## Usage

```python
from auto_client_acquisition.saudi_layer.arabic_qa import (
    ArabicQADimensions, arabic_qa_score, evaluate_qa
)

dims = ArabicQADimensions(
    clarity=90,
    executive_tone=85,
    saudi_business_fit=80,
    no_exaggeration=75,
    claim_safety=70,
    actionability=88,
    grammar_correctness=95,
    cultural_appropriateness=90,
    formatting_quality=85,
    honorific_usage=75,
    pdpl_compliance=65,
    vision_2030_alignment=70,
)

score = arabic_qa_score(dims)
result = evaluate_qa(dims)
```

## Code Reference

- **Module**: `auto_client_acquisition/saudi_layer/arabic_qa.py`
- **Classes**: `ArabicQADimensions`, `QAResult`
- **Functions**: `arabic_qa_score()`, `evaluate_qa()`, `find_lowest_dimension()`
