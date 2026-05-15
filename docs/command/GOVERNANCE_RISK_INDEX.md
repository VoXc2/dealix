# Governance Risk Index — مؤشر مخاطر الحوكمة

لكل **مشروع** و**مخرج** و**مسار وكيل**: تجميع عوامل مخاطرة إلى مؤشر 0–100 (أعلى = أخطر).

## العوامل (تُقيَّم 0–100 خطرًا قبل المتوسط)

- PII sensitivity  
- external action potential  
- source uncertainty  
- claim risk  
- channel risk  
- agent autonomy  
- client industry sensitivity  

## القرار

| المتوسط | السلوك المقترح |
|---------|----------------|
| Low | allow |
| Medium | allow with review |
| High | require approval |
| Critical | block / escalate |

**ملاحظة:** يتماشى مع اتجاه **runtime governance** — تقييم أثناء التشغيل لا ضبط ثابت فقط؛ انظر [arXiv:2603.16586](https://arxiv.org/abs/2603.16586).

## الكود

`auto_client_acquisition/command_os/governance_risk_index.py` — متوسط العوامل ثم `governance_risk_band`.

**صعود:** [`SOVEREIGN_COMMAND_SYSTEM.md`](SOVEREIGN_COMMAND_SYSTEM.md)
