# self_evolving_os — System 35: Self-Evolving Enterprise Fabric

## English

Meta-learning, meta-orchestration and continuous optimization. The fabric mines
control-plane history for patterns and proposes improvements to workflows,
governance and orchestration.

It is strictly **propose-don't-execute**:

- `propose_improvement` only ever creates a proposal (status `proposed`) plus an
  approval-gate ticket.
- `apply_proposal` raises `ProposalNotApprovedError` unless that ticket has been
  granted. There is no auto-apply path — which keeps `no_unaudited_changes` and
  approval-first intact.

## العربية

تعلّم تلوي وتنسيق تلوي وتحسين مستمر. تستخرج النسيج أنماطًا من تاريخ طبقة
التحكم وتقترح تحسينات على سير العمل والحوكمة والتنسيق. المبدأ صارم: **اقترح
ولا تنفّذ** — لا يُطبَّق أي اقتراح دون تذكرة موافقة ممنوحة، ولا يوجد مسار
تطبيق تلقائي إطلاقًا.

## API

`/api/v1/self-evolving` — `POST /analyze`, `POST /proposals`, `GET /proposals`,
`GET /proposals/{id}`, `POST /proposals/{id}/apply`.
