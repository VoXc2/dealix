"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";
import { grantOversightApproval, rejectOversightApproval } from "@/lib/api/humanAi";

interface ApprovalDecisionModalProps {
  approvalId: string;
}

export function ApprovalDecisionModal({ approvalId }: ApprovalDecisionModalProps) {
  const [reason, setReason] = useState("");
  const [status, setStatus] = useState("");

  const onGrant = async () => {
    try {
      await grantOversightApproval(approvalId, "founder");
      setStatus("approved");
    } catch {
      setStatus("approval_failed");
    }
  };

  const onReject = async () => {
    try {
      await rejectOversightApproval(approvalId, "founder", reason || "rejected");
      setStatus("rejected");
    } catch {
      setStatus("reject_failed");
    }
  };

  return (
    <div className="rounded border p-4 space-y-3">
      <h3 className="text-sm font-semibold">Approval Decision</h3>
      <Input placeholder="reason (for reject)" value={reason} onChange={(e) => setReason(e.target.value)} />
      <div className="flex gap-2">
        <Button size="sm" onClick={onGrant}>Grant</Button>
        <Button size="sm" variant="outline" onClick={onReject}>Reject</Button>
      </div>
      {status && <p className="text-xs text-muted-foreground">status: {status}</p>}
    </div>
  );
}
