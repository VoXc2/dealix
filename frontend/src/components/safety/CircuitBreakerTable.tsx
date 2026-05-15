"use client";

const mockBreakers = [
  { key: "whatsapp.send_message", failures: 3, threshold: 3, is_open: true },
  { key: "crm.update_deal", failures: 1, threshold: 3, is_open: false },
];

export function CircuitBreakerTable() {
  return (
    <div className="rounded border p-4">
      <h3 className="text-sm font-semibold mb-3">Circuit Breakers</h3>
      <div className="space-y-2">
        {mockBreakers.map((row) => (
          <div key={row.key} className="rounded border p-3 text-sm">
            <div><strong>key:</strong> {row.key}</div>
            <div><strong>failures:</strong> {row.failures}/{row.threshold}</div>
            <div><strong>open:</strong> {String(row.is_open)}</div>
          </div>
        ))}
      </div>
    </div>
  );
}
