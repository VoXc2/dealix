"use client";

import { useEffect, useState } from "react";
import { Card, CardContent, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchRunTrace } from "@/lib/api/controlPlane";

type TraceEvent = {
  node_type?: string;
  label?: string;
  occurred_at?: string;
};

interface RunTraceTimelineProps {
  customerId: string;
}

export function RunTraceTimeline({ customerId }: RunTraceTimelineProps) {
  const [events, setEvents] = useState<TraceEvent[]>([]);

  useEffect(() => {
    fetchRunTrace(customerId)
      .then((payload) => {
        const nodes = Array.isArray(payload?.nodes) ? payload.nodes : [];
        setEvents(nodes);
      })
      .catch(() => setEvents([]));
  }, [customerId]);

  return (
    <Card>
      <CardHeader>
        <CardTitle>Run Trace Timeline</CardTitle>
      </CardHeader>
      <CardContent>
        {!events.length ? (
          <p className="text-sm text-muted-foreground">No trace events yet.</p>
        ) : (
          <div className="space-y-2">
            {events.map((event, idx) => (
              <div key={`${event.occurred_at || "event"}-${idx}`} className="rounded border p-3 text-sm">
                <div><strong>type:</strong> {event.node_type || "event"}</div>
                <div><strong>label:</strong> {event.label || "-"}</div>
                <div><strong>time:</strong> {event.occurred_at || "-"}</div>
              </div>
            ))}
          </div>
        )}
      </CardContent>
    </Card>
  );
}
