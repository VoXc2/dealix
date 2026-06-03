# Dealix Ultimate Scale OS — نظام التوسع الشامل

> الانتقال من "جاهز للإطلاق" إلى **مصنع نمو وتشغيل قابل للتوسع بحدود واضحة**.

---

## المعادلة

```txt
Dealix Ultimate Scale OS
=
Launch Readiness
+ Agent Governance
+ Revenue Experimentation
+ Deliverability Control
+ Sector Expansion
+ Delivery Capacity Planning
+ Founder War Room
```

Dealix لا يكتفي بأنه يشتغل؛ يصير قادرًا على:

- **التوسع يوميًا** بحدود إنتاج وإرسال مضبوطة (Scale Modes).
- **التعلّم من السوق** عبر تجارب أسبوعية مضبوطة (Revenue Experimentation).
- **رفع جودة الاستهداف** عبر Account Packs و Need Intelligence.
- **حماية الدومين** عبر Deliverability Control.
- **منع الوكلاء من التصرف خارج الحدود** عبر Agent Governance و Autonomy Levels.

---

## الطبقات السبع

| # | الطبقة | الملف/الحزمة | الهدف |
|---|--------|--------------|-------|
| 1 | Launch Readiness | `reports/launch/` (موروث) | الأساس: النظام يشتغل |
| 2 | Agent Governance | `docs/agents/` | لكل وكيل صلاحية محددة |
| 3 | Revenue Experimentation | `docs/experiments/` | نتعلم بمتغيّر واحد كل مرة |
| 4 | Deliverability Control | `docs/deliverability/` | الإنتاج شيء والإرسال شيء آخر |
| 5 | Sector Expansion | `docs/scale/SECTOR_EXPANSION_POLICY_AR.md` | متى ندخل قطاعًا جديدًا |
| 6 | Delivery Capacity | `docs/scale/DELIVERY_CAPACITY_PLANNING_AR.md` | لا تبع أكثر من قدرتك |
| 7 | Founder War Room | `docs/scale/FOUNDER_WAR_ROOM_AR.md` | قرار يومي وأسبوعي واضح |

---

## القاعدة الحاسمة

```txt
Dealix agents may generate.
Dealix agents may recommend.
Dealix agents may prepare.
Dealix agents may not externally send, call, price-change, contract,
or start delivery without founder approval.
```

---

## مصادر الحقيقة (Machine-Readable State)

| الملف | المحتوى |
|-------|---------|
| `company_os/agents/agent_registry.json` | سجل الوكلاء ومستوياتهم وصلاحياتهم |
| `company_os/scale/scale_state.json` | الوضع الحالي وحدود كل Scale Mode |
| `company_os/scale/ultimate_scorecard.json` | أوزان ودرجات Ultimate Scale Scorecard |
| `company_os/deliverability/deliverability_state.json` | حالة SPF/DKIM/DMARC والسبام |
| `company_os/experiments/experiments.json` | سجل التجارب الأسبوعية |
| `company_os/delivery/capacity.json` | نموذج قدرة التسليم والاستغلال |
| `company_os/security/prompt_injection_tests.json` | اختبارات حقن الأوامر والنتائج |

---

## أوامر التشغيل

```bash
python dealix.py scale-score          # حساب Ultimate Scale Scorecard ووضع الجاهزية
python dealix.py agent-audit          # تدقيق حوكمة وصلاحيات الوكلاء
python dealix.py deliverability-check # فحص جاهزية الإرسال
python dealix.py experiment-review    # مراجعة سجل التجارب
python dealix.py delivery-capacity    # مراجعة استغلال قدرة التسليم
python dealix.py war-room --dry-run   # تقرير War Room اليومي (بدون أي إجراء خارجي)
python dealix.py scale-all            # تشغيل كل فحوصات التوسع
```

---

## شرط الانتقال إلى Scale Mode

```txt
Launch Score >= 90
Ultimate Scale Score >= 90
No-Go blockers = 0
Delivery capacity utilization < 80%
Email deliverability checks pass
Agent permission audit passes
Security red-team checks pass
Weekly learning report exists
```

ما لم تتحقق كل هذه الشروط، يبقى النظام في الوضع المناسب (Controlled Growth أو أدنى)
ولا يُسمح بالقفز إلى Scale.

---

## تعريف "أبعد مدى"

```txt
Dealix is:
Launch Ready
+ Scale Ready
+ Agent Governance Ready
+ Delivery Capacity Aware
+ Deliverability Controlled
+ Security Hardened
+ Founder War Room Ready
```

---

*Version: 1.0 | Last Updated: 2026-06-03 | Owner: Founder*
