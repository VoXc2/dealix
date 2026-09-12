# Dealix Software Acquisition & Evolution Factory V2

## القرار المعتمد

هذه الطبقة **معتمدة كامتداد مباشر لـ Dealix Company Machine** وليست Company Machine أو Scheduler أو Executor أو Model Router أو Agent Fleet جديدة.

- Hermes يبقى الـorchestrator والـscheduler.
- Session Factory في #1708 يبقى executor الوحيد للـjobs.
- OpenCode يبقى engineering/research capability.
- Model Broker يبقى authority لاختيار النموذج والتكلفة.
- Company Brain / Proof Ledger / Approval Queue تبقى مصادر الحقيقة القانونية.
- عدد الـpermanent agents يبقى 5 فقط.
- `DEEP_WIP_MAX=3` يبقى ثابتًا.
- L0-L4 آلي؛ merge/deploy/root/DNS/DB/secrets/firewall/payment/send/publish تبقى L5 exact-action.

## قانون V2

لا يكفي أن تكون الأداة مفيدة أو مشهورة. كل مرشح يمر بثلاث طبقات مستقلة:

1. **Value**: هل تحرك المال، تقلل Founder Minutes، تحسن reliability/delivery أو تخفض cost؟
2. **Trust / Supply Chain**: هل المصدر والنسخة والرخصة والـSBOM والـvulnerability/provenance evidence قابلة للتحقق؟
3. **Capability / Blast Radius**: ما الصلاحيات الفعلية التي تطلبها الأداة وما أقصى أثر يمكن أن تحدثه؟

`BUSINESS_VALUE_SCORE` يرتب المرشحين فقط بعد مرور gates المطلوبة. `score != evidence` و`popularity != security`.

## المسار القانوني

```text
DISCOVER
  -> SOURCE_VERIFIED
  -> PIN_VERSION_COMMIT_OR_DIGEST
  -> PROVENANCE_CHECKED
  -> SBOM_READY
  -> VULN_PRIORITIZED
  -> LICENSE_CHECKED
  -> CAPABILITY_MAPPED
  -> STRICT_SANDBOX
  -> ACCEPTANCE
  -> CANARY
  -> 7D_REVIEW
  -> 30D_REVIEW
  -> PROMOTE | KEEP_CANARY | DEMOTE | KILL | QUARANTINE
```

Internet Scout ينتج عقد V2 نفسه الذي يستهلكه Software Acquisition Factory؛ لا توجد طبقة V1 جديدة بين الاكتشاف والقرار.

## Evidence confidence منفصل عن Value score

`AUTO_SANDBOX` يحتاج شرطين معًا:

- Value score >= 80.
- Evidence confidence >= 80.

Evidence confidence يغطي: official source، immutable pin، verified license، fresh vulnerability evidence، rollback، evidence refs، SBOM، provenance، capability map.

إذا كانت القيمة عالية لكن الأدلة ناقصة: `RESEARCH_MORE`، وليس auto-execute.

## Supply-chain gates

- OSV/Trivy: إثبات أن dependency/image متأثر فعليًا.
- CISA KEV match: `QUARANTINE_KEV`.
- FIRST EPSS: prioritization signal فقط، وليس risk score كاملًا.
- HIGH/CRITICAL unresolved exposure: fail closed حتى يظهر exact-version remediation/non-applicability evidence.
- unknown license: `HOLD_LICENSE`.
- invalid/suspicious signature or provenance: `QUARANTINE`.
- missing rollback: `HOLD_ROLLBACK`.
- duplicate capability: `REJECT_DUPLICATE`، إلا إذا كان `replacement_of_existing` صريحًا لنفس الـcapability.

للـexecutables/container images/MCP servers/agent runtimes/installers/system services، provenance الموثق مطلوب. `NOT_APPLICABLE` لا يتجاوز هذا gate.

## Capability / Blast Radius gates

لا تدخل الصلاحيات الخطرة داخل weighted score. الحالات التالية تمنع auto-execution:

- privileged/root execution.
- host Docker socket.
- host network.
- unrestricted network egress.
- broad host filesystem writes.
- broad secret/environment access.
- kernel/device access.
- firewall mutation.
- production DB/DNS/deploy/root/secret effects.

النتيجة تكون `HOLD_CAPABILITY_RISK` أو `L5_REQUIRED` أو `QUARANTINE` حسب الحالة.

## AI / MCP / Agent candidates

أي MCP server أو browser/coding agent أو agent runtime أو AI execution tool يجب أن يسجل:

- tool/capability inventory.
- auth scopes.
- process/command execution ability.
- filesystem reach.
- network destinations.
- data retention and telemetry.
- untrusted-content / prompt-injection boundary.
- credential/secret visibility.
- هل material actions تحتاج human/L5 confirmation فعليًا.

Unknown capability scope للمرشح عالي الخطورة => `HOLD_CAPABILITY_RISK`.

## Strict sandbox

هناك فرق دستوري مهم:

`git worktree isolation != OS/process sandbox`.

الـworktree يمنع تداخل كتابات Git فقط. تشغيل كود مرشح غير موثوق يحتاج structural sandbox evidence. الوضع الافتراضي:

- non-root/rootless حيثما أمكن.
- no privileged mode.
- no host Docker socket.
- no host network.
- preserve seccomp + AppArmor/SELinux/MAC controls.
- drop unneeded capabilities.
- host inputs read-only.
- writable worktree/tmp معزول فقط.
- no secrets mounted by default.
- egress denied أو destination-allowlisted.
- CPU/RAM/PID/time/disk limits.
- ephemeral deterministic cleanup.
- exact artifact digest داخل receipt.

إذا لم يمكن إثبات structural sandbox المناسب، لا يشغّل العامل candidate code على الـhost؛ يقتصر على research/static inspection ويصدر HOLD بدل صناعة PASS وهمي.

## Source hierarchy

1. official project/vendor docs/repository/release metadata.
2. signed provenance/SBOM/security metadata.
3. authoritative vulnerability sources: OSV، CISA KEV، FIRST EPSS كإشارة prioritization.
4. OpenSSF Scorecard / Security Insights.
5. third-party commentary للاكتشاف التكميلي فقط.

السجل الرسمي يشمل كذلك GitHub Dependency Review / Artifact Attestations، Docker isolation guidance، CycloneDX/SPDX، Cosign/SLSA، Renovate، Crawl4AI، changedetection.io، OpenTelemetry، Uptime Kuma، OpenCode، Hermes، Ollama وMCP.

هذه مصادر/مرشحون، وليست install allowlist.

## Session Factory handoff

`software_acquisition_factory.py` لا ينفذ installer أو downloader بنفسه. عند `AUTO_SANDBOX` يصنع bounded `ENGINEERING/L4` job ويرسله إلى `make_job()/submit_job()` في #1708.

الـjob contract يفرض no merge/deploy/root/DNS/DB/secrets/firewall/send/publish/pay، ويطلب strict sandbox + evidence-backed acceptance. أي أثر إنتاجي لاحق يبقى parked في L5.

`software_evolution_tick.py` يصنع حتى 3 scout jobs وحتى 3 candidate jobs في الدورة. لا ينشئ scheduler ولا worker loop جديدًا.

## 7/30-day evolution loop

### 7 أيام — canary survival

يقاس فقط بدليل مرصود:

- job success rate.
- founder minutes saved.
- cash/resource cost.
- maintenance burden.
- security incidents.
- policy incidents.
- unexpected data-egress incidents.
- evidence refs.

نتائج محتملة: `KEEP_CANARY / DEMOTE / QUARANTINE / HOLD_MEASURE`.

### 30 يومًا — promotion gate

`PROMOTE` يتطلب جميع الآتي:

- persistent verified benefit.
- acceptable reliability/maintenance.
- no unresolved KEV/HIGH/CRITICAL exposure.
- zero security/policy/unexpected-egress incidents.
- rollback tested + rollback evidence refs.
- no duplicate stack creep.
- explicit economic reason to keep.

إذا توجد تكلفة بلا فائدة موثقة: `KILL`. إذا ارتفع الخطر: `QUARANTINE`. sunk cost ليس سببًا للإبقاء.

## GitHub / dependency controls

عند توفر خصائص المستودع/الخطة:

- Dependency Review يمنع vulnerable dependency additions في PRs.
- Artifact Attestations/Provenance تستخدم عند ملاءمتها.
- OpenSSF Scorecard/Security Insights inputs وليست trust substitute.
- GitHub job بـ`steps=[]` أو `runner_id=0` يصنف `HOSTED_EXECUTION_PLANE_BLOCKED`، لا Source PASS ولا Source FAIL.

## Hermes scheduling contract

لا Scheduler ثانٍ. بعد توفر authorized runtime channel يضاف إلى Hermes فقط:

```bash
python3 scripts/ops/software_evolution_tick.py \
  --base-sha "$PINNED_RUNTIME_SHA" \
  --max-scouts 3 \
  --max-candidate-jobs 3

python3 scripts/ops/software_benefit_review.py --window-days 7
python3 scripts/ops/software_benefit_review.py --window-days 30
```

المقترح:

- evolution tick: كل 6 ساعات، no-agent/script orchestration.
- 7d review: يوميًا، deterministic/zero-token.
- 30d review: يوميًا، deterministic/zero-token.
- #1708 watchdog يبقى العامل الوحيد للـREADY jobs.

## Operating boards

| Board | Entry |
|---|---|
| Strategy Backlog | Governed software acquisition/evolution over #1708 |
| Action Queue | scout -> evidence/capability gates -> strict sandbox -> acceptance -> review |
| Approval Queue | L5-only production/root/DNS/DB/secret/firewall promotion |
| Opportunity Graph | software research لا ينشئ customer opportunity |
| Proof Ledger | acceptance + provenance/security + 7/30d benefit receipts |
| Self Improvement | failures/gates/benchmarks feed research/demote/kill rules |
| Contacts Radar | لا consent أو relationship مشتق من software research |

## Acceptance V2

يجب أن يشمل exact-head Linux acceptance على الأقل:

```bash
pytest tests/test_software_acquisition_factory.py \
       tests/test_software_acquisition_factory_v2_edges.py \
       tests/test_software_evolution_tick.py \
       tests/test_software_benefit_review.py -q
python3 -m py_compile \
  scripts/ops/software_acquisition_factory.py \
  scripts/ops/software_evolution_tick.py \
  scripts/ops/software_benefit_review.py
git diff --check
ruff check \
  scripts/ops/software_acquisition_factory.py \
  scripts/ops/software_evolution_tick.py \
  scripts/ops/software_benefit_review.py \
  tests/test_software_acquisition_factory.py \
  tests/test_software_acquisition_factory_v2_edges.py \
  tests/test_software_evolution_tick.py \
  tests/test_software_benefit_review.py
```

الـ`12 passed` القديم يعود إلى V1 head `8e923552...` فقط ولا يصلح merge authority لـV2.

حتى يصدر fresh exact-head V2 receipt، يبقى PR Draft.

## Runtime activation status

Repo policy/code V2 معتمد على فرع #1714، لكن VPS pin / Hermes cron activation غير مدعى اكتماله. لا يتم اختلاق runtime activation بلا authorized access.

`L5_EXECUTED=NONE`.
