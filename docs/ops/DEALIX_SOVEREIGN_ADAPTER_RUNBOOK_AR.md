# Dealix Sovereign VPS Adapter — Runbook

## القرار

`#1264` هو **العقد الوحيد للتحقق** (`bin/dealix verify ...`).

هذا الـadapter لا يملك اختبارات ولا سياسات تحقق خاصة به. وظيفته فقط:

1. تحديث checkout مخصص للأداة تحت `/opt/dealix/sovereign-ci/tool-repo`.
2. جلب SHA دقيق لـ`main` أو PR موثوق.
3. استدعاء العقد canonical من #1264.
4. تخزين receipts خارج Git.
5. نشر commit status محدود على GitHub بدون GitHub Actions.
6. جدولة source/PR checks وtrusted runtime/production/commercial checks بشكل منفصل.

هذا يمنع ظهور محركي تحقق متنافسين.

## ترتيب الاعتماد

```text
#1264 canonical verifier
       |
       v
stacked sovereign adapter PR
       |
       v
VPS systemd polling/status adapter
```

يجب دمج #1264 قبل تفعيل adapter على `TOOL_REF=main`.

## حدود v1 الأمنية

v1 هو **Trusted Internal PR Verification Only**.

يسمح تلقائيًا فقط عندما:

- PR من نفس `Dealix-sa/dealix`؛ و
- `author_association` هو `OWNER` أو `MEMBER` أو `COLLABORATOR`.

أي fork أو مساهم غير موثوق لا يتم تشغيل كوده على VPS المؤسس.

السبب: الـadapter نفسه يحتاج هوية GitHub للجلب وكتابة status. بيئة child verifier تُنظف من HOME/config/credentials، لكن الفصل الكامل بين Fetcher/Runner/Reporter يبقى Definition of Done لـIssue #1266 قبل أي untrusted execution.

## Trust lanes

### Source / PR lane

يستدعي فقط أوضاع #1264 التي يسمح بها exact SHA:

```bash
bin/dealix verify trust --sha <sha>
bin/dealix verify pr --sha <sha>
```

ولا يشغّل runtime أو production على PR SHA.

### Trusted runtime lane

```bash
bin/dealix verify runtime
```

يخص current trusted checkout/runtime فقط.

### Production probe lane

```bash
bin/dealix verify production
```

read-only HTTP probes فقط.

### Commercial verification lane

```bash
bin/dealix verify commercial
```

يفحص truth/adapter logic فقط ولا يرسل أي outbound.

## GitHub status contexts

- `dealix/sovereign-source`
- `dealix/sovereign-pr`
- `dealix/sovereign-runtime`
- `dealix/sovereign-production`
- `dealix/sovereign-commercial`

Mapping:

- PASS -> success
- FAIL -> failure
- BLOCKED_EXPECTED -> pending
- invalid/missing receipt -> error

هذه ليست شهادة بأن GitHub-hosted Actions green.

## Resource policy

الـVPS يحمل Ollama/OpenClaw/Hermes/n8n وCompany OS، لذلك:

- heavy concurrency فعليًا 1 عبر `flock`؛
- poller CPUQuota=200%, MemoryHigh=5G, MemoryMax=6G؛
- trusted cycle CPUQuota=150%, MemoryHigh=4G, MemoryMax=5G؛
- إذا `load1 > 2.75` أو `MemAvailable < 4096MB` فالنتيجة `BLOCKED_EXPECTED` ولا تتم التضحية بخدمات الشركة.

## التثبيت

بعد دمج #1264 ثم adapter PR إلى `main` ومراجعة التغيير:

```bash
sudo bash scripts/ops/install_dealix_sovereign_adapter.sh
```

ثم:

```bash
sudo -iu dealix /usr/bin/python3 /opt/dealix/control/bin/dealix_sovereign_adapter.py doctor
systemctl list-timers 'dealix-sovereign-*' --no-pager
```

## اختبار قبل الدمج عبر stacked branch

يمكن مؤقتًا تشغيل adapter مع:

```bash
DEALIX_SOVEREIGN_TOOL_REF=ops/sovereign-verify-contract
```

لا تجعل هذا ref إعداد production دائمًا؛ بعد merge يصبح `main` المالك.

## Acceptance sequence

1. doctor.
2. source verify لـmain.
3. PR #1261 exact-SHA PR verify.
4. PR #1260 exact-SHA PR verify.
5. trusted runtime cycle.
6. production read-only cycle.
7. commercial verification.
8. التأكد أن receipts/status SHA متطابقة.
9. مراقبة resource impact.

## Rollback

الـinstaller ينشئ backup تحت `/root/dealix-sovereign-adapter-<timestamp>`.

```bash
sudo systemctl disable --now dealix-sovereign-adapter.timer dealix-sovereign-trusted.timer
sudo rm -f /etc/systemd/system/dealix-sovereign-adapter.service \
  /etc/systemd/system/dealix-sovereign-adapter.timer \
  /etc/systemd/system/dealix-sovereign-trusted.service \
  /etc/systemd/system/dealix-sovereign-trusted.timer
sudo systemctl daemon-reload
```

ثم استرجع الملفات من backup عند الحاجة.

## ما لا يفعله هذا النظام

- لا merge إلى main.
- لا production deploy.
- لا Railway mutation.
- لا DNS/DB/secrets mutation.
- لا payment.
- لا external customer send.
- لا self-hosted GitHub Actions runner.
- لا Woodpecker/Dagger/Forgejo control plane جديد.

## المرحلة التالية

بعد ثبات v1:

1. أكمل #1266 لفصل Fetcher / credential-free Runner / Reporter إذا ظهرت حاجة فعلية لتشغيل untrusted/fork code.
2. اربط `!dealix verify` في #1119 بهذا العقد بدل queue جديدة.
3. لا تجعل sovereign CI مشروعًا دائم التوسع؛ ارجع مباشرة إلى Revenue / Customer / Proof.
4. اجعل hosted Actions second opinion عندما تعود السعة.
