"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function KillSwitchPanel() {
  const [targetId, setTargetId] = useState("sales_agent");
  const [status, setStatus] = useState("inactive");

  return (
    <div className="rounded border p-4 space-y-3">
      <h3 className="text-sm font-semibold">Kill Switch Panel</h3>
      <Input value={targetId} onChange={(e) => setTargetId(e.target.value)} />
      <div className="flex items-center gap-2">
        <Button size="sm" variant="destructive" onClick={() => setStatus(`active:${targetId}`)}>
          Engage kill switch
        </Button>
        <span className="text-xs text-muted-foreground">status: {status}</span>
      </div>
    </div>
  );
}
