# Dealix — Founder Next Steps · ماذا تفعل الآن

> هذا الملف **مصدر الحقيقة الواحد** للفاوندر: ماذا يفعل اليوم، هذا الأسبوع، هذا الشهر، هذا الربع. حدّثه بعد كل milestone.
>
> **آخر تحديث:** 2026-05-28 · **الحالة:** فك blockers الإطلاق (Moyasar + أول عميل)

---

## 1) صورة الحال (One-paragraph state)

Dealix **منصة جاهزة تقنياً** (FastAPI + 200+ router + alembic head واحد + doctrine 11 enforced في tests). الإيراد **مغلق على Moyasar KYC**. Pipeline يحوي 50 اسم لكن **صفر رسائل مرسلة**. لا منشورات LinkedIn حية، لا cases studies، لا عميل دافع. الفجوة الكبرى: **التنفيذ التجاري** لا التقنية.

---

## 2) قبل أي شي (Pre-flight لو أول مرة تشغل الريبو)

```bash
make first-setup       # تفاعلي — يولّد .env + ينصّب hooks + يتأكد api.main يستورد
make doctor            # env-check + alembic single head + security smoke
make run               # uvicorn على :8000
```

في terminal ثاني:
```bash
curl localhost:8000/health
curl -H "X-API-Key: $ADMIN_KEY" localhost:8000/api/v1/founder/dashboard
make cockpit           # founder daily brief
```

لو أي خطوة فشلت → `make doctor` يعرض السبب. الـ optional routers (value_os, data_os, agent_os) لو فشلت تطبع الـ traceback كاملاً في الـ log الآن (تم الإصلاح).

---

## 3) هذا الأسبوع (7 أيام) — Top-3 only

| # | الإجراء | من ينفذ | الناتج المتوقع | الموعد |
|---|--------|---------|----------------|--------|
| 1 | **تفعيل Moyasar KYC** — افتح `dashboard.moyasar.com` → ارفع CR + ID + بنك → submit. | الفاوندر | فك blocker الإيراد (1-3 أيام انتظار رد) | يوم 1 |
| 2 | **أرسل 3 DMs على LinkedIn** — انسخ من `dealix/launch_content_queue.md` للـ (Alassiri / Al-Zaini / Hariri). سجّل `sent_at` في `docs/ops/pipeline_tracker.csv`. | الفاوندر | أول حركة pipeline حقيقية | يوم 2 |
| 3 | **انشر Post #1 على LinkedIn** — من `linkedin_longform_posts.md`، الثلاثاء 09:00 السعودية. | الفاوندر | أول محتوى حي + بداية inbound | يوم 7 |

**قاعدة الأسبوع:** لا تبدأ مهمة #2 إلا إذا انتهت #1. لا قفز.

**Daily check (10 دقائق صباحاً):**
```bash
make cockpit                                  # bottleneck + hard gates + اليوم
curl -fs localhost:8000/health || echo "API down — investigate"
```

---

## 4) هذا الشهر (30 يوم) — 5 milestones

- [ ] **M1 — Moyasar live + 1 SAR test transaction verified** (نهاية أسبوع 1-2)
- [ ] **M2 — أول demo مجدول من warm intro** (نهاية أسبوع 2-3)
- [ ] **M3 — 3 منشورات LinkedIn (1/أسبوع) + 10K+ impressions** (نهاية أسبوع 4)
- [ ] **M4 — أول Sprint 499 SAR مدفوع + delivered + proof pack** (نهاية أسبوع 4)
- [ ] **M5 — Pipeline CSV محدّث أسبوعياً بـ replies + objections** (مستمر)

**أداة التتبع:** `python scripts/founder_daily_scorecard.py` يطبع تقدم الـ 5.

---

## 5) هذا الربع (90 يوم) — KPI targets

| KPI | Day 0 | Day 30 | Day 60 | Day 90 |
|-----|-------|--------|--------|--------|
| MRR (SAR) | 0 | 1,500 | 5,000 | 8,000–10,000 |
| Managed-ops customers | 0 | 0 | 1 | 2–3 |
| Sprints completed | 0 | 1 | 3 | 5–8 |
| Case studies (signed permission) | 0 | 0 | 1 | 3 |
| Founder hrs/wk on sales | 35 | 30 | 20 | <15 |

**أسبوعي:** يوم الأحد 09:00 → 30 دقيقة weekly brief (`scripts/dealix_founder_daily_brief.py --format json | jq`) + تحديث الجدول فوق.

---

## 6) فجوات تقنية مفتوحة (Polish — ليست blockers)

هذه ليست عاجلة، نفّذها لما يكون فيه نَفَس. كلها موثقة في `KNOWN_LIMITATIONS.md`:

1. **Frontend split (مقصود):** `frontend/` = customer UI (i18n، landing، checkout، portal، login، register، dashboard، offer). `apps/web/` = enterprise admin UI (control plane، agents، sandbox، safety، self-evolving). كلاهما كاننوني ومبني في CI. لا تحذفهما.
2. **Docs sprawl:** 16 ملف .md في الجذر + 428 مجلد `docs/`. تم تنظيف: `dealix-v2/`, `dashboard/`, `migrations/`, `dealix-1.worktrees/` محذوفة. باقي 11 ملف .md ينقلون لـ `docs/{category}/`.
3. **Integrations behind feature flags:** WhatsApp/Email/HubSpot لها doctrine gate `whatsapp_allow_live_send` (احترام no_live_send). لو احتجت إرسال حقيقي → اقرأ `docs/ops/LEAD_MACHINE_TOOLING.md` وفعّل الـ flag بعد approval workflow.
4. **Migrations:** `db/migrations/versions/` هو المصدر الوحيد (alembic.ini يشير له فقط). `supabase/migrations/` منفصل لـ Supabase project (لا تخلطه). `alembic/` يحوي env فقط.
5. **Coverage gate:** الآن 70%. الهدف 80% خلال شهر.

---

## 7) خطوط حمراء (Doctrine — لا تكسرها أبداً)

11 non-negotiables موضوحة في `AGENTS.md`. الأهم للفاوندر يومياً:

1. **no_live_send** — لا إرسال خارجي تلقائي. كل رسالة WhatsApp/Email/LinkedIn = founder approval قبل send.
2. **no_cold_whatsapp** — WhatsApp فقط مع موافقة سابقة (warm intro أو opt-in).
3. **no_fake_proof** — أي رقم، case study، أو شهادة → يحتاج evidence حقيقي مسجل في proof pack ledger.
4. **no_scraping** — صفر web scraping بدون إذن. استخدم APIs المرخصة فقط.
5. **no_unconsented_data** — كل lead يحتاج PDPL lawful basis مسجل.

لو شككت في commit أو فعل → `scripts/dealix_founder_rules.py` يطبعها بالعربي والإنجليزي.

---

## 8) أوامر اليومي (cheat-sheet)

```bash
make cockpit                              # brief اليومي
make doctor                               # health check
make run                                  # local API :8000
make test                                 # full pytest
python scripts/dealix_founder_daily_brief.py --out data/founder_briefs/$(date +%F).md
python scripts/founder_daily_scorecard.py # تقدم الـ 5 milestones
python scripts/dealix_status.py           # bilingual snapshot
```

**Endpoint مهم:**
- `GET /api/v1/founder/dashboard` — admin-gated (يحتاج `X-API-Key: $ADMIN_KEY`)
- `GET /api/v1/founder-summary` — daily summary public-safe
- `GET /api/v1/launch-status/public` — readiness gauges

---

## 9) متى تحدّث هذا الملف

- بعد كل Milestone (M1-M5)
- بعد أول عميل دافع → استبدل "صفر عملاء" بـ الرقم الحقيقي
- بعد أي تغيير في doctrine
- نهاية كل أسبوع (يوم الأحد بعد الـ weekly brief)

---

**الخلاصة:** الكود جاهز. التجارة لم تبدأ. الـ blocker الوحيد بين اليوم والإيراد = **Moyasar KYC + 3 DMs + Post #1**. ابدأ بهذه الثلاثة هذا الأسبوع، بقية الخطة تنبني عليها.
