"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchOversightQueue } from "@/lib/api/humanAi";

type ApprovalItem = {
  approval_id?: string;
  action_type?: string;
  status?: string;
  customer_id?: string;
  tenant_id?: string;
};

export function OversightQueue() {
  const [items, setItems] = useState<ApprovalItem[]>([]);

  useEffect(() => {
    fetchOversightQueue()
      .then((payload) => setItems(Array.isArray(payload?.approvals) ? payload.approvals : []))
      .catch(() => setItems([]));
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Human-AI Oversight Queue</CardTitle>
      </CardHeader>
      <CardContent>
        {!items.length ? (
          <p className="text-sm text-muted-foreground">No pending approvals.</p>
        ) : (
          <div className="space-y-2">
            {items.map((item, idx) => (
              <div key={`${item.approval_id || "approval"}-${idx}`} className="rounded border p-3 text-sm">
                <div><strong>approval_id:</strong> {item.approval_id || "-"}</div>
                <div><strong>action:</strong> {item.action_type || "-"}</div>
                <div><strong>status:</strong> {item.status || "-"}</div>
                <div><strong>tenant:</strong> {item.tenant_id || "default"}</div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
