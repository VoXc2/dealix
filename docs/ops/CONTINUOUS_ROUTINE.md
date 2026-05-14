# Continuous Routine — الإيقاع المستمر
## Wiring `scripts/daily_routine.py` into a continuous schedule · Wave 17

---

## The promise — الوعد

One command, fifteen minutes or less every morning, idempotent on re-run, and structurally incapable of sending external messages, charging payment, or calling an LLM. `scripts/daily_routine.py` composes the daily PM digest (`dealix_pm_daily.py`), the warm-list outreach drafter (`warm_list_outreach.py`), the WhatsApp draft generator (`whatsapp_draft.py`), and in-process renewal-window and lead-waiting checks. The output is a single bilingual markdown file at `data/daily_routine/YYYY-MM-DD.md` that the founder reads, edits, and acts on manually.

أمر واحد، خمس عشرة دقيقة أو أقل كل صباح، نتائجه ثابتة عند إعادة التشغيل، وغير قادر هندسياً على إرسال رسائل خارجية أو خصم دفعات أو استدعاء LLM. السكريبت يُركّب الموجز اليومي ومسوّد التواصل الدافئ ومسوّد الواتساب وفحوصات نافذة التجديد وانتظار العميل. المخرَج ملف ماركداون ثنائي اللغة يقرأه المؤسس ويعدّل ويتصرف يدوياً.

---

## Local cron (founder's laptop) — كرون محلي

Schedule the routine at 7:30 AM Riyadh time (UTC+3 → 04:30 UTC) with a single crontab line. Logs append to `~/.dealix/daily_routine.log` with timestamp + exit code so a missed morning is visible the next day.

```bash
# crontab -e — runs daily at 07:30 Riyadh (04:30 UTC)
30 4 * * * cd /Users/founder/dealix && /usr/bin/env python3 scripts/daily_routine.py >> ~/.dealix/daily_routine.log 2>&1
```

For macOS, `launchd` is the supported alternative when the laptop is closed at the cron hour and you want the run to fire on next wake instead of being skipped.

```xml
<!-- ~/Library/LaunchAgents/me.dealix.daily.plist -->
<plist version="1.0"><dict>
  <key>Label</key><string>me.dealix.daily</string>
  <key>ProgramArguments</key><array>
    <string>/usr/bin/env</string><string>python3</string>
    <string>/Users/founder/dealix/scripts/daily_routine.py</string>
  </array>
  <key>StartCalendarInterval</key><dict>
    <key>Hour</key><integer>7</integer><key>Minute</key><integer>30</integer>
  </dict>
  <key>RunAtLoad</key><false/>
  <key>StandardOutPath</key><string>/Users/founder/.dealix/daily_routine.log</string>
  <key>StandardErrorPath</key><string>/Users/founder/.dealix/daily_routine.log</string>
</dict></plist>
```

Load with `launchctl load ~/Library/LaunchAgents/me.dealix.daily.plist`. To verify the next firing time: `launchctl list | grep dealix.daily`.

---

## Railway cron jobs (production) — كرون Railway

For server-side execution (founder is travelling, laptop off, or simply prefers separation), Railway runs the routine on its scheduler. Add a cron service alongside the API service in `railway.json` and bind the same Python entrypoint via `RAILWAY_RUN_COMMAND`.

```json
{
  "$schema": "https://railway.com/railway.schema.json",
  "services": [
    {
      "name": "daily-routine",
      "source": { "repo": "github.com/dealix/dealix" },
      "build": { "builder": "NIXPACKS" },
      "deploy": {
        "startCommand": "python scripts/daily_routine.py",
        "cronSchedule": "30 4 * * *",
        "restartPolicyType": "NEVER"
      }
    }
  ]
}
```

The `RAILWAY_RUN_COMMAND` env var pattern lets the same image serve multiple cron entrypoints — set `RAILWAY_RUN_COMMAND=scripts/daily_routine.py --quick` on a second cron service for an evening idempotent re-run, and the audit chain will record both runs without duplicating work.

نمط `RAILWAY_RUN_COMMAND` يسمح لنفس الصورة أن تخدم عدة نقاط دخول كرون. التشغيل الثاني المسائي بـ`--quick` يدوّن في سلسلة التدقيق دون تكرار العمل.

---

## Manual mobile invocation — تشغيل يدوي من الجوال

When neither cron has fired and the founder is mobile, SSH into the production host from Termius (iOS / Android) or Blink Shell and trigger the routine with one shortcut. The output file is read-only on the phone and ready in under a minute.

```bash
# Termius / Blink shortcut command
ssh dealix-prod 'cd /app && python scripts/daily_routine.py --quick && cat data/daily_routine/$(date +%F).md'
```

The `--quick` flag skips re-rendering the previous-day comparison and short-circuits if today's file already exists. Output appears in `data/daily_routine/YYYY-MM-DD.md` and the same file is fetchable through the read-only API endpoint `GET /api/v1/daily-routine/today` for founders who prefer reading inside the dashboard.

عند غياب جدولة الكرون ووجود المؤسس متنقلاً، اتصال SSH من Termius أو Blink مع اختصار واحد يكفي. المخرَج يظهر في نفس مجلد التشغيل الجدولي، وقابل للقراءة من نقطة نهاية API للقراءة فقط داخل لوحة التحكم.

---

## Verification — التحقق

After any wiring change (cron, launchd, Railway, manual), run the verification one-liner once and confirm the output renders cleanly:

```bash
python scripts/daily_routine.py --quick && cat data/daily_routine/$(date +%F).md
```

A clean run produces a bilingual file with five sections: PM digest, warm-list draft list, WhatsApp draft list, renewal window flags, lead-waiting flags. Each draft is marked `DRAFT — pending founder approval`. Zero external sends. Zero charges. Zero LLM calls.

---

## Doctrine reminders — تذكيرات العقيدة

The continuous routine is intentionally boring and inert. Even if a misconfigured cron fires every minute, it cannot violate any of the eleven non-negotiables — the audit chain proves this on every run. Specifically:

- **Never sends.** The script writes drafts to `data/daily_routine/`. The `safe_send_gateway` is not imported, and external send code paths are absent from the call graph (commitments #2, #3, #8).
- **Never charges.** No payment processor SDK is imported. `intent_only` remains the only state any retainer or Sprint reaches via this path (commitment #8).
- **Never calls an LLM.** The script reads from local Source Passports and the warm-list registry only. No outbound model call is possible from this entrypoint (commitments #4, #7).
- **Idempotent.** Re-running the same day produces the same output file with the same content hash. The audit chain records each invocation but does not duplicate work (commitment #9).

السكريبت ساكن بقصد. حتى لو شغّله الكرون كل دقيقة، لا يستطيع كسر أي من الـ١١ التزاماً غير القابل للتفاوض — سلسلة التدقيق تُثبت ذلك في كل تشغيل.

---

## Cross-links

- The Dealix Promise — [`docs/THE_DEALIX_PROMISE.md`](../THE_DEALIX_PROMISE.md)
- Daily operating loop — [`docs/ops/DAILY_OPERATING_LOOP.md`](DAILY_OPERATING_LOOP.md)
- Founder 90-day cadence — [`docs/ops/FOUNDER_90_DAY_CADENCE.md`](FOUNDER_90_DAY_CADENCE.md)

---

_Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة._
