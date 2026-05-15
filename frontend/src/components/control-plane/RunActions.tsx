"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { requestRollback } from "@/lib/api/controlPlane";

interface RunActionsProps {
  approvalId: string;
}

export function RunActions({ approvalId }: RunActionsProps) {
  const [message, setMessage] = useState("");

  const onRollbackApprove = async () => {
    try {
      await requestRollback(approvalId, "founder");
      setMessage("Rollback request approved.");
    } catch {
      setMessage("Rollback approval request failed.");
    }
  };

  return (
    <div className="flex items-center gap-2">
      <Button size="sm" variant="outline" onClick={onRollbackApprove}>
        Request rollback approval
      </Button>
      {message && <span className="text-xs text-muted-foreground">{message}</span>}
    </div>
  );
}
