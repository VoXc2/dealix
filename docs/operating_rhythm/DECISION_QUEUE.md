# Decision Queue

Append-only. Each entry: decision_id, type, target, evidence (required), owner, deadline, status.

Typed: `operating_rhythm_os.decision_queue.DecisionQueueEntry` rejects entries without evidence or owner.
