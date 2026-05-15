"use client";

import { useEffect, useState } from "react";
import { fetchValueReport } from "@/lib/api/valueEngine";

interface WorkflowROIReportProps {
  customerId: string;
}

export function WorkflowROIReport({ customerId }: WorkflowROIReportProps) {
  const [report, setReport] = useState<Record<string, unknown> | null>(null);

  useEffect(() => {
    fetchValueReport(customerId)
      .then((payload) => setReport(payload))
      .catch(() => setReport(null));
  }, [customerId]);

  return (
    <div className="rounded border p-4">
      <h3 className="text-sm font-semibold mb-3">Workflow ROI Report</h3>
      {!report ? (
        <p className="text-sm text-muted-foreground">No value report available.</p>
      ) : (
        <pre className="text-xs overflow-auto">{JSON.stringify(report, null, 2)}</pre>
      )}
    </div>
  );
}
