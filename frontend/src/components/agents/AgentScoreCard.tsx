"use client";

interface AgentScoreCardProps {
  trustScore?: number;
  routingScore?: number;
  complianceScore?: number;
}

export function AgentScoreCard({
  trustScore = 0.9,
  routingScore = 0.87,
  complianceScore = 0.95,
}: AgentScoreCardProps) {
  return (
    <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
      <div className="rounded border p-3 text-sm">
        <div className="font-semibold">Trust score</div>
        <div>{trustScore.toFixed(2)}</div>
      </div>
      <div className="rounded border p-3 text-sm">
        <div className="font-semibold">Routing score</div>
        <div>{routingScore.toFixed(2)}</div>
      </div>
      <div className="rounded border p-3 text-sm">
        <div className="font-semibold">Compliance score</div>
        <div>{complianceScore.toFixed(2)}</div>
      </div>
    </div>
  );
}
