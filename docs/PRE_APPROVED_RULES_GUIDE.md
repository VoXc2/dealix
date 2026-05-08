# Founder Pre-Approved Rules — Guide (Wave 7.7)

## لماذا هذا الملف موجود | Why this exists

كمؤسس، تقضي حوالي 45 دقيقة يومياً تضغط "موافق" على ردود متشابهة تماماً
(أسئلة شائعة، تأكيدات الفواتير، اختيار وقت الاجتماع). القواعد المسبقة
الموقعة بـ HMAC تختصر هذا إلى ~10 دقائق دون التخلي عن الإنسان في الحلقة.

As founder, you spend ~45 min/day clicking "approve" on near-identical
replies (FAQ answers, invoice acks, meeting-slot picks). HMAC-signed
pre-approved rules cut that to ~10 min while keeping the human in the
loop on every high-risk action.

## القواعد الأربعة الصلبة التي لا تنحني | Four hard rules that NEVER bend

1. **حظر القنوات | Channel block**
   WhatsApp / LinkedIn / Phone are PERMANENTLY blocked from
   auto-approve. The CLI refuses to create such rules; the engine
   refuses to match them even if a tampered rule file says otherwise.
   `_BLOCKED_AUTO_CHANNELS = {"whatsapp", "linkedin", "phone"}`

2. **حظر مستوى الخطر | Risk block**
   `risk_level == "high"` or `"blocked"` is permanently refused.
   A rule's `max_risk_level` itself cannot exceed `medium`.

3. **توقيع HMAC إلزامي | HMAC required**
   Every rule is signed with HMAC-SHA256 using
   `DEALIX_FOUNDER_RULES_SECRET`. Without the secret the CLI exits
   non-zero (fail-closed). Any mutation invalidates the signature.

4. **انتهاء صلاحية 30 يوم | 30-day expiry**
   Default TTL is 30 days, hard cap 90 days. After expiry, a rule
   refuses to match — the founder must re-sign to extend.

## أمثلة خطوة بخطوة | Step-by-step examples

### 1. Add a rule for FAQ replies on email

```bash
export DEALIX_FOUNDER_RULES_SECRET="$(openssl rand -hex 32)"
./scripts/dealix_founder_rules.py add
# Rule name: FAQ pricing replies
# Channel: email
# Customer handle: acme-real-estate
# Action type: faq_reply
# Max risk level: low
# Min confidence: 0.92
# Content pattern regex: (?i)\bpricing\b
# TTL days: 30
# Notes: covers pricing-page FAQs only
```

The CLI prints the rule_id and `Rule signed with HMAC. Active until …`.

### 2. List active rules

```bash
./scripts/dealix_founder_rules.py list
```

Each row shows `rule_id · name · channel · enabled · expires_at · sig`
where `sig=OK` means the HMAC verifies against the current secret.

### 3. Disable a stale rule

```bash
./scripts/dealix_founder_rules.py disable rule_20260507_141622_3742
```

The store rewrites the rule with `enabled=false`. The original signed
fields are preserved so the audit chain stays intact.

### 4. Audit recent matches

```bash
./scripts/dealix_founder_rules.py audit --limit 20
```

Returns JSON of the most-recent rule matches: timestamp, rule_id,
approval_id, channel, confidence.

## نموذج جلسة CLI | Sample CLI session

```text
$ export DEALIX_FOUNDER_RULES_SECRET="…32-byte-hex…"
$ ./scripts/dealix_founder_rules.py add

== Add a founder rule (HMAC-signed) ==
ar: إضافة قاعدة موافقة مسبقة موقعة من المؤسس
Permanently blocked channels: linkedin, phone, whatsapp

Rule name (short label): FAQ pricing
Channel (email | dashboard) [email]: email
Customer handle (e.g. acme-real-estate or '*') [*]: acme-real-estate
Action type (e.g. faq_reply or '*') [faq_reply]: faq_reply
Max risk level (low | medium) [low]: low
Min confidence (0.0–1.0) [0.9]: 0.92
Content pattern regex (optional, leave empty to skip): (?i)\bpricing\b
  WARNING: regex matching can produce false positives. …
  ar: تحذير — مطابقة التعبير العادي قد تعطي نتائج غير دقيقة.
TTL days (1–90) [30]: 30
Notes (optional): pricing FAQs only

Rule created. id=rule_20260508_141622_3742
  Rule signed with HMAC. Active until 2026-06-07T14:16:22+00:00.
  Refresh required after expiry.
```

## التفاعل مع safe_send_gateway | Interaction with safe_send_gateway

A founder rule firing changes only the **approval status**
(pending → approved). It does NOT bypass `safe_send_gateway`'s six
gates. After a rule auto-approves a request, `safe_send_gateway`
still independently verifies:

1. tenant has live credentials
2. recipient consent is on file
3. throttle / cooldown windows respected
4. dedupe key not already sent
5. dry-run flag honoured in non-prod
6. audit breadcrumb persisted

Rules apply BEFORE safe_send still runs all 6 gates — they are an
optimization on the human-approval step, never a replacement for the
delivery-time safety checks.

## استكشاف الأعطال | Troubleshooting

- **Rule not matching** — check `list` output; if `sig=BAD`, the
  secret used to sign differs from the current `DEALIX_FOUNDER_RULES_SECRET`.
  Re-create the rule with the correct secret.
- **Signature failed (`sig=BAD`)** — the rule file was edited by hand,
  the secret rotated, or the rule was copied across environments.
  Re-create the rule.
- **Expired** — `expires_at` is in the past. Re-add the rule
  (`disable` first, then `add`) to refresh.
- **CLI exits with code 2 immediately** — `DEALIX_FOUNDER_RULES_SECRET`
  is not set. This is fail-closed by design.
- **Rule won't match a whatsapp/linkedin/phone request** — that is
  the rule that BLOCKS cold whatsapp / linkedin / phone outreach;
  no founder rule can override it. Use the live approval queue.

## ملاحظات أمان | Security notes

- The HMAC secret must be rotated if any team member with shell
  access leaves. Rotation invalidates all existing rules — re-add.
- Rules are stored in `data/founder_rules/active_rules.jsonl` as
  append-only JSONL (gitignored). Never edit by hand; use `disable`.
- Audit breadcrumbs land in `data/founder_rules/rule_match_audit.jsonl`.
  Ship them to your central log store on the same cadence as the
  approval audit log.
