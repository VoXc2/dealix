"use client";

import { useEffect, useState } from "react";
import { fetchWeeklyLearning } from "@/lib/api/selfEvolving";

type Proposal = {
  area?: string;
  suggestion_en?: string;
  action_mode?: string;
};

export function ImprovementProposalTable() {
  const [rows, setRows] = useState<Proposal[]>([]);

  useEffect(() => {
    fetchWeeklyLearning()
      .then((payload) => {
        setRows(Array.isArray(payload?.suggestions) ? payload.suggestions : []);
      })
      .catch(() => setRows([]));
  }, []);

  return (
    <div className="rounded border p-4">
      <h3 className="text-sm font-semibold mb-3">Improvement Proposals (Propose-only)</h3>
      {!rows.length ? (
        <p className="text-sm text-muted-foreground">No proposals available.</p>
      ) : (
        <div className="space-y-2">
          {rows.map((row, idx) => (
            <div key={`${row.area || "proposal"}-${idx}`} className="rounded border p-3 text-sm">
              <div><strong>area:</strong> {row.area || "-"}</div>
              <div><strong>suggestion:</strong> {row.suggestion_en || "-"}</div>
              <div><strong>mode:</strong> {row.action_mode || "propose_only"}</div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
