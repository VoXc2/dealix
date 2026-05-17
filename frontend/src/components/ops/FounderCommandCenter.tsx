"use client";

import { useEffect, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type FounderReport = {
  top_actions_today: string[];
  metrics: Record<string, number>;
};

export function FounderCommandCenter() {
  const [report, setReport] = useState<FounderReport | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await api.getFounderCommandCenterReport();
        if (!cancelled) {
          setReport(res.data as FounderReport);
        }
      } catch (e: unknown) {
        if (!cancelled) {
          setError(e instanceof Error ? e.message : "load_failed");
        }
      }
    }
    void load();
    return () => {
      cancelled = true;
    };
  }, []);

  if (error) {
    return <p className="text-sm text-destructive">{error}</p>;
  }

  if (!report) {
    return <p className="text-sm text-muted-foreground">Loading founder command center...</p>;
  }

  const metricRows = Object.entries(report.metrics);
  return (
    <div className="space-y-5">
      <Card>
        <CardHeader>
          <CardTitle>Top 3 actions today</CardTitle>
        </CardHeader>
        <CardContent>
          <ul className="list-disc ps-5 space-y-1 text-sm text-muted-foreground">
            {report.top_actions_today.map((action) => (
              <li key={action}>{action}</li>
            ))}
          </ul>
        </CardContent>
      </Card>

      <div className="grid grid-cols-2 lg:grid-cols-4 gap-3">
        {metricRows.map(([key, value]) => (
          <Card key={key}>
            <CardHeader className="pb-2">
              <CardTitle className="text-xs text-muted-foreground">{key}</CardTitle>
            </CardHeader>
            <CardContent>
              <p className="text-2xl font-bold">{value}</p>
            </CardContent>
          </Card>
        ))}
      </div>
    </div>
  );
}

