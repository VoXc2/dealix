"use client";

import { useEffect, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type StageRow = { stage: string; count: number };
type PipelinePayload = { stages: StageRow[] };

export function SalesPipelineConsole() {
  const [data, setData] = useState<PipelinePayload | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await api.getSalesPipelineOps();
        if (!cancelled) {
          setData(res.data as PipelinePayload);
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
  if (!data) {
    return <p className="text-sm text-muted-foreground">Loading sales pipeline...</p>;
  }

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
      {data.stages.map((stage) => (
        <Card key={stage.stage}>
          <CardHeader className="pb-2">
            <CardTitle className="text-sm">{stage.stage}</CardTitle>
          </CardHeader>
          <CardContent>
            <p className="text-2xl font-bold">{stage.count}</p>
          </CardContent>
        </Card>
      ))}
    </div>
  );
}

