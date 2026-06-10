# Proof-Safe Arabic Language — اللغة العربية الآمنة للإثبات

## Evidence Levels L0-L5

All claims made by Dealix must be backed by appropriate evidence.
This guide defines evidence levels and safe language for each.

### Level Summary

| Level | Name (EN) | Name (AR) | Evidence Type |
|-------|-----------|-----------|---------------|
| L0 | No Evidence | بدون دليل | No claim allowed |
| L1 | Anecdotal | حكائي | "our client said" |
| L2 | Self-Reported | تبليغي | "client reported" |
| L3 | Observed | ملاحظ | "we measured" |
| L4 | Verified | موثّق | Third-party verified |
| L5 | Certified | معتمد | Formal certification |

## Detail by Level

### L0 — No Evidence (بدون دليل)
**No claims allowed.** Only generic, non-specific language.

**Safe phrases:**
- "نسعى لتحقيق"
- "نعمل على"
- "هدفنا"
- "من أولوياتنا"
- "نلتزم بـ"

**Example**: "نلتزم بتقديم أفضل الخدمات لعملائنا"

---

### L1 — Anecdotal (حكائي)
**Only anecdotal evidence from individual client statements.**

**Safe phrases:**
- "ذكر أحد العملاء"
- "أخبرنا عميل"
- "حسب ما أفاد به أحد العملاء"

**Example**: "ذكر أحد العملاء أن خدماتنا ساعدتهم في تحسين سير العمل"

**Footer**: "المعلومات المذكورة مبنية على تقارير العملاء. النتائج الفعلية قد تختلف."

---

### L2 — Self-Reported (تبليغي)
**Client-reported outcomes (not independently verified).**

**Safe phrases:**
- "أبلغنا العميل بتحسن"
- "بناءً على تقرير العميل"
- "حسب ما ورد من العميل"

**Example**: "أبلغنا عميلنا في قطاع التجزئة بزيادة في المبيعات بنسبة ٢٠٪"

**Footer**: "النتائج مبنية على ما أفاد به العميل ولم تخضع لتدقيق مستقل."

---

### L3 — Observed (ملاحظ)
**Measured by Dealix — quantitative data available.**

**Safe phrases:**
- "بناءً على قياساتنا"
- "أظهرت نتائجنا"
- "لاحظنا تحسناً بنسبة"
- "سجلنا زيادة بنسبة"
- "بياناتنا تشير إلى"
- "أظهر التحليل"

**Example**: "أظهرت نتائجنا تحسناً في كفاءة العمليات بنسبة ٣٥٪ خلال ثلاثة أشهر"

**Footer**: "النتائج المذكورة مبنية على قياساتنا. قد تختلف النتائج حسب الحالة."

---

### L4 — Verified (موثّق)
**Independently verified by third party.**

**Safe phrases:**
- "وفقاً لتقرير التدقيق المستقل"
- "أكدت جهة خارجية"
- "حصلنا على شهادة من"
- "تم التحقق من قبل"
- "أثبتت الدراسة المستقلة"

**Example**: "أكد تقرير التدقيق المستقل من شركة ديلويت تحقيق وفورات بنسبة ٢٥٪"

**Footer**: "النتائج تم التحقق منها من قبل جهة مستقلة. جميع الادعاءات مدعومة بأدلة."

---

### L5 — Certified (معتمد)
**Formally certified (ISO, G-Mark, government certification).**

**Safe phrases:**
- "حاصل على شهادة"
- "معتمد من"
- "حائز على جائزة"
- "مطابق للمعيار"
- "حاصل على اعتماد"

**Example**: "حاصل على شهادة ISO 27001 لأمن المعلومات من هيئة التقييس السعودية"

**Footer**: "جميع الادعاءات معتمدة رسمياً ومدعومة بشهادات موثقة."

## Claim Assessment Examples

| Claim | Required Level | 5afe at L2? | Safe at L4? |
|-------|---------------|-------------|-------------|
| "نسعى لتقديم أفضل الخدمات" | L0 | ✅ | ✅ |
| "أخبرنا العميل بتحسن" | L1 | ✅ | ✅ |
| "زادت مبيعاتهم بنسبة ٢٠٪" | L3 | ❌ (L2=L2<L3) | ✅ |
| "الأفضل في السوق" | L4 | ❌ | ✅ |
| "حاصل على شهادة ISO" | L5 | ❌ | ❌ (L4<L5) |

## Usage

```python
from auto_client_acquisition.saudi_layer.proof_safe_language import (
    ProofLevel, assess_claim_safety, safe_phrase_for_level, get_proof_safe_footer
)

# Assess a claim
assessment = assess_claim_safety(
    "نسبة النجاح ٩٥٪",
    evidence_level=ProofLevel.L3
)

# Get safe phrases for a level
phrases = safe_phrase_for_level(ProofLevel.L3)
# Returns: GENERIC_SAFE_PHRASES + ALLOWED_PHRASES_L3

# Get proof-safe footer
footer = get_proof_safe_footer(ProofLevel.L3)
```

## Code Reference

- **Module**: `auto_client_acquisition/saudi_layer/proof_safe_language.py`
- **Classes**: `ProofLevel` (IntEnum), `ClaimAssessment` (dataclass)
- **Constants**: `LEVEL_LABELS`, `ALLOWED_PHRASES_L3`, `ALLOWED_PHRASES_L4`, `ALLOWED_PHRASES_L5`, `GENERIC_SAFE_PHRASES`, `CLAIM_PATTERNS`
- **Functions**: `assess_claim_safety()`, `safe_phrase_for_level()`, `get_proof_safe_footer()`
