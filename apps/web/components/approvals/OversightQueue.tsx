type QueueItem = {
  ticketId: string;
  actionType: string;
  requestedBy: string;
  state: string;
};

export function OversightQueue({ items }: { items: QueueItem[] }) {
  return (
    <div className="card">
      <h2>Oversight Queue</h2>
      <ul>
        {items.map((item) => (
          <li key={item.ticketId}>
            {item.ticketId} — {item.actionType} — {item.requestedBy} — {item.state}
          </li>
        ))}
      </ul>
    </div>
  );
}
