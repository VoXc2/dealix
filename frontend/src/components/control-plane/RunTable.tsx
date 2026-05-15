"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchControlPlaneRuns } from "@/lib/api/controlPlane";

type RunRow = {
  run_id?: string;
  workflow_id?: string;
  state?: string;
  tenant_id?: string;
};

export function RunTable() {
  const [rows, setRows] = useState<RunRow[]>([]);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchControlPlaneRuns()
      .then((payload) => {
        const items = Array.isArray(payload?.runs) ? payload.runs : [];
        setRows(items);
      })
      .catch((err) => {
        setError(err?.message || "failed_to_load_runs");
      });
  }, []);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Control Plane Runs</CardTitle>
      </CardHeader>
      <CardContent>
        {error && <p className="text-sm text-red-400">{error}</p>}
        {!rows.length && !error && <p className="text-sm text-muted-foreground">No runs found.</p>}
        {!!rows.length && (
          <div className="space-y-2">
            {rows.map((row, idx) => (
              <div key={`${row.run_id || "run"}-${idx}`} className="rounded border p-3 text-sm">
                <div><strong>run_id:</strong> {row.run_id || "-"}</div>
                <div><strong>workflow_id:</strong> {row.workflow_id || "-"}</div>
                <div><strong>state:</strong> {row.state || "-"}</div>
                <div><strong>tenant_id:</strong> {row.tenant_id || "default"}</div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
