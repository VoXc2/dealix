# Monthly Board Memo — أرشيف القرار حتى بلا مجلس

كل شهر، أنشئ **Board Memo** حتى لو لم يكن لديك مجلس رسمي. الهدف: **أرشيف قرارات الشركة** — أصل لاحقًا للشركاء، التوظيف، أو التمويل.

## Template

```markdown
# Dealix Monthly Board Memo
## 1. Executive Summary
## 2. Revenue Quality
## 3. Proof & Value
## 4. Governance & Incidents
## 5. Client Adoption
## 6. Productization
## 7. Capital Assets Created
## 8. Market Intelligence
## 9. Business Unit Maturity
## 10. Stop / Kill Decisions
## 11. Capital Allocation
## 12. Next Strategic Bets
```

## التحقق البرمجي

أقسام المذكرة الشهرية (slug keys) معرّفة في `operating_rhythm_os/board_memo.py` — يمكن استخدامها للتحقق من اكتمال المسودة.

## الربط

- `board_decision_os/board_memo_generator.py` — تصنيف قريب للمذكرات داخل المنتج.
- [QUARTERLY_STRATEGIC_REVIEW.md](QUARTERLY_STRATEGIC_REVIEW.md) — مستوى أعلى من الزمن.
