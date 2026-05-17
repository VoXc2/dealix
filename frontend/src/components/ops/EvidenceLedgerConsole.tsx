"use client";

import { useEffect, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type EvidenceItem = {
  id: string;
  event_type: string;
  entity_type: string;
  entity_id: string;
  summary: string;
  created_at: string;
};

type EvidenceResponse = {
  items: EvidenceItem[];
};

export function EvidenceLedgerConsole() {
  const [items, setItems] = useState<EvidenceItem[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await api.getEvidenceEvents();
        if (!cancelled) {
          setItems(((res.data as EvidenceResponse).items ?? []).slice(0, 20));
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

  return (
    <Card>
      <CardHeader>
        <CardTitle>Evidence Ledger</CardTitle>
      </CardHeader>
      <CardContent>
        {items.length === 0 ? (
          <p className="text-sm text-muted-foreground">No evidence events yet.</p>
        ) : (
          <ul className="space-y-2">
            {items.map((item) => (
              <li key={item.id} className="rounded-lg border border-border p-3">
                <p className="text-sm font-semibold">{item.event_type}</p>
                <p className="text-xs text-muted-foreground">{item.entity_type} · {item.entity_id}</p>
                <p className="text-xs text-muted-foreground mt-1">{item.summary}</p>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

