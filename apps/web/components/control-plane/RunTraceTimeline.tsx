type TraceEvent = {
  id: string;
  type: string;
  actor: string;
  at: string;
};

export function RunTraceTimeline({ events }: { events: TraceEvent[] }) {
  return (
    <div className="card">
      <h2>Run Trace Timeline</h2>
      <ol>
        {events.map((event) => (
          <li key={event.id}>
            <strong>{event.type}</strong> — {event.actor} — {event.at}
          </li>
        ))}
      </ol>
    </div>
  );
}
