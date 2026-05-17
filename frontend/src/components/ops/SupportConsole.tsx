"use client";

import { useEffect, useState } from "react";

import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { api } from "@/lib/api";

type SupportTicket = {
  id: string;
  intent: string;
  priority: string;
  risk_level: string;
  status: string;
  suggested_response: string;
  source_article_ids: string[];
  escalation_required: boolean;
  sla: string;
};

type SupportResponse = {
  items: SupportTicket[];
};

export function SupportConsole() {
  const [tickets, setTickets] = useState<SupportTicket[]>([]);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    let cancelled = false;
    async function load() {
      try {
        const res = await api.getSupportTickets();
        if (!cancelled) {
          setTickets(((res.data as SupportResponse).items ?? []).slice(0, 20));
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
        <CardTitle>Customer Service Console</CardTitle>
      </CardHeader>
      <CardContent>
        {tickets.length === 0 ? (
          <p className="text-sm text-muted-foreground">No support tickets yet.</p>
        ) : (
          <ul className="space-y-2">
            {tickets.map((ticket) => (
              <li key={ticket.id} className="rounded-lg border border-border p-3">
                <div className="flex flex-wrap items-center gap-2 text-xs mb-1">
                  <span className="rounded-full bg-muted px-2 py-0.5">{ticket.intent}</span>
                  <span className="rounded-full bg-muted px-2 py-0.5">{ticket.priority}</span>
                  <span className="rounded-full bg-muted px-2 py-0.5">{ticket.risk_level}</span>
                  <span className="rounded-full bg-muted px-2 py-0.5">{ticket.sla}</span>
                </div>
                <p className="text-sm">{ticket.suggested_response}</p>
                <p className="text-xs text-muted-foreground mt-1">
                  knowledge source: {ticket.source_article_ids.join(", ") || "none"} · escalation:{" "}
                  {ticket.escalation_required ? "required" : "not required"}
                </p>
              </li>
            ))}
          </ul>
        )}
      </CardContent>
    </Card>
  );
}

