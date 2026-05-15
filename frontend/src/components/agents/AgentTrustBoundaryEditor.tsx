"use client";

import { useState } from "react";
import { Button } from "@/components/ui/button";
import { Input } from "@/components/ui/input";

export function AgentTrustBoundaryEditor() {
  const [boundary, setBoundary] = useState("standard");
  const [message, setMessage] = useState("");

  const onSave = () => {
    setMessage(`Trust boundary saved as: ${boundary}`);
  };

  return (
    <div className="rounded border p-4 space-y-3">
      <h3 className="text-sm font-semibold">Agent Trust Boundary Editor</h3>
      <Input value={boundary} onChange={(e) => setBoundary(e.target.value)} />
      <div className="flex items-center gap-2">
        <Button size="sm" onClick={onSave}>Save</Button>
        {message && <span className="text-xs text-muted-foreground">{message}</span>}
      </div>
    </div>
  );
}
