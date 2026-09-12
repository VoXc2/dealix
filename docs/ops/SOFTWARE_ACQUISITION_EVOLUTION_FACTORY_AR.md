# Dealix Software Acquisition & Evolution Factory

## القرار المعتمد

هذه الطبقة **معتمدة كامتداد لـ Dealix Company Machine** وليست شركة أو Scheduler أو Agent Fleet جديدة.

- Hermes يبقى الـorchestrator والـscheduler.
- Session Factory في #1708 يبقى executor الوحيد للـjobs.
- OpenCode يبقى engineering/research factory.
- Model Broker يبقى authority لاختيار النموذج والتكلفة.
- Company Brain / Proof Ledger / Approval Queue تبقى المصادر القانونية للحقيقة.
- عدد الـpermanent agents يبقى 5 فقط.
- `DEEP_WIP_MAX=3` يبقى ثابتًا.

## مسار التشغيل

```text
Official/Public Internet
  -> Internet Scout (bounded RESEARCH jobs)
  -> Candidate Registry
  -> Contract validation
  -> Value + Security + Maturity + Maintenance + Fit + License + Cost + Reversibility score
  -> hard gates
  -> AUTO_SANDBOX | RESEARCH_MORE | HOLD/REJECT/QUARANTINE
  -> canonical Session Factory
  -> isolated worktree/sandbox
  -> OpenCode research/engineering
  -> acceptance receipt
  -> draft-safe integration only
  -> 7-day review
  -> 30-day review
  -> PROMOTE | KEEP_CANARY | DEMOTE | KILL | QUARANTINE
```

## قاعدة الإنترنت

الإنترنت مصدر اكتشاف، وليس مصدر ثقة. يمنع تحويل نتيجة بحث أو رابط أو repository إلى install مباشر بلا تحقق.

التسلسل الإلزامي:

`DISCOVER -> OFFICIAL_SOURCE -> PIN_VERSION/COMMIT/DIGEST -> VERIFY_PROVENANCE -> SBOM -> CVE -> LICENSE -> SANDBOX -> TEST -> BENCHMARK -> DRAFT_INTEGRATION -> BENEFIT_REVIEW`

لا يوجد `curl random | sudo bash`، ولا root installer عشوائي، ولا secret dump.

## Scoring

| العامل | الوزن |
|---|---:|
| Business value | 30% |
| Security | 20% |
| Maturity | 15% |
| Maintenance | 10% |
| Integration fit | 10% |
| License | 5% |
| Cost | 5% |
| Reversibility | 5% |

- `>=80`: `AUTO_SANDBOX` إذا مرت hard gates.
- `65..79.99`: `RESEARCH_MORE`.
- `<65`: `REJECT_LOW_VALUE`.

Hard gates: critical vulnerability, unknown license, duplicate capability, secret-dump requirement, invalid/suspicious signature, or missing rollback path.

## Installation authority

| Surface | Authority |
|---|---|
| dependency inside sandbox | L3 internal |
| container/sidecar sandbox | L3 internal |
| loopback canary | L4 repo/canary |
| repo integration / draft PR | L4 |
| production/root/DNS/DB/secret/firewall | L5 required |

حتى إذا كان المرشح النهائي يحتاج L5، البحث والـsandbox والbenchmark والـdraft integration تستمر تلقائيًا حتى آخر خطوة آمنة، ثم تقف قبل الأثر الخارجي.

## Tool discovery seeds

السجل `config/company/software_acquisition_sources.json` يوجّه الـInternet Scout إلى المصادر الرسمية أولًا في المجالات التالية:

- dependency automation: Renovate.
- software supply chain: OpenSSF Scorecard, OSV-Scanner, Trivy, Cosign, SLSA.
- SBOM/provenance: CycloneDX, SPDX.
- internet intelligence: Crawl4AI, changedetection.io.
- observability: OpenTelemetry Collector, Uptime Kuma.
- agent engineering: OpenCode, Hermes, Ollama.

هذه أسماء مرشحين/مصادر بحث، وليست تصريح install مسبق. كل أداة تمر بنفس gates.

## Existing Session Factory handoff

`software_acquisition_factory.py` لا ينفذ installer بنفسه. عند `AUTO_SANDBOX` يصنع `ENGINEERING/L4` job باستخدام `make_job()` ثم يرسله عبر `submit_job()` للـSession Factory. Acceptance يتطلب `exit_zero` + marker receipt محدد.

`software_evolution_tick.py` يصنع حتى 3 Internet Scout jobs في الدورة، ثم حتى 3 candidate jobs، مع بقاء التنفيذ الفعلي تحت Resource Governor والـleases والـworktrees الخاصة بـ#1708.

## Benefit loop

`software_benefit_review.py` يقيم النتائج المرصودة فقط:

- founder minutes saved.
- cash saved / cash cost.
- job success rate.
- maintenance minutes.
- security incidents.
- evidence refs.

بعد 7 أيام: `KEEP_CANARY`, `DEMOTE`, `QUARANTINE`, أو `HOLD_MEASURE`.

بعد 30 يومًا: يمكن `PROMOTE` أو `KILL` إذا كانت الأدلة كافية. أي claim بلا evidence refs لا يحسب verified value.

## Hermes scheduling contract

لا يتم إنشاء scheduler ثانٍ. عند توفر runtime access، يضاف إلى Hermes فقط:

```bash
# deterministic/no-agent intake + scout enqueue
python3 scripts/ops/software_evolution_tick.py \
  --base-sha "$PINNED_RUNTIME_SHA" \
  --max-scouts 3 \
  --max-candidate-jobs 3

# evidence-only benefit reviews
python3 scripts/ops/software_benefit_review.py --window-days 7
python3 scripts/ops/software_benefit_review.py --window-days 30
```

التردد المقترح داخل Hermes:

- evolution tick: كل 6 ساعات، no-agent script mode.
- 7-day benefit review: يوميًا، لأن كل candidate يحمل عمره/أدلته ويُراجع فقط عندما ينطبق window.
- 30-day benefit review: يوميًا بنفس المنطق، zero-token.

Session Factory watchdog الموجود يبقى هو الذي يشغل الـREADY jobs؛ لا نضيف worker loop جديد.

## Operating-board projection

| Board | Entry |
|---|---|
| Strategy Backlog | Governed software acquisition/evolution over existing Session Factory |
| Action Queue | Internet scout -> evidence gate -> sandbox -> acceptance -> benefit review |
| Approval Queue | L5-only production/root/DNS/DB/secret/firewall promotion |
| Opportunity Graph | لا يتم إنشاء opportunity من software research |
| Proof Ledger | acceptance receipts + 7/30-day observed benefit evidence |
| Self Improvement | failed candidates/gates/benchmarks feed kill/demote/research rules |
| Contacts Radar | لا علاقة لهذه الطبقة بإنشاء consent/relationship |

## Acceptance

Focused suite:

```bash
pytest tests/test_software_acquisition_factory.py \
       tests/test_software_evolution_tick.py \
       tests/test_software_benefit_review.py -q
python3 -m py_compile \
  scripts/ops/software_acquisition_factory.py \
  scripts/ops/software_evolution_tick.py \
  scripts/ops/software_benefit_review.py
git diff --check
```

Device V exact-head acceptance on 2026-09-12: `12 passed` plus Python compile and `git diff --check` PASS.

## Runtime activation status

Repository implementation and Device V acceptance are complete. Direct non-interactive SSH from Device V to `root@100.103.59.11` and `dealix@100.103.59.11` is not authorized by the local keychain, so VPS runtime pin / Hermes cron activation was **not claimed as completed** from this lane.

Activation remains L0-L4 operational work once an authorized runtime channel is available. No merge/deploy/DNS/DB/secret/send/publish/payment action is performed by this factory.
